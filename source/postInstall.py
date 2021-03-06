from __future__ import print_function
import sys, os, wx, screenlockConfig, subprocess, log, logging, pprint, ConfigParser
from datetime import datetime
import _winreg as wreg

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
ID_SUBMIT = wx.NewId()


class PostInstallFrame(wx.Frame):
    def __init__(self):
        self.logger = logging.getLogger('postInstall')
        self.logger.debug("postInstall started")

        self.config = screenlockConfig.SLConfig()

        wx.Frame.__init__(self, None, title="Post Install",
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetBackgroundColour('#ffffff')

        font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        xPos = 10
        yPos = 10

        self.startScreenLockCheckbox = wx.CheckBox(self, -1, label="Start ScreenlockServer Upon Login",
                                                   pos=(xPos, yPos), size=(400, 30))
        self.startScreenLockCheckbox.SetFont(font)
        yPos += 35

        self.readmeCheckbox = wx.CheckBox(self, -1, label="Open post-install file", pos=(xPos, yPos),
                                          size=(400, 30))
        self.readmeCheckbox.SetFont(font)
        yPos += 32

        self.setCoralCheckbox = wx.CheckBox(self, -1, label="Use OpenCoral Client", pos=(xPos, yPos), size=(400, 30))
        self.setCoralCheckbox.SetFont(font)
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

    def OnRB(self, event):
        if (event.GetEventObject().GetValue() == False):
            event.GetEventObject().SetValue(1)

    def OnCancel(self, event):
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
                               "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, wreg.KEY_ALL_ACCESS)
            # Create new value
            wreg.SetValueEx(key, 'startScreenlockServer', 0, wreg.REG_SZ, server)
            key.Close()

        if self.readmeCheckbox.IsChecked():
            path = self.config.get('post-install')
            os.startfile(path)
            self.logger.debug(str(datetime.now()) + ' Postinstall: post-install.txt Opened')

        try:
            if self.setCoralCheckbox.IsChecked():
                self.config.writeKey('true', 'use_client')
                self.logger.debug(str(datetime.now()) + ' Postinstall: \'coral\' has been updated to \'true\'')
            else:
                self.config.writeKey('', 'use_client')
                self.logger.debug(str(datetime.now()) + ' Postinstall: \'coral\' has been updated to \'false\'')

        except Exception as e:
            self.logger.debug(str(datetime.now()) + ' Postinstall: ' + str(e))

        oldPassword = self.oldPasswordInputField.GetValue()
        newPassword = self.newPasswordInputField.GetValue()
        confirmPassword = self.confirmPasswordInputField.GetValue()
        newWebPassword = self.newWebPasswordInputField.GetValue()
        confirmWebPassword = self.confirmWebPasswordInputField.GetValue()

        self.write_new_password(oldPassword, newPassword, confirmPassword, newWebPassword, confirmWebPassword)
        writeComments()

    def write_new_password(self, oldPassword, newPassword, confirmPassword, newWebPassword, confirmWebPassword):

        #check if they are providing a new password
        if newPassword == confirmPassword and newPassword == "":
            self.logger.debug("No admin password provided")
            print( self.config.readPassword('admin_override').strip() )

            #seems they are not providing a password
            if self.config.readPassword('admin_override').strip() == "":
                self.errorMessage('Please Set an Admin Password!')
                self.logger.debug("error: Please Set an Admin Password!")
                return

        #check if they are providing a new web password
        elif newWebPassword == confirmWebPassword and newWebPassword == "":
            #seems they are not providing a password
            if self.config.readPassword('web_password').strip() == "":
                self.errorMessage('Please Set a Web Password!')
                self.logger.debug("error: Please Set a Web Password!")
                return

        elif self.config.passwordCheck(oldPassword, 'admin_override') == False:
            self.errorMessage('Wrong Current Admin Password!')
            self.logger.debug("error: Wrong Current Admin Password!")
            return

        #at this point we know that they passed password check and either a new password, or web, or both are set
        if newPassword != confirmPassword:
            self.errorMessage('Admin Password Mismatch!')
            self.logger.debug("Admin Password Mismatch!")
            return

        if newWebPassword != confirmWebPassword:
            self.errorMessage('Web Password Mismatch!')
            self.logger.debug("Web Password Mismatch!")
            return

        try:
            if newPassword:
                self.config.writePassword(newPassword.strip(), 'admin_override')
            if newWebPassword:
                self.config.writePassword(newWebPassword.strip(), 'web_password')
            self.message('Saved New Password(s)')
            self.logger.debug("Saved New Password(s)")
            self.Close()
        except Exception as e:
            self.logger.error(pprint.pformat(e))
            self.errorMessage("Error Saving Password!")

    def errorMessage(self, message):
        self.status.SetLabel(message)

    def message(self, message):
        self.status.SetLabel(message)

def makeConfigFileIfNeeded():
    if os.path.isfile("config.ini") == False:
        newConfig = ConfigParser.ConfigParser()
        configFile = open("config.ini", 'w')
        newConfig.add_section('Section')
        newConfig.set('Section', 'front_window', 'javaws.exe http://coral.nanofab.utah.edu/coral/etc/coral.jnlp')
        newConfig.set('Section', 'keysblock', 'blockKeys.exe')
        newConfig.set('Section', 'post-install', 'post-install.txt')
        newConfig.set('Section', 'test_connection_url', 'http://coral.nanofab.utah.edu/coral/etc/')
        newConfig.set('Section', 'port', '9092')
        newConfig.set('Section', 'admin_override', '')
        newConfig.set('Section', 'web_password', '')
        newConfig.set('Section', 'use_client', '')
        newConfig.set('Section', 'coral_sleep_delay', '6')
        newConfig.set('Section', 'max_coral_open_attempts', '3')
        newConfig.set('Section', 'cert', 'cert.pem')
        newConfig.set('Section', 'key', 'key.pem')
        newConfig.set('Section', 'opacity', '240')

        newConfig.add_section('SubHosts')
        newConfig.set('SubHosts', 'names', '')
        newConfig.set('SubHosts', 'schemas', '')
        newConfig.set('SubHosts', 'ports', '')

        newConfig.write(configFile)
        configFile.close()
        writeComments()

def writeComments():
        with open("config.ini", "a") as f1:
            f1.write("\n")
            f1.write("""
;multiple subhosts can be defined like so:
;names = 155.98.11.50,155.98.11.49,155.98.11.48
;schemas = http,http,http
;ports = 9200,9200,9200

;You can override opacity (from 0 to 255):
opacity = 240

;You can override window ordering with config items like the following:
;[WindowOrder]
;win0 = Notepad
;win0 = Run Data Collector
;win1 = Warning
;win2 = Error
;win3 = Confirm Enable
;win4 = Machine
;win5 = Coral
;win6 = Screen Saver
;win7 = Application Update
;win8 = Transparent Window
            """)

# =======================================================#


if __name__ == '__main__':
    makeConfigFileIfNeeded()
    log.create_log_folder()
    log.initialize_logging('postInstall')
    app = wx.App(False)
    frm = PostInstallFrame()
    frm.Show()
    app.MainLoop()

