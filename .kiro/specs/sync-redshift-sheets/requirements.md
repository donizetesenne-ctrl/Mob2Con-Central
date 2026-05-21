# Spec: Sincronização Redshift → Google Sheets

## Objetivo
Criar pipeline de dados que extrai tabelas do Amazon Redshift e sincroniza com Google Sheets para consumo dos dashboards.

## Requisitos Funcionais

### REQ-1: Conexão Redshift
- Conectar via psycopg2 usando credenciais de `redshift_config.json`
- Suportar múltiplos schemas e tabelas
- Timeout de conexão: 30 segundos
- Retry automático: 3 tentativas com backoff exponencial

### REQ-2: Extração de Dados
- Executar queries SQL parametrizadas
- Suportar filtros por data (incremental)
- Limitar resultado a 500.000 linhas por query
- Converter tipos de dados (timestamp → string, decimal → float)

### REQ-3: Escrita no Google Sheets
- Autenticar via service account (gspread + google-auth)
- Mapear tabelas para abas conforme `spreadsheets_config.json`
- Limpar aba antes de escrever (clear + update)
- Formatar cabeçalhos em negrito

### REQ-4: Agendamento
- Executar via Task Scheduler do Windows (diário 06:00)
- Log de execução em `logs/sync_YYYY-MM-DD.log`
- Notificação por email em caso de falha

### REQ-5: Monitoramento
- Registrar: linhas extraídas, tempo de execução, erros
- Dashboard de saúde no Google Sheets (aba _Status)

## Requisitos Não-Funcionais
- Execução total < 5 minutos
- Sem dependência de interface gráfica
- Compatível com .venv Python 3.10+
