@echo off
REM ============================================================
REM  Mob2Con Central - Instalador
REM  Duplo-clique para executar
REM ============================================================

title Mob2Con Central - Instalador

echo.
echo ================================================================
echo   MOB2CON CENTRAL - INSTALADOR
echo ================================================================
echo.
echo Este instalador vai:
echo   1. Verificar dependencias (Node.js, Python, uvx)
echo   2. Instalar pacotes MCP necessarios
echo   3. Configurar MCPs no Amazon Quick e Kiro
echo   4. Aplicar temas Power BI na pasta do usuario
echo   5. Criar atalhos na Area de Trabalho
echo.
echo ----------------------------------------------------------------
echo.

pause

REM Executar o script PowerShell com permissao de execucao temporaria
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Instalar-Mob2Con.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ================================================================
    echo   ERRO NA INSTALACAO
    echo ================================================================
    echo.
    echo Algo deu errado. Verifique o log acima.
    echo Voce tambem pode ler GUIA-INSTALACAO.md para instalar manualmente.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo   INSTALACAO CONCLUIDA COM SUCESSO!
echo ================================================================
echo.
pause
