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

defaultDistributionFolder = os.path.join(path, 'dist')
distributionFolder = os.path.join(path, 'screenlock')
buildFolder = os.path.join(path, 'build')
sourceFolder = os.path.join(path, 'source')
taggedFolder = os.path.join(path, 'Tags', version)

#rename dist folder so zip file is nice
os.rename( defaultDistributionFolder, distributionFolder )

#copy config file to dist folder
configFile = os.path.join(sourceFolder, 'config.ini')
shutil.copy (configFile,distributionFolder)

#create tagged folder for zip storage (overwrite existing)
if os.path.isdir(taggedFolder):
    shutil.rmtree(taggedFolder)
os.makedirs(taggedFolder)

#write distribution folder to tagged zip file
zipname = os.path.join(taggedFolder, 'screenlock-'+version +'.zip')
zipdir(distributionFolder, zipname)

#clean up
shutil.rmtree(distributionFolder)
shutil.rmtree(buildFolder)

