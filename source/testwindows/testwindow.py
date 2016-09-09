import Tkinter as tk
import time, threading
import win32gui
import win32con


def makeWindowTopmost(windowHwnd):
    win32gui.SetWindowPos(windowHwnd, win32con.HWND_TOPMOST, 0, 0, 500, 500,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def win_info(hwnd, glob):
    window = {}
    window['hwnd'] = hwnd
    window['IsWindowVisible'] = win32gui.IsWindowVisible(hwnd)
    window['IsWindowEnabled'] = win32gui.IsWindowEnabled(hwnd)
    window['GetWindowText'] = win32gui.GetWindowText(hwnd)
    window['GetForegroundWindow'] = win32gui.GetForegroundWindow() == hwnd
    if window['GetWindowText'] == 'tk':
        makeWindowTopmost(hwnd)

def enum():
    win32gui.EnumWindows(win_info, {})

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(self, text="Create new window",
                                command=self.create_window)
        self.button.pack(side="top")

    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

class Foregrounder(threading.Thread):
    def run(self):
        self.active = threading.Event()
        self.active.set()
        while self.active:
            time.sleep(3)
            enum()

fg = Foregrounder()
fg.start()
root = tk.Tk()
main = MainWindow(root)
main.pack(side="top", fill="both", expand=True)
root.mainloop()
fg.active.clear()
fg.join()