"""
Nova função gerar_html — design premium dark Mob2Con
Cole no relatorio_semanal_auto.py substituindo a função gerar_html existente
"""
import re
from datetime import datetime
from typing import Dict, List


def gerar_html(dados: Dict) -> str:
    """Gera o HTML completo do relatório — design premium dark Mob2Con"""
    meta    = dados['metadata']
    regs    = dados['registros']
    por_cat = dados['por_categoria']
    pends   = dados['pendencias']

    CORES  = dados['config']['cores']
    ICONES = dados['config']['icones']

    fmt     = lambda d: datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m')
    periodo = f"{fmt(meta['periodo_inicio'])} – {fmt(meta['periodo_fim'])}"
    total   = meta['total_registros']
    pct_ok  = int(meta['concluidos'] / total * 100) if total else 0

    # ── KPI CARDS ──────────────────────────────────────────────
    kpi_cards = ''
    for icone, label, valor, cor in [
        ('📊', 'Total',      total,               '#F46901'),
        ('✅', 'Concluídos', meta['concluidos'],  '#107C41'),
        ('⏳', 'Pendentes',  meta['pendentes'],   '#F2B100'),
        ('📂', 'Categorias', len(por_cat),        '#4285F4'),
    ]:
        kpi_cards += f'''
        <div class="kpi-card" style="border-top:3px solid {cor}">
          <div style="font-size:24px;margin-bottom:6px">{icone}</div>
          <div style="font-size:30px;font-weight:900;color:{cor};line-height:1">{valor}</div>
          <div style="font-size:10px;color:#666;font-weight:700;text-transform:uppercase;margin-top:4px">{label}</div>
        </div>'''

    # ── BARRA DE PROGRESSO ─────────────────────────────────────
    progress = f'''
    <div class="card" style="margin-bottom:20px">
      <div style="display:flex;justify-content:space-between;margin-bottom:8px">
        <span style="font-size:12px;color:#aaa;font-weight:600">Progresso da semana</span>
        <span style="font-size:13px;font-weight:800;color:#F46901">{pct_ok}% concluído</span>
      </div>
      <div style="background:#2a2a3a;border-radius:100px;height:10px;overflow:hidden">
        <div style="width:{pct_ok}%;height:100%;background:linear-gradient(90deg,#F46901,#F2C811);border-radius:100px"></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:10px;color:#555">
        <span>{meta['concluidos']} concluídos</span>
        <span>{meta['pendentes']} pendentes</span>
      </div>
    </div>'''

    # ── CATEGORIAS ─────────────────────────────────────────────
    cat_cards = ''
    for cat, count in por_cat.items():
        cor   = CORES.get(cat, '#605E5C')
        icone = ICONES.get(cat, '📋')
        pct   = int(count / total * 100) if total else 0
        cat_cards += f'''
        <div class="cat-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <span style="font-size:12px;font-weight:700;color:#ccc">{icone} {cat}</span>
            <span style="font-size:20px;font-weight:900;color:{cor}">{count}</span>
          </div>
          <div style="background:#2a2a3a;border-radius:100px;height:4px">
            <div style="width:{pct}%;height:100%;background:{cor};border-radius:100px"></div>
          </div>
          <div style="font-size:10px;color:#555;margin-top:4px">{pct}% do total</div>
        </div>'''

    # ── TIMELINE ───────────────────────────────────────────────
    timeline = ''
    por_cat_regs: Dict[str, List] = {}
    for r in regs:
        por_cat_regs.setdefault(r['categoria'], []).append(r)

    for cat, items in por_cat_regs.items():
        cor   = CORES.get(cat, '#605E5C')
        icone = ICONES.get(cat, '📋')
        for item in items:
            tags_html = ''.join(
                f'<span style="font-size:10px;padding:2px 8px;border-radius:100px;'
                f'border:1px solid {cor}44;color:{cor};font-weight:600">{t}</span>'
                for t in (item.get('tags') or [])
            )
            ok      = item['status'] == 'Concluído'
            s_bg    = 'rgba(16,124,65,.15)'  if ok else 'rgba(242,177,0,.12)'
            s_cor   = '#4ade80'              if ok else '#F2B100'
            s_label = '✅ Concluído'         if ok else '⏳ Pendente'
            titulo  = re.sub(r'^[\w\s/]+:\s*', '', item['titulo'], count=1)
            desc    = item['descricao']

            timeline += f'''
        <div class="tl-item">
          <div class="tl-dot" style="background:{cor};box-shadow:0 0 10px {cor}66">{icone}</div>
          <div class="tl-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px;margin-bottom:8px">
              <span style="font-size:10px;font-weight:700;padding:3px 10px;border-radius:100px;
                           background:{cor}22;color:{cor};border:1px solid {cor}44">
                {fmt(item["data"])} · {cat}
              </span>
              <span style="font-size:10px;padding:3px 10px;border-radius:100px;
                           background:{s_bg};color:{s_cor};font-weight:700">{s_label}</span>
            </div>
            <h3 style="font-size:14px;font-weight:800;color:#fff;margin:0 0 6px;line-height:1.4">{titulo}</h3>
            <p style="font-size:12px;color:#888;line-height:1.7;margin:0">{desc}</p>
            {f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:10px">{tags_html}</div>' if tags_html else ''}
          </div>
        </div>'''

    # ── PENDÊNCIAS ─────────────────────────────────────────────
    pend_html = ''
    if pends:
        itens_p = ''
        for p in pends:
            cor    = CORES.get(p['categoria'], '#605E5C')
            titulo = re.sub(r'^[\w\s/]+:\s*', '', p['titulo'], count=1)
            itens_p += f'''
          <div style="display:flex;align-items:center;gap:10px;padding:10px 0;
                      border-bottom:1px solid rgba(242,177,0,.1);font-size:12px">
            <span style="background:{cor};color:#fff;padding:3px 10px;
                         border-radius:100px;font-size:10px;font-weight:700;white-space:nowrap">
              {p["categoria"]}
            </span>
            <span style="color:#ccc"><strong style="color:#fff">{titulo}</strong></span>
          </div>'''
        pend_html = f'''
      <div class="card" style="border:1px solid rgba(242,177,0,.3);background:rgba(242,177,0,.06);margin-bottom:20px">
        <h4 style="font-size:12px;font-weight:700;color:#F2B100;margin:0 0 12px;text-transform:uppercase;letter-spacing:1px">
          ⚠️ Pendências / Em Andamento ({len(pends)})
        </h4>
        {itens_p}
      </div>'''

    # ── HTML FINAL ─────────────────────────────────────────────
    EMPRESA    = meta['empresa']
    RESPONSAVEL = meta['responsavel']
    GESTORA    = 'Mariliana Fagotti'
    agora      = datetime.now().strftime('%d/%m/%Y %H:%M')

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Relatório Semanal — {EMPRESA} {periodo}</title>
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{
      font-family:'Raleway',sans-serif;
      background:#0d0d1a;
      color:#e2e2f0;
      min-height:100vh;
      padding:24px 16px;
    }}
    .wrap{{max-width:780px;margin:0 auto}}

    /* HEADER */
    .header{{
      background:linear-gradient(135deg,#F46901 0%,#c45200 45%,#1a1030 100%);
      border-radius:20px;padding:32px 36px;margin-bottom:24px;
      position:relative;overflow:hidden;
      box-shadow:0 8px 40px rgba(244,105,1,.35);
    }}
    .header::after{{
      content:'';position:absolute;top:-60px;right:-60px;
      width:240px;height:240px;
      background:rgba(255,255,255,.06);border-radius:50%;
    }}
    .header::before{{
      content:'';position:absolute;bottom:-40px;left:30%;
      width:160px;height:160px;
      background:rgba(255,255,255,.04);border-radius:50%;
    }}

    /* CARDS */
    .card{{
      background:#13131f;border:1px solid #1e1e30;
      border-radius:16px;padding:18px 20px;
    }}
    .kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}}
    .kpi-card{{
      background:#13131f;border:1px solid #1e1e30;border-radius:14px;
      padding:18px 14px;text-align:center;
      transition:transform .2s,box-shadow .2s;
    }}
    .kpi-card:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,.4)}}

    /* CATEGORIAS */
    .cat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-bottom:20px}}
    .cat-card{{background:#13131f;border:1px solid #1e1e30;border-radius:12px;padding:14px}}

    /* SECTION LABEL */
    .sec-label{{
      font-size:10px;font-weight:700;color:#444;
      text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;
    }}

    /* TIMELINE */
    .timeline{{position:relative;padding-left:38px}}
    .timeline::before{{
      content:'';position:absolute;left:11px;top:4px;bottom:4px;
      width:2px;background:linear-gradient(180deg,#F46901,#4285F4 60%,transparent);
    }}
    .tl-item{{position:relative;margin-bottom:14px}}
    .tl-dot{{
      position:absolute;left:-31px;top:14px;
      width:24px;height:24px;border-radius:50%;
      display:flex;align-items:center;justify-content:center;font-size:11px;
    }}
    .tl-card{{
      background:#13131f;border:1px solid #1e1e30;border-radius:14px;
      padding:16px 18px;transition:border-color .2s,box-shadow .2s;
    }}
    .tl-card:hover{{border-color:#F46901;box-shadow:0 4px 20px rgba(244,105,1,.12)}}

    /* FOOTER */
    .footer{{text-align:center;font-size:11px;color:#333;padding:20px 0;border-top:1px solid #13131f}}

    @media(max-width:520px){{
      .kpi-grid{{grid-template-columns:repeat(2,1fr)}}
      .header{{padding:24px 20px}}
    }}
  </style>
</head>
<body>
<div class="wrap">

  <!-- HEADER -->
  <div class="header">
    <div style="display:flex;align-items:center;gap:16px;position:relative;z-index:1">
      <span style="font-size:40px">📊</span>
      <div>
        <div style="font-size:22px;font-weight:900;color:#fff">{EMPRESA} — Relatório Semanal</div>
        <div style="font-size:13px;color:rgba(255,255,255,.75);margin-top:4px">
          Período: {periodo} &nbsp;·&nbsp; {total} entregas registradas
        </div>
      </div>
    </div>
    <div style="font-size:11px;color:rgba(255,255,255,.45);margin-top:14px;position:relative;z-index:1">
      Responsável: <strong style="color:rgba(255,255,255,.7)">{RESPONSAVEL}</strong>
      &nbsp;→&nbsp; {GESTORA}
    </div>
    <div style="margin-top:14px;position:relative;z-index:1">
      <span style="background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.2);
                   border-radius:100px;padding:5px 16px;font-size:12px;font-weight:700;color:#fff">
        🗓 Semana {periodo}
      </span>
      <span style="background:rgba(16,124,65,.3);border:1px solid rgba(16,124,65,.4);
                   border-radius:100px;padding:5px 16px;font-size:12px;font-weight:700;
                   color:#4ade80;margin-left:8px">
        {pct_ok}% concluído
      </span>
    </div>
  </div>

  <!-- KPIs -->
  <div class="kpi-grid">{kpi_cards}</div>

  <!-- PROGRESSO -->
  {progress}

  <!-- CATEGORIAS -->
  <div class="sec-label">📂 Distribuição por Categoria</div>
  <div class="cat-grid">{cat_cards}</div>

  <!-- TIMELINE -->
  <div class="sec-label">📅 Timeline de Entregas</div>
  <div class="timeline" style="margin-bottom:24px">{timeline}</div>

  <!-- PENDÊNCIAS -->
  {pend_html}

  <!-- FOOTER -->
  <div class="footer">
    Gerado automaticamente por Python · {EMPRESA} · {agora}
  </div>

</div>
</body>
</html>'''
