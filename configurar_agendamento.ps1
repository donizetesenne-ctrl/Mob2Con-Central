# Script para configurar agendamento automático no Task Scheduler
# Executa a sincronização Redshift → Google Sheets todos os dias às 06:00

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Configurando Agendamento Automático" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$taskName = "Sync Redshift to Google Sheets"
$scriptPath = "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\executar_sync_diario.bat"
$workingDir = "C:\Users\Donizete Senne\Desktop\Mob2Con-Central"

# Verificar se a tarefa já existe
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "⚠️  Tarefa '$taskName' já existe. Removendo..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Criar ação (executar o script batch)
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory $workingDir

# Criar trigger (todos os dias às 06:00)
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00AM"

# Criar configurações
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

# Criar principal (executar com usuário atual)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Registrar tarefa
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Sincronização automática diária dos dados do Redshift para Google Sheets (Dimensões, Fatos e Lookup)"

Write-Host ""
Write-Host "✅ Agendamento configurado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "Detalhes:" -ForegroundColor Cyan
Write-Host "  Nome da Tarefa: $taskName"
Write-Host "  Horário: Todos os dias às 06:00"
Write-Host "  Script: $scriptPath"
Write-Host ""
Write-Host "Para gerenciar o agendamento:" -ForegroundColor Yellow
Write-Host "  1. Abra o 'Agendador de Tarefas' do Windows"
Write-Host "  2. Procure por '$taskName'"
Write-Host "  3. Clique com botão direito para editar, desabilitar ou executar manualmente"
Write-Host ""
Write-Host "Ou use os comandos PowerShell:" -ForegroundColor Yellow
Write-Host "  - Executar agora: Start-ScheduledTask -TaskName '$taskName'"
Write-Host "  - Desabilitar: Disable-ScheduledTask -TaskName '$taskName'"
Write-Host "  - Habilitar: Enable-ScheduledTask -TaskName '$taskName'"
Write-Host "  - Remover: Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Perguntar se quer executar teste agora
Write-Host ""
$response = Read-Host "Deseja executar um teste agora? (S/N)"
if ($response -eq "S" -or $response -eq "s") {
    Write-Host ""
    Write-Host "Executando teste..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $taskName
    Write-Host "✅ Teste iniciado! Verifique o arquivo 'sync_log.txt' para acompanhar o progresso." -ForegroundColor Green
}

Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
