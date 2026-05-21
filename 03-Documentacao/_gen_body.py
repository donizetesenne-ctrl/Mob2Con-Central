def write_body_start(f):
    f.write('<body>\n<div class="app">\n')

def write_sidebar(f):
    f.write('''<aside class="sidebar">
<div class="logo"><h2>Mob2Con</h2><span>CS Dashboard v2.0</span></div>
<nav>
<a href="#" data-page="overview" class="active"><i class="fas fa-chart-pie"></i>Vis\u00e3o Geral</a>
<a href="#" data-page="clusters"><i class="fas fa-layer-group"></i>Clusters CS</a>
<a href="#" data-page="health"><i class="fas fa-heartbeat"></i>Health Score</a>
<a href="#" data-page="churn"><i class="fas fa-user-minus"></i>Churn &amp; Risco</a>
<a href="#" data-page="financeiro"><i class="fas fa-dollar-sign"></i>Financeiro</a>
<a href="#" data-page="turnover"><i class="fas fa-exchange-alt"></i>Turnover</a>
<a href="#" data-page="fraude"><i class="fas fa-shield-alt"></i>Fraude</a>
<a href="#" data-page="modelo"><i class="fas fa-database"></i>Modelo Dados</a>
<a href="#" data-page="medidas"><i class="fas fa-calculator"></i>Cat\u00e1logo Medidas</a>
<a href="#" data-page="alertas"><i class="fas fa-bell"></i>Alertas <span class="badge badge-danger" id="alert-count">7</span></a>
</nav>
</aside>
''')

def write_header(f):
    f.write('''<div class="main">
<header class="header">
<div class="breadcrumb"><span>Mob2Con</span><span class="sep">/</span><span>CS Dashboard</span><span class="sep">/</span><span id="bc-page">Vis\u00e3o Geral</span></div>
<div class="hdr-actions">
<button class="btn btn-out btn-sm" onclick="openPalette()" title="Ctrl+K"><i class="fas fa-search"></i>Buscar</button>
<button class="btn btn-out btn-sm" onclick="exportPDF()"><i class="fas fa-file-pdf"></i>PDF</button>
<button class="btn btn-out btn-sm" onclick="copyData()"><i class="fas fa-copy"></i>Copiar</button>
<button class="toggle-dark" onclick="toggleDark()" title="Alternar tema"></button>
</div>
</header>
''')

def write_filters(f):
    ufs = 'AC,AL,AM,AP,BA,CE,DF,ES,GO,MA,MG,MS,MT,PA,PB,PE,PI,PR,RJ,RN,RO,RR,RS,SC,SE,SP,TO'.split(',')
    uf_opts = ''.join(f'<option value="{u}">{u}</option>' for u in ufs)
    f.write(f'''<div class="filter-bar">
<label>Per\u00edodo:</label>
<select id="f-period" onchange="applyFilters()">
<option value="7">\u00daltimos 7d</option><option value="15">\u00daltimos 15d</option><option value="30" selected>\u00daltimos 30d</option><option value="month">\u00daltimo M\u00eas</option><option value="quarter">\u00daltimo Trimestre</option><option value="semester">\u00daltimos 6 Meses</option>
</select>
<label>Cluster:</label>
<div class="chk-group">
<label><input type="checkbox" checked value="Tech" onchange="applyFilters()">Tech</label>
<label><input type="checkbox" checked value="Bronze" onchange="applyFilters()">Bronze</label>
<label><input type="checkbox" checked value="Prata" onchange="applyFilters()">Prata</label>
<label><input type="checkbox" checked value="Ouro" onchange="applyFilters()">Ouro</label>
<label><input type="checkbox" checked value="Premium" onchange="applyFilters()">Premium</label>
</div>
<label>Tipo:</label>
<select id="f-tipo" onchange="applyFilters()">
<option value="all">Todos</option><option value="agencia">Ag\u00eancia</option><option value="fornecedor">Fornecedor</option><option value="rede">Rede</option>
</select>
<label>Status:</label>
<select id="f-status" onchange="applyFilters()">
<option value="all">Todos</option><option value="ativo">Ativo</option><option value="inativo">Inativo</option><option value="inadimplente">Inadimplente</option>
</select>
<label>UF:</label>
<select id="f-uf" onchange="applyFilters()">
<option value="all">Todas</option>{uf_opts}
</select>
</div>
''')
