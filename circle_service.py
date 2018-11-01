from azure.storage.blob import BlockBlobService, PublicAccess
import os
import requests
import json
from circles import get_circles
from circle_predictor import predict_circles, interpret_results
from teams_helper import teams_message
from secret_helper import SecretHelper



def upload_circles(folder, bbService):
    """uploads files from a folder to blob"""
    for filename in os.listdir(folder):
        fname = folder.split("/")[-1]
        blob_path_to_file = "%s/%s" % (fname, filename)
        full_path_to_file = "%s/%s" % (folder, filename)
        bbService.create_blob_from_path("circles", blob_path_to_file, full_path_to_file)
        if filename.startswith("original."):
            bbService.create_blob_from_path("$web", blob_path_to_file, full_path_to_file)


def send_flow(flowurl, message):
    """sends a request to get a flow going"""
    try:
        resp = requests.post(url=flowurl, json=message)
        if resp.status_code == 202:
            print("[+] successfully sent flow")
    except:
        print("[-] issues with flow")

if __name__ == "__main__":
    if "APPID" in os.environ:
        appid = os.environ["APPID"]
    if "TENANT" in os.environ:
        tenant = os.environ["TENANT"]
    if "APPKEY" in os.environ:
        key = os.environ["APPKEY"]
    if "RESOURCE" in os.environ:
        resource = os.environ["RESOURCE"]
    if "VAULT" in os.environ:
        vbu = "https://%s.vault.azure.net" % os.environ["VAULT"]
    if not(appid and tenant and key and resource):
        print("[---] you need to have the right evironment variables")
        exit()
    
    sh = SecretHelper(client_id=appid, secret=key, tenant=tenant, resource=resource)
    block_blob_service = BlockBlobService(account_name=sh.get_secret(vbu, "blobaccount").value, account_key=sh.get_secret(vbu, "blobkey").value)
    container_name='photos'
    status = json.load(open('/etc/hackathon/status.json'))
    while True:
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            if blob.name.lower().endswith('png') or blob.name.lower().endswith('jpg') or blob.name.lower().endswith('jpeg'):
                if not blob.name in status:
                    stripped_name = blob.name.split("/")[-1]
                    filen = stripped_name.replace(".","_")
                    foldername = "/tmp/%s" % filen
                    try:
                        if not os.path.isdir(foldername):
                            os.mkdir(foldername)
                    except:
                        print("[-] unable to create folder: %s" % foldername)
                    extent = blob.name.split(".")[-1]
                    full_path_to_file2 = "%s/original.%s" % (foldername , extent)
                    block_blob_service.get_blob_to_path(container_name, blob.name, full_path_to_file2)
                    try:
                        if get_circles(full_path_to_file2, foldername):
                            upload_circles(foldername, block_blob_service)
                            circle_predictions = predict_circles(sh.get_secret(vbu, "apiurl").value, sh.get_secret(vbu, "apikey").value, foldername)
                            irm = interpret_results(blob.name, circle_predictions)
                            json.dump(circle_predictions, open(foldername+"/predictions.json","w"))
                            teams_message(irm['message'],sh.get_secret(vbu, "teamshook").value,irm['colour'], "%s/%s/original.%s" % (sh.get_secret(vbu, "webblob").value,foldername.split("/")[-1], extent))
                        else:
                            teams_message("NOT DRILLBIT. probable data quality issues with %s" % sh.get_secret(vbu, "teamshook").value,"800080", "%s/%s/original.%s" % (sh.get_secret(vbu, "webblob").value,foldername.split("/")[-1], extent))         
                        status[blob.name]=foldername
                        json.dump(status,open('/etc/hackathon/status.json','w'))
                        print("[+] processed: %s" % blob.name)
                    except:
                        print("[-] erroring when trying to find circles: %s" % blob.name)
                        teams_message("processing issues with %s" % blob.name, sh.get_secret(vbu, "teamshook").value,"800080")
                        raise

                else:
                    print("[*] already processed: %s" % blob.name)