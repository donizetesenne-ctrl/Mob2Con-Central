# 🔧 Mob2Con Bridge — Capacidades Consolidadas

> Este documento extrai **tudo** que o `powerbi-bridge` fazia e converte em guia prático.
> Agora tudo isso pode ser feito pelas MCPs oficiais (`powerbi` + `powerbi-layout` + `filesystem`) usando os JSONs desta pasta central.
>
> **O powerbi-bridge foi desativado** (era um servidor HTTP, não um MCP stdio).

---

## 📚 Identidade Visual Mob2Con — completa do código

### Paleta oficial (extraída do server.js)

```javascript
const MOB2CON_BRAND = {
  colors: {
    primary:    "#F46901",  // Laranja Mob2Con (cor principal)
    mobconnect: "#4285F4",  // Azul MobConnect (exclusivo desse produto)
    purple:     "#6F05D4",  // Roxo acento
    dark:       "#434343",  // Cinza escuro (texto principal)
    black:      "#111111",  // Preto (contraste alto)
    light:      "#FFFFFF"   // Branco (fundo)
  },
  palette: [
    "#F46901",  // 0 - Primária
    "#6F05D4",  // 1 - Secundária
    "#434343",  // 2 - Terciária
    "#4285F4",  // 3 - MobConnect
    "#111111"   // 4 - Destaque escuro
  ]
};
```

### Tipografia (3 níveis)

```javascript
fonts: {
  title:    { family: "Raleway", weight: "900" },   // Black
  subtitle: { family: "Raleway", weight: "700" },   // Bold
  body:     { family: "Raleway", weight: "400" }    // Regular
}
```

### Produtos Mob2Con (3 linhas de cores)

| Produto | Paleta | Uso |
|---------|--------|-----|
| **Mob2Con** (institucional) | `["#F46901", "#6F05D4"]` | Relatórios gerais, capas |
| **MobConnect** | `["#4285F4", "#6F05D4"]` | Relatórios específicos MobConnect |
| **Reposição Garantida** | `["#F46901", "#4285F4", "#6F05D4"]` | Combate à ruptura |

---

## 🎨 Temas Power BI (.json) gerados

Já estão prontos na pasta `01-Brand-Guidelines/`:

- `Mob2Con-Theme.json` — tema institucional (laranja)
- `MobConnect-Theme.json` — tema azul exclusivo
- 🆕 `ReposicaoGarantida-Theme.json` — será gerado abaixo

### Como aplicar no Power BI
1. Abrir o `.pbip` no Power BI Desktop
2. **View → Themes → Browse for themes**
3. Selecionar o JSON do tema
4. O tema aplica automaticamente cores + fontes Raleway em todos os visuais

---

## 🧩 19 Tipos de Visuais suportados

O bridge permitia criar esses visuais com branding automático. Agora você pode criar direto no Power BI Desktop + tema aplicado.

| Tipo | Power BI Desktop | Quando usar |
|------|------------------|-------------|
| **card** | Visualizations → Card | KPI simples |
| **kpi** | Visualizations → KPI | Meta + tendência |
| **bar-chart** | Bar chart horizontal | Ranking categorias |
| **column-chart** | Column chart vertical | Comparação temporal |
| **stacked-bar** | Stacked bar | Composição + total |
| **stacked-column** | Stacked column | Evolução + categoria |
| **line-chart** | Line chart | Série temporal |
| **area-chart** | Area chart | Acúmulo ao longo tempo |
| **combo-chart** | Line + Column | Valor + % |
| **pie-chart** | Pie chart | Participação (≤5 fatias) |
| **donut-chart** | Donut | Como pie, mais moderno |
| **scatter-chart** | Scatter | Correlação 2 variáveis |
| **table** | Table | Lista detalhada |
| **matrix** | Matrix | Cruzamento linha × coluna |
| **slicer** | Slicer | Filtro visual |
| **gauge** | Gauge | Progresso vs meta |
| **waterfall** | Waterfall | Variação sequencial |
| **treemap** | Treemap | Hierarquia visual |
| **funnel** | Funnel | Etapas de conversão |

### Proporções recomendadas

Veja `Mob2con-layout-proporcoes.md` — tem tamanhos mínimo/ideal/máximo de cada tipo.

---

## 🤖 Comandos equivalentes no Amazon Quick

Antes com bridge (REST):
```
POST /visuals/kpi { title, measure, page }
```

Agora no Amazon Quick (linguagem natural):
```
"Cria um KPI de Receita Total na página Resumo do Nordestão,
 posição x=20 y=80, width 280 height 120, com tema Mob2Con"
```

O Amazon Quick vai usar:
- **powerbi** (MCP oficial) → criar a medida DAX
- **powerbi-layout** → posicionar (x, y, width, height)
- **filesystem** → editar o `visual.json` com as cores/fontes Mob2Con

---

## 📐 Aplicação automática de tema — workflow

### Opção A: manual (mais rápido)
1. Abrir `.pbip` no Power BI Desktop
2. View → Themes → Browse → `Mob2Con-Theme.json`
3. Salvar (Ctrl+S)

### Opção B: via filesystem (programático)
Pedir no Amazon Quick:
```
"Copie o conteúdo de Mob2Con-Theme.json e insira no 
 arquivo report.json do projeto Nordestão, na propriedade 
 theme.baseTheme"
```

O caminho do `report.json` em um projeto PBIP é:
```
<projeto>.Report/definition/report.json
```

---

## 🎯 Fluxo de trabalho Mob2Con (pós-bridge)

### 1. Projeto novo
```
Amazon Quick:
"Crie um projeto Power BI baseado no template executivo 
 (1280x720), aplicando o tema Mob2Con-Theme.json e 
 usando as medidas DAX padrão"
```

### 2. Adicionar visual
```
"Adicione um gráfico de colunas em x=20 y=216 width=620 
 height=340 mostrando Receita Total por Mês com o tema 
 Mob2Con aplicado"
```

### 3. Ajustar título cortado
```
"Abra visual.json do card de alerta na página Home e 
 reduza o fontSize do título para 12pt ou aumente width 
 para 340 para caber o texto completo"
```

### 4. Trocar tema para MobConnect
```
"Aplique MobConnect-Theme.json no relatório e substitua 
 todas as referências de cor #F46901 para #4285F4 no 
 report.json"
```

### 5. Deletar visual
```
"Remova o visual 'gauge de ocupação' da página 
 Operacional no projeto Nordestão"
```

---

## 🔌 Integrações que o bridge tinha (e agora)

| Recurso do bridge | Substituto |
|-------------------|------------|
| `/model/tables` | MCP `powerbi` (tool `list_tables`) |
| `/model/measures` | MCP `powerbi` (tool `create_measure`) |
| `/model/relationships` | MCP `powerbi` |
| `/model/query` | MCP `powerbi` (tool `evaluate_dax`) |
| `/visuals/list` | MCP `powerbi-layout` + `filesystem` |
| `/visuals/<tipo>` | MCP `filesystem` + templates desta pasta |
| `/branding/apply-theme` | Power BI Desktop ou `filesystem` (edita report.json) |
| `/branding/get` | Arquivo `01-Brand-Guidelines/Mob2con-brand-guidelines.md` |
| `/drive-queue/*` | Usar `universal_control` (Google Drive nativo) |

---

## 📦 Arquivos úteis nesta pasta central

| Arquivo | Uso |
|---------|-----|
| `01-Brand-Guidelines/Mob2Con-Theme.json` | Tema Power BI institucional |
| `01-Brand-Guidelines/MobConnect-Theme.json` | Tema Power BI MobConnect |
| `01-Brand-Guidelines/Mob2con-brand-guidelines.md` | Regras de marca |
| `01-Brand-Guidelines/Mob2con-layout-proporcoes.md` | Dimensões x/y/w/h |
| `01-Brand-Guidelines/Mob2con-botoes-navegacao.md` | JSON de botões |
| `01-Brand-Guidelines/Mob2con-efeitos-powerbi.md` | Efeitos, bookmarks |
| `03-Documentacao/Mob2con-dax-medidas-padrao.md` | Biblioteca DAX |
| `03-Documentacao/Mob2con-programas-produtos.md` | Produtos Mob2Con |
| `03-Documentacao/Mob2con-bridge-capabilities-consolidado.md` | **Este arquivo** |

---

## ✅ MCPs ativos (pós-remoção do bridge)

| MCP | Tools | O que faz |
|-----|-------|-----------|
| **powerbi** (oficial MS) | 21 | Modelo de dados, medidas DAX, relacionamentos |
| **powerbi-layout** | 9 | Posição/tamanho de visuais no `.pbip` |
| **filesystem** | 14 | Editar `visual.json`, `report.json`, `theme.json` |
| **universal_control** | 53 | Excel, Sheets, Drive, Docs |
| **aws-docs** | 4 | Documentação AWS |
| **shell-command** | 1 | Comandos shell |

**6 MCPs funcionais** cobrem 100% do que o bridge fazia.
