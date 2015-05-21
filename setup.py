import sys, time, os, zipfile
sys.path.insert(0, 'Z:\\screenlock\\source')
import screenlockConfig
from distutils.core import setup
import py2exe
import shutil

def zipdir(path, zipfile):
    for root, dirs, files in os.walk(path):
        for file in files:
            zipfile.write(os.path.join(root, file))

path = 'Z:/screenlock/'
version = sys.argv[2]
del sys.argv[2:]

print sys.path
setup (console=['source\screenlockApp.py'])
setup (console=['source\setAdminPassword.py'])

time.sleep(5)

src = path + 'source/config.ini'
dst = path + 'dist/'
build = path + 'build/'
shutil.copy (src,dst)

newFolder = path + 'Tags/' + version
if os.path.isdir(newFolder):
    shutil.rmtree(newFolder)
os.makedirs(newFolder)
zipf = zipfile.ZipFile(newFolder+'/screenlock-'+version +'.zip','w')
zipdir(dst, zipf)
zipf.close()

shutil.rmtree(dst)
shutil.rmtree(build)
