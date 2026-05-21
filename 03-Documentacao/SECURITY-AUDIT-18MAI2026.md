# 🔒 AUDITORIA DE SEGURANÇA — Mob2Con-Central

**Data:** 18 de Maio de 2026  
**Agente:** security_validator  
**Workspace:** `c:\Users\Donizete Senne\Desktop\Mob2Con-Central`  
**Escopo:** Credenciais, código Python, configurações, scripts .bat/.ps1, MCP configs

---

## 📊 RESUMO EXECUTIVO

| Severidade | Quantidade | Descrição |
|:---:|:---:|---|
| 🔴 CRÍTICO | 4 | Credenciais expostas em texto plano |
| 🟡 ALERTA | 5 | Práticas inseguras que requerem atenção |
| 🟢 OK | 6 | Itens em conformidade |

**Risco Geral: 🔴 ALTO** — Credenciais de produção expostas em arquivos versionáveis.

---

## 1. CREDENCIAIS E SEGREDOS

### 🔴 CRÍTICO — Senha Redshift em texto plano

**Arquivo:** `redshift_config.json`  
**Problema:** Senha do cluster Redshift armazenada em texto plano no arquivo de configuração.

```json
{
  "host": "[REDACTED].us-west-2.redshift.amazonaws.com",
  "port": 5439,
  "database": "rg_bi",
  "user": "[REDACTED]",
  "password": "[REDACTED]"
}
```

**Impacto:** Qualquer pessoa com acesso ao workspace pode ler credenciais de produção do Redshift.  
**Recomendação:** Usar variáveis de ambiente ou AWS Secrets Manager. Remover senha do arquivo e usar `os.environ['REDSHIFT_PASSWORD']`.

---

### 🔴 CRÍTICO — API Key NVIDIA NIM exposta

**Arquivo:** `06-MCP-Tools/nvidia-nim/config.json`  
**Problema:** Chave de API NVIDIA (`nvapi-...`) armazenada em texto plano.

```json
{
  "nvidia_api_key": "[REDACTED]"
}
```

**Impacto:** Uso não autorizado da API NVIDIA com custos potenciais.  
**Atenuante:** O `.gitignore` local lista `config.json`, mas o arquivo existe no workspace e pode ser copiado inadvertidamente.  
**Recomendação:** Migrar para variável de ambiente `NVIDIA_API_KEY`.

---

### 🔴 CRÍTICO — OAuth Client ID hardcoded em 5 scripts Python

**Arquivos afetados:**
- `sync_redshift_multi_sheets.py`
- `sync_redshift_to_sheets.py`
- `sync_redshift_to_sheets_fast.py`
- `sync_redshift_daily.py`
- `consolidar_planilhas.py`

**Problema:** O `client_id` do Google OAuth está hardcoded diretamente no código-fonte:

```python
client_id='[REDACTED].apps.googleusercontent.com'
```

**Impacto:** Exposição do identificador OAuth. Embora o `client_id` sozinho não permita acesso, combinado com o `client_secret` (carregado do token file) facilita ataques de phishing OAuth.  
**Recomendação:** Carregar `client_id` do arquivo de configuração ou variável de ambiente, nunca hardcoded.

---

### 🔴 CRÍTICO — Ausência de .gitignore na raiz do workspace

**Problema:** Não existe arquivo `.gitignore` na raiz do workspace `Mob2Con-Central/`.

**Arquivos sensíveis que DEVEM ser ignorados:**
- `redshift_config.json` (senha Redshift)
- `06-MCP-Tools/nvidia-nim/config.json` (API key NVIDIA)
- `.clasp.json` (scriptId do Apps Script)
- `sync_log.txt` (pode conter dados sensíveis em mensagens de erro)
- `dashboard_dados.json` (dados de produção)
- `*.pyc`, `__pycache__/`
- `.venv/`

**Nota:** Existem `.gitignore` em subpastas (`nvidia-nim/`, `agent-manager-for-q-cli/`) mas NÃO na raiz.  
**Recomendação:** Criar `.gitignore` na raiz imediatamente.

---

## 2. CÓDIGO PYTHON

### 🟡 ALERTA — SQL com f-strings (risco baixo de injection)

**Arquivos afetados:** Todos os scripts de sync (`sync_redshift_*.py`, `list_dw_tables.py`)

**Padrão encontrado:**
```python
cur.execute(f'SELECT COUNT(*) FROM dw.{table_name}')
cur.execute(f'SELECT * FROM dw.{table_name} LIMIT {limit}')
cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
```

**Análise de risco:** BAIXO — Os valores de `table_name` vêm de `pg_tables` (sistema) e não de input do usuário. Não há risco real de SQL injection neste contexto.  
**Recomendação:** Mesmo assim, usar `sql.Identifier()` do psycopg2 para nomes de tabelas é uma boa prática defensiva:
```python
from psycopg2 import sql
cur.execute(sql.SQL("SELECT COUNT(*) FROM dw.{}").format(sql.Identifier(table_name)))
```

---

### 🟢 OK — Nenhum uso de eval() ou exec()

Nenhuma ocorrência de `eval()` ou `exec()` encontrada em nenhum script Python do workspace.

---

### 🟢 OK — Conexões Redshift usam SSL

Todos os scripts Python usam `sslmode='require'` na conexão:
```python
conn = psycopg2.connect(..., sslmode='require', connect_timeout=15)
```

**Arquivos verificados:** `sync_redshift_multi_sheets.py`, `sync_redshift_to_sheets.py`, `sync_redshift_to_sheets_fast.py`, `sync_redshift_daily.py`, `redshift_query.py`, `list_dw_tables.py`, `extrai_dashboard.py`

---

### 🟡 ALERTA — Caminho absoluto de token OAuth hardcoded

**Arquivos afetados:** `sync_redshift_multi_sheets.py`, `sync_redshift_to_sheets.py`, `sync_redshift_to_sheets_fast.py`, `sync_redshift_daily.py`, `consolidar_planilhas.py`

```python
token_path = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"
```

**Problema:** Caminho absoluto com nome de usuário hardcoded. Não funciona em outro ambiente.  
**Recomendação:** Usar `Path.home()` ou variável de ambiente:
```python
token_path = Path.home() / ".aws/amazonq/universal-control/credentials/google-oauth-token.json"
```

---

### 🟢 OK — extrai_dashboard.py usa boas práticas

O script `extrai_dashboard.py` demonstra boas práticas:
- Queries SQL são strings estáticas (sem interpolação de input do usuário)
- Usa `sslmode='require'`
- Logging estruturado
- Tratamento de erros com rollback
- Busca credenciais Google via Service Account (não hardcoded)

---

## 3. CONFIGURAÇÕES

### 🟡 ALERTA — redshift_config.json sem campo SSL explícito

**Arquivo:** `redshift_config.json`

O arquivo de configuração não inclui campo `sslmode`. O SSL é aplicado apenas no código Python.

**Recomendação:** Adicionar `"sslmode": "require"` ao JSON para documentar a exigência:
```json
{
  "host": "...",
  "port": 5439,
  "database": "rg_bi",
  "user": "...",
  "password": "...",
  "sslmode": "require"
}
```

---

### 🟢 OK — spreadsheets_config.json sem dados sensíveis

O arquivo contém apenas IDs de planilhas Google (públicos por natureza) e configurações de sync. Nenhuma credencial exposta.

---

### 🟡 ALERTA — .clasp.json expõe scriptId do Apps Script

**Arquivo:** `.clasp.json`

```json
{
  "scriptId": "[REDACTED]"
}
```

**Risco:** Baixo. O `scriptId` sozinho não permite acesso, mas facilita identificação do projeto.  
**Recomendação:** Incluir no `.gitignore` se o workspace for versionado.

---

## 4. SCRIPTS .bat/.ps1

### 🟢 OK — Nenhum download de URL não-HTTPS

Nenhum script `.bat` ou `.ps1` faz download de URLs HTTP inseguras. Não foram encontrados `Invoke-WebRequest`, `curl`, `wget` ou `DownloadFile`.

---

### 🟢 OK — Scripts .bat executam apenas código local

Os scripts batch (`INSTALAR.bat`, `agendar_atualizacao.bat`, `executar_sync_diario.bat`) apenas:
- Chamam scripts Python locais
- Executam PowerShell local
- Criam logs locais

Nenhum executa código remoto sem verificação.

---

### 🟡 ALERTA — Instalar-Mob2Con.ps1 usa -ExecutionPolicy Bypass

**Arquivo:** `INSTALAR.bat`

```batch
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Instalar-Mob2Con.ps1"
```

**Análise:** Necessário para instalação, mas desabilita proteções do PowerShell.  
**Recomendação:** Documentar que o usuário deve verificar o conteúdo do script antes de executar. Considerar assinar digitalmente o script.

---

## 5. MCP CONFIGS

### 🟢 OK — .kiro/settings/mcp.json sem credenciais

O arquivo MCP do workspace contém apenas caminhos de scripts e configurações de servidor. Nenhuma credencial exposta.

---

### 🟡 ALERTA — quickwork-mcp-central.json referencia ucm-secrets.json

**Arquivo:** `06-MCP-Tools/quickwork-mcp-central.json`

```json
"UCM_CONFIG_PATH": "[REDACTED]\\.aws\\amazonq\\universal-control\\ucm-secrets.json"
```

**Análise:** O caminho para o arquivo de segredos está documentado no JSON (não o conteúdo). Risco baixo, mas revela a localização do vault de segredos.  
**Recomendação:** Usar variável de ambiente em vez de caminho hardcoded.

---

## 📋 PLANO DE REMEDIAÇÃO (Priorizado)

### Prioridade 1 — Imediato (hoje)

| # | Ação | Esforço |
|---|------|---------|
| 1 | Criar `.gitignore` na raiz com `redshift_config.json`, `config.json`, `.env`, `*.pyc`, `.venv/`, `sync_log.txt`, `dashboard_dados.json` | 5 min |
| 2 | Rotacionar senha do Redshift (trocar no AWS Console) | 10 min |
| 3 | Rotacionar API key NVIDIA NIM | 5 min |

### Prioridade 2 — Esta semana

| # | Ação | Esforço |
|---|------|---------|
| 4 | Migrar senha Redshift para variável de ambiente `REDSHIFT_PASSWORD` | 30 min |
| 5 | Migrar NVIDIA API key para variável de ambiente `NVIDIA_API_KEY` | 15 min |
| 6 | Remover `client_id` hardcoded dos scripts Python (carregar de config) | 30 min |
| 7 | Substituir caminhos absolutos por `Path.home()` | 20 min |

### Prioridade 3 — Próxima sprint

| # | Ação | Esforço |
|---|------|---------|
| 8 | Usar `psycopg2.sql.Identifier()` para nomes de tabelas | 1h |
| 9 | Implementar AWS Secrets Manager para credenciais Redshift | 2h |
| 10 | Assinar digitalmente scripts PowerShell | 1h |

---

## 🔍 ARQUIVOS ANALISADOS

| Categoria | Arquivos |
|-----------|----------|
| Python (.py) | 10 scripts na raiz + subpastas |
| Batch (.bat) | 4 scripts |
| PowerShell (.ps1) | 3 scripts |
| JSON configs | 5 arquivos |
| JavaScript (.js) | 2 arquivos |
| .gitignore | 3 (nenhum na raiz) |

---

## ✅ PONTOS POSITIVOS

1. **SSL obrigatório** — Todas as conexões Redshift usam `sslmode='require'`
2. **Sem eval/exec** — Nenhum uso de funções perigosas de execução dinâmica
3. **Sem downloads inseguros** — Scripts não baixam de URLs HTTP
4. **Token OAuth separado** — O token fica fora do workspace (em `.aws/`)
5. **Service Account no extrai_dashboard.py** — Melhor prática de autenticação Google
6. **MCP configs limpos** — Sem credenciais nos arquivos de configuração MCP

---

*Relatório gerado automaticamente pelo agente `security_validator` em 18/05/2026.*
