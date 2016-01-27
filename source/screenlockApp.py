from __future__ import print_function
import wx, thread, time, win32api, win32gui, win32con, \
    subprocess, signal, screenlockConfig,urllib2, log, os, logging
from threading import *
from datetime import datetime

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
        makeCoralNotTopMost()
        self.Destroy()

    def OnSubmit(self, event):
        self.input = self.inputField.GetValue()
        self.inputField.Clear()
        global config
        if config.passwordCheck(self.input, 'admin_override'):
            global endFlag
            endFlag = True
            self.keyBlockerProcess.send_signal(signal.SIGTERM)
            makeCoralNotTopMost()
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


def bottomTaskManageWindow():
    logger = logging.getLogger("bottomTaskManageWindow")
    global endFlag
    while not endFlag:   
        time.sleep(0.1)
        taskwindow = getWindow("Windows Task Manager")
        if taskwindow:
            try:
                win32gui.SetWindowPos(taskwindow["Windows Task Manager"],win32con.HWND_BOTTOM,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
            except:
                logger.error (str(datetime.now()) + " screenlockApp: Windows Task Manager may not exist.")
    return
            

def getWindow(*args):
    windows = {}
    logger = logging.getLogger("screenlockApp")

    def callback(hwnd, _):
        for windowtext in args:
            if win32gui.GetWindowText(hwnd).find(windowtext)!= -1:
                if windowtext == 'Run Data Collector' and not win32gui.IsWindowVisible(hwnd):
                    continue
                if windowtext in windows:
                    continue
                windows[windowtext] = hwnd
        return True
    try:
        win32gui.EnumWindows(callback, None)
    except:
        logger.error (str(datetime.now()) + "  screenlockApp: getWindow error.")
    if len(windows) > 0 :
        return windows
    return None
    
def makeCoralNotTopMost():
    coralWindow = getWindow("Coral")
    logger = logging.getLogger("screenlockApp")
    if coralWindow:
        try:
            win32gui.SetWindowPos(coralWindow["Coral"],win32con.HWND_NOTOPMOST,0,0,500,500, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
        except:
            logger.error (str(datetime.now()) + " screenlockApp makeCoralNotTopMost: Coral window may not exist.")

# a method to be invoked by ControlFrameThread    
def makeProgramAtFront():
    def makeWindowTopmost(windowHwnd):
        win32gui.SetWindowPos(windowHwnd,win32con.HWND_TOPMOST,0,0,500,500, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
    global coral
    logger = logging.getLogger("screenlockApp")
    if (coral == 'true'):
        windows = getWindow("Run Data Collector", "Warning", "Error","Coral", "Screen Saver", "Application Update")
    else:
        windows = getWindow("Warning","Error","Screen Saver")
    global checkCoralOpen
    try:
        if windows:
            if "Warning" in windows:
                checkCoralOpen = True
                makeWindowTopmost(windows["Warning"])
            elif "Error" in windows:
                checkCoralOpen = True
                makeWindowTopmost(windows["Error"])
            elif "Coral" in windows:
                checkCoralOpen = True
            if "Application Update" in windows:
                checkCoralOpen = True
                makeWindowTopmost(windows["Application Update"])
            elif checkCoralOpen:
                makeWindowTopmost(windows["Coral"])
            if "Run Data Collector" in windows:
                makeWindowTopmost(windows["Run Data Collector"])
            if "Screen Saver" in windows:
                makeWindowTopmost(windows["Screen Saver"])
    except:
        logger.error (str(datetime.now()) + " screenlockApp makeProgramAtFront: window may not exist.")
    if not checkCoralOpen and coral == 'true':
        openCoral()
        
   
def openCoral ():
    global config, endFlag
    logger = logging.getLogger("screenlockApp")
    path = config.get('front_window')
    internet_flag = internetOn()
    while (not internet_flag) and (not endFlag):
        logger.error (str(datetime.now()) + " screenlockApp: NO internet.")
        time.sleep(2)
        internet_flag = internetOn()
    subprocess.Popen(path)
    time.sleep (6)
    
def internetOn():
    logger = logging.getLogger("screenlockApp")

    try:
        global config
        test_connection_url = config.get('test_connection_url')
        response = urllib2.urlopen(test_connection_url,timeout=1)
        return True
    except urllib2.URLError as err: 
        logger.error (str(datetime.now()) + " screenlockApp: " + str(err))
    return False

# a thread class to do the infinite loop to make sure the
# Coral window at the most front
class ControlFrameThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        global endFlag
        while not endFlag:
            global checkCoralOpen
            checkCoralOpen = False
            makeProgramAtFront()
            time.sleep(1)
        return
        
#=======================================================

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
    newthread = ControlFrameThread()
    thread.start_new_thread(bottomTaskManageWindow, ())
    app.MainLoop()
