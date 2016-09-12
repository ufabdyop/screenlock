import win32gui
import pprint
from time import sleep

def print_window(win):
    if win['IsWindowVisible']:
        pprint.pprint(win)

def print_window_diff(win1, win2):
    if (not win1['IsWindowVisible']) and (not win2['IsWindowVisible']):
        #if both are invisible, ignore them
        return

    for k in win1.keys():
        if win1[k] != win2[k]:
            print("%s %s: (%s, %s)" %(win1['hwnd'], k, win1[k], win2[k]))


def win_info(hwnd, glob):
    window = {}
    window['hwnd'] = hwnd
    window['IsWindowVisible'] = win32gui.IsWindowVisible(hwnd)
    window['IsWindowEnabled'] = win32gui.IsWindowEnabled(hwnd)
    window['GetWindowText'] = win32gui.GetWindowText(hwnd)
    window['GetForegroundWindow'] = win32gui.GetForegroundWindow() == hwnd

    stored_window = glob.get(hwnd, False)
    if stored_window == False:
        glob[hwnd] = window
        print_window(window)

    if glob[hwnd] == window:
        pass
    else:
        print_window_diff(glob[hwnd], window)
        glob[hwnd] = window

def enum(window_list):
    win32gui.EnumWindows(win_info, window_list)


window_list = {}
while True:
    enum(window_list)
    print "waiting, active window is : %s" % win32gui.GetForegroundWindow()
    sleep(2)