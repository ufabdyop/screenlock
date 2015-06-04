; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "ScreenLock"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "NANOFAB"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\w9xpopen.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "..\..\..\source\license.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page

!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Run configuration Script"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"
!insertmacro MUI_PAGE_FINISH

Function LaunchLink
  SetOutPath $INSTDIR\screenlock\screenlock	
  Exec "setAdminPassword.exe"
FunctionEnd

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Screenlock.exe"
InstallDir "$PROGRAMFILES\ScreenLock"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
SectionEnd

Section "screenlock" SEC02
  SetOutPath "$INSTDIR\screenlock\screenlock"
  SetOverwrite ifnewer
  File "..\screenlock\screenlock\wxmsw30u_html_vc90.dll"
  File "..\screenlock\screenlock\wxmsw30u_core_vc90.dll"
  File "..\screenlock\screenlock\wxmsw30u_adv_vc90.dll"
  File "..\screenlock\screenlock\wxbase30u_vc90.dll"
  File "..\screenlock\screenlock\wxbase30u_net_vc90.dll"
  File "..\screenlock\screenlock\wx._windows_.pyd"
  File "..\screenlock\screenlock\wx._misc_.pyd"
  File "..\screenlock\screenlock\wx._gdi_.pyd"
  File "..\screenlock\screenlock\wx._core_.pyd"
  File "..\screenlock\screenlock\wx._controls_.pyd"
  File "..\screenlock\screenlock\win32process.pyd"
  File "..\screenlock\screenlock\win32gui.pyd"
  File "..\screenlock\screenlock\w9xpopen.exe"
  CreateDirectory "$SMPROGRAMS\ScreenLock"
  CreateShortCut "$SMPROGRAMS\ScreenLock\ScreenLock.lnk" "$INSTDIR\screenlock\screenlock\screenlockApp.exe"
  CreateShortCut "$DESKTOP\ScreenLock.lnk" "$INSTDIR\screenlock\screenlock\screenlockApp.exe"
  File "..\screenlock\screenlock\unicodedata.pyd"
  File "..\screenlock\screenlock\setAdminPassword.exe"
  File "..\screenlock\screenlock\select.pyd"
  File "..\screenlock\screenlock\screenlockApp.exe"
  File "..\screenlock\screenlock\pywintypes27.dll"
  File "..\screenlock\screenlock\python27.dll"
  File "..\screenlock\screenlock\post-install.txt"
  File "..\screenlock\screenlock\library.zip"
  File "..\screenlock\screenlock\config.ini"
  File "..\screenlock\screenlock\bz2.pyd"
  File "..\screenlock\screenlock\_hashlib.pyd"
  SetOutPath "$INSTDIR\screenlock\keysblock"
  File "..\screenlock\keysblock\w9xpopen.exe"
  File "..\screenlock\keysblock\unicodedata.pyd"
  File "..\screenlock\keysblock\select.pyd"
  File "..\screenlock\keysblock\pywintypes27.dll"
  File "..\screenlock\keysblock\pythoncom27.dll"
  File "..\screenlock\keysblock\python27.dll"
  File "..\screenlock\keysblock\pyHook._cpyHook.pyd"
  File "..\screenlock\keysblock\library.zip"
  File "..\screenlock\keysblock\bz2.pyd"
  File "..\screenlock\keysblock\blockKeys.exe"
  File "..\screenlock\keysblock\_win32sysloader.pyd"
  File "..\screenlock\keysblock\_hashlib.pyd"
SectionEnd

Section -AdditionalIcons
  SetOutPath $INSTDIR
  CreateShortCut "$SMPROGRAMS\ScreenLock\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\screenlock\screenlock\w9xpopen.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\screenlock\screenlock\w9xpopen.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\screenlock\keysblock\_hashlib.pyd"
  Delete "$INSTDIR\screenlock\keysblock\_win32sysloader.pyd"
  Delete "$INSTDIR\screenlock\keysblock\blockKeys.exe"
  Delete "$INSTDIR\screenlock\keysblock\bz2.pyd"
  Delete "$INSTDIR\screenlock\keysblock\library.zip"
  Delete "$INSTDIR\screenlock\keysblock\pyHook._cpyHook.pyd"
  Delete "$INSTDIR\screenlock\keysblock\python27.dll"
  Delete "$INSTDIR\screenlock\keysblock\pythoncom27.dll"
  Delete "$INSTDIR\screenlock\keysblock\pywintypes27.dll"
  Delete "$INSTDIR\screenlock\keysblock\select.pyd"
  Delete "$INSTDIR\screenlock\keysblock\unicodedata.pyd"
  Delete "$INSTDIR\screenlock\keysblock\w9xpopen.exe"
  Delete "$INSTDIR\screenlock\screenlock\_hashlib.pyd"
  Delete "$INSTDIR\screenlock\screenlock\bz2.pyd"
  Delete "$INSTDIR\screenlock\screenlock\config.ini"
  Delete "$INSTDIR\screenlock\screenlock\library.zip"
  Delete "$INSTDIR\screenlock\screenlock\post-install.txt"
  Delete "$INSTDIR\screenlock\screenlock\python27.dll"
  Delete "$INSTDIR\screenlock\screenlock\pywintypes27.dll"
  Delete "$INSTDIR\screenlock\screenlock\screenlockApp.exe"
  Delete "$INSTDIR\screenlock\screenlock\select.pyd"
  Delete "$INSTDIR\screenlock\screenlock\setAdminPassword.exe"
  Delete "$INSTDIR\screenlock\screenlock\unicodedata.pyd"
  Delete "$INSTDIR\screenlock\screenlock\w9xpopen.exe"
  Delete "$INSTDIR\screenlock\screenlock\win32gui.pyd"
  Delete "$INSTDIR\screenlock\screenlock\win32process.pyd"
  Delete "$INSTDIR\screenlock\screenlock\wx._controls_.pyd"
  Delete "$INSTDIR\screenlock\screenlock\wx._core_.pyd"
  Delete "$INSTDIR\screenlock\screenlock\wx._gdi_.pyd"
  Delete "$INSTDIR\screenlock\screenlock\wx._misc_.pyd"
  Delete "$INSTDIR\screenlock\screenlock\wx._windows_.pyd"
  Delete "$INSTDIR\screenlock\screenlock\wxbase30u_net_vc90.dll"
  Delete "$INSTDIR\screenlock\screenlock\wxbase30u_vc90.dll"
  Delete "$INSTDIR\screenlock\screenlock\wxmsw30u_adv_vc90.dll"
  Delete "$INSTDIR\screenlock\screenlock\wxmsw30u_core_vc90.dll"
  Delete "$INSTDIR\screenlock\screenlock\wxmsw30u_html_vc90.dll"

  Delete "$SMPROGRAMS\ScreenLock\Uninstall.lnk"
  Delete "$DESKTOP\ScreenLock.lnk"
  Delete "$SMPROGRAMS\ScreenLock\ScreenLock.lnk"

  RMDir "$SMPROGRAMS\ScreenLock"
  RMDir "$INSTDIR\screenlock\screenlock"
  RMDir "$INSTDIR\screenlock\keysblock"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd