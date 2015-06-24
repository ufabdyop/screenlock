import os, subprocess, signal, psutil

class SLController(object):
    def __init__(self):
        self.lockerProc = None
        self.appname = "screenlockApp.exe"

    def is_running(self):
        for p in psutil.process_iter():
            try:
                if p.name == self.appname:
                    return True
            except psutil.Error:
                pass
        return False

    def lock_screen(self):
        #self.lockerProc = subprocess.Popen(["python", "screenlockApp.py"],  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        self.lockerProc = subprocess.Popen(["screenlockApp.exe"],  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    def unlock_screen(self):
        if self.lockerProc is not None:
            if self.lockerProc.pid:
                print("Killing PID: %d" % self.lockerProc.pid)
                os.kill(self.lockerProc.pid, signal.CTRL_BREAK_EVENT)
        else:
            print("ignoring unlock, no lock found")


