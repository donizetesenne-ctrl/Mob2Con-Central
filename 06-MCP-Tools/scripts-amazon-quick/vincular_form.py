import json, urllib.request, urllib.error

SCRIPT_ID   = "1eHet5kz5GIA2X6TuqSOun-OhVnQkJ_FOPZM9eKHXJnADppIZj-mEH0XJ"
SHEET_ID    = "16nMsEoVLkPcE-Vn7n5LjlGprybvSBqw2qrqflH8Bb74"
FORM_ID     = "1MNeZltLifO84ajszwRsnAuysXMfJAYkjmgMriSdrlVQ"
TOKEN_PATH  = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"

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
        return None, f"HTTP {e.code}: {e.read().decode()[:500]}"

# 1. Verificar se formulário já está vinculado à planilha
print("=== Verificando formulário ===")
res, err = api('GET', f"https://forms.googleapis.com/v1/forms/{FORM_ID}")
if err:
    print("Erro Forms API:", err)
else:
    print("Formulário:", res.get('info', {}).get('title'))
    linked = res.get('linkedSheetId', '')
    print("Planilha vinculada:", linked if linked else "NENHUMA")

    # 2. Vincular à planilha se não estiver vinculado
    if linked != SHEET_ID:
        print("\nVinculando formulário à planilha...")
        res2, err2 = api('POST',
            f"https://forms.googleapis.com/v1/forms/{FORM_ID}:setLinkedSheet",
            {"spreadsheetId": SHEET_ID}
        )
        if err2:
            print("Erro ao vincular:", err2)
        else:
            print("Vinculado com sucesso!")
    else:
        print("Já vinculado corretamente.")

# 3. Listar triggers existentes no script
print("\n=== Triggers existentes ===")
res, err = api('GET', f"https://script.googleapis.com/v1/projects/{SCRIPT_ID}/deployments")
if err:
    print("Erro:", err)
else:
    for d in res.get('deployments', []):
        print(f"  {d.get('deploymentId')} — {d.get('deploymentConfig', {}).get('description','')}")

# 4. Criar trigger onFormSubmit via Apps Script API
print("\n=== Criando trigger onFormSubmit ===")
trigger_body = {
    "scriptId": SCRIPT_ID,
    "trigger": {
        "userProcessFilter": {
            "userAccessLevel": "OWNER"
        },
        "eventType": "ON_FORM_SUBMIT",
        "formTrigger": {
            "formId": FORM_ID,
            "deploymentId": "@HEAD"
        },
        "handlerFunction": "onFormSubmit"
    }
}
res, err = api('POST',
    f"https://script.googleapis.com/v1/projects/{SCRIPT_ID}/triggers",
    trigger_body
)
if err:
    print("Erro ao criar trigger:", err)
else:
    print("Trigger criado:", res)
