import wx, ConfigParser, os, win32gui, win32process, win32con, subprocess, time
from threading import *

class OverlayFrame( wx.Frame )  :
 
    def __init__( self )  :
 
        wx.Frame.__init__( self, None, title="Transparent Window",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )
 
        self.ShowFullScreen( True )
        self.alphaValue = 255
        self.SetTransparent( self.alphaValue )
                
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
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'config.ini'))
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
