@echo off
echo ========================================
echo  Mob2Con Doc Converters - Instalacao
echo  Docling + Marker + MinerU
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Criando venv...
python -m venv .venv
call .venv\Scripts\activate.bat

echo [2/3] Instalando dependencias...
pip install -r requirements.txt

echo [3/3] Pronto!
echo.
echo Uso:
echo   .venv\Scripts\activate.bat
echo   python converter.py arquivo.pdf --engine docling
echo   python converter.py pasta\ --engine marker --batch
echo.
pause
