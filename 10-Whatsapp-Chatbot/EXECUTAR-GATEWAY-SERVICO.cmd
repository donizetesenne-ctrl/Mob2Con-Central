@echo off
setlocal
set "ROOT=C:\Users\Donizete Senne\Desktop\Mob2Con-Central\10-Whatsapp-Chatbot"
cd /d "%ROOT%\gateway"
"C:\Program Files\nodejs\node.exe" --env-file="%ROOT%\.env" "%ROOT%\gateway\index.js" >NUL 2>&1
exit /b %ERRORLEVEL%
