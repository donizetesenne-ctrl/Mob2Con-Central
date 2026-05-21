// ── Cadastro Lite v3 – Mob2Con Apps Script Backend ────────────────────────────
// Atualizado: 19/05/2026
// Confrontado com Power BI "Indicadores de Performance - Cadastro Lite"
// Medidas alinhadas: Qtd. Requisições, Qtd. CPFs, breakdown por request_type
// ──────────────────────────────────────────────────────────────────────────────
const SHEETS_ID = '17wacDgqjMwO3lOknuk6TtKfTwamB1qz-MpGGuwM7n_4';

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Cadastro Lite – Monitoramento Mob2Con')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// ── KPIs globais (aba README) ─────────────────────────────────────────────────
function getKpis() {
  const ss = SpreadsheetApp.openById(SHEETS_ID);
  const ws = ss.getSheetByName('README');
  const rows = ws.getDataRange().getValues();
  const kpis = {};
  rows.forEach(r => {
    if (r[0] && r[1] !== '') kpis[String(r[0])] = r[1];
  });
  
  // Enriquecer com métricas calculadas do Power BI
  // Medidas PBI: Qtd. Requisições = DISTINCTCOUNT(lite_visitor_id)
  //              Qtd. CPFs = DISTINCTCOUNT(lite_visitor_cpf)
  const empresas = _toObjects('Empresas');
  const nc = empresas.filter(e => String(e.status_empresa) === 'Nao Cliente');
  const cl = empresas.filter(e => String(e.status_empresa) === 'Cliente');
  
  // Totais calculados
  kpis['Total Requisicoes Lite'] = empresas.reduce((s, e) => s + (+e.cadastros || 0), 0);
  kpis['Requisicoes NC'] = nc.reduce((s, e) => s + (+e.cadastros || 0), 0);
  kpis['Requisicoes Clientes'] = cl.reduce((s, e) => s + (+e.cadastros || 0), 0);
  kpis['CPFs NC'] = nc.reduce((s, e) => s + (+e.promotores || 0), 0);
  kpis['CPFs Clientes'] = cl.reduce((s, e) => s + (+e.promotores || 0), 0);
  kpis['Empresas NC'] = nc.length;
  kpis['Empresas Clientes'] = cl.length;
  kpis['Total Empresas'] = empresas.length;
  
  // Impacto financeiro: promotores NC × R$12,10
  kpis['Impacto Mensal NC (R$)'] = (nc.reduce((s, e) => s + (+e.promotores || 0), 0) * 12.10).toFixed(2);
  
  return kpis;
}

// ── Empresas (aba Empresas) ───────────────────────────────────────────────────
function getEmpresas() {
  return _toObjects('Empresas');
}

// ── Evolução Mensal (aba Evolucao_Mensal) ─────────────────────────────────────
function getMensal() {
  return _toObjects('Evolucao_Mensal');
}

// ── Convencional Mensal (aba Conv_Mensal) ─────────────────────────────────────
function getConvMensal() {
  return _toObjects('Conv_Mensal');
}

// ── Convencional snapshot (aba Convencional) ──────────────────────────────────
function getConvencional() {
  return _toObjects('Convencional');
}

// ── Captação por Rede ─────────────────────────────────────────────────────────
function getCaptacaoRede() {
  return _toObjects('Captacao_Rede');
}

// ── Captação por Clientes ─────────────────────────────────────────────────────
function getCaptacaoClientes() {
  return _toObjects('Captacao_Clientes');
}

// ── Redes com nome da empresa ─────────────────────────────────────────────────
function getRedes() {
  const redes = _toObjects('Redes');
  const empresas = _toObjects('Empresas');
  const empMap = {};
  empresas.forEach(e => { empMap[String(e.empresa_id)] = e.empresa; });
  redes.forEach(r => { r.empresa_nome = empMap[String(r.empresa_id)] || 'ID: ' + r.empresa_id; });
  return redes;
}

// ── Ações CS (leitura) ────────────────────────────────────────────────────────
function getAcoesCS() {
  const ss = SpreadsheetApp.openById(SHEETS_ID);
  const ws = ss.getSheetByName('Acoes_CS');
  if (!ws) return [];
  return _toObjects('Acoes_CS');
}

// ── Ações CS (gravação) ───────────────────────────────────────────────────────
function addAcaoCS(dados) {
  const ss = SpreadsheetApp.openById(SHEETS_ID);
  let ws = ss.getSheetByName('Acoes_CS');
  if (!ws) {
    ws = ss.insertSheet('Acoes_CS');
    ws.appendRow(['empresa_id', 'empresa', 'acao', 'responsavel', 'data_acao', 'status', 'observacao']);
  }
  ws.appendRow([
    dados.empresa_id || '',
    dados.empresa || '',
    dados.acao || '',
    dados.responsavel || '',
    new Date().toISOString().slice(0, 10),
    dados.status || 'Pendente',
    dados.observacao || ''
  ]);
  return { ok: true };
}

// ── NOVO: Indicadores confrontados com Power BI ───────────────────────────────
// Equivalências com medidas DAX do PBI:
// PBI: Qtd. Requisições (Não Clientes) = DISTINCTCOUNT('Não Clientes'[lite_visitor_id])
// Sheets: SUM(cadastros) WHERE status_empresa = 'Nao Cliente'
//
// PBI: Qtd. CPFs (Não Clientes) = DISTINCTCOUNT('Não Clientes'[lite_visitor_cpf])
// Sheets: SUM(promotores) WHERE status_empresa = 'Nao Cliente'
//
// PBI: request_type = 'Cadastro Promotor' | 'Alocacao' | 'Sem efeito'
// Sheets: Não disponível granularmente — usar Evolucao_Mensal para tendência
//
// NOTA: A planilha agrega por empresa. O PBI tem dados por requisição individual.
// Para breakdown por request_type, seria necessário nova aba com dados granulares.
function getIndicadoresPBI() {
  const empresas = _toObjects('Empresas');
  const mensal = _toObjects('Evolucao_Mensal');
  
  const nc = empresas.filter(e => String(e.status_empresa) === 'Nao Cliente');
  const cl = empresas.filter(e => String(e.status_empresa) === 'Cliente');
  
  // Medidas equivalentes ao Power BI
  const indicadores = {
    // === NÃO CLIENTES ===
    'Qtd. Requisições (Não Clientes)': nc.reduce((s, e) => s + (+e.cadastros || 0), 0),
    'Qtd. CPFs (Não Clientes)': nc.reduce((s, e) => s + (+e.promotores || 0), 0),
    'Empresas Não Clientes': nc.length,
    
    // === CLIENTES ===
    'Qtd. Requisições (Clientes)': cl.reduce((s, e) => s + (+e.cadastros || 0), 0),
    'Qtd. CPFs (Clientes)': cl.reduce((s, e) => s + (+e.promotores || 0), 0),
    'Empresas Clientes': cl.length,
    
    // === TOTAIS ===
    'Total Requisições': empresas.reduce((s, e) => s + (+e.cadastros || 0), 0),
    'Total CPFs Únicos': empresas.reduce((s, e) => s + (+e.promotores || 0), 0),
    'Total Empresas': empresas.length,
    
    // === FINANCEIRO ===
    'Impacto Mensal NC (R$)': nc.reduce((s, e) => s + (+e.promotores || 0), 0) * 12.10,
    
    // === POR TIPO (Agência vs Fornecedor) ===
    'Agências NC': nc.filter(e => e.contratante_tipo === 'Agencia').length,
    'Fornecedores NC': nc.filter(e => e.contratante_tipo === 'Fornecedor').length,
    'CPFs Agências NC': nc.filter(e => e.contratante_tipo === 'Agencia').reduce((s, e) => s + (+e.promotores || 0), 0),
    'CPFs Fornecedores NC': nc.filter(e => e.contratante_tipo === 'Fornecedor').reduce((s, e) => s + (+e.promotores || 0), 0),
    
    // === CLASSIFICAÇÃO DE RISCO ===
    'Críticos (score>80)': empresas.filter(e => (+e.score_suspeita || 0) > 80).length,
    'Alta Suspeita': empresas.filter(e => e.classificacao === 'Alta Suspeita').length,
    'Suspeito': empresas.filter(e => e.classificacao === 'Suspeito').length,
    'Atenção': empresas.filter(e => e.classificacao === 'Atencao').length,
    'Normal': empresas.filter(e => e.classificacao === 'Normal').length,
    
    // === NOTA DE CONFRONTO ===
    '_nota': 'Dados agregados por empresa. PBI tem granularidade por requisição (lite_visitor_id). ' +
             'Breakdown por request_type (Cadastro Promotor/Alocação/Sem efeito) não disponível nesta base. ' +
             'Para equivalência exata com PBI, necessário exportar dados granulares do Redshift.',
    '_fonte_pbi': 'Indicadores de Performance - Cadastro Lite.pbip',
    '_fonte_sheets': SHEETS_ID,
    '_atualizado': new Date().toISOString()
  };
  
  return indicadores;
}

// ── NOVO: Funil de conversão (confrontado com PBI) ────────────────────────────
function getFunil() {
  // Lê da aba README linhas 24-38 onde estão os dados do funil
  const ss = SpreadsheetApp.openById(SHEETS_ID);
  const ws = ss.getSheetByName('README');
  const data = ws.getRange('A24:B38').getValues();
  const funil = [];
  data.forEach(r => {
    if (r[0] && r[0] !== 'Metrica') {
      funil.push({ metrica: String(r[0]).split('(')[0].trim(), valor: r[1] || 0, percentual: '' });
    }
  });
  return funil;
}

// ── NOVO: Breakdown por request_type (confrontado com PBI) ────────────────────
function getBreakdown() {
  return _toObjects('Breakdown_RequestType');
}

// ── NOVO: Status dos promotores (confrontado com PBI) ─────────────────────────
function getStatusPromotores() {
  return _toObjects('Status_Promotores');
}

// ── helpers ───────────────────────────────────────────────────────────────────
function _toObjects(sheetName) {
  const ss = SpreadsheetApp.openById(SHEETS_ID);
  const ws = ss.getSheetByName(sheetName);
  if (!ws) return [];
  const data = ws.getDataRange().getValues();
  if (data.length < 2) return [];
  const headers = data[0].map(String);
  return data.slice(1).map(row => {
    const obj = {};
    headers.forEach((h, i) => { obj[h] = row[i]; });
    return obj;
  });
}
