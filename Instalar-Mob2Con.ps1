# ============================================================
#  Mob2Con Central - Instalador Automatico
#  Versao: 1.0 | Maio 2026
# ============================================================

$ErrorActionPreference = "Continue"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════════╗" -ForegroundColor DarkYellow
Write-Host "  ║   MOB2CON CENTRAL - INSTALADOR v1.0         ║" -ForegroundColor DarkYellow
Write-Host "  ╚══════════════════════════════════════════════╝" -ForegroundColor DarkYellow
Write-Host ""

# ============================================================
# PASSO 1: Verificar dependencias
# ============================================================
Write-Host "[1/5] Verificando dependencias..." -ForegroundColor Cyan

$errors = @()

# Node.js
$nodeVersion = node --version 2>$null
if ($nodeVersion) {
    Write-Host "  ✓ Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Node.js NAO encontrado" -ForegroundColor Red
    Write-Host "    Baixe em: https://nodejs.org" -ForegroundColor Gray
    $errors += "Node.js"
}

# Python/uvx
$uvxPath = Get-Command uvx -ErrorAction SilentlyContinue
if ($uvxPath) {
    Write-Host "  ✓ uvx: $($uvxPath.Source)" -ForegroundColor Green
} else {
    Write-Host "  ✗ uvx NAO encontrado" -ForegroundColor Red
    Write-Host "    Instale com: pip install uv" -ForegroundColor Gray
    $errors += "uvx"
}

# npx
$npxPath = Get-Command npx.cmd -ErrorAction SilentlyContinue
if ($npxPath) {
    Write-Host "  ✓ npx: $($npxPath.Source)" -ForegroundColor Green
} else {
    Write-Host "  ✗ npx NAO encontrado (vem com Node.js)" -ForegroundColor Red
    $errors += "npx"
}

# Power BI MCP exe
$pbiExe = "$env:USERPROFILE\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe"
if (Test-Path $pbiExe) {
    Write-Host "  ✓ Power BI MCP: encontrado" -ForegroundColor Green
} else {
    Write-Host "  ✗ Power BI MCP NAO encontrado" -ForegroundColor Yellow
    Write-Host "    Instale a extensao 'Power BI Modeling MCP' no VS Code/Kiro" -ForegroundColor Gray
    $errors += "PowerBI-MCP"
}

if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "  ⚠ Dependencias em falta: $($errors -join ', ')" -ForegroundColor Yellow
    Write-Host "  A instalacao vai continuar, mas algumas MCPs podem nao funcionar." -ForegroundColor Yellow
    Write-Host ""
}

# ============================================================
# PASSO 2: Copiar pasta central para Desktop
# ============================================================
Write-Host ""
Write-Host "[2/5] Instalando pasta Mob2Con-Central..." -ForegroundColor Cyan

$destino = "$env:USERPROFILE\Desktop\Mob2Con-Central"
if (Test-Path $destino) {
    Write-Host "  Pasta ja existe em: $destino" -ForegroundColor Yellow
    Write-Host "  Mantendo existente (nao sobrescreve)" -ForegroundColor Gray
} else {
    Copy-Item $ScriptDir -Destination $destino -Recurse -Force
    Write-Host "  ✓ Pasta copiada para: $destino" -ForegroundColor Green
}

# ============================================================
# PASSO 3: Instalar node_modules do powerbi-layout-mcp
# ============================================================
Write-Host ""
Write-Host "[3/5] Instalando dependencias Node.js..." -ForegroundColor Cyan

$layoutMcp = "$destino\06-MCP-Tools\powerbi-layout-mcp"
if (Test-Path "$layoutMcp\package.json") {
    Push-Location $layoutMcp
    npm install --silent 2>$null
    Pop-Location
    Write-Host "  ✓ powerbi-layout-mcp: dependencias instaladas" -ForegroundColor Green
}

# ============================================================
# PASSO 4: Configurar MCPs
# ============================================================
Write-Host ""
Write-Host "[4/5] Configurando MCPs..." -ForegroundColor Cyan

# Detectar caminho curto (8.3) para evitar problemas com espacos
$shortPath = (New-Object -ComObject Scripting.FileSystemObject).GetFolder($env:USERPROFILE).ShortPath

# --- Kiro ---
$kiroDir = "$env:USERPROFILE\.kiro\settings"
if (-not (Test-Path $kiroDir)) { New-Item -ItemType Directory -Path $kiroDir -Force | Out-Null }

$kiroConfig = @{
    mcpServers = @{
        "aws-docs" = @{
            command = "uvx"
            args = @("awslabs.aws-documentation-mcp-server@latest")
            env = @{ FASTMCP_LOG_LEVEL = "ERROR" }
            disabled = $false
            autoApprove = @()
        }
        "powerbi-layout" = @{
            command = "node"
            args = @("$shortPath\Downloads\Mob2Con-Bridge-v2.0.0\mcp\powerbi-layout-mcp\server.js")
            type = "stdio"
            env = @{
                POWERBI_PROJECT_PATH = "$shortPath\Desktop\Mob2Con-Central\02-Powerbi-Projetos"
                MOB2CON_BRAND_CONTEXT = "$shortPath\Desktop\Mob2Con-Central\01-Brand-Guidelines\Mob2con-brand-guidelines.md"
                MOB2CON_LAYOUT_BASE = "$shortPath\Desktop\Mob2Con-Central\01-Brand-Guidelines\Mob2con-layout-base.md"
            }
        }
    }
} | ConvertTo-Json -Depth 10

$kiroFile = "$kiroDir\mcp.json"
if (Test-Path $kiroFile) {
    Copy-Item $kiroFile "$kiroFile.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
}
[System.IO.File]::WriteAllText($kiroFile, $kiroConfig, [System.Text.UTF8Encoding]::new($false))
Write-Host "  ✓ Kiro configurado: $kiroFile" -ForegroundColor Green

# --- Amazon Quick (se existir) ---
$quickProfile = Get-ChildItem "$env:USERPROFILE\.quickwork\profiles" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
if ($quickProfile) {
    $quickFile = "$($quickProfile.FullName)\mcp_config.json"
    if (Test-Path $quickFile) {
        Copy-Item $quickFile "$quickFile.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
    }

    $quickConfig = @{
        mcpServers = @{
            "powerbi-official" = @{
                command = "$shortPath\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe"
                args = @("--start")
                _quick = @{ name = "powerbi" }
            }
            "powerbi-layout" = @{
                command = "node"
                args = @("$shortPath\Downloads\Mob2Con-Bridge-v2.0.0\mcp\powerbi-layout-mcp\server.js")
                env = @{
                    POWERBI_PROJECT_PATH = "$shortPath\Desktop\Mob2Con-Central\02-Powerbi-Projetos"
                    MOB2CON_BRAND_CONTEXT = "$shortPath\Desktop\Mob2Con-Central\01-Brand-Guidelines\Mob2con-brand-guidelines.md"
                    MOB2CON_LAYOUT_BASE = "$shortPath\Desktop\Mob2Con-Central\01-Brand-Guidelines\Mob2con-layout-base.md"
                }
                _quick = @{ name = "powerbi-layout" }
            }
            "universal-control" = @{
                command = "node"
                args = @("$shortPath\Desktop\Mob2Con_MCP_Setup\universal-control-mcp\server.js")
                env = @{
                    UCM_CONFIG_PATH = "$shortPath\.aws\amazonq\universal-control\ucm-secrets.json"
                    UCM_DISABLE_APPSHEET = "true"
                    UCM_LOCAL_ROOTS = "$shortPath\Desktop\Mob2Con-Central;$shortPath\Desktop;$shortPath\Documents;$shortPath\Downloads"
                    UCM_AUTO_BACKUP = "true"
                    UCM_MAX_TEXT_CHARS = "50000"
                    UCM_MAX_CELLS = "40000"
                    UCM_PYTHON_PATH = "python"
                }
                _quick = @{ name = "universal_control" }
            }
            "aws-docs" = @{
                command = "uvx"
                args = @("awslabs.aws-documentation-mcp-server@latest")
                env = @{ FASTMCP_LOG_LEVEL = "ERROR" }
                _quick = @{ name = "aws-docs" }
            }
            "shell-command" = @{
                command = "npx.cmd"
                args = @("-y", "shell-command-mcp")
                _quick = @{ name = "shell-command" }
            }
            "filesystem" = @{
                command = "npx.cmd"
                args = @("-y", "@modelcontextprotocol/server-filesystem", "$shortPath\Desktop\Mob2Con-Central", "$shortPath\Desktop", "$shortPath\Documents", "$shortPath\Downloads")
                _quick = @{ name = "filesystem" }
            }
        }
    } | ConvertTo-Json -Depth 10

    [System.IO.File]::WriteAllText($quickFile, $quickConfig, [System.Text.UTF8Encoding]::new($false))
    Write-Host "  ✓ Amazon Quick configurado: $quickFile" -ForegroundColor Green
} else {
    Write-Host "  - Amazon Quick nao encontrado (pular)" -ForegroundColor Gray
}

# ============================================================
# PASSO 5: Verificacao final
# ============================================================
Write-Host ""
Write-Host "[5/5] Verificacao final..." -ForegroundColor Cyan

$checks = @(
    @{ Name = "Pasta central"; Path = $destino },
    @{ Name = "Brand Guidelines"; Path = "$destino\01-Brand-Guidelines\Mob2Con-Theme.json" },
    @{ Name = "DAX Library"; Path = "$destino\03-Documentacao\Mob2con-dax-medidas-padrao.md" },
    @{ Name = "Kiro config"; Path = $kiroFile }
)

$allOk = $true
foreach ($check in $checks) {
    if (Test-Path $check.Path) {
        Write-Host "  ✓ $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $($check.Name): $($check.Path)" -ForegroundColor Red
        $allOk = $false
    }
}

# ============================================================
# RESULTADO
# ============================================================
Write-Host ""
Write-Host "  ╔══════════════════════════════════════════════╗" -ForegroundColor $(if ($allOk) { "Green" } else { "Yellow" })
if ($allOk) {
    Write-Host "  ║   ✓ INSTALACAO CONCLUIDA COM SUCESSO!      ║" -ForegroundColor Green
} else {
    Write-Host "  ║   ⚠ INSTALACAO PARCIAL (verifique erros)   ║" -ForegroundColor Yellow
}
Write-Host "  ╚══════════════════════════════════════════════╝" -ForegroundColor $(if ($allOk) { "Green" } else { "Yellow" })
Write-Host ""
Write-Host "  Proximos passos:" -ForegroundColor White
Write-Host "  1. Reinicie o Kiro e/ou Amazon Quick" -ForegroundColor Gray
Write-Host "  2. Abra um projeto .pbip no Power BI Desktop" -ForegroundColor Gray
Write-Host "  3. Aplique o tema: View > Themes > Browse > Mob2Con-Theme.json" -ForegroundColor Gray
Write-Host "  4. Leia o README.md na pasta Mob2Con-Central" -ForegroundColor Gray
Write-Host ""
Write-Host "  Pasta instalada: $destino" -ForegroundColor Cyan
Write-Host ""
