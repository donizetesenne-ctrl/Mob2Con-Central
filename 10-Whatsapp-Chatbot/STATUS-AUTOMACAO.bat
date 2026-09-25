@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0STATUS-AUTOMACAO.ps1"
echo.
pause
