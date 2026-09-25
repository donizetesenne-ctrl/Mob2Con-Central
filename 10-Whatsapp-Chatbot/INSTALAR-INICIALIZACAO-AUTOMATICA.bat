@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALAR-INICIALIZACAO-AUTOMATICA.ps1"
set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" echo Falha ao instalar. Codigo %RC%.
pause
exit /b %RC%
