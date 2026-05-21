@echo off
REM ══════════════════════════════════════════════════════════════════
REM  AGENDAMENTO - PIPELINE DASHBOARD MOB2CON
REM  Executa extrai_dashboard.py todo dia às 07:00
REM ══════════════════════════════════════════════════════════════════
REM
REM  COMO ADICIONAR NO WINDOWS TASK SCHEDULER:
REM  ───────────────────────────────────────────
REM  1. Abrir "Agendador de Tarefas" (taskschd.msc)
REM  2. Clique em "Criar Tarefa Básica..." no painel direito
REM  3. Nome: "Mob2Con - Atualização Dashboard"
REM  4. Descrição: "Pipeline diário Redshift → Sheets → JSON"
REM  5. Disparador: Diariamente, às 07:00
REM  6. Ação: "Iniciar um programa"
REM     - Programa: C:\Users\Donizete Senne\Desktop\Mob2Con-Central\agendar_atualizacao.bat
REM     - Iniciar em: C:\Users\Donizete Senne\Desktop\Mob2Con-Central
REM  7. Marcar "Executar estando o usuário conectado ou não"
REM  8. Marcar "Executar com privilégios mais altos" (se necessário)
REM
REM  OU via linha de comando (cmd como Admin):
REM  schtasks /create /tn "Mob2Con_Dashboard" /tr "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\agendar_atualizacao.bat" /sc daily /st 07:00 /ru "Donizete Senne" /rl highest
REM
REM  PARA TESTAR MANUALMENTE:
REM  - Basta executar este .bat clicando duas vezes
REM  - Verificar log em: logs\dashboard.log
REM
REM ══════════════════════════════════════════════════════════════════

REM Define o diretório de trabalho
cd /d "C:\Users\Donizete Senne\Desktop\Mob2Con-Central"

REM Cria pasta de logs se não existir
if not exist "logs" mkdir logs

REM Registra início no log
echo. >> logs\dashboard.log
echo ══════════════════════════════════════════════════════════════ >> logs\dashboard.log
echo [%date% %time%] INÍCIO - Execução agendada do Pipeline >> logs\dashboard.log
echo ══════════════════════════════════════════════════════════════ >> logs\dashboard.log

REM Executa o script Python
REM (Ajuste o caminho do Python se estiver em um virtualenv)
python extrai_dashboard.py >> logs\dashboard.log 2>&1

REM Verifica se houve erro
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ❌ ERRO - Pipeline finalizado com código %ERRORLEVEL% >> logs\dashboard.log
) else (
    echo [%date% %time%] ✅ SUCESSO - Pipeline concluído >> logs\dashboard.log
)

echo ══════════════════════════════════════════════════════════════ >> logs\dashboard.log
echo. >> logs\dashboard.log

REM Pausa se executado manualmente (para ver resultado)
REM Remova a linha abaixo se rodar apenas pelo Task Scheduler
if "%1"=="" pause
