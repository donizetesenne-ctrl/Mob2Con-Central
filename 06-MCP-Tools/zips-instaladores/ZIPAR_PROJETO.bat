@echo off
chcp 65001 >nul
title Mob2Con - Zipar Projeto
color 0B

echo.
echo ============================================================
echo   MOB2CON - CRIANDO PACOTE ZIP PARA ENVIO
echo ============================================================
echo.

set "DESKTOP=C:\Users\%USERNAME%\Desktop"
set "DESTINO=%DESKTOP%\Mob2Con_Pacote_Completo.zip"

:: Remover zip antigo se existir
if exist "%DESTINO%" del "%DESTINO%"

echo Compactando projeto... Aguarde...
echo.

powershell -Command "& { $files = @('%DESKTOP%\projetos BI', '%DESKTOP%\projeto', '%DESKTOP%\powerbi-layout-mcp', '%DESKTOP%\Mob2con-Theme.json'); $zip = '%DESTINO%'; Add-Type -Assembly 'System.IO.Compression.FileSystem'; $archive = [System.IO.Compression.ZipFile]::Open($zip, 'Create'); foreach ($f in $files) { if (Test-Path $f) { if ((Get-Item $f).PSIsContainer) { $base = Split-Path $f -Parent; Get-ChildItem $f -Recurse | Where-Object { !$_.PSIsContainer } | ForEach-Object { $entry = $_.FullName.Substring($base.Length + 1); [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $_.FullName, $entry) | Out-Null } } else { $entry = Split-Path $f -Leaf; [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $f, $entry) | Out-Null } } }; $archive.Dispose() }"

if exist "%DESTINO%" (
    echo ============================================================
    echo   ZIP CRIADO COM SUCESSO!
    echo ============================================================
    echo.
    echo   Arquivo: %DESTINO%
    for %%A in ("%DESTINO%") do echo   Tamanho: %%~zA bytes
    echo.
    echo   Conteudo do pacote:
    echo   - projetos BI\         (todos os .pbip e dados)
    echo   - projeto\             (universal-control-mcp)
    echo   - powerbi-layout-mcp\  (MCP de layout)
    echo   - Mob2con-Theme.json   (tema visual)
    echo.
    echo   Envie o arquivo para seu colega e peca para:
    echo   1. Extrair no Desktop
    echo   2. Executar INSTALAR.bat dentro de "projetos BI"
    echo.
    :: Abrir pasta do arquivo
    explorer "%DESKTOP%"
) else (
    echo   ERRO ao criar o ZIP!
    echo   Tente zipar manualmente as pastas.
)

pause
