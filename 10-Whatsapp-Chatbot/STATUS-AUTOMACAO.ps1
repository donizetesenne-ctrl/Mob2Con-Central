Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonw = Join-Path $root ".venv\Scripts\pythonw.exe"
$watchdogScript = Join-Path $root "scripts\watchdog_servicos.py"
$heartbeatPath = Join-Path $root "dados\watchdog-heartbeat.json"
$runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$runName = "Mob2ConChatbotWatchdog"
$expectedRun = '"' + $pythonw + '" "' + $watchdogScript + '"'
$scheduledTaskNames = @(
    "Mob2Con Chatbot - Watchdog",
    "Mob2Con Chatbot - Health Watchdog",
    "Mob2Con Chatbot - Bot Supervisor",
    "Mob2Con Chatbot - Gateway Supervisor",
    "Mob2Con Chatbot - Bot",
    "Mob2Con Chatbot - Gateway",
    "Mob2Con Chatbot - Gateway Service"
)
$healthy = $true
$botHealth = $null
$gatewayHealth = $null

Write-Output "=== AUTOSTART ==="
$runProperties = Get-ItemProperty -Path $runKey -ErrorAction SilentlyContinue
$runProperty = if ($null -ne $runProperties) {
    $runProperties.PSObject.Properties[$runName]
} else {
    $null
}
$runValue = if ($null -ne $runProperty) {
    [string]$runProperty.Value
} else {
    $null
}
if ($runValue -ceq $expectedRun) {
    Write-Output "HKCU Run | OK | nome=$runName"
} else {
    Write-Output "HKCU Run | AUSENTE OU DIVERGENTE"
    $healthy = $false
}

$heartbeat = Get-Item -LiteralPath $heartbeatPath -ErrorAction SilentlyContinue
$watchdogProcess = $null
if ($null -eq $heartbeat) {
    Write-Output "Watchdog | heartbeat AUSENTE"
    $healthy = $false
} else {
    try {
        $heartbeatData = Get-Content `
            -LiteralPath $heartbeatPath `
            -Raw | ConvertFrom-Json
        $watchdogPidValue = [int]$heartbeatData.pid
        $watchdogProcess = Get-CimInstance Win32_Process `
            -Filter "ProcessId = $watchdogPidValue" `
            -ErrorAction SilentlyContinue
        $ageSeconds = [math]::Round(
            ((Get-Date) - $heartbeat.LastWriteTime).TotalSeconds,
            1
        )
        Write-Output (
            "Watchdog | PID=$watchdogPidValue | heartbeat=" +
            "$($heartbeat.LastWriteTime) | idade=${ageSeconds}s" +
            " | worker=$($heartbeatData.worker_exit_code)"
        )
        if (
            $null -eq $watchdogProcess -or
            $watchdogProcess.Name -notin @("python.exe", "pythonw.exe") -or
            $watchdogProcess.CommandLine -notlike "*$watchdogScript*" -or
            $ageSeconds -gt 120
        ) {
            $healthy = $false
        }
    } catch {
        Write-Output "Watchdog | heartbeat invalido: $($_.Exception.Message)"
        $healthy = $false
    }
}

Write-Output "`n=== TAREFAS ANTIGAS ==="
foreach ($name in $scheduledTaskNames) {
    $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($null -eq $task) {
        Write-Output "$name | AUSENTE"
    } else {
        Write-Output "$name | $($task.State)"
        if ($task.State -ne "Disabled") {
            $healthy = $false
        }
    }
}

Write-Output "`n=== PORTAS ==="
foreach ($port in @(8000, 8080)) {
    $listener = Get-NetTCPConnection `
        -State Listen `
        -LocalPort $port `
        -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($null -eq $listener) {
        Write-Output "$port | SEM LISTENER"
        $healthy = $false
        continue
    }

    $process = Get-CimInstance Win32_Process `
        -Filter "ProcessId = $($listener.OwningProcess)" `
        -ErrorAction SilentlyContinue
    Write-Output (
        "$port | LISTENING | PID=$($listener.OwningProcess)" +
        " | processo=$($process.Name) | criado=$($process.CreationDate)"
    )
}

Write-Output "`n=== HEALTH ==="
try {
    $botHealth = Invoke-RestMethod `
        -Uri "http://127.0.0.1:8000/health" `
        -TimeoutSec 10
    Write-Output (
        "8000 | HTTP 200 | status=$($botHealth.status)" +
        " | gateway=$($botHealth.evolution_alcancavel)" +
        " | persistencia=$($botHealth.persistencia_sessoes)" +
        " | perguntas=$($botHealth.perguntas_pendentes)" +
        " | manuais=$($botHealth.manuais.documentos)" +
        " | chunks=$($botHealth.manuais.chunks)" +
        " | whatsapp=$($botHealth.whatsapp.instance.state)"
    )
} catch {
    Write-Output "8000 | INDISPONIVEL | $($_.Exception.Message)"
    $healthy = $false
}

try {
    $gatewayHealth = Invoke-RestMethod `
        -Uri "http://127.0.0.1:8080/health" `
        -TimeoutSec 10
    Write-Output (
        "8080 | HTTP 200 | status=$($gatewayHealth.status)" +
        " | instancia=$($gatewayHealth.instance)" +
        " | whatsapp=$($gatewayHealth.state)"
    )
} catch {
    Write-Output "8080 | INDISPONIVEL | $($_.Exception.Message)"
    $healthy = $false
}

if (
    $null -eq $botHealth -or
    $botHealth.status -ne "ok" -or
    $botHealth.evolution_alcancavel -ne $true -or
    $botHealth.persistencia_sessoes -ne "BancoSQLite" -or
    $botHealth.manuais.ativo -ne $true -or
    $botHealth.manuais.fts5 -ne $true -or
    $botHealth.manuais.documentos -ne 60 -or
    $botHealth.whatsapp.instance.state -ne "open"
) {
    $healthy = $false
}
if (
    $null -eq $gatewayHealth -or
    $gatewayHealth.status -ne 200 -or
    $gatewayHealth.state -ne "open"
) {
    $healthy = $false
}

Write-Output "`n=== PERSISTENCIA ==="
$database = Join-Path $root "dados\chatbot.sqlite3"
$credentials = Join-Path $root "gateway\sessao\creds.json"
foreach ($artifact in @(
    [PSCustomObject]@{ Name = "SQLite"; Path = $database },
    [PSCustomObject]@{ Name = "Pareamento"; Path = $credentials }
)) {
    $file = Get-Item -LiteralPath $artifact.Path -ErrorAction SilentlyContinue
    if ($null -eq $file -or $file.Length -le 0) {
        Write-Output "$($artifact.Name) | AUSENTE OU VAZIO"
        $healthy = $false
    } else {
        Write-Output (
            "$($artifact.Name) | OK | bytes=$($file.Length)" +
            " | alterado=$($file.LastWriteTime)"
        )
    }
}

Write-Output "`n=== RESULTADO ==="
if ($healthy) {
    Write-Output "AUTOMACAO_OK"
    exit 0
}
Write-Output "AUTOMACAO_COM_FALHA"
exit 1
