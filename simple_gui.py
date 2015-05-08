import wx, ConfigParser, os, win32gui, win32process, win32con, subprocess, time

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
    
class RunProgram ( ):
    def __init__ (self):
        self.openCoral()
        
    def openCoral (self):
        print 
        # config = ConfigParser.ConfigParser()
#         config.readfp(open(r'config.ini'))
#         path = config.get('Section', 'front_window')
#         subprocess.Popen(path)
#         time.sleep (3)
        
    def makeProgramInFront(self):
        def callback(hwnd, _):
            if win32gui.GetWindowText(hwnd).find("Coral")!= -1 :
                win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )    
                return False
            return True
        try:
            win32gui.EnumWindows(callback, None)
            #return True
        except:
            pass
            #return False

           
#end RunProgram class
#=======================================================
    
if __name__ == '__main__' :
    
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()
    runP = RunProgram()
    windowList = []
    win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd),hwnd)), windowList)
    for i in windowList:
        print i
    cmdWindow = [i for i in windowList if i[0].find("Coral")!= -1]
    print len(cmdWindow)
    while True:
        runP.makeProgramInFront()
        #if runP.makeProgramInFront():
            #time.sleep(2)
    app.MainLoop()
    
