@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo   INSTALADOR — NVIDIA NIM Stack (IA Gratuita)
echo   3 modelos de IA no seu terminal
echo ============================================================
echo.

:: Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo    Python nao encontrado!
    echo    Baixe em: https://www.python.org/downloads/
    echo    Marque "Add Python to PATH" na instalacao.
    echo.
    pause
    exit /b 1
)
echo    Python encontrado!

:: Instalar dependencia
echo.
echo [2/4] Instalando pacote openai...
pip install openai >nul 2>&1
if errorlevel 1 (
    echo    Tentando com --user...
    pip install --user openai >nul 2>&1
)
echo    Pacote openai instalado!

:: Configurar API key
echo.
echo [3/4] Configurando API key...
if exist config.json (
    echo    config.json ja existe!
) else (
    echo.
    echo    Voce precisa de uma API key gratuita da NVIDIA.
    echo    1. Acesse: https://build.nvidia.com
    echo    2. Crie conta gratuita
    echo    3. Gere key em: https://org.ngc.nvidia.com/setup/api-keys
    echo.
    set /p NVIDIA_KEY="    Cole sua API key aqui (nvapi-...): "
    if "%NVIDIA_KEY%"=="" (
        echo    Key vazia! Copie config_exemplo.json para config.json manualmente.
        copy config_exemplo.json config.json >nul
    ) else (
        echo {> config.json
        echo   "nvidia_api_key": "%NVIDIA_KEY%",>> config.json
        echo   "base_url": "https://integrate.api.nvidia.com/v1",>> config.json
        echo   "modelos": {>> config.json
        echo     "analise": {>> config.json
        echo       "nome": "meta/llama-3.3-70b-instruct",>> config.json
        echo       "descricao": "Analise profunda de dados, raciocinio, KPIs",>> config.json
        echo       "max_tokens": 4096,>> config.json
        echo       "temperature": 0.3>> config.json
        echo     },>> config.json
        echo     "codigo": {>> config.json
        echo       "nome": "nvidia/llama-3.3-nemotron-super-49b-v1",>> config.json
        echo       "descricao": "Geracao de codigo, apps, SQL, DAX",>> config.json
        echo       "max_tokens": 4096,>> config.json
        echo       "temperature": 0.2>> config.json
        echo     },>> config.json
        echo     "layout": {>> config.json
        echo       "nome": "nvidia/nemotron-nano-12b-v2-vl",>> config.json
        echo       "descricao": "Analise visual, imagens, wireframes, layout",>> config.json
        echo       "max_tokens": 2048,>> config.json
        echo       "temperature": 0.4>> config.json
        echo     }>> config.json
        echo   },>> config.json
        echo   "system_prompts": {>> config.json
        echo     "analise": "Voce e um analista de dados especialista em logistica e varejo brasileiro. Responda sempre em portugues.",>> config.json
        echo     "codigo": "Voce e um desenvolvedor Python/Streamlit/FastAPI especialista. Gere codigo limpo e comentado.",>> config.json
        echo     "layout": "Voce e um designer de dashboards. Analise layouts e sugira melhorias de UX.">> config.json
        echo   }>> config.json
        echo }>> config.json
        echo    config.json criado com sua key!
    )
)

:: Testar conexao
echo.
echo [4/4] Testando conexao com NVIDIA...
python -c "from nvidia_nim_client import NvidiaStack; s = NvidiaStack(); print('    Conexao OK!'); [print(f'       [{k}] {v[chr(34)+chr(110)+chr(111)+chr(109)+chr(101)+chr(34)]}') for k,v in s.modelos.items()]" 2>nul
if errorlevel 1 (
    echo    Teste falhou. Verifique sua API key no config.json
)

echo.
echo ============================================================
echo   INSTALACAO CONCLUIDA!
echo ============================================================
echo.
echo   Para usar:
echo     python chat.py          - Chat interativo (3 IAs)
echo     python demo_analise.py  - Demo analise de dados
echo     python demo_codigo.py   - Demo geracao de codigo
echo     python demo_layout.py   - Demo analise de layout
echo.
echo   No chat, use:
echo     /analise  - IA de dados (Llama 3.3 70B)
echo     /codigo   - IA de codigo (Nemotron Super 49B)
echo     /layout   - IA de layout (Nemotron Nano 12B VL)
echo     /sair     - Encerrar
echo.
echo   Quer abrir o chat agora? (S/N)
set /p ABRIR="   > "
if /i "%ABRIR%"=="S" python chat.py
if /i "%ABRIR%"=="s" python chat.py

pause
