from __future__ import print_function
import sys, os, wx, screenlockConfig, log, logging, subprocess, pprint
from datetime import datetime
import _winreg as wreg

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
ID_SUBMIT = wx.NewId()
global username, password

class PostInstallFrame( wx.Frame ):

    def __init__(self):
            self.logger = logging.getLogger('userLock')
            self.logger.debug("userLock started")

            self.config = screenlockConfig.SLConfig()

            wx.Frame.__init__(self, None, title="Screenlock for User",
                              style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, size=(300, 300))

            self.SetBackgroundColour('#ffffff')

            font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

            xPos = 10
            yPos = 10

            # Name
            self.nameLable = wx.StaticText(self, label="Enter your name:", pos=(xPos, yPos))
            self.nameLable.SetFont(font)
            yPos += 25
            self.nameField = wx.TextCtrl(self, value="", size=(200, 30), pos=(xPos, yPos), name="input")
            self.nameField.SetFont(font)
            self.nameField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 40

            # Password
            self.passwordLabel = wx.StaticText(self, label="Enter temporary password:", pos=(xPos, yPos))
            self.passwordLabel.SetFont(font)
            yPos += 25
            self.passwordInputField = wx.TextCtrl(self, value="", size=(200, 30), pos=(xPos, yPos), name="input",
                                                     style=wx.TE_PASSWORD)
            self.passwordInputField.SetFont(font)
            self.passwordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 40

            # Re-enter Password
            self.confirmPasswordLabel = wx.StaticText(self, label="Re-enter password:", pos=(xPos, yPos))
            self.confirmPasswordLabel.SetFont(font)
            yPos += 25
            self.confirmPasswordInputField = wx.TextCtrl(self, value="", size=(200, 30), pos=(xPos, yPos), name="input",
                                                  style=wx.TE_PASSWORD)
            self.confirmPasswordInputField.SetFont(font)
            self.confirmPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)
            yPos += 40

            self.status = wx.StaticText(self, -1, '', pos=(xPos, yPos))
            self.status.SetFont(font)
            self.status.SetForegroundColour(wx.RED)
            yPos += 30

            self.OKbutton = wx.Button(self, ID_SUBMIT, label='OK', pos=(xPos + 40, yPos))
            self.OKbutton.SetFont(font)
            self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
            self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
            self.input = None

            self.CancelBtn = wx.Button(self, label='Cancel', pos=(xPos + 140, yPos))
            self.CancelBtn.SetFont(font)
            self.CancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
            yPos += 20

            self.empty = wx.StaticText(self, -1, '', pos=(xPos, yPos))

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
        if currentFocus == self.nameField:
            self.passwordInputField.SetFocus()
        elif currentFocus == self.passwordInputField:
            self.confirmPasswordInputField.SetFocus()

    def OnSubmit(self, event):
        global username, password
        passwordVal = self.passwordInputField.GetValue()
        confirmPassVal = self.confirmPasswordInputField.GetValue()

        if self.nameField.GetValue() == "":
            self.errorMessage('Empty Name Field!')
        elif passwordVal == "":
            self.errorMessage('Empty Password Field!')
        elif confirmPassVal == "":
            self.errorMessage('Please re-enter password!')
        elif passwordVal != confirmPassVal:
            self.errorMessage('Password Mismatch!')
        else:
            username = self.nameField.GetValue()
            password = passwordVal
            self.message('Saved Password!')
            self.Close()

    def errorMessage(self, message):
        self.status.SetLabel(message)

    def message(self, message):
        self.status.SetLabel(message)


#=======================================================#


if __name__ == '__main__' :
    global username, password
    log.create_log_folder()
    log.initialize_logging('userLock')
    app = wx.App( False )
    frm = PostInstallFrame()
    frm.Show()
    app.MainLoop()
    import screenlockApp
    screenlockApp.main([username, password])