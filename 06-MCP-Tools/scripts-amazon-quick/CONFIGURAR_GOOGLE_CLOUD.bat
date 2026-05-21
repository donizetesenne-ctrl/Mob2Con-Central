@echo off
REM ═══════════════════════════════════════════════════════════════
REM 🔧 CONFIGURADOR AUTOMÁTICO - Google Cloud Project
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🔧 CONFIGURADOR GOOGLE CLOUD PROJECT - Mob2Con Relatórios
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar se já existe credentials
set CRED_PATH=%USERPROFILE%\.aws\amazonq\universal-control\google-credentials.json

if exist "%CRED_PATH%" (
    echo ✅ Credentials já existe em:
    echo    %CRED_PATH%
    echo.
    choice /C SN /M "Deseja reconfigurar (S/N)"
    if errorlevel 2 goto :fim
)

echo 📋 PASSO 1: Abrindo Google Cloud Console...
echo.
start https://console.cloud.google.com/projectcreate

echo ═══════════════════════════════════════════════════════════════
echo 📝 INSTRUÇÕES - Siga na tela do navegador:
echo ═══════════════════════════════════════════════════════════════
echo.
echo 1️⃣ CRIAR PROJETO:
echo    Nome do projeto: Mob2Con Relatorios
echo    Clique em: CREATE
echo    Aguarde alguns segundos...
echo.
pause

echo.
echo 2️⃣ HABILITAR APIs:
echo    Abrindo página de APIs...
echo.
start https://console.cloud.google.com/apis/library/docs.googleapis.com
timeout /t 3 >nul
start https://console.cloud.google.com/apis/library/drive.googleapis.com
timeout /t 3 >nul
start https://console.cloud.google.com/apis/library/sheets.googleapis.com

echo.
echo    Para CADA aba aberta:
echo    - Selecione o projeto "Mob2Con Relatorios"
echo    - Clique em ENABLE
echo    - Aguarde ativar
echo.
pause

echo.
echo 3️⃣ CRIAR CREDENTIALS:
echo    Abrindo página de Credentials...
echo.
start https://console.cloud.google.com/apis/credentials

echo.
echo    Na página que abriu:
echo    1. Clique em: + CREATE CREDENTIALS
echo    2. Escolha: OAuth client ID
echo    3. Se pedir "Configure consent screen":
echo       - Clique em "Configure consent screen"
echo       - User Type: External
echo       - Clique: CREATE
echo       - App name: Mob2Con Relatorios
echo       - User support email: seu email
echo       - Developer contact: seu email
echo       - Clique: SAVE AND CONTINUE (3 vezes)
echo       - Clique: BACK TO DASHBOARD
echo       - Volte para Credentials
echo    4. Clique novamente: + CREATE CREDENTIALS → OAuth client ID
echo    5. Application type: Desktop app
echo    6. Name: Mob2Con Desktop Client
echo    7. Clique: CREATE
echo    8. Clique em: DOWNLOAD JSON
echo.
pause

echo.
echo 4️⃣ SALVAR CREDENTIALS:
echo.
echo    Agora vou abrir a pasta onde você deve salvar o arquivo:
echo.
pause

REM Criar pasta se não existir
if not exist "%USERPROFILE%\.aws\amazonq\universal-control" (
    mkdir "%USERPROFILE%\.aws\amazonq\universal-control"
)

REM Abrir pasta no Explorer
start "" "%USERPROFILE%\.aws\amazonq\universal-control"

echo.
echo    📂 Pasta aberta no Explorer!
echo.
echo    IMPORTANTE:
echo    1. Vá na pasta Downloads
echo    2. Encontre o arquivo: client_secret_XXXXX.json
echo    3. COPIE o arquivo
echo    4. COLE na pasta que acabou de abrir
echo    5. RENOMEIE para: google-credentials.json
echo.
echo    Caminho final deve ser:
echo    %CRED_PATH%
echo.
pause

echo.
echo 5️⃣ VERIFICANDO...
echo.

if exist "%CRED_PATH%" (
    echo ✅ SUCESSO! Credentials encontrado!
    echo.
    echo    Arquivo: %CRED_PATH%
    echo    Tamanho: 
    for %%A in ("%CRED_PATH%") do echo    %%~zA bytes
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ✅ CONFIGURAÇÃO CONCLUÍDA!
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo PRÓXIMOS PASSOS:
    echo 1. Execute: INSTALAR_RELATORIO.bat
    echo 2. O sistema vai pedir autorização no navegador
    echo 3. Faça login com sua conta Google
    echo 4. Autorize o acesso
    echo.
) else (
    echo ❌ ERRO: Credentials não encontrado!
    echo.
    echo    Verifique se você:
    echo    1. Baixou o arquivo JSON
    echo    2. Copiou para a pasta correta
    echo    3. Renomeou para: google-credentials.json
    echo.
    echo    Caminho esperado:
    echo    %CRED_PATH%
    echo.
    echo Execute este script novamente após corrigir.
    echo.
)

:fim
pause
