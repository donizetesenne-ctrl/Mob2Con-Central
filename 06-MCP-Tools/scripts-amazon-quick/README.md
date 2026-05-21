# Scripts Amazon Quick / MCP

> Scripts Python, PowerShell e Apps Script consolidados aqui em 14/05/2026.
> Origem: estavam soltos no Desktop.

---

## 📜 Inventário

### Python — Apps Script / Forms / Drive
| Script | O que faz |
|---|---|
| `add_config_func.py` | Adiciona função de configuração ao Apps Script |
| `check_forms.py` | Verifica formulários Google Forms vinculados |
| `check_triggers.py` | Verifica triggers do Apps Script |
| `config_script.py` / `config_script2.py` | Configuração inicial do projeto Apps Script |
| `criar_tasks.py` | Cria tasks/cards a partir do sprint |
| `fix_sprint_ic.py` | Corrige inconsistências no sprint IC |
| `ia_orquestradora_mob2con.py` | Orquestrador IA Mob2Con (entry point) |
| `upload_script.py` | Faz upload de scripts ao Apps Script |
| `vincular_form.py` / `vincular_form2.py` | Vincula formulários ao projeto |

### Configurações
| Arquivo | Descrição |
|---|---|
| `sprint_ic_original.json` | Versão original do sprint IC |
| `sprint_ic_script.json` | Sprint IC ativo |
| `sprint_ic_v9.json` | Sprint IC versão 9 |
| `sprint_ic_v9_CODIGO.gs` | Apps Script (Google) — código completo v9 |
| `recent_files_report.csv` | Relatório de arquivos recentes |

### PowerShell
| Script | O que faz |
|---|---|
| `try_fix_q.ps1` | Tentativa de correção do Amazon Q |
| `Configurar-MemoriaVirtual-ADMIN.ps1` | Configura memória virtual (precisa ADMIN) |

### Backups
| Arquivo | Data |
|---|---|
| `sprint_ic_script.json.bak-20260511114018` | 11/05/2026 11:40 |
| `sprint_ic_script.json.bak-20260511114033` | 11/05/2026 11:40 |

---

## 🔧 Como usar

A maioria dos scripts depende de:
- Python 3.x
- Bibliotecas: `google-api-python-client`, `google-auth-oauthlib`
- Credenciais OAuth em `06-MCP-Tools/google-oauth-setup.js` (já configurado)

```cmd
cd 06-MCP-Tools\scripts-amazon-quick
python ia_orquestradora_mob2con.py
```

---

## ⚠️ Importante

Antes de executar qualquer script, conferir se os caminhos hardcoded internos (que apontavam para `Desktop\...`) ainda fazem sentido depois da reorganização. Se algum script usa `os.path.join('Desktop', ...)`, ajustar para apontar para `Mob2Con-Central\...`.
