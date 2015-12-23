import sys, os, wx, screenlockConfig, subprocess, log
from datetime import datetime
import _winreg as wreg

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
ID_SUBMIT = wx.NewId()


class PostInstallFrame( wx.Frame ):
 
    def __init__( self ):

        self.config = screenlockConfig.SLConfig()
 
        wx.Frame.__init__( self, None, title= "Post Install",
                           style=wx.DEFAULT_FRAME_STYLE )
        self.SetBackgroundColour('#CCCCCC')
        
        font=wx.Font(14,wx.DECORATIVE,wx.NORMAL,wx.BOLD)

        xPos = 10
        yPos = 10

        self.startScreenLockCheckbox = wx.CheckBox(self, -1, label="Start ScreenlockServer Upon Login", pos = (xPos,yPos), size = (400, 20))
        self.startScreenLockCheckbox.SetFont(font)
        yPos += 35
        
        self.readmeCheckbox = wx.CheckBox(self, -1, label="Open post-install file", pos = (xPos,yPos), size = (400, 20))
        self.readmeCheckbox.SetFont(font)
        yPos += 35
        
        self.setPasswordCheckbox = wx.CheckBox(self, -1, label="Set Administrator and Web Passwords", pos = (xPos,yPos), size = (400, 20))
        self.setPasswordCheckbox.SetFont(font)
        yPos += 35
        

        self.setCoralRadioBtn = wx.RadioButton(self,label= "Coral", pos = (xPos,yPos), size = (400, 20), style = wx.RB_GROUP)
        self.setCoralRadioBtn.SetFont(font)
        self.setCoralRadioBtn.Bind(wx.EVT_LEFT_DOWN,self.OnRB)
        yPos += 20
        
        self.setBlankRadioBtn = wx.RadioButton(self, label = "No Client", pos = (xPos,yPos), size = (400,20))
        self.setBlankRadioBtn.SetFont(font)
        self.setBlankRadioBtn.Bind(wx.EVT_LEFT_DOWN,self.OnRB)
        yPos += 35
        
        self.OKbutton = wx.Button(self, ID_SUBMIT, label='OK', pos=(xPos + 250,yPos))
        self.OKbutton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.input = None

        self.CancelBtn = wx.Button(self, label = 'Cancel', pos=(xPos + 350,yPos))
        self.CancelBtn.SetFont(font)
        self.CancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        yPos += 50

        self.Fit()

    def OnRB(self,event):
        if (event.GetEventObject().GetValue() == False):
            event.GetEventObject().SetValue(1)
            
    def OnCancel(self,event):
        sys.exit()

    def OnSubmit(self, event):
        if self.startScreenLockCheckbox.IsChecked():
            server = os.path.join(PATH, 'screenlockServer.exe')
            key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",0, wreg.KEY_ALL_ACCESS)
            # Create new value
            wreg.SetValueEx(key, 'startScreenlockServer', 0, wreg.REG_SZ, server)
            key.Close()

        if self.readmeCheckbox.IsChecked():
            path = self.config.get('post-install')
            os.startfile(path)
            print str(datetime.now()) + '   Postinstall: post-install.txt Opened'

        if self.setPasswordCheckbox.IsChecked():
            path = self.config.get('setAdminPsw')
            print str(datetime.now()) + '   Postinstall: Set Passwords Opened'
            self.p = subprocess.Popen(path)
        try:
            if self.setCoralRadioBtn.GetValue():
                self.config.writeKey('true','coral')
                print str(datetime.now()) + '   Postinstall: \'coral\' has been updated to \'true\''
            else:
                self.config.writeKey('false','coral')
                print str(datetime.now()) + '   Postinstall: \'coral\' has been updated to \'false\''
        except Exception, e:
            print str(datetime.now()) + '   Postinstall: ' + str(e)
        sys.exit()
        
#=======================================================#


if __name__ == '__main__' :
    log.create_log_folder()
    logFile = open(log.create_log_file('postInstall'), "a")
    sys.stdout = logFile
    app = wx.App( False )
    frm = PostInstallFrame()
    frm.Show()
    app.MainLoop()
    logFile.close()
    
