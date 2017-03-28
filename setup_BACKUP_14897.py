import sys, time, os, shutil, pprint, subprocess
from distutils.core import setup
from distutils.dir_util import copy_tree

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PATH, "source"))
from version import VERSION

#constants
DEFAULT_DISTRIBUTION_FOLDER = os.path.join(PATH, 'dist')
COMBINED_DISTRIBUTION_FOLDER = os.path.join(DEFAULT_DISTRIBUTION_FOLDER, 'screenlock')
NEW_DISTRIBUTION_FOLDER = COMBINED_DISTRIBUTION_FOLDER
BUILD_FOLDER = os.path.join(PATH, 'build')
SOURCE_FOLDER = os.path.join(PATH, 'source')
STATIC_FOLDER = os.path.join(SOURCE_FOLDER, 'static')
<<<<<<< HEAD
GRAPHIC_FOLDER = os.path.join(SOURCE_FOLDER, 'graphics')
=======
>>>>>>> 66c9c0888012cf972a59658f7735df98ea406928
TEMPLATE_FOLDER = os.path.join(SOURCE_FOLDER, 'templates')
TAGS_BASE_FOLDER = os.path.join(PATH, 'Tags')
TAGGED_FOLDER = os.path.join(TAGS_BASE_FOLDER, VERSION)

def main():
    delete_old_build()
    create_exe()
    merge_files()
    copy_static_files_to_tagged_folder()
    copy_support_files_to_dist_folder()
    dynamically_add_file_list_to_nsis()
    create_tagged_folder()
    move_assets_to_tagged_folder()
    print_message()
    try_running_nsis()
    clean_up()

def delete_old_build():
    if os.path.isdir(DEFAULT_DISTRIBUTION_FOLDER):
        shutil.rmtree(DEFAULT_DISTRIBUTION_FOLDER)
    if os.path.isdir(NEW_DISTRIBUTION_FOLDER):
        shutil.rmtree(NEW_DISTRIBUTION_FOLDER)
    if os.path.isdir(BUILD_FOLDER):
        shutil.rmtree(BUILD_FOLDER)

def create_exe():
<<<<<<< HEAD
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed --uac-admin --icon=source/graphics/Lock_256.ico source/postinstall.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --console --icon=source/graphics/Lock_256.ico source/commandClient.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --console --icon=source/graphics/Lock_256.ico source/ncdClient.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --console -n screenlockServerNCD_console --icon=source/graphics/Lock_256.ico source/screenlockServerNCD.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed --icon=source/graphics/Lock_256.ico source/screenlockServer.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed --icon=source/graphics/Lock_256.ico source/screenlockServerNCD.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed --icon=source/graphics/Lock_256.ico source/screenlockApp.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed --icon=source/graphics/Lock_256.ico source/userLock.py')
=======
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed --uac-admin --icon=Logo_256.ico source/postinstall.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --console source/commandClient.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --console source/ncdClient.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --console -n screenlockServerNCD_console source/screenlockServerNCD.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed source/screenlockServer.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed source/screenlockServerNCD.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed source/screenlockApp.py')
    os.system('C:\\Python27\\Scripts\\pyinstaller  --windowed source/userLock.py')
>>>>>>> 66c9c0888012cf972a59658f7735df98ea406928

def merge_files():
    if not os.path.isdir(COMBINED_DISTRIBUTION_FOLDER):
        os.mkdir(COMBINED_DISTRIBUTION_FOLDER)

    for i in source_files():
        copy_tree("dist/%s" % i, COMBINED_DISTRIBUTION_FOLDER)

def copy_static_files_to_tagged_folder():
    destination = os.path.join(NEW_DISTRIBUTION_FOLDER, "static")
    shutil.copytree(STATIC_FOLDER, destination)
    destination = os.path.join(NEW_DISTRIBUTION_FOLDER, "templates")
    shutil.copytree(TEMPLATE_FOLDER, destination)

def copy_support_files_to_dist_folder():
    copy_config_and_text_files_to_dist_folder()
    write_version_to_text_file()
    copy_nsis_file_to_dist_folder()

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
        nsis_location = "c:\\Program Files\\NSIS\\makensis.exe"
        if os.path.isfile("c:\\Program Files (x86)\\NSIS\\makensis.exe"):
            nsis_location = "c:\\Program Files (x86)\\NSIS\\makensis.exe"
        make_nsis_command = [nsis_location, os.path.join(TAGGED_FOLDER, 'screenlock','installer', 'install.nsi')]
        subprocess.call(make_nsis_command)
        print( "Successfully Ran NSIS.\n Check the folder %s for installer exe file" % (os.path.join(TAGS_BASE_FOLDER)))
    except:
        print( "Failed to automatically run nsis\n")

def clean_up():
    shutil.rmtree(BUILD_FOLDER)
    shutil.rmtree(DEFAULT_DISTRIBUTION_FOLDER)
    clean_up_temporary_assets_if_nsis_succeeded()

    filelist = [f for f in os.listdir(".") if f.endswith(".spec")]
    for f in filelist:
        os.remove(f)


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
<<<<<<< HEAD
            os.path.join(GRAPHIC_FOLDER, 'Lock_256.ico'),
=======
>>>>>>> 66c9c0888012cf972a59658f7735df98ea406928
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
    print("copying %s to %s" %  (nsis_file,new_installer_folder))
    shutil.copy (nsis_file,new_installer_folder)

def clean_up_temporary_assets_if_nsis_succeeded():
    nsis_setup_file = os.path.join(TAGGED_FOLDER, 'screenlock','installer', 'ScreenLock-' + VERSION + '-Setup.exe')
    if os.path.isfile(nsis_setup_file):
        shutil.copy(nsis_setup_file, TAGS_BASE_FOLDER )
        shutil.rmtree(TAGGED_FOLDER)

def dynamically_add_file_list_to_nsis():
    nsis_file = os.path.join(NEW_DISTRIBUTION_FOLDER, 'installer', 'install.nsi')
    buff = create_nsis_file_instructions()
    file = open(nsis_file)
    contents = file.read()
    file.close()
    new_contents = contents.replace(';DYNAMIC_ADD_OF_PY2EXE_FILES', ";DYNAMIC_ADD_OF_PY2EXE_FILES\n" + buff)
    file = open(nsis_file, 'w')
    file.write(new_contents)
    file.close()

def create_nsis_file_instructions():
    path = NEW_DISTRIBUTION_FOLDER

    buff = ''
    toplevel = next(os.walk(path))[0]
    toplevel_subdirs = next(os.walk(path))[1]
    toplevel_files = next(os.walk(path))[2]
    pprint.pprint(toplevel_subdirs)

    for f in toplevel_files:
        # buff += "; in root: %s\n" % root
        buff += 'File "..\\%s"' % f
        buff += "\n"

    for f in toplevel_subdirs:
        buff += 'File /r "..\\%s"' % f
        buff += "\n"

    return buff.replace(toplevel + "\\", "")

def touch(filename):
    if not os.path.exists(filename):
        print("Creating file")
        open(filename, 'w').close() 
    else:
        print("file exists, skipping")

def source_files():
    return [
        'postinstall',
        'commandClient',
        'ncdClient',
        'screenlockServerNCD',
        'screenlockServer',
        'screenlockServerNCD',
        'screenlockApp',
        'userLock']


main()
