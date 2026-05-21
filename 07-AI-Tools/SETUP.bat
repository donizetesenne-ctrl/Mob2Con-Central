@echo off
title Mob2Con AI Tools - Setup
echo ============================================
echo   Mob2Con AI Tools - Instalacao Unificada
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Instalando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo [2/3] Instalando LLMLingua do source local...
pip install -e LLMLingua --quiet 2>nul
pip install -e cpc --quiet 2>nul

echo [3/3] Verificando instalacao...
python -c "import llmlingua; print('  LLMLingua OK')"
python -c "import langfuse; print('  Langfuse OK')"
python -c "import tiktoken; print('  Tiktoken OK')"
python -c "import openai; print('  OpenAI SDK OK')"

echo.
echo ============================================
echo   Setup concluido! Use: python compress.py
echo ============================================
pause
