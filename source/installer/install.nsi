; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "ScreenLock"
!define /file PRODUCT_VERSION "..\releaseVersion.txt"
!define PRODUCT_PUBLISHER "Utah Nanofab"
!define PRODUCT_WEB_SITE "http://www.nanofab.utah.edu"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\screenlockApp.exe"
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
!insertmacro MUI_PAGE_LICENSE "..\license.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
;!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\post-install.txt"
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Run configuration Script"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"
!insertmacro MUI_PAGE_FINISH

Function LaunchLink
  SetOutPath $INSTDIR
  Exec "setAdminPassword.exe"
FunctionEnd

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "ScreenLock-${PRODUCT_VERSION}-Setup.exe"
InstallDir "$PROGRAMFILES\ScreenLock"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "ScreenLock" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File "..\_hashlib.pyd"
  File "..\_win32sysloader.pyd"
  File "..\blockKeys.exe"
  File "..\bz2.pyd"
  File "..\config.ini"
  File "..\library.zip"
  File "..\pyHook._cpyHook.pyd"
  File "..\python27.dll"
  File "..\pythoncom27.dll"
  File "..\pywintypes27.dll"
  File "..\screenlockApp.exe"
  CreateShortCut "$STARTMENU.lnk" "$INSTDIR\screenlockApp.exe"
  File "..\select.pyd"
  File "..\setAdminPassword.exe"
  CreateShortCut "$STARTMENU.lnk" "$INSTDIR\setAdminPassword.exe"
  File "..\unicodedata.pyd"
  File "..\w9xpopen.exe"
  File "..\win32gui.pyd"
  File "..\win32process.pyd"
  File "..\wx._controls_.pyd"
  File "..\wx._core_.pyd"
  File "..\wx._gdi_.pyd"
  File "..\wx._misc_.pyd"
  File "..\wx._windows_.pyd"
  File "..\wxbase30u_net_vc90.dll"
  File "..\wxbase30u_vc90.dll"
  File "..\wxmsw30u_adv_vc90.dll"
  File "..\wxmsw30u_core_vc90.dll"
  File "..\wxmsw30u_html_vc90.dll"
  SetOverwrite ifnewer
  File "..\post-install.txt"
  File "..\license.txt"
  File "..\README.md"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\ScreenLock"
  CreateShortCut "$SMPROGRAMS\ScreenLock\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\ScreenLock\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\screenlockApp.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\screenlockApp.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
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
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\post-install.txt"
  Delete "$INSTDIR\wxmsw30u_html_vc90.dll"
  Delete "$INSTDIR\wxmsw30u_core_vc90.dll"
  Delete "$INSTDIR\wxmsw30u_adv_vc90.dll"
  Delete "$INSTDIR\wxbase30u_vc90.dll"
  Delete "$INSTDIR\wxbase30u_net_vc90.dll"
  Delete "$INSTDIR\wx._windows_.pyd"
  Delete "$INSTDIR\wx._misc_.pyd"
  Delete "$INSTDIR\wx._gdi_.pyd"
  Delete "$INSTDIR\wx._core_.pyd"
  Delete "$INSTDIR\wx._controls_.pyd"
  Delete "$INSTDIR\win32process.pyd"
  Delete "$INSTDIR\win32gui.pyd"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\setAdminPassword.exe"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\screenlockApp.exe"
  Delete "$INSTDIR\pywintypes27.dll"
  Delete "$INSTDIR\pythoncom27.dll"
  Delete "$INSTDIR\python27.dll"
  Delete "$INSTDIR\pyHook._cpyHook.pyd"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\config.ini"
  Delete "$INSTDIR\bz2.pyd"
  Delete "$INSTDIR\blockKeys.exe"
  Delete "$INSTDIR\_win32sysloader.pyd"
  Delete "$INSTDIR\_hashlib.pyd"

  Delete "$SMPROGRAMS\ScreenLock\Uninstall.lnk"
  Delete "$SMPROGRAMS\ScreenLock\Website.lnk"
  Delete "$STARTMENU.lnk"
  Delete "$STARTMENU.lnk"

  RMDir "$SMPROGRAMS\ScreenLock"
  RMDir "$INSTDIR"
  RMDir ""

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd
