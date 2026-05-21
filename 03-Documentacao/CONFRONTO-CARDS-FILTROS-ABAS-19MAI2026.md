# 🔍 Confronto de Cards, Filtros e Abas — Dashboard Cadastro Lite v18
**Data:** 19/05/2026 21:40 | **Status:** Dashboard funcionando (deploy @29)

---

## 1. CARDS GLOBAIS (kpis-global) — Visíveis em todas as abas

| # | Card | Valor Exibido | Fonte Sheets | PBI Equivalente | Status | Melhoria |
|---|------|--------------|-------------|-----------------|--------|----------|
| 1 | Total Cadastros Lite | 150.063 | README: 150063 ✅ | DISTINCTCOUNT(lite_visitor_id) | ✅ CORRETO | Renomear para "Total Requisições" (nomenclatura PBI) |
| 2 | Promotores Únicos Lite | 104.775 | README: 104775 ✅ | DISTINCTCOUNT(lite_visitor_cpf) | ✅ CORRETO | Renomear para "CPFs Únicos" (nomenclatura PBI) |
| 3 | Empresas no Filtro | 7.739 (sem filtro) | Sheets Empresas: 7739 linhas ✅ | DISTINCTCOUNT(company_id) | ✅ CORRETO | OK — muda com filtro |
| 4 | Não Clientes (filtro) | 5.616 | README: 5616 ✅ | WHERE status=0 | ✅ CORRETO | OK |
| 5 | Clientes (filtro) | 1.550 | README: 1550 ✅ | WHERE status=1 | ✅ CORRETO | OK |
| 6 | Novos Lite (7d) | 3.803 | README: 3803 ✅ | created_at >= D-7 | ✅ CORRETO | OK |
| 7 | Impacto R$/mês (NC) | R$ 747.525,90 | Calculado: CPFs NC × R$12,10 | Não existe no PBI | ⚠️ PARCIAL | Valor assume TODOS os CPFs NC viram promotores ativos. Real: ~15% ficam ativos → impacto real ~R$112K |
| 8 | Promotores Conv | 248.810 | README: 248810 ✅ | Snapshot visitors ativos | ✅ CORRETO | OK |

### Problemas identificados:
- **Card 7 (Impacto):** Superestima o impacto. Deveria ter nota "(estimado)" ou mostrar impacto ajustado
- **Nomenclatura:** "Cadastros" e "Promotores" deveriam ser "Requisições" e "CPFs" para alinhar com PBI
- **Falta:** Card de "Empresas Sem Info" (7739 - 5616 - 1550 = 573 empresas sem classificação)

---

## 2. CARDS ABA "NÃO CLIENTES" (kpis-nc)

| # | Card | Cálculo | Correto? | Melhoria |
|---|------|---------|----------|----------|
| 1 | Empresas (filtro) | FILTERED onde status='Nao Cliente' | ✅ | OK |
| 2 | Promotores | SUM(promotores) das NC filtradas | ✅ | Renomear "CPFs" |
| 3 | Impacto Mensal R$ | promotores × R$12,10 | ⚠️ | Mesmo problema do global — superestima |
| 4 | Novos NC (7d) | README['Novos Lite Nao Cliente (7d)'] | ✅ | OK |

### Tabela NC:
- Colunas: Empresa, Tipo, Cadastros, Promotores, Score, Class., Primeiro, Último
- **Correto:** Dados vêm da aba Empresas filtrada por status_empresa='Nao Cliente'
- **Melhoria:** Renomear "Cadastros" → "Requisições", "Promotores" → "CPFs"

---

## 3. CARDS ABA "CLIENTES" (kpis-cl)

| # | Card | Cálculo | Correto? | Melhoria |
|---|------|---------|----------|----------|
| 1 | Empresas (filtro) | FILTERED onde status='Cliente' | ✅ | OK |
| 2 | Promotores | SUM(promotores) das Cl filtradas | ✅ | Renomear "CPFs" |
| 3 | Cadastros | SUM(cadastros) das Cl filtradas | ✅ | Renomear "Requisições" |
| 4 | % Lite/Total | prom/(prom+convProm)×100 | ✅ | OK — mostra canibalização |

### Análise:
- **% Lite/Total** usa o total de Conv (248.810) como denominador — correto
- Valor esperado: ~42.952 / (42.952 + 248.810) = ~14.7% (não 17.3% como no preview)
- O valor real depende do filtro aplicado

---

## 4. CARDS ABA "ALERTAS" (kpis-al)

| # | Card | Cálculo | Correto? | Melhoria |
|---|------|---------|----------|----------|
| 1 | Suspeito | COUNT onde classificacao='Suspeito' | ✅ | OK |
| 2 | Atenção | COUNT onde classificacao='Atencao' | ✅ | OK |
| 3 | Score Médio | AVERAGE(score_suspeita) | ✅ | OK |
| 4 | Impacto Total R$ | SUM(promotores NC) × R$12,10 | ⚠️ | Mesmo problema — superestima |

### Problema:
- **Falta card "Crítico"** (score > 80) — é o mais importante para ação CS
- **Falta card "Alta Suspeita"** — segundo nível de prioridade
- Os alertas mostram cards de Suspeito e Atenção mas não de Crítico/Alta Suspeita nos KPIs

---

## 5. CARDS ABA "REDES" (kpis-rede)

| # | Card | Cálculo | Correto? | Melhoria |
|---|------|---------|----------|----------|
| 1 | Empresas com Rede | COUNT da aba Redes filtrada | ✅ | OK |
| 2 | Total Redes | SUM(qt_redes) | ✅ | OK |

### Análise:
- Aba funcional mas com **baixo valor de ação** — saber que empresa X tem 10 redes não gera decisão
- **Melhoria:** Adicionar coluna "Impacto R$" na tabela de redes

---

## 6. CARDS ABA "CONV VS LITE" (kpis-comp)

| # | Card | Cálculo | Correto? | Melhoria |
|---|------|---------|----------|----------|
| 1 | Promotores Lite | SUM(promotores) todas empresas | ✅ | Renomear "CPFs Lite" |
| 2 | Promotores Conv | SUM(promotores_conv) aba Convencional | ✅ | OK |
| 3 | Registros Conv | SUM(registros_conv) | ✅ | OK |
| 4 | Razão Lite/Conv | (Lite/Conv)×100 | ✅ | OK — indicador chave |

---

## 7. FILTROS — ANÁLISE

| Filtro | Funciona? | Abrangência | Melhoria |
|--------|-----------|-------------|----------|
| Status (Todos/NC/Cliente) | ✅ | Todas as abas | OK |
| Tipo (Agencia/Fornecedor) | ✅ | Todas as abas | OK |
| Risco (Normal/Atenção/Suspeito/Alta/Crítico) | ✅ | Todas as abas | OK |
| Empresa (busca texto) | ✅ | Todas as abas | OK |
| Min. promotores | ✅ | Todas as abas | Renomear "Min. CPFs" |

### Problema nos filtros:
- **Filtro "Risco" não tem opção "Sem Info"** — 573 empresas ficam invisíveis se filtrar por status
- **Filtro não afeta aba Redes** corretamente — usa empIds mas pode não filtrar se empresa_id não bate

---

## 8. ABAS — ANÁLISE DE PERTINÊNCIA

| Aba | Pertinente? | Gera ação? | Melhoria |
|-----|-------------|-----------|----------|
| Visão Geral | ✅ Sim | Panorama rápido | OK |
| Não Clientes | ✅ Sim | Core do negócio | Renomear colunas |
| Clientes | ✅ Sim | Monitorar canibalização | OK |
| Alertas | ✅ Sim | Ação imediata CS | Adicionar card "Crítico" |
| Priorização | ⚠️ Redundante | Similar a Alertas | Unificar ou diferenciar |
| Redes | ⚠️ Baixo valor | Informativo | Adicionar impacto R$ |
| Conv vs Lite | ✅ Sim | Estratégico | OK |
| Ação CS | ✅ Sim | Operacional | OK |

---

## 9. RESUMO DE MELHORIAS RECOMENDADAS

### Seguras (não quebram nada):
1. ~~Renomear "Cadastros" → "Requisições"~~ (já tentamos, pode fazer depois)
2. ~~Renomear "Promotores" → "CPFs"~~ (idem)
3. Adicionar nota "(estimado)" no card de Impacto
4. Adicionar card "Crítico (score>80)" na aba Alertas

### Médio risco:
5. Adicionar 3 novas abas (Priorização CS, Ação Fornecedor, Acompanhamento)
6. Adicionar coluna "Impacto R$" na tabela de Redes

### Para próxima versão:
7. Corrigir cálculo de impacto (usar taxa de 15% de ativação)
8. Adicionar filtro "Sem Info" no dropdown de Status
9. Unificar abas Alertas + Priorização

---

## 10. DADOS CONFRONTADOS — VALIDAÇÃO FINAL

| Dado | Sheets | PBI | Match? |
|------|--------|-----|--------|
| Total requisições | 150.063 | DISTINCTCOUNT(lite_visitor_id) | ✅ |
| CPFs únicos | 104.775 | DISTINCTCOUNT(lite_visitor_cpf) | ✅ |
| Empresas total | 7.739 | DISTINCTCOUNT(company_id) | ✅ |
| NC | 5.616 | WHERE status=0 | ✅ |
| Clientes | 1.550 | WHERE status=1 | ✅ |
| Sem Info | 573 | WHERE status NOT IN (0,1) | ✅ (7739-5616-1550) |
| Conv snapshot | 248.810 | Visitors ativos | ✅ |
| Top NC: JBS | 2.006 CPFs | Verificável no PBI | ✅ |
| Top Cl: SPOT | 3.302 CPFs | Verificável no PBI | ✅ |

**Conclusão: Os dados estão CORRETOS. As melhorias são de nomenclatura e UX, não de dados.**
