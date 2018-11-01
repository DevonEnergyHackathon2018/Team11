from azure.storage.blob import BlockBlobService, PublicAccess
import os
import requests
import json
import logging
import datetime
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

if __name__ == "__main__":
    logfile = "/var/log/drillbit-logs/log-%s.log" % datetime.datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(filename=logfile,level=logging.INFO)
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
        logging.critical("[---] you need to have the right evironment variables")
        exit()
    
    sh = SecretHelper(client_id=appid, secret=key, tenant=tenant, resource=resource)
    block_blob_service = BlockBlobService(account_name=sh.get_secret(vbu, "blobaccount").value, account_key=sh.get_secret(vbu, "blobkey").value)
    container_name='photos'
    status = json.load(open('/opt/drillbit/status.json'))
    while True:
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            if blob.name.lower().endswith('png') or blob.name.lower().endswith('jpg') or blob.name.lower().endswith('jpeg'):
                if not blob.name in status:
                    stripped_name = blob.name.split("/")[-1]
                    filen = stripped_name.replace(".","_")
                    foldername = "/opt/drillbit/cache/%s" % filen
                    try:
                        if not os.path.isdir(foldername):
                            os.mkdir(foldername)
                    except:
                        logging.error("[-] unable to create folder: %s" % foldername)
                    extent = blob.name.split(".")[-1]
                    full_path_to_file2 = "%s/original.%s" % (foldername , extent)
                    block_blob_service.get_blob_to_path(container_name, blob.name, full_path_to_file2)
                    try:
                        if get_circles(full_path_to_file2, foldername):
                            upload_circles(foldername, block_blob_service)
                            circle_predictions = predict_circles(sh.get_secret(vbu, "apiurl").value, sh.get_secret(vbu, "apikey").value, foldername)
                            irm = interpret_results(blob.name, circle_predictions)
                            json.dump(circle_predictions, open(foldername+"/predictions.json","w"))
                            teams_message(irm['message'], sh.get_secret(vbu, "teamshook").value, irm['colour'], "%s/%s/original.%s" % (sh.get_secret(vbu, "webblob").value,foldername.split("/")[-1], extent))
                        else:
                            teams_message("NOT DRILLBIT. probable data quality issues with %s" % blob.name, sh.get_secret(vbu, "teamshook").value,"800080", "%s/%s/original.%s" % (sh.get_secret(vbu, "webblob").value,foldername.split("/")[-1], extent))         
                        status[blob.name]=foldername
                        json.dump(status,open('/opt/drillbit/status.json','w'))
                        logging.info("[+] processed: %s" % blob.name)
                    except:
                        logging.error("[-] erroring when trying to find circles: %s" % blob.name)
                        teams_message("processing issues with %s" % blob.name, sh.get_secret(vbu, "teamshook").value,"800080")
                        raise

                else:
                    logging.error("[*] already processed: %s" % blob.name)