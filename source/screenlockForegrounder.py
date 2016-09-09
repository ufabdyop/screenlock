import logging
import subprocess
import time
import os.path
import traceback
import urllib2, threading, thread
from datetime import datetime
from threading import Thread
from screenlockWindowHelper import getWindow, getAllVisibleWindows, windowTitleMatchesAny
import win32gui
import win32con
import pprint
import psutil

# a thread class to do the infinite loop to make sure the
# Coral window at the most front
#=======================================================

class ControlFrameThread(Thread):
    windows = {}

    def __init__(self):
        Thread.__init__(self)
        self.logger = logging.getLogger("screenlockApp")
        self.active = threading.Event()
        self.active.set()
        self.setConfig()

    def setConfig(self):
        preferred_order_of_windows = {
            0: "Run Data Collector",
            1: "Warning",
            2: "Error",
            3: "Coral",
            4: "Screen Saver",
            5: "Application Update",
            6: "Transparent Window"
        }
        self.config = {
            "order": preferred_order_of_windows
        }

    def stopRunning(self):
        self.active.clear()

    def run(self):
        while self.active.isSet():
            self.updateWindowList()
            self.pushNecessaryWindowsToForeground()
            time.sleep(0.5)
        self.undoTopmost()
        self.logger.debug("foregrounder over")

    def updateWindowList(self):
        newWindows = getAllVisibleWindows()
        self.addPreferredOrderAttribute(newWindows)
        self.printListDiffs(ControlFrameThread.windows, newWindows)
        ControlFrameThread.windows = newWindows

    def pushNecessaryWindowsToForeground(self):
        titles_we_care_about = self.config['order'].values()
        windows_we_care_about = self.filterByTitle(titles_we_care_about).values()
        zOrdering = list(windows_we_care_about)
        self.orderByZ(zOrdering)

        preferredOrder = list(windows_we_care_about)
        self.orderByPreference(preferredOrder)

        reOrder = False
        if zOrdering != preferredOrder:
            self.logger.debug("Ordering of preferred windows needs to be changed!")
            reOrder = True
        else:
            pass
            #self.logger.debug("Ordering of preferred windows seems good!")

        topWindow = self.getTopWindow()
        if topWindow not in windows_we_care_about:
            self.logger.debug("Why isn't the top window one of our preferred ones?")
            self.logger.debug(topWindow)
            reOrder = True

        if reOrder:
            for win in reversed(preferredOrder):
                self.makeTopMost(win['hwnd'])

    def filterByTitle(self, titles_we_care_about):
        filtered = {}
        for h in ControlFrameThread.windows:
            window = ControlFrameThread.windows[h]
            title = window['title']
            if windowTitleMatchesAny(title, titles_we_care_about):
                filtered[h] = window
        return filtered

    def printListDiffs(self, win1, win2):
        buffer = ""
        for h in win1:
            if h not in win2:
                buffer += "Only in list 1: %s\n" % pprint.pformat(win1[h])
            else:
                buffer += self.printWinDiff(win1[h], win2[h])
        for h in win2:
            if win1.get(h, False) == False:
                buffer += "Only in list 2: %s\n" % pprint.pformat(win2[h])

        if buffer:
            self.logger.debug("win1 length: %s, win2 length: %s" % (len(win1), len(win2)))
            self.logger.debug(buffer)

    def printWinDiff(self, win1, win2):
        buffer = ""
        for k in win1.keys():
            if win1[k] != win2[k]:
                buffer += "%s %s: (%s, %s)\n" % (win1['hwnd'], k, win1[k], win2[k])

        return buffer

    def orderByZ(self, windowList):
        windowList.sort(key=lambda x: x['zIndex'])

    def orderByPreference(self, windowList):
        windowList.sort(key=lambda x: x['preferredOrder'])

    def addPreferredOrderAttribute(self, objects):
        order = self.config['order']
        for k in objects:
            ob = objects[k]
            ob['preferredOrder'] = 999
            for key in order:
                if order[key] in ob['title']:
                    ob['preferredOrder'] = key

    def getTopWindow(self):
        if ControlFrameThread.windows.values():
            topWin = ControlFrameThread.windows.values()[0]
            for h in ControlFrameThread.windows:
                win = ControlFrameThread.windows[h]
                if win['zIndex'] < topWin['zIndex']:
                    topWin = win
            return topWin
        else:
            return None

    def undoTopmost(self):
        titles_we_care_about = self.config['order'].values()
        windows_we_care_about = self.filterByTitle(titles_we_care_about).values()
        for win in windows_we_care_about:
            try:
                win32gui.SetWindowPos(win['hwnd'], win32con.HWND_NOTOPMOST, 0, 0, 500, 500,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            except:
                self.logger.error("Couldn't set NOT topmost %s" % win['hwnd'])

    def makeTopMost(self, hwnd):
        try:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 500, 500,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except:
            self.logger.error("Couldn't set NOT topmost %s" % hwnd)

        try:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 500, 500,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except:
            self.logger.error("Couldn't set as topmost %s" % hwnd)

        try:
            win32gui.SetForegroundWindow(hwnd)
        except:
            self.logger.error("SetForegroundWindow failed for hwnd: %s" % hwnd)