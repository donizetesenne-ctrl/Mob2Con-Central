@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

echo Reiniciando somente o gateway. Sessao e pareamento serao preservados.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0REINICIAR-SERVICO.ps1" -Servico Gateway
if errorlevel 1 (
    echo.
    echo [X] Falha ao reiniciar o gateway.
    pause
    exit /b 1
)

echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0STATUS-AUTOMACAO.ps1"
pause
exit /b %ERRORLEVEL%
