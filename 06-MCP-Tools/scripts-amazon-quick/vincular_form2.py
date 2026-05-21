import json, urllib.request, urllib.error

SHEET_ID   = "16nMsEoVLkPcE-Vn7n5LjlGprybvSBqw2qrqflH8Bb74"
FORM_ID    = "1MNeZltLifO84ajszwRsnAuysXMfJAYkjmgMriSdrlVQ"
TOKEN_PATH = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"

with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
    access_token = json.load(f)['access_token']

def api(method, url, body=None):
    data = json.dumps(body).encode('utf-8') if body else None
    req  = urllib.request.Request(url, data=data, method=method, headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type':  'application/json',
    })
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:600]}"

# Verificar abas existentes na planilha
print("=== Abas da planilha ===")
res, err = api('GET', f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=sheets.properties.title,sheets.properties.sheetId")
if err:
    print("Erro:", err)
else:
    sheets = res.get('sheets', [])
    for s in sheets:
        p = s['properties']
        print(f"  [{p['sheetId']}] {p['title']}")

# Verificar se já existe aba de respostas do formulário
titles = [s['properties']['title'] for s in sheets] if not err else []
form_sheet = next((t for t in titles if 'Respostas' in t or 'Form' in t or 'Solicitação' in t), None)
print("\nAba de respostas encontrada:", form_sheet if form_sheet else "NENHUMA")

# Tentar vincular via Sheets API updateSpreadsheetProperties
print("\n=== Tentando vincular formulário via Sheets API ===")
res2, err2 = api('POST',
    f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate",
    {"requests": [{"addSheet": {"properties": {"title": "🔗 Form Responses (temp)"}}}]}
)
if err2:
    print("Erro batchUpdate:", err2)
else:
    new_sheet_id = res2['replies'][0]['addSheet']['properties']['sheetId']
    print("Aba temp criada, sheetId:", new_sheet_id)
    # Remover aba temp
    api('POST',
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate",
        {"requests": [{"deleteSheet": {"sheetId": new_sheet_id}}]}
    )
    print("Aba temp removida.")

# Verificar URL de resposta do formulário via Drive
print("\n=== Metadados do formulário via Drive ===")
res3, err3 = api('GET', f"https://www.googleapis.com/drive/v3/files/{FORM_ID}?fields=id,name,mimeType,description,parents")
if err3:
    print("Erro Drive:", err3)
else:
    print("Nome:", res3.get('name'))
    print("Tipo:", res3.get('mimeType'))
    print("Parents:", res3.get('parents'))
