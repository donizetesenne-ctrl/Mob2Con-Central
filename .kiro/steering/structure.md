# Mob2Con-Central — Project Structure

## Top-level layout

```
Mob2Con-Central/
├── 01-Brand-Guidelines/     🎨 Visual identity, themes, design system
├── 02-Powerbi-Projetos/     📊 Power BI .pbip projects and themes
├── 03-Documentacao/         📚 Documentation, guides, reports
├── 04-Dados-Fontes/         📈 Source data (Excel bases)
├── 05-Apresentacoes/        🎥 PowerPoint presentations
├── 06-MCP-Tools/            🔧 MCP configs, scripts, installers
├── agent-manager-for-q-cli/ 🤖 Amazon Q CLI agent manager
├── logs/                    📝 Execution logs
├── .kiro/                   ⚙️ Kiro IDE configuration
├── .venv/                   🐍 Python virtual environment
└── *.py / *.bat / *.ps1     🔄 Root-level automation scripts
```

## Folder responsibilities

### `01-Brand-Guidelines/`
- `Mob2con-brand-context.md` — full visual identity rules (colors, fonts, Z-pattern, spacing)
- `Mob2con-brand-guidelines.md` — brand guidelines document
- `Mob2Con-Theme.json` — Power BI theme (main)
- `design-system/` — 4-layer design system:
  - `design-tokens.json` — single source of truth (colors, fonts, spacing)
  - `layout-templates.json` — visual coordinates for 5 dashboard templates
  - `mob2con.css` — CSS mirror of tokens
  - `sync-tokens.js` — sync verification tool
  - `templates/*.html` — visual previews per template type

### `02-Powerbi-Projetos/`
- `.pbip` files — Power BI project files (open with PBI Desktop)
- `.Report/` folders — report definitions (pages, visuals, layout JSON)
- `.SemanticModel/` folders — data models (tables, measures, relationships)
- `Mob2Con-Brand-Theme.json` — official theme applied to all projects

### `03-Documentacao/`
- Project documentation, production reports, guides
- DAX patterns: `Mob2con-dax-medidas-padrao.md`
- Product catalog: `Mob2con-programas-produtos.md`
- Bridge capabilities: `Mob2con-bridge-capabilities-consolidado.md`

### `04-Dados-Fontes/`
- Excel source files used by Power BI models
- `Mob2Con_Base_Consolidada_PowerBI.xlsx` — main consolidated base

### `06-MCP-Tools/`
- `scripts-amazon-quick/` — Python/PS1 automation scripts
- `zips-instaladores/` — packaged installers and ZIPs
- `specs/` — MCP tool specifications
- Google OAuth and bridge wrapper scripts

## Naming conventions

- Folders use numbered prefixes (`01-`, `02-`, etc.) for logical ordering
- Markdown docs use `Mob2con-` prefix for brand-related files
- Power BI themes use `-Theme.json` suffix
- Python scripts use `snake_case`
- Config files use `snake_case.json`

## Key config files (root)

| File | Purpose |
|------|---------|
| `redshift_config.json` | Redshift connection settings |
| `spreadsheets_config.json` | Google Sheets target mapping |
| `requirements_dashboard.txt` | Python pip dependencies |
| `INSTALAR.bat` / `Instalar-Mob2Con.ps1` | One-click setup scripts |
