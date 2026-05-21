import json, urllib.request, urllib.error, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_ID  = "1eHet5kz5GIA2X6TuqSOun-OhVnQkJ_FOPZM9eKHXJnADppIZj-mEH0XJ"
TOKEN_PATH = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    token = json.load(f)['access_token']

def run(func, dev=True):
    url  = f"https://script.googleapis.com/v1/scripts/{SCRIPT_ID}:run"
    body = json.dumps({"function": func, "devMode": dev}).encode()
    req  = urllib.request.Request(url, data=body, method='POST', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type':  'application/json',
    })
    try:
        with urllib.request.urlopen(req) as r:
            res = json.loads(r.read())
            if res.get('error'):
                return None, res['error']
            return res.get('response', {}).get('result'), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:400]}"

# Tentar executar criarListasDeTasksParaTodos
print("Tentando executar criarListasDeTasksParaTodos...")
res, err = run("criarListasDeTasksParaTodos", dev=True)
print("devMode=True:", res, "|", err)

res, err = run("criarListasDeTasksParaTodos", dev=False)
print("devMode=False:", res, "|", err)
