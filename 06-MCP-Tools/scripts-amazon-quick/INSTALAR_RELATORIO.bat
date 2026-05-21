@echo off
REM ═══════════════════════════════════════════════════════════════
REM 📊 INSTALADOR RÁPIDO — Sistema de Relatório Semanal Mob2Con
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo 📊 INSTALADOR — Sistema de Relatório Semanal Mob2Con
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo    Instale em: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python encontrado

REM Instalar dependências
echo.
echo [2/5] Instalando dependências Python...
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dateutil
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)
echo ✅ Dependências instaladas

REM Criar diretórios
echo.
echo [3/5] Criando estrutura de pastas...
if not exist "backups" mkdir backups
if not exist "logs" mkdir logs
echo ✅ Pastas criadas

REM Verificar credentials
echo.
echo [4/5] Verificando credentials.json...
set CRED_PATH=%USERPROFILE%\.aws\amazonq\universal-control\google-credentials.json
if not exist "%CRED_PATH%" (
    echo ⚠️ credentials.json não encontrado em:
    echo    %CRED_PATH%
    echo.
    echo    PRÓXIMOS PASSOS:
    echo    1. Acesse: https://console.cloud.google.com/
    echo    2. Crie projeto "Mob2Con Relatórios"
    echo    3. Habilite: Google Docs API, Drive API, Sheets API
    echo    4. Credentials → OAuth 2.0 Client ID → Desktop app
    echo    5. Baixe credentials.json
    echo    6. Salve em: %CRED_PATH%
    echo    7. Execute novamente este instalador
    echo.
    pause
    exit /b 1
)
echo ✅ credentials.json encontrado

REM Primeira autenticação
echo.
echo [5/5] Iniciando primeira autenticação...
echo     Uma janela do navegador vai abrir para autorizar.
echo     Faça login com sua conta Google e autorize.
echo.
pause
python relatorio_semanal_auto.py --test
if errorlevel 1 (
    echo ❌ Erro na autenticação
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo ✅ INSTALAÇÃO CONCLUÍDA!
echo ═══════════════════════════════════════════════════════════════
echo.
echo PRÓXIMOS PASSOS:
echo.
echo 1. Configurar Apps Script:
echo    - Abra qualquer Google Sheets
echo    - Extensions → Apps Script
echo    - Cole o conteúdo de: relatorio_semanal_apps_script.gs
echo    - Edite EMAIL_GESTORA e NOME_GESTORA
echo    - Salve e execute uma vez para autorizar
echo    - Triggers → + → gerarRelatorioSemanal → Sexta 17:00
echo.
echo 2. Agendar Python (Task Scheduler):
echo    - Abra: taskschd.msc
echo    - Criar tarefa básica
echo    - Nome: Mob2Con - Processar Relatório
echo    - Trigger: Semanal, Sexta, 16:00
echo    - Action: python.exe
echo    - Arguments: "%CD%\relatorio_semanal_auto.py"
echo.
echo 3. Testar:
echo    - python relatorio_semanal_auto.py --test
echo.
echo 📖 Documentação completa: README_RELATORIO_SEMANAL.md
echo.
pause
