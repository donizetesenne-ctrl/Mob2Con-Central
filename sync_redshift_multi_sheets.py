import psycopg2
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Configurações
MAX_ROWS_SMALL = 50000
MAX_ROWS_MEDIUM = 10000
MAX_ROWS_LARGE = 5000
BATCH_SIZE = 5000

# Tabelas para pular
SKIP_TABLES = [
    'dim_produto_rede_to_delete', 'dim_produto_rede_to_delete2',
    'to_delete_unidade_fabril', 'to_delete_unidade_fabril_2',
    'tmp_sk_user_to_delete', 'tmp_sk_visitante_to_delete',
    'tmp_tbl_base_store_product_infos',
    'stg_dim_documento', 'stg_fato_mobconnect_atendimento_lojas',
    'fato_contrato_anual', 'fato_contrato_mensal', 'fato_execucao_dia',
    'tbl_rls_controle_varejo_prestador'
]

# Carregar config Redshift
with open('redshift_config.json', 'r') as f:
    cfg = json.load(f)

print("="*70)
print("SINCRONIZAÇÃO REDSHIFT → GOOGLE SHEETS (MÚLTIPLAS PLANILHAS)")
print("="*70)

# Conectar Redshift
print("\n[1/5] Conectando ao Redshift...")
conn = psycopg2.connect(
    host=cfg['host'], port=cfg['port'], dbname=cfg['database'],
    user=cfg['user'], password=cfg['password'],
    sslmode='require', connect_timeout=15
)
cur = conn.cursor()
print("✅ Conectado")

# Carregar credenciais Google
print("\n[2/5] Autenticando no Google...")
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
drive_service = build('drive', 'v3', credentials=creds)
print("✅ Autenticado")

# Listar tabelas
print("\n[3/5] Listando tabelas do schema dw...")
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'dw' ORDER BY tablename")
all_tables = [row[0] for row in cur.fetchall()]
tables = [t for t in all_tables if t not in SKIP_TABLES]
print(f"✅ {len(tables)} tabelas para processar")

# Categorizar
categorized = {'dim': [], 'fato': [], 'outros': []}
for table in tables:
    if table.startswith('dim_'):
        categorized['dim'].append(table)
    elif table.startswith('fato_'):
        categorized['fato'].append(table)
    else:
        categorized['outros'].append(table)

print(f"   - Dimensões: {len(categorized['dim'])}")
print(f"   - Fatos: {len(categorized['fato'])}")
print(f"   - Outros: {len(categorized['outros'])}")

# Criar planilhas
print("\n[4/5] Criando planilhas no Google Drive...")
spreadsheets = {}

categories_config = {
    'dim': {'name': '📊 Redshift - Dimensões', 'emoji': '📊'},
    'fato': {'name': '📈 Redshift - Fatos', 'emoji': '📈'},
    'outros': {'name': '🔗 Redshift - Lookup e Tabelas', 'emoji': '🔗'}
}

for cat_key, config in categories_config.items():
    if len(categorized[cat_key]) == 0:
        continue
    
    print(f"\n   Criando: {config['name']}...")
    
    # Criar planilha
    spreadsheet = sheets_service.spreadsheets().create(body={
        'properties': {'title': config['name']},
        'sheets': [{'properties': {'title': '📋 Índice'}}]
    }).execute()
    
    spreadsheet_id = spreadsheet['spreadsheetId']
    spreadsheets[cat_key] = spreadsheet_id
    
    print(f"   ✅ Criada: {spreadsheet_id}")
    print(f"      https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

# Função para sincronizar tabela
def sync_table(table_name, spreadsheet_id, category_emoji):
    # Contar registros
    cur.execute(f'SELECT COUNT(*) FROM dw.{table_name}')
    total_count = cur.fetchone()[0]
    
    if total_count == 0:
        return 0, 'Vazia'
    
    # Determinar limite
    if total_count < 100000:
        limit = min(total_count, MAX_ROWS_SMALL)
    elif total_count < 1000000:
        limit = MAX_ROWS_MEDIUM
    else:
        limit = MAX_ROWS_LARGE
    
    print(f"   {table_name}: {total_count:,} registros → extraindo {limit:,}...", end=' ')
    
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
    
    sheet_data = [columns]
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
    
    # Criar aba (nome curto para evitar erros)
    sheet_title = table_name[:100]
    
    try:
        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': [{'addSheet': {'properties': {'title': sheet_title}}}]}
        ).execute()
    except:
        pass
    
    # Enviar dados
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_title}'!A1",
        valueInputOption='RAW',
        body={'values': sheet_data}
    ).execute()
    
    print(f"✅ {len(sheet_data)-1:,} linhas")
    return len(sheet_data)-1, 'OK'

# Processar cada categoria
print("\n[5/5] Sincronizando dados...")

for cat_key, spreadsheet_id in spreadsheets.items():
    config = categories_config[cat_key]
    tables_list = categorized[cat_key]
    
    print(f"\n{'='*70}")
    print(f"{config['emoji']} {config['name'].upper()}")
    print(f"{'='*70}")
    print(f"Planilha: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    print(f"Tabelas: {len(tables_list)}\n")
    
    # Criar índice
    index_data = [['Tabela', 'Total Registros', 'Sincronizados', 'Status', 'Atualização']]
    
    for table in tables_list:
        try:
            synced, status = sync_table(table, spreadsheet_id, config['emoji'])
            
            # Contar total
            cur.execute(f'SELECT COUNT(*) FROM dw.{table}')
            total = cur.fetchone()[0]
            
            index_data.append([
                table, total, synced, status,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
            
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            index_data.append([table, 0, 0, f'Erro: {str(e)[:50]}', ''])
    
    # Atualizar índice
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="'📋 Índice'!A1",
        valueInputOption='RAW',
        body={'values': index_data}
    ).execute()
    
    print(f"\n✅ Categoria concluída: {len(tables_list)} tabelas processadas")

conn.close()

print("\n" + "="*70)
print("✅ SINCRONIZAÇÃO CONCLUÍDA!")
print("="*70)
print("\nPLANILHAS CRIADAS:")
for cat_key, spreadsheet_id in spreadsheets.items():
    config = categories_config[cat_key]
    print(f"\n{config['emoji']} {config['name']}")
    print(f"   https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
