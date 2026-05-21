# -*- coding: utf-8 -*-
"""Parts for the v2 dashboard generator."""

def write_head(f):
    f.write('''<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>An\u00e1lise CS \u2014 Cadastro Promotores v2 | Mob2Con</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700;900&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
''')

def write_styles(f):
    f.write('''<style>
:root{--pri:#F46901;--pri-l:#FF8534;--pri-d:#C45500;--bg:#F8F9FA;--sf:#FFF;--tx:#1A1A2E;--tx2:#6B7280;--bd:#E5E7EB;--ok:#10B981;--wn:#F59E0B;--dg:#EF4444;--info:#8B5CF6;--sw:220px;--hh:56px;--fh:48px;--r:8px;--sh:0 2px 8px rgba(0,0,0,.08);--f:'Raleway',sans-serif}
[data-theme="dark"]{--bg:#0F1117;--sf:#1A1D2E;--tx:#E5E7EB;--tx2:#9CA3AF;--bd:#2D3348;--sh:0 2px 8px rgba(0,0,0,.3)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--f);background:var(--bg);color:var(--tx);font-size:13px;line-height:1.5;overflow-x:hidden;transition:background .3s,color .3s}
a{color:var(--pri);text-decoration:none}
button{font-family:var(--f);cursor:pointer;border:none;background:none}
.app{display:flex;min-height:100vh}
.sidebar{width:var(--sw);background:var(--sf);border-right:1px solid var(--bd);position:fixed;top:0;left:0;height:100vh;z-index:100;display:flex;flex-direction:column;transition:background .3s,border .3s}
.sidebar .logo{padding:16px;text-align:center;border-bottom:1px solid var(--bd)}
.sidebar .logo h2{font-size:15px;font-weight:900;color:var(--pri)}
.sidebar .logo span{font-size:10px;color:var(--tx2);display:block;margin-top:2px}
.sidebar nav{flex:1;overflow-y:auto;padding:8px}
.sidebar nav a{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:var(--r);color:var(--tx);font-weight:600;font-size:11px;transition:all .2s;margin-bottom:2px}
.sidebar nav a:hover,.sidebar nav a.active{background:var(--pri);color:#fff}
.sidebar nav a i{width:16px;text-align:center;font-size:12px}
.badge{font-size:9px;padding:2px 6px;border-radius:10px;font-weight:700}
.badge-danger{background:var(--dg);color:#fff}
.badge-warn{background:var(--wn);color:#fff}
.badge-ok{background:var(--ok);color:#fff}
.main{margin-left:var(--sw);flex:1;display:flex;flex-direction:column;transition:margin .3s}
.header{height:var(--hh);background:var(--sf);border-bottom:1px solid var(--bd);display:flex;align-items:center;justify-content:space-between;padding:0 24px;position:sticky;top:0;z-index:90;transition:background .3s,border .3s}
.breadcrumb{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--tx2)}
.breadcrumb .sep{color:var(--bd)}
.hdr-actions{display:flex;align-items:center;gap:10px}
.btn{padding:6px 14px;border-radius:var(--r);font-size:11px;font-weight:600;transition:all .2s;display:inline-flex;align-items:center;gap:6px}
.btn-pri{background:var(--pri);color:#fff}.btn-pri:hover{background:var(--pri-d)}
.btn-out{border:1px solid var(--bd);color:var(--tx)}.btn-out:hover{border-color:var(--pri);color:var(--pri)}
.btn-sm{padding:4px 10px;font-size:10px}
.toggle-dark{width:36px;height:20px;border-radius:10px;background:var(--bd);position:relative;transition:background .3s}
.toggle-dark::after{content:'';position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;transition:transform .3s}
[data-theme="dark"] .toggle-dark{background:var(--pri)}
[data-theme="dark"] .toggle-dark::after{transform:translateX(16px)}
.filter-bar{min-height:var(--fh);background:var(--sf);border-bottom:1px solid var(--bd);display:flex;align-items:center;gap:10px;padding:8px 24px;position:sticky;top:var(--hh);z-index:80;flex-wrap:wrap;transition:background .3s,border .3s}
.filter-bar select{font-family:var(--f);font-size:11px;padding:5px 8px;border:1px solid var(--bd);border-radius:var(--r);background:var(--sf);color:var(--tx)}
.filter-bar label{font-size:10px;font-weight:700;color:var(--tx2);white-space:nowrap}
.chk-group{display:flex;gap:6px;align-items:center}
.chk-group label{display:flex;align-items:center;gap:3px;font-weight:400;font-size:11px;cursor:pointer}
.chk-group input[type="checkbox"]{accent-color:var(--pri);width:13px;height:13px}
.content{flex:1;padding:24px}
.page{display:none;animation:fadeIn .3s}
.page.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.grid{display:grid;gap:16px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
.g5{grid-template-columns:repeat(5,1fr)}
.card{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:16px;box-shadow:var(--sh);transition:all .3s}
.card:hover{box-shadow:0 4px 16px rgba(244,105,1,.12);border-color:var(--pri-l)}
.card-title{font-size:10px;font-weight:700;color:var(--tx2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.card-value{font-size:24px;font-weight:900;color:var(--tx)}
.card-sub{font-size:11px;color:var(--tx2);margin-top:4px;display:flex;align-items:center;gap:4px}
.card-sub .up{color:var(--ok)}.card-sub .down{color:var(--dg)}
.card-spark{height:30px;margin-top:8px}
.section-title{font-size:14px;font-weight:700;margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid var(--pri)}
.tbl-wrap{overflow-x:auto;border-radius:var(--r);border:1px solid var(--bd)}
table{width:100%;border-collapse:collapse;font-size:11px}
th{background:var(--sf);font-weight:700;text-align:left;padding:8px 12px;border-bottom:2px solid var(--bd);cursor:pointer;user-select:none;white-space:nowrap}
th:hover{color:var(--pri)}
td{padding:8px 12px;border-bottom:1px solid var(--bd)}
tr:hover td{background:rgba(244,105,1,.04)}
.progress-bar{height:6px;background:var(--bd);border-radius:3px;overflow:hidden}
.progress-bar .fill{height:100%;background:var(--pri);border-radius:3px;transition:width .5s}
.chart-container{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:16px;box-shadow:var(--sh)}
.gauge-wrap{display:flex;align-items:center;justify-content:center;flex-direction:column}
.tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700}
.tag-ok{background:#D1FAE5;color:#065F46}
.tag-wn{background:#FEF3C7;color:#92400E}
.tag-dg{background:#FEE2E2;color:#991B1B}
.tag-info{background:#EDE9FE;color:#5B21B6}
[data-theme="dark"] .tag-ok{background:#064E3B;color:#6EE7B7}
[data-theme="dark"] .tag-wn{background:#78350F;color:#FCD34D}
[data-theme="dark"] .tag-dg{background:#7F1D1D;color:#FCA5A5}
[data-theme="dark"] .tag-info{background:#4C1D95;color:#C4B5FD}
.cmd-palette{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:9999;align-items:flex-start;justify-content:center;padding-top:120px}
.cmd-palette.open{display:flex}
.cmd-box{background:var(--sf);border-radius:12px;width:500px;max-height:400px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.cmd-box input{width:100%;padding:16px 20px;border:none;font-size:14px;font-family:var(--f);background:transparent;color:var(--tx);outline:none}
.cmd-results{max-height:300px;overflow-y:auto;border-top:1px solid var(--bd)}
.cmd-results a{display:flex;align-items:center;gap:10px;padding:10px 20px;font-size:12px;color:var(--tx);transition:background .1s}
.cmd-results a:hover,.cmd-results a.sel{background:rgba(244,105,1,.1);color:var(--pri)}
.alert-panel{position:fixed;top:var(--hh);right:0;width:320px;max-height:calc(100vh - var(--hh));background:var(--sf);border-left:1px solid var(--bd);box-shadow:-4px 0 20px rgba(0,0,0,.1);z-index:95;transform:translateX(100%);transition:transform .3s;overflow-y:auto;padding:16px}
.alert-panel.open{transform:translateX(0)}
.alert-item{padding:10px;border-radius:var(--r);border:1px solid var(--bd);margin-bottom:8px;font-size:11px}
.alert-item .dismiss{float:right;cursor:pointer;color:var(--tx2);font-size:10px}
.measure-card{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);margin-bottom:8px;overflow:hidden}
.measure-card .mh{padding:10px 14px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;font-size:12px;font-weight:600}
.measure-card .mh:hover{background:rgba(244,105,1,.04)}
.measure-card .mb{display:none;padding:12px 14px;border-top:1px solid var(--bd);background:var(--bg)}
.measure-card .mb.open{display:block}
.measure-card pre{font-size:11px;white-space:pre-wrap;word-break:break-all;font-family:'Courier New',monospace;line-height:1.6}
.search-measures{width:100%;padding:8px 12px;border:1px solid var(--bd);border-radius:var(--r);font-family:var(--f);font-size:12px;margin-bottom:16px;background:var(--sf);color:var(--tx)}
@media print{.sidebar,.header,.filter-bar,.btn,.toggle-dark,.alert-panel,.cmd-palette{display:none!important}.main{margin-left:0!important}.page{display:block!important;page-break-after:always}.card{box-shadow:none;border:1px solid #ddd}}
@media(max-width:1024px){.g4,.g5{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:1fr}}
@media(max-width:768px){.sidebar{transform:translateX(-100%)}.main{margin-left:0}.g2,.g3,.g4,.g5{grid-template-columns:1fr}.filter-bar{flex-direction:column;align-items:flex-start}}
</style>
</head>
''')
