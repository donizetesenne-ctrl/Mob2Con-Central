# Mob2Con - Base de Templates de Layout Power BI

## Canvas Padrao

| Tipo | Largura | Altura | Uso |
|------|---------|--------|-----|
| Widescreen 16:9 (padrao novo) | 1920px | 1080px | Dashboards modernos, telas grandes |
| Widescreen 16:9 (padrao antigo) | 1280px | 720px | Compatibilidade, telas menores |
| Profissional Mob2Con | 1600px | 900px | Recomendado para Quick Suite |
| Mobile | 320px | 568px | Relatorios para celular |
| Impressao A4 | 794px | 1123px | Exportacao PDF |

> **Referencia Microsoft:** Novas paginas criadas no Power BI Desktop usam 1920x1080 por padrao.
> Fonte: [learn.microsoft.com](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-reports-visual-defaults)

---

## TEMPLATE 1 — Dashboard Executivo (1600x900)

Ideal para C-suite, board reporting, KPIs de alto nivel.
Segue o Z-Pattern: logo/titulo topo esquerdo, filtros topo direito, KPIs linha do meio, graficos embaixo.

```
Canvas: 1600 x 900px

┌──────────────────────────────────────────────────────────────────┐
│ HEADER (y:0, h:64)                                               │
│  [Logo+Titulo x:16]              [Periodo/Filtro x:1200]         │
├──────────────────────────────────────────────────────────────────┤
│ KPIs (y:80, h:140)                                               │
│  [KPI1 x:16]  [KPI2 x:400]  [KPI3 x:784]  [KPI4 x:1168]        │
├──────────────────────────────────────────────────────────────────┤
│ GRAFICOS PRINCIPAIS (y:240, h:380)                               │
│  [Grafico Principal x:16, w:960]   [Grafico Sec. x:992, w:592]  │
├──────────────────────────────────────────────────────────────────┤
│ BASE (y:640, h:244)                                              │
│  [Tabela/Matrix x:16, w:960]       [Grafico Comp. x:992, w:592] │
└──────────────────────────────────────────────────────────────────┘
```

### Coordenadas exatas — Template Executivo 1600x900

| Visual | x | y | width | height | Descricao |
|--------|---|---|-------|--------|-----------|
| header_bg | 0 | 0 | 1600 | 64 | Fundo do header (retangulo azul #0078D4) |
| logo_titulo | 16 | 8 | 400 | 48 | Logo + titulo da pagina |
| filtro_periodo | 1200 | 12 | 384 | 40 | Slicer de periodo/data |
| kpi_1 | 16 | 80 | 368 | 140 | KPI principal (metrica mais importante) |
| kpi_2 | 400 | 80 | 368 | 140 | KPI secundario |
| kpi_3 | 784 | 80 | 368 | 140 | KPI terciario |
| kpi_4 | 1168 | 80 | 416 | 140 | KPI quaternario |
| grafico_principal | 16 | 240 | 960 | 380 | Grafico de tendencia ou barras principal |
| grafico_secundario | 992 | 240 | 592 | 380 | Grafico de pizza, donut ou barras |
| tabela_detalhe | 16 | 640 | 960 | 244 | Matrix ou tabela de detalhes |
| grafico_complementar | 992 | 640 | 592 | 244 | Grafico complementar ou KPI adicional |

---

## TEMPLATE 2 — Dashboard Operacional (1280x720)

Ideal para monitoramento diario, equipes operacionais, muitos filtros.

```
Canvas: 1280 x 720px

┌──────────────────────────────────────────────────────┐
│ HEADER (y:0, h:56)                                   │
│  [Logo x:16]        [Titulo x:200]   [Data x:1000]   │
├────────────┬─────────────────────────────────────────┤
│ FILTROS    │ KPIs (y:72, h:120)                      │
│ (x:0,w:200)│  [K1 x:216] [K2 x:476] [K3 x:736]      │
│            ├─────────────────────────────────────────┤
│ (y:72      │ GRAFICO PRINCIPAL (y:208, h:280)         │
│  h:592)    │  [Line/Bar Chart x:216, w:1048]          │
│            ├─────────────────────────────────────────┤
│            │ BASE (y:504, h:200)                      │
│            │  [Tabela x:216, w:512] [Graf x:744,w:520]│
└────────────┴─────────────────────────────────────────┘
```

### Coordenadas exatas — Template Operacional 1280x720

| Visual | x | y | width | height | Descricao |
|--------|---|---|-------|--------|-----------|
| header_bg | 0 | 0 | 1280 | 56 | Fundo header azul |
| logo | 16 | 8 | 160 | 40 | Logo Mob2Con |
| titulo_pagina | 200 | 12 | 600 | 32 | Titulo da pagina |
| data_atualizacao | 1000 | 16 | 264 | 24 | Ultima atualizacao |
| painel_filtros | 0 | 56 | 200 | 664 | Painel lateral de filtros (fundo cinza) |
| slicer_1 | 8 | 72 | 184 | 80 | Filtro 1 (ex: regiao) |
| slicer_2 | 8 | 168 | 184 | 80 | Filtro 2 (ex: produto) |
| slicer_3 | 8 | 264 | 184 | 80 | Filtro 3 (ex: vendedor) |
| kpi_1 | 216 | 72 | 240 | 120 | KPI 1 |
| kpi_2 | 472 | 72 | 240 | 120 | KPI 2 |
| kpi_3 | 728 | 72 | 240 | 120 | KPI 3 |
| kpi_4 | 984 | 72 | 280 | 120 | KPI 4 |
| grafico_principal | 216 | 208 | 1048 | 280 | Grafico principal (linha ou barra) |
| tabela | 216 | 504 | 512 | 200 | Tabela de detalhes |
| grafico_base | 744 | 504 | 520 | 200 | Grafico complementar |

---

## TEMPLATE 3 — Dashboard Analitico (1920x1080)

Ideal para analistas, muitos dados, drill-down, comparacoes detalhadas.

```
Canvas: 1920 x 1080px

┌────────────────────────────────────────────────────────────────────────┐
│ HEADER (y:0, h:72)                                                     │
│  [Logo x:16]  [Titulo x:240]              [Filtros x:1400]             │
├────────────────────────────────────────────────────────────────────────┤
│ KPIs (y:88, h:160)                                                     │
│  [K1 x:16] [K2 x:390] [K3 x:764] [K4 x:1138] [K5 x:1512]             │
├────────────────────────────────────────────────────────────────────────┤
│ LINHA GRAFICOS (y:264, h:420)                                          │
│  [Graf1 x:16,w:608] [Graf2 x:640,w:608] [Graf3 x:1264,w:640]          │
├────────────────────────────────────────────────────────────────────────┤
│ BASE (y:700, h:364)                                                    │
│  [Tabela Grande x:16, w:1248]          [Painel x:1280, w:624]          │
└────────────────────────────────────────────────────────────────────────┘
```

### Coordenadas exatas — Template Analitico 1920x1080

| Visual | x | y | width | height | Descricao |
|--------|---|---|-------|--------|-----------|
| header_bg | 0 | 0 | 1920 | 72 | Fundo header |
| logo | 16 | 12 | 200 | 48 | Logo |
| titulo | 240 | 16 | 800 | 40 | Titulo |
| filtros_topo | 1400 | 12 | 504 | 48 | Slicers de filtro |
| kpi_1 | 16 | 88 | 358 | 160 | KPI 1 |
| kpi_2 | 390 | 88 | 358 | 160 | KPI 2 |
| kpi_3 | 764 | 88 | 358 | 160 | KPI 3 |
| kpi_4 | 1138 | 88 | 358 | 160 | KPI 4 |
| kpi_5 | 1512 | 88 | 392 | 160 | KPI 5 |
| grafico_1 | 16 | 264 | 608 | 420 | Grafico 1 (tendencia) |
| grafico_2 | 640 | 264 | 608 | 420 | Grafico 2 (comparacao) |
| grafico_3 | 1264 | 264 | 640 | 420 | Grafico 3 (distribuicao) |
| tabela_grande | 16 | 700 | 1248 | 364 | Matrix/tabela principal |
| painel_lateral | 1280 | 700 | 624 | 364 | KPIs adicionais ou grafico |

---

## TEMPLATE 4 — Pagina de Capa / Home (1600x900)

Pagina inicial de navegacao entre relatorios.

### Coordenadas exatas — Template Capa 1600x900

| Visual | x | y | width | height | Descricao |
|--------|---|---|-------|--------|-----------|
| fundo_completo | 0 | 0 | 1600 | 900 | Retangulo fundo (cor #004578) |
| logo_grande | 600 | 80 | 400 | 120 | Logo Mob2Con centralizado |
| titulo_relatorio | 400 | 240 | 800 | 60 | Titulo do relatorio |
| subtitulo | 500 | 320 | 600 | 40 | Subtitulo ou descricao |
| botao_nav_1 | 200 | 440 | 240 | 80 | Botao navegacao pagina 1 |
| botao_nav_2 | 480 | 440 | 240 | 80 | Botao navegacao pagina 2 |
| botao_nav_3 | 760 | 440 | 240 | 80 | Botao navegacao pagina 3 |
| botao_nav_4 | 1040 | 440 | 240 | 80 | Botao navegacao pagina 4 |
| linha_divisoria | 200 | 560 | 1200 | 2 | Linha decorativa |
| rodape_info | 400 | 820 | 800 | 32 | Data, versao, responsavel |

---

## TEMPLATE 5 — Layout Mobile (320x568)

Para relatorios acessados pelo app Power BI Mobile.

### Coordenadas exatas — Template Mobile 320x568

| Visual | x | y | width | height | Descricao |
|--------|---|---|-------|--------|-----------|
| header_mobile | 0 | 0 | 320 | 48 | Header compacto |
| kpi_1 | 8 | 56 | 304 | 100 | KPI principal (tela cheia) |
| kpi_2 | 8 | 164 | 144 | 80 | KPI secundario esquerdo |
| kpi_3 | 160 | 164 | 152 | 80 | KPI secundario direito |
| grafico_mobile | 8 | 252 | 304 | 200 | Grafico principal |
| tabela_mobile | 8 | 460 | 304 | 100 | Tabela resumida |

---

## Regras de Espacamento (Grid de 8px)

Todo posicionamento deve usar multiplos de 8:

```
8px  — espaco minimo entre elementos
16px — gap padrao entre visuais
24px — espaco entre secoes
32px — margem de pagina em telas grandes
48px — altura minima de header mobile
64px — altura padrao de header desktop
```

### Calculos rapidos para alinhar visuais

**4 KPIs em linha no canvas 1600px:**
- Largura disponivel: 1600 - 32 (margens) - 48 (gaps) = 1520px
- Largura de cada KPI: 1520 / 4 = 380px
- Posicoes x: 16, 412, 808, 1204

**3 KPIs em linha no canvas 1280px:**
- Largura disponivel: 1280 - 32 - 32 (gaps) = 1216px
- Largura de cada KPI: 1216 / 3 = ~405px
- Posicoes x: 16, 437, 858

**2 graficos lado a lado no canvas 1600px:**
- Largura disponivel: 1600 - 32 - 16 (gap) = 1552px
- Largura de cada grafico: 1552 / 2 = 776px
- Posicoes x: 16, 808

---

## Alturas Recomendadas por Tipo de Visual

| Visual | Altura minima | Altura ideal | Altura maxima |
|--------|--------------|--------------|---------------|
| KPI Card | 80px | 140px | 200px |
| Slicer dropdown | 40px | 48px | 64px |
| Slicer lista | 120px | 200px | 400px |
| Line Chart | 200px | 320px | 500px |
| Bar/Column Chart | 200px | 300px | 500px |
| Donut/Pie Chart | 200px | 280px | 400px |
| Matrix/Tabela | 160px | 280px | 500px |
| Scatter Chart | 240px | 360px | 500px |
| Mapa | 240px | 400px | 600px |
| Header/Banner | 48px | 64px | 80px |

---

## Posicionamento Z-Pattern aplicado aos Templates

```
ZONA 1 (topo esq)     ZONA 2 (topo dir)
  Logo, Titulo    ──►   Filtros, Data
       │
       │ (diagonal — KPIs)
       ▼
ZONA 3 (base esq)     ZONA 4 (base dir)
  Grafico principal ──►  Detalhes, Tabela
```

- **Zona 1** (x: 0-50%, y: 0-30%): Identidade + KPI mais importante
- **Zona 2** (x: 50-100%, y: 0-30%): Contexto + filtros
- **Zona 3** (x: 0-60%, y: 30-100%): Analise principal
- **Zona 4** (x: 60-100%, y: 30-100%): Suporte + detalhes

---

## Como usar estes templates com o MCP powerbi-layout

Exemplo de chamada para posicionar um KPI no template executivo:

```json
{
  "tool": "update_visual_layout",
  "args": {
    "visualName": "kpi_receita",
    "x": 16,
    "y": 80,
    "width": 368,
    "height": 140
  }
}
```

Exemplo para alinhar 4 KPIs em linha:

```json
{
  "tool": "align_visuals",
  "args": {
    "visualNames": ["kpi_1", "kpi_2", "kpi_3", "kpi_4"],
    "direction": "row",
    "startX": 16,
    "startY": 80,
    "width": 368,
    "height": 140,
    "gap": 16
  }
}
```

---

## Referencias

- Canvas size Power BI: [learn.microsoft.com](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-display-settings)
- Visual defaults 1920x1080: [learn.microsoft.com](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-reports-visual-defaults)
- Dashboard design best practices: [powerbiconsulting.com](https://powerbiconsulting.com/blog/power-bi-dashboard-best-practices-2026)
- Canvas size guide 1600x900: [lukasreese.com](https://lukasreese.com/2025/08/22/power-bi-canvas-size-guide/)
- Snap to grid: [learn.microsoft.com](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-gridlines-snap-to-grid)
- KPI best practices: [tabulareditor.com](https://tabulareditor.com/blog/kpi-card-best-practices-dashboard-design)