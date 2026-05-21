# 📊 Análise Completa — Dashboard Cadastro Lite (Monitoramento Mob2Con)

**Data:** 18/05/2026  
**Projeto:** Apps Script + Google Sheets → HTML Dashboard  
**Script ID:** `1vgjMumNtjp2EkSoXa8gV_SizQjhljskv8hrRcDOZEGcEI-ZUh78t6N20`  
**Base de dados:** Sheets `17wacDgqjMwO3lOknuk6TtKfTwamB1qz-MpGGuwM7n_4`  
**Base bruta:** Sheets `1o5_pT2aPNO2Cjv0orMjIfINbrerw_IqGl1az944IwrM`  
**URL publicada:** https://script.google.com/a/macros/mob2con.com.br/s/AKfycbziwj_n575Ez7m16SCWsjd_CvWRt4Yey5DBgCHVRwPccYYlZC0UZTUcaVwsQzPSnFIh/exec

---

## 1. RESUMO EXECUTIVO

| KPI | Valor |
|-----|-------|
| Total Cadastros Lite | 150.063 |
| Promotores Únicos Lite | 104.775 |
| Empresas com Lite | 7.739 |
| Empresas Não Cliente | 5.616 |
| Empresas Cliente | 1.550 |
| Novos Lite (7d) | 3.803 |
| Impacto Receita Mensal | R$ 747.525,90 |
| Promotores Convencional (snapshot) | 248.810 |

**Objetivo do negócio:** Identificar e mensurar desvios de cadastros convencionais → Lite, entendendo impacto em receita, comportamento das contas e possíveis gaps operacionais/comerciais.

---

## 2. ESTRUTURA ATUAL DAS ABAS

| # | Aba | Propósito | Faz sentido? | Observação |
|---|-----|-----------|:---:|------------|
| 1 | **Visão Geral Cadastros** | KPIs globais + 4 gráficos | ✅ | Boa porta de entrada |
| 2 | **Base Não Clientes** | Tabela filtrada NC + KPIs | ✅ | Core do negócio — empresas que usam Lite sem pagar |
| 3 | **Base Clientes** | Tabela filtrada Clientes | ⚠️ | Útil mas falta contexto: por que um cliente usa Lite se já paga? |
| 4 | **Alertas de Desvio** | Cards de alerta por score | ✅ | Bom para CS, mas falta ação/botão de follow-up |
| 5 | **Priorização Comercial** | Ranking por score | ✅ | Essencial para vendas |
| 6 | **Por Rede** | Empresas × redes | ⚠️ | Mostra apenas `empresa_id` sem nome — ilegível |
| 7 | **Comparativo Conv** | Lite vs Convencional | ✅ | Atende ao objetivo principal do projeto |

### Recomendações de abas:

1. **Aba "Clientes"** — Adicionar coluna de "plano atual" e "% Lite vs Conv" para mostrar se o cliente está migrando promotores do convencional para Lite (desvio de receita).
2. **Aba "Por Rede"** — Precisa urgentemente do nome da empresa (hoje só mostra ID numérico). Sem isso, a aba é inútil para o usuário final.
3. **Nova aba sugerida: "Linha do Tempo"** — Gráfico de linha comparando quantidade de cadastros convencionais vs Lite mês a mês (conforme briefing do cliente).
4. **Nova aba sugerida: "Ação CS"** — Visão por fornecedor com histórico, reversões Lite→Regular, reincidência e efetividade.

---

## 3. PROBLEMAS DE TOOLTIPS (INEXISTENTES)

Nenhum card de KPI possui tooltip explicativo. O usuário não sabe:

| Card | O que falta explicar |
|------|---------------------|
| Total Cadastros Lite | "Soma de todos os registros com origem_cadastro = 'lite' desde 01/10/2025" |
| Promotores Únicos Lite | "Contagem distinta de id_promotor com pelo menos 1 cadastro Lite" |
| Impacto R$/mês (NC) | "Promotores de Não Clientes × R$12,10 (ticket médio estimado)" |
| Novos Lite (7d) | "Cadastros criados nos últimos 7 dias" |
| Score Suspeita | "Fórmula: NC +25, >200 prom +25, >50 +15, >10 +5, Agência +5" |
| Classificação | "Normal ≤20, Atenção ≤40, Suspeito ≤60, Alta Suspeita ≤80, Crítico >80" |

### Implementação sugerida:

```html
<!-- Adicionar atributo title nos cards -->
<div class="kpi" title="Soma de registros com origem_cadastro='lite' desde 01/10/2025">
  <span>Total Cadastros Lite</span>
  <strong>150.063</strong>
</div>
```

Ou melhor, usar tooltip customizado com CSS:

```css
.kpi { position: relative; cursor: help; }
.kpi::after {
  content: attr(data-tip);
  position: absolute; bottom: 100%; left: 50%;
  transform: translateX(-50%); padding: 6px 10px;
  background: #1f2937; color: #fff; font-size: 11px;
  border-radius: 6px; white-space: nowrap;
  opacity: 0; pointer-events: none; transition: opacity .2s;
}
.kpi:hover::after { opacity: 1; }
```

---

## 4. CARDS VAZIOS / PROBLEMAS IDENTIFICADOS

| Problema | Onde | Impacto | Solução |
|----------|------|---------|---------|
| Aba "Redes" mostra `empresa_id` sem nome | Tabela `trede` | Usuário não identifica a empresa | JOIN com tabela Empresas no backend |
| KPIs de "Clientes" não mostram % de desvio | `kpis-cl` | Não responde "quanto o cliente está desviando?" | Adicionar KPI "% Lite/Total" |
| Gráfico "Lite vs Conv – Acumulado" usa barras com 1 categoria | `ch-comp-acum` | Gráfico de barras com 1 barra é inútil visualmente | Trocar por gauge ou usar barras empilhadas por mês |
| Filtro "Min. promotores" começa em 0 | Filtros | Não filtra nada por padrão | Manter, mas adicionar preset "Top 50" |
| Sem indicador de tendência nos KPIs | Todos os cards | Não mostra se está subindo ou descendo | Adicionar seta ↑↓ com % vs período anterior |
| Sem data de última atualização visível | Header | Usuário não sabe se dados são frescos | Já existe no código mas pode ficar mais destacado |
| Tabela Convencional não tem coluna `dt_referencia` formatada | `tconv` | Data aparece como ISO string | Formatar para dd/mm/yyyy |
| Alertas não têm botão de ação | `page-alertas` | CS não pode marcar como "em tratamento" | Adicionar status/ação (requer backend) |

---

## 5. MELHORIAS DE UX/UI PRIORITÁRIAS

### 5.1 Tooltips em todos os KPIs (ALTA PRIORIDADE)

Cada `kpiHtml()` deve receber um campo `tip` e renderizar `data-tip`:

```javascript
function kpiHtml(id, items) {
  document.getElementById(id).innerHTML = items.map(i=>`
    <div class="kpi" ${i.tip ? `data-tip="${i.tip}" title="${i.tip}"` : ''}>
      <span>${i.l}</span>
      <strong>${i.v}</strong>
      ${i.s?`<small>${i.s}</small>`:''}
    </div>`).join('');
}
```

### 5.2 Resolver aba "Redes" — mostrar nome da empresa

No backend (`Code.gs`), alterar `getRedes()` para fazer JOIN:

```javascript
function getRedes() {
  const ss = SpreadsheetApp.openById(SHEETS_ID);
  const redes = _toObjects('Redes');
  const empresas = _toObjects('Empresas');
  const empMap = {};
  empresas.forEach(e => { empMap[String(e.empresa_id)] = e.empresa; });
  redes.forEach(r => { r.empresa_nome = empMap[String(r.empresa_id)] || 'Desconhecida'; });
  return redes;
}
```

E no frontend, exibir `r.empresa_nome` na tabela.

### 5.3 Gráfico de linha Conv vs Lite (PEDIDO DO CLIENTE)

O briefing pede explicitamente: "criar um gráfico de linha comparando a quantidade de cadastros convencionais com a de cadastros lite". O gráfico `ch-litevconv` já faz isso com promotores, mas falta um com **quantidade de cadastros** (não promotores).

Sugestão: adicionar na aba "Comparativo Conv" um novo gráfico:

```javascript
// Cadastros Lite por mês
const liteCad = mAll.map(m => DATA.mensal.filter(r=>String(r.mes)===m)
  .reduce((s,r)=>s+(+r.cadastros||0),0));
// Registros Conv por mês  
const convCad = mAll.map(m => DATA.convMensal.filter(r=>String(r.mes)===m)
  .reduce((s,r)=>s+(+r.registros_conv||0),0));
```

### 5.4 Indicadores de tendência nos KPIs

Adicionar seta e % de variação comparando mês atual vs anterior:

```javascript
function trendIcon(current, previous) {
  if (!previous) return '';
  const pct = ((current - previous) / previous * 100).toFixed(1);
  const icon = pct > 0 ? '↑' : pct < 0 ? '↓' : '→';
  const color = pct > 0 ? 'var(--red)' : 'var(--green)';
  return `<small style="color:${color}">${icon} ${Math.abs(pct)}%</small>`;
}
```

### 5.5 Fonte tipográfica

O CSS usa `'Segoe UI', Arial, sans-serif` — deveria usar **Raleway** conforme brand guidelines Mob2Con:

```css
body { font-family: 'Raleway', 'Segoe UI', sans-serif; }
```

Adicionar no `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;700;900&display=swap" rel="stylesheet">
```

---

## 6. CAMPOS ADICIONAIS SUGERIDOS (BASE BRUTA DISPONÍVEL)

A base bruta (`1o5_pT2aPNO2Cjv0orMjIfINbrerw_IqGl1az944IwrM`) tem campos que NÃO estão sendo usados no dashboard:

| Campo disponível | Uso sugerido |
|-----------------|--------------|
| `status_promotor` | Filtro: Ativo vs Descartado |
| `tipo_base` | Identificar se é "Cliente Ativo" ou outro |
| `status_cadastro` | approved/expired/pending — funil de conversão |
| `motivo_reprovacao` | Análise de qualidade do cadastro |
| `data_descarte` | Calcular "dias até descarte" |
| `qtd_tentativas_cadastro` | Indicador de fricção no processo |
| `qtd_reprovacoes` | Qualidade dos documentos |
| `usuario_responsavel_cadastro` | Rastreabilidade |
| `empresa_responsavel_cadastro` | Quem está cadastrando (pode ser diferente da empresa) |
| `data_entrada_empresa` / `data_saida_empresa` | Histórico de migração |

### Campos calculados sugeridos (para nova view no Sheets):

| Campo | Fórmula |
|-------|---------|
| `tipo_anterior` | Inferir do histórico (se teve cadastro convencional antes) |
| `flag_migracao` | 1 se empresa tinha conv e agora tem lite |
| `flag_reversao` | 1 se voltou de lite para conv |
| `dias_desde_migracao` | DATEDIFF(data_criacao_registro, hoje) |
| `reincidencia` | COUNT de tentativas > 1 |
| `impacto_estimado_rs` | promotores × R$12,10 |

---

## 7. AUTOMAÇÃO SUGERIDA

| Item | Status atual | Recomendação |
|------|-------------|--------------|
| Atualização dos dados | Manual (script Python) | Agendar `sync_redshift_to_sheets.py` via cron/Task Scheduler diário |
| Views no Redshift | Não mencionadas | Criar views: `vw_desvios_ativos`, `vw_novos_desvios_7d`, `vw_reincidencia` |
| Alertas por email | Não existe | Apps Script trigger diário que envia email se novos críticos |
| Histórico de ações CS | Não existe | Nova aba "Ações" no Sheets para registrar follow-ups |

---

## 8. SCORE DE SUSPEITA — ANÁLISE DA FÓRMULA

Fórmula atual:
- Não Cliente: +25
- \>200 promotores: +25
- \>50 promotores: +15
- \>10 promotores: +5
- Agência: +5
- Max: 100

**Problemas identificados:**
1. Não considera **velocidade de crescimento** (empresa que ganhou 500 promotores em 1 semana é mais suspeita que uma com 500 em 6 meses)
2. Não considera **reincidência** (empresa que já foi alertada e continua)
3. Não diferencia **Fornecedor** de **Agência** adequadamente (fornecedor direto com muitos Lite é mais grave)
4. Falta peso para **concentração em rede** (empresa com Lite em 10+ redes é mais suspeita)

**Sugestão de score v2:**
- Não Cliente: +25
- \>200 promotores: +25
- \>50 promotores: +15
- \>10 promotores: +5
- Agência: +5
- **Crescimento >50% no mês: +15** (novo)
- **Reincidência (já alertado): +10** (novo)
- **>5 redes: +5** (novo)
- **Fornecedor direto: +10** (novo, mais grave que agência)

---

## 9. RESUMO DE AÇÕES IMEDIATAS

| # | Ação | Esforço | Impacto |
|---|------|---------|---------|
| 1 | Adicionar tooltips em todos os KPIs | Baixo (1h) | Alto — usabilidade |
| 2 | Corrigir aba Redes (mostrar nome empresa) | Baixo (30min) | Alto — aba inutilizável hoje |
| 3 | Adicionar fonte Raleway | Baixo (5min) | Médio — brand compliance |
| 4 | Gráfico de linha Cadastros Conv vs Lite | Médio (2h) | Alto — pedido explícito do cliente |
| 5 | Indicadores de tendência (↑↓) nos KPIs | Médio (2h) | Alto — contexto temporal |
| 6 | Melhorar gráfico "Acumulado" (trocar barras) | Baixo (30min) | Médio — visual pobre hoje |
| 7 | Adicionar filtro por status_cadastro | Médio (1h) | Médio — funil de conversão |
| 8 | Nova aba "Ação CS" com histórico | Alto (4h) | Alto — operacional |
| 9 | Score v2 com velocidade e reincidência | Alto (3h) | Alto — precisão dos alertas |
| 10 | Automação diária de atualização | Médio (2h) | Alto — dados sempre frescos |

---

## 10. CONCLUSÃO

O dashboard está **bem estruturado** para um MVP — as 7 abas cobrem os principais ângulos do problema. Os pontos críticos são:

1. **Falta de tooltips** — o usuário de CS/Comercial não entende as métricas sem contexto
2. **Aba Redes ilegível** — mostra ID numérico sem nome
3. **Gráfico comparativo Conv vs Lite** precisa ser de linha temporal (pedido explícito)
4. **Score de suspeita simplista** — não captura velocidade nem reincidência
5. **Sem ações/follow-up** — dashboard é read-only, CS precisa registrar ações

A base de dados bruta tem campos ricos (status_cadastro, tentativas, reprovações, datas de descarte) que não estão sendo explorados e podem alimentar análises muito mais profundas.
