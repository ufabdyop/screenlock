import os, stat, sys, shutil, win32api, win32file, win32security, ntsecuritycon
from datetime import datetime

PATH = os.path.dirname(os.path.abspath(__file__))
LOG_FOLDER = os.path.join(PATH, '../Log')
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
	global FILENAME
	time = str(datetime.now())
	time = time.replace(':', '_')
	FILENAME = os.path.join(LOG_FOLDER, time +'-'+ name +'.log')
	logFile = open(FILENAME,'a')
	logFile.close()
	return FILENAME
