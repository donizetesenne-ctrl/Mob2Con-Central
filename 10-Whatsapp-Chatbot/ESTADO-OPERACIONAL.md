# Estado operacional — chatbot Mob2Con

Data da validação: 17/09/2026, horário de Brasília.

## Arquitetura ativa

1. `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` inicia o valor
   `Mob2ConChatbotWatchdog` no logon do usuário.
2. `scripts/watchdog_servicos.py` permanece oculto e grava heartbeat a cada
   ciclo de 30 segundos.
3. O watchdog executa `SUPERVISOR-SERVICOS.ps1`, que testa HTTP e recupera
   somente processos cujo comando pertence ao bot ou gateway deste projeto.
4. Bot Python atende em `127.0.0.1:8000`; gateway Node atende em
   `127.0.0.1:8080`.
5. Sessões do atendimento ficam em `dados/chatbot.sqlite3`; pareamento do
   WhatsApp permanece em `gateway/sessao/`.
6. Os 60 manuais são indexados em `dados/manuais.sqlite3` com FTS5. O bot usa
   os trechos relevantes antes do fallback de IA.

O Task Scheduler foi descartado para os processos do chatbot nesta máquina.
O Bitdefender suspendeu processos iniciados por tarefas antes do primeiro
heartbeat. Sete definições antigas ficaram desativadas, preservadas apenas para
rollback e sem gatilho operacional.

## Evidências de validação

- Gate estático: `AUTOMATION_STATIC_OK | PowerShell=7 | Batch=6`.
- Testes Python direcionados: 10 testes, todos aprovados.
- Regressão conversacional: 122 aprovados, 0 falhas.
- Manuais: 60 documentos, 489 chunks, FTS5 ativo e `quick_check=ok`.
- Indexação incremental: 0 atualizados e 60 inalterados na segunda execução.
- Corpus limpo: zero Stonly/URL/caminho local e zero documento sem chunks.
- Recuperação validada em seis consultas operacionais; consulta aleatória e
  operadores FTS foram rejeitados.
- Compilação: `py_compile` Python e gate PowerShell aprovados.
- SQLite real: `SONDA_GRAVADA`, `SONDA_PERSISTIU`, `SONDA_REMOVIDA`.
- Recuperação do bot: PID 20440 encerrado; PID 31000 criado;
  `RECUPERACAO_BOT_OK`; sessão SQLite preservada.
- Recuperação do gateway: PID 20716 encerrado; PID 31004 criado;
  `RECUPERACAO_GATEWAY_OK`; WhatsApp voltou a `open`; número e pareamento
  preservados.
- O teste não enviou mensagens a contatos.

## Estado esperado no diagnóstico

`STATUS-AUTOMACAO.bat` deve terminar com `AUTOMACAO_OK` e mostrar:

- `HKCU Run | OK`;
- heartbeat com idade inferior a 120 segundos e `worker=0`;
- todas as tarefas antigas como `Disabled` ou ausentes;
- portas 8000 e 8080 em `LISTENING`;
- bot e gateway em HTTP 200;
- WhatsApp em `open`;
- persistência `BancoSQLite`;
- índice local com `manuais=60`, `chunks=489` e FTS5 ativo;
- arquivos SQLite e `creds.json` presentes.

## Operação

```powershell
.\STATUS-AUTOMACAO.bat
.\REINICIAR-BOT.bat
.\INICIAR-GATEWAY.bat
```

Logs principais: `watchdog.log`, `supervisor.log`, `bot.log` e `gateway.log`.
Nenhum desses arquivos deve ser versionado.

## Limites conhecidos

- Autostart ocorre no logon do usuário, não antes do login do Windows.
- IA continua inativa enquanto `LLM_API_KEY` estiver vazia; fluxo determinístico
  e busca extrativa nos 60 manuais continuam funcionando.
- O gateway usa Baileys, protocolo não oficial do WhatsApp; risco de bloqueio
  pela Meta permanece.
