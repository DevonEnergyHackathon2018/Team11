from circles import get_circles
import os
import sys

if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
        filen = filename.split("/")[-1].replace(".","_")
        foldername = "./circles/%s" % filen
        try:
            if not os.path.isdir(foldername):
                os.mkdir(foldername)
            get_circles(filename, foldername)
        except:
            print("[-] unable to create folder: %s" % foldername)