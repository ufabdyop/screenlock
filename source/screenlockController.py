import os, subprocess, signal, psutil

class SLController(object):
    def __init__(self):
        self.lockerProc = {}
        self.count = 0
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
        self.count += 1
        self.lockerProc[self.count] = subprocess.Popen(["screenlockApp.exe"],  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    def unlock_screen(self):
        if self.count == 0:
            print("ignoring unlock, no lock found")
        else:
            for number in range (1, self.count+1):
                if self.lockerProc[number].pid:
                    print("Killing PID: %d" % self.lockerProc[number].pid)
                    try:
                        os.kill(self.lockerProc[number].pid, signal.CTRL_BREAK_EVENT)
                    except:
                        print ("Error: The Screenlock app is not running.")
                        continue
            self.count = 0
                


