#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGENTE MOB2CON - Powered by Agno Framework
Agente inteligente para analise e atualizacao do Dashboard de Performance

Uso: python agente_mob2con.py
Requer: pip install agno google-auth google-api-python-client
Variavel: OPENAI_API_KEY ou GROQ_API_KEY
"""

import os, json, re, shutil
from datetime import datetime
from pathlib import Path

from agno.agent import Agent
from agno.models.groq import Groq

# ============================================================
# CONFIGURACAO
# ============================================================
os.environ["GROQ_API_KEY"] = "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"

CONFIG = {
    "html_path": r"C:\Users\Donizete Senne\Desktop\Mob2Con-Central\03-Documentacao\📊 Dashboard Dados Reais.html",
    "sheets": {
        "dimensoes": "1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q",
        "fatos": "1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs",
        "lookups": "1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI",
    },
    "drive_file_id": "1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc",
    "dashboard_url": "https://script.google.com/macros/s/AKfycbwkF4in7_FjTDUwruBtl-LRGw5ugQcrMmdb63TbJO091MGJu4y_1keuHRrdFrLyxTrdZw/exec",
    "redes": ["BIGBOX", "GBARBOSA", "NORDESTAO", "NOVAERA", "PREZUNIC", "PAGUEMENOS"],
    "token_path": r"C:\Users\Donizete Senne\.aws\amazonq\universal-control\credentials\google-oauth-token.json",
}


# ============================================================
# FERRAMENTAS DO AGENTE
# ============================================================

def ler_google_sheets(sheet_id: str, aba: str) -> str:
    """Le dados de uma aba do Google Sheets usando OAuth."""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        with open(CONFIG["token_path"], "r") as f:
            token_data = json.load(f)
        creds = Credentials.from_authorized_user_info(token_data)
        service = build("sheets", "v4", credentials=creds)
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"{aba}!A1:Z100"
        ).execute()
        values = result.get("values", [])
        if not values:
            return json.dumps({"error": "Sem dados", "aba": aba})
        cols = values[0]
        rows = [dict(zip(cols, row + [None]*(len(cols)-len(row)))) for row in values[1:]]
        return json.dumps({"aba": aba, "total": len(rows), "colunas": cols, "amostra": rows[:5]}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "aba": aba})


def analisar_dashboard_html() -> str:
    """Le o dashboard HTML e retorna metricas sobre os dados atuais."""
    try:
        with open(CONFIG["html_path"], "r", encoding="utf-8") as f:
            html = f.read()
        metricas = {
            "tamanho_bytes": len(html),
            "total_linhas": html.count("\n"),
            "cards_vazios": html.count(">—<"),
            "total_tooltips": html.count("tooltip-wrapper"),
            "redes_encontradas": [r for r in CONFIG["redes"] if r in html],
            "tem_gestao_performance": "DATA_GESTAO_PERFORMANCE" in html,
            "tem_promotores": "DATA_PROMOTORES" in html,
        }
        return json.dumps(metricas, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


def upload_dashboard_drive() -> str:
    """Faz upload do dashboard HTML para o Google Drive."""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        with open(CONFIG["token_path"], "r") as f:
            token_data = json.load(f)
        creds = Credentials.from_authorized_user_info(token_data)
        service = build("drive", "v3", credentials=creds)
        media = MediaFileUpload(CONFIG["html_path"], mimetype="text/html")
        service.files().update(fileId=CONFIG["drive_file_id"], media_body=media).execute()
        return json.dumps({"sucesso": True, "link": CONFIG["dashboard_url"],
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"sucesso": False, "error": str(e)})


def gerar_relatorio_performance() -> str:
    """Gera relatorio de performance baseado nos dados do dashboard."""
    try:
        with open(CONFIG["html_path"], "r", encoding="utf-8") as f:
            html = f.read()
        confiabilidade = {}
        for rede in CONFIG["redes"]:
            match = re.search(rf"{rede}.*?confiabilidade:\s*([\d.]+)", html)
            if match:
                confiabilidade[rede] = float(match.group(1))
        alertas = []
        for rede, conf in confiabilidade.items():
            if conf == 0:
                alertas.append(f"CRITICO: {rede} com 0% de confiabilidade")
            elif conf < 0.85:
                alertas.append(f"ATENCAO: {rede} com {conf*100:.0f}% de confiabilidade")
        return json.dumps({
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "confiabilidade": {k: f"{v*100:.0f}%" for k, v in confiabilidade.items()},
            "alertas": alertas,
            "redes_ok": sum(1 for v in confiabilidade.values() if v >= 0.9),
            "redes_criticas": sum(1 for v in confiabilidade.values() if v < 0.5),
            "link": CONFIG["dashboard_url"],
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ============================================================
# AGENTE PRINCIPAL
# ============================================================

def criar_agente():
    agente = Agent(
        name="Mob2Con Dashboard Agent",
        model=Groq(id="llama-3.3-70b-versatile"),
        instructions="""Voce e o agente de analise do Dashboard Mob2Con.
Seu papel:
1. Analisar dados de performance das redes de supermercados
2. Identificar alertas criticos (ruptura > 5%, confiabilidade < 90%, horas < 80%)
3. Gerar insights acionaveis para a equipe
4. Atualizar o dashboard HTML quando necessario
5. Reportar status diario

Redes: BIGBOX, GBARBOSA, NORDESTAO, NOVAERA, PREZUNIC, PAGUEMENOS
Metricas: Venda R$, Ruptura (meta <5%), Horas (meta >80%), Confiabilidade (meta >90%)
Sempre responda em portugues brasileiro. Use emojis para alertas.
""",
        tools=[ler_google_sheets, analisar_dashboard_html, upload_dashboard_drive, gerar_relatorio_performance],
        markdown=True,
    )
    return agente


# ============================================================
# MAIN
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("  AGENTE MOB2CON - Powered by Agno v2.6")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60 + "\n")

    if not os.environ.get("GROQ_API_KEY"):
        print("GROQ_API_KEY nao configurada.")
        print("   Verifique o arquivo agente_mob2con.py")
        return

    agente = criar_agente()
    print("Agente pronto! Exemplos:")
    print("   - 'Analise o dashboard atual'")
    print("   - 'Gere um relatorio de performance'")
    print("   - 'Quais redes estao com problemas?'")
    print("   - 'sair' para encerrar\n")

    while True:
        try:
            pergunta = input("Voce: ").strip()
            if not pergunta:
                continue
            if pergunta.lower() in ("sair", "exit", "quit"):
                print("\nAte a proxima!")
                break
            print("\nAgente:")
            resposta = agente.run(pergunta)
            print(resposta.content)
            print("")
        except KeyboardInterrupt:
            print("\nEncerrado.")
            break
        except Exception as e:
            print(f"\nErro: {e}\n")


if __name__ == "__main__":
    main()
