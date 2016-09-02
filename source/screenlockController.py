from __future__ import print_function
import os, subprocess, signal, psutil,log, sys, pprint, logging, win32api
from datetime import datetime
from screenlockConfig import SLConfig
from screenlockWindowHelper import getWindow
import win32gui
import win32con

class SLController(object):
    def __init__(self):
        log.initialize_logging("SLController")
        self.logger = logging.getLogger("SLController")
        self.config = SLConfig()
        self.lockerProc = []

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            self.app_init = [os.path.join(application_path,
                                          "screenlockApp.exe")]
            self.appname="screenlockApp.exe"
        elif __file__:
            application_path = os.path.dirname(__file__)
            self.app_init = ["python.exe",
                                os.path.join(application_path,
                                 "screenlockApp.py")]
            self.appname="screenlockApp.py"

        self.logger.debug("Screenlock Controller Initialized, path: %s, appName: %s" %
                          (application_path, self.appname))

    def is_running(self):
        for p in psutil.process_iter():
            try:
                if p.name == self.appname:
                    return True
            except psutil.Error as err:
                #permission error on getting name of process (safe to ignore)
                pass
        return False

    def lock_screen(self):
        self.lockerProc.append( subprocess.Popen(self.app_init,  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) )

    def unlock_screen(self):
        if len(self.lockerProc) == 0:
            self.logger.debug("ScreenlockController: ignoring unlock, no lock found")
        else:
            for p in self.lockerProc:
                if p.pid:
                    self.logger.debug("%s %s" % (" Killing PID: ", p.pid))
                    try:
                        p.send_signal(signal.SIGTERM)
                    except:
                        self.logger.debug("ScreenlockController: The Screenlock app is not running.")
                        continue
            del self.lockerProc[:]
        self.unlock_screen_started_by_other_process()
        self.make_coral_not_top_most()

    def unlock_screen_started_by_other_process(self):
        keyBlocker = self.config.get('keysblock')
        for p in psutil.process_iter():
            try:
                if p.name == self.appname or p.name == keyBlocker:
                    self.logger.debug("Killing %s by pid %s" % (p.name, p.pid))
                    p.send_signal(signal.SIGTERM)
                    return True
            except psutil.Error as err:
                self.logger.error("Error on unlock: %s" % (pprint.pformat(err)))
        return False

    def make_coral_not_top_most(self):
        self.logger.debug("making coral NOT topmost from SERVER")

        coralWindow = getWindow("Coral")
        if coralWindow:
            try:
                win32gui.SetWindowPos(coralWindow["Coral"],win32con.HWND_NOTOPMOST,0,0,500,500, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
                self.logger.debug("Made coral not topmost")
            except:
                self.logger.error (" screenlockApp makeCoralNotTopMost: Coral window may not exist.")
        else:
            self.logger.debug("No coral window to not topmost")


