import wx, thread, time, win32api, win32gui, win32con, subprocess, signal, screenlockConfig,urllib2
from threading import *

global endFlag
endFlag = False

global config
config = screenlockConfig.SLConfig()

ID_SUBMIT = wx.NewId()

class OverlayFrame( wx.Frame ):
 
    def __init__( self )  :
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
        
        self.submitbutton = wx.Button(self, ID_SUBMIT, 'Submit', pos=(160,50))
        self.submitbutton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.input = None
        
        self.status = wx.StaticText(self, -1, '', pos=(10,80))
        self.status.SetFont(font)

        win32api.SetConsoleCtrlHandler(self.signal_handler, True)
        
        self.openKeysBlock ()
        try:
            thread.start_new_thread(self.deleteLabel, (self.status,))
        except:
            print ("Can not start a new thread.")

    def signal_handler(self, signalNumber):
        if self.p.pid:
            self.p.send_signal(signal.SIGTERM)
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
            self.p.send_signal(signal.SIGTERM)
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
        self.p = subprocess.Popen(path)


#end OverlayFrame class        


def bottomTaskManageWindow():
    global endFlag
    while not endFlag:   
        time.sleep(0.1)
        taskwindow = getWindow("Windows Task Manager")
        if taskwindow:
            try:
                win32gui.SetWindowPos(taskwindow["Windows Task Manager"],win32con.HWND_BOTTOM,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
            except:
                print ("Error: window may not exist.")
    return
            

def getWindow(*args):
    windows = {}
    def callback(hwnd, _):
        for windowtext in args:
            if win32gui.GetWindowText(hwnd).find(windowtext)!= -1:
                if windowtext in windows:
                    continue
                windows[windowtext] = hwnd
        return True
    try:
        win32gui.EnumWindows(callback, None)
    except:
        pass
    if len(windows) > 0 :
        return windows
    return None
    
def makeCoralNotTopMost():
    coralWindow = getWindow("Coral")
    if coralWindow:
        try:
            win32gui.SetWindowPos(coralWindow["Coral"],win32con.HWND_NOTOPMOST,0,0,500,500, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
        except:
            print ("Error: Window may not exist.")
                  
# a method to be invoked by ControlFrameThread    
def makeProgramAtFront():
    windows = getWindow("Run Data Collector", "Warning", "Error","Coral", "Screen Saver")
    global checkCoralOpen
    try:
        if windows:
            if "Warning" in windows:
                win32gui.SetWindowPos(windows["Warning"],win32con.HWND_TOPMOST,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
            if "Error" in windows:
                win32gui.SetWindowPos(windows["Error"],win32con.HWND_TOPMOST,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
            if "Coral" in windows:
                checkCoralOpen = True
                win32gui.SetWindowPos(windows["Coral"],win32con.HWND_TOPMOST,0,0,500,500, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
            if "Run Data Collector" in windows:
                win32gui.SetWindowPos(windows["Run Data Collector"],win32con.HWND_TOPMOST,0,0,500,500, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
            if "Screen Saver" in windows:
                win32gui.SetWindowPos(windows["Screen Saver"],win32con.HWND_TOPMOST,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
    except:
        print "Error: window may not exist."
    if not checkCoralOpen:
        openCoral()
        
   
def openCoral ():
    global config, endFlag
    path = config.get('front_window')
    internet_flag = internet_on()
    while (not internet_flag) and (not endFlag):
        print "No Internet"
        time.sleep(2)
        internet_flag = internet_on()
    subprocess.Popen(path)
    time.sleep (6)
    
def internet_on():
    try:
        response = urllib2.urlopen('https://coral.nanofab.utah.edu/',timeout=1)
        return True
    except urllib2.URLError as err: pass
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
    
if __name__ == '__main__' :
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()
    newthread = ControlFrameThread()
    thread.start_new_thread(bottomTaskManageWindow, ())
    app.MainLoop()
