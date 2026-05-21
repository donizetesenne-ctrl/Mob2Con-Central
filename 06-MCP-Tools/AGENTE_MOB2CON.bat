@echo off
title Agente Mob2Con - Powered by Agno
echo.
echo ============================================================
echo   AGENTE MOB2CON - Powered by Agno Framework
echo   Agente inteligente de analise de performance
echo ============================================================
echo.

cd /d "C:\Users\Donizete Senne\Desktop\Mob2Con-Central"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "06-MCP-Tools\agente_mob2con.py"
) else (
    python "06-MCP-Tools\agente_mob2con.py"
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: Verifique se OPENAI_API_KEY esta configurada.
    echo   set OPENAI_API_KEY=sk-...
    pause
)
