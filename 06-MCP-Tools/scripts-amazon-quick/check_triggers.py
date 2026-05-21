import json, urllib.request, urllib.error, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_ID  = "1eHet5kz5GIA2X6TuqSOun-OhVnQkJ_FOPZM9eKHXJnADppIZj-mEH0XJ"
TOKEN_PATH = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    token = json.load(f)['access_token']

req = urllib.request.Request(
    f"https://script.googleapis.com/v1/projects/{SCRIPT_ID}/triggers",
    headers={'Authorization': f'Bearer {token}'}
)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    triggers = data.get('triggers', [])
    print(f"Total de triggers: {len(triggers)}\n")
    for t in triggers:
        func     = t.get('handlerFunction', '?')
        etype    = t.get('eventType', '?')
        esource  = t.get('eventSource', '?')
        tid      = t.get('triggerId', '?')
        print(f"  ✅ {func}")
        print(f"     Tipo:   {etype}")
        print(f"     Origem: {esource}")
        print(f"     ID:     {tid}")
        print()
except urllib.error.HTTPError as e:
    print("Erro:", e.code, e.read().decode()[:300])
