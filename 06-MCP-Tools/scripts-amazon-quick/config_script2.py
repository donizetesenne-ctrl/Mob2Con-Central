import json, urllib.request, urllib.error

SCRIPT_ID   = "1eHet5kz5GIA2X6TuqSOun-OhVnQkJ_FOPZM9eKHXJnADppIZj-mEH0XJ"
DEPLOY_ID   = "AKfycbwbhkVgVgpi3Mm2r68XsBkth-t02Fhlq3sbY3AGM0v4DbKeSq5vpyq6D_j84-OfSyhR"
TOKEN_PATH  = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"
WEBAPP_URL  = "https://chat.googleapis.com/v1/spaces/AAQAOo6ucb8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fZ28agCZO2t2PVUIa93GGHxrEaOxTq64IJiwnO3tlVA"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    access_token = json.load(f)['access_token']

def run_function(func_name, params=[], dev=True):
    url  = f"https://script.googleapis.com/v1/scripts/{SCRIPT_ID}:run"
    body = {"function": func_name, "parameters": params, "devMode": dev}
    req  = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type':  'application/json',
    })
    try:
        with urllib.request.urlopen(req) as r:
            res = json.loads(r.read().decode('utf-8'))
            if res.get('error'):
                return None, res['error'].get('details', res['error'])
            return res.get('response', {}).get('result'), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:400]}"

# Tentar com devMode=False usando deployment publicado
def run_deployed(func_name, params=[]):
    url  = f"https://script.googleapis.com/v1/scripts/{SCRIPT_ID}:run"
    body = {"function": func_name, "parameters": params, "devMode": False}
    req  = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type':  'application/json',
    })
    try:
        with urllib.request.urlopen(req) as r:
            res = json.loads(r.read().decode('utf-8'))
            if res.get('error'):
                return None, str(res['error'])
            return res.get('response', {}).get('result'), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:400]}"

# 1. Tentar configurar WEBAPP_URL via setScriptProperties
print("=== Configurando WEBAPP_URL ===")
# Criar função inline via novo arquivo temporário no script
# Alternativa: usar Sheets API para escrever na aba Config se existir

# Verificar se há uma planilha vinculada ao script
print("Tentando run devMode=True...")
res, err = run_function("testarWebhook")
print("devMode=True:", res, "|", err)

print("\nTentando run devMode=False...")
res, err = run_deployed("testarWebhook")
print("devMode=False:", res, "|", err)
