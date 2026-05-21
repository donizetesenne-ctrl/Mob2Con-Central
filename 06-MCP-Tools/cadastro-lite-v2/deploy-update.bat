@echo off
echo ============================================
echo  Cadastro Lite - Atualizar Apps Script
echo ============================================
echo.
echo Copiando Index.html para clipboard...
powershell -Command "Get-Content '%~dp0Index.html' -Raw | Set-Clipboard"
echo.
echo [OK] Index.html copiado para clipboard!
echo.
echo Agora faca:
echo   1. No editor que vai abrir, clique em Index.html
echo   2. Ctrl+A, Ctrl+V, Ctrl+S
echo   3. Implantar - Gerenciar - Lapis - Nova versao - Implantar
echo.
echo Abrindo o editor...
start https://script.google.com/home/projects/1vgjMumNtjp2EkSoXa8gV_SizQjhljskv8hrRcDOZEGcEI-ZUh78t6N20/edit
echo.
pause
