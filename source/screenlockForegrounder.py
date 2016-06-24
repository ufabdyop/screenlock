import logging
import subprocess
import time
import urllib2, threading
from datetime import datetime
from threading import Thread
from screenlockWindowHelper import getWindow
import win32gui
import win32con

# a thread class to do the infinite loop to make sure the
# Coral window at the most front
#=======================================================

class ControlFrameThread(Thread):
    def __init__(self, front_window, test_connection_url, use_coral):
        Thread.__init__(self)
        self.front_window = front_window
        self.test_connection_url = test_connection_url
        self.use_coral = use_coral
        self.checkCoralOpen = False
        self.logger = logging.getLogger("screenlockApp")
        self.active = threading.Event()
        self.active.set()

    def stopRunning(self):
        self.active.clear()

    def run(self):
        while self.active.isSet():
            self.checkCoralOpen = False
            self.makeProgramAtFront()
            time.sleep(1)
        self.makeCoralNotTopMost()
        print("deactivated fg")
        return

    # a method to be invoked by ControlFrameThread
    def makeProgramAtFront(self):
        def makeWindowTopmost(windowHwnd):
            win32gui.SetWindowPos(windowHwnd, win32con.HWND_TOPMOST, 0, 0, 500, 500,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        logger = logging.getLogger("screenlockApp")
        if (self.use_coral == 'true'):
            windows = getWindow("Run Data Collector", "Warning", "Error", "Coral", "Screen Saver", "Application Update")
        else:
            windows = getWindow("Warning", "Error", "Screen Saver")
        try:
            if windows:
                if "Warning" in windows:
                    self.checkCoralOpen = True
                    makeWindowTopmost(windows["Warning"])
                elif "Error" in windows:
                    self.checkCoralOpen = True
                    makeWindowTopmost(windows["Error"])
                elif "Coral" in windows:
                    self.checkCoralOpen = True

                if "Application Update" in windows:
                    self.checkCoralOpen = True
                    makeWindowTopmost(windows["Application Update"])
                elif self.checkCoralOpen:
                    makeWindowTopmost(windows["Coral"])
                if "Run Data Collector" in windows:
                    makeWindowTopmost(windows["Run Data Collector"])
                if "Screen Saver" in windows:
                    makeWindowTopmost(windows["Screen Saver"])
        except:
            logger.error(str(datetime.now()) + " screenlockApp makeProgramAtFront: window may not exist.")
        if not self.checkCoralOpen and self.use_coral == 'true':
            self.openCoral()

    def openCoral(self):
        logger = logging.getLogger("screenlockApp")
        path = self.front_window
        internet_flag = self.internetOn()
        while (not internet_flag) and (self.active.isSet()):
            logger.error (str(datetime.now()) + " screenlockApp: NO internet.")
            time.sleep(2)
            internet_flag = self.internetOn()
        subprocess.Popen(path)
        time.sleep (6)

    def internetOn(self):
        try:
            test_connection_url = self.test_connection_url
            response = urllib2.urlopen(test_connection_url,timeout=1)
            return True
        except urllib2.URLError as err:
            self.logger.error (str(datetime.now()) + " screenlockApp: " + str(err))
        return False

    def makeCoralNotTopMost(self):
        coralWindow = getWindow("Coral")

        if coralWindow:
            try:
                win32gui.SetWindowPos(coralWindow["Coral"],win32con.HWND_NOTOPMOST,0,0,500,500, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
            except:
                self.logger.error (str(datetime.now()) + " screenlockApp makeCoralNotTopMost: Coral window may not exist.")
