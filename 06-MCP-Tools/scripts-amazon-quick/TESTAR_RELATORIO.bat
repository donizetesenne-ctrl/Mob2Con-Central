@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo  GERANDO RELATORIO DE TESTE...
echo ========================================
echo.

python relatorio_semanal_auto.py --test

echo.
echo ========================================
echo  ABRINDO HTML NO NAVEGADOR...
echo ========================================

:: Pega o HTML mais recente da pasta backups
for /f "delims=" %%f in ('dir /b /o-d backups\relatorio_*.html 2^>nul') do (
    start "" "backups\%%f"
    goto :fim
)

:fim
echo.
echo Pronto! Verifique o navegador.
echo.
pause
