# Mob2Con-Central — Tech Stack

## Languages

- **Python 3** — data pipelines (Redshift → Sheets sync, data extraction)
- **JavaScript/Node.js** — design system tooling, MCP wrappers, OAuth setup
- **DAX** — Power BI measures and calculated columns
- **Power Query (M)** — data transformations inside Power BI
- **PowerShell / Batch** — Windows automation, scheduled tasks, installers
- **Google Apps Script** — Sheets/Forms automation, web apps
- **HTML/CSS** — design system previews, dashboard web views

## Key libraries (Python)

- `psycopg2-binary` — Redshift/PostgreSQL connection
- `gspread` — Google Sheets API
- `google-auth` / `google-auth-oauthlib` — Google authentication
- `pandas` — data manipulation

## MCP Servers (AI tool integrations)

| Server | Purpose |
|--------|---------|
| powerbi-layout | Visual positioning (x/y/width/height) in PBIR reports |
| powerbi-bridge | Full semantic model operations (measures, tables, relationships) |
| universal-control | Google Sheets, Drive, Docs, Gmail, Calendar |
| filesystem | Local file read/write within workspace |
| shell-command | Shell execution |
| aws-docs | AWS documentation lookup |

## Power BI project format

- Uses `.pbip` (Power BI Project) format with separate `.Report/` and `.SemanticModel/` folders
- Theme files are `.json` applied via View → Themes → Browse
- Canvas sizes: 1280×720 (standard), 1600×900 (executive/cover), 1920×1080 (analytical), 320×568 (mobile)

## Common commands

```cmd
# Verify design system sync (tokens ↔ CSS ↔ theme)
cd 01-Brand-Guidelines\design-system
node sync-tokens.js

# Regenerate CSS from tokens
node sync-tokens.js --apply

# Install Python dependencies
pip install -r requirements_dashboard.txt

# Run Redshift → Sheets sync
python sync_redshift_to_sheets.py

# Run daily sync (multi-sheet)
python sync_redshift_multi_sheets.py
```

## Environment

- OS: Windows 10/11
- Shell: cmd / PowerShell
- Python virtualenv at `.venv/`
- Config files: `redshift_config.json`, `spreadsheets_config.json`
- Credentials: Google service account JSON (not in repo)
