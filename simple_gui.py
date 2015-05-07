import wx, ConfigParser, os, win32gui, win32process, win32con, subprocess

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
#=======================================================
 
if __name__ == '__main__' :
 
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'config.ini'))
    path = config.get('Section', 'front_window')
    print (path)
    #os.startfile(path)
    p = subprocess.Popen(path)
    windowList = []
    win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd),hwnd)), windowList)
    print len(windowList)
    for i in windowList:
        print i
#     cmdWindow = [i for i in windowList if path in i[0].lower()]
#     print len(cmdWindow)
#     win32gui.SetWindowPos(hwnd1,win32con.HWND_TOPMOST,0,0,100,100,0)
    app.MainLoop()
    
