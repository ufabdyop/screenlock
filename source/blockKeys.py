import  pythoncom, pyHook, signal

class BlockKeys(object):
    def __init__ (self):
        self.keylist = {}
        self.beginBlocking()
        
    def beginBlocking(self):
        hm = pyHook.HookManager()   # create a hook manager
        hm.KeyAll = self.OnKeyboardEvent    # watch for all keyboard events
        hm.HookKeyboard()         # set the hook
        signal.signal(signal.SIGTERM, self.signal_handler)
        try:
            pythoncom.PumpMessages()
        except Exception:
            print "exception",ex
            sys.exit(0)  
            
    # create a keyboard hook
    def OnKeyboardEvent(self, event):
        if "down" in event.MessageName.lower():
            self.keylist[event.Key.lower()] = event.Key
        elif "up" in event.MessageName.lower():
            if self.keylist.has_key(event.Key.lower()):
                del self.keylist[event.Key.lower()]
        keys = self.keylist.keys()
        keys.sort()
        if keys in [['escape', 'lcontrol'],['c', 'lcontrol'],['escape', 'lcontrol', 'lshift'],['tab'] ]:
            return False    # block these keys
        else:
            return True    # return True to pass the event to other handlers

    def signal_handler(self, signal, frame):
      print 'catcher: signal %d received!' % signal
      raise Exception('catcher: i am done')
  
bk = BlockKeys()
      
