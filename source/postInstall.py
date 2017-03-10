from __future__ import print_function
import sys, os, wx, screenlockConfig, subprocess, log, logging, pprint
from datetime import datetime
import _winreg as wreg

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
ID_SUBMIT = wx.NewId()


class PostInstallFrame( wx.Frame ):

    def __init__(self):
            self.logger = logging.getLogger('postInstall')
            self.logger.debug("postInstall started")

            self.config = screenlockConfig.SLConfig()

            wx.Frame.__init__(self, None, title="Post Install",
                              style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
            self.SetBackgroundColour('#ffffff')

            font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

            xPos = 10
            yPos = 10

            self.startScreenLockCheckbox = wx.CheckBox(self, -1, label="Start ScreenlockServer Upon Login" ,
                                                       pos=(xPos, yPos), size=(400, 30))
            self.startScreenLockCheckbox.SetFont(font)
            yPos += 35

            self.readmeCheckbox = wx.CheckBox(self, -1, label="Open post-install file", pos=(xPos, yPos),
                                              size=(400, 30))
            self.readmeCheckbox.SetFont(font)
            yPos += 32

            self.setCoralRadioBtn = wx.CheckBox(self, label="Use OpenCoral Client", pos=(xPos, yPos), size=(400, 30),
                                                   style=wx.RB_GROUP)
            self.setCoralRadioBtn.SetFont(font)
            self.setCoralRadioBtn.Bind(wx.EVT_LEFT_DOWN, self.OnRB)
            yPos += 50

            # section 1: local screen password
            self.section1Label = wx.StaticText(self, label="Section 1: Change the local screen admin password   ",
                                               pos=(xPos, yPos))
            self.section1Label.SetFont(font)
            self.section1Label.SetForegroundColour(wx.BLUE)
            yPos += 35

            # Old Password
            self.oldPasswordLabel = wx.StaticText(self, label="Enter Current Admin Password:", pos=(xPos, yPos))
            self.oldPasswordLabel.SetFont(font)
            yPos += 25
            self.oldPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(xPos, yPos), name="input",
                                                     style=wx.TE_PASSWORD)
            self.oldPasswordInputField.SetFont(font)
            self.oldPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 40

            # New Password
            self.newPasswordLabel = wx.StaticText(self, label="Set New Admin Password:", pos=(xPos, yPos))
            self.newPasswordLabel.SetFont(font)
            yPos += 25
            self.newPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(xPos, yPos), name="input",
                                                     style=wx.TE_PASSWORD)
            self.newPasswordInputField.SetFont(font)
            self.newPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 40

            # Confirm New Password
            self.confirmPasswordLabel = wx.StaticText(self, label="Confirm New Admin Password:", pos=(xPos, yPos))
            self.confirmPasswordLabel.SetFont(font)
            yPos += 25
            self.confirmPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(xPos, yPos), name="input",
                                                         style=wx.TE_PASSWORD)
            self.confirmPasswordInputField.SetFont(font)
            self.confirmPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 65

            # section 2: admin web password
            self.section2Label = wx.StaticText(self, label="Section 2: Change the admin web password   ",
                                               pos=(xPos, yPos))
            self.section2Label.SetFont(font)
            self.section2Label.SetForegroundColour(wx.BLUE)
            yPos += 35

            # New web Password
            self.newWebPasswordLabel = wx.StaticText(self, label="Set New Web Password:", pos=(xPos, yPos))
            self.newWebPasswordLabel.SetFont(font)
            yPos += 25
            self.newWebPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(xPos, yPos), name="input",
                                                        style=wx.TE_PASSWORD)
            self.newWebPasswordInputField.SetFont(font)
            self.newWebPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 40

            # Confirm New web Password
            self.confirmWebPasswordLabel = wx.StaticText(self, label="Confirm New Web Password:", pos=(xPos, yPos))
            self.confirmWebPasswordLabel.SetFont(font)
            yPos += 25
            self.confirmWebPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(xPos, yPos),
                                                            name="input", style=wx.TE_PASSWORD)
            self.confirmWebPasswordInputField.SetFont(font)
            self.confirmWebPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 35

            self.status = wx.StaticText(self, -1, '', pos=(xPos, yPos))
            self.status.SetFont(font)
            self.status.SetForegroundColour(wx.RED)
            yPos += 30

            self.OKbutton = wx.Button(self, ID_SUBMIT, label='OK', pos=(xPos + 150, yPos))
            self.OKbutton.SetFont(font)
            self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
            self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
            self.input = None

            self.CancelBtn = wx.Button(self, label='Cancel', pos=(xPos + 250, yPos))
            self.CancelBtn.SetFont(font)
            self.CancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
            yPos += 20

            self.empty = wx.StaticText(self, -1, '', pos=(xPos, yPos))
            self.Fit()

    def OnRB(self,event):
        if (event.GetEventObject().GetValue() == False):
            event.GetEventObject().SetValue(1)
            
    def OnCancel(self,event):
        sys.exit()

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

        if self.startScreenLockCheckbox.IsChecked():
            server = os.path.join(PATH, 'screenlockServer.exe')
            key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE,
                               "Software\\Microsoft\\Windows\\CurrentVersion\\Run",0, wreg.KEY_ALL_ACCESS)
            # Create new value
            wreg.SetValueEx(key, 'startScreenlockServer', 0, wreg.REG_SZ, server)
            key.Close()

        if self.readmeCheckbox.IsChecked():
            path = self.config.get('post-install')
            os.startfile(path)
            self.logger.debug(str(datetime.now()) + ' Postinstall: post-install.txt Opened')

        try:
            if self.setCoralCheckbox.IsChecked():
                self.config.writeKey('true','coral')
                self.logger.debug( str(datetime.now()) + ' Postinstall: \'coral\' has been updated to \'true\'')
            else:
                self.config.writeKey('false','coral')
                self.logger.debug(str(datetime.now()) + ' Postinstall: \'coral\' has been updated to \'false\'')

        except Exception, e:
            self.logger.debug(str(datetime.now()) + ' Postinstall: ' + str(e))

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
                self.logger.debug("Saved a New Password")
                self.Close()
            except Exception, e:
                self.logger.error(pprint.pformat(e))

    def errorMessage(self, message):
        self.status.SetLabel(message)

    def message(self, message):
        self.status.SetLabel(message)


#=======================================================#


if __name__ == '__main__' :
    log.create_log_folder()
    log.initialize_logging('postInstall')
    app = wx.App( False )
    frm = PostInstallFrame()
    frm.Show()
    app.MainLoop()