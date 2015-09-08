import os,sys, wx, win32gui, win32con, time, thread, win32process, subprocess, ConfigParser, signal, pythoncom, pyHook, psutil, zope.interface
from twisted.internet import protocol, reactor, endpoints
from threading import *
import screenlockConfig, screenlockController, version
from flask import Flask, request, Response
from functools import wraps
from urlparse import urlparse
from OpenSSL import SSL
import json

ID_SUBMIT = wx.NewId()
global endFlag
endFlag = False

class PasswordChangeFrame( wx.Frame ):
 
    def __init__( self ):

        self.config = screenlockConfig.SLConfig()
 
        wx.Frame.__init__( self, None, title="Set Screenlock Password",
                           style=wx.DEFAULT_FRAME_STYLE )
        self.SetBackgroundColour('#CCCCCC')
        
        font=wx.Font(16,wx.DECORATIVE,wx.NORMAL,wx.BOLD)

        xPos = 10
        yPos = 10

        #Old Password
        self.oldPasswordLabel = wx.StaticText(self, label="Enter Current Admin Password:", pos=(xPos,yPos))
        self.oldPasswordLabel.SetFont(font)
        yPos += 35
        self.oldPasswordInputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(xPos,yPos), name="input", style=wx.TE_PASSWORD)
        self.oldPasswordInputField.SetFont(font)
        self.oldPasswordInputField.Bind(wx.EVT_KEY_DOWN, self.OnTab)

        yPos += 55

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

        yPos += 35        
        
        self.submitbutton = wx.Button(self, ID_SUBMIT, 'Submit', pos=(xPos,yPos))
        self.submitbutton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.input = None
        yPos += 35
        
        self.status = wx.StaticText(self, -1, '', pos=(xPos,yPos))
        self.status.SetFont(font)

        self.Fit()
        try:
            thread.start_new_thread(self.deleteLabel, (self.status,))
        except:
            pass

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
            self.oldPasswordInputField.SetFocus()
            
    def OnSubmit(self, event):
        oldPassword = self.oldPasswordInputField.GetValue()
        newPassword = self.newPasswordInputField.GetValue()
        confirmPassword = self.confirmPasswordInputField.GetValue()
        if self.config.passwordCheck(oldPassword, 'admin_override') == False:
            self.errorMessage('Wrong Password!')            
        elif newPassword.strip() == "":
            self.errorMessage('Empty Password!')
        elif newPassword != confirmPassword:
            self.errorMessage('Password Mismatch!')
        else:
            self.config.writePassword(newPassword, 'admin_override')
            self.message('Saved New Password')

    def errorMessage(self, message):
        self.status.SetLabel(message)

    def message(self, message):
        self.status.SetLabel(message)

    def deleteLabel(self,status):
        global endFlag
        while not endFlag:
            time.sleep(5)
            if not endFlag:
                if status.GetLabel() != '' :
                    time.sleep(5)
                    if not endFlag:
                        status.SetLabel('')
        return
#end OverlayFrame class
        
#=======================================================
    
if __name__ == '__main__' :
    app = wx.App( False )
    frm = PasswordChangeFrame()
    frm.Show()
    config = screenlockConfig.SLConfig()
    path = config.get('post-install')
    os.startfile(path)
    app.MainLoop()
    endFlag = True
    
