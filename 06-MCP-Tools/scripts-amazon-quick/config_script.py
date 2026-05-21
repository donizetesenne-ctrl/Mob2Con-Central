import json, urllib.request, urllib.error

SCRIPT_ID  = "1eHet5kz5GIA2X6TuqSOun-OhVnQkJ_FOPZM9eKHXJnADppIZj-mEH0XJ"
TOKEN_PATH = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    access_token = json.load(f)['access_token']

def api(method, path, body=None):
    url = f"https://script.googleapis.com/v1/{path}"
    data = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type':  'application/json',
    })
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')[:400]}"

# 1. Listar triggers existentes
print("=== TRIGGERS EXISTENTES ===")
res, err = api('GET', f'projects/{SCRIPT_ID}')
if err:
    print("Erro ao buscar projeto:", err)
else:
    print("Projeto:", res.get('title'))
    print("URL webapp:", res.get('deploymentId', 'sem deployment'))

# 2. Listar deployments
print("\n=== DEPLOYMENTS ===")
res, err = api('GET', f'projects/{SCRIPT_ID}/deployments')
if err:
    print("Erro:", err)
else:
    deps = res.get('deployments', [])
    if deps:
        for d in deps:
            print(f"  ID: {d.get('deploymentId')} | Config: {d.get('deploymentConfig', {}).get('description','')}")
    else:
        print("  Nenhum deployment encontrado")

# 3. Tentar executar configurarTodosOsTriggers via API
print("\n=== EXECUTAR configurarTodosOsTriggers ===")
res, err = api('POST', f'scripts/{SCRIPT_ID}:run', {
    "function": "configurarTodosOsTriggers",
    "devMode": True
})
if err:
    print("Erro:", err)
else:
    print("Resultado:", res)
