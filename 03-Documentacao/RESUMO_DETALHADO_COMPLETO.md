# 📊 Resumo Detalhado - Projeto Sincronização Redshift → Google Sheets

**Data:** 15 de Maio de 2026  
**Status:** ✅ Concluído e em Produção  
**Duração do Projeto:** ~4 horas

---

## 🎯 Objetivo do Projeto

Criar um sistema automatizado que sincronize diariamente os dados do **Amazon Redshift** (banco de dados `rg_bi`, schema `dw`) para **Google Sheets**, permitindo:

- Acesso fácil aos dados sem precisar de ferramentas SQL
- Compartilhamento com equipe via Google Sheets
- Integração com Power BI e outras ferramentas de BI
- Atualização automática diária sem intervenção manual

---

## 📋 O Que Foi Desenvolvido

### 1. Conexão com Amazon Redshift

**Configuração:**
- Host: `m2c-redshift-cluster-1.cdsdjzdiml9e.us-west-2.redshift.amazonaws.com`
- Porta: `5439`
- Database: `rg_bi`
- Schema: `dw`
- Usuário: `marcelo.prado`

**Tecnologia:**
- Python 3.13 com biblioteca `psycopg2-binary`
- Conexão SSL segura
- Timeout de 15 segundos

**Resultado:**
- ✅ Conexão testada e funcionando
- ✅ 76 tabelas identificadas no schema `dw`
- ✅ 63 tabelas selecionadas para sincronização (13 ignoradas por serem temporárias/vazias)

---

### 2. Criação das Planilhas Google Sheets

**Estratégia de Organização:**

Devido ao limite de 10 milhões de células por planilha do Google Sheets, os dados foram divididos em **3 planilhas separadas** por categoria:

#### 📊 Planilha 1: Dimensões (23 tabelas)
**ID:** `1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q`  
**Link:** https://docs.google.com/spreadsheets/d/1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q

**Tabelas incluídas:**
- `dim_agencia` (4.006 registros)
- `dim_loja` (11.103 registros)
- `dim_fornecedor` (58.391 registros → 50k sincronizados)
- `dim_produto` (5.006.698 registros → 5k sincronizados)
- `dim_produto_rede` (7.272.273 registros → 5k sincronizados)
- `dim_rede` (491 registros)
- `dim_tempo` (12.417 registros)
- `dim_user` (53.608 registros → 50k sincronizados)
- `dim_visitante` (977.863 registros → 10k sincronizados)
- `dim_contratante` (62.893 registros → 50k sincronizados)
- `dim_contrato` (179 registros)
- `dim_documento` (153 registros)
- `dim_escala_trabalho` (5 registros)
- `dim_funcao_prestador_servico` (320 registros)
- `dim_prestador_servico` (841 registros)
- `dim_unidade_fabril` (846.996 registros → 10k sincronizados)
- `dim_projeto_agencia_fornecedor` (7.973 registros)
- `dim_status_aprovacao` (6 registros)
- `dim_app_acesso` (5 registros)
- `dim_mobconnect_destino_problema` (4 registros)
- `dim_mobconnect_status_atividade` (5 registros)
- `dim_mobconnect_tag` (124 registros)
- `dim_mobconnect_tipo_problema` (10 registros)

**Total sincronizado:** ~250.000 registros

---

#### 📈 Planilha 2: Fatos (28 tabelas)
**ID:** `1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs`  
**Link:** https://docs.google.com/spreadsheets/d/1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs

**Tabelas incluídas:**

**Fatos de Acesso:**
- `fato_acesso` (131.021.521 registros → 5k sincronizados)
- `fato_acesso_prestador_servico` (3.583.414 registros → 5k sincronizados)
- `fato_acesso_validacao` (1.860.968 registros → 5k sincronizados)

**Fatos Agregados:**
- `fato_agg_prestador_servico_diario` (3.464.985 registros → 5k sincronizados)
- `fato_agg_prestador_servico_mensal` (139.221 registros → 10k sincronizados)
- `fato_agg_status_documentacao_colaboradores_redes` (4.343.449 registros → 5k sincronizados)
- `fato_agg_status_documentacao_redes` (56.621.039 registros → 5k sincronizados)

**Fatos de Contrato:**
- `fato_contrato_pontual` (627 registros)
- `fato_contrato_semanal` (996 registros)

**Fatos Operacionais:**
- `fato_declaracao` (62.672.834 registros → 5k sincronizados)
- `fato_horas_ideais` (911.721.599 registros → 5k sincronizados)

**Fatos MobConnect:**
- `fato_mobconnect_atendimento` (408.007 registros → 10k sincronizados)
- `fato_mobconnect_atendimento_fornecedores` (1.426.354 registros → 5k sincronizados)
- `fato_mobconnect_atendimento_lojas` (101.816 registros → 10k sincronizados)
- `fato_mobconnect_atividades` (19.993.917 registros → 5k sincronizados)
- `fato_mobconnect_atividades_pendentes` (50.263.993 registros → 5k sincronizados)
- `fato_mobconnect_evidencias` (76.373 registros → 50k sincronizados)
- `fato_mobconnect_evidencias_fornecedores` (4.977.439 registros → 5k sincronizados)
- `fato_mobconnect_ruptura_administrativa` (4.850.515 registros → 5k sincronizados)
- `fato_mobconnect_visitas` (168.342 registros → 10k sincronizados)

**Fatos de Status:**
- `fato_status_colaboradores` (17.435.604 registros → 5k sincronizados)
- `fato_status_contratantes` (97.166.674 registros → 5k sincronizados)
- `fato_status_documento_colaboradores_redes` (14.411.614 registros → 5k sincronizados)
- `fato_status_documento_redes` (741.992.231 registros → 5k sincronizados)
- `fato_status_lojas` (5.354.011 registros → 5k sincronizados)
- `fato_status_promotores` (604.212.381 registros → 5k sincronizados)
- `fato_status_promotores_alocacao_vinculo` (890.489.705 registros → 5k sincronizados)

**Fatos de Projeto:**
- `fato_projeto_agencia_fornecedor` (100.064.885 registros → 5k sincronizados)

**Total sincronizado:** ~200.000 registros

---

#### 🔗 Planilha 3: Lookup e Tabelas (12 tabelas)
**ID:** `1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI`  
**Link:** https://docs.google.com/spreadsheets/d/1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI

**Tabelas incluídas:**

**Lookups:**
- `lkp_alocacao_promotor` (1.713.576 registros → 5k sincronizados)
- `lkp_fornecedor_rede` (164.954 registros → 10k sincronizados)
- `lkp_projeto_agencia_fornecedor` (367.056 registros → 10k sincronizados)

**Tabelas Auxiliares:**
- `tbl_ajustes_codigos_lojas` (27 registros)
- `tbl_ajustes_niveis_produto` (16 registros)
- `tbl_cnpj_inativo_mob` (6.100 registros)
- `tbl_cnpj_rede_cadastro` (262.194 registros → 10k sincronizados)
- `tbl_estrutura_mercadologica` (296.317 registros → 10k sincronizados)
- `tbl_mobconnect_respostas` (35.800 registros)
- `tbl_prestador_servico_promotor` (1.694.833 registros → 5k sincronizados)
- `tbl_scores_redes` (501 registros)

**Staging:**
- `stg_yhub_mercadologica` (511.420 registros → 10k sincronizados)

**Total sincronizado:** ~100.000 registros

---

### 3. Estrutura de Cada Planilha

Cada uma das 3 planilhas possui:

**Aba "📋 Índice":**
- Lista todas as tabelas da categoria
- Mostra total de registros no Redshift
- Mostra quantidade sincronizada
- Status da sincronização (OK, Vazia, Erro)
- Data/hora da última atualização

**Abas de Dados:**
- Uma aba para cada tabela
- Nome da aba = nome da tabela
- Primeira linha = cabeçalhos (nomes das colunas)
- Linhas seguintes = dados

---

### 4. Limitações Implementadas

Para evitar estourar o limite de 10 milhões de células do Google Sheets:

| Tamanho da Tabela | Limite de Registros |
|-------------------|---------------------|
| < 100.000 registros | Até 50.000 |
| 100.000 - 1.000.000 | Até 10.000 |
| > 1.000.000 | Até 5.000 |

**Tabelas ignoradas (13):**
- `dim_produto_rede_to_delete`
- `dim_produto_rede_to_delete2`
- `to_delete_unidade_fabril`
- `to_delete_unidade_fabril_2`
- `tmp_sk_user_to_delete`
- `tmp_sk_visitante_to_delete`
- `tmp_tbl_base_store_product_infos`
- `stg_dim_documento` (vazia)
- `stg_fato_mobconnect_atendimento_lojas` (vazia)
- `fato_contrato_anual` (vazia)
- `fato_contrato_mensal` (vazia)
- `fato_execucao_dia` (vazia)
- `tbl_rls_controle_varejo_prestador` (vazia)

---

## 🔄 Sistema de Sincronização Automática

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Windows Task Scheduler                    │
│                  (Executa todo dia às 06:00)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              executar_sync_diario.bat                        │
│              (Script batch executor)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              sync_redshift_daily.py                          │
│              (Script Python principal)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌─────────────────┐
│   Redshift   │ │  Google  │ │  Google Sheets  │
│   Database   │ │  OAuth   │ │   API v4        │
│              │ │  Token   │ │                 │
└──────────────┘ └──────────┘ └─────────────────┘
        │              │              │
        └──────────────┴──────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    sync_log.txt                              │
│              (Log de execução com timestamp)                 │
└─────────────────────────────────────────────────────────────┘
```

### Componentes do Sistema

**1. Arquivos de Configuração:**
- `redshift_config.json` - Credenciais do Redshift
- `spreadsheets_config.json` - IDs das planilhas e limites
- Token OAuth Google (gerenciado automaticamente)

**2. Scripts de Sincronização:**
- `sync_redshift_daily.py` - Script principal Python
- `executar_sync_diario.bat` - Executor batch para Windows
- `configurar_agendamento.ps1` - Configurador do Task Scheduler

**3. Sistema de Log:**
- `sync_log.txt` - Log detalhado com timestamp
- Registra início, progresso e conclusão
- Registra erros e avisos

**4. Agendamento:**
- Windows Task Scheduler
- Nome da tarefa: "Sync Redshift to Google Sheets"
- Horário: Diariamente às 06:00
- Timeout: 2 horas
- Executa mesmo em bateria
- Reexecuta se perdeu horário

---

## 📊 Estatísticas do Projeto

### Dados Sincronizados

| Métrica | Valor |
|---------|-------|
| Tabelas processadas | 63 de 76 |
| Tabelas ignoradas | 13 |
| Planilhas criadas | 3 |
| Abas criadas | 66 (63 tabelas + 3 índices) |
| Registros sincronizados | ~550.000 linhas |
| Células populadas | ~8.000.000 |

### Performance

| Operação | Tempo |
|----------|-------|
| Conexão Redshift | ~2 segundos |
| Listagem de tabelas | ~1 segundo |
| Extração por tabela | 5-30 segundos |
| Upload para Sheets | 10-60 segundos |
| **Sincronização completa** | **15-30 minutos** |

### Distribuição de Dados

| Categoria | Tabelas | Registros | % do Total |
|-----------|---------|-----------|------------|
| Dimensões | 23 | ~250.000 | 45% |
| Fatos | 28 | ~200.000 | 36% |
| Lookup/Tabelas | 12 | ~100.000 | 19% |

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.13**
  - `psycopg2-binary` - Conexão PostgreSQL/Redshift
  - `google-auth` - Autenticação Google
  - `google-api-python-client` - Google Sheets API v4
  - `json` - Manipulação de configurações
  - `datetime` - Timestamps e logs

### Infraestrutura
- **Amazon Redshift** - Data Warehouse
- **Google Sheets API v4** - Armazenamento de dados
- **Google OAuth 2.0** - Autenticação
- **Windows Task Scheduler** - Agendamento

### Ferramentas
- **PowerShell** - Automação Windows
- **Batch Scripts** - Execução de tarefas
- **Git** (opcional) - Controle de versão

---

## 📁 Organização de Arquivos

### Pasta Local: `C:\Users\Donizete Senne\Desktop\Mob2Con-Central`

```
Mob2Con-Central/
│
├── 📄 Configuração
│   ├── redshift_config.json
│   ├── spreadsheets_config.json
│   └── .gitignore
│
├── 🐍 Scripts Python
│   ├── sync_redshift_daily.py (PRINCIPAL)
│   ├── sync_redshift_multi_sheets.py
│   ├── list_dw_tables.py
│   └── redshift_query.py
│
├── 🔧 Scripts de Automação
│   ├── executar_sync_diario.bat
│   └── configurar_agendamento.ps1
│
├── 📚 Documentação
│   ├── README_SYNC_REDSHIFT.md
│   ├── RESUMO_PROJETO_SYNC.md
│   ├── RESUMO_DETALHADO_COMPLETO.md (este arquivo)
│   ├── COMANDOS_RAPIDOS.txt
│   ├── ORGANIZACAO_FINAL.txt
│   └── 🎉 PROJETO_CONCLUIDO.txt
│
└── 📋 Logs
    └── sync_log.txt (criado automaticamente)
```

### Pasta Google Drive: "Projeto"
**ID:** `1WmfS-xpi8GKSHghaIZxkRfbbGSXMxfG3`  
**Link:** https://drive.google.com/drive/folders/1WmfS-xpi8GKSHghaIZxkRfbbGSXMxfG3

```
Projeto/
│
├── 📊 Planilhas Redshift (NOVAS)
│   ├── 📊 Redshift - Dimensões
│   ├── 📈 Redshift - Fatos
│   └── 🔗 Redshift - Lookup e Tabelas
│
├── 📊 Planilhas Antigas
│   └──  Amazon Redshift (pode deletar)
│
├── 💼 Power BI
│   ├── Mockup Dash Implantação.pbip
│   ├── Acompanhamento Captação RG 2.0.pbip
│   ├── Analítico RG 2.0.pbip
│   └── (arquivos .pbix e pastas .Report/.SemanticModel)
│
└── 📊 Bases Excel
    ├── Mob2Con_Base_Consolidada_PowerBI.xlsx
    └── Mob2Con_Base_Implantacao_v2.xlsx
```

---

## 🎯 Casos de Uso

### 1. Análise no Power BI
**Cenário:** Criar dashboards conectando no Google Sheets

**Passos:**
1. Abrir Power BI Desktop
2. Obter Dados → Serviços Online → Google Sheets
3. Conectar nas 3 planilhas:
   - Dimensões
   - Fatos
   - Lookup/Tabelas
4. Criar relacionamentos entre tabelas
5. Construir visualizações
6. Publicar no Power BI Service

**Benefício:** Dados atualizados automaticamente todo dia às 06:00

---

### 2. Análise Direta no Google Sheets
**Cenário:** Análise rápida sem ferramentas de BI

**Passos:**
1. Acessar a planilha desejada
2. Usar fórmulas (VLOOKUP, SUMIF, etc.)
3. Criar tabelas dinâmicas
4. Criar gráficos
5. Compartilhar com equipe

**Benefício:** Acesso imediato, sem instalação de software

---

### 3. Exportação para Excel
**Cenário:** Trabalhar offline ou enviar relatórios

**Passos:**
1. Abrir planilha Google Sheets
2. Arquivo → Fazer download → Microsoft Excel
3. Trabalhar no Excel localmente

**Benefício:** Flexibilidade para trabalhar offline

---

### 4. Integração com Outras Ferramentas
**Cenário:** Usar dados em Python, R, Tableau, etc.

**Passos:**
1. Usar Google Sheets API
2. Ou exportar para CSV
3. Importar na ferramenta desejada

**Benefício:** Compatibilidade universal

---

## 🔐 Segurança

### Credenciais Redshift
- ✅ Armazenadas em arquivo JSON local
- ✅ Não versionadas no Git (.gitignore)
- ⚠️ **Recomendação:** Rotacionar senha periodicamente

### Token Google OAuth
- ✅ Armazenado em pasta protegida do sistema
- ✅ Renovado automaticamente
- ✅ Acesso apenas à conta do usuário

### Acesso às Planilhas
- ✅ Controlado por permissões do Google Drive
- ✅ Pode compartilhar com equipe
- ✅ Histórico de versões mantido pelo Google

---

## 📈 Monitoramento e Manutenção

### Verificar Status da Sincronização

**1. Via Task Scheduler:**
```
1. Win + R → taskschd.msc
2. Procurar "Sync Redshift to Google Sheets"
3. Ver "Última Execução" e "Próxima Execução"
```

**2. Via Log:**
```
type "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\sync_log.txt"
```

**3. Via Planilhas:**
```
Abrir aba "📋 Índice" em qualquer planilha
Ver coluna "Atualização" com data/hora
```

### Alertas de Problemas

**Sincronização não executou:**
- Verificar se PC estava ligado às 06:00
- Verificar histórico no Task Scheduler
- Executar manualmente para ver erros

**Erro de autenticação:**
- Token Google expirado
- Reautenticar: `node google-oauth-setup.js`

**Erro de conexão Redshift:**
- Verificar internet
- Verificar se cluster está ativo
- Verificar credenciais

**Dados desatualizados:**
- Verificar log de execução
- Executar sincronização manual
- Verificar aba "📋 Índice"

---

## 🚀 Próximas Melhorias Sugeridas

### Curto Prazo (1-2 semanas)
1. **Sincronização Incremental**
   - Sincronizar apenas dados novos/alterados
   - Reduzir tempo de execução
   - Usar colunas de data/timestamp

2. **Notificação por Email**
   - Enviar email ao concluir sincronização
   - Alertar em caso de erro
   - Resumo de registros sincronizados

3. **Dashboard de Monitoramento**
   - Criar planilha com histórico de execuções
   - Gráficos de performance
   - Alertas visuais

### Médio Prazo (1-2 meses)
4. **Filtros por Data**
   - Sincronizar apenas últimos 90 dias para fatos
   - Reduzir volume de dados
   - Melhorar performance

5. **Backup Automático**
   - Criar cópias das planilhas antes de atualizar
   - Manter histórico de 7 dias
   - Facilitar recuperação

6. **Views no Redshift**
   - Criar views pré-agregadas
   - Reduzir processamento
   - Melhorar performance

### Longo Prazo (3-6 meses)
7. **Interface Web**
   - Dashboard para gerenciar sincronizações
   - Configurar horários e tabelas
   - Visualizar logs

8. **Múltiplos Ambientes**
   - Desenvolvimento, Homologação, Produção
   - Sincronizações independentes
   - Testes sem impactar produção

9. **API REST**
   - Endpoint para disparar sincronização
   - Webhook para notificações
   - Integração com outros sistemas

---

## 📞 Suporte e Contatos

### Documentação
- **Manual Completo:** `README_SYNC_REDSHIFT.md`
- **Comandos Rápidos:** `COMANDOS_RAPIDOS.txt`
- **Este Resumo:** `RESUMO_DETALHADO_COMPLETO.md`

### Troubleshooting
1. Verificar `sync_log.txt`
2. Executar sincronização manual
3. Verificar Task Scheduler
4. Verificar credenciais

### Recursos Externos
- **Google Sheets API:** https://developers.google.com/sheets/api
- **Redshift Documentation:** https://docs.aws.amazon.com/redshift/
- **Python psycopg2:** https://www.psycopg.org/docs/

---

## ✅ Checklist de Conclusão

- [x] Conexão com Redshift configurada e testada
- [x] 3 planilhas Google Sheets criadas
- [x] 63 tabelas sincronizadas
- [x] Sistema de sincronização automática implementado
- [x] Agendamento diário configurado (06:00)
- [x] Sistema de log implementado
- [x] Documentação completa criada
- [x] Planilhas organizadas na pasta "Projeto"
- [x] Configuração atualizada com localização
- [x] Testes de sincronização realizados

---

## 🎉 Conclusão

O projeto foi **concluído com sucesso** e está **100% funcional em produção**.

**Principais Conquistas:**
- ✅ Dados do Redshift acessíveis via Google Sheets
- ✅ Atualização automática diária sem intervenção
- ✅ Organização inteligente por categoria
- ✅ Fácil integração com Power BI
- ✅ Compartilhamento simples com equipe
- ✅ Monitoramento via log
- ✅ Documentação completa

**Próxima Execução Automática:** 16/05/2026 às 06:00

---

**Desenvolvido em:** 15 de Maio de 2026  
**Versão:** 1.0  
**Status:** ✅ Produção  
**Última Atualização:** 15/05/2026 12:45
