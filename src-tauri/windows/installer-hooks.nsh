!macro NSIS_HOOK_POSTINSTALL
  CreateShortcut "$DESKTOP\Stellaris Writing.lnk" "$INSTDIR\Stellaris Writing.exe"
!macroend

!macro NSIS_HOOK_POSTUNINSTALL
  Delete "$DESKTOP\Stellaris Writing.lnk"
!macroend
