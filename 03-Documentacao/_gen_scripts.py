def write_scripts(f):
    f.write('''<script>
// === STATE ===
const pages=['overview','clusters','health','churn','financeiro','turnover','fraude','modelo','medidas','alertas'];
const pageNames=['Vis\u00e3o Geral','Clusters CS','Health Score','Churn & Risco','Financeiro','Turnover','Fraude','Modelo Dados','Cat\u00e1logo Medidas','Alertas'];
let currentPage='overview';
let charts={};

// === NAVIGATION ===
function goTo(page){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('pg-'+page).classList.add('active');
  document.querySelectorAll('.sidebar nav a').forEach(a=>{a.classList.remove('active');if(a.dataset.page===page)a.classList.add('active')});
  document.getElementById('bc-page').textContent=pageNames[pages.indexOf(page)];
  currentPage=page;
  if(page==='overview')initOverviewCharts();
  if(page==='clusters')initClusterCharts();
  if(page==='health')initHealthCharts();
  if(page==='churn')initChurnCharts();
  if(page==='financeiro')initFinCharts();
  if(page==='turnover')initTurnoverCharts();
  if(page==='fraude')initFraudeCharts();
}
document.querySelectorAll('.sidebar nav a').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();goTo(a.dataset.page)}));

// === DARK MODE ===
function toggleDark(){
  const t=document.documentElement.dataset.theme==='dark'?'light':'dark';
  document.documentElement.dataset.theme=t;
  localStorage.setItem('theme',t);
  Object.values(charts).forEach(c=>{if(c&&c.options){c.options.plugins=c.options.plugins||{};c.update()}});
}
(function(){const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t})();

// === FILTERS ===
function applyFilters(){
  const period=document.getElementById('f-period').value;
  const clusters=[...document.querySelectorAll('.chk-group input:checked')].map(i=>i.value);
  const tipo=document.getElementById('f-tipo').value;
  const status=document.getElementById('f-status').value;
  const uf=document.getElementById('f-uf').value;
  // Simulate filter effect on cards
  const base={contas:1953,health:72.4,churn:4.2,mrr:287,alerts:7};
  let mult=1;
  if(clusters.length<5)mult*=(clusters.length/5);
  if(tipo!=='all')mult*=0.4;
  if(status==='inativo')mult*=0.15;
  else if(status==='inadimplente')mult*=0.12;
  if(uf!=='all')mult*=0.08;
  if(period==='7')mult*=0.85;
  else if(period==='15')mult*=0.92;
  else if(period==='quarter')mult*=1.1;
  else if(period==='semester')mult*=1.2;
  const c=Math.round(base.contas*mult);
  document.getElementById('v-contas').textContent=c.toLocaleString('pt-BR');
  document.getElementById('v-health').textContent=(base.health*(0.9+mult*0.1)).toFixed(1);
  document.getElementById('v-churn').textContent=(base.churn*(2-mult)).toFixed(1)+'%';
  document.getElementById('v-mrr').textContent='R$ '+(base.mrr*mult).toFixed(0)+'k';
}

// === EXPORT ===
function exportPDF(){window.print()}
function copyData(){
  const tables=document.querySelectorAll('.page.active table');
  if(!tables.length){navigator.clipboard.writeText('Nenhuma tabela na p\u00e1gina atual');return}
  let txt='';
  tables.forEach(t=>{
    t.querySelectorAll('tr').forEach(r=>{
      const cells=[...r.querySelectorAll('th,td')].map(c=>c.textContent.trim());
      txt+=cells.join('\\t')+'\\n';
    });
    txt+='\\n';
  });
  navigator.clipboard.writeText(txt).then(()=>alert('Dados copiados!'));
}

// === COMMAND PALETTE ===
function openPalette(){document.getElementById('cmd-palette').classList.add('open');document.getElementById('cmd-input').focus()}
function closePalette(){document.getElementById('cmd-palette').classList.remove('open');document.getElementById('cmd-input').value=''}
function searchCmd(q){
  const r=document.getElementById('cmd-results');
  if(!q){r.innerHTML='';return}
  const items=[...pages.map((p,i)=>({label:pageNames[i],action:()=>goTo(p),icon:'fas fa-file'})),
    {label:'Exportar PDF',action:exportPDF,icon:'fas fa-file-pdf'},
    {label:'Copiar Dados',action:copyData,icon:'fas fa-copy'},
    {label:'Alternar Tema',action:toggleDark,icon:'fas fa-moon'}
  ];
  const filtered=items.filter(i=>i.label.toLowerCase().includes(q.toLowerCase()));
  r.innerHTML=filtered.map(i=>`<a href="#" onclick="event.preventDefault();closePalette();(${i.action.toString()})()" ><i class="${i.icon}"></i>${i.label}</a>`).join('');
}
document.addEventListener('keydown',e=>{
  if(e.ctrlKey&&e.key==='k'){e.preventDefault();openPalette()}
  if(e.key==='Escape')closePalette();
  if(!e.ctrlKey&&!e.altKey&&e.target.tagName!=='INPUT'){
    const idx='1234567890'.indexOf(e.key);
    if(idx>=0&&idx<pages.length){e.preventDefault();goTo(pages[idx])}
  }
});

// === TABLE SORT ===
function sortTable(id,col){
  const t=document.getElementById(id);if(!t)return;
  const tbody=t.querySelector('tbody');
  const rows=[...tbody.querySelectorAll('tr')];
  const dir=t.dataset.sortDir==='asc'?'desc':'asc';
  t.dataset.sortDir=dir;
  rows.sort((a,b)=>{
    const av=a.cells[col].textContent.trim();
    const bv=b.cells[col].textContent.trim();
    const an=parseFloat(av.replace(/[^0-9.-]/g,''));
    const bn=parseFloat(bv.replace(/[^0-9.-]/g,''));
    if(!isNaN(an)&&!isNaN(bn))return dir==='asc'?an-bn:bn-an;
    return dir==='asc'?av.localeCompare(bv):bv.localeCompare(av);
  });
  rows.forEach(r=>tbody.appendChild(r));
}

// === MEASURES FILTER ===
function filterMeasures(){
  const q=document.getElementById('search-measures').value.toLowerCase();
  document.querySelectorAll('.measure-card').forEach(c=>{
    const match=c.dataset.name.includes(q)||c.dataset.folder.includes(q);
    c.style.display=match?'':'none';
  });
  document.querySelectorAll('[data-folder]').forEach(h=>{
    if(h.classList.contains('measure-card'))return;
    const folder=h.dataset.folder.toLowerCase();
    h.style.display=folder.includes(q)||!q?'':'none';
  });
}

// === ALERT COUNT ===
function updateAlertCount(){
  const c=document.querySelectorAll('#alerts-list .alert-item').length;
  document.getElementById('alert-count').textContent=c;
  document.getElementById('v-alerts').textContent=c;
}

// === CHARTS ===
const pri='#F46901',pril='#FF8534',ok='#10B981',wn='#F59E0B',dg='#EF4444',info='#8B5CF6';
function getTextColor(){return getComputedStyle(document.documentElement).getPropertyValue('--tx').trim()||'#1A1A2E'}
function getGridColor(){return getComputedStyle(document.documentElement).getPropertyValue('--bd').trim()||'#E5E7EB'}

function makeSparkline(id,data,color){
  const ctx=document.getElementById(id);if(!ctx)return;
  new Chart(ctx,{type:'line',data:{labels:data.map((_,i)=>i),datasets:[{data,borderColor:color||pri,borderWidth:2,fill:true,backgroundColor:color?color+'20':pri+'20',pointRadius:0,tension:.4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},datalabels:{display:false}},scales:{x:{display:false},y:{display:false}}}});
}

function drawGauge(id,value,max){
  const ctx=document.getElementById(id);if(!ctx)return;
  const color=value>=75?ok:value>=50?wn:value>=25?dg:'#7F1D1D';
  new Chart(ctx,{type:'doughnut',data:{datasets:[{data:[value,max-value],backgroundColor:[color,'#E5E7EB'],borderWidth:0}]},options:{responsive:false,circumference:180,rotation:270,cutout:'75%',plugins:{legend:{display:false},datalabels:{display:false}}}});
}

function initOverviewCharts(){
  makeSparkline('spark-contas',[1820,1850,1870,1890,1910,1930,1953]);
  makeSparkline('spark-health',[69,70,70.5,71,71.8,72,72.4]);
  makeSparkline('spark-churn',[5.1,4.9,4.8,4.6,4.5,4.3,4.2],dg);
  makeSparkline('spark-mrr',[260,265,270,275,278,283,287]);
  makeSparkline('spark-alerts',[12,10,9,8,8,7,7],wn);
  // Cluster distribution
  if(charts.clDist)charts.clDist.destroy();
  charts.clDist=new Chart(document.getElementById('chart-clusters'),{type:'doughnut',data:{labels:['Tech','Bronze','Prata','Ouro','Premium'],datasets:[{data:[952,587,327,67,20],backgroundColor:[info,'#CD7F32','#C0C0C0','#FFD700',pri]}]},options:{plugins:{legend:{position:'right',labels:{font:{family:'Raleway',size:11}}},datalabels:{color:'#fff',font:{weight:'bold',size:11},formatter:(v,c)=>Math.round(v/1953*100)+'%'}}}});
  // Health trend
  if(charts.hTrend)charts.hTrend.destroy();
  charts.hTrend=new Chart(document.getElementById('chart-health-trend'),{type:'line',data:{labels:['D1','D5','D10','D15','D20','D25','D30'],datasets:[{label:'Health Score',data:[69,70,70.5,71.2,71.8,72,72.4],borderColor:pri,backgroundColor:pri+'20',fill:true,tension:.4}]},options:{plugins:{legend:{display:false},datalabels:{display:false}},scales:{y:{min:60,max:80,grid:{color:getGridColor()}},x:{grid:{display:false}}}}});
  // MRR Waterfall
  if(charts.mrrW)charts.mrrW.destroy();
  charts.mrrW=new Chart(document.getElementById('chart-mrr-waterfall'),{type:'bar',data:{labels:['Inicio','Expansao','Novos','Churn','Downgrade','Final'],datasets:[{label:'MRR',data:[275,18,12,-8,-10,287],backgroundColor:['#6B7280',ok,ok,dg,dg,pri]}]},options:{plugins:{legend:{display:false},datalabels:{anchor:'end',align:'top',font:{size:10,weight:'bold'},formatter:v=>v>0?'+'+v:v}},scales:{y:{grid:{color:getGridColor()}},x:{grid:{display:false}}}}});
  // UF Heatmap
  const hm=document.getElementById('heatmap-uf');
  if(hm){
    const ufs=[['SP',420],['RJ',180],['MG',150],['PR',95],['RS',88],['BA',72],['SC',65],['GO',55],['PE',48],['CE',42],['DF',38],['ES',32],['PA',28],['MA',22],['MT',18],['MS',16],['RN',14],['PB',12],['AL',10],['SE',8],['PI',7],['RO',6],['TO',5],['AM',4],['AP',3],['AC',2],['RR',1]];
    let html='<div style="display:flex;flex-wrap:wrap;gap:4px">';
    ufs.forEach(([uf,v])=>{
      const pct=v/420;const bg=pct>.5?pri:pct>.2?pril:'#FED7AA';const c=pct>.5?'#fff':'#1A1A2E';
      html+=`<div style="padding:4px 8px;border-radius:4px;background:${bg};color:${c};font-size:10px;font-weight:700;min-width:48px;text-align:center">${uf}<br><span style="font-weight:400">${v}</span></div>`;
    });
    html+='</div>';hm.innerHTML=html;
  }
}

function initClusterCharts(){
  if(charts.clBar)charts.clBar.destroy();
  charts.clBar=new Chart(document.getElementById('chart-cluster-bar'),{type:'bar',data:{labels:['Tech','Bronze','Prata','Ouro','Premium'],datasets:[{data:[952,587,327,67,20],backgroundColor:[info,'#CD7F32','#C0C0C0','#FFD700',pri]}]},options:{indexAxis:'y',plugins:{legend:{display:false},datalabels:{anchor:'end',align:'right',font:{size:10,weight:'bold'}}},scales:{x:{grid:{color:getGridColor()}},y:{grid:{display:false}}}}});
  if(charts.sla)charts.sla.destroy();
  charts.sla=new Chart(document.getElementById('chart-sla'),{type:'bar',data:{labels:['Tech','Bronze','Prata','Ouro','Premium'],datasets:[{label:'SLA %',data:[94,91,88,96,99],backgroundColor:pri}]},options:{plugins:{legend:{display:false},datalabels:{anchor:'end',align:'top',font:{size:10},formatter:v=>v+'%'}},scales:{y:{min:80,max:100,grid:{color:getGridColor()}},x:{grid:{display:false}}}}});
}

function initHealthCharts(){
  drawGauge('gauge-health',72.4,100);
  if(charts.hCluster)charts.hCluster.destroy();
  charts.hCluster=new Chart(document.getElementById('chart-health-cluster'),{type:'bar',data:{labels:['Tech','Bronze','Prata','Ouro','Premium'],datasets:[{label:'Health Score',data:[65,68,74,82,91],backgroundColor:[info,'#CD7F32','#C0C0C0','#FFD700',pri]}]},options:{plugins:{legend:{display:false},datalabels:{anchor:'end',align:'top',font:{size:11,weight:'bold'}}},scales:{y:{min:50,max:100,grid:{color:getGridColor()}},x:{grid:{display:false}}}}});
}

function initChurnCharts(){
  if(charts.chTrend)charts.chTrend.destroy();
  charts.chTrend=new Chart(document.getElementById('chart-churn-trend'),{type:'line',data:{labels:['Jan','Fev','Mar','Abr','Mai','Jun'],datasets:[{label:'Taxa Churn %',data:[5.8,5.4,5.1,4.8,4.5,4.2],borderColor:dg,backgroundColor:dg+'20',fill:true,tension:.3}]},options:{plugins:{legend:{display:false},datalabels:{display:false}},scales:{y:{min:3,max:7,grid:{color:getGridColor()}},x:{grid:{display:false}}}}});
  if(charts.fatZ)charts.fatZ.destroy();
  charts.fatZ=new Chart(document.getElementById('chart-fat-zerado'),{type:'doughnut',data:{labels:['OK','Alerta Leve','A\u00e7\u00e3o Necess\u00e1ria','Cr\u00edtico','Churn Iminente'],datasets:[{data:[1580,120,95,87,71],backgroundColor:[ok,wn,'#F97316',dg,'#7F1D1D']}]},options:{plugins:{legend:{position:'right',labels:{font:{family:'Raleway',size:10}}},datalabels:{color:'#fff',font:{weight:'bold',size:10},formatter:(v)=>v}}}});
}

function initFinCharts(){
  if(charts.finW)charts.finW.destroy();
  charts.finW=new Chart(document.getElementById('chart-fin-waterfall'),{type:'bar',data:{labels:['MRR Anterior','Expans\u00e3o','Novos Clientes','Churn','Downgrade','Inadimpl\u00eancia','MRR Atual'],datasets:[{data:[275,18,12,-8,-10,-5,287],backgroundColor:['#6B7280',ok,ok,dg,dg,wn,pri]}]},options:{plugins:{legend:{display:false},datalabels:{anchor:'end',align:'top',font:{size:10,weight:'bold'},formatter:v=>'R$'+v+'k'}},scales:{y:{grid:{color:getGridColor()}},x:{grid:{display:false}}}}});
}

function initTurnoverCharts(){
  if(charts.turn)charts.turn.destroy();
  charts.turn=new Chart(document.getElementById('chart-turnover'),{type:'bar',data:{labels:['Jan','Fev','Mar','Abr','Mai','Jun'],datasets:[{label:'Admiss\u00f5es',data:[310,295,320,335,328,342],backgroundColor:ok},{label:'Desligamentos',data:[280,265,290,275,270,287],backgroundColor:dg}]},options:{plugins:{datalabels:{display:false}},scales:{y:{grid:{color:getGridColor()}},x:{grid:{display:false}}}}});
}

function initFraudeCharts(){drawGauge('gauge-fraude',23,100)}

// === INIT ===
document.addEventListener('DOMContentLoaded',()=>{initOverviewCharts()});
</script>
</body>
''')
