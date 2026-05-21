# 📊 SISTEMA DE RELATÓRIO SEMANAL AUTOMÁTICO — Mob2Con

> **Automação robusta e completa**: Você joga texto no Google Docs durante a semana, na sexta-feira o sistema gera e envia relatório HTML formatado automaticamente.

---

## 🎯 O QUE FAZ

1. **Você escreve** no Google Docs durante a semana (texto livre, bullets, o que quiser)
2. **Python processa** o texto com IA (detecta datas, categorias, tags)
3. **Apps Script gera** HTML formatado igual ao modelo que você mostrou
4. **Email automático** toda sexta-feira para sua gestora

---

## 🏗️ ARQUITETURA

```
┌─────────────────────────────────────────────────────────────┐
│  VOCÊ (Segunda a Quinta)                                    │
│  ↓                                                           │
│  Google Docs "Mob2Con - Diário de Produção Semanal"        │
│  • Joga texto livre do que fez no dia                      │
│  • Pode ser bullets, parágrafos, qualquer formato          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PYTHON (Sexta 16:00 - via Task Scheduler)                 │
│  ↓                                                           │
│  relatorio_semanal_auto.py                                  │
│  • Lê Google Docs via API                                  │
│  • Detecta datas, categorias, tags automaticamente         │
│  • Gera JSON estruturado                                    │
│  • Salva no Drive                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  APPS SCRIPT (Sexta 17:00 - Trigger automático)            │
│  ↓                                                           │
│  relatorio_semanal_apps_script.gs                           │
│  • Lê JSON do Drive                                         │
│  • Gera HTML formatado (igual ao modelo)                   │
│  • Envia email para gestora                                 │
│  • Salva HTML no Drive                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  EMAIL GESTORA (Sexta 17:00)                                │
│  📊 Relatório Semanal Mob2Con — 12/05 – 16/05              │
│  • HTML formatado com cores Mob2Con                         │
│  • Timeline de entregas                                     │
│  • Resumo por categoria                                     │
│  • Pendências destacadas                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 INSTALAÇÃO

### 1️⃣ Instalar Python e Dependências

```bash
# Verificar Python 3.8+
python --version

# Instalar dependências
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dateutil
```

### 2️⃣ Configurar Google Cloud Project

1. Acesse: https://console.cloud.google.com/
2. Crie novo projeto: "Mob2Con Relatórios"
3. Habilite APIs:
   - Google Docs API
   - Google Drive API
   - Google Sheets API (opcional)
4. Credentials → Create Credentials → OAuth 2.0 Client ID
5. Application type: Desktop app
6. Baixe `credentials.json`
7. Salve em: `C:\Users\Donizete Senne\.aws\amazonq\universal-control\google-credentials.json`

### 3️⃣ Primeira Execução (Autorização)

```bash
cd "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick"

python relatorio_semanal_auto.py --setup
# Vai abrir navegador para autorizar
# Token será salvo automaticamente
```

### 4️⃣ Configurar Apps Script

1. Abra qualquer Google Sheets (ou crie um novo)
2. Extensions → Apps Script
3. Cole o conteúdo de `relatorio_semanal_apps_script.gs`
4. **IMPORTANTE**: Edite as linhas 18-20:
   ```javascript
   EMAIL_GESTORA: 'email.gestora@empresa.com',  // ⚠️ PREENCHER
   NOME_GESTORA: 'Nome da Gestora',             // ⚠️ PREENCHER
   ```
5. Salve (Ctrl+S)
6. Execute `gerarRelatorioSemanal` uma vez para autorizar
7. Triggers (relógio) → + Add Trigger:
   - Function: `gerarRelatorioSemanal`
   - Event source: Time-driven
   - Type: Week timer
   - Day: Friday
   - Time: 5pm to 6pm

### 5️⃣ Agendar Python (Windows Task Scheduler)

```powershell
# Abrir Task Scheduler
taskschd.msc

# Criar nova tarefa:
# Nome: Mob2Con - Processar Relatório Semanal
# Trigger: Semanal, Sexta-feira, 16:00
# Action: Start a program
#   Program: C:\Python\python.exe
#   Arguments: "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick\relatorio_semanal_auto.py"
#   Start in: C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick
```

---

## 📝 COMO USAR

### Durante a Semana (Segunda a Quinta)

Abra o Google Docs: **"Mob2Con - Diário de Produção Semanal"**

Jogue o que você fez no dia (formato livre):

```
---
[DATA] Segunda 12/05
• MCP: Configurei o universal-control com OAuth Google
• Power BI: Ajustei layout do dashboard RG via MCP
• Apps Script: Corrigi bug B3 do mapeamento Form CRM
• Reunião com Zelone sobre métricas RG

---
[DATA] Terça 13/05
• DAX: Criei 3 medidas novas para conta corrente
• Dados: Tratamento da base de implantação
• Pendência: Aguardando retorno do Gustavo sobre fontes

---
[DATA] Quarta 14/05
• Apps Script: 6 bugs corrigidos no Sprint IC
• Melhoria M1: Responsável sempre vai para triagem
• Melhoria M2: Alerta no Google Chat
• Validação 18/18 ✅
```

**O sistema detecta automaticamente:**
- ✅ Datas (vários formatos)
- ✅ Categorias (MCP, Power BI, Apps Script, Dados, Reunião, etc)
- ✅ Tags (#tag ou [tag])
- ✅ Status (Concluído ou Pendência)

### Na Sexta-feira

**16:00** → Python processa o Docs e gera JSON  
**17:00** → Apps Script gera HTML e envia email

**Você não faz NADA!** 🎉

---

## 🎨 CATEGORIAS DETECTADAS AUTOMATICAMENTE

| Categoria | Palavras-chave | Cor | Ícone |
|-----------|---------------|-----|-------|
| **MCP** | mcp, universal-control, oauth, servidor, bridge | 🟠 #F46901 | ⚙️ |
| **Power BI** | power bi, pbi, dashboard, dax, medida, visual, layout | 🟡 #F2C811 | 📊 |
| **Apps Script** | apps script, script, trigger, automação, form | 🟣 #6F05D4 | 🤖 |
| **Dados** | dados, etl, tratamento, fonte, tabela, query | 🔵 #4285F4 | 🗄️ |
| **Reunião** | reunião, meeting, alinhamento, planning, sprint | ⚫ #434343 | 👥 |
| **Doc** | documentação, doc, relatório, manual | 🟢 #107C41 | 📝 |
| **Bug Fix** | bug, correção, fix, erro, corrigir | 🔴 #C00000 | 🐛 |
| **Melhoria** | melhoria, otimização, refactor, implementar | 🟢 #107C41 | ✨ |
| **Pendência** | pendência, aguardando, bloqueado, waiting | 🟡 #F2B100 | ⏳ |

---

## 🧪 TESTAR ANTES DA SEXTA

### Teste Python

```bash
cd "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick"

# Modo teste (não envia, só processa)
python relatorio_semanal_auto.py --test

# Ver logs
type logs\relatorio_20260515.log
```

### Teste Apps Script

1. Abra o Apps Script
2. Execute `testarBuscaJSON()`
3. Deve mostrar: "✅ JSON encontrado! Total: X registros"
4. Execute `gerarRelatorioSemanal()` manualmente
5. Verifique email

---

## 📂 ESTRUTURA DE ARQUIVOS

```
06-MCP-Tools/scripts-amazon-quick/
├── relatorio_semanal_auto.py          ← Script Python principal
├── relatorio_semanal_apps_script.gs   ← Apps Script (colar no Google)
├── README_RELATORIO_SEMANAL.md        ← Este arquivo
├── backups/                           ← Backups automáticos
│   ├── diario_20260515_160000.txt
│   └── relatorio_20260515_160030.json
└── logs/                              ← Logs detalhados
    └── relatorio_20260515.log
```

---

## 🔧 TROUBLESHOOTING

### ❌ "Nenhum JSON encontrado"
- Execute o Python primeiro: `python relatorio_semanal_auto.py`
- Verifique se o JSON foi salvo no Drive (pasta "Mob2Con - Relatórios Semanais")

### ❌ "credentials.json não encontrado"
- Baixe do Google Cloud Console
- Salve em: `C:\Users\Donizete Senne\.aws\amazonq\universal-control\google-credentials.json`

### ❌ "Email não enviado"
- Verifique se `CONFIG.EMAIL_GESTORA` está preenchido no Apps Script
- Execute `gerarRelatorioSemanal()` manualmente para ver o erro

### ❌ Python não detecta categorias
- Verifique se o texto no Docs tem palavras-chave (MCP, Power BI, etc)
- Veja os logs: `type logs\relatorio_YYYYMMDD.log`

---

## 🚀 FEATURES AVANÇADAS

### Adicionar Nova Categoria

**Python** (`relatorio_semanal_auto.py` linha 150):
```python
'Nova Categoria': ['palavra1', 'palavra2', 'palavra3'],
```

**Config** (linha 50):
```python
'Nova Categoria': '#FF5733',  # Cor
```

**Config** (linha 60):
```python
'Nova Categoria': '🎯',  # Ícone
```

### Webhook Google Chat

No Apps Script, preencha:
```javascript
WEBHOOK_CHAT: 'https://chat.googleapis.com/v1/spaces/.../messages?key=...'
```

Vai notificar no Chat quando enviar o relatório.

---

## 📊 EXEMPLO DE SAÍDA

O relatório gerado terá:

✅ **Header** com período e total de entregas  
✅ **Cards resumo** por categoria (MCP: 5, Power BI: 3, etc)  
✅ **Timeline** com todas as entregas da semana  
✅ **Pendências** destacadas em amarelo  
✅ **Footer** com data/hora de geração  

**Formato idêntico ao HTML que você mostrou!**

---

## 📞 SUPORTE

Logs detalhados em:
- Python: `logs/relatorio_YYYYMMDD.log`
- Apps Script: View → Logs (no editor)

Backups automáticos em:
- `backups/diario_YYYYMMDD_HHMMSS.txt` (texto original)
- `backups/relatorio_YYYYMMDD_HHMMSS.json` (dados processados)

---

## ✅ CHECKLIST DE INSTALAÇÃO

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install ...`)
- [ ] Google Cloud Project criado
- [ ] APIs habilitadas (Docs, Drive, Sheets)
- [ ] credentials.json baixado e salvo
- [ ] Primeira execução com `--setup` (autorização)
- [ ] Apps Script colado e configurado
- [ ] EMAIL_GESTORA preenchido
- [ ] Trigger Apps Script criado (Sexta 17:00)
- [ ] Task Scheduler configurado (Sexta 16:00)
- [ ] Teste manual executado com sucesso

---

**🎉 Pronto! Agora é só jogar texto no Docs durante a semana e deixar o sistema trabalhar!**
