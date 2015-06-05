ScreenLock
===

This program locks the screen of a windows computer and only allows coral to run in the foreground.  
All other programs are blocked by a large, transparent window

Prerequisites:
---

Currently, this requires:

* python (https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi)
* pywin32 (http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20219/pywin32-219.win32-py2.7.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpywin32%2Ffiles%2Fpywin32%2FBuild%2520219%2F&ts=1431713378&use_mirror=iweb)
* wxpython (http://downloads.sourceforge.net/project/wxpython/wxPython/3.0.2.0/wxPython3.0-win32-3.0.2.0-py27.exe?r=http%3A%2F%2Fwxpython.org%2Fdownload.php&ts=1431713419&use_mirror=softlayer-dal)
* java (for coral: http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-windows-i586.exe)
* py2exe (download at http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/)
* Visual Studio C++ Redistributable (for running py2exe) https://www.microsoft.com/en-us/download/details.aspx?id=29
* pyhook (http://downloads.sourceforge.net/project/pyhook/pyhook/1.5.1/pyHook-1.5.1.zip) or whl file for use with pip: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook

Download All as Zip File:

http://archiva.eng.utah.edu:4040/repository/internal/edu/utah/nanofab/screenlock/prerequisites/1.0.3/prerequisites-1.0.3.zip


Building EXE File
---

We are using py2exe for building an exe file.  In order to build, python needs to have access to msvcp90.dll.
You should copy that file to C:\python27\DLLs to avoid any issues during build.

To build, follow these steps in a cmd window (We are assuming this directory is located in Z:\screenlock )

    z:
    cd \screenlock
    python.exe setup.py py2exe

Once built, you should have a directory matching the current version in Tags with a zip file containing the exe and all
prerequisites (excluding DLLs that are included in windows)

Notes:
---
Building exe requires msvcp90.dll (similar issue: http://stackoverflow.com/questions/323424/py2exe-fails-to-generate-an-executable)

