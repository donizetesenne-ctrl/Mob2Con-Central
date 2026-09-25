[CmdletBinding()]
param(
    [ValidateRange(10, 120)]
    [int]$StartupTimeoutSeconds = 45
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
$node = "C:\Program Files\nodejs\node.exe"
$envFile = Join-Path $root ".env"
$gatewayDir = Join-Path $root "gateway"
$gatewayIndex = Join-Path $gatewayDir "index.js"
$logPath = Join-Path $root "supervisor.log"
$botStdout = Join-Path $root "bot-service.stdout.log"
$botStderr = Join-Path $root "bot-service.stderr.log"
$gatewayStdout = Join-Path $root "gateway-service.stdout.log"
$gatewayStderr = Join-Path $root "gateway-service.stderr.log"
$taskkill = Join-Path $env:SystemRoot "System32\taskkill.exe"
$mutex = New-Object System.Threading.Mutex(
    $false,
    "Local\Mob2ConChatbotHealthWatchdog"
)
$lockTaken = $false

function Write-SupervisorLog {
    param([Parameter(Mandatory = $true)][string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -LiteralPath $logPath -Value "$timestamp $Message" -Encoding UTF8
}

function Test-HttpReady {
    param(
        [Parameter(Mandatory = $true)][string]$Uri,
        [int]$TimeoutSeconds = 4
    )
    try {
        $response = Invoke-WebRequest `
            -UseBasicParsing `
            -Uri $Uri `
            -TimeoutSec $TimeoutSeconds
        return $response.StatusCode -ge 200 -and $response.StatusCode -lt 300
    } catch {
        return $false
    }
}

function Wait-HttpReady {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Uri
    )
    $deadline = [DateTime]::UtcNow.AddSeconds($StartupTimeoutSeconds)
    do {
        if (Test-HttpReady -Uri $Uri) {
            Write-SupervisorLog "$Name iniciado e respondeu HTTP."
            return
        }
        Start-Sleep -Seconds 1
    } while ([DateTime]::UtcNow -lt $deadline)

    throw "$Name nao respondeu em $StartupTimeoutSeconds segundos."
}

function Get-ServiceProcesses {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("bot", "gateway")]
        [string]$Service
    )

    $all = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue
    if ($Service -eq "gateway") {
        return @($all | Where-Object {
            $_.Name -ieq "node.exe" -and
            $_.CommandLine -like "*$gatewayIndex*"
        })
    }

    return @($all | Where-Object {
        $_.Name -in @("python.exe", "pythonw.exe") -and
        $_.CommandLine -like "*uvicorn bot.main:app*" -and
        $_.CommandLine -like "*--port 8000*"
    })
}

function Stop-ServiceProcesses {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("bot", "gateway")]
        [string]$Service
    )

    $processes = @(Get-ServiceProcesses -Service $Service)
    if ($processes.Count -eq 0) {
        return
    }

    $ids = @($processes | ForEach-Object { [int]$_.ProcessId })
    $roots = @($processes | Where-Object {
        [int]$_.ParentProcessId -notin $ids
    })
    if ($roots.Count -eq 0) {
        $roots = $processes
    }

    foreach ($process in $roots) {
        Write-SupervisorLog (
            "Encerrando $Service PID=$($process.ProcessId), comando confirmado."
        )
        try {
            Stop-Process `
                -Id $process.ProcessId `
                -Force `
                -ErrorAction Stop
        } catch {
            Write-SupervisorLog (
                "Stop-Process falhou para PID=$($process.ProcessId): " +
                $_.Exception.Message
            )
        }
    }

    $deadline = [DateTime]::UtcNow.AddSeconds(8)
    do {
        if (@(Get-ServiceProcesses -Service $Service).Count -eq 0) {
            return
        }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $deadline)

    foreach ($process in @(Get-ServiceProcesses -Service $Service)) {
        Write-SupervisorLog (
            "Aplicando taskkill restrito ao $Service PID=$($process.ProcessId)."
        )
        & $taskkill /PID $process.ProcessId /T /F | Out-Null
    }

    $deadline = [DateTime]::UtcNow.AddSeconds(10)
    do {
        if (@(Get-ServiceProcesses -Service $Service).Count -eq 0) {
            return
        }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $deadline)

    $remaining = @(
        Get-ServiceProcesses -Service $Service |
            ForEach-Object { $_.ProcessId }
    ) -join ","
    throw "Processos antigos de $Service nao encerraram: $remaining"
}

function Start-Gateway {
    Stop-ServiceProcesses -Service "gateway"
    $arguments = '--env-file="' + $envFile + '" "' + $gatewayIndex + '"'
    $process = Start-Process `
        -FilePath $node `
        -ArgumentList $arguments `
        -WorkingDirectory $gatewayDir `
        -WindowStyle Hidden `
        -RedirectStandardOutput $gatewayStdout `
        -RedirectStandardError $gatewayStderr `
        -PassThru
    Write-SupervisorLog "Gateway criado com PID=$($process.Id)."
    Wait-HttpReady -Name "Gateway" -Uri "http://127.0.0.1:8080/health"
}

function Start-Bot {
    Stop-ServiceProcesses -Service "bot"
    $process = Start-Process `
        -FilePath $python `
        -ArgumentList "-m uvicorn bot.main:app --host 127.0.0.1 --port 8000" `
        -WorkingDirectory $root `
        -WindowStyle Hidden `
        -RedirectStandardOutput $botStdout `
        -RedirectStandardError $botStderr `
        -PassThru
    Write-SupervisorLog "Bot criado com PID=$($process.Id)."
    Wait-HttpReady -Name "Bot" -Uri "http://127.0.0.1:8000/health"
}

try {
    $lockTaken = $mutex.WaitOne(0)
    if (-not $lockTaken) {
        exit 0
    }

    foreach ($required in @($python, $node, $envFile, $gatewayIndex)) {
        if (-not (Test-Path -LiteralPath $required)) {
            throw "Arquivo obrigatorio ausente: $required"
        }
    }

    if (-not (Test-HttpReady -Uri "http://127.0.0.1:8080/health")) {
        Write-SupervisorLog "Gateway indisponivel; iniciando recuperacao."
        Start-Gateway
    }

    if (-not (Test-HttpReady -Uri "http://127.0.0.1:8000/health")) {
        Write-SupervisorLog "Bot indisponivel; iniciando recuperacao."
        Start-Bot
    }

    exit 0
} catch {
    Write-SupervisorLog "ERRO: $($_.Exception.Message)"
    exit 1
} finally {
    if ($lockTaken) {
        $mutex.ReleaseMutex()
    }
    $mutex.Dispose()
}
