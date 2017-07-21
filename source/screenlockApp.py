from __future__ import print_function

from threading import Thread
import logging
import os
import sys
import signal
import subprocess
import thread, threading
import time
import version
import urllib2
from datetime import datetime

import win32api
import win32con
import win32gui
import wx
import psutil
from screenlockForegrounder import ControlFrameThread
# from childController import child_controller
from threading import Timer

import log
import screenlockConfig
import blockKeys

global endFlag
endFlag = False

global config
config = screenlockConfig.SLConfig()

ID_SUBMIT = wx.NewId()
USR_SUBMIT = wx.NewId()

class OverlayFrame( wx.Frame ):

    def __init__( self, userlock_name=None, userlock_password=None )  :
        global coral
        coral = config.get('use_client')
        self.logger=logging.getLogger('screenlockApp')
        self.logger.debug(" screenlockApp: Starting")
        self.appProcess = None
        self.userlock_name = userlock_name
        self.userlock_password = userlock_password
        # self.childController = child_controller()
        self.logger.debug(" use coral: %s" % coral )

        wx.Frame.__init__( self, None, title="Transparent Window",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )

        self.alphaValue = int(config.get('opacity'))

        if self.alphaValue <= 180 or self.alphaValue > 255:
            self.alphaValue = 240

        if wx.Display_GetCount() >= 2:
            xPos2 = wx.Display(1).GetGeometry()[0]
            self.secondFrame = wx.Frame(None, title="Transparent Window", pos=(xPos2, 0),
                                        style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
            self.secondFrame.SetTransparent(self.alphaValue)
            self.secondFrame.SetBackgroundColour('#666666')
            self.secondFrame.ShowFullScreen(True)
            self.secondFrame.Show()

        yPos = 50;

        self.ShowFullScreen( True )
        self.SetTransparent(self.alphaValue)
        self.SetBackgroundColour('#666666')
        
        font=wx.Font(16,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        self.label = wx.StaticText(self, label="For Administrator Only:", pos=(0, yPos), size=(300,30), style=wx.ALIGN_CENTER)
        self.label.SetFont(font)
        self.label.SetForegroundColour(wx.Colour(255, 255, 255))

        yPos+=35;

        self.inputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(25,yPos), name="input", style=wx.TE_PASSWORD)
        self.inputField.SetFont(font)
        self.inputField.Bind(wx.EVT_TEXT_ENTER, self.OnEnterAdmin)

        self.submitButton = wx.Button(self, ID_SUBMIT, 'Submit', size=(100, 30), pos=(185 ,yPos))
        self.submitButton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        #self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)

        yPos += 50;

        if coral:
            START_CORAL = wx.NewId()
            self.clientButton = wx.Button(self, START_CORAL, 'Start Client', pos=(10,yPos), size=wx.Size(300, 50))
            self.clientButton.SetFont(font)
            self.Bind(wx.EVT_BUTTON, self.OnStartCoral, id=START_CORAL)
            yPos += 60;
        else:
            self.logger.debug("No coral client")

        self.versionLable = wx.StaticText(self, -1, 'v' + version.VERSION, pos=(30, yPos), size=wx.Size(100, 50), style=wx.ALIGN_LEFT)
        self.versionLable.SetForegroundColour(wx.Colour(255, 255, 255))
        self.versionLable.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))

        self.input = None

        if self.userlock_name and self.userlock_password:
            yPos += 300;
            font = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
            self.userlabel = wx.StaticText(self, label="Locked by: " + self.userlock_name, pos=(0, yPos), size=(300, 30),
                                       style=wx.ALIGN_CENTER)
            self.userlabel.SetFont(font)
            self.userlabel.SetForegroundColour(wx.Colour(255, 255, 255))

            yPos += 35;

            self.userPassword = wx.TextCtrl(self, value="", size=(140, 30), pos=(25, yPos), name="input",
                                          style=wx.TE_PASSWORD)
            self.userPassword.SetFont(font)
            self.userPassword.Bind(wx.EVT_TEXT_ENTER, self.OnEnterUser)

            self.userSubmitButton = wx.Button(self, USR_SUBMIT, 'Submit', size=(100, 30), pos=(185, yPos))
            self.userSubmitButton.SetFont(font)
            self.Bind(wx.EVT_BUTTON, self.OnSubmitUser, id=USR_SUBMIT)
            #self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmitUser)

        yPos+=50;

        self.status = wx.StaticText(self, -1, '', pos=(10,yPos))
        self.status.SetFont(font)

        win32api.SetConsoleCtrlHandler(self.signalHandler, True)

        self.openKeysBlock()
        try:
            thread.start_new_thread(self.deleteLabel, (self.status,))
        except:
            self.logger.error(" screenlockApp: Can not start a new thread to delete Label.")

    def signalHandler(self, signalNumber):
        self.logger.debug("received signal: %s" % signalNumber)
        self.logger.debug("no keyblocker pid for signal")
        global endFlag
        endFlag = True
        self.Destroy()

    def OnEnterAdmin(self, event):
        self.OnSubmit(event)

    def OnEnterUser(self, event):
        self.OnSubmitUser(event)

    def OnSubmit(self, event):
        self.input = self.inputField.GetValue()
        self.inputField.Clear()
        global config
        if config.passwordCheck(self.input, 'admin_override'):
            global endFlag
            endFlag = True
            # self.childController.unlock_childs("admin", self.input)
            self.Close()
            self.Destroy()
            if wx.Display_GetCount() >= 2:
                self.secondFrame.Close()
                self.secondFrame.Destroy()
        else:
            self.status.SetLabel('You are not authorized.')

    def OnSubmitUser(self, event):
        self.userinput = self.userPassword.GetValue()
        self.userPassword.Clear()
        if self.userlock_password == self.userinput:
            global endFlag
            endFlag = True
            self.Close()
            self.Destroy()
            if wx.Display_GetCount() >= 2:
                self.secondFrame.Close()
                self.secondFrame.Destroy()
        else:
            self.status.SetLabel('You are not authorized.')

    def OnStartCoral(self, event):
        path = config.get('front_window')
        self.appProcess = subprocess.Popen(path)

    def deleteLabel(self,status):
        global endFlag
        while not endFlag:
            time.sleep(5)
            if not endFlag:
                if status.GetLabel() != '' :
                    time.sleep(5)
                    if not endFlag:
                        status.SetLabel('')
        return
        
    def openKeysBlock (self):
        keyBlocker = blockKeys.BlockKeys()
        keyBlocker.beginBlocking()


class NullProcess(object):
    def __init__(self):
        self.pid = False
        self.logger = logging.getLogger("NullProcess")
    def send_signal(self, sig):
        self.logger.error("NullProcess Received sig: %s" % sig)


def main(sysargs):
    log.initialize_logging('screenlockApp')
    logger = logging.getLogger("Main Method")

    runApp = True
    lockCounter = 0
    logger.debug("Checking if screenlock app is already running.")
    for p in psutil.process_iter():
        try:
            if p.name == "screenlockApp.exe":
                lockCounter += 1;
            elif p.name == "userLock.exe":
                lockCounter += 1
            if lockCounter >=2:
                logger.debug("Screenlockapp already running, exiting.")
                runApp = False
                break

        except psutil.Error as err:
            # permission error on getting name of process (safe to ignore)
            pass


    if (runApp):
        app = wx.App( False )
        if len(sysargs) == 2:
            frm = OverlayFrame(sysargs[0], sysargs[1])
        else:
            frm = OverlayFrame()

        frm.Show()

        frameController = ControlFrameThread()
        frameController.start()

        #taskmgrController = TaskManagerHider(frameController.logger)
        #taskmgrController.start()

        app.MainLoop()
        logger.debug("main loop exited")

        #taskmgrController.stopRunning()
        #logger.debug("taskmgr signaled stop")

        frameController.stopRunning()
        logger.debug("frame controller signaled stop")

        #taskmgrController.join(5)
        #logger.debug("taskmgr exited")

        print (threading.active_count())
        print (threading.enumerate())

        frameController.join()
        logger.debug("frame controller exited")

        logger.debug (threading.active_count())
        logger.debug (threading.enumerate())

        try:
            frm.Close()
            frm.Destroy()
        except Exception:
            logger.error("Could not destroy frame: %s" % Exception)

    logger.debug("Exiting normally")
    sys.exit(0)

if __name__ == '__main__' :
    main(sys.argv[1:3])