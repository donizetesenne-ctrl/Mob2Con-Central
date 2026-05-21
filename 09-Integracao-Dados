@echo off
REM Script de Sincronização Diária Redshift → Google Sheets
REM Executado automaticamente pelo Task Scheduler

cd /d "C:\Users\Donizete Senne\Desktop\Mob2Con-Central"

echo ========================================
echo Sincronizacao Redshift - Google Sheets
echo Data/Hora: %date% %time%
echo ========================================
echo.

python sync_redshift_daily.py

echo.
echo ========================================
echo Sincronizacao finalizada
echo ========================================
echo.

REM Manter janela aberta por 10 segundos se executado manualmente
timeout /t 10 /nobreak >nul
