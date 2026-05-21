"""
enriquecer_base_lite.py — Enriquece a planilha Cadastro Lite com dados do PBI
Confrontado com: Indicadores de Performance - Cadastro Lite.pbip
Fonte: Base bruta Redshift (1o5_pT2aPNO2Cjv0orMjIfINbrerw_IqGl1az944IwrM)
Destino: Planilha Cadastro Lite (17wacDgqjMwO3lOknuk6TtKfTwamB1qz-MpGGuwM7n_4)

Novas abas criadas:
- Breakdown_RequestType: requisicoes por tipo (Cadastro/Alocacao/Sem efeito)
- Status_Promotores: promotores ativos vs descartados por empresa
- Funil_Global: totais para o mini-funil no HTML

Autor: Kiro AI | Data: 19/05/2026
"""
import gspread
from google.oauth2.service_account import Credentials
from collections import defaultdict
from datetime import datetime
import os

BASE_BRUTA_ID = '1o5_pT2aPNO2Cjv0orMjIfINbrerw_IqGl1az944IwrM'
DESTINO_ID = '17wacDgqjMwO3lOknuk6TtKfTwamB1qz-MpGGuwM7n_4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_client():
    """Conecta ao Google Sheets via service account."""
    cred_path = os.path.join(os.path.expanduser('~'),
                             '.aws', 'amazonq', 'universal-control',
                             'credentials', 'google-service-account.json')
    if not os.path.exists(cred_path):
        # Fallback
        cred_path = os.path.join(os.path.dirname(__file__), '..', '..',
                                 'credentials.json')
    creds = Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    return gspread.authorize(creds)


def ler_base_bruta(gc):
    """Le a base bruta do Redshift (dados granulares)."""
    print('Lendo base bruta...')
    sh = gc.open_by_key(BASE_BRUTA_ID)
    ws = sh.sheet1
    data = ws.get_all_records()
    print(f'   {len(data)} registros lidos')
    return data


def classificar_request_type(row):
    """
    Classifica o tipo de requisicao.
    PBI equivalente: request_type (Cadastro Promotor/Alocacao/Sem efeito)
    """
    status = str(row.get('status_cadastro', '')).lower()
    qtd = int(row.get('qtd_tentativas_cadastro', 0) or 0)
    if status in ('expired', 'rejected', 'pending', ''):
        return 'Sem efeito'
    elif qtd > 1:
        return 'Alocacao'
    else:
        return 'Cadastro Promotor'


def classificar_status_final(row):
    """
    PBI equivalente: Status_Final (Promotor Ativo/Descartado)
    """
    status = str(row.get('status_promotor', ''))
    if 'Descartado' in status:
        return 'Promotor Descartado'
    elif 'Ativo' in status:
        return 'Promotor Ativo'
    elif 'Inativo' in status:
        return 'Promotor Inativo'
    return 'Sem Efeito'


def agregar_por_empresa(data):
    """Agrega dados por empresa com breakdown."""
    empresas = defaultdict(lambda: {
        'total': 0, 'cpfs': set(),
        'cadastro': 0, 'alocacao': 0, 'sem_efeito': 0,
        'ativo': 0, 'descartado': 0, 'inativo': 0,
        'tipo': '', 'status': ''
    })
    for row in data:
        emp = str(row.get('empresa_responsavel_cadastro', '')
                  or row.get('empresa', ''))
        if not emp:
            continue
        e = empresas[emp]
        e['total'] += 1
        cpf = str(row.get('cpf', ''))
        if cpf:
            e['cpfs'].add(cpf)
        rt = classificar_request_type(row)
        if rt == 'Cadastro Promotor':
            e['cadastro'] += 1
        elif rt == 'Alocacao':
            e['alocacao'] += 1
        else:
            e['sem_efeito'] += 1
        sf = classificar_status_final(row)
        if sf == 'Promotor Ativo':
            e['ativo'] += 1
        elif sf == 'Promotor Descartado':
            e['descartado'] += 1
        elif sf == 'Promotor Inativo':
            e['inativo'] += 1
        if not e['tipo']:
            t = str(row.get('empresa', ''))
            e['tipo'] = 'Agencia' if 'Ag' in t else 'Fornecedor'
        if not e['status']:
            tb = str(row.get('tipo_base', ''))
            e['status'] = ('Cliente' if ('Cliente' in tb and
                           'Nao' not in tb and 'Não' not in tb)
                           else 'Nao Cliente')
    return empresas


def calcular_funil_global(data):
    """Calcula totais globais para o funil (equivalente ao PBI)."""
    total = len(data)
    cpfs = set()
    cadastro = alocacao = sem_efeito = ativos = descartados = 0
    for row in data:
        cpf = str(row.get('cpf', ''))
        if cpf:
            cpfs.add(cpf)
        rt = classificar_request_type(row)
        if rt == 'Cadastro Promotor':
            cadastro += 1
        elif rt == 'Alocacao':
            alocacao += 1
        else:
            sem_efeito += 1
        sf = classificar_status_final(row)
        if sf == 'Promotor Ativo':
            ativos += 1
        elif sf == 'Promotor Descartado':
            descartados += 1
    pct = lambda v: round(v / total * 100, 1) if total else 0
    return {
        'total': total, 'cpfs': len(cpfs),
        'cadastro': cadastro, 'alocacao': alocacao, 'sem_efeito': sem_efeito,
        'pct_cadastro': pct(cadastro), 'pct_alocacao': pct(alocacao),
        'pct_sem_efeito': pct(sem_efeito),
        'ativos': ativos, 'descartados': descartados,
        'pct_ativos': pct(ativos)
    }


def escrever_abas(gc, empresas_agg, funil):
    """Escreve novas abas na planilha destino."""
    print('Escrevendo abas...')
    sh = gc.open_by_key(DESTINO_ID)

    # Aba: Breakdown_RequestType
    try:
        ws = sh.worksheet('Breakdown_RequestType')
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet('Breakdown_RequestType', rows=1000, cols=10)
    hdr = ['empresa', 'tipo', 'status_empresa', 'total_requisicoes',
           'cpfs_unicos', 'cadastro_promotor', 'alocacao', 'sem_efeito',
           'pct_cadastro', 'pct_sem_efeito']
    rows = [hdr]
    for emp, d in sorted(empresas_agg.items(),
                         key=lambda x: x[1]['total'], reverse=True):
        t = d['total']
        rows.append([emp, d['tipo'], d['status'], t, len(d['cpfs']),
                     d['cadastro'], d['alocacao'], d['sem_efeito'],
                     round(d['cadastro']/t*100, 1) if t else 0,
                     round(d['sem_efeito']/t*100, 1) if t else 0])
    ws.update(range_name='A1', values=rows)
    print(f'   Breakdown_RequestType: {len(rows)-1} empresas')

    # Aba: Status_Promotores
    try:
        ws2 = sh.worksheet('Status_Promotores')
        ws2.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws2 = sh.add_worksheet('Status_Promotores', rows=1000, cols=8)
    hdr2 = ['empresa', 'tipo', 'status_empresa', 'promotor_ativo',
             'promotor_descartado', 'promotor_inativo', 'total', 'pct_ativo']
    rows2 = [hdr2]
    for emp, d in sorted(empresas_agg.items(),
                         key=lambda x: x[1]['descartado'], reverse=True):
        tp = d['ativo'] + d['descartado'] + d['inativo']
        if tp == 0:
            continue
        rows2.append([emp, d['tipo'], d['status'], d['ativo'],
                      d['descartado'], d['inativo'], tp,
                      round(d['ativo']/tp*100, 1) if tp else 0])
    ws2.update(range_name='A1', values=rows2)
    print(f'   Status_Promotores: {len(rows2)-1} empresas')

    # Aba: Funil_Global
    try:
        ws3 = sh.worksheet('Funil_Global')
        ws3.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws3 = sh.add_worksheet('Funil_Global', rows=20, cols=3)
    f = funil
    funil_rows = [
        ['metrica', 'valor', 'percentual'],
        ['Total Requisicoes', f['total'], '100%'],
        ['CPFs Unicos', f['cpfs'], ''],
        ['Cadastro Promotor', f['cadastro'], str(f['pct_cadastro']) + '%'],
        ['Alocacao', f['alocacao'], str(f['pct_alocacao']) + '%'],
        ['Sem Efeito', f['sem_efeito'], str(f['pct_sem_efeito']) + '%'],
        ['', '', ''],
        ['Promotores Ativos', f['ativos'], str(f['pct_ativos']) + '%'],
        ['Promotores Descartados', f['descartados'], ''],
        ['', '', ''],
        ['Atualizado em', datetime.now().strftime('%Y-%m-%d %H:%M'), ''],
        ['Fonte', 'Redshift mc2-production (base bruta)', ''],
        ['PBI ref', 'Indicadores de Performance - Cadastro Lite.pbip', ''],
    ]
    ws3.update(range_name='A1', values=funil_rows)
    print('   Funil_Global: escrito')


def main():
    """Execucao principal."""
    print('=' * 60)
    print('Enriquecendo base Cadastro Lite')
    print('=' * 60)
    gc = get_client()
    data = ler_base_bruta(gc)
    if not data:
        print('Base bruta vazia. Abortando.')
        return
    print('Agregando por empresa...')
    empresas_agg = agregar_por_empresa(data)
    print(f'   {len(empresas_agg)} empresas')
    print('Calculando funil global...')
    funil = calcular_funil_global(data)
    print(f'   Total: {funil["total"]} req | {funil["cpfs"]} CPFs')
    print(f'   Cadastro: {funil["pct_cadastro"]}%')
    print(f'   Alocacao: {funil["pct_alocacao"]}%')
    print(f'   Sem efeito: {funil["pct_sem_efeito"]}%')
    escrever_abas(gc, empresas_agg, funil)
    print('=' * 60)
    print('Concluido! Novas abas criadas.')
    print('=' * 60)


if __name__ == '__main__':
    main()
