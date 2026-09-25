[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Bot", "Gateway")]
    [string]$Servico
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$supervisor = Join-Path $root "SUPERVISOR-SERVICOS.ps1"
$gatewayIndex = Join-Path $root "gateway\index.js"
$port = if ($Servico -eq "Bot") { 8000 } else { 8080 }
$uri = "http://127.0.0.1:$port/health"

function Test-HttpReady {
    param([Parameter(Mandatory = $true)][string]$TargetUri)
    try {
        $response = Invoke-WebRequest `
            -UseBasicParsing `
            -Uri $TargetUri `
            -TimeoutSec 4
        return $response.StatusCode -ge 200 -and $response.StatusCode -lt 300
    } catch {
        return $false
    }
}

function Get-Listener {
    return Get-NetTCPConnection `
        -State Listen `
        -LocalPort $port `
        -ErrorAction SilentlyContinue |
        Select-Object -First 1
}

$listener = Get-Listener
$pidBefore = 0
if ($null -ne $listener) {
    $pidBefore = [int]$listener.OwningProcess
    $process = Get-CimInstance Win32_Process `
        -Filter "ProcessId = $pidBefore" `
        -ErrorAction Stop
    $managed = if ($Servico -eq "Bot") {
        $process.Name -in @("python.exe", "pythonw.exe") -and
        $process.CommandLine -like "*uvicorn bot.main:app*" -and
        $process.CommandLine -like "*--port 8000*"
    } else {
        $process.Name -ieq "node.exe" -and
        $process.CommandLine -like "*$gatewayIndex*"
    }

    if (-not $managed) {
        throw (
            "Porta $port pertence a processo nao gerenciado: " +
            "$($process.Name) PID=$pidBefore"
        )
    }

    Write-Output "Encerrando $Servico gerenciado: PID=$pidBefore"
    Stop-Process -Id $pidBefore -Force -ErrorAction Stop

    $deadline = [DateTime]::UtcNow.AddSeconds(20)
    do {
        if ($null -eq (Get-Listener)) {
            break
        }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $deadline)
    if ($null -ne (Get-Listener)) {
        throw "Porta $port nao foi liberada."
    }
}

& powershell.exe `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $supervisor
if ($LASTEXITCODE -ne 0) {
    throw "Supervisor retornou codigo $LASTEXITCODE."
}

$deadline = [DateTime]::UtcNow.AddSeconds(90)
do {
    if (Test-HttpReady -TargetUri $uri) {
        $listener = Get-Listener
        if ($null -ne $listener) {
            break
        }
    }
    Start-Sleep -Seconds 1
} while ([DateTime]::UtcNow -lt $deadline)

if ($null -eq $listener -or -not (Test-HttpReady -TargetUri $uri)) {
    throw "$Servico nao respondeu em ate 90 segundos."
}
$pidAfter = [int]$listener.OwningProcess
if ($pidBefore -ne 0 -and $pidAfter -eq $pidBefore) {
    throw "PID de $Servico nao mudou apos reinicio."
}

if ($Servico -eq "Gateway") {
    $health = $null
    $deadline = [DateTime]::UtcNow.AddSeconds(90)
    do {
        try {
            $health = Invoke-RestMethod -Uri $uri -TimeoutSec 5
            if ($health.state -eq "open") {
                break
            }
        } catch {
            # Continua aguardando reconexao.
        }
        Start-Sleep -Seconds 2
    } while ([DateTime]::UtcNow -lt $deadline)
    if ($null -eq $health -or $health.state -ne "open") {
        throw "Gateway voltou, mas WhatsApp nao reconectou."
    }
}

Write-Output (
    "REINICIO_OK | servico=$Servico | PID antes=$pidBefore" +
    " | PID depois=$pidAfter"
)
