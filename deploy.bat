@echo off
rem NESND deploy: source directory -> MOD folder. Double-click for the menu.
rem   deploy.bat deploy   clear the MOD folder, copy runtime files, write a new version
rem   deploy.bat preview  list what would be deleted and copied; change nothing
rem   deploy.bat check    compare the two version files and the last update_record.json entry
rem   deploy.bat force    deploy despite a version mismatch, after typing DELETE
rem Engine and whitelist: deploy\deploy.ps1, deploy\deploy-whitelist.txt
setlocal
set "MODE=%~1"
if "%MODE%"=="" set "MODE=menu"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy\deploy.ps1" -Mode %MODE%
set "RC=%ERRORLEVEL%"
if /i "%MODE%"=="menu" pause
exit /b %RC%
