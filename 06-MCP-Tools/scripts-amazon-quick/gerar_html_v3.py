import re
from datetime import datetime
from typing import Dict, List


def gerar_html(dados: dict) -> str:
    meta    = dados['metadata']
    regs    = dados['registros']
    por_cat = dados['por_categoria']
    pends   = dados['pendencias']
    CORES   = CONFIG['CORES']
    ICONES  = CONFIG['ICONES']

    fmt     = lambda d: datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m')
    periodo = f"{fmt(meta['periodo_inicio'])} \u2013 {fmt(meta['periodo_fim'])}"
    total   = meta['total_registros']
    pct_ok  = int(meta['concluidos'] / total * 100) if total else 0

    # ── FLUXO DE PROCESSO (setas) ──────────────────────────────
    todos = sorted(regs, key=lambda r: r['data'])
    nos_flow = ''
    for idx, item in enumerate(todos):
        cat   = item['categoria']
        cor   = CORES.get(cat, '#605E5C')
        icone = ICONES.get(cat, '\U0001f4cb')
        titulo_curto = re.sub(r'^[\w\s/]+:\s*', '', item['titulo'], count=1)[:38]
        dia   = fmt(item['data'])
        nos_flow += f'''
        <div class="flow-node">
          <div class="flow-box" style="background:{cor}" title="{item['descricao'][:120]}">
            <span style="font-size:16px">{icone}</span><br>{titulo_curto}
          </div>
          <div class="flow-label">{dia} \u00b7 {cat}</div>
        </div>'''
        if idx < len(todos) - 1:
            nos_flow += '<div class="flow-arrow">\u2192</div>'

    # ── KPI CARDS ──────────────────────────────────────────────
    kpi_html = ''
    for icone, label, valor, cor in [
        ('\U0001f4ca', 'Total',      total,               '#F46901'),
        ('\u2705', 'Conclu\u00eddos', meta['concluidos'],  '#107C41'),
        ('\u23f3', 'Pendentes',  meta['pendentes'],   '#F2B100'),
        ('\U0001f4c2', 'Categorias', len(por_cat),        '#4285F4'),
    ]:
        kpi_html += f'''
        <div class="kpi-card" style="border-top:3px solid {cor}">
          <div style="font-size:22px;margin-bottom:6px">{icone}</div>
          <div style="font-size:28px;font-weight:900;color:{cor};line-height:1">{valor}</div>
          <div style="font-size:10px;color:var(--mob-text-muted);font-weight:700;text-transform:uppercase;margin-top:4px">{label}</div>
        </div>'''

    # ── BARRA DE PROGRESSO ─────────────────────────────────────
    progress = f'''
    <div style="background:var(--mob-surface);border:1px solid var(--mob-border);border-radius:12px;padding:16px 20px;margin-bottom:20px">
      <div style="display:flex;justify-content:space-between;margin-bottom:8px">
        <span style="font-size:12px;color:var(--mob-text-muted);font-weight:600">Progresso da semana</span>
        <span style="font-size:13px;font-weight:800;color:#F46901">{pct_ok}% conclu\u00eddo</span>
      </div>
      <div style="background:#E2E8F0;border-radius:100px;height:8px;overflow:hidden">
        <div style="width:{pct_ok}%;height:100%;background:linear-gradient(90deg,#F46901,#F2C811);border-radius:100px"></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:10px;color:#aaa">
        <span>{meta['concluidos']} conclu\u00eddos</span>
        <span>{meta['pendentes']} pendentes</span>
      </div>
    </div>'''

    # ── TIMELINE ───────────────────────────────────────────────
    timeline_items = ''
    for idx, item in enumerate(todos):
        cat   = item['categoria']
        cor   = CORES.get(cat, '#605E5C')
        icone = ICONES.get(cat, '\U0001f4cb')
        ok    = item['status'] == 'Conclu\u00eddo'
        s_bg  = '#D1FAE5' if ok else '#FEF3C7'
        s_txt = '#065F46' if ok else '#92400E'
        titulo = re.sub(r'^[\w\s/]+:\s*', '', item['titulo'], count=1)

        tags_html = ''.join(
            f'<span class="tag" style="color:{cor};border-color:{cor}">{t}</span>'
            for t in (item.get('tags') or [])
        )

        # Tooltip: linhas da descricao
        linhas = [l.strip() for l in item['descricao'].split('  ') if l.strip()]
        tooltip_linhas = ''.join(
            f'<div style="padding:3px 0;border-bottom:1px solid #E2E8F0;font-size:11px;color:var(--mob-text-muted)">{l}</div>'
            for l in linhas[1:4]
        ) or f'<div style="font-size:11px;color:var(--mob-text-muted)">{item["descricao"][:150]}</div>'

        timeline_items += f'''
      <div class="timeline-item">
        <div class="timeline-dot" style="background:{cor}">{icone}</div>
        <div class="timeline-card">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">
            <span class="date" style="background:{cor}18;color:{cor}">{fmt(item["data"])} \u00b7 {cat}</span>
            <span style="font-size:10px;padding:2px 10px;border-radius:100px;background:{s_bg};color:{s_txt};font-weight:700">
              {"\u2705 Conclu\u00eddo" if ok else "\u23f3 Pendente"}
            </span>
          </div>
          <h3 style="margin-top:8px">{titulo}</h3>
          <p>{item["descricao"]}</p>
          {f'<div class="tags" style="margin-top:8px">{tags_html}</div>' if tags_html else ''}
          <div class="tooltip-detail">
            <div style="font-size:11px;font-weight:700;color:{cor};margin-bottom:6px">\U0001f4a1 Detalhes do processo</div>
            {tooltip_linhas}
          </div>
        </div>
      </div>'''

        # Seta de conexao entre itens
        if idx < len(todos) - 1:
            prox = todos[idx + 1]
            prox_cor = CORES.get(prox['categoria'], '#605E5C')
            prox_titulo = re.sub(r'^[\w\s/]+:\s*', '', prox['titulo'], count=1)[:45]
            timeline_items += f'''
      <div style="display:flex;align-items:center;gap:10px;padding:4px 0 4px 54px;font-size:11px;color:#aaa">
        <div style="width:3px;height:20px;background:linear-gradient({cor},{prox_cor});border-radius:2px;margin-left:-34px;flex-shrink:0"></div>
        <span>levou a \u2192</span>
        <span style="color:{prox_cor};font-weight:600">{prox_titulo}...</span>
      </div>'''

    # ── PENDENCIAS ─────────────────────────────────────────────
    pend_html = ''
    if pends:
        itens_p = ''
        for p in pends:
            cor = CORES.get(p['categoria'], '#605E5C')
            titulo_p = re.sub(r'^[\w\s/]+:\s*', '', p['titulo'], count=1)
            itens_p += f'''
          <div class="pending-item">
            <span class="person-badge" style="background:{cor}">{p["categoria"]}</span>
            <span><strong>{titulo_p}</strong></span>
          </div>'''
        pend_html = f'''
    <div class="pending-box" style="margin-bottom:24px">
      <h4>\u26a0\ufe0f Pend\u00eancias / Em Andamento ({len(pends)})</h4>
      {itens_p}
    </div>'''

    EMPRESA     = CONFIG['EMPRESA']
    RESPONSAVEL = CONFIG['RESPONSAVEL']
    GESTORA     = CONFIG['NOME_GESTORA']
    agora       = datetime.now().strftime('%d/%m/%Y %H:%M')

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Relat\u00f3rio Semanal \u2014 {EMPRESA} {periodo}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root{{--mob-laranja:#F46901;--mob-grafite:#434343;--mob-preto:#111111;
           --mob-roxo:#6F05D4;--mob-azul:#4285F4;--mob-verde:#107C41;
           --mob-bg:#F3F6FA;--mob-surface:#ffffff;--mob-border:#E2E8F0;
           --mob-text:#323130;--mob-text-muted:#605E5C}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:'Raleway',sans-serif;background:var(--mob-bg);color:var(--mob-text);padding:24px;min-height:100vh}}
    .wrap{{max-width:860px;margin:0 auto}}
    .header{{background:linear-gradient(135deg,var(--mob-preto) 0%,#2d2d2d 100%);border-radius:16px;
             padding:28px 32px;margin-bottom:24px;display:flex;justify-content:space-between;
             align-items:center;border-left:6px solid var(--mob-laranja);opacity:0}}
    .header h1{{color:#fff;font-size:22px;font-weight:800}}
    .header h1 span{{color:var(--mob-laranja)}}
    .header p{{color:#aaa;font-size:13px;margin-top:4px}}
    .header-badge{{background:var(--mob-laranja);color:#fff;padding:8px 20px;border-radius:100px;
                   font-size:13px;font-weight:700;display:flex;align-items:center;gap:8px;white-space:nowrap}}
    .sec{{font-size:13px;font-weight:700;color:var(--mob-text-muted);text-transform:uppercase;
          letter-spacing:.1em;margin-bottom:16px;display:flex;align-items:center;gap:8px;opacity:0}}
    .sec::after{{content:'';flex:1;height:1px;background:var(--mob-border)}}
    .kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;opacity:0}}
    .kpi-card{{background:var(--mob-surface);border:1px solid var(--mob-border);border-radius:12px;
               padding:16px;text-align:center;transition:transform .2s,box-shadow .2s}}
    .kpi-card:hover{{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.08)}}
    .flow-wrap{{background:var(--mob-surface);border:1px solid var(--mob-border);border-radius:16px;
                padding:24px;margin-bottom:24px;opacity:0}}
    .flow{{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:0;row-gap:12px}}
    .flow-node{{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:100px}}
    .flow-box{{padding:10px 14px;border-radius:10px;font-size:11px;font-weight:700;text-align:center;
               color:#fff;line-height:1.4;min-width:90px;cursor:default;
               transition:transform .2s,box-shadow .2s}}
    .flow-box:hover{{transform:scale(1.08);box-shadow:0 6px 20px rgba(0,0,0,.2)}}
    .flow-label{{font-size:10px;color:var(--mob-text-muted);font-weight:600;text-align:center}}
    .flow-arrow{{font-size:22px;color:#ccc;padding:0 4px;margin-top:-18px}}
    .timeline{{position:relative;margin-bottom:24px;opacity:0}}
    .timeline-track{{position:absolute;left:20px;top:0;bottom:0;width:3px;
                     background:linear-gradient(to bottom,#F46901,#6F05D4,#4285F4);border-radius:4px}}
    .timeline-item{{display:flex;gap:20px;margin-bottom:12px;padding-left:54px;position:relative}}
    .timeline-dot{{position:absolute;left:11px;top:12px;width:20px;height:20px;border-radius:50%;
                   border:3px solid var(--mob-surface);display:flex;align-items:center;
                   justify-content:center;font-size:9px;color:#fff;font-weight:800}}
    .timeline-card{{flex:1;background:var(--mob-surface);border:1px solid var(--mob-border);
                    border-radius:12px;padding:14px 18px;transition:box-shadow .2s,transform .2s;cursor:default}}
    .timeline-card:hover{{box-shadow:0 4px 20px rgba(0,0,0,.1);transform:translateX(4px)}}
    .date{{font-size:11px;font-weight:700;padding:2px 8px;border-radius:100px;display:inline-block;margin-bottom:6px}}
    .timeline-card h3{{font-size:14px;font-weight:700;margin-bottom:4px}}
    .timeline-card p{{font-size:12px;color:var(--mob-text-muted);line-height:1.6}}
    .tags{{display:flex;flex-wrap:wrap;gap:6px}}
    .tag{{font-size:11px;padding:2px 8px;border-radius:100px;font-weight:600;border:1px solid}}
    .tooltip-detail{{display:none;margin-top:12px;padding:12px 14px;
                     background:#F8F9FA;border:1px solid var(--mob-border);border-radius:10px}}
    .timeline-card:hover .tooltip-detail{{display:block}}
    .pending-box{{background:#FFF9F0;border:1px solid #F2C811;border-radius:12px;padding:16px 20px}}
    .pending-box h4{{font-size:13px;font-weight:700;color:#856404;margin-bottom:10px;display:flex;align-items:center;gap:8px}}
    .pending-item{{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #fde68a;font-size:12px}}
    .pending-item:last-child{{border-bottom:none}}
    .person-badge{{padding:3px 10px;border-radius:100px;font-size:11px;font-weight:700;color:#fff;white-space:nowrap}}
    .footer{{text-align:center;padding:20px;color:var(--mob-text-muted);font-size:12px;
             border-top:1px solid var(--mob-border);margin-top:8px;opacity:0}}
    .footer span{{color:var(--mob-laranja);font-weight:700}}
    @media(max-width:600px){{
      .kpi-grid{{grid-template-columns:repeat(2,1fr)}}
      .header{{flex-direction:column;gap:16px;align-items:flex-start}}
    }}
  </style>
</head>
<body>
<div class="wrap">

  <div class="header" id="el-header">
    <div>
      <h1>Relat\u00f3rio Semanal <span>{EMPRESA}</span></h1>
      <p>Per\u00edodo: {periodo} &nbsp;|&nbsp; Respons\u00e1vel: {RESPONSAVEL} &nbsp;|&nbsp; <span style="color:var(--mob-laranja)">{EMPRESA}</span></p>
    </div>
    <div class="header-badge"><i class="fa-solid fa-check-double"></i> {pct_ok}% Conclu\u00eddo</div>
  </div>

  <p class="sec" id="el-s1"><i class="fa-solid fa-chart-bar"></i> Resumo da Semana</p>
  <div class="kpi-grid" id="el-kpi">{kpi_html}</div>
  {progress}

  <p class="sec" id="el-s2"><i class="fa-solid fa-diagram-project"></i> Fluxo de Entregas \u2014 {periodo}</p>
  <div class="flow-wrap" id="el-flow">
    <div style="font-size:14px;font-weight:800;margin-bottom:20px;display:flex;align-items:center;gap:10px">
      <i class="fa-solid fa-sitemap" style="color:var(--mob-laranja)"></i>
      Sequ\u00eancia de trabalho desta semana
    </div>
    <div class="flow">{nos_flow}</div>
  </div>

  <p class="sec" id="el-s3"><i class="fa-solid fa-timeline"></i> Timeline Detalhada</p>
  <div class="timeline" id="el-timeline">
    <div class="timeline-track"></div>
    {timeline_items}
  </div>

  {pend_html}

  <div class="footer" id="el-footer">
    Gerado automaticamente por Python &nbsp;\u00b7&nbsp; <span>{EMPRESA}</span> &nbsp;\u00b7&nbsp; {agora}
    &nbsp;\u00b7&nbsp; Destinat\u00e1rio: {GESTORA}
  </div>

</div>
<script>
  const els = ['el-header','el-s1','el-kpi','el-s2','el-flow','el-s3','el-timeline','el-footer'];
  els.forEach((id,i) => {{
    const el = document.getElementById(id);
    if(el){{
      el.style.transform = 'translateY(16px)';
      setTimeout(() => {{
        el.style.transition = 'opacity .5s ease, transform .5s ease';
        el.style.transform = 'translateY(0)';
        el.style.opacity = '1';
      }}, i * 130);
    }}
  }});
</script>
</body>
</html>'''
