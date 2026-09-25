[CmdletBinding()]
param(
    [switch]$Executar
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $Executar) {
    throw "Teste interrompe o gateway por ate 120 segundos. Use -Executar conscientemente."
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$gatewayIndex = Join-Path $root "gateway\index.js"
$supervisor = Join-Path $root "SUPERVISOR-SERVICOS.ps1"
$heartbeat = Join-Path $root "dados\watchdog-heartbeat.json"
$credentials = Join-Path $root "gateway\sessao\creds.json"
$gatewayUri = "http://127.0.0.1:8080/health"
$botUri = "http://127.0.0.1:8000/health"
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

function Get-GatewayPid {
    $connection = Get-NetTCPConnection `
        -State Listen `
        -LocalPort 8080 `
        -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($null -eq $connection) {
        return 0
    }
    return [int]$connection.OwningProcess
}

function Assert-ManagedGateway {
    param([Parameter(Mandatory = $true)][int]$ProcessId)
    $process = Get-CimInstance Win32_Process `
        -Filter "ProcessId = $ProcessId" `
        -ErrorAction Stop
    if (
        $process.Name -ine "node.exe" -or
        $process.CommandLine -notlike "*$gatewayIndex*"
    ) {
        throw "PID $ProcessId na porta 8080 nao pertence ao gateway Mob2Con."
    }
}

function Restore-Gateway {
    if (-not (Test-HttpReady -Uri $gatewayUri)) {
        & powershell.exe `
            -NoProfile `
            -NonInteractive `
            -ExecutionPolicy Bypass `
            -File $supervisor
    }
}

foreach ($required in @($gatewayIndex, $supervisor, $heartbeat, $credentials)) {
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

$initialGateway = Invoke-RestMethod -Uri $gatewayUri -TimeoutSec 5
if ($initialGateway.state -ne "open") {
    throw "WhatsApp nao esta open; teste cancelado."
}
$numberBefore = [string]$initialGateway.number
$pidBefore = Get-GatewayPid
Assert-ManagedGateway -ProcessId $pidBefore
$heartbeatBefore = (Get-Item -LiteralPath $heartbeat).LastWriteTimeUtc
Write-Output "Gateway antes: PID=$pidBefore | WhatsApp=open"

try {
    Stop-Process -Id $pidBefore -Force -ErrorAction Stop
    Write-Output "Falha controlada aplicada ao gateway PID=$pidBefore."

    $deadline = [DateTime]::UtcNow.AddSeconds(130)
    $pidAfter = 0
    $finalGateway = $null
    do {
        $candidate = Get-GatewayPid
        if ($candidate -ne 0 -and $candidate -ne $pidBefore) {
            try {
                $health = Invoke-RestMethod -Uri $gatewayUri -TimeoutSec 5
                if ($health.state -eq "open") {
                    $pidAfter = $candidate
                    $finalGateway = $health
                    break
                }
            } catch {
                # Continua aguardando API e WhatsApp.
            }
        }
        Start-Sleep -Seconds 1
    } while ([DateTime]::UtcNow -lt $deadline)

    if ($pidAfter -eq 0 -or $null -eq $finalGateway) {
        throw "Watchdog nao recuperou gateway e WhatsApp em 130 segundos."
    }
    Assert-ManagedGateway -ProcessId $pidAfter

    $heartbeatAfter = (Get-Item -LiteralPath $heartbeat).LastWriteTimeUtc
    if ($heartbeatAfter -le $heartbeatBefore) {
        throw "Heartbeat nao avancou durante a recuperacao."
    }
    if (-not (Test-HttpReady -Uri $botUri)) {
        throw "Bot perdeu saude durante recuperacao do gateway."
    }
    if (-not (Test-Path -LiteralPath $credentials)) {
        throw "Credenciais de pareamento desapareceram."
    }
    if ([string]$finalGateway.number -ne $numberBefore) {
        throw "Numero pareado mudou durante recuperacao."
    }

    $testPassed = $true
    Write-Output (
        "RECUPERACAO_GATEWAY_OK | PID antes=$pidBefore" +
        " | PID depois=$pidAfter | WhatsApp=open | pareamento=preservado"
    )
} finally {
    if (-not $testPassed) {
        Restore-Gateway
    }
}
