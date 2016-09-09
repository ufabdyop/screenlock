import os, stat, sys, shutil, win32api, win32file, win32security, ntsecuritycon
import logging
from datetime import datetime

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    APPLICATION_PATH = os.path.dirname(sys.executable)
elif '.exe' in os.path.dirname(__file__):
    APPLICATION_PATH = os.path.dirname(os.path.dirname(__file__))
elif __file__:
    APPLICATION_PATH = os.path.dirname(__file__)

print("Path: " + APPLICATION_PATH)


APPLICATION_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_FOLDER = os.path.join(APPLICATION_PATH, '..', 'Log')

print("Log Path: " + LOG_FOLDER)

# LOG_FOLDER = 'C:\Temp\Log'

#  create a log folder
def create_log_folder():
	if os.path.isdir(LOG_FOLDER):
		shutil.rmtree(LOG_FOLDER)
	os.makedirs(LOG_FOLDER)
	allow_everyone_permission_to_log_folder()

def allow_everyone_permission_to_log_folder():
	sidWorld = win32security.CreateWellKnownSid(win32security.WinWorldSid, None)
	worldRights = win32file.FILE_ALL_ACCESS
	flags = win32security.OBJECT_INHERIT_ACE| win32security.CONTAINER_INHERIT_ACE

	#get DACL
	fileSecDesc = win32security.GetNamedSecurityInfo(LOG_FOLDER, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION)
	fileDacl = fileSecDesc.GetSecurityDescriptorDacl()

	#add rights
	fileDacl.AddAccessAllowedAceEx(win32security.ACL_REVISION_DS, flags, worldRights, sidWorld)

	win32security.SetNamedSecurityInfo( \
    LOG_FOLDER, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION, \
    None, None, fileDacl, None )


def create_log_file(name):
    filename = get_log_filename(name)
    logFile = open(filename,'a')
    logFile.close()
    return filename

def get_log_filename(name):
    time = str(datetime.now())
    time = time.replace(':', '_')
    time = time.replace('.', '_')
    filename = os.path.join(LOG_FOLDER, time + '-' + name + '.log')
    #filename = os.path.join(LOG_FOLDER, name + '.log')
    return filename

def initialize_logging(name):
    filename = get_log_filename("screenlock")
    logging.basicConfig(filename=filename,
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s\t%(thread)d-%(threadName)s\t%(filename)s\t%(lineno)s\t%(message)s\t")


