import wx, ConfigParser, win32gui, win32process, win32con, subprocess, time
from threading import *
import base64 

ID_SUBMIT = wx.NewId()

class OverlayFrame( wx.Frame )  :
 
    def __init__( self )  :
 
        wx.Frame.__init__( self, None, title="Transparent Window",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )
        self.ShowFullScreen( True )
        self.SetBackgroundColour('#CCE8CF')
        
        font=wx.Font(16,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        self.label = wx.StaticText(self, label="For Administrator Only:", pos=(10,10))
        self.label.SetFont(font)
        
        self.inputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(10,45), name="input",  style=wx.TE_PASSWORD)
        self.inputField.SetFont(font)
        
        self.submitbutton = wx.Button(self, ID_SUBMIT, 'Submit', pos=(160,50))
        self.submitbutton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.input = None
        
    def OnSubmit(self, event):
        self.input = self.inputField.GetValue()
        encrypt = base64.encodestring(self.input) 
        print encrypt
        fp = open(r'config.ini')
        config = ConfigParser.ConfigParser()
        config.readfp(fp)
        fp.close()
        pw = config.get('Section', 'front_window')
        # if encrypt == pw,destroy window, may do more on encrypt 
        # else display error message
        # close thread?
        # input: do limitation
        
    def OnCloseWindow( self, evt ) :
        self.Destroy()
    
#end OverlayFrame class

    
# a method to be invoked by ControlFrameThread    
def makeProgramAtFront():
    def callback(hwnd, _):
        if win32gui.GetWindowText(hwnd).find("Warning")!= -1:
            win32gui.SetWindowPos(hwnd,win32con.HWND_TOP,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )    
        elif win32gui.GetWindowText(hwnd).find("Coral")!= -1:
            global checkCoralOpen
            checkCoralOpen = True
            win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )    
        return True
    try:
        win32gui.EnumWindows(callback, None)
        global checkCoralOpen
        if not checkCoralOpen:
            openCoral()
    except:
        pass
                     
def openCoral ():
    fp = open(r'config.ini')
    config = ConfigParser.ConfigParser()
    config.readfp(fp)
    fp.close()
    path = config.get('Section', 'front_window')
    subprocess.Popen(path)
    time.sleep (5)

# a thread class to do the infinite loop to make sure the
# Coral window at the most front
class ControlFrameThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        while True:
            global checkCoralOpen
            checkCoralOpen = False
            makeProgramAtFront()
            time.sleep(1)
        
#=======================================================
    
if __name__ == '__main__' :
    
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()
    thread = ControlFrameThread()

    app.MainLoop()
