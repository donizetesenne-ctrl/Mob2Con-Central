# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  PIPELINE DE DADOS - DASHBOARD MOB2CON                         ║
║  Redshift → Google Sheets → dashboard_dados.json               ║
║                                                                  ║
║  Autor: Mob2Con Data Team                                        ║
║  Criado: 2026-05-15                                              ║
║  Descrição: Extrai dados agregados do Redshift, atualiza         ║
║             planilhas Google e gera JSON para o dashboard.        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import psycopg2
import psycopg2.extras
import gspread
from google.oauth2.service_account import Credentials

# ═══════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DE PATHS E LOGGING
# ═══════════════════════════════════════════════════════════════════

BASE_DIR = Path(r"C:\Users\Donizete Senne\Desktop\Mob2Con-Central")
CONFIG_FILE = BASE_DIR / "redshift_config.json"
OUTPUT_JSON = BASE_DIR / "dashboard_dados.json"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configuração de logging com timestamp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "dashboard.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("mob2con_dashboard")

# ═══════════════════════════════════════════════════════════════════
# IDs DAS PLANILHAS GOOGLE SHEETS
# ═══════════════════════════════════════════════════════════════════

SHEETS_CONFIG = {
    "dimensoes": "1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q",
    "fatos": "1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs",
    "lookups": "1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI"
}

# Escopo necessário para Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ═══════════════════════════════════════════════════════════════════
# QUERIES AGREGADAS (GROUP BY rede, mês)
# Todas usam agregações: SUM, COUNT, AVG — nunca linhas brutas
# ═══════════════════════════════════════════════════════════════════

QUERIES = {
    "promotores": """
        -- KPIs de promotores por rede e mês
        SELECT
            dr.nome_rede,
            TO_CHAR(fp.data_referencia, 'YYYY-MM') AS mes,
            COUNT(DISTINCT fp.id_promotor) AS total_promotores,
            SUM(CASE WHEN fp.status = 'Ativo' THEN 1 ELSE 0 END) AS promotores_ativos,
            SUM(CASE WHEN fp.status = 'Inativo' THEN 1 ELSE 0 END) AS promotores_inativos,
            ROUND(AVG(fp.score_promotor)::numeric, 2) AS score_medio,
            SUM(fp.horas_trabalhadas) AS total_horas
        FROM dw.fato_status_promotores fp
        LEFT JOIN dw.dim_rede dr ON fp.id_rede = dr.id_rede
        WHERE fp.data_referencia >= DATEADD(month, -3, CURRENT_DATE)
        GROUP BY dr.nome_rede, TO_CHAR(fp.data_referencia, 'YYYY-MM')
        ORDER BY dr.nome_rede, mes DESC
    """,

    "contratos_pontual": """
        -- Contratos pontuais por rede e mês
        SELECT
            dr.nome_rede,
            TO_CHAR(fc.data_referencia, 'YYYY-MM') AS mes,
            COUNT(*) AS total_contratos,
            SUM(CASE WHEN fc.status = 'Ativo' THEN 1 ELSE 0 END) AS contratos_ativos,
            SUM(CASE WHEN fc.status = 'Finalizado' THEN 1 ELSE 0 END) AS contratos_finalizados,
            SUM(fc.valor_contrato) AS valor_total
        FROM dw.fato_contrato_pontual fc
        LEFT JOIN dw.dim_rede dr ON fc.id_rede = dr.id_rede
        WHERE fc.data_referencia >= DATEADD(month, -3, CURRENT_DATE)
        GROUP BY dr.nome_rede, TO_CHAR(fc.data_referencia, 'YYYY-MM')
        ORDER BY dr.nome_rede, mes DESC
    """,

    "contratos_semanal": """
        -- Contratos semanais por rede e mês
        SELECT
            dr.nome_rede,
            TO_CHAR(fc.data_referencia, 'YYYY-MM') AS mes,
            COUNT(*) AS total_contratos,
            SUM(CASE WHEN fc.status = 'Ativo' THEN 1 ELSE 0 END) AS contratos_ativos,
            SUM(CASE WHEN fc.status = 'Finalizado' THEN 1 ELSE 0 END) AS contratos_finalizados,
            SUM(fc.valor_contrato) AS valor_total
        FROM dw.fato_contrato_semanal fc
        LEFT JOIN dw.dim_rede dr ON fc.id_rede = dr.id_rede
        WHERE fc.data_referencia >= DATEADD(month, -3, CURRENT_DATE)
        GROUP BY dr.nome_rede, TO_CHAR(fc.data_referencia, 'YYYY-MM')
        ORDER BY dr.nome_rede, mes DESC
    """,

    "documentacao": """
        -- Status de documentação por rede
        SELECT
            dr.nome_rede,
            TO_CHAR(fd.data_referencia, 'YYYY-MM') AS mes,
            SUM(fd.total_documentos) AS total_documentos,
            SUM(fd.documentos_aprovados) AS docs_aprovados,
            SUM(fd.documentos_pendentes) AS docs_pendentes,
            SUM(fd.documentos_reprovados) AS docs_reprovados,
            ROUND(
                (SUM(fd.documentos_aprovados)::float / NULLIF(SUM(fd.total_documentos), 0) * 100)::numeric, 1
            ) AS pct_aprovacao
        FROM dw.fato_agg_status_documentacao_redes fd
        LEFT JOIN dw.dim_rede dr ON fd.id_rede = dr.id_rede
        WHERE fd.data_referencia >= DATEADD(month, -3, CURRENT_DATE)
        GROUP BY dr.nome_rede, TO_CHAR(fd.data_referencia, 'YYYY-MM')
        ORDER BY dr.nome_rede, mes DESC
    """,

    "atividades_pendentes": """
        -- Atividades pendentes por rede
        SELECT
            dr.nome_rede,
            TO_CHAR(fa.data_referencia, 'YYYY-MM') AS mes,
            COUNT(*) AS total_atividades,
            SUM(CASE WHEN fa.status = 'Pendente' THEN 1 ELSE 0 END) AS pendentes,
            SUM(CASE WHEN fa.status = 'Concluída' THEN 1 ELSE 0 END) AS concluidas,
            SUM(CASE WHEN fa.status = 'Atrasada' THEN 1 ELSE 0 END) AS atrasadas
        FROM dw.fato_mobconnect_atividades_pendentes fa
        LEFT JOIN dw.dim_rede dr ON fa.id_rede = dr.id_rede
        WHERE fa.data_referencia >= DATEADD(month, -3, CURRENT_DATE)
        GROUP BY dr.nome_rede, TO_CHAR(fa.data_referencia, 'YYYY-MM')
        ORDER BY dr.nome_rede, mes DESC
    """,

    "scores_redes": """
        -- Scores por rede (último registro)
        SELECT
            dr.nome_rede,
            ts.score_geral,
            ts.score_documentacao,
            ts.score_operacional,
            ts.score_financeiro,
            TO_CHAR(ts.data_atualizacao, 'YYYY-MM-DD') AS ultima_atualizacao
        FROM dw.tbl_scores_redes ts
        LEFT JOIN dw.dim_rede dr ON ts.id_rede = dr.id_rede
        WHERE ts.data_atualizacao = (
            SELECT MAX(data_atualizacao) FROM dw.tbl_scores_redes
        )
        ORDER BY ts.score_geral DESC
    """,

    "redes_ativas": """
        -- Lista de redes ativas (dimensão)
        SELECT
            id_rede,
            nome_rede,
            regiao,
            estado,
            cidade,
            status
        FROM dw.dim_rede
        WHERE status = 'Ativa'
        ORDER BY nome_rede
    """
}


# ═══════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════════

def carregar_config():
    """Carrega credenciais do Redshift a partir do arquivo JSON de configuração."""
    logger.info(f"Carregando configuração de: {CONFIG_FILE}")
    
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {CONFIG_FILE}")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Campos obrigatórios
    campos_obrigatorios = ["host", "port", "dbname", "user", "password"]
    for campo in campos_obrigatorios:
        if campo not in config:
            raise KeyError(f"Campo obrigatório ausente no config: '{campo}'")
    
    logger.info(f"Config carregado | Host: {config['host']} | DB: {config['dbname']} | User: {config['user']}")
    return config


def conectar_redshift(config):
    """Estabelece conexão com o cluster Redshift."""
    logger.info("Conectando ao Redshift...")
    
    conn = psycopg2.connect(
        host=config["host"],
        port=config.get("port", 5439),
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"],
        sslmode="require",
        connect_timeout=30
    )
    
    logger.info("✅ Conexão com Redshift estabelecida com sucesso")
    return conn


def executar_query(conn, nome_query, sql):
    """
    Executa uma query individual e retorna DataFrame.
    Trata caso de tabela inexistente com try/except.
    """
    logger.info(f"Executando query: {nome_query}")
    
    try:
        df = pd.read_sql_query(sql, conn)
        logger.info(f"  → {nome_query}: {len(df)} registros retornados")
        return df
    
    except psycopg2.errors.UndefinedTable as e:
        logger.warning(f"  ⚠️  Tabela não encontrada para '{nome_query}': {e.diag.message_primary}")
        # Rollback para limpar o estado da transação
        conn.rollback()
        return pd.DataFrame()
    
    except psycopg2.errors.UndefinedColumn as e:
        logger.warning(f"  ⚠️  Coluna não encontrada para '{nome_query}': {e.diag.message_primary}")
        conn.rollback()
        return pd.DataFrame()
    
    except Exception as e:
        logger.error(f"  ❌ Erro na query '{nome_query}': {str(e)}")
        conn.rollback()
        return pd.DataFrame()


def extrair_dados_redshift(conn):
    """Executa todas as queries e retorna dicionário de DataFrames."""
    logger.info("=" * 60)
    logger.info("INICIANDO EXTRAÇÃO DE DADOS DO REDSHIFT")
    logger.info("=" * 60)
    
    resultados = {}
    
    for nome, sql in QUERIES.items():
        resultados[nome] = executar_query(conn, nome, sql)
    
    # Resumo da extração
    logger.info("-" * 40)
    logger.info("RESUMO DA EXTRAÇÃO:")
    for nome, df in resultados.items():
        status = "✅" if not df.empty else "⚠️ VAZIO"
        logger.info(f"  {status} {nome}: {len(df)} registros")
    logger.info("-" * 40)
    
    return resultados


# ═══════════════════════════════════════════════════════════════════
# MONTAGEM DO JSON PARA O DASHBOARD
# ═══════════════════════════════════════════════════════════════════

def montar_json_dashboard(resultados):
    """
    Monta a estrutura JSON otimizada para o Dashboard.
    Inclui: período, redes, kpis_overview, promotores, contratos, documentação, scores.
    """
    logger.info("Montando JSON do Dashboard...")
    
    agora = datetime.now()
    mes_atual = agora.strftime("%Y-%m")
    mes_anterior = (agora.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
    
    # ─── Período ───
    periodo = {
        "m1": agora.strftime("%b/%Y"),
        "m2": (agora.replace(day=1) - timedelta(days=1)).strftime("%b/%Y"),
        "gerado_em": agora.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # ─── Redes ativas ───
    df_redes = resultados.get("redes_ativas", pd.DataFrame())
    redes = df_redes.to_dict(orient="records") if not df_redes.empty else []
    
    # ─── KPIs Overview (totais gerais do mês atual) ───
    df_prom = resultados.get("promotores", pd.DataFrame())
    kpis_overview = {}
    
    if not df_prom.empty:
        # Filtrar mês atual
        df_mes_atual = df_prom[df_prom["mes"] == mes_atual] if "mes" in df_prom.columns else df_prom
        kpis_overview = {
            "total_promotores": int(df_mes_atual["total_promotores"].sum()) if "total_promotores" in df_mes_atual.columns else 0,
            "promotores_ativos": int(df_mes_atual["promotores_ativos"].sum()) if "promotores_ativos" in df_mes_atual.columns else 0,
            "promotores_inativos": int(df_mes_atual["promotores_inativos"].sum()) if "promotores_inativos" in df_mes_atual.columns else 0,
            "score_medio_geral": float(df_mes_atual["score_medio"].mean()) if "score_medio" in df_mes_atual.columns else 0.0,
            "total_redes_ativas": len(redes)
        }
    
    # ─── Promotores (dados por rede/mês) ───
    promotores = df_prom.to_dict(orient="records") if not df_prom.empty else []
    
    # ─── Contratos (pontual + semanal) ───
    df_cp = resultados.get("contratos_pontual", pd.DataFrame())
    df_cs = resultados.get("contratos_semanal", pd.DataFrame())
    
    contratos = {
        "pontual": df_cp.to_dict(orient="records") if not df_cp.empty else [],
        "semanal": df_cs.to_dict(orient="records") if not df_cs.empty else [],
        "resumo": {
            "total_pontual": int(df_cp["total_contratos"].sum()) if not df_cp.empty and "total_contratos" in df_cp.columns else 0,
            "total_semanal": int(df_cs["total_contratos"].sum()) if not df_cs.empty and "total_contratos" in df_cs.columns else 0,
            "valor_total_pontual": float(df_cp["valor_total"].sum()) if not df_cp.empty and "valor_total" in df_cp.columns else 0.0,
            "valor_total_semanal": float(df_cs["valor_total"].sum()) if not df_cs.empty and "valor_total" in df_cs.columns else 0.0,
        }
    }
    
    # ─── Documentação ───
    df_doc = resultados.get("documentacao", pd.DataFrame())
    df_ativ = resultados.get("atividades_pendentes", pd.DataFrame())
    
    documentacao = {
        "status_por_rede": df_doc.to_dict(orient="records") if not df_doc.empty else [],
        "atividades_pendentes": df_ativ.to_dict(orient="records") if not df_ativ.empty else [],
        "resumo": {
            "total_documentos": int(df_doc["total_documentos"].sum()) if not df_doc.empty and "total_documentos" in df_doc.columns else 0,
            "docs_aprovados": int(df_doc["docs_aprovados"].sum()) if not df_doc.empty and "docs_aprovados" in df_doc.columns else 0,
            "docs_pendentes": int(df_doc["docs_pendentes"].sum()) if not df_doc.empty and "docs_pendentes" in df_doc.columns else 0,
            "atividades_pendentes_total": int(df_ativ["pendentes"].sum()) if not df_ativ.empty and "pendentes" in df_ativ.columns else 0,
        }
    }
    
    # ─── Scores por rede ───
    df_scores = resultados.get("scores_redes", pd.DataFrame())
    scores = df_scores.to_dict(orient="records") if not df_scores.empty else []
    
    # ─── Montagem final ───
    dashboard_data = {
        "periodo": periodo,
        "redes": redes,
        "kpis_overview": kpis_overview,
        "promotores": promotores,
        "contratos": contratos,
        "documentacao": documentacao,
        "scores": scores
    }
    
    logger.info(f"JSON montado com sucesso | Redes: {len(redes)} | Promotores: {len(promotores)} registros")
    return dashboard_data


def salvar_json(data):
    """Salva o JSON do dashboard no arquivo de saída."""
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    tamanho_kb = OUTPUT_JSON.stat().st_size / 1024
    logger.info(f"✅ JSON salvo: {OUTPUT_JSON} ({tamanho_kb:.1f} KB)")


# ═══════════════════════════════════════════════════════════════════
# ATUALIZAÇÃO DAS PLANILHAS GOOGLE SHEETS
# ═══════════════════════════════════════════════════════════════════

def conectar_google_sheets():
    """
    Conecta ao Google Sheets via Service Account.
    Procura o arquivo de credenciais em locais padrão.
    """
    logger.info("Conectando ao Google Sheets...")
    
    # Caminhos possíveis para o arquivo de credenciais do Service Account
    caminhos_credenciais = [
        BASE_DIR / "google_credentials.json",
        BASE_DIR / "service_account.json",
        BASE_DIR / "credentials.json",
        Path.home() / ".config" / "gspread" / "service_account.json",
    ]
    
    credencial_path = None
    for caminho in caminhos_credenciais:
        if caminho.exists():
            credencial_path = caminho
            break
    
    if credencial_path is None:
        raise FileNotFoundError(
            "Arquivo de credenciais Google não encontrado. "
            "Coloque 'google_credentials.json' (Service Account) em:\n"
            f"  {BASE_DIR}\n"
            "Ou configure em ~/.config/gspread/service_account.json"
        )
    
    logger.info(f"Credenciais encontradas: {credencial_path}")
    
    creds = Credentials.from_service_account_file(str(credencial_path), scopes=SCOPES)
    client = gspread.authorize(creds)
    
    logger.info("✅ Conexão com Google Sheets estabelecida")
    return client


def df_para_sheet(worksheet, df, incluir_header=True):
    """
    Atualiza uma aba da planilha com dados de um DataFrame.
    Limpa a aba antes de inserir os novos dados.
    """
    if df.empty:
        logger.warning(f"  ⚠️  DataFrame vazio - aba não atualizada")
        return
    
    # Limpar aba existente
    worksheet.clear()
    
    # Preparar dados (header + linhas)
    if incluir_header:
        dados = [df.columns.tolist()] + df.fillna("").values.tolist()
    else:
        dados = df.fillna("").values.tolist()
    
    # Converter tipos numpy para Python nativo
    dados_limpos = []
    for linha in dados:
        linha_limpa = []
        for val in linha:
            if isinstance(val, (pd.Timestamp,)):
                linha_limpa.append(str(val))
            elif hasattr(val, 'item'):  # numpy types
                linha_limpa.append(val.item())
            else:
                linha_limpa.append(val)
        dados_limpos.append(linha_limpa)
    
    # Atualizar em batch (mais eficiente que célula por célula)
    worksheet.update(dados_limpos, value_input_option="USER_ENTERED")
    logger.info(f"  → Aba atualizada: {len(dados_limpos)-1} linhas × {len(dados_limpos[0])} colunas")


def atualizar_google_sheets(client, resultados):
    """
    Atualiza as 3 planilhas Google Sheets com os dados extraídos.
    
    - Dimensões: redes ativas
    - Fatos: promotores, contratos, documentação, atividades
    - Lookups: scores por rede
    """
    logger.info("=" * 60)
    logger.info("ATUALIZANDO GOOGLE SHEETS")
    logger.info("=" * 60)
    
    try:
        # ─── 1. Planilha DIMENSÕES ───
        logger.info("📊 Atualizando planilha: Dimensões")
        sh_dim = client.open_by_key(SHEETS_CONFIG["dimensoes"])
        
        # Aba: Redes
        try:
            ws_redes = sh_dim.worksheet("Redes")
        except gspread.exceptions.WorksheetNotFound:
            ws_redes = sh_dim.add_worksheet(title="Redes", rows=500, cols=20)
        
        df_redes = resultados.get("redes_ativas", pd.DataFrame())
        df_para_sheet(ws_redes, df_redes)
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar Dimensões: {e}")
    
    try:
        # ─── 2. Planilha FATOS ───
        logger.info("📊 Atualizando planilha: Fatos")
        sh_fatos = client.open_by_key(SHEETS_CONFIG["fatos"])
        
        # Aba: Promotores
        try:
            ws_prom = sh_fatos.worksheet("Promotores")
        except gspread.exceptions.WorksheetNotFound:
            ws_prom = sh_fatos.add_worksheet(title="Promotores", rows=2000, cols=20)
        df_para_sheet(ws_prom, resultados.get("promotores", pd.DataFrame()))
        
        # Aba: Contratos_Pontual
        try:
            ws_cp = sh_fatos.worksheet("Contratos_Pontual")
        except gspread.exceptions.WorksheetNotFound:
            ws_cp = sh_fatos.add_worksheet(title="Contratos_Pontual", rows=2000, cols=20)
        df_para_sheet(ws_cp, resultados.get("contratos_pontual", pd.DataFrame()))
        
        # Aba: Contratos_Semanal
        try:
            ws_cs = sh_fatos.worksheet("Contratos_Semanal")
        except gspread.exceptions.WorksheetNotFound:
            ws_cs = sh_fatos.add_worksheet(title="Contratos_Semanal", rows=2000, cols=20)
        df_para_sheet(ws_cs, resultados.get("contratos_semanal", pd.DataFrame()))
        
        # Aba: Documentacao
        try:
            ws_doc = sh_fatos.worksheet("Documentacao")
        except gspread.exceptions.WorksheetNotFound:
            ws_doc = sh_fatos.add_worksheet(title="Documentacao", rows=2000, cols=20)
        df_para_sheet(ws_doc, resultados.get("documentacao", pd.DataFrame()))
        
        # Aba: Atividades_Pendentes
        try:
            ws_ativ = sh_fatos.worksheet("Atividades_Pendentes")
        except gspread.exceptions.WorksheetNotFound:
            ws_ativ = sh_fatos.add_worksheet(title="Atividades_Pendentes", rows=2000, cols=20)
        df_para_sheet(ws_ativ, resultados.get("atividades_pendentes", pd.DataFrame()))
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar Fatos: {e}")
    
    try:
        # ─── 3. Planilha LOOKUPS ───
        logger.info("📊 Atualizando planilha: Lookups")
        sh_lookups = client.open_by_key(SHEETS_CONFIG["lookups"])
        
        # Aba: Scores
        try:
            ws_scores = sh_lookups.worksheet("Scores")
        except gspread.exceptions.WorksheetNotFound:
            ws_scores = sh_lookups.add_worksheet(title="Scores", rows=500, cols=20)
        df_para_sheet(ws_scores, resultados.get("scores_redes", pd.DataFrame()))
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar Lookups: {e}")
    
    logger.info("✅ Atualização do Google Sheets concluída")


# ═══════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL (PIPELINE COMPLETO)
# ═══════════════════════════════════════════════════════════════════

def main():
    """
    Pipeline completo:
    1. Carrega configuração
    2. Conecta ao Redshift
    3. Extrai dados agregados
    4. Monta JSON do dashboard
    5. Salva JSON local
    6. Atualiza Google Sheets
    """
    inicio = datetime.now()
    
    logger.info("╔══════════════════════════════════════════════════════════════╗")
    logger.info("║  PIPELINE MOB2CON - INÍCIO DA EXECUÇÃO                     ║")
    logger.info(f"║  {inicio.strftime('%Y-%m-%d %H:%M:%S')}                                       ║")
    logger.info("╚══════════════════════════════════════════════════════════════╝")
    
    conn = None
    
    try:
        # 1. Carregar configuração
        config = carregar_config()
        
        # 2. Conectar ao Redshift
        conn = conectar_redshift(config)
        
        # 3. Extrair dados
        resultados = extrair_dados_redshift(conn)
        
        # 4. Montar JSON
        dashboard_data = montar_json_dashboard(resultados)
        
        # 5. Salvar JSON local
        salvar_json(dashboard_data)
        
        # 6. Atualizar Google Sheets
        try:
            client = conectar_google_sheets()
            atualizar_google_sheets(client, resultados)
        except FileNotFoundError as e:
            logger.warning(f"⚠️  Google Sheets não atualizado: {e}")
            logger.info("   O JSON local foi gerado com sucesso. Configure as credenciais para habilitar o Sheets.")
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar Google Sheets: {e}")
            logger.info("   O JSON local foi gerado com sucesso mesmo sem o Sheets.")
        
        # Sucesso!
        duracao = (datetime.now() - inicio).total_seconds()
        logger.info("=" * 60)
        logger.info(f"✅ Dashboard atualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"⏱️  Tempo total: {duracao:.1f} segundos")
        logger.info("=" * 60)
        
        print(f"\n✅ Dashboard atualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except FileNotFoundError as e:
        logger.error(f"❌ Arquivo não encontrado: {e}")
        sys.exit(1)
    
    except psycopg2.OperationalError as e:
        logger.error(f"❌ Erro de conexão com Redshift: {e}")
        sys.exit(1)
    
    except KeyError as e:
        logger.error(f"❌ Configuração inválida: {e}")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        # Sempre fecha a conexão
        if conn:
            conn.close()
            logger.info("Conexão com Redshift encerrada")


# ═══════════════════════════════════════════════════════════════════
# EXECUÇÃO
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
