from __future__ import print_function

import logging
import os
import signal
import subprocess
import thread
import time
import urllib2
from datetime import datetime

import win32api
import win32con
import win32gui
import wx
from screenlockForegrounder import ControlFrameThread

import log
import screenlockConfig
from screenlockTaskManagerHider import TaskManagerHider
from screenlockWindowHelper import getWindow

global endFlag
endFlag = False

global config
config = screenlockConfig.SLConfig()

ID_SUBMIT = wx.NewId()

class OverlayFrame( wx.Frame ):

    def __init__( self )  :
        self.logger=logging.getLogger('screenlockApp')
        self.logger.debug(" screenlockApp: Starting")

        wx.Frame.__init__( self, None, title="Transparent Window",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )

        self.ShowFullScreen( True )
        self.alphaValue = 220
        self.SetTransparent( self.alphaValue )
        self.SetBackgroundColour('#CCE8CF')
        
        font=wx.Font(16,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        self.label = wx.StaticText(self, label="For Administrator Only:", pos=(10,10))
        self.label.SetFont(font)
        
        self.inputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(10,45), name="input", style=wx.TE_PASSWORD)
        self.inputField.SetFont(font)
        
        self.submitButton = wx.Button(self, ID_SUBMIT, 'Submit', pos=(160,50))
        self.submitButton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.input = None
        
        self.status = wx.StaticText(self, -1, '', pos=(10,80))
        self.status.SetFont(font)

        win32api.SetConsoleCtrlHandler(self.signalHandler, True)

        global coral
        global config
        coral = config.get('coral')

        self.openKeysBlock ()
        try:
            thread.start_new_thread(self.deleteLabel, (self.status,))
        except:
            self.logger.error(" screenlockApp: Can not start a new thread to delete Label.")

    def signalHandler(self, signalNumber):
        self.logger.debug("received signal: %s" % signalNumber)
        if self.keyBlockerProcess.pid:
            self.logger.debug("propagating signal")
            self.keyBlockerProcess.send_signal(signal.SIGTERM)
        else:
            self.logger.debug("no keyblocker pid for signal")
        global endFlag
        endFlag = True
        self.Destroy()

    def OnSubmit(self, event):
        self.input = self.inputField.GetValue()
        self.inputField.Clear()
        global config
        if config.passwordCheck(self.input, 'admin_override'):
            global endFlag
            endFlag = True
            self.keyBlockerProcess.send_signal(signal.SIGTERM)
            self.Close()
            self.Destroy()
        else:
            self.status.SetLabel('You are not authorized.')
    
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
        global config
        path = config.get('keysblock')
        if os.path.isfile(path):
            self.logger.debug("blocking keys")
            self.keyBlockerProcess = subprocess.Popen(path)
        else:
            self.keyBlockerProcess = NullProcess()
            self.logger.error("ERROR: Cannot find keysblock from config %s" % path)


#end OverlayFrame class        


class NullProcess(object):
    def __init__(self):
        self.pid = False
        self.logger = logging.getLogger("NullProcess")
    def send_signal(self, sig):
        self.logger.error("NullProcess Received sig: %s" % sig)
    
if __name__ == '__main__' :
    log.initialize_logging('screenlockApp')
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()

    frameController = ControlFrameThread(config.get('front_window'),
                                         config.get('test_connection_url'),
                                         config.get('coral'))
    frameController.start()

    taskmgrController = TaskManagerHider()
    taskmgrController.start()

    app.MainLoop()
    print("main loop exited")

    taskmgrController.stopRunning()
    frameController.stopRunning()

    taskmgrController.join(5)
    print("taskmgr exited")

    frameController.join(5)
    print("frame controller exited")

    frm.Destroy()
    #raise Exception("Just exit!")
