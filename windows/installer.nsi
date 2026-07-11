!define APPNAME "Mechanic Board"
!define COMPANYNAME "Mechanic Board"
!define DESCRIPTION "Local workshop board and admin app"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://example.com"
!define UPDATEURL "https://example.com"
!define ABOUTURL "https://example.com"

RequestExecutionLevel admin

SetCompressor lzma

Name "${APPNAME}"
OutFile "mechanic-board-installer.exe"
InstallDir "$LOCALAPPDATA\MechanicBoard"
InstallDirRegKey HKCU "Software\${APPNAME}" "InstallDir"

Page directory
Page instfiles

Section "install"
  SetOutPath "$INSTDIR"

  File /r "..\*"

  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\start-mechanic-board.bat" "" "$INSTDIR\start-mechanic-board.bat" 0
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\start-mechanic-board.bat" "" "$INSTDIR\start-mechanic-board.bat" 0

  WriteRegStr HKCU "Software\${APPNAME}" "InstallDir" "$INSTDIR"
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  Delete "$DESKTOP\${APPNAME}.lnk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\${APPNAME}"
SectionEnd
