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
        self.lockerProc = subprocess.Popen(["screenlockApp.exe"],  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    def unlock_screen(self):
        if self.lockerProc is None:
            print("ignoring unlock, no lock found")
        else:
            if self.lockerProc.pid:
                print("Killing PID: %d" % self.lockerProc.pid)
                try:
                    os.kill(self.lockerProc.pid, signal.CTRL_BREAK_EVENT)
                except:
                    print ("Error: The Screenlock app is not running.")
                finally:
                    self.lockerProc = None


