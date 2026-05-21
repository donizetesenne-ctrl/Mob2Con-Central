# 🔘 Mob2Con — Botões e Navegação Power BI

> Código JSON dos botões padronizados para copiar direto no `visual.json` do PBIP.

---

## 🎯 Botão Primário (CTA Mob2Con)

**Dimensões:** 180 x 48 (ou 180 x 60)
**Cor:** `#F46901` / Texto branco
**Fonte:** Raleway Bold 13pt

### JSON para visual Button

```json
{
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "button": [{
        "properties": {
          "shape": "rectangle",
          "cornerRadius": { "expr": { "Literal": { "Value": "4D" } } }
        }
      }],
      "fill": [{
        "properties": {
          "show": { "expr": { "Literal": { "Value": "true" } } },
          "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#F46901'" } } } } },
          "transparency": { "expr": { "Literal": { "Value": "0D" } } }
        },
        "selector": { "id": "default" }
      }],
      "text": [{
        "properties": {
          "text": { "expr": { "Literal": { "Value": "'CLIQUE AQUI'" } } },
          "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
          "fontFamily": { "expr": { "Literal": { "Value": "'Raleway'" } } },
          "fontSize": { "expr": { "Literal": { "Value": "13D" } } },
          "bold": { "expr": { "Literal": { "Value": "true" } } },
          "horizontalAlignment": { "expr": { "Literal": { "Value": "'center'" } } }
        },
        "selector": { "id": "default" }
      }]
    }
  }
}
```

---

## 🎯 Botão Secundário (Outline)

**Dimensões:** 180 x 48
**Cor:** transparente com borda laranja / Texto `#F46901`

```json
{
  "objects": {
    "fill": [{
      "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } }
      },
      "selector": { "id": "default" }
    }],
    "outline": [{
      "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "lineColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#F46901'" } } } } },
        "weight": { "expr": { "Literal": { "Value": "2D" } } }
      },
      "selector": { "id": "default" }
    }],
    "text": [{
      "properties": {
        "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#F46901'" } } } } },
        "fontFamily": { "expr": { "Literal": { "Value": "'Raleway'" } } },
        "fontSize": { "expr": { "Literal": { "Value": "13D" } } },
        "bold": { "expr": { "Literal": { "Value": "true" } } }
      }
    }]
  }
}
```

---

## 🎯 Botão Navegação (entre páginas do relatório)

**Dimensões:** 120 x 40
**Hover state:** fundo `#FFE5CC`
**Selected state:** fundo `#F46901` + texto branco

```json
{
  "objects": {
    "fill": [
      {
        "properties": {
          "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } }
        },
        "selector": { "id": "default" }
      },
      {
        "properties": {
          "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFE5CC'" } } } } }
        },
        "selector": { "id": "hover" }
      },
      {
        "properties": {
          "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#F46901'" } } } } }
        },
        "selector": { "id": "selected" }
      }
    ],
    "visualLink": [{
      "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
        "navigationSection": { "expr": { "Literal": { "Value": "'NOME_DA_PAGINA'" } } }
      }
    }]
  }
}
```

### Ações de navegação disponíveis
- `PageNavigation` → ir para página X
- `Bookmark` → aplicar um bookmark
- `DrillThrough` → drill through
- `WebUrl` → abrir URL externa
- `QA` → abrir Q&A
- `Back` → voltar à página anterior

---

## 🎯 Botão "Exportar dados"

**Dimensões:** 140 x 36, ícone 16px + texto
**Ação:** bookmark que dispara showVisualActions

```json
{
  "text": { "expr": { "Literal": { "Value": "'⬇ EXPORTAR'" } } },
  "fontFamily": { "expr": { "Literal": { "Value": "'Raleway'" } } },
  "fontSize": { "expr": { "Literal": { "Value": "11D" } } }
}
```

---

## 🎯 Botão "Aplicar Filtros" / "Limpar Filtros"

**Par de botões:** 120 x 36 cada, gap 8

**Aplicar:**
- Fundo `#F46901` / texto branco
- Ícone check (✓) ou filter

**Limpar:**
- Fundo transparente / borda `#434343` / texto `#434343`
- Ícone reset (↻)
- Ação: bookmark "Reset All Slicers" (usar bookmark que limpa todos os slicers)

---

## 🧭 Menu Lateral (5+ páginas)

Container: **width 200px**, fundo `#434343`
Logo no topo: 160x60, padding 20
Divisor: linha 1px `#5C5C5C`
Itens do menu: 180x40, gap 4

### Estados dos itens

| Estado | Fundo | Texto | Ícone |
|--------|-------|-------|-------|
| Default | transparente | `#FFFFFF` | `#FFFFFF` |
| Hover | `#5C5C5C` | `#FFFFFF` | `#F46901` |
| Ativo | `#F46901` | `#FFFFFF` | `#FFFFFF` |

---

## 🎨 Ícones recomendados (Unicode/Emoji)

Para usar direto no texto do botão sem precisar importar SVG:

| Função | Ícone | Código |
|--------|-------|--------|
| Home | 🏠 ou ⌂ | `⌂` |
| Voltar | ← | `\u2190` |
| Avançar | → | `\u2192` |
| Filtrar | ⚙ ou ⟲ | `\u2699` |
| Exportar | ⬇ | `\u2B07` |
| Info | ⓘ | `\u24D8` |
| Alerta | ⚠ | `\u26A0` |
| Check | ✓ | `\u2713` |
| X | ✕ | `\u2715` |
| Busca | 🔍 ou ⌕ | `\u2315` |

---

## 📦 Bookmarks padrão para usar

Criar sempre estes bookmarks no projeto:

1. **`Home`** — volta todos os slicers ao default e vai para página inicial
2. **`ResetAllFilters`** — limpa todos os slicers da página atual
3. **`ToggleMenu`** — abre/fecha o menu lateral
4. **`Export`** — mostra visuais de export (slicer desabilitado)
5. **`DrillView`** — mostra visuais de drill adicional

Nome pattern: `<Acao><Contexto>` em PascalCase
