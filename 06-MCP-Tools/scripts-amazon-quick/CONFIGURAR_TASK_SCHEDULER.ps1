# Configurar Task Scheduler para enviar relatorio toda sexta 17:00
$taskName = "Mob2Con - Relatorio Semanal"
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) { $pythonPath = "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe" }
$scriptPath = "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick\relatorio_semanal_auto.py"
$workDir = "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick"

# Remover tarefa antiga se existir
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Criar nova tarefa
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`"" -WorkingDirectory $workDir
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "17:00"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Envia relatorio semanal Mob2Con para Mariliana toda sexta 17h"

Write-Host ""
Write-Host "Tarefa criada com sucesso!" -ForegroundColor Green
Write-Host "  Nome: $taskName" -ForegroundColor Cyan
Write-Host "  Quando: Toda sexta-feira as 17:00" -ForegroundColor Cyan
Write-Host "  Acao: python relatorio_semanal_auto.py" -ForegroundColor Cyan
Write-Host ""
