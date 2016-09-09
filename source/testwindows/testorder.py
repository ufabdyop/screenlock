def orderByZ(windowList):
    windowList.sort(key=lambda x: x['zIndex'])

windows = [{'IsForegroundWindow': False, 'preferredOrder': 3, 'zIndex': 5, 'title': 'Coral Login Dialog', 'hwnd': 394952,
  'IsWindowVisible': 1, 'minimized': 0, 'GetWindowText': 'Coral Login Dialog', 'IsWindowEnabled': 1, 'next': 65644,
  'rectangle': (495, 340, 804, 510)},
 {'IsForegroundWindow': True, 'preferredOrder': 6, 'zIndex': 2, 'title': 'Transparent Window', 'hwnd': 1377866,
  'IsWindowVisible': 1, 'minimized': 0, 'GetWindowText': 'Transparent Window', 'IsWindowEnabled': 1, 'next': 198174,
  'rectangle': (0, 0, 1298, 891)}]


print(windows)
orderByZ(windows)
print(windows)