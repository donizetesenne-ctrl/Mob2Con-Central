[CmdletBinding()]
param(
    [switch]$NoStart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
$pythonw = Join-Path $root ".venv\Scripts\pythonw.exe"
$node = "C:\Program Files\nodejs\node.exe"
$envFile = Join-Path $root ".env"
$gatewayModules = Join-Path $root "gateway\node_modules"
$gatewayIndex = Join-Path $root "gateway\index.js"
$supervisor = Join-Path $root "SUPERVISOR-SERVICOS.ps1"
$watchdogScript = Join-Path $root "scripts\watchdog_servicos.py"
$heartbeat = Join-Path $root "dados\watchdog-heartbeat.json"
$runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$runName = "Mob2ConChatbotWatchdog"
$runCommand = '"' + $pythonw + '" "' + $watchdogScript + '"'
$scheduledTaskNames = @(
    "Mob2Con Chatbot - Watchdog",
    "Mob2Con Chatbot - Health Watchdog",
    "Mob2Con Chatbot - Bot Supervisor",
    "Mob2Con Chatbot - Gateway Supervisor",
    "Mob2Con Chatbot - Bot",
    "Mob2Con Chatbot - Gateway",
    "Mob2Con Chatbot - Gateway Service"
)

foreach ($required in @(
    $python,
    $pythonw,
    $node,
    $envFile,
    $gatewayModules,
    $gatewayIndex,
    $supervisor,
    $watchdogScript
)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Arquivo obrigatorio ausente: $required"
    }
}

if (-not (Test-Path -LiteralPath $runKey)) {
    New-Item -Path $runKey -Force | Out-Null
}
function Get-RunValue {
    $properties = Get-ItemProperty -Path $runKey -ErrorAction SilentlyContinue
    if ($null -eq $properties) {
        return $null
    }
    $property = $properties.PSObject.Properties[$runName]
    if ($null -eq $property) {
        return $null
    }
    return [string]$property.Value
}

$currentRun = Get-RunValue
if ($currentRun -cne $runCommand) {
    Set-ItemProperty `
        -Path $runKey `
        -Name $runName `
        -Value $runCommand `
        -Type String
    Write-Output "Autostart HKCU Run configurado: $runName"
} else {
    Write-Output "Autostart HKCU Run preservado: $runName"
}

foreach ($name in $scheduledTaskNames) {
    $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($null -eq $task) {
        Write-Output "Tarefa antiga ausente: $name"
        continue
    }

    if ($task.State -eq "Running") {
        Stop-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
    }
    $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($null -ne $task -and $task.State -ne "Disabled") {
        Disable-ScheduledTask -TaskName $name -ErrorAction Stop | Out-Null
    }
    Write-Output "Tarefa antiga desativada: $name"
}

function Get-WatchdogState {
    $file = Get-Item -LiteralPath $heartbeat -ErrorAction SilentlyContinue
    if ($null -eq $file) {
        return $null
    }

    try {
        $data = Get-Content -LiteralPath $heartbeat -Raw | ConvertFrom-Json
        $watchdogPidValue = [int]$data.pid
    } catch {
        return $null
    }

    $process = Get-CimInstance Win32_Process `
        -Filter "ProcessId = $watchdogPidValue" `
        -ErrorAction SilentlyContinue
    $matches = (
        $null -ne $process -and
        $process.Name -in @("python.exe", "pythonw.exe") -and
        $process.CommandLine -like "*$watchdogScript*"
    )

    return [PSCustomObject]@{
        Pid = $watchdogPidValue
        Process = $process
        Matches = $matches
        AgeSeconds = ((Get-Date) - $file.LastWriteTime).TotalSeconds
    }
}

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

function Wait-Operational {
    param([int]$TimeoutSeconds = 90)

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        $state = Get-WatchdogState
        if (
            $null -ne $state -and
            $state.Matches -and
            $state.AgeSeconds -le 120 -and
            (Test-HttpReady -Uri "http://127.0.0.1:8080/health") -and
            (Test-HttpReady -Uri "http://127.0.0.1:8000/health")
        ) {
            return $state
        }
        Start-Sleep -Seconds 1
    } while ([DateTime]::UtcNow -lt $deadline)

    throw "Watchdog, gateway ou bot nao ficaram operacionais em $TimeoutSeconds segundos."
}

if (-not $NoStart) {
    $state = Get-WatchdogState
    $needsStart = (
        $null -eq $state -or
        -not $state.Matches -or
        $state.AgeSeconds -gt 120
    )

    if ($needsStart) {
        if (
            $null -ne $state -and
            $state.Matches -and
            $state.AgeSeconds -gt 120
        ) {
            Stop-Process -Id $state.Pid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
        }

        Start-Process `
            -FilePath $pythonw `
            -ArgumentList ('"' + $watchdogScript + '"') `
            -WorkingDirectory $root `
            -WindowStyle Hidden | Out-Null
        Write-Output "Watchdog iniciado fora do Agendador."
    } else {
        Write-Output "Watchdog ja ativo: PID=$($state.Pid)"
    }

    $state = Wait-Operational
    Write-Output "Watchdog operacional: PID=$($state.Pid)"
}

$finalRun = Get-ItemPropertyValue `
    -Path $runKey `
    -Name $runName `
    -ErrorAction Stop
$finalState = Get-WatchdogState
[PSCustomObject]@{
    Startup = "HKCU Run"
    RegistryName = $runName
    RegistryCommandOk = ($finalRun -ceq $runCommand)
    WatchdogPid = if ($null -ne $finalState) { $finalState.Pid } else { 0 }
    HeartbeatAgeSeconds = if ($null -ne $finalState) {
        [math]::Round($finalState.AgeSeconds, 1)
    } else {
        -1
    }
    ScheduledTasksEnabled = @(
        $scheduledTaskNames |
            ForEach-Object {
                Get-ScheduledTask -TaskName $_ -ErrorAction SilentlyContinue
            } |
            Where-Object { $null -ne $_ -and $_.State -ne "Disabled" }
    ).Count
}
