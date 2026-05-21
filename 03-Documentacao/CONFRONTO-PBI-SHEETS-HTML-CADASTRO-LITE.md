# 🔍 Análise Minuciosa — Confronto PBI × Sheets × HTML (Cadastro Lite)
**Data:** 19/05/2026  
**Analista:** Kiro AI  
**Fontes confrontadas:**
1. Power BI: `Indicadores de Performance - Cadastro Lite.pbip` (Redshift mc2-production)
2. Google Sheets: `17wacDgqjMwO3lOknuk6TtKfTwamB1qz-MpGGuwM7n_4`
3. Apps Script HTML: `06-MCP-Tools/cadastro-lite-v2/Index.html`

---

## 1. ESTRUTURA DE DADOS — O QUE CADA FONTE TEM

### Power BI (fonte primária — dados granulares)
| Tabela | Colunas principais | Filtro SQL |
|--------|-------------------|------------|
| **Não Clientes** | lite_visitor_id, lite_visitor_cpf, lite_visitor_name, company_type, company_id, company_name, company_status, retailer_id, retailer_trade_name, request_type, lite_visitor_created_at, last_access_at, days_from_last_access, visitor_discarded_status, Status_Final, Mais de uma Solicitação | `common_client_info.status = 0` AND `lv.status = 'approved'` |
| **Clientes** | (mesmas + visitor_status, client_approve_status, client_approve_expiration_date, approve_status_changed_at, days_until_approve_status_changed) | `common_client_info.status = 1` AND `lv.status = 'approved'` |
| **Indicadores** | 16 medidas DAX (calculadas) | — |
| **Calendario** | Date | Relaciona com lite_visitor_created_date |

### Google Sheets (fonte intermediária — dados agregados)
| Aba | Colunas | Granularidade |
|-----|---------|---------------|
| **README** | KPI, Valor | Totais globais |
| **Empresas** | empresa_id, empresa, contratante_tipo, status_empresa, cadastros, promotores, primeiro_cadastro, ultimo_cadastro, score_suspeita, classificacao | 1 linha por empresa |
| **Evolucao_Mensal** | mes, contratante_tipo, status_empresa, cadastros, promotores | 1 linha por mês/tipo/status |
| **Conv_Mensal** | mes, contratante_tipo, promotores_conv, registros_conv | 1 linha por mês/tipo |
| **Convencional** | contratante_tipo, empresa_id, empresa, tp_plano_cliente, nm_plano_cliente, promotores_conv | 1 linha por empresa conv |
| **Redes** | contratante_tipo, empresa_id, qt_redes, redes | 1 linha por empresa |

### HTML/Apps Script (frontend — o que o usuário vê)
| Aba | KPIs mostrados | Tabela |
|-----|---------------|--------|
| Visão Geral | Total Cadastros, Promotores Únicos, Empresas, NC, Clientes, Novos 7d, Impacto, Conv | Gráficos evolução + tipo + top10 |
| Não Clientes | Empresas, Promotores, Impacto, Críticos | Tabela empresa com score |
| Clientes | Empresas, Promotores, Cadastros, % Lite/Total | Tabela empresa com score |
| Alertas | Críticos, Alta Suspeita, Suspeito, Total | Cards de alerta |
| Priorização | Ranking por score | Tabela com impacto R$ |
| Redes | Empresas com Rede, Total Redes | Tabela empresa-rede |
| Conv vs Lite | Prom Lite, Prom Conv, Registros, Razão | Gráficos + tabela conv |
| Ação CS | Ações Registradas, Pendentes | Tabela + formulário |

---

## 2. CONFRONTO DETALHADO — O QUE BATE E O QUE NÃO BATE

### ✅ O QUE ESTÁ CORRETO (bate PBI ↔ Sheets ↔ HTML)

| Conceito | PBI | Sheets | HTML | Veredicto |
|----------|-----|--------|------|-----------|
| Separação NC vs Cliente | `common_client_info.status` (0 vs 1) | `status_empresa` (Nao Cliente vs Cliente) | Filtro por status_empresa | ✅ Correto |
| Tipo empresa | `company_type` (Agência/Fornecedor) | `contratante_tipo` (Agencia/Fornecedor) | Filtro + pill | ✅ Correto |
| Período | `>= 2025-10-01` | `desde 01/10/2025` | Header mostra | ✅ Correto |
| Empresa ID | `company_id` | `empresa_id` | Usado em filtros | ✅ Correto |
| Empresa Nome | `company_name` | `empresa` | Exibido em tabelas | ✅ Correto |
| Redes | `retailer_trade_name` | `redes` (concatenado) | Aba Redes | ✅ Correto |
| Evolução temporal | Por `lite_visitor_created_date` | Por `mes` | Gráficos mensais | ✅ Correto |
| Convencional | Snapshot visitors ativos | Aba Convencional | Aba Conv vs Lite | ✅ Correto |

### ⚠️ O QUE ESTÁ APROXIMADO (funciona mas não é exato)

| Conceito | PBI (exato) | Sheets (aproximado) | Diferença | Impacto |
|----------|-------------|---------------------|-----------|---------|
| **Requisições** | `DISTINCTCOUNT(lite_visitor_id)` = cada solicitação única | `cadastros` = soma agregada por empresa | Sheets soma, PBI conta distintos. Se 1 CPF fez 3 requisições, PBI conta 3, Sheets também conta 3 | **Baixo** — na prática são equivalentes pois lite_visitor_id é único por requisição |
| **CPFs/Promotores** | `DISTINCTCOUNT(lite_visitor_cpf)` = CPFs únicos | `promotores` = contagem por empresa | Se 1 CPF aparece em 2 empresas, PBI conta 1 global mas Sheets conta 1 por empresa | **Médio** — total global pode divergir ~5-10% |
| **Novos 7d** | Calculado em tempo real no PBI | Calculado no momento da extração | Defasagem de até 24h | **Baixo** |

### ❌ O QUE FALTA NO SHEETS/HTML (existe no PBI mas não está disponível)

| Informação PBI | Por que importa | Solução |
|----------------|-----------------|---------|
| **request_type** (Cadastro Promotor / Alocação / Sem efeito) | PBI mostra funil de conversão: quantas requisições viram cadastro vs alocação vs sem efeito | Adicionar coluna na extração Redshift → Sheets |
| **Status_Final** (Promotor Ativo / Descartado / Dois Status) | PBI mostra quantos promotores cadastrados via Lite estão ativos vs descartados | Adicionar coluna na extração |
| **visitor_status** (active / inactive / temporary_inactive) | Clientes: mostra estado atual do promotor | Adicionar coluna na extração |
| **client_approve_status** | Clientes: mostra se cadastro foi aprovado/rejeitado/expirado | Adicionar coluna na extração |
| **days_from_last_access** | Mostra engajamento — promotores inativos há X dias | Adicionar coluna na extração |
| **days_until_approve_status_changed** | SLA de aprovação do cliente | Adicionar coluna na extração |
| **Funil visual** (Total → Cadastro → Alocação → Sem Efeito) | Principal visual do PBI — mostra efetividade | Requer dados granulares |
| **Gráfico por Status_Final** | Mostra saúde dos promotores cadastrados | Requer dados granulares |

---

## 3. ANÁLISE CRÍTICA — O QUE FAZ SENTIDO E O QUE NÃO FAZ

### ✅ FAZ SENTIDO MANTER NO HTML:
1. **KPIs globais** (Total, Promotores, Empresas, Novos 7d, Impacto) — são os mesmos do PBI
2. **Tabela de empresas com score** — PBI não tem score de suspeita, isso é EXCLUSIVO do Sheets/HTML (valor agregado)
3. **Aba Alertas/Priorização** — PBI não tem isso, é inteligência adicional do Apps Script
4. **Aba Ação CS** — funcionalidade operacional que PBI não oferece (gravação de dados)
5. **Aba Redes** — mostra vínculo empresa-rede de forma mais clara que o PBI
6. **Aba Conv vs Lite** — comparativo que PBI não faz diretamente
7. **Filtros interativos** — Status, Tipo, Risco, Empresa, Min. promotores

### ❌ NÃO FAZ SENTIDO / ESTÁ ERRADO:
1. **"Cadastros" como label** — deveria ser "Requisições" (é DISTINCTCOUNT de lite_visitor_id)
2. **"Promotores" como label** — deveria ser "CPFs Únicos" (é DISTINCTCOUNT de lite_visitor_cpf)
3. **Fonte "Base Power BI"** — errado, a fonte real é Redshift mc2-production (DSN ODBC)
4. **Falta o funil** — principal visual do PBI não está representado no HTML

### 🔄 PODE MELHORAR:
1. **Adicionar breakdown por request_type** na extração → nova aba `Breakdown_RequestType`
2. **Adicionar Status_Final** na extração → enriquecer aba Empresas
3. **Adicionar mini-funil** no HTML (mesmo sem dados granulares, usar proporções estimadas)
4. **Adicionar days_from_last_access médio** por empresa → indicador de engajamento

---

## 4. DUPLICAÇÕES IDENTIFICADAS

| Item | Onde aparece | Ação |
|------|-------------|------|
| `empresa_id` + `empresa` | Sheets.Empresas + Sheets.Convencional + Sheets.Redes | OK — é chave de join, não duplicação |
| KPIs no README | Sheets.README + calculado no JS do HTML | ⚠️ Redundante — HTML recalcula do zero. README serve só como cache rápido |
| `contratante_tipo` | Em todas as abas | OK — é dimensão de filtro |
| Score/Classificação | Só em Sheets.Empresas | OK — não duplicado |
| Promotores Conv | Sheets.Convencional + Sheets.Conv_Mensal | OK — um é snapshot, outro é série temporal |

**Conclusão: NÃO há duplicação real de dados.** A estrutura está limpa.

---

## 5. RECOMENDAÇÕES FINAIS

### Prioridade ALTA (fazer agora):
1. ✅ **FEITO** — Renomear labels: "Cadastros" → "Requisições", "Promotores" → "CPFs"
2. ✅ **FEITO** — Corrigir fonte: "Redshift mc2-production" (não "Base Power BI")
3. ✅ **FEITO** — Atualizar tooltips com referência às medidas DAX

### Prioridade MÉDIA (próxima iteração):
4. Adicionar coluna `request_type` na extração Redshift → Sheets (requer alterar o script Python de sync)
5. Adicionar coluna `status_final` (Ativo/Descartado) na aba Empresas
6. Criar mini-funil no HTML: Total Requisições → % Cadastro → % Alocação → % Sem Efeito

### Prioridade BAIXA (futuro):
7. Adicionar `days_from_last_access` médio por empresa
8. Adicionar `client_approve_status` para clientes
9. Criar aba "Saúde" no HTML mostrando promotores ativos vs descartados

---

## 6. MAPEAMENTO DE EQUIVALÊNCIAS (referência rápida)

```
┌─────────────────────────────────────────────────────────────────────┐
│ POWER BI (DAX)                    │ SHEETS (coluna)  │ HTML (label) │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ Qtd. Requisições (NC)             │ SUM(cadastros)   │ Requisições  │
│ = DISTINCTCOUNT(lite_visitor_id)  │ WHERE NC         │              │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ Qtd. CPFs (NC)                    │ SUM(promotores)  │ CPFs         │
│ = DISTINCTCOUNT(lite_visitor_cpf) │ WHERE NC         │              │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ company_type                      │ contratante_tipo │ Tipo         │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ company_name                      │ empresa          │ Empresa      │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ company_status                    │ status_empresa   │ Status       │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ retailer_trade_name               │ redes            │ Redes        │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ lite_visitor_created_date         │ mes              │ Período      │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ request_type                      │ ❌ NÃO TEM       │ ❌ NÃO TEM   │
│ (Cadastro/Alocação/Sem efeito)    │                  │              │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ Status_Final                      │ ❌ NÃO TEM       │ ❌ NÃO TEM   │
│ (Ativo/Descartado/Dois Status)    │                  │              │
├───────────────────────────────────┼──────────────────┼──────────────┤
│ ❌ NÃO TEM                        │ score_suspeita   │ Score        │
│                                   │ classificacao    │ Class.       │
└───────────────────────────────────┴──────────────────┴──────────────┘
```

**Nota importante:** O score_suspeita e classificação são EXCLUSIVOS do Sheets/HTML — o PBI não tem essa inteligência. Isso é valor agregado do Apps Script.

---

## 7. VEREDICTO FINAL

O HTML/Apps Script **complementa** o Power BI, não duplica. Cada um tem seu papel:

| Ferramenta | Papel | Público |
|-----------|-------|---------|
| **Power BI** | Análise granular, drill-through por empresa/data, funil de conversão | Analistas internos |
| **Apps Script/HTML** | Monitoramento rápido, score de risco, priorização comercial, ações CS | Equipe comercial/CS |
| **Google Sheets** | Base intermediária, atualizada diariamente via Redshift sync | Ambos |

**A estrutura está correta e não há duplicação.** As melhorias são incrementais (adicionar request_type e Status_Final na extração).
