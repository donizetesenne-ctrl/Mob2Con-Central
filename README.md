# 📁 Mob2Con-Central — Workspace Consolidado

> Workspace único com **tudo** para uso com Amazon Quick, Kiro e MCPs Power BI.
> Atualizado: 14 de Maio de 2026

---

## 🆕 O que mudou (14/05/2026)

- ✅ **Design System em 4 camadas** complementares (`01-Brand-Guidelines/design-system/`) — JSON + CSS + HTML + Theme PBI que se complementam
- ✅ **Arquivos perdidos do Amazon Quick** consolidados em `06-MCP-Tools/scripts-amazon-quick/` e `06-MCP-Tools/zips-instaladores/`
- ✅ **Relatórios e planos** movidos para `03-Documentacao/`
- ✅ **Recursos externos grandes** (Bridge, MCP_Setup) catalogados em `06-MCP-Tools/RECURSOS-EXTERNOS.md`

---

## 🗂️ Estrutura

```
Mob2Con-Central/
├── README.md                              ← este arquivo
├── INSTALAR.bat
├── Instalar-Mob2Con.ps1
├── GUIA-INSTALACAO.md
│
├── 01-Brand-Guidelines/                   🎨 Identidade visual
│   ├── Mob2con-brand-guidelines.md
│   ├── Mob2con-brand-context.md
│   ├── Mob2con-layout-base.md
│   ├── Mob2con-layout-proporcoes.md
│   ├── Mob2con-botoes-navegacao.md
│   ├── Mob2con-efeitos-powerbi.md
│   ├── Mob2Con-Theme.json                 (tema PBI principal)
│   ├── MobConnect-Theme.json
│   ├── ReposicaoGarantida-Theme.json
│   ├── Mob2con-Theme-desktop-old.json     (backup do Desktop)
│   └── design-system/                     🆕 Sistema de 4 camadas
│       ├── README.md
│       ├── design-tokens.json             (camada 1 - tokens)
│       ├── layout-templates.json          (camada 1 - layouts)
│       ├── mob2con.css                    (camada 2 - CSS)
│       ├── index.html                     (camada 3 - preview)
│       ├── sync-tokens.js                 (verifica sincronia)
│       └── templates/                     (5 previews HTML)
│           ├── executive.html
│           ├── operational.html
│           ├── analytical.html
│           ├── cover.html
│           └── mobile.html
│
├── 02-Powerbi-Projetos/                   📊 Projetos .pbip
│   ├── Mob2Con-Brand-Theme.json
│   ├── Acompanhamento Captação RG 2.0.pbip
│   ├── Analítico RG 2.0.pbip
│   ├── Mockup Dash Implantação.pbip
│   ├── Mockup Dash Implantação.pbix
│   ├── Nordestão Exclusivo dn.pbip
│   ├── *.Report/  *.SemanticModel/
│   └── CHANGELOG-brand-migration.md
│
├── 03-Documentacao/                       📚 Docs e relatórios
│   ├── README.md
│   ├── MOB2CON_PROJETO_COMPLETO.md
│   ├── GUIA-TEMAS-POWERBI.md
│   ├── Mob2con-bridge-capabilities-consolidado.md
│   ├── Mob2con-dax-medidas-padrao.md
│   ├── Mob2con-programas-produtos.md
│   ├── NORDESTAO_DASHBOARD_PLAN.md        🆕
│   ├── RELATORIO_PRODUCAO_AMAZON_QUICK.md 🆕
│   ├── Relatorio_Producao_Mob2Con_Mai2026.html 🆕
│   ├── analise_analitico_rg_mcp2.html     🆕
│   ├── visual_designer.md                 🆕
│   ├── q-dev-chat-2026-05-07.md           🆕
│   └── fix_sprint_ic.py.analise.md        🆕
│
├── 04-Dados-Fontes/                       📈 Bases Excel
│   ├── Mob2Con_Base_Consolidada_PowerBI.xlsx
│   └── Mob2Con_Base_Implantacao_v2.xlsx
│
├── 05-Apresentacoes/                      🎥 PPT
│   └── Apresentação Modelo Mob2con (1).pptx
│
└── 06-MCP-Tools/                          🔧 MCP, scripts, instaladores
    ├── RECURSOS-EXTERNOS.md               🆕 índice de recursos grandes
    ├── google-oauth-setup.js
    ├── powerbi-bridge-wrapper.js
    ├── quickwork-mcp-central.json
    ├── patch-validacao-api.md
    ├── specs/
    │   └── powerbi-layout-mcp-authoring/
    ├── scripts-amazon-quick/              🆕 scripts Python/PS1
    │   ├── README.md
    │   ├── add_config_func.py · check_forms.py · check_triggers.py
    │   ├── config_script.py · criar_tasks.py · fix_sprint_ic.py
    │   ├── ia_orquestradora_mob2con.py · upload_script.py
    │   ├── vincular_form.py · vincular_form2.py
    │   ├── sprint_ic_*.json · sprint_ic_v9_CODIGO.gs
    │   └── try_fix_q.ps1 · Configurar-MemoriaVirtual-ADMIN.ps1
    └── zips-instaladores/                 🆕 ZIPs e instaladores
        ├── Melhorias_Amazon_Quick.zip
        ├── Melhorias_Amazon_Quick_FINAL.zip
        ├── Mob2Con-Central-Instalador.zip
        ├── Mob2Con_MCP_Setup.zip
        ├── Mob2Con_Pacote_Completo.zip
        ├── quickwork-diagnostics-2026-05-12-192744.zip
        └── ZIPAR_PROJETO.bat
```

---

## 🧱 Design System em 4 camadas (NOVO)

Para garantir que se uma camada falhar, as outras continuam mantendo a marca:

| # | Camada | Para quê |
|---|---|---|
| 1 | `design-tokens.json` + `layout-templates.json` | **Fonte da verdade**. Lido por MCPs e scripts. |
| 2 | `mob2con.css` | Espelho web — variáveis CSS com as mesmas cores. Garante marca em qualquer HTML. |
| 3 | `index.html` + `templates/*.html` | **Preview visual** — vê o dashboard sem abrir Power BI. |
| 4 | `02-Powerbi-Projetos/Mob2Con-Brand-Theme.json` | Formato Microsoft — aplicado via View → Themes → Browse. |

### Como abrir o preview
Duplo-clique em `01-Brand-Guidelines/design-system/index.html`

### Como verificar sincronia entre as 4 camadas
```cmd
cd 01-Brand-Guidelines\design-system
node sync-tokens.js
```

### Como regenerar CSS após editar JSON
```cmd
node sync-tokens.js --apply
```

Documentação completa: [`01-Brand-Guidelines/design-system/README.md`](01-Brand-Guidelines/design-system/README.md)

---

## 🎨 Identidade Visual (resumo)

| Cor | HEX | Uso |
|-----|-----|-----|
| 🟠 Laranja | `#F46901` | Primária Mob2Con |
| ⬛ Grafite | `#434343` | Títulos, bordas |
| ⬛ Preto | `#111111` | Texto, KPIs |
| 🔵 Azul | `#4285F4` | **EXCLUSIVO MobConnect** |
| 🟣 Roxo | `#6F05D4` | Acento secundário |
| 🟢 Sucesso | `#107C41` | Indicadores positivos |
| 🔴 Alerta | `#C00000` | Indicadores negativos |

**Tipografia:** Raleway — Black (títulos), Bold (subtítulos), Regular (corpo)

---

## 🔧 Como usar com Amazon Quick / Kiro

### Aplicar tema no Power BI
1. Abrir `.pbip` em `02-Powerbi-Projetos/`
2. View → Themes → Browse for themes
3. Selecionar `02-Powerbi-Projetos/Mob2Con-Brand-Theme.json`

### Pedir ao agente
```
"Aplica o template Executivo do design-system no Nordestão"
"Recalcula coordenadas dos KPIs do Analítico RG seguindo layout-templates.json"
"Adiciona as medidas DAX padrão do Mob2Con na tabela _Medidas"
```

---

## 🌉 Recursos externos (não duplicados aqui)

Pastas grandes que ficam onde estão e estão catalogadas em:
[`06-MCP-Tools/RECURSOS-EXTERNOS.md`](06-MCP-Tools/RECURSOS-EXTERNOS.md)

- Mob2Con-Bridge-v2.0.0 (Downloads — 270 MB) — executável principal porta 3333
- Mob2Con_MCP_Setup (Desktop — 270 MB)
- powerbi-layout-mcp standalone (Desktop — 36 MB) — versão antiga
- universal-control-mcp (Desktop — 33 KB)
- projetos BI legado (Desktop — 16 MB)

---

## 🧭 Localização

```
C:\Users\Donizete Senne\Desktop\Mob2Con-Central\
```

---

## 📞 MCPs ativos

- ✅ **aws-docs** (4 tools) — documentação AWS
- ✅ **powerbi-layout** (9 tools) — x/y/width/height
- ✅ **powerbi-bridge** (60+ tools) — modelagem, medidas, visuais, branding
- ✅ **universal_control** (53 tools) — Sheets, Drive, Excel
- ✅ **filesystem** (14 tools) — esta pasta incluída
- ✅ **shell-command** (1 tool) — execução

Configuração: `C:\Users\Donizete Senne\.kiro\settings\mcp.json`
