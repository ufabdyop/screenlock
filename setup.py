import sys, time, os
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(path, "source"))

from distutils.core import setup
import py2exe
import shutil
from buildtools import zipdir

version = sys.argv[2]
del sys.argv[2:]

setup (console=['source\\blockKeys.py'])
setup (console=['source\\screenlockApp.py'])
setup (console=['source\\setAdminPassword.py'])

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
zipdir(dst, zipname)

shutil.rmtree(dst)
shutil.rmtree(build)

