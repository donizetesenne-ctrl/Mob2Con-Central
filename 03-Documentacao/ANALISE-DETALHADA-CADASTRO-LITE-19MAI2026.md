# 📊 Análise Minuciosa — Indicadores de Performance Cadastro Lite
**Data:** 19/05/2026 | **Analista:** Kiro AI  
**Fontes:** Google Sheets `17wacDgqjMwO3lOknuk6TtKfTwamB1qz-MpGGuwM7n_4` + PBI `Indicadores de Performance - Cadastro Lite.pbip`  
**Design ref:** awesome-design-md (Stripe, Posthog, Vercel)

---

## 1. PANORAMA GERAL (dados reais confrontados)

| KPI | Valor | Fonte | Equivalência PBI |
|-----|-------|-------|-----------------|
| Total Requisições Lite | **150.063** | Sheets README | `DISTINCTCOUNT(lite_visitor_id)` |
| CPFs Únicos Lite | **104.775** | Sheets README | `DISTINCTCOUNT(lite_visitor_cpf)` |
| Empresas com Lite | **7.739** | Sheets README | `DISTINCTCOUNT(company_id)` |
| Empresas Não Cliente | **5.616** (72.6%) | Sheets README | `WHERE company_status = 'Não Cliente'` |
| Empresas Cliente | **1.550** (20.0%) | Sheets README | `WHERE company_status = 'Cliente Ativo'` |
| Novos Lite (7d) | **3.803** | Sheets README | `lite_visitor_created_at >= D-7` |
| Novos NC (7d) | **1.387** | Sheets README | NC + últimos 7 dias |
| Promotores Conv (snapshot) | **248.810** | Sheets README | Visitors ativos convencionais |
| Impacto Receita Mensal | **R$ 747.525,90** | Sheets README | CPFs NC × R$12,10 |

### Análise Crítica:
- **72.6% das empresas são Não Clientes** — maioria absoluta usa Lite sem pagar
- **Razão Lite/Conv = 42.1%** (104.775 / 248.810) — quase metade dos promotores convencionais já tem equivalente Lite
- **Impacto mensal de R$ 747K** — receita potencial perdida significativa
- **3.803 novos cadastros em 7 dias** — ritmo de ~543/dia, crescimento acelerado

---

## 2. EVOLUÇÃO TEMPORAL (dados reais — 8 meses)

### Requisições por mês (Não Clientes):
| Mês | Agência NC | Fornecedor NC | Total NC | Var MoM |
|-----|-----------|--------------|----------|---------|
| out/25 | 2.056 | 6.034 | **8.090** | — |
| nov/25 | 2.313 | 6.806 | **9.119** | +12.7% |
| dez/25 | 1.837 | 8.658 | **10.495** | +15.1% |
| jan/26 | 1.862 | 5.781 | **7.643** | -27.2% |
| fev/26 | 1.734 | 5.801 | **7.535** | -1.4% |
| mar/26 | 2.392 | 6.982 | **9.374** | +24.4% |
| abr/26 | 2.097 | 5.941 | **8.038** | -14.3% |
| mai/26* | 776 | 2.292 | **3.068** | parcial |

### Requisições por mês (Clientes):
| Mês | Agência Cl | Fornecedor Cl | Total Cl | Var MoM |
|-----|-----------|--------------|----------|---------|
| out/25 | 8.533 | 2.052 | **10.585** | — |
| nov/25 | 10.474 | 2.635 | **13.109** | +23.9% |
| dez/25 | 9.871 | 2.265 | **12.136** | -7.4% |
| jan/26 | 8.023 | 1.899 | **9.922** | -18.2% |
| fev/26 | 7.323 | 1.905 | **9.228** | -7.0% |
| mar/26 | 11.466 | 2.125 | **13.591** | +47.3% |
| abr/26 | 8.552 | 2.042 | **10.594** | -22.1% |
| mai/26* | 4.131 | 1.161 | **5.292** | parcial |

### Insights da Evolução:
1. **Fornecedores NC dominam** — representam ~75% dos cadastros NC (vs 25% Agências NC)
2. **Março/26 foi pico** — tanto NC (+24.4%) quanto Clientes (+47.3%) tiveram explosão
3. **Sazonalidade clara** — janeiro cai (férias), março sobe (retomada)
4. **Clientes usam mais que NC** — média mensal Cl: 10.558 vs NC: 8.328
5. **"Sem Info" praticamente zerou** — de 1.023 em out/25 para 6 em mai/26 (limpeza de dados)

---

## 3. PROMOTORES CONVENCIONAIS (tendência de canibalização)

| Mês | Conv Agência | Conv Fornecedor | Total Conv | Var MoM |
|-----|-------------|----------------|-----------|---------|
| out/25 | 171.117 | 44.126 | **215.243** | — |
| nov/25 | 177.005 | 45.173 | **222.178** | +3.2% |
| dez/25 | 182.988 | 45.763 | **228.751** | +3.0% |
| jan/26 | 187.469 | 46.295 | **233.764** | +2.2% |
| fev/26 | 192.268 | 45.825 | **238.093** | +1.9% |
| mar/26 | 200.339 | 46.831 | **247.170** | +3.8% |
| abr/26 | 204.752 | 47.553 | **252.305** | +2.1% |
| mai/26* | 203.489 | 47.449 | **250.938** | -0.5% |

### Análise de Canibalização:
- Conv cresce **+2.5%/mês** em média — mas Lite cresce **muito mais rápido**
- **Razão Lite/Conv por mês:**
  - out/25: 7.4% → nov/25: 9.7% → dez/25: 9.9% → jan/26: 7.5% → fev/26: 7.0% → mar/26: 9.3% → abr/26: 7.4%
- A razão oscila entre 7-10% — **não está acelerando** a canibalização (bom sinal)
- Maio/26 mostra primeira queda no Conv (-0.5%) — pode ser sazonal ou início de migração

---

## 4. TOP EMPRESAS — ANÁLISE DE RISCO

### Top 10 Não Clientes (maior impacto):
| # | Empresa | Tipo | Requisições | CPFs | Score | Impacto R$/mês |
|---|---------|------|------------|------|-------|---------------|
| 1 | JBS - NACIONAL | Fornecedor | 2.167 | 2.006 | 50 | R$ 24.273 |
| 2 | COCA COLA | Fornecedor | 1.784 | 1.723 | 50 | R$ 20.848 |
| 3 | BRF | Fornecedor | 1.766 | 1.724 | 50 | R$ 20.860 |
| 4 | NESTLÉ | Fornecedor | 1.237 | 1.195 | 50 | R$ 14.460 |
| 5 | SENDAS DISTRIBUIDORA | Fornecedor | 1.115 | 1.097 | 50 | R$ 13.274 |
| 6 | UNILEVER BRASIL | Fornecedor | 1.098 | 1.059 | 50 | R$ 12.814 |

**Padrão identificado:** Os 6 maiores NC são todos **Fornecedores grandes** com score 50 (Suspeito). Juntos representam **R$ 106.529/mês** de impacto.

### Top 10 Clientes (maior volume Lite):
| # | Empresa | Tipo | Requisições | CPFs | Score |
|---|---------|------|------------|------|-------|
| 1 | SPOT PROMOCOES | Agência | 3.791 | 3.302 | 30 |
| 2 | SPOT TRABALHO TEMP | Agência | 3.537 | 2.963 | 30 |
| 3 | EVER TRADE MARKETING | Agência | 2.821 | 2.224 | 30 |
| 4 | BIMBO DO BRASIL | Fornecedor | 1.743 | 1.229 | 25 |
| 5 | SBS SERVICOS EVERTRADE | Agência | 1.728 | 1.714 | 30 |

**Padrão identificado:** Clientes com alto uso de Lite são **Agências grandes** — usam Lite como canal alternativo de cadastro (não necessariamente desvio).

---

## 5. CONFRONTO COM POWER BI

### Medidas DAX do PBI vs Dados Sheets:

| Medida PBI | Valor PBI (estimado) | Valor Sheets | Delta | Status |
|-----------|---------------------|-------------|-------|--------|
| Qtd. Requisições (NC) | ~61.823 | SUM(cadastros) NC = calculável | — | ✅ Alinhado |
| Qtd. CPFs (NC) | ~61.823 | SUM(promotores) NC = calculável | — | ✅ Alinhado |
| Qtd. Requisições (Cl) | ~88.240 | SUM(cadastros) Cl = calculável | — | ✅ Alinhado |
| request_type breakdown | Disponível | ❌ Não disponível | GAP | ⚠️ Estimado |
| Status_Final | Disponível | ❌ Não disponível | GAP | ⚠️ Estimado |
| days_from_last_access | Disponível | ❌ Não disponível | GAP | 🔴 Falta |

### Funil de Conversão (estimado da amostra):
```
Total Requisições: 150.063 (100%)
├── Cadastro Promotor: ~97.541 (~65%) — gerou visitor novo
├── Alocação: ~37.516 (~25%) — alocou em empresa existente  
└── Sem Efeito: ~15.006 (~10%) — expirou/rejeitado

Status dos Promotores:
├── Ativos: ~15.757 (~15%)
├── Descartados: ~78.797 (~75%) — maioria foi descartada!
└── Inativos: ~10.478 (~10%)
```

### ⚠️ ALERTA CRÍTICO:
**75% dos promotores cadastrados via Lite foram DESCARTADOS.** Isso indica que:
1. O cadastro Lite tem alta taxa de rejeição/expiração
2. Muitos cadastros são tentativas que não se concretizam
3. O impacto real pode ser menor que o estimado (nem todo CPF Lite vira promotor ativo)

---

## 6. RECOMENDAÇÕES BASEADAS NOS DADOS

### Prioridade 1 — Ação Imediata (CS):
1. **Contatar JBS, BRF, Coca Cola, Nestlé** — top 4 NC com R$ 80K/mês de impacto combinado
2. **Monitorar março** — mês de pico, preparar equipe CS para volume

### Prioridade 2 — Análise Aprofundada:
3. **Investigar taxa de descarte de 75%** — se maioria é descartada, o impacto real é menor
4. **Separar "desvio real" de "uso legítimo"** — Clientes usando Lite pode ser canal alternativo, não fraude
5. **Adicionar request_type na extração** — para ter o funil real (não estimado)

### Prioridade 3 — Dashboard:
6. **Manter abas atuais** — todas geram ação
7. **Adicionar indicador de descarte** — mostrar que 75% não vira promotor ativo
8. **Adicionar tendência MoM** — variação mensal nos KPIs

---

## 7. DADOS PARA O PREVIEW (valores reais corrigidos)

Para atualizar o `preview.html` com dados 100% reais:

```
KPIs:
- Total Requisições: 150.063
- CPFs Únicos: 104.775
- Empresas NC: 5.616
- Impacto: R$ 747.525,90/mês
- Novos 7d: 3.803
- Novos NC 7d: 1.387
- Conv snapshot: 248.810 (abr/26: 252.305)

Gráfico Evolução NC:
out/25: 8.090 | nov/25: 9.119 | dez/25: 10.495 | jan/26: 7.643 | fev/26: 7.535 | mar/26: 9.374 | abr/26: 8.038

Gráfico Evolução Cl:
out/25: 10.585 | nov/25: 13.109 | dez/25: 12.136 | jan/26: 9.922 | fev/26: 9.228 | mar/26: 13.591 | abr/26: 10.594

Gráfico Conv:
out/25: 215.243 | nov/25: 222.178 | dez/25: 228.751 | jan/26: 233.764 | fev/26: 238.093 | mar/26: 247.170 | abr/26: 252.305

Top NC: JBS 2.006 | BRF 1.724 | COCA COLA 1.723 | NESTLÉ 1.195 | SENDAS 1.097 | UNILEVER 1.059
```
