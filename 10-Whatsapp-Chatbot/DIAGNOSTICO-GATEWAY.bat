@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

set SAIDA=%~dp0gateway-console.log

echo ============================================================
echo   Diagnostico do gateway - grava TUDO em gateway-console.log
echo ============================================================
echo.

echo == ambiente == > "%SAIDA%"
echo pasta atual: %CD% >> "%SAIDA%"
where node >> "%SAIDA%" 2>&1
node --version >> "%SAIDA%" 2>&1
if exist "gateway\node_modules" (echo node_modules: presente >> "%SAIDA%") else (echo node_modules: AUSENTE >> "%SAIDA%")
if exist ".env" (echo .env: presente >> "%SAIDA%") else (echo .env: AUSENTE >> "%SAIDA%")
if exist "gateway\sessao\creds.json" (echo creds.json: presente >> "%SAIDA%") else (echo creds.json: AUSENTE >> "%SAIDA%")
echo. >> "%SAIDA%"

echo == saida do node == >> "%SAIDA%"
echo Subindo o gateway. Deixe rodando; feche esta janela para parar.
echo Tudo esta sendo gravado em gateway-console.log
echo.

cd gateway
node --env-file=../.env index.js >> "%SAIDA%" 2>&1

echo. >> "%SAIDA%"
echo == o node ENCERROU, codigo %ERRORLEVEL% == >> "%SAIDA%"

echo.
echo ============================================================
echo   O node encerrou. Codigo: %ERRORLEVEL%
echo   Ultimas linhas:
echo ============================================================
powershell -NoProfile -Command "Get-Content '%SAIDA%' -Tail 25"
echo.
pause
