import logging
import subprocess
import time
import urllib2, threading, thread
from datetime import datetime
from threading import Thread
from screenlockWindowHelper import getWindow
import win32gui
import win32con
import pprint
import psutil

# a thread class to do the infinite loop to make sure the
# Coral window at the most front
#=======================================================

class ControlFrameThread(Thread):
    def __init__(self,
                 front_window,
                 test_connection_url,
                 use_coral,
                 coral_sleep_delay=6):
        Thread.__init__(self)
        self.front_window = front_window
        self.test_connection_url = test_connection_url
        self.use_coral = use_coral
        self.coral_sleep_delay = coral_sleep_delay
        self.checkCoralOpen = False
        self.logger = logging.getLogger("screenlockApp")
        self.active = threading.Event()
        self.active.set()
        self.max_coral_attempts = 10
        self.coral_attempts = 0
        self.appProcess = False

    def stopRunning(self):
        self.active.clear()

    def run(self):
        while self.active.isSet():
            self.checkCoralOpen = False
            self.makeProgramAtFront()
            self.debugPidInfo()
            time.sleep(1)
        self.makeCoralNotTopMost()
        thread.exit()
        return

    # a method to be invoked by ControlFrameThread
    def makeProgramAtFront(self):
        def makeWindowTopmost(windowHwnd):
            win32gui.SetWindowPos(windowHwnd, win32con.HWND_TOPMOST, 0, 0, 500, 500,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

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
                    self.coral_attempts = 0

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
            self.logger.error(str(datetime.now()) + " screenlockApp makeProgramAtFront: window may not exist.")
        if not self.checkCoralOpen and self.use_coral == 'true':
            self.openCoral()

    def openCoral(self):
        path = self.front_window
        internet_flag = self.internetOn()
        while (not internet_flag) and (self.active.isSet()):
            self.logger.error (str(datetime.now()) + " screenlockApp: NO internet.")
            time.sleep(2)
            internet_flag = self.internetOn()

        self.logger.debug("opening coral attempt %s" % self.coral_attempts)

        if self.coral_attempts <= self.max_coral_attempts:
            self.coral_attempts += 1
            self.appProcess = subprocess.Popen(path)
            self.logger.debug("Opened PID: %s" % self.appProcess.pid)
            self.debugPidInfo()
        else:
            self.logger.debug("exceeded max coral open attempts")
        time.sleep(int(self.coral_sleep_delay))

    def debugPidInfo(self):
        if self.appProcess:
            if self.appProcess.pid:
                try:
                    procObject = psutil.Process(self.appProcess.pid)
                    self.logger.debug("object: %s" % (pprint.pformat(procObject)))
                except:
                    self.logger.debug("No process for %s" % (self.appProcess.pid))

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
