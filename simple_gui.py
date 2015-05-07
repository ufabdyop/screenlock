import wx, ConfigParser, os, win32gui, win32process, win32con, subprocess, time

class OverlayFrame( wx.Frame )  :
 
    def __init__( self )  :
 
        wx.Frame.__init__( self, None, title="Transparent Window",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )
 
        self.ShowFullScreen( True )
        self.alphaValue = 180
        self.SetTransparent( self.alphaValue )
                
    def OnCloseWindow( self, evt ) :
        self.Destroy()
    
#end OverlayFrame class
    
class RunProgram (object):
    def __init__ (self):
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.ini'))
        path = config.get('Section', 'front_window')
        p = subprocess.Popen(path)
        self.pid = p.pid
        print "self.pid"
        print self.pid
        print
    
    def makeProgramInFront(self, pid):
        def callback(hwnd, _):
            ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
            print "cpid"
            print cpid
            if cpid == pid:
                win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,500,500,0)
                print "hwnd"
                print hwnd
                return False
            return True
        win32gui.EnumWindows(callback, None)

           
#end RunProgram class
#=======================================================
    
if __name__ == '__main__' :
    
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()
    runP = RunProgram()
    time.sleep (2)
    runP.makeProgramInFront(runP.pid)
    windowList = []
    win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd),hwnd)), windowList)
    print len(windowList)
    for i in windowList:
        print i
    app.MainLoop()
    
