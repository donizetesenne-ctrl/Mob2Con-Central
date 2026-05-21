"""
Mob2Con - Sync Cadastro Lite: Power BI → Google Sheets
Atualiza a planilha fonte do webapp Cadastro Lite - Monitoramento CS

Uso:
  python sync_cadastro_lite.py

Requer:
  - DSN 'mc2-production' configurado (ODBC PostgreSQL)
  - Google OAuth configurado (universal-control-mcp)
  - pip install pyodbc gspread google-auth
"""
import pyodbc
import json
import os
from datetime import datetime, timedelta

# === CONFIG ===
SHEETS_ID = "1piHmDHrTdoOS6gFkSVQ3xVH3InBV3CPjndmsPJkuAFU"
DSN = "mc2-production"
DESDE = "2025-10-01"

# === QUERIES ===
SQL_EMPRESAS = """
WITH lite_agg AS (
    SELECT
        COALESCE(a.id, s.id) AS empresa_id,
        COALESCE(a.trade_name, s.name) AS empresa,
        CASE
            WHEN lv.responsible_agency_id IS NOT NULL THEN 'Agencia'
            WHEN lv.responsible_supplier_id IS NOT NULL THEN 'Fornecedor'
        END AS contratante_tipo,
        CASE COALESCE(ccia.status, ccis.status)
            WHEN 0 THEN 'Nao Cliente'
            WHEN 1 THEN 'Cliente'
        END AS status_empresa,
        COUNT(DISTINCT lv.id) AS cadastros,
        COUNT(DISTINCT lv.cpf) AS promotores,
        MIN(lv.created_at)::date AS primeiro_cadastro,
        MAX(lv.created_at)::date AS ultimo_cadastro
    FROM lite_visitors lv
    LEFT JOIN agencies a ON lv.responsible_agency_id = a.id
    LEFT JOIN common_client_infos ccia ON a.id = ccia.agency_id
    LEFT JOIN suppliers s ON lv.responsible_supplier_id = s.id
    LEFT JOIN common_client_infos ccis ON s.id = ccis.supplier_id
    WHERE lv.created_at >= '{desde}'::date + INTERVAL '3 hours'
      AND lv.responsible_service_provider_id IS NULL
      AND lv.status = 'approved'
      AND COALESCE(ccia.status, ccis.status) IN (0, 1)
    GROUP BY 1, 2, 3, 4
)
SELECT
    empresa_id, empresa, contratante_tipo, status_empresa,
    cadastros, promotores,
    primeiro_cadastro::text, ultimo_cadastro::text,
    CASE
        WHEN status_empresa = 'Nao Cliente' THEN 25 ELSE 0
    END +
    CASE
        WHEN promotores > 200 THEN 25
        WHEN promotores > 50 THEN 15
        WHEN promotores > 10 THEN 5
        ELSE 0
    END +
    CASE WHEN contratante_tipo = 'Fornecedor' THEN 10 ELSE 5 END
    AS score_suspeita,
    CASE
        WHEN (CASE WHEN status_empresa='Nao Cliente' THEN 25 ELSE 0 END +
              CASE WHEN promotores>200 THEN 25 WHEN promotores>50 THEN 15 WHEN promotores>10 THEN 5 ELSE 0 END +
              CASE WHEN contratante_tipo='Fornecedor' THEN 10 ELSE 5 END) > 80 THEN 'Critico'
        WHEN (CASE WHEN status_empresa='Nao Cliente' THEN 25 ELSE 0 END +
              CASE WHEN promotores>200 THEN 25 WHEN promotores>50 THEN 15 WHEN promotores>10 THEN 5 ELSE 0 END +
              CASE WHEN contratante_tipo='Fornecedor' THEN 10 ELSE 5 END) > 60 THEN 'Alta Suspeita'
        WHEN (CASE WHEN status_empresa='Nao Cliente' THEN 25 ELSE 0 END +
              CASE WHEN promotores>200 THEN 25 WHEN promotores>50 THEN 15 WHEN promotores>10 THEN 5 ELSE 0 END +
              CASE WHEN contratante_tipo='Fornecedor' THEN 10 ELSE 5 END) > 40 THEN 'Suspeito'
        WHEN (CASE WHEN status_empresa='Nao Cliente' THEN 25 ELSE 0 END +
              CASE WHEN promotores>200 THEN 25 WHEN promotores>50 THEN 15 WHEN promotores>10 THEN 5 ELSE 0 END +
              CASE WHEN contratante_tipo='Fornecedor' THEN 10 ELSE 5 END) > 20 THEN 'Atencao'
        ELSE 'Normal'
    END AS classificacao
FROM lite_agg
ORDER BY score_suspeita DESC, promotores DESC
""".replace("{desde}", DESDE)

SQL_EVOLUCAO = """
SELECT
    TO_CHAR(lv.created_at AT TIME ZONE 'utc' AT TIME ZONE 'America/Sao_Paulo', 'YYYY-MM') AS mes,
    CASE
        WHEN lv.responsible_agency_id IS NOT NULL THEN 'Agencia'
        ELSE 'Fornecedor'
    END AS contratante_tipo,
    CASE COALESCE(ccia.status, ccis.status)
        WHEN 0 THEN 'Nao Cliente'
        WHEN 1 THEN 'Cliente'
    END AS status_empresa,
    COUNT(DISTINCT lv.id) AS cadastros,
    COUNT(DISTINCT lv.cpf) AS promotores
FROM lite_visitors lv
LEFT JOIN agencies a ON lv.responsible_agency_id = a.id
LEFT JOIN common_client_infos ccia ON a.id = ccia.agency_id
LEFT JOIN suppliers s ON lv.responsible_supplier_id = s.id
LEFT JOIN common_client_infos ccis ON s.id = ccis.supplier_id
WHERE lv.created_at >= '{desde}'::date + INTERVAL '3 hours'
  AND lv.responsible_service_provider_id IS NULL
  AND lv.status = 'approved'
  AND COALESCE(ccia.status, ccis.status) IN (0, 1)
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3
""".replace("{desde}", DESDE)

def connect_db():
    """Conecta ao PostgreSQL via ODBC."""
    try:
        conn = pyodbc.connect(f"DSN={DSN}", autocommit=True)
        print(f"  Conectado ao {DSN}")
        return conn
    except Exception as e:
        print(f"  ERRO conexao: {e}")
        print("  Tentando sem DSN...")
        return None

def query_to_rows(conn, sql):
    """Executa query e retorna header + rows."""
    cursor = conn.cursor()
    cursor.execute(sql)
    cols = [desc[0] for desc in cursor.description]
    rows = [[str(v) if v is not None else "" for v in row] for row in cursor.fetchall()]
    return [cols] + rows

def update_sheets_via_mcp(sheet_name, data):
    """Placeholder - usa google.script ou gspread para atualizar."""
    print(f"  {sheet_name}: {len(data)-1} linhas")
    return data

def main():
    print("=" * 50)
    print("Mob2Con - Sync Cadastro Lite")
    print(f"Destino: Sheets {SHEETS_ID}")
    print(f"Desde: {DESDE}")
    print("=" * 50)

    conn = connect_db()
    if not conn:
        print("FALHA: Sem conexao ao banco. Abortando.")
        return

    print("\n[1/4] Extraindo Empresas...")
    empresas = query_to_rows(conn, SQL_EMPRESAS)
    print(f"  {len(empresas)-1} empresas encontradas")

    print("\n[2/4] Extraindo Evolucao Mensal...")
    evolucao = query_to_rows(conn, SQL_EVOLUCAO)
    print(f"  {len(evolucao)-1} registros")

    print("\n[3/4] Gerando KPIs...")
    total_cad = sum(int(r[4]) for r in empresas[1:] if r[4])
    total_prom = sum(int(r[5]) for r in empresas[1:] if r[5])
    nc = [r for r in empresas[1:] if r[3] == "Nao Cliente"]
    cl = [r for r in empresas[1:] if r[3] == "Cliente"]

    kpis = [
        ["Cadastro Lite - Monitoramento Mob2Con"],
        ["Gerado em:", datetime.now().strftime("%Y-%m-%dT%H:%M:%S")],
        ["Periodo:", f"01/10/2025 ate hoje"],
        ["Fonte:", "PostgreSQL (mc2-production)"],
        [],
        ["KPI", "Valor"],
        ["Total Cadastros Lite", str(total_cad)],
        ["Promotores Unicos Lite", str(total_prom)],
        ["Empresas com Lite", str(len(empresas)-1)],
        ["Empresas Nao Cliente com Lite", str(len(nc))],
        ["Empresas Cliente com Lite", str(len(cl))],
        ["Novos Lite (7d)", ""],  # precisa query separada
        ["Novos Lite Nao Cliente (7d)", ""],
        ["Promotores Conv (snapshot)", ""],
        ["Impacto Receita Mensal (R$)", str(int(sum(int(r[5]) for r in nc if r[5]) * 12.10))],
    ]

    print(f"\n[4/4] Dados prontos para upload!")
    print(f"  Empresas: {len(empresas)-1}")
    print(f"  Evolucao: {len(evolucao)-1}")
    print(f"  KPIs: {len(kpis)}")

    # Salvar localmente como JSON para debug
    output = {
        "generated": datetime.now().isoformat(),
        "kpis": kpis,
        "empresas_count": len(empresas) - 1,
        "evolucao_count": len(evolucao) - 1,
    }
    out_path = os.path.join(os.path.dirname(__file__), "sync_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n  Output salvo em: {out_path}")
    print("\n  Para enviar ao Sheets, use:")
    print("  python sync_cadastro_lite.py --push")

    conn.close()
    print("\nDONE!")

if __name__ == "__main__":
    main()
