@echo off
:: ============================================
:: EXECUTAR COMO ADMINISTRADOR (botao direito > Executar como admin)
:: ============================================
echo Habilitando Windows Long Paths...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
if errorlevel 1 (
    echo.
    echo ERRO: Execute este script como ADMINISTRADOR!
    echo Botao direito no arquivo ^> Executar como administrador
    pause
    exit /b 1
)
echo.
echo Long Paths habilitado com sucesso!
echo.
echo Instalando PyTorch CPU e dependencias...
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers accelerate huggingface-hub safetensors tokenizers pyyaml packaging typer
echo.
echo ============================================
echo   PRONTO! Agora rode: SETUP.bat
echo ============================================
pause
