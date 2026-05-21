import psycopg2
import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Configurações
SPREADSHEET_ID = "1fWUeTtlzjSxHOLkhcURCDRaowZw0Z0UqGXz9WC4KC_M"
MAX_ROWS_PER_TABLE = 100000  # Limite para tabelas grandes
BATCH_SIZE = 10000  # Processar em lotes

# Carregar config Redshift
with open('redshift_config.json', 'r') as f:
    cfg = json.load(f)

# Conectar Redshift
print("Conectando ao Redshift...")
conn = psycopg2.connect(
    host=cfg['host'],
    port=cfg['port'],
    dbname=cfg['database'],
    user=cfg['user'],
    password=cfg['password'],
    sslmode='require',
    connect_timeout=15
)
cur = conn.cursor()

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

# Listar tabelas do schema dw
print("Listando tabelas do schema dw...")
cur.execute("""
    SELECT tablename
    FROM pg_tables 
    WHERE schemaname = 'dw'
    ORDER BY tablename
""")
tables = [row[0] for row in cur.fetchall()]

print(f"Encontradas {len(tables)} tabelas no schema dw")

# Categorizar tabelas
def categorize_table(name):
    if name.startswith('dim_'):
        return 'Dimensões'
    elif name.startswith('fato_'):
        return 'Fatos'
    elif name.startswith('lkp_'):
        return 'Lookup'
    elif name.startswith('stg_'):
        return 'Staging'
    elif name.startswith('tmp_') or 'to_delete' in name:
        return 'Temporárias'
    elif name.startswith('tbl_'):
        return 'Tabelas'
    else:
        return 'Outras'

# Agrupar tabelas
categorized = {}
for table in tables:
    category = categorize_table(table)
    if category not in categorized:
        categorized[category] = []
    categorized[category].append(table)

# Criar aba índice
print("\nCriando aba de índice...")
index_data = [['Categoria', 'Tabela', 'Registros', 'Status', 'Última Atualização']]

for category in sorted(categorized.keys()):
    for table in categorized[category]:
        cur.execute(f'SELECT COUNT(*) FROM dw.{table}')
        count = cur.fetchone()[0]
        index_data.append([category, table, count, 'Pendente', ''])

# Limpar e criar aba Índice
try:
    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': '📋 Índice',
                        'index': 0
                    }
                }
            }]
        }
    ).execute()
except:
    pass  # Aba já existe

# Escrever índice
sheets_service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='📋 Índice!A1',
    valueInputOption='RAW',
    body={'values': index_data}
).execute()

print(f"Índice criado com {len(index_data)-1} tabelas")

# Função para extrair e enviar dados
def sync_table(table_name, category):
    print(f"\n[{category}] Processando {table_name}...")
    
    # Contar registros
    cur.execute(f'SELECT COUNT(*) FROM dw.{table_name}')
    total_count = cur.fetchone()[0]
    
    if total_count == 0:
        print(f"  ⚠️  Tabela vazia, pulando...")
        return 'Vazia'
    
    # Limitar registros grandes
    limit = min(total_count, MAX_ROWS_PER_TABLE)
    
    # Obter colunas
    cur.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'dw' AND table_name = '{table_name}'
        ORDER BY ordinal_position
    """)
    columns = [row[0] for row in cur.fetchall()]
    
    # Extrair dados
    print(f"  Extraindo {limit:,} de {total_count:,} registros...")
    cur.execute(f'SELECT * FROM dw.{table_name} LIMIT {limit}')
    
    # Preparar dados para Sheets
    sheet_data = [columns]  # Header
    
    batch_count = 0
    while True:
        rows = cur.fetchmany(BATCH_SIZE)
        if not rows:
            break
        
        for row in rows:
            # Converter valores para string (Sheets API requirement) e corrigir encoding de control characters (Mac Roman importados como Latin-1)
            sheet_data.append([
                str(val).replace('\x83', 'Ã').replace('\x93', 'Ó')
                if val is not None else ''
                for val in row
            ])
        
        batch_count += len(rows)
        print(f"  Processados {batch_count:,} registros...")
    
    # Criar aba
    sheet_title = f"{category[:3]}_{table_name}"[:100]  # Limite de 100 chars
    
    try:
        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_title
                        }
                    }
                }]
            }
        ).execute()
    except Exception as e:
        if 'already exists' not in str(e):
            print(f"  ⚠️  Erro ao criar aba: {e}")
    
    # Limpar aba existente
    try:
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_title}'!A1:ZZ"
        ).execute()
    except:
        pass
    
    # Enviar dados
    print(f"  Enviando para Google Sheets...")
    sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{sheet_title}'!A1",
        valueInputOption='RAW',
        body={'values': sheet_data}
    ).execute()
    
    print(f"  ✅ {len(sheet_data)-1:,} registros sincronizados")
    
    return 'Sincronizado'

# Processar tabelas por categoria
print("\n" + "="*60)
print("INICIANDO SINCRONIZAÇÃO")
print("="*60)

for category in sorted(categorized.keys()):
    print(f"\n{'='*60}")
    print(f"CATEGORIA: {category} ({len(categorized[category])} tabelas)")
    print(f"{'='*60}")
    
    for table in categorized[category]:
        try:
            status = sync_table(table, category)
            
            # Atualizar índice
            for i, row in enumerate(index_data[1:], 2):
                if row[1] == table:
                    index_data[i-1][3] = status
                    index_data[i-1][4] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    break
            
            # Atualizar índice no Sheets
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range='📋 Índice!A1',
                valueInputOption='RAW',
                body={'values': index_data}
            ).execute()
            
        except Exception as e:
            print(f"  ❌ ERRO: {e}")
            continue

conn.close()
print("\n" + "="*60)
print("SINCRONIZAÇÃO CONCLUÍDA!")
print("="*60)
