from azure.storage.blob import BlockBlobService, PublicAccess
import json
from circles import get_circles
import os

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
                if not os.path.isdir(foldername):
                    os.mkdir(foldername)
                extent = blob.name.split(".")[-1]
                full_path_to_file2 = "%s/original.%s" % (foldername , extent)
                block_blob_service.get_blob_to_path(container_name, blob.name, full_path_to_file2)
                try:
                    get_circles(full_path_to_file2, foldername)
                    status[blob.name]=foldername
                    json.dump(status,open('/etc/hackathon/status.json','w'))
                    print("[+] processed: %s" % blob.name)
                except:
                    print("[-] unable to create folder: %s" % foldername)
            else:
                print("[*] already processed: %s" % blob.name)