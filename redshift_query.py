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

# Listar schemas e tabelas
cur.execute("""
    SELECT schemaname, tablename 
    FROM pg_tables 
    WHERE schemaname NOT IN ('pg_catalog','information_schema','pg_internal')
    ORDER BY schemaname, tablename
    LIMIT 50
""")

rows = cur.fetchall()
print("=== CONEXAO OK! ===")
print(f"Database: {cfg['database']}")
print(f"Tabelas encontradas: {len(rows)}\n")
print(f"{'SCHEMA':<20} {'TABELA':<40}")
print("-" * 60)
for schema, table in rows:
    print(f"{schema:<20} {table:<40}")

conn.close()
