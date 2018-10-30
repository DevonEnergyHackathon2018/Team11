from azure.storage.blob import BlockBlobService, PublicAccess
import json
from circles import get_circles
import os


def upload_circles(folder, bbService):
    """uploads files from a folder to blob"""
    for filename in os.listdir(folder):
        fname = folder.split("/")[-1]
        blob_path_to_file = "%s/%s" % (fname, filename)
        full_path_to_file = "%s/%s" % (folder, filename)
        bbService.create_blob_from_path("circles", blob_path_to_file, full_path_to_file)

creds = json.load(open('/etc/hackathon/creds.json'))

block_blob_service = BlockBlobService(account_name=creds['blobacct'], account_key=creds['blobkey'])
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
                    get_circles(full_path_to_file2, foldername)
                    upload_circles(foldername, block_blob_service)
                    status[blob.name]=foldername
                    json.dump(status,open('/etc/hackathon/status.json','w'))
                    print("[+] processed: %s" % blob.name)
                except:
                    print("[-] unable to find circles")                
            else:
                print("[*] already processed: %s" % blob.name)