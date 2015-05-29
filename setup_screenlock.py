import sys, time, os, zipfile
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(path, "source"))

from distutils.core import setup
import py2exe
import shutil

# def zipdir(path, zipfile):
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             zipfile.write(os.path.join(root, file))

def zipdir(foldersToZip, zipfile):
    for folder in foldersToZip:
        for root, dirs, files in os.walk(folder):
            for file in files:
                zipfile.write(os.path.join(root, file))

version = sys.argv[2]
del sys.argv[2:]

newFolder = os.path.join(path, 'Tags', version)
if os.path.isdir(newFolder):
    shutil.rmtree(newFolder)
os.makedirs(newFolder)

setup (console=['source\screenlockApp.py'])
setup (console=['source\setAdminPassword.py'])
time.sleep(5)

src = os.path.join(path, 'source', 'config.ini')
os.rename( os.path.join(path, 'dist'), os.path.join(path, 'screenlock') )
dst =  os.path.join(path, 'screenlock')
build = os.path.join(path, 'build')
keysblock = os.path.join(path,'keysblock')

shutil.copy (src,dst)

zipname = os.path.join(newFolder, 'screenlock-'+version +'.zip')
zipf = zipfile.ZipFile(zipname,'w')
foldersToZip = [dst, keysblock]
#zipdir(dst, zipf)
zipdir(foldersToZip, zipf)
zipf.close()

shutil.rmtree(dst)
shutil.rmtree(build)
shutil.rmtree(keysblock)