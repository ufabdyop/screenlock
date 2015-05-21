import sys, time, os, zipfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "source"))
import screenlockConfig
from distutils.core import setup
import py2exe
import shutil

def zipdir(path, zipfile):
    for root, dirs, files in os.walk(path):
        for file in files:
            zipfile.write(os.path.join(root, file))

path = os.path.dirname(__file__)
version = sys.argv[2]
del sys.argv[2:]

print sys.path
setup (console=['source\screenlockApp.py'])
setup (console=['source\setAdminPassword.py'])

time.sleep(5)

src = os.path.join(path, 'source', 'config.ini')
os.rename( os.path.join(path, 'dist'), os.path.join(path, 'screenlock') )
dst =  os.path.join(path, 'screenlock')
build = os.path.join(path, 'build')

shutil.copy (src,dst)

newFolder = os.path.join(path, 'Tags', version)
if os.path.isdir(newFolder):
    shutil.rmtree(newFolder)
os.makedirs(newFolder)
zipname = os.path.join(newFolder, 'screenlock-'+version +'.zip')
zipf = zipfile.ZipFile(zipname,'w')
zipdir(dst, zipf)
zipf.close()

shutil.rmtree(dst)
shutil.rmtree(build)

