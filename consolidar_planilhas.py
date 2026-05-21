"""
Script para consolidar as 3 planilhas Redshift em uma única planilha
"""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

print("="*70)
print("CONSOLIDANDO PLANILHAS REDSHIFT")
print("="*70)

# Carregar credenciais Google
token_path = r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json"
with open(token_path, 'r') as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data['access_token'],
    refresh_token=token_data.get('refresh_token'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id='436757880380-rmej7o84om2blop4urtur6806leghq2h.apps.googleusercontent.com',
    client_secret=token_data.get('client_secret')
)

sheets_service = build('sheets', 'v4', credentials=creds)

# IDs das planilhas
SOURCE_SHEETS = {
    'Dimensões': '1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q',
    'Fatos': '1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs',
    'Lookup': '1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI'
}

TARGET_SHEET = '1fWUeTtlzjSxHOLkhcURCDRaowZw0Z0UqGXz9WC4KC_M'

print("\nPlanilha destino: Amazon Redshift")
print(f"ID: {TARGET_SHEET}")
print()

# Limpar planilha destino (remover todas as abas exceto a primeira)
print("Limpando planilha destino...")
target_metadata = sheets_service.spreadsheets().get(spreadsheetId=TARGET_SHEET).execute()
existing_sheets = target_metadata.get('sheets', [])

# Manter apenas a primeira aba e renomear para "📋 Índice Geral"
if len(existing_sheets) > 0:
    first_sheet_id = existing_sheets[0]['properties']['sheetId']
    
    # Renomear primeira aba
    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=TARGET_SHEET,
        body={
            'requests': [{
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': first_sheet_id,
                        'title': '📋 Índice Geral'
                    },
                    'fields': 'title'
                }
            }]
        }
    ).execute()
    
    # Remover outras abas
    if len(existing_sheets) > 1:
        delete_requests = []
        for sheet in existing_sheets[1:]:
            delete_requests.append({
                'deleteSheet': {
                    'sheetId': sheet['properties']['sheetId']
                }
            })
        
        if delete_requests:
            sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=TARGET_SHEET,
                body={'requests': delete_requests}
            ).execute()

print("✅ Planilha destino limpa")

# Copiar abas de cada planilha fonte
total_copied = 0

for category, source_id in SOURCE_SHEETS.items():
    print(f"\n{'='*70}")
    print(f"Copiando abas de: {category}")
    print(f"{'='*70}")
    
    # Obter metadados da planilha fonte
    source_metadata = sheets_service.spreadsheets().get(spreadsheetId=source_id).execute()
    source_sheets = source_metadata.get('sheets', [])
    
    print(f"Encontradas {len(source_sheets)} abas")
    
    for sheet in source_sheets:
        sheet_title = sheet['properties']['title']
        sheet_id = sheet['properties']['sheetId']
        
        print(f"  Copiando: {sheet_title}...", end=' ')
        
        try:
            # Copiar aba
            copy_request = sheets_service.spreadsheets().sheets().copyTo(
                spreadsheetId=source_id,
                sheetId=sheet_id,
                body={'destinationSpreadsheetId': TARGET_SHEET}
            ).execute()
            
            # Renomear se necessário (adicionar prefixo da categoria)
            if sheet_title != '📋 Índice':
                new_title = sheet_title
            else:
                new_title = f"📋 Índice - {category}"
            
            # Atualizar título
            copied_sheet_id = copy_request['sheetId']
            sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=TARGET_SHEET,
                body={
                    'requests': [{
                        'updateSheetProperties': {
                            'properties': {
                                'sheetId': copied_sheet_id,
                                'title': new_title
                            },
                            'fields': 'title'
                        }
                    }]
                }
            ).execute()
            
            print(f"✅")
            total_copied += 1
            
        except Exception as e:
            print(f"❌ Erro: {str(e)[:50]}")

print(f"\n{'='*70}")
print(f"✅ CONSOLIDAÇÃO CONCLUÍDA!")
print(f"{'='*70}")
print(f"Total de abas copiadas: {total_copied}")
print(f"\nPlanilha consolidada:")
print(f"https://docs.google.com/spreadsheets/d/{TARGET_SHEET}")
print()
