@echo off
setlocal
cd /d "%~dp0"
echo Isto para e remove somente as tarefas agendadas do chatbot.
echo Dados, logs, .env e pareamento serao preservados.
echo.
choice /C SN /N /M "Continuar? [S/N]: "
if errorlevel 2 exit /b 0
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0REMOVER-INICIALIZACAO-AUTOMATICA.ps1"
echo.
pause
