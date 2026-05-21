# 📐 Mob2Con — Guia de Layout e Proporções Power BI

> Padrões de posicionamento e dimensões para dashboards Mob2Con
> Unidade: pixels no canvas Power BI (16:9)

---

## 📏 Dimensões padrão do canvas

| Formato | Width x Height |
|---------|----------------|
| **Dashboard Executivo (padrão)** | 1280 x 720 |
| **Dashboard Operacional (wide)** | 1920 x 1080 |
| **Mobile Portrait** | 414 x 736 |
| **Custom 4:3 (slideshow)** | 1024 x 768 |

## 🧮 Grid sistema

Usar **grid de 12 colunas** com gap de **16px**.

- Canvas 1280: col = 96px, gutter = 16px
- Canvas 1920: col = 144px, gutter = 24px

### Margens obrigatórias
- **Topo:** 20px (header)
- **Esquerda/Direita:** 20px
- **Base:** 16px
- **Entre visuais:** 16px (gap padrão)

---

## 🎯 Template Dashboard Executivo (1280x720)

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (logo + titulo + filtros globais)      20px | 80px  │
├─────────────────────────────────────────────────────────────┤
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4  │  h: 120px        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│       GRAFICO PRINCIPAL (620 x 340)      │   TABELA         │
│                                          │   LATERAL        │
│                                          │   (380 x 340)    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│          RODAPE: 2 visuais lado a lado    h: 160px          │
└─────────────────────────────────────────────────────────────┘
```

### Coordenadas exatas (x, y, width, height)

| Visual | x | y | width | height |
|--------|---|---|-------|--------|
| Logo | 20 | 20 | 80 | 40 |
| Título da página | 120 | 20 | 600 | 40 |
| Slicer global 1 | 760 | 20 | 200 | 40 |
| Slicer global 2 | 980 | 20 | 280 | 40 |
| KPI 1 | 20 | 80 | 308 | 120 |
| KPI 2 | 340 | 80 | 308 | 120 |
| KPI 3 | 660 | 80 | 308 | 120 |
| KPI 4 | 980 | 80 | 280 | 120 |
| Gráfico principal | 20 | 216 | 620 | 340 |
| Tabela lateral | 656 | 216 | 604 | 340 |
| Visual rodapé 1 | 20 | 572 | 620 | 130 |
| Visual rodapé 2 | 656 | 572 | 604 | 130 |

---

## 🎯 Template Dashboard Operacional (1920x1080)

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER completo (120px altura)                             │
├──────────┬──────────────────────────────────────────────────┤
│ SLICERS  │  6 KPIs em linha (altura 140px)                  │
│ LATERAL  ├──────────────────────────────────────────────────┤
│ 250px    │                                                  │
│ width    │     3 GRAFICOS (3 x 550 x 380)                   │
│          ├──────────────────────────────────────────────────┤
│          │     TABELA GRANDE (1650 x 300)                   │
└──────────┴──────────────────────────────────────────────────┘
```

### Coordenadas

| Visual | x | y | width | height |
|--------|---|---|-------|--------|
| Header | 0 | 0 | 1920 | 120 |
| Painel slicers | 20 | 140 | 230 | 920 |
| KPI 1-6 | 270 a 1620 (gap 16) | 140 | 260 | 140 |
| Gráfico 1 | 270 | 300 | 540 | 380 |
| Gráfico 2 | 830 | 300 | 540 | 380 |
| Gráfico 3 | 1390 | 300 | 510 | 380 |
| Tabela | 270 | 700 | 1630 | 360 |

---

## 🎯 Template Capa / Home

Canvas 1280x720

```
┌─────────────────────────────────────────────┐
│                                             │
│           LOGO MOB2CON (centralizado)        │
│                                             │
│           TÍTULO DO RELATÓRIO                │
│           Subtítulo descritivo               │
│                                             │
│                                             │
│     [BOTÃO 1]  [BOTÃO 2]  [BOTÃO 3]          │
│                                             │
│     Rodapé: v1.0 · atualizado em ...         │
└─────────────────────────────────────────────┘
```

| Elemento | x | y | width | height |
|----------|---|---|-------|--------|
| Logo central | 540 | 140 | 200 | 100 |
| Título H1 | 140 | 260 | 1000 | 60 |
| Subtítulo | 240 | 330 | 800 | 40 |
| Botão nav 1 | 340 | 460 | 180 | 60 |
| Botão nav 2 | 550 | 460 | 180 | 60 |
| Botão nav 3 | 760 | 460 | 180 | 60 |
| Rodapé | 20 | 690 | 1240 | 20 |

---

## 📐 Tamanhos recomendados por tipo de visual

| Tipo | Mínimo | Ideal | Máximo |
|------|--------|-------|--------|
| **Card / KPI** | 200x100 | 280x120 | 400x140 |
| **Slicer dropdown** | 180x40 | 220x40 | 300x40 |
| **Slicer lista** | 200x200 | 240x400 | 300x600 |
| **Bar chart** | 320x240 | 540x380 | 1200x600 |
| **Line chart** | 400x280 | 620x340 | 1400x500 |
| **Pie/Donut** | 240x240 | 320x320 | 420x420 |
| **Table** | 400x200 | 600x400 | 1600x700 |
| **Matrix** | 500x300 | 760x440 | 1800x800 |
| **Gauge** | 200x200 | 260x260 | 360x360 |
| **Map** | 400x300 | 640x440 | 1200x700 |
| **Botão** | 100x40 | 180x60 | 240x80 |

---

## 🎨 Proporções recomendadas

- **KPI:** 2.3:1 (width:height) — ex: 280x120
- **Bar chart horizontal:** 16:9 — ex: 640x360
- **Line chart:** 16:9 ou 3:1 — ex: 900x300 (timeline)
- **Cards em linha:** sempre dividir canvas útil igualmente com gap 16
- **Donut:** 1:1 exato
- **Tabela com >8 colunas:** forçar 2:1 mínimo (width 2x height)

---

## 🧩 Anatomia do KPI (padrão Mob2Con)

```
┌──────────────────────────┐
│  [Ícone]   Título        │  ← 14pt, #434343, Raleway Bold
│                          │
│  R$ 1.2M                 │  ← 28pt, #F46901, Raleway Black
│                          │
│  ▲ 12% vs mês anterior   │  ← 11pt, verde #107C41
└──────────────────────────┘
```

**Dimensões:** 280 x 120 (proporção 2.3:1)
**Padding interno:** 16px
**Border:** 1px solid `#E0E0E0`, border-radius 4px

---

## 🔗 Navegação entre páginas

Sempre no **topo direito**:
- Botões de 120x40, gap 8
- Ativo: fundo `#F46901` + texto branco
- Inativo: fundo transparente + texto `#434343`
- Hover: fundo `#FFE5CC`

Ou **menu lateral esquerdo** (para relatórios com 5+ páginas):
- Width: 200px
- Cada item: 180x40, gap 4
- Ativo: fundo `#F46901`
- Ícone à esquerda (24px) + texto
