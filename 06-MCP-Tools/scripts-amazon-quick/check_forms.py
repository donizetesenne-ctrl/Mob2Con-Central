import json, urllib.request, urllib.error, sys
sys.stdout.reconfigure(encoding='utf-8')

SHEET_ID   = "16nMsEoVLkPcE-Vn7n5LjlGprybvSBqw2qrqflH8Bb74"
FORM_IC    = "1MNeZltLifO84ajszwRsnAuysXMfJAYkjmgMriSdrlVQ"
TOKEN_PATH = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    token = json.load(f)['access_token']

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:300]}"

# Listar todas as abas
data, err = get(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=sheets.properties")
if err:
    print("Erro:", err)
else:
    print("=== ABAS DA PLANILHA ===")
    for s in data['sheets']:
        p = s['properties']
        print(f"  [{p['sheetId']}] {p['title']}")

# Verificar metadados do formulário IC
print("\n=== FORMULÁRIO IC ===")
res, err = get(f"https://www.googleapis.com/drive/v3/files/{FORM_IC}?fields=id,name,mimeType")
if err:
    print("Erro:", err)
else:
    print(f"  Nome: {res['name']}")
    print(f"  ID:   {res['id']}")

# Verificar se o formulário já tem respostas vinculadas à planilha
# via spreadsheet metadata
print("\n=== VERIFICANDO VINCULAÇÃO ===")
res2, err2 = get(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=spreadsheetId,properties.title")
if not err2:
    print(f"  Planilha: {res2['properties']['title']}")
    print(f"  ID: {res2['spreadsheetId']}")

# Ler primeiras linhas das abas de respostas para identificar qual é do formulário IC
print("\n=== CONTEÚDO ABA RESPOSTAS 1 (sheetId 589562186) ===")
res3, err3 = get(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/589562186!A1:C3")
if err3:
    # Tentar pelo nome
    res3, err3 = get(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/'Respostas ao formul%C3%A1rio 1'!A1:C3")
print("  Resultado:", res3 if res3 else err3)

print("\n=== CONTEÚDO ABA RESPOSTAS 2 (sheetId 156245518) ===")
res4, err4 = get(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/156245518!A1:C3")
print("  Resultado:", res4 if res4 else err4)
