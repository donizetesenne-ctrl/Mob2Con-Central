import psycopg2
import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Configurações OTIMIZADAS
SPREADSHEET_ID = "1fWUeTtlzjSxHOLkhcURCDRaowZw0Z0UqGXz9WC4KC_M"
MAX_ROWS_SMALL = 50000   # Tabelas < 100k registros
MAX_ROWS_MEDIUM = 10000  # Tabelas 100k-1M registros
MAX_ROWS_LARGE = 5000    # Tabelas > 1M registros
BATCH_SIZE = 5000

# Tabelas para PULAR (temporárias, duplicadas, staging vazio)
SKIP_TABLES = [
    'dim_produto_rede_to_delete',
    'dim_produto_rede_to_delete2',
    'to_delete_unidade_fabril',
    'to_delete_unidade_fabril_2',
    'tmp_sk_user_to_delete',
    'tmp_sk_visitante_to_delete',
    'tmp_tbl_base_store_product_infos',
    'stg_dim_documento',
    'stg_fato_mobconnect_atendimento_lojas',
    'fato_contrato_anual',  # Vazia
    'fato_contrato_mensal',  # Vazia
    'fato_execucao_dia',  # Vazia
    'tbl_rls_controle_varejo_prestador'  # Vazia
]

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
all_tables = [row[0] for row in cur.fetchall()]

# Filtrar tabelas
tables = [t for t in all_tables if t not in SKIP_TABLES]
print(f"Processando {len(tables)} de {len(all_tables)} tabelas (pulando {len(SKIP_TABLES)} temporárias/vazias)")

# Categorizar tabelas
def categorize_table(name):
    if name.startswith('dim_'):
        return 'Dim'
    elif name.startswith('fato_'):
        return 'Fato'
    elif name.startswith('lkp_'):
        return 'Lkp'
    elif name.startswith('tbl_'):
        return 'Tbl'
    else:
        return 'Outro'

# Agrupar tabelas
categorized = {}
for table in tables:
    category = categorize_table(table)
    if category not in categorized:
        categorized[category] = []
    categorized[category].append(table)

# Criar aba índice
print("\nCriando aba de índice...")
index_data = [['Categoria', 'Tabela', 'Total Registros', 'Sincronizados', 'Status', 'Atualização']]

for category in sorted(categorized.keys()):
    for table in categorized[category]:
        cur.execute(f'SELECT COUNT(*) FROM dw.{table}')
        count = cur.fetchone()[0]
        index_data.append([category, table, count, 0, 'Pendente', ''])

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
    pass

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
    print(f"\n[{category}] {table_name}...", end=' ')
    
    # Contar registros
    cur.execute(f'SELECT COUNT(*) FROM dw.{table_name}')
    total_count = cur.fetchone()[0]
    
    if total_count == 0:
        print(f"⚠️ Vazia")
        return 0, 'Vazia'
    
    # Determinar limite baseado no tamanho
    if total_count < 100000:
        limit = min(total_count, MAX_ROWS_SMALL)
    elif total_count < 1000000:
        limit = MAX_ROWS_MEDIUM
    else:
        limit = MAX_ROWS_LARGE
    
    print(f"({total_count:,} registros, extraindo {limit:,})...", end=' ')
    
    # Obter colunas
    cur.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'dw' AND table_name = '{table_name}'
        ORDER BY ordinal_position
    """)
    columns = [row[0] for row in cur.fetchall()]
    
    # Extrair dados
    cur.execute(f'SELECT * FROM dw.{table_name} LIMIT {limit}')
    
    # Preparar dados para Sheets
    sheet_data = [columns]  # Header
    
    while True:
        rows = cur.fetchmany(BATCH_SIZE)
        if not rows:
            break
        
        for row in rows:
            # Converter valores para string e corrigir encoding de control characters (Mac Roman importados como Latin-1)
            sheet_data.append([
                str(val).replace('\x83', 'Ã').replace('\x93', 'Ó')
                if val is not None else ''
                for val in row
            ])
    
    # Criar aba
    sheet_title = f"{category}_{table_name}"[:100]
    
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
    except:
        pass
    
    # Limpar aba existente
    try:
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_title}'!A1:ZZ"
        ).execute()
    except:
        pass
    
    # Enviar dados
    sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{sheet_title}'!A1",
        valueInputOption='RAW',
        body={'values': sheet_data}
    ).execute()
    
    print(f"✅ {len(sheet_data)-1:,} linhas")
    
    return len(sheet_data)-1, 'OK'

# Processar tabelas por categoria
print("\n" + "="*70)
print("SINCRONIZAÇÃO RÁPIDA - REDSHIFT → GOOGLE SHEETS")
print("="*70)

total_synced = 0
for category in sorted(categorized.keys()):
    print(f"\n{'='*70}")
    print(f"{category.upper()} ({len(categorized[category])} tabelas)")
    print(f"{'='*70}")
    
    for table in categorized[category]:
        try:
            synced_rows, status = sync_table(table, category)
            total_synced += synced_rows
            
            # Atualizar índice
            for i, row in enumerate(index_data[1:], 2):
                if row[1] == table:
                    index_data[i-1][3] = synced_rows
                    index_data[i-1][4] = status
                    index_data[i-1][5] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    break
            
            # Atualizar índice no Sheets a cada 5 tabelas
            if total_synced % 5 == 0:
                sheets_service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range='📋 Índice!A1',
                    valueInputOption='RAW',
                    body={'values': index_data}
                ).execute()
            
        except Exception as e:
            print(f"❌ ERRO: {e}")
            continue

# Atualização final do índice
sheets_service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='📋 Índice!A1',
    valueInputOption='RAW',
    body={'values': index_data}
).execute()

conn.close()
print("\n" + "="*70)
print(f"✅ CONCLUÍDO! {total_synced:,} registros sincronizados")
print("="*70)
print(f"\nAcesse: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
