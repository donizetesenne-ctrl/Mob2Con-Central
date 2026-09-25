@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   Trocar o numero do WhatsApp do bot
echo ============================================================
echo.
echo   Isto arquiva a sessao atual e gera um QR Code novo,
echo   para voce parear OUTRO numero.
echo.
echo   A sessao antiga NAO e apagada: fica em gateway\sessao.bak-*
echo   Para voltar ao numero anterior, renomeie a pasta de volta.
echo.

rem ---- 1. as portas precisam estar livres ---------------------------------
set OCUPADA=
for %%P in (8080 8000) do (
    powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort %%P -State Listen -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"
    if errorlevel 1 set OCUPADA=!OCUPADA! %%P
)

if not "!OCUPADA!"=="" (
    echo [X] As portas!OCUPADA! ainda estao em uso.
    echo.
    echo     FECHE as janelas abertas antes de continuar:
    echo       - "Gateway WhatsApp (8080)"
    echo       - "Bot Python (8000)"
    echo.
    echo     Depois rode este arquivo de novo.
    echo.
    pause
    exit /b 1
)

echo [1/4] Portas livres.
echo.

rem ---- 2. arquiva a sessao atual ------------------------------------------
if exist "gateway\sessao" (
    for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set TS=%%T
    move "gateway\sessao" "gateway\sessao.bak-!TS!" >nul
    if errorlevel 1 (
        echo [X] Nao consegui mover gateway\sessao
        pause
        exit /b 1
    )
    echo [2/4] Sessao anterior arquivada em gateway\sessao.bak-!TS!
) else (
    echo [2/4] Nenhuma sessao anterior para arquivar.
)
echo.

rem ---- 3. sobe os dois servicos -------------------------------------------
echo [3/4] Subindo bot e gateway...
start "Bot Python (8000)" cmd /k "chcp 65001 >nul && cd /d "%~dp0" && set PYTHONIOENCODING=utf-8 && python -m uvicorn bot.main:app --host 127.0.0.1 --port 8000"
timeout /t 4 /nobreak >nul
start "Gateway WhatsApp (8080)" cmd /k "chcp 65001 >nul && cd /d "%~dp0gateway" && node --env-file=../.env index.js"
echo      aguardando o gateway subir...
timeout /t 12 /nobreak >nul
echo.

rem ---- 4. QR Code ---------------------------------------------------------
echo [4/4] Buscando o QR Code...
echo.
set PYTHONIOENCODING=utf-8
python scripts\setup_instancia.py --aguardar 180

echo.
echo ============================================================
echo   Depois de conectar, confira com:
echo     python scripts\status.py
echo ============================================================
echo.
pause
