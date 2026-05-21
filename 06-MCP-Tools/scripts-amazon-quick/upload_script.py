import json, urllib.request, urllib.error

SCRIPT_ID  = "1eHet5kz5GIA2X6TuqSOun-OhVnQkJ_FOPZM9eKHXJnADppIZj-mEH0XJ"
TOKEN_PATH = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"
V9_PATH    = r"C:\Users\Donizete Senne\Desktop\sprint_ic_v9.json"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    access_token = json.load(f)['access_token']

with open(V9_PATH, 'r', encoding='utf-8') as f:
    raw = json.load(f)

# API aceita apenas name, type, source — remove id
payload = {
    "files": [
        {"name": fi["name"], "type": fi["type"], "source": fi["source"]}
        for fi in raw["files"]
    ]
}

body = json.dumps(payload).encode('utf-8')
url  = f"https://script.googleapis.com/v1/projects/{SCRIPT_ID}/content"
req  = urllib.request.Request(url, data=body, method='PUT', headers={
    'Authorization': f'Bearer {access_token}',
    'Content-Type':  'application/json',
})

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        print("SUCESSO! scriptId:", result.get('scriptId'))
        print("Files:", [f['name'] for f in result.get('files', [])])
except urllib.error.HTTPError as e:
    print("ERRO HTTP", e.code, ":", e.read().decode('utf-8')[:600])
except Exception as ex:
    print("ERRO:", ex)
