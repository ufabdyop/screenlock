from __future__ import print_function
import os, wx, screenlockConfig, log
from datetime import datetime

ID_SUBMIT = wx.NewId()

class PasswordChangeFrame( wx.Frame ):
 
    def __init__( self ):

        self.config = screenlockConfig.SLConfig()
 
        wx.Frame.__init__( self, None, title="Set Screenlock Password",
                           style=wx.DEFAULT_FRAME_STYLE )
        self.SetBackgroundColour('#CCCCCC')
        
        font=wx.Font(16,wx.DECORATIVE,wx.NORMAL,wx.BOLD)

        xPos = 10
        yPos = 10

        #section 1: local screen password
        self.section1Label = wx.StaticText(self, label="Section 1: Change the local screen admin password   ", pos=(xPos,yPos))
        self.section1Label.SetFont(font)
        self.section1Label.SetForegroundColour(wx.BLUE)
        yPos += 50
        
        #Old Password
        self.oldPasswordLabel = wx.StaticText(self, label="Enter Current Admin Password:", pos=(xPos,yPos))
        self.oldPasswordLabel.SetFont(font)
        yPos += 35
        self.oldPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(xPos,yPos), name="input", style=wx.TE_PASSWORD)
        self.oldPasswordInputField.SetFont(font)
        self.oldPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        yPos += 35

        #New Password
        self.newPasswordLabel = wx.StaticText(self, label="Set New Admin Password:",  pos=(xPos,yPos))
        self.newPasswordLabel.SetFont(font)
        yPos += 35
        self.newPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30),  pos=(xPos,yPos), name="input", style=wx.TE_PASSWORD)
        self.newPasswordInputField.SetFont(font)
        self.newPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        yPos += 35
        
        #Confirm New Password
        self.confirmPasswordLabel = wx.StaticText(self, label="Confirm New Admin Password:",  pos=(xPos,yPos))
        self.confirmPasswordLabel.SetFont(font)
        yPos += 35
        self.confirmPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30),  pos=(xPos,yPos), name="input", style=wx.TE_PASSWORD)
        self.confirmPasswordInputField.SetFont(font)
        self.confirmPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        yPos += 65     
        
        #section 2: admin web password
        self.section2Label = wx.StaticText(self, label="Section 2: Change the admin web password   ", pos=(xPos,yPos))
        self.section2Label.SetFont(font)
        self.section2Label.SetForegroundColour(wx.BLUE)
        yPos += 50
        
        #New web Password
        self.newWebPasswordLabel = wx.StaticText(self, label="Set New Web Password:",  pos=(xPos,yPos))
        self.newWebPasswordLabel.SetFont(font)
        yPos += 35
        self.newWebPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30),  pos=(xPos,yPos), name="input", style=wx.TE_PASSWORD)
        self.newWebPasswordInputField.SetFont(font)
        self.newWebPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        yPos += 35
        
        #Confirm New web Password
        self.confirmWebPasswordLabel = wx.StaticText(self, label="Confirm New Web Password:",  pos=(xPos,yPos))
        self.confirmWebPasswordLabel.SetFont(font)
        yPos += 35
        self.confirmWebPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30),  pos=(xPos,yPos), name="input", style=wx.TE_PASSWORD)
        self.confirmWebPasswordInputField.SetFont(font)
        self.confirmWebPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
        yPos += 55
        
        self.submitbutton = wx.Button(self, ID_SUBMIT, 'Submit', pos=(xPos,yPos))
        self.submitbutton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.input = None
        yPos += 50
        
        self.status = wx.StaticText(self, -1, '', pos=(xPos,yPos))
        self.status.SetFont(font)
        self.status.SetForegroundColour(wx.RED)

        self.Fit()

    def OnTab(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_TAB:
            self.NextFocus()
        event.Skip()

    def NextFocus(self):
        currentFocus = wx.Window.FindFocus()
        if currentFocus == self.oldPasswordInputField:
            self.newPasswordInputField.SetFocus()
        elif currentFocus == self.newPasswordInputField:
            self.confirmPasswordInputField.SetFocus()
        elif currentFocus == self.confirmPasswordInputField:
            self.newWebPasswordInputField.SetFocus()
        elif currentFocus == self.newWebPasswordInputField:
            self.confirmWebPasswordInputField.SetFocus()
        elif currentFocus == self.confirmWebPasswordInputField:
            self.oldPasswordInputField.SetFocus()
            
    def OnSubmit(self, event):
        oldPassword = self.oldPasswordInputField.GetValue()
        newPassword = self.newPasswordInputField.GetValue()
        confirmPassword = self.confirmPasswordInputField.GetValue()
        newWebPassword = self.newWebPasswordInputField.GetValue()
        confirmWebPassword = self.confirmWebPasswordInputField.GetValue()
        
        if self.config.passwordCheck(oldPassword, 'admin_override') == False:
            self.errorMessage('Wrong Current Admin Password!')            
        elif newPassword.strip() == "":
            self.errorMessage('Empty Admin Password!')
        elif newPassword != confirmPassword:
            self.errorMessage('Admin Password Mismatch!')
        elif newWebPassword.strip() == "":
            self.errorMessage('Empty Web Password!')
        elif newWebPassword != confirmWebPassword:
            self.errorMessage('Web Password Mismatch!')
        else:
            try:
                self.config.writePassword(newPassword, 'admin_override')
                self.config.writePassword(newWebPassword, 'web_password')
                self.message('Saved New Passwords')
            except Exception, e:
                logFile = open(log.create_log_file('setAdminPassword'), "a")
                print (str(datetime.now()) + "  setAdminPassword: {}".format(str(e)),file = logFile)
                logFile.close()
                
    def errorMessage(self, message):
        self.status.SetLabel(message)

    def message(self, message):
        self.status.SetLabel(message)
        
#=======================================================
    
if __name__ == '__main__' :
    app = wx.App( False )
    frm = PasswordChangeFrame()
    frm.Show()
    app.MainLoop()
    
