#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE RELATÓRIO SEMANAL AUTOMÁTICO — Mob2Con v2.0
Docs → Python → HTML → Gmail
"""
import os, sys, json, re, base64, logging, argparse
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Dict, Optional

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaInMemoryUpload
except ImportError:
    print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/gmail.send',
]

CONFIG = {
    'DOCUMENT_ID': '1mqlmUkxKaVoVm5FFHjrNp4A8OPM2BKWdIgDIUZZk--0',
    'FOLDER_ID':   '1sc90vFM_Jghjlv0p7LCuePqrwfUFhQlt',
    'CREDENTIALS_PATH': Path.home() / '.aws' / 'amazonq' / 'universal-control' / 'google-credentials.json',
    'TOKEN_PATH':       Path.home() / '.aws' / 'amazonq' / 'universal-control' / 'token_v2.json',
    'BACKUP_DIR': Path(__file__).parent / 'backups',
    'LOG_DIR':    Path(__file__).parent / 'logs',
    'EMAIL_GESTORA': 'mariliana.fagotti@mob2con.com.br',
    'NOME_GESTORA':  'Mariliana Fagotti',
    'EMPRESA':       'Mob2Con',
    'RESPONSAVEL':   'Donizete Senne',
    'CORES': {
        'MCP': '#F46901', 'Power BI': '#F2C811', 'Apps Script': '#6F05D4',
        'Dados': '#4285F4', 'Reunião': '#434343', 'Doc': '#107C41',
        'Bug Fix': '#C00000', 'Melhoria': '#107C41', 'Pendência': '#F2B100', 'Geral': '#605E5C',
    },
    'ICONES': {
        'MCP': '⚙️', 'Power BI': '📊', 'Apps Script': '🤖', 'Dados': '🗄️',
        'Reunião': '👥', 'Doc': '📝', 'Bug Fix': '🐛', 'Melhoria': '✨',
        'Pendência': '⏳', 'Geral': '📋',
    },
}

CONFIG['LOG_DIR'].mkdir(parents=True, exist_ok=True)
CONFIG['BACKUP_DIR'].mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(CONFIG['LOG_DIR'] / f"relatorio_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
              logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
def autenticar_google() -> Credentials:
    creds = None
    if CONFIG['TOKEN_PATH'].exists():
        creds = Credentials.from_authorized_user_file(str(CONFIG['TOKEN_PATH']), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CONFIG['CREDENTIALS_PATH'].exists():
                logger.error(f"credentials.json nao encontrado: {CONFIG['CREDENTIALS_PATH']}"); sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CONFIG['CREDENTIALS_PATH']), SCOPES)
            creds = flow.run_local_server(port=0)
        CONFIG['TOKEN_PATH'].parent.mkdir(parents=True, exist_ok=True)
        CONFIG['TOKEN_PATH'].write_text(creds.to_json())
        logger.info("Token salvo")
    return creds

def extrair_texto_docs(doc_id: str, creds) -> str:
    service = build('docs', 'v1', credentials=creds)
    doc = service.documents().get(documentId=doc_id).execute()
    texto = ''.join(
        tr['textRun']['content']
        for el in doc.get('body',{}).get('content',[])
        if 'paragraph' in el
        for tr in el['paragraph'].get('elements',[])
        if 'textRun' in tr
    )
    logger.info(f"Extraido {len(texto)} chars do Docs")
    (CONFIG['BACKUP_DIR'] / f"diario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt").write_text(texto, encoding='utf-8')
    return texto

# ═══════════════════════════════════════════════════════════════
def detectar_data(linha):
    for p in [r'\[DATA\]\s*\w+\s+(\d{1,2})/(\d{1,2})', r'(\d{1,2})/(\d{1,2})/(\d{4})',
              r'(?:^\s*---\s*)?(?:\w+\s+)?(\d{1,2})/(\d{1,2})(?:\s*$)']:
        m = re.search(p, linha, re.IGNORECASE)
        if m:
            try:
                g = m.groups()
                d, mes = int(g[0]), int(g[1])
                ano = int(g[2]) if len(g)==3 else datetime.now().year
                return datetime(ano, mes, d)
            except: pass
    return None

def detectar_categoria(linha):
    ll = linha.lower()
    for cat, kws in {
        'MCP': ['mcp','universal-control','oauth','servidor','bridge'],
        'Power BI': ['power bi','pbi','dashboard','dax','medida','visual','layout'],
        'Apps Script': ['apps script','script','trigger','automação','form'],
        'Dados': ['dados','etl','tratamento','fonte','tabela','query','sql'],
        'Reunião': ['reunião','meeting','alinhamento','planning','sprint'],
        'Doc': ['documentação','doc','manual','guia'],
        'Bug Fix': ['bug','correção','fix','erro','corrigir'],
        'Melhoria': ['melhoria','otimização','refactor','implementar'],
        'Pendência': ['pendência','aguardando','bloqueado','waiting'],
    }.items():
        if any(k in ll for k in kws): return cat
    return 'Geral'

def processar_texto(texto):
    linhas = texto.split('\n')
    registros, data_atual, buffer, cat_atual = [], None, [], 'Geral'
    _IGN = ['não precisa','apenas jogue','dicas:','❌ formatar','✅ use [data]']
    def flush():
        if buffer and data_atual:
            desc = ' '.join(buffer).strip()
            titulo = buffer[0].strip()[:100]
            if not titulo or any(p in desc.lower() for p in _IGN): return
            registros.append({'data': data_atual.strftime('%Y-%m-%d'), 'categoria': cat_atual,
                'titulo': titulo, 'descricao': desc,
                'tags': list(set(re.findall(r'#(\w+)', desc)))[:5],
                'status': 'Pendência' if any(p in desc.lower() for p in ['pendência','aguardando','bloqueado']) else 'Concluído'})
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith('═'): continue
        nd = detectar_data(linha)
        if nd: flush(); buffer=[]; data_atual=nd; cat_atual='Geral'; continue
        if linha.startswith(('•','-','*')): flush(); buffer=[]; cat_atual=detectar_categoria(linha); buffer.append(linha.lstrip('•-* '))
        else: buffer.append(linha)
    flush()
    vistos = {}
    for r in registros:
        k = (r['data'], r['titulo'][:60])
        if k not in vistos or len(r['descricao']) > len(vistos[k]['descricao']): vistos[k] = r
    registros = list(vistos.values())
    logger.info(f"Processados {len(registros)} registros")
    return registros

def filtrar_semana_atual(registros):
    hoje = datetime.now()
    inicio = (hoje - timedelta(days=hoje.weekday())).replace(hour=0,minute=0,second=0,microsecond=0)
    f = [r for r in registros if inicio <= datetime.strptime(r['data'],'%Y-%m-%d') <= hoje]
    logger.info(f"{len(f)} registros desta semana")
    return f

def gerar_json_estruturado(registros):
    hoje = datetime.now(); inicio = hoje - timedelta(days=hoje.weekday())
    por_cat = {}
    for r in registros: por_cat.setdefault(r['categoria'],[]).append(r)
    return {'metadata': {'gerado_em': hoje.isoformat(), 'periodo_inicio': inicio.strftime('%Y-%m-%d'),
        'periodo_fim': hoje.strftime('%Y-%m-%d'), 'total_registros': len(registros),
        'concluidos': sum(1 for r in registros if r['status']=='Concluído'),
        'pendentes': sum(1 for r in registros if r['status']!='Concluído'),
        'empresa': CONFIG['EMPRESA'], 'responsavel': CONFIG['RESPONSAVEL']},
        'registros': registros, 'por_categoria': {c:len(v) for c,v in por_cat.items()},
        'pendencias': [r for r in registros if r['status']!='Concluído'],
        'config': {'cores': CONFIG['CORES'], 'icones': CONFIG['ICONES']}}

# ═══════════════════════════════════════════════════════════════
# GERAÇÃO DO HTML — importa do arquivo v3
# ═══════════════════════════════════════════════════════════════
# Importa a função do arquivo gerar_html_v3.py que está na mesma pasta
import importlib.util
_spec = importlib.util.spec_from_file_location("gerar_html_v3", Path(__file__).parent / "gerar_html_v3.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

def gerar_html(dados):
    # Injeta CONFIG no módulo importado para ele ter acesso
    _mod.CONFIG = CONFIG
    return _mod.gerar_html(dados)

# ═══════════════════════════════════════════════════════════════
def salvar_no_drive(creds, dados, html):
    service = build('drive', 'v3', credentials=creds)
    hoje = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    service.files().create(body={'name': f'relatorio_dados_{hoje}.json','parents':[CONFIG['FOLDER_ID']],'mimeType':'application/json'},
        media_body=MediaInMemoryUpload(json.dumps(dados,ensure_ascii=False,indent=2).encode('utf-8'),mimetype='application/json'),fields='id').execute()
    file = service.files().create(body={'name': f'Relatorio_Semanal_{hoje}.html','parents':[CONFIG['FOLDER_ID']],'mimeType':'text/html'},
        media_body=MediaInMemoryUpload(html.encode('utf-8'),mimetype='text/html'),fields='id, webViewLink').execute()
    link = file.get('webViewLink','')
    logger.info(f"Salvos no Drive: {link}")
    return link

def enviar_email(creds, html, dados, drive_link=''):
    meta = dados['metadata']
    fmt = lambda d: datetime.strptime(d,'%Y-%m-%d').strftime('%d/%m')
    periodo = f"{fmt(meta['periodo_inicio'])} – {fmt(meta['periodo_fim'])}"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📊 Relatório Semanal {CONFIG['EMPRESA']} — {periodo} ({meta['total_registros']} entregas)"
    msg['From'] = f"{CONFIG['EMPRESA']} Automação <me>"
    msg['To'] = CONFIG['EMAIL_GESTORA']
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    build('gmail','v1',credentials=creds).users().messages().send(userId='me',body={'raw':raw}).execute()
    logger.info(f"Email enviado para: {CONFIG['EMAIL_GESTORA']}")

# ═══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--doc-id')
    args = parser.parse_args()
    logger.info("📊 RELATÓRIO SEMANAL AUTOMÁTICO — Mob2Con v2.0")
    if args.setup: autenticar_google(); logger.info("Autenticado!"); return
    if args.doc_id: CONFIG['DOCUMENT_ID'] = args.doc_id
    try:
        creds = autenticar_google()
        texto = extrair_texto_docs(CONFIG['DOCUMENT_ID'], creds)
        registros = processar_texto(texto)
        registros_semana = filtrar_semana_atual(registros)
        if not registros_semana: logger.warning("Nenhum registro esta semana"); return
        dados = gerar_json_estruturado(registros_semana)
        html = gerar_html(dados)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        (CONFIG['BACKUP_DIR'] / f'relatorio_{ts}.json').write_text(json.dumps(dados,ensure_ascii=False,indent=2),encoding='utf-8')
        (CONFIG['BACKUP_DIR'] / f'relatorio_{ts}.html').write_text(html, encoding='utf-8')
        logger.info("Backup local salvo")
        drive_link = salvar_no_drive(creds, dados, html)
        if args.test:
            logger.info(f"TESTE — Preview: backups/relatorio_{ts}.html")
        else:
            enviar_email(creds, html, dados, drive_link)
        logger.info(f"CONCLUIDO: {dados['metadata']['total_registros']} registros, {dados['metadata']['concluidos']} concluidos")
    except Exception as e:
        logger.error(f"ERRO: {e}", exc_info=True); sys.exit(1)

if __name__ == '__main__':
    main()
