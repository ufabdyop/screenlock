# ScreenLock  [![version][version-badge]][CHANGELOG] [![license][license-badge]][LICENSE]

This program locks the screen of a windows computer and only allows coral to run in the foreground.  
All other programs are blocked by a large, transparent window

## Installing
Use the installer (ScreenLock-VERSION-Setup.exe).  This will guide you through installing all the EXE files.

## Post Install
Some configuration is required after installing.  You may have to edit config.ini to change some settings.
You will have to set an admin password for local override (the installer guides you through this). You
will have to set the admin password for web access.  The default web access password is 1234.  To change it,
you must start the server (as administrator so it has permissions to write config files).  Then, log into
https://localhost:PORT/admin and set the new password.  A future release will make these post installation
steps unnecessary.

## Running
Start the screen lock by running the Screenlock Server item from the start menu.  This locks the screen
(which can be overridden by a password) and starts a server (https://YOURCOMPUTERIP:PORT/status).  You
can visit the server URL in a browser and use the web interface to lock or unlock the screen.  The port
and password can be configured.

You may alternatively use Screenlock Server NCD to run an NCD-like server to accept commands as though
an NCD device.

## Running on Startup or Login
The working directory must be set correctly to run the executables for this application.  There are
some startup batch files in the install directory that will do this for you (startup.bat, startupNCD.bat).
Configure your windows machine to run one of those startup scripts on login and it should run the 
application automatically.  In addition to batch files, there are some vbs files that are provided to 
do the same thing, but should hide the command prompt window.

## Features

<img src="screenshots/v11-1.png" align="right" width="500">

#### Walk Away
User can use the screenlock shortcut on the desktop to lock the computer with a temporary password which expires after once use.

#### Multiple Monitors
Screenlock works with mulitple monitors.
<br><br>
#### Multiple Computers
Master computer can be set to unlock child computers. To setup this feature, you will need to add the IP addresses, schemas, and the port number of the child computers to the 'config.ini' file of the master computer. Each IP address should be separated but a comma. You do not need to edit the 'config.ini' file of the child computers.

Note: If no schema or port number is specified, the default will be used. (Default schema is HTTP and port number is 9092)

<table>
<tr>
<td>
Example of one child:
<pre>
[SubHosts]
names = 127.0.0.5
schemas = HTTP                               
ports = 1234</pre>
</td>
<td>
Example of two childs with default schemas and ports:
<pre>
[SubHosts]
names = 127.0.0.5, 127.0.0.12               
schemas = ,
ports = ,</pre>
</td>
</tr>
</table>

#### Adjustable Opacity
The opacity of the screenlock's screen can be changed through the 'config.ini' file. Change the opacity field to a number within the range of 180 to 255 (inclusive). The default opacity is 240.

## Prerequisites for Developing on Python Source Code :

Currently, this requires:

* python 32-bit version, 64 bit won't work (https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi)
* pywin32 (http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20219/pywin32-219.win32-py2.7.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpywin32%2Ffiles%2Fpywin32%2FBuild%2520219%2F&ts=1431713378&use_mirror=iweb)
* wxpython (http://downloads.sourceforge.net/project/wxpython/wxPython/3.0.2.0/wxPython3.0-win32-3.0.2.0-py27.exe?r=http%3A%2F%2Fwxpython.org%2Fdownload.php&ts=1431713419&use_mirror=softlayer-dal)
* java (for coral: http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-windows-i586.exe)
* pyinstaller (pip install pyinstaller)
* pyhook (http://downloads.sourceforge.net/project/pyhook/pyhook/1.5.1/pyHook-1.5.1.zip) or whl file for use with pip: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook
* flask (pip install flask)
* rocket (pip install rocket)
* requests (pip install requests)
* psutil v1.2.1 (https://pypi.python.org/packages/2.7/p/psutil/psutil-1.2.1.win32-py2.7.exe#md5=c4264532a64414cf3aa0d8b17d17e015)
* twisted (https://pypi.python.org/packages/2.7/T/Twisted/Twisted-15.2.1.win32-py2.7.exe#md5=54d71f4b56106541a1feb3306a0a72c7)
* pyopenssl (required using older version for building on linux -- pyOpenSSL-0.13.winxp32-py2.7.exe)
* NSIS: http://nsis.sourceforge.net/Download (build scripts expect this to be installed in "C:\Program Files\NSIS" or "C:\Program Files (x86)\NSIS")

Zip of prerequisites:

* http://www.nanofab.utah.edu/sv/index.php?dec=1&cat=Computer%20Passwords&t1=Prerequisites%20For%20Screenlock%20Build&t2=

## Building EXE File

#### With Docker:

Use the instructions in docker-screenlock-builder/README.md
This build process uses wine to run the pyinstaller process.

#### With Windows:

We are using pyinstaller for building an exe file.

To build, follow these steps in a cmd window (We are assuming this directory is located in Z:\screenlock )

    z:
    cd \screenlock
    python.exe setup.py

Once built, you should have a directory matching the current version in Tags with a zip file containing the exe and all
prerequisites (excluding DLLs that are included in windows)


## Emulating NCD Device:
The screenlockServerNCD.py and .exe files emulate the commands that the NCD network interlock devices use.  Some examples
follow.  This is assuming coral is set to use channel 1 (operating NCD relay at index 1).  Also, we assume the ncd device
is using port 2101.

To enable (unlock screen), you can send an NCD device two bytes (254, 9, in decimal notation, or 0xfe, 0x09 in hex).  On the command line, you can send this with (assuming port 2101):

  echo 'fe09' | xxd -r -p | nc ncd-device.example.com 2101

To disable (lock screen), you can send an NCD device two bytes (254, 1, in decimal notation, or 0xfe, 0x01 in hex).  On the command line, you can send this with (assuming port 2101):

  echo 'fe01' | xxd -r -p | nc ncd-device.example.com 2101

To detect status, you can send an NCD device two bytes (254, 17, in decimal notation, or 0xfe, 0x11 in hex).  On the command line, you can send this with (assuming port 2101):

  echo 'fe11' | xxd -r -p | nc ncd-device.example.com 2101

The device will respond with a 1 or a 0 byte to show it is enabled or disabled respectively.

## Screenshot:
![Screenshot](screenshots/v11.png)

More screenshots at:

[more screenshots](https://github.com/ufabdyop/screenlock/tree/master/screenshots/example.md "Examples") 

## More Info:
https://github.com/ufabdyop/screenlock



[CHANGELOG]: ./CHANGELOG.md
[LICENSE]: ./LICENSE
[version-badge]: https://img.shields.io/badge/Version-1.1.17-blue.svg
[license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
