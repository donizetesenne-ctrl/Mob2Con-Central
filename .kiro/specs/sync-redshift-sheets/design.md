# Design: Sincronização Redshift → Google Sheets

## Arquitetura

```
[Redshift] → psycopg2 → [DataFrame Pandas] → gspread → [Google Sheets]
                                ↓
                         [Log local + _Status]
```

## Componentes

### sync_redshift_to_sheets.py (principal)
- Lê `redshift_config.json` para conexão
- Lê `spreadsheets_config.json` para mapeamento tabela→aba
- Executa queries e converte para DataFrame
- Escreve no Sheets via gspread

### sync_redshift_multi_sheets.py (multi-planilha)
- Orquestra múltiplas sincronizações em paralelo
- Gerencia rate limiting da API Google (100 req/100s)

### Configs
```json
// redshift_config.json
{
  "host": "cluster.redshift.amazonaws.com",
  "port": 5439,
  "database": "analytics",
  "user": "readonly_user",
  "password": "***"
}

// spreadsheets_config.json
{
  "mappings": [
    {
      "query": "SELECT * FROM schema.tabela WHERE dt >= '{date}'",
      "spreadsheet_id": "1abc...",
      "sheet_name": "Dados",
      "clear_before_write": true
    }
  ]
}
```

## MCPs Utilizados
- **universal-control**: Verificar/criar planilhas no Drive
- **filesystem**: Ler/escrever configs e logs
- **shell-command**: Executar scripts Python

## Fluxo
1. Ler configs → 2. Conectar Redshift → 3. Executar queries → 4. Converter dados → 5. Escrever Sheets → 6. Registrar log
