import zipfile, os

def zipdir(path, zipname):
    zipf = zipfile.ZipFile(zipname,'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

