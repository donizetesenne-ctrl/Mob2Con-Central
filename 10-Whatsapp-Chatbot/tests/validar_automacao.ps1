Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$powerShellFiles = @(
    "SUPERVISOR-SERVICOS.ps1",
    "INSTALAR-INICIALIZACAO-AUTOMATICA.ps1",
    "STATUS-AUTOMACAO.ps1",
    "REMOVER-INICIALIZACAO-AUTOMATICA.ps1",
    "REINICIAR-SERVICO.ps1",
    "TESTAR-RECUPERACAO-AUTOMATICA.ps1",
    "TESTAR-RECUPERACAO-GATEWAY.ps1"
)
$batchFiles = @(
    "INICIAR-SEM-DOCKER.bat",
    "REINICIAR-BOT.bat",
    "INICIAR-GATEWAY.bat",
    "INSTALAR-INICIALIZACAO-AUTOMATICA.bat",
    "STATUS-AUTOMACAO.bat",
    "REMOVER-INICIALIZACAO-AUTOMATICA.bat"
)
$failures = New-Object System.Collections.Generic.List[string]

foreach ($relative in $powerShellFiles) {
    $path = Join-Path $root $relative
    if (-not (Test-Path -LiteralPath $path)) {
        $failures.Add("Ausente: $relative")
        continue
    }

    $tokens = $null
    $parseErrors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $path,
        [ref]$tokens,
        [ref]$parseErrors
    )
    foreach ($parseError in @($parseErrors)) {
        $failures.Add(
            "${relative}:$($parseError.Extent.StartLineNumber): " +
            $parseError.Message
        )
    }
}

foreach ($relative in $batchFiles) {
    $path = Join-Path $root $relative
    if (-not (Test-Path -LiteralPath $path)) {
        $failures.Add("Ausente: $relative")
        continue
    }
    $content = Get-Content -LiteralPath $path -Raw
    if ($content -match "Bot Supervisor|Gateway Supervisor") {
        $failures.Add("Referencia a tarefa legada em $relative")
    }
    if ($content -match "python\s+-c") {
        $failures.Add("Python inline proibido em $relative")
    }
}

$installer = Get-Content `
    -LiteralPath (Join-Path $root "INSTALAR-INICIALIZACAO-AUTOMATICA.ps1") `
    -Raw
$status = Get-Content `
    -LiteralPath (Join-Path $root "STATUS-AUTOMACAO.ps1") `
    -Raw
foreach ($required in @(
    "Mob2ConChatbotWatchdog",
    "watchdog_servicos.py",
    "CurrentVersion\Run"
)) {
    if ($installer -notmatch [regex]::Escape($required)) {
        $failures.Add("Instalador sem referencia obrigatoria: $required")
    }
    if ($status -notmatch [regex]::Escape($required)) {
        $failures.Add("Status sem referencia obrigatoria: $required")
    }
}

if ($failures.Count -gt 0) {
    foreach ($failure in $failures) {
        Write-Error $failure
    }
    throw "Gate de automacao falhou com $($failures.Count) erro(s)."
}

Write-Output (
    "AUTOMATION_STATIC_OK | PowerShell=$($powerShellFiles.Count)" +
    " | Batch=$($batchFiles.Count)"
)
