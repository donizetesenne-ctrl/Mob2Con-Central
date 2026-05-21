import psycopg2
import json

with open('redshift_config.json', 'r') as f:
    cfg = json.load(f)

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

# Listar todas as tabelas do schema dw com contagem de registros
cur.execute("""
    SELECT 
        schemaname, 
        tablename
    FROM pg_tables 
    WHERE schemaname = 'dw'
    ORDER BY tablename
""")

tables = cur.fetchall()
print(f"=== TABELAS NO SCHEMA DW ({len(tables)} tabelas) ===\n")

for i, (schema, table) in enumerate(tables, 1):
    # Contar registros
    try:
        cur.execute(f'SELECT COUNT(*) FROM {schema}.{table}')
        count = cur.fetchone()[0]
        print(f"{i:2d}. {table:<50} ({count:,} registros)")
    except Exception as e:
        print(f"{i:2d}. {table:<50} (erro ao contar)")

conn.close()
