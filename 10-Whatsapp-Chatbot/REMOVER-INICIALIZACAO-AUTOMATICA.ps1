Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$runName = "Mob2ConChatbotWatchdog"
$taskNames = @(
    "Mob2Con Chatbot - Watchdog",
    "Mob2Con Chatbot - Health Watchdog",
    "Mob2Con Chatbot - Bot Supervisor",
    "Mob2Con Chatbot - Gateway Supervisor",
    "Mob2Con Chatbot - Bot",
    "Mob2Con Chatbot - Gateway",
    "Mob2Con Chatbot - Gateway Service"
)
$failures = New-Object System.Collections.Generic.List[string]

try {
    Remove-ItemProperty `
        -Path $runKey `
        -Name $runName `
        -ErrorAction SilentlyContinue
    Write-Output "Autostart HKCU Run removido: $runName"
} catch {
    $failures.Add("HKCU Run")
    Write-Warning "Falha ao remover HKCU Run: $($_.Exception.Message)"
}

foreach ($name in $taskNames) {
    $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($null -eq $task) {
        Write-Output "Tarefa ja ausente: $name"
        continue
    }

    try {
        if ($task.State -eq "Running") {
            Stop-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
        }
        Disable-ScheduledTask -TaskName $name -ErrorAction Stop | Out-Null
        Write-Output "Tarefa desativada: $name"
    } catch {
        $failures.Add($name)
        Write-Warning "Falha ao desativar '$name': $($_.Exception.Message)"
    }
}

Write-Output (
    "Automacao de proximo logon removida. Dados, logs, .env, banco e " +
    "pareamento foram preservados. Processos atuais nao foram encerrados."
)
if ($failures.Count -gt 0) {
    throw "Falha em $($failures.Count) item(ns) da remocao."
}
