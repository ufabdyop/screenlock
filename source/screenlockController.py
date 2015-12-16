from __future__ import print_function
import os, subprocess, signal, psutil,log
from datetime import datetime

global logFile
logFile = open(log.create_log_file('ScreenlockController'), "a")

class SLController(object):
    def __init__(self):
        self.lockerProc = []
        self.appname = "screenlockApp.exe"

    def is_running(self):
        for p in psutil.process_iter():
            try:
                if p.name == self.appname:
                    return True
            except psutil.Error as err:
                global logFile
                print (str(datetime.now()) + "  ScreenlockController: " + str(err), file = logFile )
        del self.lockerProc[:]
        return False

    def lock_screen(self):
        self.lockerProc.append( subprocess.Popen(["screenlockApp.exe"],  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) )

    def unlock_screen(self):
        if len(self.lockerProc) == 0:
            global logFile
            print (str(datetime.now()) + " ScreenlockController: ignoring unlock, no lock found", file = logFile)
        else:
            for p in self.lockerProc:
                if p.pid:
                    print (str(datetime.now()) + " Killing PID: " +  p.pid, file = logFile)
                    try:
                        os.kill(p.pid, signal.CTRL_BREAK_EVENT)
                    except:
                        print (str(datetime.now()) + " ScreenlockController: The Screenlock app is not running.", file = logFile)
                        continue
            del self.lockerProc[:]
                


