# -*- coding: utf-8 -*-
"""Gera o HTML completo do dashboard Estudo Cadastro Promotores."""
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "ANALISE-ESTUDO-CADASTRO-PROMOTORES.html")

html = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mob2Con - Estudo Cadastro Promotores | Dashboard Interativo</title>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;700;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"><\/script>
'''

html += r'''<style>
:root{--p:#F46901;--pl:#FF8C3A;--pd:#C85500;--g:#16A34A;--r:#DC2626;--y:#EAB308;--b:#2563EB;--pu:#7C3AED;
--bg:#F1F5F9;--card:#FFF;--sb:#1E293B;--tx:#0F172A;--tx2:#475569;--mu:#94A3B8;--bd:#E2E8F0;
--sh:0 2px 8px rgba(0,0,0,.08);--f:'Raleway',sans-serif;--rad:8px}
[data-t=d]{--bg:#0F172A;--card:#1E293B;--tx:#F1F5F9;--tx2:#CBD5E1;--mu:#64748B;--bd:#334155;--sh:0 2px 8px rgba(0,0,0,.3)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--f);background:var(--bg);color:var(--tx);display:flex;min-height:100vh;font-size:13px;line-height:1.5;transition:all .3s}
.sb{width:250px;min-height:100vh;background:var(--sb);color:#E2E8F0;position:fixed;left:0;top:0;bottom:0;z-index:100;overflow-y:auto;display:flex;flex-direction:column}
.sb-h{padding:16px;border-bottom:1px solid rgba(255,255,255,.1);display:flex;align-items:center;justify-content:space-between}
.sb-h h1{font-size:17px;font-weight:900;color:var(--p)}
.sb-h small{font-size:9px;color:var(--mu);display:block;margin-top:2px}
.tb{width:30px;height:30px;border-radius:6px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#E2E8F0;font-size:14px;border:none;background:none}
.tb:hover{background:rgba(255,255,255,.1)}
.ns{padding:10px 14px}
.ns input{width:100%;padding:7px 10px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);border-radius:6px;color:#E2E8F0;outline:none;font-size:11px}
.ns input:focus{border-color:var(--p)}
.ns input::placeholder{color:var(--mu)}
.nt{padding:4px 14px;font-size:9px;text-transform:uppercase;letter-spacing:1px;color:var(--mu);margin-top:10px}
.ni{display:flex;align-items:center;padding:8px 14px;margin:1px 6px;border-radius:6px;cursor:pointer;transition:all .2s;gap:8px;font-size:11.5px;font-weight:700}
.ni:hover{background:rgba(255,255,255,.06)}
.ni.a{background:var(--p);color:#fff}
.ni .nn{width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:900;flex-shrink:0}
.ni.a .nn{background:rgba(255,255,255,.2)}
.mn{margin-left:250px;flex:1;display:flex;flex-direction:column;min-height:100vh}
.fb{background:var(--card);border-bottom:1px solid var(--bd);padding:12px 24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;position:sticky;top:0;z-index:50}
.fb select,.fb input[type=date]{padding:6px 10px;border:1px solid var(--bd);border-radius:6px;font-size:11px;background:var(--card);color:var(--tx);outline:none}
.fb select:focus,.fb input:focus{border-color:var(--p)}
.fb label{font-size:10px;font-weight:700;color:var(--mu);text-transform:uppercase;letter-spacing:.5px}
.fb .fg{display:flex;flex-direction:column;gap:3px}
.fb .sep{width:1px;height:28px;background:var(--bd);margin:0 8px}
.fb .clear-btn{padding:5px 12px;border-radius:6px;border:1px solid var(--bd);font-size:10px;font-weight:700;color:var(--tx2);cursor:pointer;transition:all .2s}
.fb .clear-btn:hover{border-color:var(--p);color:var(--p)}
.pg{display:none;padding:24px;animation:fi .3s ease}
.pg.a{display:block}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.ph{margin-bottom:24px}
.ph h2{font-size:22px;font-weight:900}
.ph p{color:var(--tx2);font-size:12px;margin-top:2px}
.badge{display:inline-block;background:var(--p);color:#fff;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;margin-left:6px;vertical-align:middle}
.cg{display:grid;gap:16px;margin-bottom:24px}
.cg4{grid-template-columns:repeat(4,1fr)}
.cg3{grid-template-columns:repeat(3,1fr)}
.cg5{grid-template-columns:repeat(5,1fr)}
.cg2{grid-template-columns:repeat(2,1fr)}
.cd{background:var(--card);border-radius:var(--rad);padding:20px;box-shadow:var(--sh);border:1px solid var(--bd);transition:transform .2s,box-shadow .2s}
.cd:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.12)}
.cd-l{font-size:10px;color:var(--mu);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}
.cd-v{font-size:24px;font-weight:900;line-height:1.2}
.cd-v.o{color:var(--p)}.cd-v.g{color:var(--g)}.cd-v.r{color:var(--r)}.cd-v.b{color:var(--b)}
.cd-d{font-size:11px;margin-top:3px;color:var(--tx2)}
.cd-d.up{color:var(--g)}.cd-d.dn{color:var(--r)}
.cr{display:grid;gap:20px;margin-bottom:24px}
.cr2{grid-template-columns:repeat(2,1fr)}
.cr3{grid-template-columns:repeat(3,1fr)}
.cb{background:var(--card);border-radius:var(--rad);padding:20px;box-shadow:var(--sh);border:1px solid var(--bd)}
.cb h3{font-size:13px;font-weight:700;margin-bottom:12px}
.tw{background:var(--card);border-radius:var(--rad);box-shadow:var(--sh);border:1px solid var(--bd);overflow-x:auto;margin-bottom:24px}
table.dt{width:100%;border-collapse:collapse;font-size:12px}
table.dt th{background:var(--sb);color:#E2E8F0;padding:10px 14px;text-align:left;font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:.5px}
table.dt td{padding:9px 14px;border-bottom:1px solid var(--bd)}
table.dt tr:hover td{background:rgba(244,105,1,.04)}
.tg{display:inline-block;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700}
.tg-tech{background:#E5E7EB;color:#374151}.tg-bronze{background:#FDE68A;color:#92400E}
.tg-prata{background:#D1D5DB;color:#374151}.tg-ouro{background:#FEF3C7;color:#D97706}
.tg-premium{background:#FED7AA;color:#C2410C}
.al{padding:14px 20px;border-radius:var(--rad);border-left:4px solid;margin-bottom:12px;background:var(--card);box-shadow:var(--sh)}
.al-c{border-color:var(--r)}.al-w{border-color:var(--y)}.al-i{border-color:var(--b)}
.al h4{font-size:13px;font-weight:700;margin-bottom:3px}
.al p{font-size:11px;color:var(--tx2)}
.sum{background:linear-gradient(135deg,var(--sb),#0F3460);color:#E2E8F0;border-radius:var(--rad);padding:24px;margin-bottom:24px}
.sum h3{font-size:16px;font-weight:900;color:var(--p);margin-bottom:12px}
.sum ul{list-style:none;display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
.sum li{font-size:12px;color:rgba(255,255,255,.85);padding:4px 0}
.sum li::before{content:"▸ ";color:var(--p);font-weight:700}
.ig{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-bottom:24px}
.ib{background:var(--card);border-radius:var(--rad);padding:20px;box-shadow:var(--sh);border:1px solid var(--bd)}
.ib h4{font-size:12px;font-weight:700;color:var(--p);margin-bottom:6px}
.ib li{font-size:11px;color:var(--tx2);padding:2px 0;list-style:none}
.ib li::before{content:"• ";color:var(--p)}
@media(max-width:1200px){.cg4,.cg5{grid-template-columns:repeat(2,1fr)}.cr2,.cr3{grid-template-columns:1fr}}
@media(max-width:768px){.sb{display:none}.mn{margin-left:0}.cg4,.cg3,.cg5,.cg2{grid-template-columns:1fr}}
@media print{.sb,.fb{display:none!important}.mn{margin-left:0!important}.pg{display:block!important;page-break-after:always}}
</style>
</head>
<body>
'''

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Parte 1 escrita: {len(html)} chars")
