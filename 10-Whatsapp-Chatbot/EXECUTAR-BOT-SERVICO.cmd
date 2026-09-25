@echo off
setlocal
set "ROOT=C:\Users\Donizete Senne\Desktop\Mob2Con-Central\10-Whatsapp-Chatbot"
cd /d "%ROOT%"
"%ROOT%\.venv\Scripts\python.exe" -m uvicorn bot.main:app --host 127.0.0.1 --port 8000 >NUL 2>&1
exit /b %ERRORLEVEL%
