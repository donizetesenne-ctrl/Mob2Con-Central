# Mob2Con-Central — Product Summary

Mob2Con-Central is the consolidated workspace for **Mob2Con**, a Brazilian company that builds Power BI dashboards and data pipelines for retail/logistics clients.

## What it does

- Manages Power BI dashboard projects (.pbip/.pbix) with a strict brand identity
- Syncs data from Amazon Redshift to Google Sheets for dashboard consumption
- Provides a 4-layer design system (JSON tokens → CSS → HTML previews → PBI Theme) ensuring brand consistency
- Integrates with MCP tools (powerbi-layout, powerbi-bridge, universal-control) for AI-assisted dashboard authoring

## Key products/clients

- **Reposição Garantida (RG)** — supply chain / stock replenishment dashboards
- **MobConnect** — a separate product line that uses blue (#4285F4) instead of orange
- **Nordestão** — retail client with exclusive dashboards

## Brand identity (critical rules)

- Primary color: Orange `#F46901` — always the main accent
- Blue `#4285F4` is **exclusively** for MobConnect reports — never use elsewhere
- Never use Microsoft blue `#0078D4` — it was fully deprecated
- Font: **Raleway** only (weights 400, 700, 900) — never Segoe UI or Arial
- Layout follows Z-pattern with 8px grid spacing on 1280×720 canvas

## Language

- All documentation, comments, and commit messages are in **Brazilian Portuguese (pt-BR)**
- Code identifiers (variables, functions) use English
- File and folder names use Portuguese descriptive names or English technical names
