# 🎨 Mob2Con Design System

> Kit reutilizável de UI para qualquer projeto HTML/CSS/JS. Copie `style.css` + `DESIGN.md` e pronto.

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-F46901?style=flat-square)](https://SEU-USUARIO.github.io/mob2con-design-system/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

---

## 🚀 Quick Start

```html
<!-- Adicione no <head> do seu HTML -->
<link rel="stylesheet" href="style.css">

<!-- Use as classes -->
<div class="card kpi">
  <div class="kpi-label">FATURAMENTO</div>
  <div class="kpi-value">R$ 2.4M</div>
  <div class="kpi-trend up">▲ 12.3%</div>
</div>
```

Ou use as **variáveis CSS** em qualquer lugar:
```css
.meu-elemento {
  color: var(--primary);
  background: var(--bg);
  border-radius: var(--radius-lg);
  padding: var(--sp-2);
  box-shadow: var(--shadow-sm);
}
```

---

## 📁 Estrutura

```
mob2con-design-system/
├── index.html              ← Landing page (GitHub Pages)
├── style.css               ← CSS universal — copie para qualquer projeto
├── DESIGN.md               ← Agentes de IA leem este arquivo
├── preview.html            ← Catálogo visual (light)
├── preview-dark.html       ← Catálogo visual (dark)
└── templates/
    ├── executive.html      ← Dashboard executivo
    ├── operational.html    ← Dashboard operacional
    ├── cover.html          ← Página de navegação
    ├── mobile.html         ← Layout mobile
    └── components.html     ← Todos os componentes isolados
```

---

## 🎯 O que inclui

| Componente | Classes |
|-----------|---------|
| Header | `.header`, `.logo`, `.nav-link` |
| KPI Cards | `.card .kpi`, `.kpi-value`, `.kpi-trend.up/.down` |
| Buttons | `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-sm/.btn-lg` |
| Tables | `.table`, `tr.total`, alternating rows automático |
| Badges | `.badge`, `.badge-success/.danger/.warning/.info` |
| Inputs | `.input` |
| Grid | `.grid`, `.grid-2/.grid-3/.grid-4` |
| Utilities | `.mt-1`, `.mb-2`, `.p-3`, `.shadow`, `.rounded`, `.text-muted` |

---

## 🎨 Cores (variáveis CSS)

| Variável | Hex | Uso |
|----------|-----|-----|
| `--primary` | `#F46901` | CTAs, destaques, hover |
| `--secondary` | `#6F05D4` | Acento, gráficos |
| `--graphite` | `#434343` | Títulos, header |
| `--success` | `#107C41` | Positivo |
| `--danger` | `#C00000` | Negativo |
| `--warning` | `#FFC107` | Atenção |
| `--bg` | `#F3F6FA` | Fundo da página |

---

## 🤖 Para Agentes de IA

Coloque o `DESIGN.md` na raiz do projeto e diga:

> "Build me a page following DESIGN.md"

Funciona com: Amazon Q, Claude, Cursor, Kiro, Google Stitch, Copilot.

---

## 📦 Como usar no GitHub Pages

1. Crie um repo no GitHub
2. Faça push desta pasta
3. Settings → Pages → Source: `main` / `root`
4. Acesse: `https://seu-usuario.github.io/mob2con-design-system/`

---

## 📄 License

MIT — use em qualquer projeto, comercial ou pessoal.
