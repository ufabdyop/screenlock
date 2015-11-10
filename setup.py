import sys, time, os, py2exe, shutil, pprint, subprocess
from distutils.core import setup
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PATH, "source"))
from version import VERSION

def main():
    create_zope_init_fix()
    delete_old_build()
    run_setups()
    rename_dist_folder()
    copy_support_files_to_dist_folder()
    time.sleep(5)
    create_tagged_folder()
    move_assets_to_tagged_folder()
    print_message()
    try_running_nsis()
    clean_up()

def run_setups():
    setup (console=['source\\screenlockServer.py'])
    setup (console=['source\\screenlockServerNCD.py'])
    setup (console=['source\\blockKeys.py'])
    setup (console=['source\\screenlockApp.py'])
    setup (console=['source\\setAdminPassword.py'])
    setup (console=['source\\builder.py'])

def rename_dist_folder():
    os.rename(DEFAULT_DISTRIBUTION_FOLDER, NEW_DISTRIBUTION_FOLDER)

def copy_support_files_to_dist_folder():
    copy_config_and_text_files_to_dist_folder()
    write_version_to_text_file()
    copy_nsis_file_to_dist_folder()
    dynamically_add_file_list_to_nsis()

def copy_config_and_text_files_to_dist_folder():
    files = [os.path.join(SOURCE_FOLDER, 'config.ini'),
    		os.path.join(SOURCE_FOLDER, 'key.pem'),
    		os.path.join(SOURCE_FOLDER, 'cert.pem'),
            os.path.join(SOURCE_FOLDER, 'license.txt'),
            os.path.join(SOURCE_FOLDER, 'post-install.txt'),
            os.path.join(SOURCE_FOLDER, 'startup.bat'),
            os.path.join(SOURCE_FOLDER, 'startup.vbs'),
            os.path.join(SOURCE_FOLDER, 'startupNCD.bat'),
            os.path.join(SOURCE_FOLDER, 'startupNCD.vbs'),
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

def delete_old_build():
    if os.path.isdir(DEFAULT_DISTRIBUTION_FOLDER):
        shutil.rmtree(DEFAULT_DISTRIBUTION_FOLDER)
    if os.path.isdir(NEW_DISTRIBUTION_FOLDER):
        shutil.rmtree(NEW_DISTRIBUTION_FOLDER)
    if os.path.isdir(BUILD_FOLDER):
        shutil.rmtree(BUILD_FOLDER)

def create_tagged_folder():
    if os.path.isdir(TAGGED_FOLDER):
        shutil.rmtree(TAGGED_FOLDER)
    os.makedirs(TAGGED_FOLDER)

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

def create_nsis_file_instructions():
    path = NEW_DISTRIBUTION_FOLDER
    filenames = next(os.walk(path))[2]

    buff = ''
    for f in filenames:
        buff += 'File "..\\%s"' % f
        buff += "\n"
    return buff

def dynamically_add_file_list_to_nsis():
    nsis_file = os.path.join(NEW_DISTRIBUTION_FOLDER, 'installer', 'install.nsi')
    buff = create_nsis_file_instructions()
    file = open(nsis_file)
    contents = file.read()
    file.close()
    new_contents = contents.replace(';DYNAMIC_ADD_OF_PY2EXE_FILES', buff)
    file = open(nsis_file, 'w')
    file.write(new_contents)
    file.close()

def touch(filename):
    if not os.path.exists(filename):
        print("Creating file")
        open(filename, 'w').close() 
    else:
        print("file exists, skipping")

def create_zope_init_fix():
    #See : http://stackoverflow.com/a/11632115/1243508
    pythondir = sys.exec_prefix
    zope_init_file = os.path.join(pythondir, 'Lib', 'site-packages', 'zope', '__init__.py')
    touch(zope_init_file)

#constants
DEFAULT_DISTRIBUTION_FOLDER = os.path.join(PATH, 'dist')
NEW_DISTRIBUTION_FOLDER = os.path.join(PATH, 'screenlock')
BUILD_FOLDER = os.path.join(PATH, 'build')
SOURCE_FOLDER = os.path.join(PATH, 'source')
TAGS_BASE_FOLDER = os.path.join(PATH, 'Tags')
TAGGED_FOLDER = os.path.join(TAGS_BASE_FOLDER, VERSION)

main()
