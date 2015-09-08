import os, subprocess, signal, psutil

class SLController(object):
    def __init__(self):
        self.lockerProc = []
        self.appname = "screenlockApp.exe"

    def is_running(self):
        for p in psutil.process_iter():
            try:
                if p.name == self.appname:
                    return True
            except psutil.Error:
                pass
        del self.lockerProc[:]
        return False

    def lock_screen(self):
        self.lockerProc.append( subprocess.Popen(["screenlockApp.exe"],  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) )

    def unlock_screen(self):
        if len(self.lockerProc) == 0:
            print("ignoring unlock, no lock found")
        else:
            for p in self.lockerProc:
                if p.pid:
                    print("Killing PID: %d" % p.pid)
                    try:
                        os.kill(p.pid, signal.CTRL_BREAK_EVENT)
                    except:
                        print ("Error: The Screenlock app is not running.")
                        continue
            del self.lockerProc[:]
                


