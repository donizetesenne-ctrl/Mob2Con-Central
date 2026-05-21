# 🔄 Sincronização Automática Redshift → Google Sheets

Sistema de sincronização diária dos dados do Amazon Redshift para Google Sheets, organizado em 3 planilhas por categoria.

## 📊 Planilhas Criadas

### 1. 📊 Redshift - Dimensões (23 tabelas)
**URL:** https://docs.google.com/spreadsheets/d/1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q

Contém todas as tabelas de dimensão (dim_*):
- dim_agencia, dim_loja, dim_rede, dim_fornecedor
- dim_produto, dim_tempo, dim_user, dim_visitante
- E outras 15 tabelas de dimensão

### 2. 📈 Redshift - Fatos (28 tabelas)
**URL:** https://docs.google.com/spreadsheets/d/1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs

Contém todas as tabelas de fatos (fato_*):
- fato_acesso, fato_declaracao, fato_horas_ideais
- fato_mobconnect_* (atendimento, atividades, evidências, visitas)
- fato_status_* (colaboradores, promotores, lojas, documentos)
- E outras 18 tabelas de fatos

### 3. 🔗 Redshift - Lookup e Tabelas (12 tabelas)
**URL:** https://docs.google.com/spreadsheets/d/1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI

Contém lookups (lkp_*) e tabelas auxiliares (tbl_*):
- lkp_alocacao_promotor, lkp_fornecedor_rede
- tbl_ajustes_*, tbl_cnpj_*, tbl_estrutura_mercadologica
- E outras 8 tabelas

---

## 🚀 Como Funciona

### Arquivos do Sistema

1. **redshift_config.json** - Credenciais do Redshift
2. **spreadsheets_config.json** - IDs das planilhas e configurações
3. **sync_redshift_daily.py** - Script principal de sincronização
4. **executar_sync_diario.bat** - Script batch para execução
5. **configurar_agendamento.ps1** - Configura agendamento automático
6. **sync_log.txt** - Log de execução (criado automaticamente)

### Limitações de Dados

Para evitar estourar o limite de 10 milhões de células do Google Sheets:

- **Tabelas pequenas** (< 100k registros): até 50.000 registros
- **Tabelas médias** (100k - 1M registros): até 10.000 registros
- **Tabelas grandes** (> 1M registros): até 5.000 registros

Tabelas temporárias e vazias são automaticamente ignoradas.

---

## ⚙️ Configuração Inicial

### 1. Instalar Dependências Python

```bash
pip install psycopg2-binary google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Configurar Agendamento Automático

**Opção A: Usar o script PowerShell (Recomendado)**

1. Clique com botão direito em `configurar_agendamento.ps1`
2. Selecione "Executar com PowerShell"
3. Confirme se quer executar um teste

**Opção B: Configurar manualmente**

1. Abra o "Agendador de Tarefas" do Windows
2. Clique em "Criar Tarefa Básica"
3. Nome: `Sync Redshift to Google Sheets`
4. Gatilho: Diariamente às 06:00
5. Ação: Iniciar programa
   - Programa: `C:\Users\Donizete Senne\Desktop\Mob2Con-Central\executar_sync_diario.bat`
   - Iniciar em: `C:\Users\Donizete Senne\Desktop\Mob2Con-Central`

---

## 🔧 Uso Manual

### Executar Sincronização Agora

**Opção 1: Duplo clique**
```
executar_sync_diario.bat
```

**Opção 2: Linha de comando**
```bash
cd "C:\Users\Donizete Senne\Desktop\Mob2Con-Central"
python sync_redshift_daily.py
```

**Opção 3: Via Task Scheduler**
```powershell
Start-ScheduledTask -TaskName "Sync Redshift to Google Sheets"
```

### Ver Log de Execução

```bash
type sync_log.txt
```

Ou abra o arquivo `sync_log.txt` no Notepad.

---

## 📝 Gerenciar Agendamento

### Desabilitar Sincronização Automática
```powershell
Disable-ScheduledTask -TaskName "Sync Redshift to Google Sheets"
```

### Habilitar Sincronização Automática
```powershell
Enable-ScheduledTask -TaskName "Sync Redshift to Google Sheets"
```

### Remover Agendamento
```powershell
Unregister-ScheduledTask -TaskName "Sync Redshift to Google Sheets" -Confirm:$false
```

### Alterar Horário

1. Abra o "Agendador de Tarefas"
2. Localize "Sync Redshift to Google Sheets"
3. Clique com botão direito → Propriedades
4. Aba "Gatilhos" → Editar
5. Altere o horário desejado

---

## 🔍 Monitoramento

### Verificar Última Execução

1. Abra o "Agendador de Tarefas"
2. Localize "Sync Redshift to Google Sheets"
3. Veja "Última Execução" e "Resultado da Última Execução"

### Verificar Log Detalhado

O arquivo `sync_log.txt` contém:
- Timestamp de cada execução
- Tabelas processadas
- Quantidade de registros sincronizados
- Erros (se houver)

---

## ⚠️ Solução de Problemas

### Erro: "Não foi possível conectar ao Redshift"

- Verifique se as credenciais em `redshift_config.json` estão corretas
- Verifique sua conexão com a internet
- Verifique se o cluster Redshift está ativo

### Erro: "Token do Google expirado"

Execute novamente o script de autenticação do Google OAuth:
```bash
cd "C:\Users\Donizete Senne\.aws\amazonq\universal-control"
node google-oauth-setup.js
```

### Erro: "Limite de células excedido"

Reduza os limites em `spreadsheets_config.json`:
```json
"max_rows_small": 30000,
"max_rows_medium": 5000,
"max_rows_large": 2000
```

### Sincronização muito lenta

- Reduza `batch_size` em `spreadsheets_config.json`
- Adicione mais tabelas à lista `skip_tables`
- Execute fora do horário de pico

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique o arquivo `sync_log.txt`
2. Execute manualmente para ver erros em tempo real
3. Verifique as planilhas no Google Sheets

---

## 📅 Histórico de Versões

### v1.0 - 2026-05-15
- ✅ Sincronização inicial criada
- ✅ 3 planilhas organizadas por categoria
- ✅ 63 tabelas do schema `dw` sincronizadas
- ✅ Agendamento automático diário configurado
- ✅ Sistema de log implementado

---

## 🎯 Próximas Melhorias

- [ ] Sincronização incremental (apenas dados novos)
- [ ] Notificação por email ao concluir
- [ ] Dashboard de monitoramento
- [ ] Backup automático das planilhas
- [ ] Filtros por data nas tabelas de fatos
