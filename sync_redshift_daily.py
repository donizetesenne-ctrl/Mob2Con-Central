"""
Script de Sincronização Diária: Redshift → Google Sheets
Atualiza automaticamente as 3 planilhas com dados do Redshift
"""
import psycopg2
import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import traceback

# Configurar encoding para Windows
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def log(msg):
    """Log com timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}")
    
    # Salvar em arquivo de log
    with open('sync_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {msg}\n")

def main():
    log("="*70)
    log("SINCRONIZAÇÃO DIÁRIA INICIADA")
    log("="*70)
    
    try:
        # Carregar configurações
        log("Carregando configurações...")
        with open('redshift_config.json', 'r') as f:
            redshift_cfg = json.load(f)
        
        with open('spreadsheets_config.json', 'r') as f:
            sheets_cfg = json.load(f)
        
        sync_config = sheets_cfg['sync_config']
        spreadsheets = sheets_cfg['spreadsheets']
        
        # Conectar Redshift
        log("Conectando ao Redshift...")
        conn = psycopg2.connect(
            host=redshift_cfg['host'],
            port=redshift_cfg['port'],
            dbname=redshift_cfg['database'],
            user=redshift_cfg['user'],
            password=redshift_cfg['password'],
            sslmode='require',
            connect_timeout=15
        )
        cur = conn.cursor()
        log("✅ Conectado ao Redshift")
        
        # Autenticar Google
        log("Autenticando no Google...")
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
        log("✅ Autenticado no Google")
        
        # Listar tabelas
        log("Listando tabelas do schema dw...")
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'dw' ORDER BY tablename")
        all_tables = [row[0] for row in cur.fetchall()]
        tables = [t for t in all_tables if t not in sync_config['skip_tables']]
        log(f"✅ {len(tables)} tabelas para processar")
        
        # Categorizar
        categorized = {'dim': [], 'fato': [], 'outros': []}
        for table in tables:
            if table.startswith('dim_'):
                categorized['dim'].append(table)
            elif table.startswith('fato_'):
                categorized['fato'].append(table)
            else:
                categorized['outros'].append(table)
        
        # Mapear categorias para planilhas
        category_map = {
            'dim': 'dimensoes',
            'fato': 'fatos',
            'outros': 'outros'
        }
        
        # Função para sincronizar tabela
        def sync_table(table_name, spreadsheet_id):
            # Contar registros
            cur.execute(f'SELECT COUNT(*) FROM dw.{table_name}')
            total_count = cur.fetchone()[0]
            
            if total_count == 0:
                return 0, 'Vazia'
            
            # Determinar limite
            if total_count < 100000:
                limit = min(total_count, sync_config['max_rows_small'])
            elif total_count < 1000000:
                limit = sync_config['max_rows_medium']
            else:
                limit = sync_config['max_rows_large']
            
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
                rows = cur.fetchmany(sync_config['batch_size'])
                if not rows:
                    break
                for row in rows:
                    sheet_data.append([
                        str(val).replace('\x83', 'Ã').replace('\x93', 'Ó') 
                        if val is not None else '' 
                        for val in row
                    ])
            
            # Limpar aba existente
            sheet_title = table_name[:100]
            try:
                sheets_service.spreadsheets().values().clear(
                    spreadsheetId=spreadsheet_id,
                    range=f"'{sheet_title}'!A:ZZ"
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
            
            return len(sheet_data)-1, 'OK'
        
        # Processar cada categoria
        total_synced = 0
        total_errors = 0
        
        for cat_key, tables_list in categorized.items():
            if len(tables_list) == 0:
                continue
            
            sheet_key = category_map[cat_key]
            spreadsheet_id = spreadsheets[sheet_key]['id']
            sheet_name = spreadsheets[sheet_key]['name']
            
            log(f"\n{'='*70}")
            log(f"Processando: {sheet_name}")
            log(f"Tabelas: {len(tables_list)}")
            log(f"{'='*70}")
            
            # Criar índice
            index_data = [['Tabela', 'Total Registros', 'Sincronizados', 'Status', 'Atualização']]
            
            for table in tables_list:
                try:
                    synced, status = sync_table(table, spreadsheet_id)
                    
                    # Contar total
                    cur.execute(f'SELECT COUNT(*) FROM dw.{table}')
                    total = cur.fetchone()[0]
                    
                    index_data.append([
                        table, total, synced, status,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ])
                    
                    log(f"   ✅ {table}: {synced:,} registros")
                    total_synced += synced
                    
                except Exception as e:
                    log(f"   ❌ {table}: ERRO - {str(e)[:100]}")
                    index_data.append([table, 0, 0, f'Erro: {str(e)[:50]}', ''])
                    total_errors += 1
            
            # Atualizar índice
            try:
                sheets_service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range="'📋 Índice'!A1",
                    valueInputOption='RAW',
                    body={'values': index_data}
                ).execute()
                log(f"✅ Índice atualizado")
            except Exception as e:
                log(f"⚠️  Erro ao atualizar índice: {e}")
        
        conn.close()
        
        log("\n" + "="*70)
        log("✅ SINCRONIZAÇÃO CONCLUÍDA COM SUCESSO!")
        log(f"   Total de registros sincronizados: {total_synced:,}")
        log(f"   Erros: {total_errors}")
        log("="*70)
        
        return 0
        
    except Exception as e:
        log(f"\n❌ ERRO CRÍTICO: {e}")
        log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
