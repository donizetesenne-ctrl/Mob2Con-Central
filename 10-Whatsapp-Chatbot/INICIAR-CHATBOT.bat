@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   Chatbot WhatsApp Mob2Con
echo ============================================================
echo.

where docker >nul 2>&1
if errorlevel 1 (
    echo [X] Docker nao encontrado no PATH.
    echo.
    echo     Instale o Docker Desktop e abra ele antes de rodar:
    echo     https://www.docker.com/products/docker-desktop/
    echo.
    echo     Alternativa sem Docker: veja a secao "Rodar sem Docker"
    echo     no README.md deste projeto.
    echo.
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo [X] Docker esta instalado mas nao esta rodando.
    echo     Abra o Docker Desktop e espere ficar verde.
    echo.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [1/3] Gerando .env com segredos aleatorios...
    python scripts\gerar_env.py
    if errorlevel 1 (
        echo [X] Falha ao gerar o .env.
        pause
        exit /b 1
    )
    echo.
) else (
    echo [1/3] .env ja existe, mantendo.
    echo.
)

echo [2/3] Subindo Postgres, Redis, Evolution API e bot...
docker compose up -d
if errorlevel 1 (
    echo [X] Falha no docker compose up.
    pause
    exit /b 1
)
echo.

echo      Aguardando a Evolution API responder...
timeout /t 25 /nobreak >nul
echo.

echo [3/3] Instancia e QR Code
python scripts\setup_instancia.py
echo.

echo ============================================================
echo   Manager  : http://localhost:8080/manager
echo   Bot      : http://localhost:8000/health
echo.
echo   Logs     : docker compose logs -f bot
echo   Status   : python scripts\status.py
echo   Parar    : docker compose down
echo ============================================================
echo.
pause
