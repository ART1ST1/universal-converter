; Universal Converter NSIS Installer Script
; Professional installer for Universal Converter application

!define APP_NAME "Universal Converter"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Universal Converter Team"
!define APP_URL "https://github.com/universalconverter/universal-converter"
!define APP_DESCRIPTION "Universal file format converter with modern GUI"

; Modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "WinVer.nsh"

; Application details
Name "${APP_NAME}"
OutFile "UniversalConverter-${APP_VERSION}-Setup.exe"
Unicode True

; Default installation folder
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKCU "Software\${APP_NAME}" ""

; Request administrator privileges
RequestExecutionLevel admin

; Variables
Var StartMenuFolder

; Modern UI Configuration
!define MUI_ABORTWARNING
!define MUI_ICON "resources\icon.ico"
!define MUI_UNICON "resources\icon.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "resources\header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "resources\welcome.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "resources\welcome.bmp"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

; Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${APP_NAME}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

!insertmacro MUI_PAGE_INSTFILES

; Finish page configuration
!define MUI_FINISHPAGE_RUN "$INSTDIR\UniversalConverter.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Executar ${APP_NAME}"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.txt"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Mostrar arquivo README"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "English"

; Version Information
VIProductVersion "${APP_VERSION}.0"
VIAddVersionKey /LANG=${LANG_PORTUGUESE} "ProductName" "${APP_NAME}"
VIAddVersionKey /LANG=${LANG_PORTUGUESE} "Comments" "${APP_DESCRIPTION}"
VIAddVersionKey /LANG=${LANG_PORTUGUESE} "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_PORTUGUESE} "LegalCopyright" "© 2024 ${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_PORTUGUESE} "FileDescription" "${APP_DESCRIPTION}"
VIAddVersionKey /LANG=${LANG_PORTUGUESE} "FileVersion" "${APP_VERSION}"
VIAddVersionKey /LANG=${LANG_PORTUGUESE} "ProductVersion" "${APP_VERSION}"

; Installer Sections
Section "Aplicativo Principal" SecMain
  SectionIn RO

  ; Set output path to the installation directory
  SetOutPath $INSTDIR

  ; Files to install
  File "dist\UniversalConverter.exe"
  File "README.md"
  File "LICENSE"

  ; Create README.txt (converted from markdown)
  CopyFiles "$INSTDIR\README.md" "$INSTDIR\README.txt"

  ; Store installation folder
  WriteRegStr HKCU "Software\${APP_NAME}" "" $INSTDIR

  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Add to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "URLInfoAbout" "${APP_URL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "DisplayIcon" "$INSTDIR\UniversalConverter.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "QuietUninstallString" "$INSTDIR\Uninstall.exe /S"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                     "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                     "NoRepair" 1

  ; Calculate and store size
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                     "EstimatedSize" "$0"

SectionEnd

Section "Atalho na Área de Trabalho" SecDesktop
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\UniversalConverter.exe" "" \
                 "$INSTDIR\UniversalConverter.exe" 0 SW_SHOWNORMAL "" \
                 "Conversor universal de arquivos"
SectionEnd

Section "Menu Iniciar" SecStartMenu
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application

    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\${APP_NAME}.lnk" \
                   "$INSTDIR\UniversalConverter.exe" "" \
                   "$INSTDIR\UniversalConverter.exe" 0 SW_SHOWNORMAL "" \
                   "Conversor universal de arquivos"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Desinstalar ${APP_NAME}.lnk" \
                   "$INSTDIR\Uninstall.exe" "" \
                   "$INSTDIR\Uninstall.exe" 0 SW_SHOWNORMAL "" \
                   "Desinstalar ${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\README.lnk" \
                   "$INSTDIR\README.txt" "" \
                   "notepad.exe" 0 SW_SHOWNORMAL "" \
                   "Ler documentação"

  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section "Associações de Arquivo" SecFileAssoc
  ; Register common file associations

  ; Image files
  WriteRegStr HKCR ".jpg\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".jpeg\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".png\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".gif\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".bmp\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".tiff\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".webp\OpenWithList\UniversalConverter.exe" "" ""

  ; Document files
  WriteRegStr HKCR ".pdf\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".docx\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".doc\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".txt\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".rtf\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".odt\OpenWithList\UniversalConverter.exe" "" ""

  ; Spreadsheet files
  WriteRegStr HKCR ".xlsx\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".xls\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".csv\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".ods\OpenWithList\UniversalConverter.exe" "" ""

  ; Audio files
  WriteRegStr HKCR ".mp3\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".wav\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".ogg\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".flac\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".aac\OpenWithList\UniversalConverter.exe" "" ""

  ; Video files
  WriteRegStr HKCR ".mp4\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".avi\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".mkv\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".mov\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".webm\OpenWithList\UniversalConverter.exe" "" ""

  ; Archive files
  WriteRegStr HKCR ".zip\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".rar\OpenWithList\UniversalConverter.exe" "" ""
  WriteRegStr HKCR ".7z\OpenWithList\UniversalConverter.exe" "" ""

  ; Refresh shell
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
SectionEnd

; Section Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} "Arquivos principais do ${APP_NAME}. Este componente é obrigatório."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Criar atalho na área de trabalho para acesso rápido."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Adicionar ${APP_NAME} ao Menu Iniciar."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFileAssoc} "Associar tipos de arquivo comuns com ${APP_NAME} para conversão rápida."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Functions
Function .onInit
  ; Check Windows version
  ${IfNot} ${AtLeastWin7}
    MessageBox MB_OK|MB_ICONSTOP "Este programa requer Windows 7 ou superior."
    Abort
  ${EndIf}

  ; Check if already installed
  ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString"
  StrCmp $R0 "" done

  MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
  "${APP_NAME} já está instalado. $\n$\nClique em 'OK' para remover a versão anterior ou 'Cancelar' para cancelar a instalação." \
  IDOK uninst
  Abort

  uninst:
    ClearErrors
    ExecWait '$R0 _?=$INSTDIR'

    IfErrors no_remove_uninstaller done
      Delete $R0
      RMDir $INSTDIR
    no_remove_uninstaller:

  done:
FunctionEnd

; Uninstaller Section
Section "Uninstall"

  ; Remove files
  Delete "$INSTDIR\UniversalConverter.exe"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\Uninstall.exe"

  ; Remove directory
  RMDir "$INSTDIR"

  ; Remove desktop shortcut
  Delete "$DESKTOP\${APP_NAME}.lnk"

  ; Remove start menu items
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
  Delete "$SMPROGRAMS\$StartMenuFolder\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Desinstalar ${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\README.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"

  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKCU "Software\${APP_NAME}"

  ; Remove file associations
  DeleteRegKey HKCR ".jpg\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".jpeg\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".png\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".gif\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".bmp\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".tiff\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".webp\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".pdf\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".docx\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".doc\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".txt\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".rtf\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".odt\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".xlsx\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".xls\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".csv\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".ods\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".mp3\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".wav\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".ogg\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".flac\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".aac\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".mp4\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".avi\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".mkv\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".mov\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".webm\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".zip\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".rar\OpenWithList\UniversalConverter.exe"
  DeleteRegKey HKCR ".7z\OpenWithList\UniversalConverter.exe"

  ; Refresh shell
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'

SectionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Tem certeza de que deseja desinstalar completamente $(^Name) e todos os seus componentes?" IDYES +2
  Abort
FunctionEnd