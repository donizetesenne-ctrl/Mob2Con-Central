# Mob2Con — Guia de Padrões Visuais (Atualizado)

## Identidade Visual

**Marca:** Mob2Con  
**Produto principal:** Quick Suite / Power BI Dashboards  
**Atualizado:** 2026-05 (migração completa Segoe UI → Raleway, #0078D4 → #F46901)

---

## 🎨 Paleta de Cores Oficial

| Nome | HEX | Uso |
|------|-----|-----|
| **Laranja Mob2Con** | `#F46901` | Cor principal — headers, KPIs, destaques, gauges |
| **Grafite** | `#434343` | Títulos, cabeçalhos de tabela, bordas |
| **Preto** | `#111111` | Texto em alto contraste, valores de KPI |
| **Azul MobConnect** | `#4285F4` | **EXCLUSIVO** — só usar em relatórios sobre MobConnect |
| **Roxo** | `#6F05D4` | Acento, elementos secundários |
| **Cinza médio** | `#605E5C` | Texto secundário, labels, eixos |
| **Cinza claro** | `#F3F2F1` | Alternativo de fundo neutro |
| **Branco** | `#FFFFFF` | Fundo de visuais, cards |
| **Verde Sucesso** | `#107C41` | Indicadores positivos |
| **Vermelho Alerta** | `#C00000` | Indicadores negativos, ruptura |
| **Amarelo Aviso** | `#FFC107` | Avisos, atenção |

### ⚠️ Regras críticas de cor

> ❌ **NUNCA** usar `#0078D4` (Microsoft blue) — este padrão foi completamente removido
> ❌ **NUNCA** usar `#4285F4` fora de contextos MobConnect
> ✅ O **Laranja `#F46901`** é sempre a cor primária de destaque

### Regras de uso de cor
- Máximo de 5 cores diferentes por página
- Cor semântica: verde = bom, vermelho = ruim, amarelo = atenção
- Nunca usar cores vibrantes no fundo — reservar para destaques
- Contraste mínimo 4.5:1 entre texto e fundo (WCAG AA)

---

## 🔤 Tipografia

| Elemento | Fonte | Peso | Tamanho | Cor |
|----------|-------|------|---------|-----|
| **Título da página** | Raleway | Black (900) | 20pt | `#111111` |
| **Título de visual** | Raleway | Bold (700) | 14pt | `#434343` |
| **Rótulos / eixos** | Raleway | Regular (400) | 9-10pt | `#605E5C` |
| **Valores de KPI** | Raleway | Black (900) | 28pt | `#111111` |
| **Subtítulos** | Raleway | Bold (700) | 12pt | `#434343` |

### ⚠️ Regra tipográfica crítica

> ❌ **NUNCA** usar `Segoe UI`, `Arial`, ou qualquer outra fonte
> ✅ **Sempre Raleway** — se não estiver instalada, instalar antes de qualquer ajuste

- Download: https://fonts.google.com/specimen/Raleway
- Pesos necessários: 400 (Regular), 700 (Bold), 900 (Black)

---

## Conceito de Layout em Z (Z-Pattern)

O padrão Z descreve como o olho humano percorre um dashboard:

```
[1] TOPO ESQUERDO ────────────────► [2] TOPO DIREITO
                                              │
                                    (diagonal)│
                                              ▼
[3] BASE ESQUERDA ────────────────► [4] BASE DIREITA
```

### Como aplicar no Power BI

| Zona | Posição | O que colocar |
|------|---------|---------------|
| Zona 1 — Topo Esquerdo | x:0, y:0 | Logo, título da página, KPI mais importante |
| Zona 2 — Topo Direito | x:alto, y:0 | Filtros, slicers, data de atualização |
| Zona 3 — Base Esquerda | x:0, y:alto | Gráfico principal, tendência |
| Zona 4 — Base Direita | x:alto, y:alto | Detalhes, tabelas, drill-down |

### Regras do Z-Pattern

1. **KPI principal sempre no topo esquerdo** — é o primeiro ponto de atenção
2. **Informações de contexto no topo direito** — filtros e período
3. **Gráficos de tendência na diagonal** — guiam o olho naturalmente
4. **Detalhes e tabelas na base** — consultados por quem quer aprofundar
5. **Nunca coloque informação crítica no centro** — o olho passa por ali rapidamente

---

## Hierarquia Visual

```
NÍVEL 1 — PRIMÁRIO (maior destaque)
  └── KPIs principais, números grandes, títulos de página

NÍVEL 2 — SECUNDÁRIO (destaque médio)
  └── Gráficos principais, subtítulos, variações percentuais

NÍVEL 3 — TERCIÁRIO (destaque baixo)
  └── Tabelas, labels, legendas, notas de rodapé
```

### Como criar hierarquia no Power BI
- **Tamanho:** KPI cards maiores que gráficos, gráficos maiores que tabelas
- **Cor:** Use Laranja `#F46901` para o elemento mais importante da página
- **Contraste:** Fundo `#F3F6FA` ou `#FFFFFF` com texto `#111111` ou `#434343`
- **Espaço em branco:** Mais espaço ao redor = mais importância
- **Posição:** Topo esquerdo = mais importante (regra do Z)

---

## 📐 Grid e Espaçamento (Sistema de 8 pontos)

Todo espaçamento deve ser múltiplo de 8px para consistência visual.

- **Canvas Power BI:** 1280 x 720px (Widescreen 16:9 padrão)
- **Margem de página:** 16px em todos os lados
- **Gap entre visuais:** 16px (padrão), 8px (compacto)
- **Padding interno de cards:** 8px
- **Altura de header:** 64px
- **Altura de KPI card:** 120px ou 160px
- **Largura de slicer lateral:** 200px ou 240px

---

## Estrutura de Página Padrão (Z-Pattern aplicado)

```
┌─────────────────────────────────────────────────────────┐
│  [LOGO + TÍTULO]              [FILTROS / SLICERS]        │  y: 0–64px
├─────────────────────────────────────────────────────────┤
│  [KPI 1]    [KPI 2]    [KPI 3]    [KPI 4]               │  y: 80–240px
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [GRÁFICO PRINCIPAL]          [GRÁFICO SECUNDÁRIO]       │  y: 256–560px
│                                                          │
├─────────────────────────────────────────────────────────┤
│  [TABELA / DETALHES]          [GRÁFICO COMPLEMENTAR]     │  y: 576–720px
└─────────────────────────────────────────────────────────┘
   x: 0–640px                   x: 656–1280px
```

---

## Cores por Contexto de Fundo

| Contexto | Background | Outspace |
|----------|-----------|---------|
| **Padrão Mob2Con** | `#F3F6FA` | `#E2E8F0` |
| **Cards / Visuais** | `#FFFFFF` | — |
| **Alternativo neutro** | `#F8F8F8` | `#F8F8F8` |

---

## Temas Power BI Disponíveis

| Arquivo | Contexto | Cor primária |
|---------|---------|-------------|
| `Mob2Con-Brand-Theme.json` | **Principal** — todos os relatórios Mob2Con | `#F46901` |
| `Mob2Con-Theme.json` | Alternativo corporativo | `#F46901` |
| `MobConnect-Theme.json` | Relatórios sobre MobConnect | `#4285F4` |
| `ReposicaoGarantida-Theme.json` | Reposição Garantida / Combate à Ruptura | `#F46901` |

---

## Visuais Recomendados por Tipo de Dado

- **KPI simples:** Card visual — valor grande, variação percentual abaixo
- **Tendência temporal:** Line chart — cor `#F46901`, linha 3px
- **Comparação entre categorias:** Bar/Column chart — `#F46901` como cor principal
- **Parte do todo:** Donut chart — paleta Mob2Con, máximo 5 fatias
- **Correlação:** Scatter chart — pontos laranja
- **Detalhe operacional:** Matrix — cabeçalho `#434343`, linhas alternadas
- **Filtro de período:** Slicer de data — estilo dropdown ou between
- **Performance/Meta:** Gauge — fill `#F46901`, target `#434343`

---

## Checklist de Validação Visual

- [ ] Usa **Raleway** (não Segoe UI, Arial, etc.)
- [ ] Laranja `#F46901` como destaque principal (ou `#4285F4` se MobConnect)
- [ ] Textos longos truncados (títulos curtos, sem "...")
- [ ] Contraste adequado (texto escuro em fundo claro)
- [ ] Bordas/separadores em `#E0E0E0` ou `#E2E8F0` (não preto puro)
- [ ] Espaçamento consistente entre visuais (grid 16px)
- [ ] Fundo da página: `#F3F6FA` (ou `#F8F8F8`)
- [ ] KPI principal no topo esquerdo (Z-pattern)
- [ ] Máximo 5 cores por página

---

## 🔗 Referências

- Brand Guidelines: `01-Brand-Guidelines/Mob2con-brand-guidelines.md`
- Tema principal: `02-Powerbi-Projetos/Mob2Con-Brand-Theme.json`
- Projeto de referência: `02-Powerbi-Projetos/Nordestão Exclusivo dn.pbip`
