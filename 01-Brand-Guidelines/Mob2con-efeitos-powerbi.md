# ✨ Mob2Con — Efeitos Visuais e Interações Power BI

> Receitas de efeitos visuais, animações e interações para dashboards Mob2Con.

---

## 🎨 Efeitos no Tema (visualStyles)

### Sombra suave em todos os visuais
Adicionar ao tema JSON dentro de `visualStyles."*"."*"`:

```json
"dropShadow": [{
  "show": true,
  "color": { "solid": { "color": "#000000" } },
  "transparency": 85,
  "position": "Outer",
  "preset": "Custom",
  "shadowOffset": { "x": 2, "y": 2 },
  "blur": 6,
  "spread": 0
}]
```

### Borda arredondada (padrão Mob2Con)
```json
"border": [{
  "show": true,
  "color": { "solid": { "color": "#E0E0E0" } },
  "radius": 8,
  "width": 1
}]
```

### Fundo com transparência sutil
```json
"background": [{
  "show": true,
  "color": { "solid": { "color": "#FFFFFF" } },
  "transparency": 5
}]
```

---

## 🎬 Interações e Animações

### 1. Bookmarks para transições
Criar bookmarks e linkar em botões:

**Setup:**
1. View → Bookmarks → Add bookmark (nome: "Visao1")
2. Alterar filtros/visuais → Add bookmark (nome: "Visao2")
3. Botão com ação: `Bookmark` → "Visao1"

**Uso típico Mob2Con:**
- Botão "Mensal" / "Semanal" / "Diário" → bookmarks com diferentes slicers
- Botão "Visão Executiva" / "Visão Operacional" → mostrar/esconder visuais

### 2. Drill through
Configurar página oculta com detalhes:
- Direita → Drill through → arrastar campo (ex: `Loja`)
- Clicar com direito em qualquer visual no dashboard → "Drill through" → levar para página detalhada

### 3. Tooltip customizada (mini-dashboard no hover)
1. Criar página nova (tamanho 320x240)
2. View → Format page → Tooltip → ON
3. Adicionar visuais na página
4. Na página principal, no visual: Format → Tooltip → Report page → selecionar

### 4. Cross-highlighting controlado
Selecionar visual → Format → Edit interactions:
- 🔗 Filter (default)
- 🔆 Highlight (suave)
- ⊘ None (isolado)

**Regra Mob2Con:** KPIs nunca filtram outros KPIs; gráficos principais filtram tabelas.

---

## 📱 Responsividade

### Mobile Layout
1. View → Mobile layout
2. Arrastar só os visuais essenciais (KPIs + 1 gráfico + tabela)
3. Resolução: 414 x 736 (retrato)

**Proporção recomendada:**
- KPIs: 2 por linha, 200x100 cada
- Gráficos: 1 por linha, 400x280
- Tabela: scroll horizontal, 400x360

---

## 🎭 Conditional Formatting (Formatação Condicional)

### Barra de progresso numa tabela
Campo → Conditional formatting → **Data bars**:
- Positive bar color: `#F46901`
- Negative bar color: `#C00000`
- Show bar only: ❌ (mostra valor também)

### Background cor baseada no KPI
Campo → Conditional formatting → **Background color** → Format by: `Field value` → selecionar medida `Cor Status` (que retorna `#107C41`, `#F46901` ou `#C00000`).

### Ícones de semáforo
Campo → Conditional formatting → **Icons**:
- 🟢 Verde se valor >= meta
- 🟡 Amarelo se valor >= 80% meta
- 🔴 Vermelho abaixo de 80%

---

## 🎯 Estados de Slicer Interativos

### Slicer "Chip Style" (pílulas)
Slicer → Format → **Items**:
- Padding: 8px
- Border radius: 20 (transforma em pílula)
- Background selected: `#F46901`
- Background unselected: `#F0F0F0`
- Font color selected: `#FFFFFF`
- Font color unselected: `#434343`

### Slicer Dropdown minimalista
Slicer → Format:
- Slicer header: OFF
- Dropdown
- Border: bottom only, color `#F46901`, width 2

---

## 🔄 Sync Slicers (slicers sincronizados entre páginas)

1. Criar slicer na Página 1
2. View → **Sync slicers** pane
3. Selecionar o slicer
4. Marcar **todas as páginas** onde ele deve aplicar
5. Dica: na página onde ele NÃO deve APARECER, marcar só "Sync" (sem "Visible")

**Regra Mob2Con:** slicer de data, slicer de rede e slicer de loja sempre sincronizados entre todas as páginas.

---

## 🎨 Gradientes e Imagem de Fundo

### Página com fundo gradiente sutil
Page → Format → **Wallpaper**:
- Image: criar SVG com gradiente `#F8F8F8` → `#FFFFFF`
- Ou usar cor sólida `#F8F8F8`

### SVG de gradiente (exemplo para copiar como wallpaper)
Salvar como `bg-gradient.svg`:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8F8F8"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#g)"/>
</svg>
```

---

## 🧩 Trucos de Layout

### 1. Visual "flutuante" sobre outro
- Enviar para trás / para frente com menu direito
- Usar para ícones em cima de KPIs, badges de alerta

### 2. Separadores visuais
Criar Shape (retângulo) 1x visual-height:
- Fill: `#E0E0E0`
- Width: 1
- Sem borda
- Funciona como divisor entre colunas de KPIs

### 3. Card com ícone
Dentro de um card, adicionar:
- **Image** (ícone) 32x32 no canto esquerdo
- **Card** do KPI à direita
- Alinhar os dois manualmente

### 4. Título de seção com linha horizontal
```
┌──────────────────────────────────────┐
│ INDICADORES PRINCIPAIS ══════════════│
└──────────────────────────────────────┘
```
Criar:
- Text box "INDICADORES PRINCIPAIS" (Raleway Bold 16pt, `#434343`)
- Shape (line) abaixo, cor `#F46901`, height 2px, width total

---

## ⚡ Performance Visual

### Evitar sobreposição pesada
- Máximo 15-20 visuais por página
- Tabelas com mais de 100 linhas → usar paginação / drill

### Desabilitar interações desnecessárias
View → Edit interactions → configurar: cards/KPIs → "None" (não filtram nada)

### Reduzir animações
Em relatórios publicados, Power BI Service → Settings → disable animations (em dashboards de refresh frequente)

---

## 📋 Checklist de Polimento Final

- [ ] Tema Mob2Con aplicado (View → Themes)
- [ ] Todas as páginas com Wallpaper `#F8F8F8`
- [ ] Fonte Raleway em todos os textos
- [ ] KPIs com sombra sutil
- [ ] Botões de navegação com 3 estados (default/hover/selected)
- [ ] Slicers sincronizados entre páginas
- [ ] Bookmarks criados (Home, Reset, Export)
- [ ] Tooltips configuradas nos gráficos principais
- [ ] Edit interactions revisado (KPIs não filtram)
- [ ] Mobile layout testado
- [ ] Todos os títulos **sem corte** (sem "...")
- [ ] Bordas arredondadas em 4px ou 8px
- [ ] Gap de 16px entre visuais mantido
