import sys, time, os, py2exe, shutil, pprint, subprocess
from distutils.core import setup
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PATH, "source"))
from buildtools import zipdir
from version import VERSION

def main():
    run_setups()
    rename_dist_folder()
    copy_support_files_to_dist_folder()
    time.sleep(5)
    create_tagged_folder()
    write_zip_file()
    move_assets_to_tagged_folder()
    print_message()
    try_running_nsis()
    clean_up()

def run_setups():
    setup (console=['source\\blockKeys.py'])
    setup (console=['source\\screenlockApp.py'])
    setup (console=['source\\setAdminPassword.py'])

def rename_dist_folder():
    os.rename(DEFAULT_DISTRIBUTION_FOLDER, NEW_DISTRIBUTION_FOLDER)

def copy_support_files_to_dist_folder():
    copy_config_and_text_files_to_dist_folder()
    write_version_to_text_file()
    copy_nsis_file_to_dist_folder()

def copy_config_and_text_files_to_dist_folder():
    files = [os.path.join(SOURCE_FOLDER, 'config.ini'),
            os.path.join(SOURCE_FOLDER, 'license.txt'),
            os.path.join(SOURCE_FOLDER, 'post-install.txt'),
            os.path.join(SOURCE_FOLDER, 'startup.bat'),
            os.path.join(SOURCE_FOLDER, 'shutdown.bat'),
            os.path.join(SOURCE_FOLDER, 'startup.vbs'),
            os.path.join(SOURCE_FOLDER, 'shutdown.vbs'),
            os.path.join(PATH, 'README.md')]

    for f in files:
        shutil.copy (f,NEW_DISTRIBUTION_FOLDER)

def write_version_to_text_file():
    version_filename = os.path.join(NEW_DISTRIBUTION_FOLDER, 'releaseVersion.txt')
    with open(version_filename, "w") as text_file:
        text_file.write( VERSION )

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

def move_assets_to_tagged_folder():
    shutil.move(NEW_DISTRIBUTION_FOLDER, TAGGED_FOLDER)

def print_message():
    make_nsis_command_example = '"c:\\Program Files\\NSIS\\makensis.exe" %s' % (os.path.join(TAGGED_FOLDER, 'screenlock','installer', 'install.nsi'))

    message = """
    Finished building EXE files for Nanofab Screenlock.  The files
    are located in the Tag folder (%s).  
    You may want to package
    them all up into an installer.  To do so, run the make NSI
    application using the build file located in the Tagged folder's
    subdirectory "installer"

    For example, you might run:
    %s
    """
    print(message % (TAGGED_FOLDER, make_nsis_command_example))

def try_running_nsis():
    try:
        print( "Trying to automatically run nsis make for you\n")
        make_nsis_command = ["c:\\Program Files\\NSIS\\makensis.exe", os.path.join(TAGGED_FOLDER, 'screenlock','installer', 'install.nsi')]
        subprocess.call(make_nsis_command)
        print( "Successfully Ran NSIS.\n Check the folder %s for installer exe file" % (os.path.join(TAGS_BASE_FOLDER)))
    except:
        print( "Failed to automatically run nsis\n")

def clean_up():
    shutil.rmtree(BUILD_FOLDER)
    clean_up_temporary_assets_if_nsis_succeeded()

def clean_up_temporary_assets_if_nsis_succeeded():
    nsis_setup_file = os.path.join(TAGGED_FOLDER, 'screenlock','installer', 'ScreenLock-' + VERSION + '-Setup.exe')
    if os.path.isfile(nsis_setup_file):
        shutil.copy(nsis_setup_file, TAGS_BASE_FOLDER )
        shutil.rmtree(TAGGED_FOLDER)

#constants
DEFAULT_DISTRIBUTION_FOLDER = os.path.join(PATH, 'dist')
NEW_DISTRIBUTION_FOLDER = os.path.join(PATH, 'screenlock')
BUILD_FOLDER = os.path.join(PATH, 'build')
SOURCE_FOLDER = os.path.join(PATH, 'source')
TAGS_BASE_FOLDER = os.path.join(PATH, 'Tags')
TAGGED_FOLDER = os.path.join(TAGS_BASE_FOLDER, VERSION)

main()
