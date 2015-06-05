import sys, time, os, py2exe, shutil, pprint
from distutils.core import setup
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(path, "source"))
from buildtools import zipdir
from version import VERSION

def main():
    run_setups()
    rename_dist_folder()
    copy_config_file_to_dist_folder()
    copy_nsis_file_to_dist_folder()
    time.sleep(5)
    create_tagged_folder()
    write_zip_file()
    clean_up()

def run_setups():
    setup (console=['source\\blockKeys.py'])
    setup (console=['source\\screenlockApp.py'])
    setup (console=['source\\setAdminPassword.py'])

def rename_dist_folder():
    os.rename(DEFAULT_DISTRIBUTION_FOLDER, NEW_DISTRIBUTION_FOLDER)

def copy_config_file_to_dist_folder():
    config_file = os.path.join(SOURCE_FOLDER, 'config.ini')
    shutil.copy (config_file,NEW_DISTRIBUTION_FOLDER)

def copy_nsis_file_to_dist_folder():
    nsis_file = os.path.join(SOURCE_FOLDER, 'installer', 'install.nsi')
    new_installer_folder = os.path.join(NEW_DISTRIBUTION_FOLDER, 'installer')
    os.makedirs(new_installer_folder)
    shutil.copy (nsis_file,new_installer_folder)

def create_tagged_folder():
    if os.path.isdir(TAGGED_FOLDER):
        shutil.rmtree(TAGGED_FOLDER)
    os.makedirs(TAGGED_FOLDER)

def write_zip_file():
    zipname = os.path.join(TAGGED_FOLDER, 'screenlock-' + VERSION + '.zip')
    zipdir(NEW_DISTRIBUTION_FOLDER, zipname)

def clean_up():
    shutil.move(NEW_DISTRIBUTION_FOLDER, TAGGED_FOLDER)
    shutil.rmtree(BUILD_FOLDER)

#constants
DEFAULT_DISTRIBUTION_FOLDER = os.path.join(path, 'dist')
NEW_DISTRIBUTION_FOLDER = os.path.join(path, 'screenlock')
BUILD_FOLDER = os.path.join(path, 'build')
SOURCE_FOLDER = os.path.join(path, 'source')
TAGGED_FOLDER = os.path.join(path, 'Tags', VERSION)

main()
