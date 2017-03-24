' Get working directory of this script
strWorkingDir = Replace (WScript.ScriptFullName, Wscript.ScriptName, "")

' Get shell object
Set objShell = WScript.CreateObject("WScript.Shell")
Set objFileSys = CreateObject("Scripting.FileSystemObject")

' Change to working directory
objShell.currentdirectory = strWorkingDir

' Start screen lock
strReturn = objShell.Run( "screenlockServer.exe", 0, true)
