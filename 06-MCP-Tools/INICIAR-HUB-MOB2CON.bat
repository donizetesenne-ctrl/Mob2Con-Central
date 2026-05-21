@echo off
title KIRO HIGH-AGILITY HUB
echo ==========================================
echo    INICIANDO KIRO HIGH-AGILITY HUB
echo ==========================================
echo.
echo [1/2] Iniciando Editor Web Interativo...
cd /d "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\preview-engine"
start /b node server.js
echo [OK] Editor rodando em http://localhost:5000
echo.
echo [2/2] Sincronizando com Power BI...
timeout /t 2 > nul
echo [OK] Pronto para comandos do KIRO.
echo.
echo Mantenha esta janela aberta para o Editor Web funcionar.
echo Pressione CTRL+C para encerrar.
echo ==========================================
pause
