import logging, pprint, traceback
from datetime import datetime
import win32gui

def getWindow(*args):
    """
    Note: There seems to be a race condition somewhere.  If a thread calls this method then
    exits, that thread seems to hang.

    """
    windows = {}
    all_the_windows = {}
    logger = logging.getLogger("screenlockApp")

    def callback(hwnd, _):
        """
        this gets called once for each active window, and it builds up a dictionary of all
        windows that match the window_title argument
        """
        if win32gui.IsWindow(hwnd):
            current_window = win32gui.GetWindowText(hwnd)
            for window_title in args:
                all_the_windows[current_window] = hwnd
                if current_window.find(window_title) != -1:
                    if window_title == 'Run Data Collector' and not win32gui.IsWindowVisible(hwnd):
                        pass
                    elif window_title in windows:
                        pass
                    else:
                        windows[window_title] = hwnd
        else:
            logger.error("Window disappeared? %s" % hwnd)

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
    #logger.debug("All The Windows: %s" % (pprint.pformat(all_the_windows)))
    return None