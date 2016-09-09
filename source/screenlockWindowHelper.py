import logging, pprint, traceback
from datetime import datetime
import win32gui
import win32con
import ctypes

"""
Note: There seems to be a race condition somewhere.  If a thread calls this method then
exits, that thread seems to hang.

"""

def win_info(hwnd, glob):
    window = hwndToWindow(hwnd)
    glob[hwnd] = window


def hwndToWindow(hwnd, zIndex=None):
    window = {}
    window['hwnd'] = hwnd
    window['IsWindowVisible'] = win32gui.IsWindowVisible(hwnd)
    window['IsWindowEnabled'] = win32gui.IsWindowEnabled(hwnd)
    window['GetWindowText'] = win32gui.GetWindowText(hwnd)
    window['IsForegroundWindow'] = win32gui.GetForegroundWindow() == hwnd
    window['title'] = window['GetWindowText']
    window["minimized"] = win32gui.IsIconic(hwnd)
    window["rectangle"] = win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)
    window["next"] = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)  # Window handle to below window
    window["zIndex"] = zIndex
    return window

def enum(window_list):
    win32gui.EnumWindows(win_info, window_list)
    return window_list

def getWindow(*args):
    logger = logging.getLogger("screenlockApp")

    windows = {}

    try:
        enum(windows)
    except:
        logger.error(str(datetime.now()) + "  screenlockApp: getWindow error.")
        traceback.print_stack()

    filtered_windows = {}
    for hwnd in windows:
        w = windows[hwnd]
        if w['GetWindowText'] and windowTitleMatchesAny(w['GetWindowText'], args):
            key = windowTitleMatchesAny(w['GetWindowText'], args)
            filtered_windows[key] = w['hwnd']

    if len(filtered_windows) > 0:
        logger.debug("getWindow : Returning windows: %s" % pprint.pformat(filtered_windows))
        return filtered_windows

    logger.debug("getWindow : Returning None")
    return None

def windowTitleMatchesAny(needle, haystack):
    for h in haystack:
        if h in needle:
            return h
    return False

def getAllVisibleWindows():
    winHandles = getAllWindowHandles()
    windows = {}
    index = 0
    for h in winHandles:
        window = hwndToWindow(h, index)
        if window['IsWindowVisible']:
            windows[h] = window
        index += 1
    return windows

def getAllWindowHandles():
    '''Returns windows in z-order (top first)'''
    user32 = ctypes.windll.user32
    lst = []
    top = user32.GetTopWindow(None)
    if not top:
        return lst
    lst.append(top)
    while True:
        next = user32.GetWindow(lst[-1], win32con.GW_HWNDNEXT)
        if not next:
            break
        lst.append(next)
    return lst

