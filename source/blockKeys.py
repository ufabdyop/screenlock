from __future__ import print_function
import pythoncom, pyHook, signal,log, sys,logging
from win32api import GetSystemMetrics
from datetime import datetime

class BlockKeys(object):
    def __init__ (self):
        log.initialize_logging('BlockKeys')
        self.logger = logging.getLogger('BlockKeys')
        self.logger.debug("blocking keys")

        self.keylist = {}
        self.blockkeys = ['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10',
            'f11','f12','escape','lwin','rwin','lmenu','rmenu']
        self.beginBlocking()

        
    def beginBlocking(self):
        hm = pyHook.HookManager()   # create a hook manager
        hm.KeyAll = self.OnKeyboardEvent    # watch for all keyboard events
        hm.MouseAll = self.OnMouseEvent
        hm.HookKeyboard()         # set the hook
        hm.HookMouse()
        signal.signal(signal.SIGTERM, self.signal_handler)
        try:
            pythoncom.PumpMessages()
        except Exception as err:
            self.logger.error(err)
            sys.exit(0)
            
    # create a keyboard hook
    def OnKeyboardEvent(self, event):
        if "down" in event.MessageName.lower():
            self.keylist[event.Key.lower()] = event.Key
        elif "up" in event.MessageName.lower():
            if self.keylist.has_key(event.Key.lower()):
                del self.keylist[event.Key.lower()]
        for key in self.keylist.keys():     
            if key in self.blockkeys:
                return False    # block these keys
        keys = self.keylist.keys()
        keys.sort()
        if keys in [['c', 'lcontrol'],['c', 'rcontrol']]:
            return False    # block these keys
        
        return True    # return True to pass the event to other handlers
        
    def OnMouseEvent(self, event):
        if (event.Position[0] < 100 and event.Position[1] > 600 and event.WindowName == None) or event.Position[1] > (GetSystemMetrics(1)-60):
            return False
        if event.WindowName != None:
            if 'start' == event.WindowName.lower():
                return False
            elif 'running applications' == event.WindowName.lower():
                return False
        return True

    def signal_handler(self, signal, frame):
        self.logger.debug("received signal : %s" % signal)
        sys.exit(0)
      
BlockKeys()
      
