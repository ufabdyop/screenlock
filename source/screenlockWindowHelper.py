import logging
from datetime import datetime
import win32gui

def getWindow(*args):
    windows = {}
    logger = logging.getLogger("screenlockApp")

    def callback(hwnd, _):
        for windowtext in args:
            if win32gui.GetWindowText(hwnd).find(windowtext)!= -1:
                if windowtext == 'Run Data Collector' and not win32gui.IsWindowVisible(hwnd):
                    continue
                if windowtext in windows:
                    continue
                windows[windowtext] = hwnd
        return True
    try:
        win32gui.EnumWindows(callback, None)
    except:
        logger.error (str(datetime.now()) + "  screenlockApp: getWindow error.")
    if len(windows) > 0 :
        return windows
    return None