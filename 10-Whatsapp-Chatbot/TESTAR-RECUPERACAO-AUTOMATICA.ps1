[CmdletBinding()]
param(
    [switch]$Executar
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $Executar) {
    throw "Teste interrompe o bot por ate 90 segundos. Use -Executar conscientemente."
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
$probe = Join-Path $root "scripts\sonda_persistencia.py"
$supervisor = Join-Path $root "SUPERVISOR-SERVICOS.ps1"
$heartbeat = Join-Path $root "dados\watchdog-heartbeat.json"
$botUri = "http://127.0.0.1:8000/health"
$gatewayUri = "http://127.0.0.1:8080/health"
$marker = [Guid]::NewGuid().ToString("N")
$probeWritten = $false
$testPassed = $false

function Test-HttpReady {
    param([Parameter(Mandatory = $true)][string]$Uri)
    try {
        $response = Invoke-WebRequest `
            -UseBasicParsing `
            -Uri $Uri `
            -TimeoutSec 4
        return $response.StatusCode -ge 200 -and $response.StatusCode -lt 300
    } catch {
        return $false
    }
}

function Get-BotPid {
    $connection = Get-NetTCPConnection `
        -State Listen `
        -LocalPort 8000 `
        -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($null -eq $connection) {
        return 0
    }
    return [int]$connection.OwningProcess
}

function Assert-ManagedBot {
    param([Parameter(Mandatory = $true)][int]$ProcessId)
    $process = Get-CimInstance Win32_Process `
        -Filter "ProcessId = $ProcessId" `
        -ErrorAction Stop
    if (
        $process.Name -notin @("python.exe", "pythonw.exe") -or
        $process.CommandLine -notlike "*uvicorn bot.main:app*" -or
        $process.CommandLine -notlike "*--port 8000*"
    ) {
        throw "PID $ProcessId na porta 8000 nao pertence ao bot Mob2Con."
    }
}

function Restore-Bot {
    if (-not (Test-HttpReady -Uri $botUri)) {
        & powershell.exe `
            -NoProfile `
            -NonInteractive `
            -ExecutionPolicy Bypass `
            -File $supervisor
    }
}

foreach ($required in @($python, $probe, $supervisor, $heartbeat)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Arquivo obrigatorio ausente: $required"
    }
}
if (-not (Test-HttpReady -Uri $gatewayUri)) {
    throw "Gateway 8080 nao esta saudavel; teste cancelado."
}
if (-not (Test-HttpReady -Uri $botUri)) {
    throw "Bot 8000 nao esta saudavel; teste cancelado."
}

$pidBefore = Get-BotPid
Assert-ManagedBot -ProcessId $pidBefore
$heartbeatBefore = (Get-Item -LiteralPath $heartbeat).LastWriteTimeUtc
Write-Output "Bot antes: PID=$pidBefore"

try {
    & $python $probe gravar --marcador $marker
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao gravar sonda SQLite."
    }
    $probeWritten = $true

    Stop-Process -Id $pidBefore -Force -ErrorAction Stop
    Write-Output "Falha controlada aplicada ao bot PID=$pidBefore."

    $deadline = [DateTime]::UtcNow.AddSeconds(110)
    $pidAfter = 0
    do {
        $candidate = Get-BotPid
        if (
            $candidate -ne 0 -and
            $candidate -ne $pidBefore -and
            (Test-HttpReady -Uri $botUri)
        ) {
            $pidAfter = $candidate
            break
        }
        Start-Sleep -Seconds 1
    } while ([DateTime]::UtcNow -lt $deadline)

    if ($pidAfter -eq 0) {
        throw "Watchdog nao recuperou o bot em 110 segundos."
    }
    Assert-ManagedBot -ProcessId $pidAfter

    $heartbeatAfter = (Get-Item -LiteralPath $heartbeat).LastWriteTimeUtc
    if ($heartbeatAfter -le $heartbeatBefore) {
        throw "Heartbeat nao avancou durante a recuperacao."
    }
    if (-not (Test-HttpReady -Uri $gatewayUri)) {
        throw "Gateway perdeu saude durante recuperacao do bot."
    }

    & $python $probe verificar --marcador $marker
    if ($LASTEXITCODE -ne 0) {
        throw "Sessao sintetica nao persistiu ao reinicio."
    }

    $testPassed = $true
    Write-Output (
        "RECUPERACAO_BOT_OK | PID antes=$pidBefore" +
        " | PID depois=$pidAfter | SQLite=preservado"
    )
} finally {
    if ($probeWritten) {
        & $python $probe limpar | Out-Null
    }
    if (-not $testPassed) {
        Restore-Bot
    }
}
