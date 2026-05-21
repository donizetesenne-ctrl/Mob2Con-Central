import json, urllib.request, urllib.error

SCRIPT_ID  = "1eHet5kz5GIA2X6TuqSOun-OhVnQkJ_FOPZM9eKHXJnADppIZj-mEH0XJ"
TOKEN_PATH = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"
V9_PATH    = r"C:\Users\Donizete Senne\Desktop\sprint_ic_v9.json"
WEBAPP_URL = "https://chat.googleapis.com/v1/spaces/AAQAOo6ucb8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fZ28agCZO2t2PVUIa93GGHxrEaOxTq64IJiwnO3tlVA"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    access_token = json.load(f)['access_token']

with open(V9_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

code = data['files'][1]['source']

# Adicionar função configurarPropriedades() que seta WEBHOOK_URL e WEBAPP_URL
nova_funcao = f"""

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO EXTRA — SETUP INICIAL DE PROPRIEDADES (v9.0)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function configurarPropriedades() {{
  const props = PropertiesService.getScriptProperties();
  const webhookAtual = props.getProperty("WEBHOOK_URL") || "";
  const webappAtual  = props.getProperty("WEBAPP_URL")  || "";

  // Salvar WEBAPP_URL se ainda não estiver configurada
  if (!webappAtual) {{
    props.setProperty("WEBAPP_URL", "{WEBAPP_URL}");
    Logger.log("[configurarPropriedades] WEBAPP_URL configurada.");
  }}

  // Se WEBHOOK_URL não estiver configurada, usar WEBAPP_URL como fallback
  if (!webhookAtual) {{
    props.setProperty("WEBHOOK_URL", props.getProperty("WEBAPP_URL"));
    Logger.log("[configurarPropriedades] WEBHOOK_URL copiada de WEBAPP_URL.");
  }}

  const ui = SpreadsheetApp.getUi();
  ui.alert(
    "✅ Propriedades configuradas!\\n\\n" +
    "WEBHOOK_URL: " + (props.getProperty("WEBHOOK_URL") ? "✅ OK" : "❌ Vazia") + "\\n" +
    "WEBAPP_URL:  " + (props.getProperty("WEBAPP_URL")  ? "✅ OK" : "❌ Vazia") + "\\n\\n" +
    "Agora execute: ⚙️ Configuração → 🔧 Configurar Triggers"
  );
}}
"""

# Adicionar ao final do código
if 'configurarPropriedades' not in code:
    code = code + nova_funcao
    print("Função configurarPropriedades adicionada.")
else:
    print("Função já existe, pulando.")

# Adicionar item no menu Configuração
old_menu = '.addItem("📥 Importar Dados Jira/HubSpot",      "importarDadosConsolidados"))'
new_menu = '.addItem("📥 Importar Dados Jira/HubSpot",      "importarDadosConsolidados")\n      .addSeparator()\n      .addItem("🔑 Configurar Propriedades (WEBHOOK)",  "configurarPropriedades"))'
if old_menu in code and 'configurarPropriedades' not in code.split(old_menu)[0][-200:]:
    code = code.replace(old_menu, new_menu)
    print("Item de menu adicionado.")

data['files'][1]['source'] = code

# Upload
payload = {
    "files": [
        {"name": fi["name"], "type": fi["type"], "source": fi["source"]}
        for fi in data["files"]
    ]
}
body = json.dumps(payload).encode('utf-8')
url  = f"https://script.googleapis.com/v1/projects/{SCRIPT_ID}/content"
req  = urllib.request.Request(url, data=body, method='PUT', headers={
    'Authorization': f'Bearer {access_token}',
    'Content-Type':  'application/json',
})
try:
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode('utf-8'))
        print("UPLOAD OK! scriptId:", res.get('scriptId'))
        print("Files:", [f['name'] for f in res.get('files', [])])
except urllib.error.HTTPError as e:
    print("ERRO HTTP", e.code, ":", e.read().decode()[:400])

# Salvar v9 atualizado
with open(V9_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
print("Arquivo v9 atualizado localmente.")
