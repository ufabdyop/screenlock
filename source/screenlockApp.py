global endFlag
endFlag = False

import os, wx, win32gui, win32con, time, thread, win32process, subprocess, ConfigParser, signal, pythoncom, pyHook, psutil
import screenlockConfig
from threading import *
from flask import Flask, request, Response
from functools import wraps

ID_SUBMIT = wx.NewId()
global config
config = screenlockConfig.SLConfig()

class OverlayFrame( wx.Frame )  :
 
    def __init__( self )  :
 
        wx.Frame.__init__( self, None, title="Transparent Window",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )

        self.ShowFullScreen( True )
        self.alphaValue = 220
        self.SetTransparent( self.alphaValue )
        self.SetBackgroundColour('#CCE8CF')
        
        font=wx.Font(16,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        self.label = wx.StaticText(self, label="For Administrator Only:", pos=(10,10))
        self.label.SetFont(font)
        
        self.inputField = wx.TextCtrl(self, value="", size=(140, 30), pos=(10,45), name="input", style=wx.TE_PASSWORD)
        self.inputField.SetFont(font)
        
        self.submitbutton = wx.Button(self, ID_SUBMIT, 'Submit', pos=(160,50))
        self.submitbutton.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.input = None
        
        self.status = wx.StaticText(self, -1, '', pos=(10,80))
        self.status.SetFont(font)
        
        self.openKeysBlock ()
        try:
            thread.start_new_thread(self.deleteLabel, (self.status,))
        except:
            pass
            
    def OnSubmit(self, event):
        
        self.input = self.inputField.GetValue()
        self.inputField.Clear()
        global config
        if config.passwordCheck(self.input):
            global endFlag
            endFlag = True
            self.p.send_signal(signal.SIGTERM)
            self.Destroy()
        else:
            self.status.SetLabel('You are not authorized.')
    
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
        
    def openKeysBlock (self):
        global config
        path = config.get('keysblock')
        self.p = subprocess.Popen(path)
        
#end OverlayFrame class

# a method to be invoked by ControlFrameThread    
def makeProgramAtFront():
    def callback(hwnd, _):
        if win32gui.GetWindowText(hwnd).find("Windows Task Manager")!= -1:
            win32gui.SetWindowPos(hwnd,win32con.HWND_BOTTOM,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
        if win32gui.GetWindowText(hwnd).find("Warning")!= -1:
            win32gui.SetWindowPos(hwnd,win32con.HWND_TOP,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
        if win32gui.GetWindowText(hwnd).find("Run Data Collector")!= -1:
            win32gui.SetWindowPos(hwnd,win32con.HWND_TOP,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )
        elif win32gui.GetWindowText(hwnd).find("Coral")!= -1:
            global checkCoralOpen
            checkCoralOpen = True
            win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,500,500,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE )   
        return True
    try:
        win32gui.EnumWindows(callback, None)
        global checkCoralOpen
        if not checkCoralOpen:
            openCoral()
    except:
        pass
                     
def openCoral ():
    global config
    path = config.get('front_window')
    # print ("opening %s" % path)
    subprocess.Popen(path)
    time.sleep (6)

# a thread class to do the infinite loop to make sure the
# Coral window at the most front
class ControlFrameThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        global endFlag
        while not endFlag:
            global checkCoralOpen
            checkCoralOpen = False
            makeProgramAtFront()
            time.sleep(1)
        return
        
#=======================================================
    
if __name__ == '__main__' :
    app = wx.App( False )
    frm = OverlayFrame()
    frm.Show()
    newthread = ControlFrameThread()
    app.MainLoop()