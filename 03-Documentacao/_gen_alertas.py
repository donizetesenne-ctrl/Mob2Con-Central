def write_page_alertas(f):
    f.write('''<div id="pg-alertas" class="page">
<h2 class="section-title">Central de Alertas</h2>
<div class="grid g3" style="margin-bottom:16px">
<div class="card"><div class="card-title">Alertas Ativos</div><div class="card-value" style="color:var(--dg)">7</div></div>
<div class="card"><div class="card-title">Cr\u00edticos</div><div class="card-value" style="color:var(--dg)">3</div></div>
<div class="card"><div class="card-title">Resolvidos (7d)</div><div class="card-value" style="color:var(--ok)">12</div></div>
</div>
<div id="alerts-list">
<div class="alert-item" style="border-left:3px solid var(--dg)"><span class="dismiss" onclick="this.parentElement.remove();updateAlertCount()">&times;</span><strong style="color:var(--dg)">CR\u00cdTICO</strong> - 96 contas com Health Score &lt; 25 (Churn Risk)<br><small style="color:var(--tx2)">Detectado h\u00e1 2h | Cluster: Bronze, Tech</small></div>
<div class="alert-item" style="border-left:3px solid var(--dg)"><span class="dismiss" onclick="this.parentElement.remove();updateAlertCount()">&times;</span><strong style="color:var(--dg)">CR\u00cdTICO</strong> - MRR em risco: R$ 18.5k em contas com score &lt; 50<br><small style="color:var(--tx2)">Detectado h\u00e1 4h | Financeiro</small></div>
<div class="alert-item" style="border-left:3px solid var(--dg)"><span class="dismiss" onclick="this.parentElement.remove();updateAlertCount()">&times;</span><strong style="color:var(--dg)">CR\u00cdTICO</strong> - 214 contas inativas h\u00e1 30+ dias<br><small style="color:var(--tx2)">Detectado h\u00e1 6h | Sinais</small></div>
<div class="alert-item" style="border-left:3px solid var(--wn)"><span class="dismiss" onclick="this.parentElement.remove();updateAlertCount()">&times;</span><strong style="color:var(--wn)">ALERTA</strong> - Queda brusca de Health Score em 15 contas (delta &gt; -15)<br><small style="color:var(--tx2)">Detectado h\u00e1 12h | Health Score</small></div>
<div class="alert-item" style="border-left:3px solid var(--wn)"><span class="dismiss" onclick="this.parentElement.remove();updateAlertCount()">&times;</span><strong style="color:var(--wn)">ALERTA</strong> - Taxa de turnover acima de 15% no cluster Bronze<br><small style="color:var(--tx2)">Detectado h\u00e1 1d | Turnover</small></div>
<div class="alert-item" style="border-left:3px solid var(--wn)"><span class="dismiss" onclick="this.parentElement.remove();updateAlertCount()">&times;</span><strong style="color:var(--wn)">ALERTA</strong> - 7 contas com Score Fraude &gt; 60<br><small style="color:var(--tx2)">Detectado h\u00e1 1d | Fraude</small></div>
<div class="alert-item" style="border-left:3px solid var(--info)"><span class="dismiss" onclick="this.parentElement.remove();updateAlertCount()">&times;</span><strong style="color:var(--info)">INFO</strong> - 143 contas eleg\u00edveis para expans\u00e3o Tier 1<br><small style="color:var(--tx2)">Detectado h\u00e1 2d | Expans\u00e3o</small></div>
</div>
<h3 class="section-title">Hist\u00f3rico de Alertas (7 dias)</h3>
<div class="tbl-wrap"><table><thead><tr><th>Data</th><th>Severidade</th><th>Descri\u00e7\u00e3o</th><th>Status</th></tr></thead><tbody>
<tr><td>2026-05-19</td><td><span class="tag tag-dg">Cr\u00edtico</span></td><td>Pico de churn: 12 contas perdidas em 24h</td><td><span class="tag tag-ok">Resolvido</span></td></tr>
<tr><td>2026-05-18</td><td><span class="tag tag-wn">Alerta</span></td><td>SLA violado: 3 tickets Premium sem resposta</td><td><span class="tag tag-ok">Resolvido</span></td></tr>
<tr><td>2026-05-17</td><td><span class="tag tag-wn">Alerta</span></td><td>Inadimpl\u00eancia acima de 12% no cluster Prata</td><td><span class="tag tag-ok">Resolvido</span></td></tr>
<tr><td>2026-05-16</td><td><span class="tag tag-info">Info</span></td><td>28 novos onboardings conclu\u00eddos</td><td><span class="tag tag-ok">Resolvido</span></td></tr>
<tr><td>2026-05-15</td><td><span class="tag tag-dg">Cr\u00edtico</span></td><td>Falha na sincroniza\u00e7\u00e3o Redshift - dados desatualizados</td><td><span class="tag tag-ok">Resolvido</span></td></tr>
</tbody></table></div>
</div>
''')

def write_command_palette(f):
    f.write('''<div class="cmd-palette" id="cmd-palette" onclick="if(event.target===this)closePalette()">
<div class="cmd-box">
<input type="text" id="cmd-input" placeholder="Buscar p\u00e1gina, medida ou a\u00e7\u00e3o..." oninput="searchCmd(this.value)">
<div class="cmd-results" id="cmd-results"></div>
</div>
</div>
''')
