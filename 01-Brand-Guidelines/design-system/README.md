# Mob2Con Design System — Camadas Complementares

> 4 camadas que se complementam: se uma falhar, as outras assumem.
> Atualizado: 2026-05-14

---

## 🧩 Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│ CAMADA 1 — design-tokens.json + layout-templates.json        │ ← fonte da verdade
│   → Lido por MCPs (powerbi-layout, powerbi-bridge)            │
│   → Lido por scripts de automação                             │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 2 — mob2con.css                                        │ ← espelho web
│   → Mesmas cores via CSS custom properties                    │
│   → Garante marca em qualquer página HTML, wiki, dashboard    │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 3 — index.html + templates/*.html                      │ ← preview visual
│   → Mostra como o dashboard deve parecer                      │
│   → Fallback quando o Power BI Desktop não está disponível    │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 4 — Mob2Con-Brand-Theme.json (em 02-Powerbi-Projetos)  │ ← formato Microsoft
│   → Aplicado no Power BI: View → Themes → Browse              │
└──────────────────────────────────────────────────────────────┘
```

### Por que 4 camadas?

| Cenário de falha | O que assume |
|---|---|
| Tema PBI não carrega (versão antiga, conflito) | CSS + HTML mantêm a marca em qualquer preview |
| MCP não consegue ler o tema | Lê os tokens JSON diretamente |
| JSON corrompido | CSS tem as mesmas cores hardcoded como fallback |
| CSS não disponível | HTML inline usa as cores do JSON |
| Tudo isso falha | Markdown em `Mob2con-brand-context.md` documenta cada hex |

---

## 📁 Estrutura

```
design-system/
├── README.md                  ← este arquivo
├── design-tokens.json         ← fonte única de verdade (cores, fontes, espaços)
├── layout-templates.json      ← coordenadas x/y/w/h para os 5 templates
├── mob2con.css                ← variáveis CSS + componentes (espelha o JSON)
├── sync-tokens.js             ← verifica e regenera CSS/tema a partir do JSON
├── index.html                 ← preview do design system completo
└── templates/
    ├── executive.html         ← canvas 1600 × 900
    ├── operational.html       ← canvas 1280 × 720
    ├── analytical.html        ← canvas 1920 × 1080
    ├── cover.html             ← canvas 1600 × 900 (capa)
    └── mobile.html            ← canvas 320 × 568
```

---

## 🚀 Como usar

### Para abrir o preview
Duplo clique em `index.html` ou abra em qualquer navegador.

### Para verificar se as 3 camadas estão em sincronia
```cmd
cd 01-Brand-Guidelines\design-system
node sync-tokens.js
```

Saída esperada:
```
Tokens version : 1.0.0
Orange (JSON)  : #F46901
Orange in CSS  : ✅ ok
Orange in PBI  : ✅ #F46901
```

### Para regenerar CSS após editar o JSON
```cmd
node sync-tokens.js --apply
```
Isso atualiza:
- O bloco `:root { ... }` em `mob2con.css`
- Cria/atualiza `Mob2Con-Theme-auto.json` (versão minimal de fallback do tema PBI)

> ⚠️ O `Mob2Con-Brand-Theme.json` oficial em `02-Powerbi-Projetos/` **não** é sobrescrito pra preservar `visualStyles` detalhado. Use o auto.json apenas como verificação.

### Para usar nos MCPs

Os MCPs `powerbi-layout` e `powerbi-bridge` podem ler diretamente:

```js
const tokens = JSON.parse(fs.readFileSync('design-tokens.json'));
const layout = JSON.parse(fs.readFileSync('layout-templates.json'));

// Aplicar coordenadas do template executivo
for (const v of layout.templates.executive.visuals) {
  await callTool('update_visual_layout', {
    visualName: v.name,
    x: v.x, y: v.y,
    width: v.width, height: v.height
  });
}
```

### Para usar em uma página HTML/wiki

```html
<link rel="stylesheet" href=".../01-Brand-Guidelines/design-system/mob2con.css">

<div class="m2c-kpi m2c-kpi--orange">
  <div class="m2c-kpi__title">Receita</div>
  <div class="m2c-kpi__value">R$ 1.2M</div>
  <div class="m2c-kpi__delta m2c-kpi__delta--up">▲ 12%</div>
</div>
```

---

## 🎨 Tokens disponíveis

### Cores
- Brand: `orange`, `graphite`, `black`, `blueConnect` (só MobConnect), `purple`
- Neutral: `gray50` → `gray900`
- Semantic: `success`, `warning`, `danger`, `info`
- KPI: `altRow`, `totalRow`

### Tipografia
- Family: `primary` (Raleway), `monospace`
- Weight: `regular` (400), `bold` (700), `black` (900)
- Size: `xs` (9pt) → `kpi` (28pt)

### Layout
- Canvas: `executive`, `operational`, `analytical`, `cover`, `mobile`
- Spacing: escala de 8px (`0`, `1`, `2`, `3`, `4`, `6`, `8`)
- Radius: `sm` (4px), `md` (6px), `lg` (8px)

---

## 🔁 Quando atualizar

1. **Mudou cor de marca?** Edite `design-tokens.json` e rode `node sync-tokens.js --apply`
2. **Novo template de canvas?** Adicione em `layout-templates.json` e crie HTML correspondente em `templates/`
3. **Novo componente?** Adicione no CSS e adicione exemplo em `index.html`

---

## 📚 Referências

- Brand Guidelines completos: `../Mob2con-brand-guidelines.md`
- Z-Pattern e princípios: `../Mob2con-brand-context.md`
- Layouts em markdown: `../Mob2con-layout-base.md`
- Botões e navegação: `../Mob2con-botoes-navegacao.md`
- Efeitos Power BI: `../Mob2con-efeitos-powerbi.md`
- Tema PBI oficial: `../../02-Powerbi-Projetos/Mob2Con-Brand-Theme.json`
