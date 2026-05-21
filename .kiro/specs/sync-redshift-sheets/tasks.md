# Tasks: Sincronização Redshift → Google Sheets

## Task 1: Configuração do ambiente
- [ ] Verificar `requirements_dashboard.txt` (psycopg2, gspread, pandas, google-auth)
- [ ] Validar `redshift_config.json` (conexão funcional)
- [ ] Validar service account Google (permissões no Sheets)
- [ ] Criar `spreadsheets_config.json` se não existir

## Task 2: Script de extração
- [ ] Criar/atualizar `sync_redshift_to_sheets.py`
- [ ] Implementar conexão com retry e timeout
- [ ] Implementar query parametrizada por data
- [ ] Converter tipos de dados para compatibilidade Sheets
- [ ] Tratamento de erros com logging

## Task 3: Script multi-planilha
- [ ] Criar/atualizar `sync_redshift_multi_sheets.py`
- [ ] Implementar loop sobre mappings do config
- [ ] Rate limiting (sleep entre requests)
- [ ] Execução paralela com ThreadPool (max 3)

## Task 4: Logging e monitoramento
- [ ] Criar pasta `logs/` se não existir
- [ ] Implementar log rotativo (1 arquivo por dia)
- [ ] Criar aba _Status no Sheets com última execução
- [ ] Registrar: timestamp, linhas, duração, status

## Task 5: Agendamento Windows
- [ ] Criar `sync_daily.bat` para Task Scheduler
- [ ] Configurar execução diária 06:00
- [ ] Testar execução manual
- [ ] Documentar no README
