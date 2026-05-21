# Changelog — Nordestão Exclusivo dn.pbip
## Migração Brand Guidelines Mob2Con
**Data:** 13/05/2026  
**Autor:** Amazon Quick (assistido por Donizete Senne)  
**Projeto:** `Nordestão Exclusivo dn.pbip`  
**Caminho:** `C:\\Users\\Donizete Senne\\Desktop\\Mob2Con-Central\\02-Powerbi-Projetos\\`  
**Status final:** ✅ 148 arquivos validados · 0 erros

---

## Resumo Executivo

Migração completa do layout e identidade visual do relatório Nordestão Exclusivo para os
padrões da Brand Guidelines Mob2Con. Todas as alterações foram aplicadas diretamente nos
arquivos `.json` do formato PBIR (Power BI Report), sem necessidade de edição manual no
Power BI Desktop — exceto a importação do tema e instalação da fonte Raleway.

---

## Alterações por Categoria

### 1. Canvas — Resolução Atualizada
- **De:** 1280 × 720 px (padrão antigo)
- **Para:** 1600 × 900 px (Profissional Mob2Con)
- **Páginas afetadas:** todas as 6
  - 🏠 Executivo · 📈 Vendas · 🔴 Ruptura · ⚙️ Operação · 🏆 Produtividade · 📦 Estoque
- **Arquivos editados:** `definition/pages/{page}/page.json` (6 arquivos)

---

### 2. Headers — Altura e Largura Corrigidas
- **De:** `height: 52px, width: 1280px`
- **Para:** `height: 64px, width: 1600px`
- **Visuais afetados:** exec_titulo, vnd_titulo, rup_titulo, op_titulo, prod_titulo, est_titulo
- **Justificativa:** Brand standard recomenda mínimo 64px para header desktop

---

### 3. Slicers — Reposicionamento e Espaçamento Uniforme
- **De:** y=56, height=40, largura variável, margem final de 28px
- **Para:** y=72, height=48, width=376px (4 slicers) ou 512px (3 slicers — Estoque)
- **Distribuição:** gap=16px, margem direita=16px em todas as páginas
- **Slicers atualizados:** 21 (4 por página × 5 páginas + 3 na página Estoque)

---

### 4. Fix de Overlap — Página Executivo
- **Problema:** exec_alertas (y=528, h=64) sobrepunha exec_bar_lojas (y=556) em 36px
- **Correção:**
  - Cards de alerta: y=548, height=48
  - Gráficos (bar_lojas, pie_ruptura): y=600, height=120
- **Visuais corrigidos:** 7

---

### 5. Escalonamento Proporcional 1.25×
Todos os visuais foram escalados proporcionalmente para preencher o novo canvas 1600×900.

- **Fator:** 1.25× (uniforme em X, Y, Width e Height)
- **Fórmula:** `new_val = round(original_val × 1.25)`
- **Resultado:** visuais preenchem o canvas sem espaço vazio, sem distorção
- **Visuais atualizados:** 84 (distribuídos pelas 6 páginas)
- **Exemplos:**
  | Visual | Antes | Depois |
  |--------|-------|--------|
  | exec_gauge_saude | x=16, y=208, 412×160 | x=20, y=260, 515×200 |
  | exec_bar_lojas | x=16, y=600, 626×120 | x=20, y=750, 782×150 |
  | vnd_linha_evolucao | x=12, y=304, 788×236 | x=15, y=380, 985×295 |
  | prod_tabela_ranking | x=12, y=208, 766×264 | x=15, y=260, 957×330 |
  | est_donut_problemas | x=786, y=208, 482×264 | x=982, y=260, 602×330 |

---

### 6. Correção de Cores — Azuis Proibidos Eliminados

#### 6a. Headers: #4285F4 → #F46901
O azul MobConnect (#4285F4) estava sendo usado em headers de páginas que **não** são
sobre o produto MobConnect — violação direta das Brand Guidelines.

| Visual corrigido | Página |
|---|---|
| exec_titulo | 🏠 Executivo |
| exec_represent | 🏠 Executivo |
| vnd_titulo | 📈 Vendas |
| vnd_kpi_m1 | 📈 Vendas |
| vnd_kpi_media_loja | 📈 Vendas |
| vnd_kpi_yoy | 📈 Vendas |
| rup_titulo | 🔴 Ruptura |
| op_titulo | ⚙️ Operação |
| prod_titulo | 🏆 Produtividade |
| est_titulo | 📦 Estoque |

#### 6b. Gauges e Cards: #0078D4 → #F46901
O azul Microsoft (#0078D4) é o padrão do Power BI Desktop — explicitamente proibido
pela Brand Mob2Con em qualquer contexto.

| Visual corrigido | Página |
|---|---|
| exec_gauge_saude | 🏠 Executivo |
| exec_gauge_efic_horas | 🏠 Executivo |
| exec_gauge_visitas | 🏠 Executivo |
| exec_gauge_ruptura | 🏠 Executivo |
| exec_gauge_cobertura | 🏠 Executivo |
| exec_gauge_tarefas | 🏠 Executivo |
| vnd_card_evolucao | 📈 Vendas |
| op_gauge_efic | ⚙️ Operação |
| op_gauge_tarefas | ⚙️ Operação |
| op_gauge_visitas | ⚙️ Operação |

**Varredura final:** 113 arquivos verificados — **zero ocorrências** de #4285F4 ou #0078D4.

---

### 7. Fonte Global: Segoe UI → Raleway
- **De:** `'Segoe UI'` (fonte padrão Power BI — proibida pela Brand)
- **Para:** `'Raleway'` (fonte oficial Mob2Con)
- **Escopo:** todos os campos `fontFamily` em todos os visual.json
- **Arquivos alterados:** **113 de 113** (100%) · 0 erros
- **Validação:** 148 arquivos PBIR verificados sem problemas

> ⚠️ **Pré-requisito:** instalar Raleway no sistema antes de abrir o relatório.  
> Download: https://fonts.google.com/specimen/Raleway (pesos 400, 700, 900)

---

### 8. Tema Power BI — Mob2Con Brand Theme
Gerado e salvo na pasta do projeto para importação via Power BI Desktop.

- **Arquivo:** `Mob2Con-Brand-Theme.json`
- **Caminho:** mesma pasta do `.pbip`
- **Cobertura:** 12 tipos de visual (card, multiRowCard, gauge, barChart, columnChart,
  lineChart, donutChart, scatterChart, tableEx, slicer, shape, textbox)
- **dataColors:** #F46901 · #434343 · #6F05D4 · #107C41 · #C00000 · #111111 · #FFA94D · #9B59B6
- **good/neutral/bad:** #107C41 / #F46901 / #C00000
- **Para importar:** Power BI Desktop → Exibição → Temas → Procurar temas → selecionar este arquivo

---

## Paleta Final Aplicada

| Elemento | Cor | Hex |
|---|---|---|
| Header background | 🟠 Laranja Mob2Con | `#F46901` |
| Gauge needle / destaque | 🟠 Laranja Mob2Con | `#F46901` |
| Valor KPI | ⚫ Preto | `#111111` |
| Título de visual | 🩶 Grafite | `#434343` |
| Label / eixo | 🩶 Grafite médio | `#605E5C` |
| Fundo card | ⬜ Branco | `#FFFFFF` |
| Borda KPI | 🔵 Azul claro | `#CBD5E1` |
| Fundo página | 🔵 Azul gelo | `#F3F6FA` |
| Indicador positivo | 🟢 Verde | `#107C41` |
| Indicador alerta | 🔴 Vermelho | `#C00000` |

---

## Validação Final

```
Arquivos PBIR verificados:  148
Problemas encontrados:        0
Azuis proibidos restantes:    0  (#0078D4 e #4285F4)
Ocorrências de 'Segoe UI':   0
```

---

## Arquivos Gerados / Modificados

| Arquivo | Tipo | Operação |
|---|---|---|
| `*/page.json` (×6) | Página | Canvas 1600×900 |
| `*/visuals/*/visual.json` (×113) | Visual | Fonte, cores, layout |
| `Mob2Con-Brand-Theme.json` | Tema PBI | Criado |

---

## Pendências (aplicar no Power BI Desktop)

- [ ] Instalar fonte **Raleway** (pesos 400, 700, 900) — [link](https://fonts.google.com/specimen/Raleway)
- [ ] Importar tema **Mob2Con-Brand-Theme.json** (Exibição → Temas → Procurar temas)
- [ ] Revisar visualmente os 6 dashboards após aplicação do tema
- [ ] (Opcional) Adicionar logo Mob2Con como imagem no header de cada página

---

*Gerado automaticamente por Amazon Quick em 13/05/2026 às 08:53 (BRT)*
