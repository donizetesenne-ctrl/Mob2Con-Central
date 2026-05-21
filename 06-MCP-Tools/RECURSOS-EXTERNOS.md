# 🔗 Recursos Externos do Projeto Mob2Con

> Este arquivo cataloga **pastas e executáveis grandes** que ficam fora da `Mob2Con-Central` por questão de tamanho/peso, mas são parte integral do projeto MCP/Amazon Quick.
> Atualizado: 2026-05-14

---

## 🌉 Mob2Con Bridge v2.0.0 (executável principal)

**Localização:** `C:\Users\Donizete Senne\Downloads\Mob2Con-Bridge-v2.0.0\`
**Tamanho aproximado:** ~270 MB (incluindo Python empacotado)

```
Mob2Con-Bridge-v2.0.0/
├── bridge/
│   └── mob2con-bridge.exe          ← Executável principal — porta 3333
├── mcp/
│   ├── powerbi-layout-mcp/
│   │   ├── server.js               ← MCP Node.js de layout (corrigido 11/05)
│   │   ├── Mob2con-brand-context.md
│   │   └── Mob2con-layout-base.md
│   ├── server.js                   ← MCP bridge principal
│   └── mcp-powerbi.js
├── docs/
│   ├── README.md
│   ├── KIRO.md
│   └── CLAUDE.md
├── drive-queue/                    ← Fila Google Drive (inbox/running/done/error)
├── vsix/                           ← Extensões VS Code
├── iniciar-bridge.bat
├── iniciar-tudo.bat                ← USE ESTE — sobe bridge + queue
├── configurar-mcp.ps1
└── install-standalone.ps1
```

### Como iniciar
```cmd
"C:\Users\Donizete Senne\Downloads\Mob2Con-Bridge-v2.0.0\iniciar-tudo.bat"
```

### Endpoints HTTP (porta 3333)
- `GET  /health`
- `GET  /tools`
- `POST /tools/call`
- `GET  /model/tables` · `/model/measures` · `/model/relationships`
- `POST /model/query` · `/model/measures` · `/model/analyze`
- `POST /visuals/{card,bar-chart,column-chart,line-chart,area-chart,combo-chart,pie-chart,donut-chart,scatter-chart,table,matrix,slicer,kpi,gauge,waterfall,treemap,funnel,branded,page}`
- `GET  /branding/info` · `/branding/theme`
- `POST /branding/apply-theme`
- `POST /drive-queue/submit`
- `GET  /drive-queue/status/:id` · `/drive-queue/list`

---

## 📦 Mob2Con_MCP_Setup (instalação MCP completa)

**Localização:** `C:\Users\Donizete Senne\Desktop\Mob2Con_MCP_Setup\`
**Tamanho aproximado:** ~270 MB

Pacote de instalação do MCP — manter onde está. Para reinstalar:
```cmd
"C:\Users\Donizete Senne\Desktop\Mob2Con_MCP_Setup\install.bat"  (verificar nome real)
```

---

## 🛠️ powerbi-layout-mcp (MCP standalone antigo)

**Localização:** `C:\Users\Donizete Senne\Desktop\powerbi-layout-mcp\`
**Tamanho aproximado:** ~36 MB
**Status:** ⚠️ Versão antiga — substituída pela versão dentro do `Mob2Con-Bridge-v2.0.0/mcp/powerbi-layout-mcp/`. Manter como referência/backup.

---

## 🌐 universal-control-mcp

**Localização:** `C:\Users\Donizete Senne\Desktop\universal-control-mcp\`
**Tamanho aproximado:** ~33 KB

MCP universal (Sheets, Drive, Excel — 53 tools).

---

## 📊 projetos BI (legado)

**Localização:** `C:\Users\Donizete Senne\Desktop\projetos BI\`
**Tamanho aproximado:** ~16 MB

Pasta antiga de projetos Power BI. Os `.pbip` foram movidos para `02-Powerbi-Projetos/`. Manter `projetos BI/` como histórico até confirmar que nada quebrou.

> 🔄 **Sugestão:** após validar tudo funcionando, mover `projetos BI/*.Report` e `*.SemanticModel` para `02-Powerbi-Projetos/` ou apagar.

---

## 🐍 projeto/ (MCPs universais)

**Localização:** `C:\Users\Donizete Senne\Desktop\projeto\`
**Tamanho aproximado:** ~234 MB

Pasta com instâncias antigas dos MCPs universais. Manter como backup.

---

## 🗂️ Arquivos do Amazon Quick consolidados na Central

Movidos do Desktop em 14/05/2026:

| Arquivo | Destino |
|---|---|
| Scripts Python (`add_config_func.py`, `check_forms.py`, `criar_tasks.py`, `ia_orquestradora_mob2con.py`, etc) | `06-MCP-Tools/scripts-amazon-quick/` |
| Configurações Sprint IC (`sprint_ic_script.json`, `sprint_ic_v9.json`, etc) | `06-MCP-Tools/scripts-amazon-quick/` |
| Apps Script (`sprint_ic_v9_CODIGO.gs`) | `06-MCP-Tools/scripts-amazon-quick/` |
| ZIPs e instaladores | `06-MCP-Tools/zips-instaladores/` |
| Relatórios HTML/MD | `03-Documentacao/` |
| Plano dashboard Nordestão | `03-Documentacao/NORDESTAO_DASHBOARD_PLAN.md` |
| Tema PBI alternativo | `01-Brand-Guidelines/Mob2con-Theme-desktop-old.json` |

---

## ⚙️ Configuração MCP atual

**Caminho:** `C:\Users\Donizete Senne\.kiro\settings\mcp.json`

Aponta para:
- `aws-docs` (uvx)
- `powerbi-layout` (Node.js — `Downloads\Mob2Con-Bridge-v2.0.0\mcp\powerbi-layout-mcp\server.js`)
- Variáveis ambiente:
  - `POWERBI_PROJECT_PATH`: aponta para `02-Powerbi-Projetos\Nordestão Exclusivo dn.pbip`
  - `MOB2CON_BRAND_CONTEXT`: aponta para `01-Brand-Guidelines\Mob2con-brand-guidelines.md`
  - `MOB2CON_LAYOUT_BASE`: aponta para `01-Brand-Guidelines\Mob2con-layout-base.md`

> 💡 **Próximo passo opcional:** atualizar `MOB2CON_BRAND_CONTEXT` para apontar para o JSON novo do design-system, que é mais estruturado:
> ```
> "MOB2CON_BRAND_CONTEXT": "...01-Brand-Guidelines\\design-system\\design-tokens.json"
> "MOB2CON_LAYOUT_BASE":   "...01-Brand-Guidelines\\design-system\\layout-templates.json"
> ```
