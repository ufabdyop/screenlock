import os, shutil
from distutils.dir_util import copy_tree

def main():
    create_exe()
    merge_files()
    copy_config_files()

def source_files():
    return [
        'setAdminPassword',
        'postinstall',
        'commandClient',
        'ncdClient',
        'screenlockServerNCD',
        'screenlockServer',
        'screenlockServerNCD',
        'screenlockApp']

def create_exe():
    os.system('pyinstaller  --windowed --uac-admin source/setAdminPassword.py')
    os.system('pyinstaller  --windowed --uac-admin source/postinstall.py')
    os.system('pyinstaller  --console source/commandClient.py')
    os.system('pyinstaller  --console source/ncdClient.py')
    os.system('pyinstaller  --console -n screenlockServerNCD_console source/screenlockServerNCD.py')
    os.system('pyinstaller  --windowed source/screenlockServer.py')
    os.system('pyinstaller  --windowed source/screenlockServerNCD.py')
    os.system('pyinstaller  --windowed source/screenlockApp.py')

def copy_config_files():
    shutil.copy('source/config.ini', 'dist/combined')
    shutil.copy('source/key.pem', 'dist/combined')
    shutil.copy('source/cert.pem', 'dist/combined')
    shutil.copy('source/license.txt', 'dist/combined')
    shutil.copy('source/post-install.txt', 'dist/combined')
    shutil.copy('source/startup.bat', 'dist/combined')
    shutil.copy('source/startup.vbs', 'dist/combined')
    shutil.copy('source/startupNCD.bat', 'dist/combined')
    shutil.copy('source/startupNCD.vbs', 'dist/combined')
    shutil.copy('README.md', 'dist/combined')

def merge_files():
    if not os.path.isdir("dist/combined"):
        os.mkdir("dist/combined")

    for i in source_files():
        copy_tree("dist/%s" % i, "dist/combined")


main()
