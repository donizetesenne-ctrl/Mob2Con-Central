@echo off
REM ═══════════════════════════════════════════════════════════════
REM 🚀 CONFIGURADOR AUTOMÁTICO COMPLETO - Google Cloud
REM Projeto: My Project 53522 (symbolic-envoy-496315-g9)
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🚀 CONFIGURADOR AUTOMÁTICO - Mob2Con Relatórios
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ Usando projeto existente:
echo    Nome: My Project 53522
echo    ID: symbolic-envoy-496315-g9
echo    Número: 436757880380
echo.
echo Este script vai:
echo ✅ Habilitar as 3 APIs necessárias
echo ✅ Configurar OAuth Consent Screen
echo ✅ Criar OAuth Client ID
echo ✅ Baixar credentials automaticamente
echo.
pause

REM ═══════════════════════════════════════════════════════════════
REM PASSO 1: HABILITAR APIs
REM ═══════════════════════════════════════════════════════════════

echo.
echo [1/5] Habilitando APIs...
echo.

echo 📊 Google Docs API...
start https://console.cloud.google.com/apis/library/docs.googleapis.com?project=symbolic-envoy-496315-g9
timeout /t 3 >nul

echo 📂 Google Drive API...
start https://console.cloud.google.com/apis/library/drive.googleapis.com?project=symbolic-envoy-496315-g9
timeout /t 3 >nul

echo 📋 Google Sheets API...
start https://console.cloud.google.com/apis/library/sheets.googleapis.com?project=symbolic-envoy-496315-g9

echo.
echo ✅ 3 abas abertas!
echo.
echo ⚠️ AÇÃO NECESSÁRIA:
echo    Para CADA aba aberta, clique em: ENABLE (ou ATIVAR)
echo    Aguarde ativar e feche a aba
echo.
pause

REM ═══════════════════════════════════════════════════════════════
REM PASSO 2: OAUTH CONSENT SCREEN
REM ═══════════════════════════════════════════════════════════════

echo.
echo [2/5] Configurando OAuth Consent Screen...
echo.

start https://console.cloud.google.com/apis/credentials/consent?project=symbolic-envoy-496315-g9

echo.
echo ⚠️ AÇÃO NECESSÁRIA:
echo.
echo 1. User Type: EXTERNAL
echo 2. CREATE
echo.
echo 3. Preencha:
echo    App name: Mob2Con Relatorios
echo    User support email: (seu email)
echo    Developer contact: (seu email)
echo.
echo 4. SAVE AND CONTINUE (3 vezes)
echo 5. BACK TO DASHBOARD
echo.
pause

REM ═══════════════════════════════════════════════════════════════
REM PASSO 3: CRIAR OAUTH CLIENT
REM ═══════════════════════════════════════════════════════════════

echo.
echo [3/5] Criando OAuth Client ID...
echo.

start https://console.cloud.google.com/apis/credentials?project=symbolic-envoy-496315-g9

echo.
echo ⚠️ AÇÃO NECESSÁRIA:
echo.
echo 1. + CREATE CREDENTIALS
echo 2. OAuth client ID
echo 3. Application type: Desktop app
echo 4. Name: Mob2Con Desktop Client
echo 5. CREATE
echo 6. DOWNLOAD JSON
echo.
echo O arquivo será baixado para Downloads
echo Nome: client_secret_XXXXX.json
echo.
pause

REM ═══════════════════════════════════════════════════════════════
REM PASSO 4: MOVER E RENOMEAR CREDENTIALS
REM ═══════════════════════════════════════════════════════════════

echo.
echo [4/5] Configurando credentials...
echo.

REM Criar estrutura de pastas
set DEST_DIR=%USERPROFILE%\.aws\amazonq\universal-control
set CRED_FILE=%DEST_DIR%\google-credentials.json

if not exist "%DEST_DIR%" (
    echo Criando pastas...
    mkdir "%USERPROFILE%\.aws" 2>nul
    mkdir "%USERPROFILE%\.aws\amazonq" 2>nul
    mkdir "%DEST_DIR%" 2>nul
    echo ✅ Pastas criadas!
)

REM Procurar arquivo baixado
echo.
echo Procurando arquivo baixado...
echo.

set DOWNLOADS=%USERPROFILE%\Downloads
set FOUND=0

for %%F in ("%DOWNLOADS%\client_secret_*.json") do (
    echo ✅ Encontrado: %%~nxF
    echo.
    echo Copiando para: %DEST_DIR%
    copy "%%F" "%CRED_FILE%" >nul
    if exist "%CRED_FILE%" (
        echo ✅ Copiado com sucesso!
        set FOUND=1
        goto :verificar
    )
)

if %FOUND%==0 (
    echo ⚠️ Arquivo não encontrado automaticamente!
    echo.
    echo Abrindo pastas para você fazer manualmente...
    echo.
    start "" "%DOWNLOADS%"
    timeout /t 1 >nul
    start "" "%DEST_DIR%"
    echo.
    echo FAÇA MANUALMENTE:
    echo 1. Na pasta DOWNLOADS: copie client_secret_XXXXX.json
    echo 2. Na pasta UNIVERSAL-CONTROL: cole
    echo 3. Renomeie para: google-credentials.json
    echo.
    pause
)

REM ═══════════════════════════════════════════════════════════════
REM PASSO 5: VERIFICAR
REM ═══════════════════════════════════════════════════════════════

:verificar
echo.
echo [5/5] Verificando configuração...
echo.

if exist "%CRED_FILE%" (
    echo ✅ Credentials encontrado!
    echo    %CRED_FILE%
    echo.
    
    REM Verificar conteúdo
    findstr /C:"client_id" "%CRED_FILE%" >nul
    if errorlevel 1 (
        echo ❌ Arquivo inválido!
        goto :erro
    )
    
    echo ✅ Arquivo válido!
    echo.
    
    REM Mostrar informações
    for %%A in ("%CRED_FILE%") do (
        echo Tamanho: %%~zA bytes
        echo Data: %%~tA
    )
    
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo 🎉 Tudo pronto! Agora execute:
    echo.
    echo    INSTALAR_RELATORIO.bat
    echo.
    echo O instalador vai:
    echo ✅ Instalar Python e dependências
    echo ✅ Abrir navegador para autorização
    echo ✅ Salvar token automaticamente
    echo ✅ Testar o sistema
    echo.
    
) else (
    :erro
    echo ❌ Credentials não encontrado!
    echo.
    echo Caminho esperado:
    echo %CRED_FILE%
    echo.
    echo Execute este script novamente ou configure manualmente.
    echo.
)

pause
