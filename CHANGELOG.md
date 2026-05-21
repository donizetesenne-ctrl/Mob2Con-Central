# Mob2Con-Central — Changelog

## 2026-05-14 — Design System em 4 camadas + Reorganização

### ✨ Adicionado

#### Design System complementar (`01-Brand-Guidelines/design-system/`)
- **`design-tokens.json`** — fonte única de verdade: cores, tipografia, espaçamento, raios, sombras, canvas
- **`layout-templates.json`** — coordenadas (x, y, w, h) dos 5 templates: executive, operational, analytical, cover, mobile
- **`mob2con.css`** — variáveis CSS + componentes (KPI card, botões, tabela, header, canvas)
- **`index.html`** — preview interativo do sistema completo
- **`templates/executive.html`** — preview canvas 1600 × 900
- **`templates/operational.html`** — preview canvas 1280 × 720
- **`templates/analytical.html`** — preview canvas 1920 × 1080
- **`templates/cover.html`** — preview canvas capa
- **`templates/mobile.html`** — preview canvas 320 × 568
- **`sync-tokens.js`** — verifica e regenera sincronia entre JSON ↔ CSS ↔ Theme PBI
- **`README.md`** — documentação da arquitetura de 4 camadas

#### Catálogo de recursos externos
- **`06-MCP-Tools/RECURSOS-EXTERNOS.md`** — registra Bridge, MCP_Setup, projetos BI legado

### 📦 Reorganizado (movido do Desktop)

#### Para `03-Documentacao/`
- `NORDESTAO_DASHBOARD_PLAN.md`
- `RELATORIO_PRODUCAO_AMAZON_QUICK.md`
- `Relatorio_Producao_Mob2Con_Mai2026.html`
- `analise_analitico_rg_mcp2.html`
- `visual_designer.md`
- `q-dev-chat-2026-05-07.md`
- `fix_sprint_ic.py.analise.md`

#### Para `01-Brand-Guidelines/`
- `Mob2con-Theme.json` → `Mob2con-Theme-desktop-old.json` (backup)

#### Para `02-Powerbi-Projetos/`
- `Mockup Dash Implantação.pbix`

#### Para `06-MCP-Tools/scripts-amazon-quick/` (novo)
- 9 scripts Python (`add_config_func.py`, `check_forms.py`, `check_triggers.py`, `config_script.py`, `config_script2.py`, `criar_tasks.py`, `fix_sprint_ic.py`, `ia_orquestradora_mob2con.py`, `upload_script.py`, `vincular_form.py`, `vincular_form2.py`)
- 4 JSON do sprint IC (`sprint_ic_original.json`, `sprint_ic_script.json`, `sprint_ic_v9.json`) + 2 backups
- 1 Apps Script (`sprint_ic_v9_CODIGO.gs`)
- 2 PowerShell (`try_fix_q.ps1`, `Configurar-MemoriaVirtual-ADMIN.ps1`)
- `recent_files_report.csv`
- `README.md` documentando o inventário

#### Para `06-MCP-Tools/zips-instaladores/` (novo)
- `Melhorias_Amazon_Quick.zip`, `Melhorias_Amazon_Quick_FINAL.zip`
- `Mob2Con-Central-Instalador.zip`
- `Mob2Con_MCP_Setup.zip`, `Mob2Con_Pacote_Completo.zip`
- `quickwork-diagnostics-2026-05-12-192744.zip`
- `ZIPAR_PROJETO.bat`

### ✅ Validado

- `node sync-tokens.js` rodando com sucesso, todas as 4 camadas em sincronia (#F46901 alinhado em JSON, CSS e Theme PBI)
- 22 arquivos do Desktop reorganizados sem conflitos

---

## Versões anteriores

Ver `02-Powerbi-Projetos/CHANGELOG-brand-migration.md` para a migração de marca (Microsoft Blue → Mob2Con Orange).
