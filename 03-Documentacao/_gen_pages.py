def write_pages(f):
    write_page_overview(f)
    write_page_clusters(f)
    write_page_health(f)
    write_page_churn(f)
    write_page_financeiro(f)
    write_page_turnover(f)
    write_page_fraude(f)
    write_page_modelo(f)
    write_page_medidas(f)
    write_page_alertas(f)
    f.write('</div></div></div>\n')  # close content, main, app

def write_page_overview(f):
    f.write('''<div class="content"><div id="pg-overview" class="page active">
<h2 class="section-title">Vis\u00e3o Geral CS</h2>
<div class="grid g5" id="cards-overview">
<div class="card"><div class="card-title">Total Contas Ativas</div><div class="card-value" id="v-contas">1.953</div><div class="card-sub"><span class="up"><i class="fas fa-arrow-up"></i> +3.2%</span> vs per\u00edodo anterior</div><canvas class="card-spark" id="spark-contas"></canvas></div>
<div class="card"><div class="card-title">Health Score M\u00e9dio</div><div class="card-value" id="v-health">72.4</div><div class="card-sub"><span class="up"><i class="fas fa-arrow-up"></i> +1.8</span> pontos</div><canvas class="card-spark" id="spark-health"></canvas></div>
<div class="card"><div class="card-title">Taxa Churn</div><div class="card-value" id="v-churn">4.2%</div><div class="card-sub"><span class="down"><i class="fas fa-arrow-down"></i> -0.5%</span> redu\u00e7\u00e3o</div><canvas class="card-spark" id="spark-churn"></canvas></div>
<div class="card"><div class="card-title">MRR Total</div><div class="card-value" id="v-mrr">R$ 287k</div><div class="card-sub"><span class="up"><i class="fas fa-arrow-up"></i> +R$ 12k</span> expans\u00e3o</div><canvas class="card-spark" id="spark-mrr"></canvas></div>
<div class="card"><div class="card-title">Alertas Ativos</div><div class="card-value" id="v-alerts">7</div><div class="card-sub"><span class="badge badge-danger">3 cr\u00edticos</span></div><canvas class="card-spark" id="spark-alerts"></canvas></div>
</div>
<div class="grid g2" style="margin-top:24px">
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Distribui\u00e7\u00e3o por Cluster</h3><canvas id="chart-clusters" height="200"></canvas></div>
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Health Score - Evolu\u00e7\u00e3o 30d</h3><canvas id="chart-health-trend" height="200"></canvas></div>
</div>
<div class="grid g2" style="margin-top:16px">
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">MRR Movimenta\u00e7\u00f5es (Waterfall)</h3><canvas id="chart-mrr-waterfall" height="200"></canvas></div>
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Cobertura por UF</h3><div id="heatmap-uf" style="overflow-x:auto"></div></div>
</div>
</div>
''')

def write_page_clusters(f):
    f.write('''<div id="pg-clusters" class="page">
<h2 class="section-title">Clusters CS</h2>
<div class="grid g5">
<div class="card" style="border-top:3px solid var(--info)"><div class="card-title">Tech</div><div class="card-value">952</div><div class="card-sub">Low-touch | SLA 48h</div></div>
<div class="card" style="border-top:3px solid #CD7F32"><div class="card-title">Bronze</div><div class="card-value">587</div><div class="card-sub">Low-touch | SLA 24h</div></div>
<div class="card" style="border-top:3px solid #C0C0C0"><div class="card-title">Prata</div><div class="card-value">327</div><div class="card-sub">Mid-touch | SLA 12h</div></div>
<div class="card" style="border-top:3px solid #FFD700"><div class="card-title">Ouro</div><div class="card-value">67</div><div class="card-sub">High-touch | SLA 4h</div></div>
<div class="card" style="border-top:3px solid var(--pri)"><div class="card-title">Premium</div><div class="card-value">20</div><div class="card-sub">White-glove | SLA 1h</div></div>
</div>
<h3 class="section-title">Detalhamento Clusters</h3>
<div class="tbl-wrap">
<table id="tbl-clusters">
<thead><tr><th onclick="sortTable('tbl-clusters',0)">Cluster</th><th onclick="sortTable('tbl-clusters',1)">Threshold</th><th onclick="sortTable('tbl-clusters',2)">Toque</th><th onclick="sortTable('tbl-clusters',3)">SLA (h)</th><th onclick="sortTable('tbl-clusters',4)">Target</th><th onclick="sortTable('tbl-clusters',5)">Respons\u00e1vel</th><th>Email</th></tr></thead>
<tbody>
<tr><td><span class="tag tag-info">Tech</span></td><td>7</td><td>Low-touch</td><td>48</td><td>952</td><td>Ana Claudia Batista Benides</td><td>ana.benides@mob2con.com.br</td></tr>
<tr><td><span class="tag" style="background:#FEF3C7;color:#92400E">Bronze</span></td><td>7</td><td>Low-touch</td><td>24</td><td>587</td><td>Ana Claudia Batista Benides</td><td>ana.benides@mob2con.com.br</td></tr>
<tr><td><span class="tag" style="background:#E5E7EB;color:#374151">Prata</span></td><td>5</td><td>Mid-touch</td><td>12</td><td>327</td><td>Ana Claudia Batista Benides</td><td>ana.benides@mob2con.com.br</td></tr>
<tr><td><span class="tag" style="background:#FEF3C7;color:#78350F">Ouro</span></td><td>3</td><td>High-touch</td><td>4</td><td>67</td><td>Monique Andrade</td><td>monique.andrade@mob2con.com.br</td></tr>
<tr><td><span class="tag" style="background:#FED7AA;color:#C45500">Premium</span></td><td>1</td><td>White-glove</td><td>1</td><td>20</td><td>Monique Andrade</td><td>monique.andrade@mob2con.com.br</td></tr>
</tbody></table></div>
<div class="grid g2" style="margin-top:24px">
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Contas por Cluster</h3><canvas id="chart-cluster-bar" height="180"></canvas></div>
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">SLA Cumprimento (%)</h3><canvas id="chart-sla" height="180"></canvas></div>
</div>
</div>
''')

def write_page_health(f):
    f.write('''<div id="pg-health" class="page">
<h2 class="section-title">Health Score</h2>
<div class="grid g3">
<div class="card gauge-wrap"><div class="card-title">Health Score Geral</div><canvas id="gauge-health" width="180" height="120"></canvas><div class="card-value" style="font-size:28px;margin-top:8px">72.4</div><span class="tag tag-ok">SAUD\u00c1VEL</span></div>
<div class="card"><div class="card-title">Distribui\u00e7\u00e3o por Status</div><div style="margin-top:12px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:11px">Saud\u00e1vel (\u226575)</span><span style="font-size:11px;font-weight:700">1.247 (63.8%)</span></div><div class="progress-bar"><div class="fill" style="width:63.8%;background:var(--ok)"></div></div></div><div style="margin-top:12px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:11px">Aten\u00e7\u00e3o (50-74)</span><span style="font-size:11px;font-weight:700">412 (21.1%)</span></div><div class="progress-bar"><div class="fill" style="width:21.1%;background:var(--wn)"></div></div></div><div style="margin-top:12px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:11px">Cr\u00edtico (25-49)</span><span style="font-size:11px;font-weight:700">198 (10.1%)</span></div><div class="progress-bar"><div class="fill" style="width:10.1%;background:var(--dg)"></div></div></div><div style="margin-top:12px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:11px">Churn Risk (&lt;25)</span><span style="font-size:11px;font-weight:700">96 (4.9%)</span></div><div class="progress-bar"><div class="fill" style="width:4.9%;background:#7F1D1D"></div></div></div></div>
<div class="card"><div class="card-title">F\u00f3rmula DAX</div><pre style="font-size:10px;margin-top:8px;background:var(--bg);padding:10px;border-radius:var(--r);overflow-x:auto">CS_Health_Score =
VAR pct_acesso =
  DIVIDE(
    COUNTROWS(FILTER(
      fato_status_contratantes,
      [fl_acesso] = TRUE())),
    COUNTROWS(fato_status_contratantes), 0
  ) * 100
VAR is_ativo =
  IF(SELECTEDVALUE(
    dim_contratante[ds_status_atual]) = "1",
    100, 0)
VAR is_pagante =
  IF(SELECTEDVALUE(
    fato_status_contratantes
    [fl_cliente_pagante_mobcontrol]) = TRUE(),
    100, 50)
RETURN
  (pct_acesso * 0.40)
  + (is_ativo * 0.35)
  + (is_pagante * 0.25)</pre></div>
</div>
<div class="chart-container" style="margin-top:16px"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Health Score por Cluster</h3><canvas id="chart-health-cluster" height="160"></canvas></div>
</div>
''')

def write_page_churn(f):
    f.write('''<div id="pg-churn" class="page">
<h2 class="section-title">Churn &amp; Risco</h2>
<div class="grid g4">
<div class="card"><div class="card-title">Taxa Churn</div><div class="card-value" style="color:var(--dg)">4.2%</div><div class="card-sub">82 contas perdidas</div></div>
<div class="card"><div class="card-title">Contas Churn Risk</div><div class="card-value">96</div><div class="card-sub">Health Score &lt; 25</div></div>
<div class="card"><div class="card-title">Expans\u00e3o Tier 1</div><div class="card-value" style="color:var(--ok)">143</div><div class="card-sub">Score &gt;80, Uso &gt;80%</div></div>
<div class="card"><div class="card-title">Inativos 30d+</div><div class="card-value">214</div><div class="card-sub">Sem login h\u00e1 30+ dias</div></div>
</div>
<div class="grid g2" style="margin-top:16px">
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Evolu\u00e7\u00e3o Churn (6 meses)</h3><canvas id="chart-churn-trend" height="180"></canvas></div>
<div class="chart-container"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Flag Faturamento Zerado</h3><canvas id="chart-fat-zerado" height="180"></canvas></div>
</div>
<h3 class="section-title">Tier Expans\u00e3o</h3>
<div class="tbl-wrap"><table><thead><tr><th>Tier</th><th>Crit\u00e9rio</th><th>Contas</th><th>MRR Potencial</th></tr></thead>
<tbody>
<tr><td><span class="tag tag-ok">TIER_1</span></td><td>Score &gt;80 &amp;&amp; Uso &gt;80%</td><td>143</td><td>R$ 42.900</td></tr>
<tr><td><span class="tag tag-wn">TIER_2</span></td><td>Score \u226565 &amp;&amp; Uso &gt;60%</td><td>287</td><td>R$ 57.400</td></tr>
<tr><td><span class="tag tag-info">TIER_3</span></td><td>Score \u226550 &amp;&amp; Uso &gt;40%</td><td>198</td><td>R$ 29.700</td></tr>
<tr><td><span class="tag tag-dg">NENHUM</span></td><td>Abaixo dos crit\u00e9rios</td><td>1.325</td><td>-</td></tr>
</tbody></table></div>
</div>
''')

def write_page_financeiro(f):
    f.write('''<div id="pg-financeiro" class="page">
<h2 class="section-title">Financeiro</h2>
<div class="grid g4">
<div class="card"><div class="card-title">MRR Total</div><div class="card-value">R$ 287k</div><div class="card-sub"><span class="up"><i class="fas fa-arrow-up"></i> +4.3%</span></div></div>
<div class="card"><div class="card-title">Inadimpl\u00eancia</div><div class="card-value" style="color:var(--dg)">R$ 34k</div><div class="card-sub">11.8% da base</div></div>
<div class="card"><div class="card-title">MRR em Risco</div><div class="card-value" style="color:var(--wn)">R$ 18.5k</div><div class="card-sub">Contas com Health &lt;50</div></div>
<div class="card"><div class="card-title">Expans\u00e3o Potencial</div><div class="card-value" style="color:var(--ok)">R$ 130k</div><div class="card-sub">Tiers 1+2+3</div></div>
</div>
<div class="chart-container" style="margin-top:16px"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">MRR Waterfall - Movimenta\u00e7\u00f5es do M\u00eas</h3><canvas id="chart-fin-waterfall" height="220"></canvas></div>
</div>
''')

def write_page_turnover(f):
    f.write('''<div id="pg-turnover" class="page">
<h2 class="section-title">Turnover Promotores</h2>
<div class="grid g4">
<div class="card"><div class="card-title">Admiss\u00f5es</div><div class="card-value" style="color:var(--ok)">+342</div><div class="card-sub">\u00daltimos 30 dias</div></div>
<div class="card"><div class="card-title">Desligamentos</div><div class="card-value" style="color:var(--dg)">-287</div><div class="card-sub">\u00daltimos 30 dias</div></div>
<div class="card"><div class="card-title">Saldo</div><div class="card-value">+55</div><div class="card-sub">Crescimento l\u00edquido</div></div>
<div class="card"><div class="card-title">Taxa Turnover</div><div class="card-value">14.7%</div><div class="card-sub">M\u00e9dia mensal</div></div>
</div>
<div class="chart-container" style="margin-top:16px"><h3 style="font-size:12px;font-weight:700;margin-bottom:12px">Turnover - Admiss\u00f5es vs Desligamentos (6m)</h3><canvas id="chart-turnover" height="200"></canvas></div>
</div>
''')

def write_page_fraude(f):
    f.write('''<div id="pg-fraude" class="page">
<h2 class="section-title">Score Fraude</h2>
<div class="grid g3">
<div class="card gauge-wrap"><div class="card-title">Score Fraude M\u00e9dio</div><canvas id="gauge-fraude" width="180" height="120"></canvas><div class="card-value" style="font-size:28px;margin-top:8px">23</div><span class="tag tag-ok">BAIXO RISCO</span></div>
<div class="card"><div class="card-title">Distribui\u00e7\u00e3o Risco</div><div style="margin-top:12px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:11px">Baixo (0-30)</span><span style="font-size:11px;font-weight:700">78%</span></div><div class="progress-bar"><div class="fill" style="width:78%;background:var(--ok)"></div></div></div><div style="margin-top:12px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:11px">M\u00e9dio (31-60)</span><span style="font-size:11px;font-weight:700">15%</span></div><div class="progress-bar"><div class="fill" style="width:15%;background:var(--wn)"></div></div></div><div style="margin-top:12px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:11px">Alto (61-100)</span><span style="font-size:11px;font-weight:700">7%</span></div><div class="progress-bar"><div class="fill" style="width:7%;background:var(--dg)"></div></div></div></div>
<div class="card"><div class="card-title">F\u00f3rmula DAX</div><pre style="font-size:10px;margin-top:8px;background:var(--bg);padding:10px;border-radius:var(--r);overflow-x:auto">CS_Score_Fraude =
VAR _Curtas =
  CALCULATE(COUNTROWS(fato_acesso),
    fato_acesso[qt_horas_permanencia] &lt; 0.5)
VAR _Longas =
  CALCULATE(COUNTROWS(fato_acesso),
    fato_acesso[qt_horas_permanencia] &gt; 4)
VAR _Total = COUNTROWS(fato_acesso)
RETURN
  ROUND(
    DIVIDE(_Curtas + _Longas, _Total, 0) * 100,
  0)</pre></div>
</div>
</div>
''')
