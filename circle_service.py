from pydocumentdb import document_client
from azure.storage.blob import BlockBlobService, PublicAccess
import json
from circles import get_circles
import os

creds = json.load(open('/etc/hackathon/creds.json'))


block_blob_service = BlockBlobService(account_name=creds['blobacct'], account_key=creds['blobkey'])
container_name='photos'
generator = block_blob_service.list_blobs(container_name)

for blob in generator:
    if blob.name.lower().endswith('png') or blob.name.lower().endswith('jpg') or blob.name.lower().endswith('jpeg'):
        print("\t Blob name: " + blob.name)
        full_path_to_file2 = "/tmp/%s" % blob.name
        print("\nDownloading blob to " + full_path_to_file2)
        block_blob_service.get_blob_to_path(container_name, blob.name, full_path_to_file2)
        filen = blob.name.split("/")[-1].replace(".","_")
        foldername = "/tmp/%s" % filen
        try:
            if not os.path.isdir(foldername):
                os.mkdir(foldername)
            get_circles(full_path_to_file2, foldername)
        except:
            print("[-] unable to create folder: %s" % foldername)