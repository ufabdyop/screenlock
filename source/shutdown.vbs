' Get working directory of this script
strWorkingDir = Replace (WScript.ScriptFullName, Wscript.ScriptName, "")

' Get shell object
Set objShell = WScript.CreateObject("WScript.Shell")
Set objFileSys = CreateObject("Scripting.FileSystemObject")

' Change to working directory
objShell.currentdirectory = strWorkingDir

' Stop screen lock
strReturn = objShell.Run( "taskkill /f /im blockKeys.exe", 0, true)
strReturn = objShell.Run( "taskkill /f /im screenlockApp.exe", 0, true)

