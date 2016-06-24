import logging
import time
from threading import Thread

import thread
import win32gui
import win32con

from datetime import datetime
import threading

from screenlockWindowHelper import getWindow

# a thread class to do the infinite loop to hide taskmgr
class TaskManagerHider(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.logger = logging.getLogger("bottomTaskManageWindow")
        self.active = threading.Event()
        self.active.set()

    def run(self):
        self.bottomTaskManageWindow()
        self.logger.debug("taskmgr hider done")

    def stopRunning(self):
        self.logger.debug("taskmgr hider signaled")
        self.active.clear()

    def bottomTaskManageWindow(self):
        while True:
            if not self.active.isSet():
                self.logger.debug("quitting task manager")
                break

            time.sleep(0.5)
            taskwindow = getWindow("Windows Task Manager")
            if taskwindow:
                try:
                    win32gui.SetWindowPos(taskwindow["Windows Task Manager"],
                                          win32con.HWND_BOTTOM, 0, 0, 500, 500,
                                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                except:
                    self.logger.error(str(datetime.now()) + " screenlockApp: Windows Task Manager may not exist.")
