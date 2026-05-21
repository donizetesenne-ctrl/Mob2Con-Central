# 🎨 Guia de Uso dos Temas Power BI — Mob2Con

> **Versão:** 1.0 — Maio/2026  
> **Autor:** Equipe Mob2Con  
> **Status:** ✅ Canônico — seguir este guia em todos os projetos

---

## 📦 Temas Disponíveis

| Arquivo | Localização | Quando usar |
|---------|-------------|-------------|
| `Mob2Con-Brand-Theme.json` | `02-Powerbi-Projetos/` | **PADRÃO** — todos os relatórios Mob2Con |
| `Mob2Con-Theme.json` | `01-Brand-Guidelines/` | Alternativo corporativo (mesma paleta) |
| `MobConnect-Theme.json` | `01-Brand-Guidelines/` | Exclusivo para relatórios sobre MobConnect |
| `ReposicaoGarantida-Theme.json` | `01-Brand-Guidelines/` | Combate à Ruptura / Reposição Garantida |

---

## 🏆 Tema Canônico — `Mob2Con-Brand-Theme.json`

**Use este tema em qualquer novo projeto Mob2Con.**  
É o mais completo — cobre 12+ tipos de visual com estilos pré-definidos.

### Como aplicar no Power BI Desktop

1. Abra o relatório `.pbip` no **Power BI Desktop**
2. Vá em **Exibição → Temas → Procurar temas**
3. Navegue até:  
   `C:\Users\Donizete Senne\Desktop\Mob2Con-Central\02-Powerbi-Projetos\Mob2Con-Brand-Theme.json`
4. Clique em **Abrir**
5. Confirme a aplicação

> ⚠️ Após aplicar o tema, verifique visualmente as páginas — alguns visuais com formatação local sobrepõem o tema.

---

## 🗺️ Qual Tema Escolher?

```
Novo relatório
│
├─ É sobre MobConnect (produto)?
│   └─ SIM → MobConnect-Theme.json  (#4285F4 azul)
│
├─ É sobre Reposição Garantida / Combate à Ruptura?
│   └─ SIM → ReposicaoGarantida-Theme.json  (laranja + azul + roxo)
│
└─ Qualquer outro relatório Mob2Con?
    └─ → Mob2Con-Brand-Theme.json  (#F46901 laranja) ← PADRÃO
```

---

## 🎨 Referência Rápida de Cores

### Paleta Principal (todos os temas Mob2Con)

<table>
  <tr>
    <th>Nome</th>
    <th>HEX</th>
    <th>Amostra</th>
    <th>Uso</th>
  </tr>
  <tr>
    <td><strong>Laranja Mob2Con</strong></td>
    <td><code>#F46901</code></td>
    <td>🟠</td>
    <td>KPIs, gauges, headers, destaques — cor primária</td>
  </tr>
  <tr>
    <td><strong>Grafite</strong></td>
    <td><code>#434343</code></td>
    <td>⚫</td>
    <td>Títulos de visual, cabeçalhos de tabela</td>
  </tr>
  <tr>
    <td><strong>Preto</strong></td>
    <td><code>#111111</code></td>
    <td>⬛</td>
    <td>Valores de KPI, texto em alto contraste</td>
  </tr>
  <tr>
    <td><strong>Cinza médio</strong></td>
    <td><code>#605E5C</code></td>
    <td>🔘</td>
    <td>Labels, eixos, texto secundário (9pt)</td>
  </tr>
  <tr>
    <td><strong>Roxo</strong></td>
    <td><code>#6F05D4</code></td>
    <td>🟣</td>
    <td>Acento, elementos secundários</td>
  </tr>
  <tr>
    <td><strong>Verde Sucesso</strong></td>
    <td><code>#107C41</code></td>
    <td>🟢</td>
    <td>Indicadores positivos</td>
  </tr>
  <tr>
    <td><strong>Vermelho Alerta</strong></td>
    <td><code>#C00000</code></td>
    <td>🔴</td>
    <td>Indicadores negativos, ruptura</td>
  </tr>
</table>

### Cores Exclusivas por Produto

| Produto | Cor | HEX | ⚠️ Regra |
|---------|-----|-----|---------|
| **MobConnect** | Azul | `#4285F4` | Exclusivo — não usar em outros contextos |
| **Mob2Con padrão** | Laranja | `#F46901` | Padrão para todo o resto |

---

## 🔤 Tipografia

**Fonte única: Raleway** — obrigatória em todos os projetos.

| Elemento | Peso | Tamanho | Cor |
|----------|------|---------|-----|
| Título da página | Black (900) | 20pt | `#111111` |
| Título de visual | Bold (700) | 14pt | `#434343` |
| Valor de KPI | Black (900) | 28pt | `#111111` |
| Labels / eixos | Regular (400) | 9–10pt | `#605E5C` |
| Subtítulos | Bold (700) | 12pt | `#434343` |

> ❌ **NUNCA** usar Segoe UI, Arial ou qualquer outra fonte.  
> Se Raleway não estiver instalada: https://fonts.google.com/specimen/Raleway

---

## 📐 Layout Padrão

| Parâmetro | Valor |
|-----------|-------|
| Canvas | **1600 × 900px** (Nordestão) / 1280×720px (padrão) |
| Fundo da página | `#F3F6FA` |
| Outspace | `#E2E8F0` |
| Fundo de visuais / cards | `#FFFFFF` |
| Borda de KPI cards | `#CBD5E1` — radius 10px |
| Borda de gráficos | `#E2E8F0` |
| Gap entre visuais | 16px |
| Margem de página | 16px |

---

## 🗂️ Projetos Ativos e Tema Aplicado

| Projeto | Tema Aplicado | Status |
|---------|--------------|--------|
| `Nordestão Exclusivo dn.pbip` | `Mob2Con` (customTheme) | ✅ Ativo |
| `Acompanhamento Captação RG 2.0.pbip` | A verificar | ⚠️ Checar |
| `Analítico RG 2.0.pbip` | A verificar | ⚠️ Checar |
| `Mockup Dash Implantação.pbip` | A verificar | ⚠️ Checar |

---

## ✅ Checklist Antes de Publicar

- [ ] Tema `Mob2Con-Brand-Theme.json` aplicado
- [ ] Fonte **Raleway** em todos os visuais
- [ ] Laranja `#F46901` como cor primária (ou `#4285F4` se MobConnect)
- [ ] Fundo da página: `#F3F6FA`
- [ ] KPI principal no **topo esquerdo** (Z-pattern)
- [ ] Máximo 5 cores por página
- [ ] Contraste mínimo 4.5:1 texto/fundo
- [ ] Títulos curtos — sem truncamento ("...")
- [ ] Espaçamento consistente entre visuais (16px)

---

## 🔗 Arquivos de Referência

```
Mob2Con-Central/
├── 01-Brand-Guidelines/
│   ├── Mob2con-brand-guidelines.md   ← paleta, tipografia, regras
│   ├── Mob2con-brand-context.md      ← Z-pattern, layout, checklist
│   ├── Mob2Con-Theme.json            ← tema alternativo corporativo
│   ├── MobConnect-Theme.json         ← tema azul (MobConnect)
│   └── ReposicaoGarantida-Theme.json ← tema Reposição Garantida
│
└── 02-Powerbi-Projetos/
    └── Mob2Con-Brand-Theme.json      ← ⭐ TEMA CANÔNICO (usar este)
```

---

*Gerado automaticamente — Amazon Quick + Mob2Con Brand System*
