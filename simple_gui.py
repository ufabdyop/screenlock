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
        #os.startfile(path)
        p = subprocess.Popen(path)
        self.pid = p.pid
        print "self.pid"
        print self.pid
        print
    
    def find_window_for_pid(self, pid):
        global result
        result = None
        def callback(hwnd, _):
            global result
            ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
            print "cpid"
            print cpid
            if cpid == pid:
                result = hwnd
                win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,500,500,0)
                print "hwnd"
                print hwnd
                print "result"
                print result
                return False
            return True
        win32gui.EnumWindows(callback, None)
        print "final result"
        print result
        print
        return result    
    
    def show(self):  
        hwnd = self.find_window_for_pid(self.pid)  
        #win32gui.SetForegroundWindow (hwnd)  
        #win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,500,500,0)
        
     
           
#end RunProgram class
#=======================================================
    
if __name__ == '__main__' :
    
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()
    runP = RunProgram()
    time.sleep (2)
    runP.show()
    windowList = []
    win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd),hwnd)), windowList)
    print len(windowList)
    for i in windowList:
        print i
    #cmdWindow = [i for i in windowList if 'New Tab - Google Chrome' in i[0].lower()]
    #print len(cmdWindow)
    #win32gui.SetWindowPos(cmdWindow[0][1],win32con.HWND_TOPMOST,0,0,100,100,0)
    app.MainLoop()
    
