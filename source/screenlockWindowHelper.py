import logging, pprint, traceback
from datetime import datetime
import win32gui

def getWindow(*args):
    windows = {}
    logger = logging.getLogger("screenlockApp")

    def callback(hwnd, _):
        """
        this gets called once for each active window, and it builds up a dictionary of all
        windows that match the window_title argument
        """
        for window_title in args:
            if win32gui.GetWindowText(hwnd).find(window_title)!= -1:
                if window_title == 'Run Data Collector' and not win32gui.IsWindowVisible(hwnd):
                    pass
                elif window_title in windows:
                    pass
                else:
                    windows[window_title] = hwnd
        return True

    try:
        win32gui.EnumWindows(callback, None)
    except:
        logger.error(str(datetime.now()) + "  screenlockApp: getWindow error.")
        traceback.print_stack()

    if len(windows) > 0:
        logger.debug("getWindow : Returning windows: %s" % pprint.pformat(windows))
        return windows

    logger.debug("getWindow : Returning None")
    return None