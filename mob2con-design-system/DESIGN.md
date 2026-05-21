# DESIGN.md — Mob2Con

> AI-readable design system for Mob2Con brand. Drop this file in any project and tell your agent: "build using this design".

---

## 1. Visual Theme & Atmosphere

- **Mood:** Professional, warm, data-driven. Corporate dashboards with human touch.
- **Density:** Medium-high. Information-rich but never cluttered.
- **Philosophy:** "Orange energy, graphite structure." Every element serves a KPI or navigation purpose.
- **Surface:** Light backgrounds (#F3F6FA), white cards with subtle shadows, orange accents for emphasis.
- **Dark mode:** Not supported. Always light surfaces.

---

## 2. Color Palette & Roles

### Brand Colors

| Name | Hex | Role |
|------|-----|------|
| Orange (Primary) | `#F46901` | Primary brand, CTAs, active states, highlights |
| Graphite | `#434343` | Titles, borders, header backgrounds |
| Black | `#111111` | Body text, KPI values (high contrast) |
| Blue Connect | `#4285F4` | EXCLUSIVE to MobConnect sub-brand. Never use for Mob2Con. |
| Purple | `#6F05D4` | Secondary accent, charts series 2 |

### Semantic Colors

| Name | Hex | Role |
|------|-----|------|
| Success | `#107C41` | Positive indicators, growth, on-target |
| Danger | `#C00000` | Negative indicators, alerts, off-target |
| Warning | `#FFC107` | Caution, approaching threshold |
| Info | `#4285F4` | Informational, neutral highlights |

### Neutral Scale

| Token | Hex | Usage |
|-------|-----|-------|
| white | `#FFFFFF` | Card backgrounds |
| gray50 | `#F8F8F8` | Hover states |
| gray100 | `#F3F2F1` | Alternate rows |
| gray150 | `#F3F6FA` | Page background (default) |
| gray200 | `#E2E8F0` | Borders, dividers |
| gray300 | `#E0E0E0` | Card borders |
| gray400 | `#F0F0F0` | Gridlines |
| gray500 | `#605E5C` | Secondary text, labels |
| gray700 | `#434343` | Titles (same as graphite) |
| gray900 | `#111111` | Primary text |

### KPI-specific

| Token | Hex | Usage |
|-------|-----|-------|
| altRow | `#FFF8F2` | Alternating table rows (warm tint) |
| totalRow | `#FFF0E0` | Total/summary row highlight |

---

## 3. Typography Rules

**Font family:** `Raleway, 'Segoe UI', Arial, sans-serif`
**Monospace:** `Consolas, 'Courier New', monospace`

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Page title | 20pt | 900 (Black) | #434343 |
| Visual title | 14pt | 700 (Bold) | #434343 |
| Subtitle | 12pt | 700 (Bold) | #605E5C |
| Body text | 11pt | 400 (Regular) | #111111 |
| Small/labels | 10pt | 400 (Regular) | #605E5C |
| Caption/axis | 9pt | 400 (Regular) | #605E5C |
| KPI value | 28pt | 900 (Black) | #111111 |
| KPI label | 10pt | 700 (Bold) | #605E5C |

### Rules
- Never use font weights below 400
- Titles are always uppercase-first, never ALL CAPS
- KPI values use tabular/monospace numerals when available
- Line height: 1.4 for body, 1.2 for headings

---

## 4. Component Stylings

### Cards (KPI)
```
background: #FFFFFF
border: 1px solid #E0E0E0
border-radius: 8px
shadow: 0 1px 3px rgba(17,17,17,0.08), 0 1px 2px rgba(17,17,17,0.04)
padding: 16px
```
- Hover: shadow changes to `0 4px 12px rgba(244,105,1,0.18)`
- Active/selected: left border 3px solid #F46901

### Buttons (Navigation)
```
background: #F46901
color: #FFFFFF
border-radius: 6px
font-weight: 700
font-size: 11pt
padding: 12px 24px
```
- Hover: darken 10% → `#D95E01`
- Disabled: opacity 0.5
- Secondary variant: background #FFFFFF, border 1px solid #F46901, color #F46901

### Header Bar
```
background: #434343
height: 64px (desktop), 48px (mobile)
```
- Logo left-aligned, filters right-aligned
- Text inside header: #FFFFFF

### Tables / Matrix
```
header-row: background #434343, color #FFFFFF, font-weight 700
body-row: background #FFFFFF
alt-row: background #FFF8F2
total-row: background #FFF0E0, font-weight 700
gridlines: 1px solid #F0F0F0
```

### Charts
- Series 1: `#F46901` (orange)
- Series 2: `#6F05D4` (purple)
- Series 3: `#4285F4` (blue)
- Series 4: `#107C41` (green)
- Series 5: `#FFC107` (yellow)
- Series 6: `#C00000` (red)
- Axis labels: 9pt, #605E5C
- Gridlines: #F0F0F0

---

## 5. Layout Principles

### Spacing Scale (base = 8px)
| Token | Value |
|-------|-------|
| 0 | 0px |
| 1 | 8px |
| 2 | 16px (default gap between visuals) |
| 3 | 24px |
| 4 | 32px |
| 6 | 48px |
| 8 | 64px (header height) |

### Grid
- No fixed column grid. Uses absolute positioning (x, y, width, height in px).
- Visual gap: 16px minimum between elements.
- Page margin: 16px on all sides.
- Header always full-width, pinned to top.

### Canvas Sizes
| Template | Width | Height | Use case |
|----------|-------|--------|----------|
| Executive | 1600 | 900 | C-suite, KPIs, Z-pattern |
| Analytical | 1920 | 1080 | Drill-down, comparisons |
| Operational | 1280 | 720 | Daily monitoring |
| Cover | 1600 | 900 | Navigation home page |
| Mobile | 320 | 568 | Power BI Mobile |

### Z-Pattern (Executive)
1. Top-left: Logo + title
2. Top-right: Filters
3. Middle row: 4 KPI cards (equal width)
4. Bottom-left: Main chart (60% width)
5. Bottom-right: Secondary chart (40% width)

---

## 6. Depth & Elevation

| Level | Shadow | Usage |
|-------|--------|-------|
| 0 | none | Flat elements, backgrounds |
| 1 | `0 1px 3px rgba(17,17,17,0.08), 0 1px 2px rgba(17,17,17,0.04)` | Cards, panels |
| 2 | `0 4px 12px rgba(244,105,1,0.18)` | Hover states, focused cards |
| 3 | `0 8px 24px rgba(17,17,17,0.20)` | Modals, tooltips, dropdowns |

- Cards float at level 1 by default
- On hover, cards rise to level 2 (orange-tinted shadow)
- No elevation on mobile (flat design)

---

## 7. Do's and Don'ts

### ✅ Do
- Use orange (#F46901) as the single dominant accent
- Keep backgrounds light (#F3F6FA or #FFFFFF)
- Use Raleway for all text
- Place KPIs in a horizontal row at the top
- Use graphite (#434343) for headers and structural elements
- Maintain 16px gap between all visuals
- Use warm alternating rows (#FFF8F2) in tables

### ❌ Don't
- Never use blue (#4285F4) as primary — it's reserved for MobConnect
- Never use dark/black backgrounds for pages
- Never use more than 6 chart series colors
- Never use rounded corners > 8px
- Never center-align body text (left-align always)
- Never use gradients on backgrounds
- Never mix font families (Raleway only)
- Never place KPIs below charts

---

## 8. Responsive Behavior

| Breakpoint | Canvas | Behavior |
|------------|--------|----------|
| Desktop (default) | 1600×900 or 1920×1080 | Full layout, side-by-side charts |
| Tablet | 1280×720 | Operational template, stacked where needed |
| Mobile | 320×568 | Single column, KPIs stacked, no side panels |

### Collapsing Strategy
1. KPI row: stays horizontal on desktop/tablet, stacks vertically on mobile
2. Charts: side-by-side on desktop, full-width stacked on mobile
3. Tables: full-width always, horizontal scroll on mobile
4. Header: shrinks from 64px to 48px on mobile
5. Filters: move from header to expandable panel on mobile

---

## 9. Agent Prompt Guide

### Quick Color Reference
```
primary:    #F46901  (orange — use for CTAs, highlights, active)
secondary:  #6F05D4  (purple — charts, accents)
text:       #111111  (body text, KPI values)
title:      #434343  (headings, header bg)
background: #F3F6FA  (page bg)
card-bg:    #FFFFFF  (card surfaces)
success:    #107C41  (positive)
danger:     #C00000  (negative)
```

### Ready-to-Use Prompts

**Dashboard page:**
> "Create a dashboard with a dark graphite header (64px), 4 orange-accented KPI cards in a row, a main line chart (60% width) and a donut chart (40% width) below. Use Raleway font, #F3F6FA background, white cards with subtle shadow. Primary color #F46901."

**Landing/Cover page:**
> "Create a centered cover page with white background, large Mob2Con logo, title in Raleway Black 20pt #434343, 4 navigation buttons in a row with #F46901 background and white text, rounded 6px."

**Table/Report page:**
> "Create a data table with #434343 header row (white text), alternating rows #FFFFFF and #FFF8F2, total row #FFF0E0 bold. 9pt axis labels in #605E5C. Border 1px #E0E0E0."

**Mobile layout:**
> "Create a mobile-first layout 320px wide. 48px header, stacked KPI cards (full width), single chart below, compact table at bottom. Same colors, Raleway font, 8px gaps."

---

## File References

| File | Purpose |
|------|---------|
| `01-Brand-Guidelines/design-system/design-tokens.json` | Source of truth (JSON) |
| `01-Brand-Guidelines/design-system/layout-templates.json` | Exact coordinates for Power BI |
| `01-Brand-Guidelines/design-system/mob2con.css` | CSS variables mirror |
| `02-Powerbi-Projetos/Mob2Con-Brand-Theme.json` | Power BI theme file |
