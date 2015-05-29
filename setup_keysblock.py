import sys, time, os
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(path, "source"))

from distutils.core import setup
import py2exe
import shutil

setup (console=['source\\blockKeys.py'])

time.sleep(3)

dst =  os.path.join(path, 'keysblock')
build = os.path.join(path, 'build')
if os.path.isdir(dst):
    shutil.rmtree(dst)

os.rename( os.path.join(path, 'dist'), dst )

shutil.rmtree(build)
