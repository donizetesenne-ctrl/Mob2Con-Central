@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   Chatbot WhatsApp Mob2Con - iniciar e validar
echo ============================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALAR-INICIALIZACAO-AUTOMATICA.ps1"
if errorlevel 1 (
    echo.
    echo [X] Falha ao iniciar o watchdog ou os servicos.
    pause
    exit /b 1
)

echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0STATUS-AUTOMACAO.ps1"
if errorlevel 1 (
    echo.
    echo [X] A verificacao operacional falhou.
    pause
    exit /b 1
)

echo.
echo [OK] Watchdog, bot e gateway estao ativos em segundo plano.
echo      Nenhuma janela precisa ficar aberta.
pause
exit /b 0
