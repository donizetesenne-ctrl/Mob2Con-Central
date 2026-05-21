var SHEETS_ID = '1piHmDHrTdoOS6gFkSVQ3xVH3InBV3CPjndmsPJkuAFU';

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Cadastro Lite - Monitoramento Mob2Con')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getKpis() {
  var ss = SpreadsheetApp.openById(SHEETS_ID);
  var ws = ss.getSheetByName('README');
  var rows = ws.getDataRange().getValues();
  var kpis = {};
  rows.forEach(function(r) {
    if (r[0] && r[1] !== '') kpis[String(r[0])] = r[1];
  });
  return kpis;
}

function getEmpresas() { return _toObjects('Empresas'); }
function getMensal() { return _toObjects('Evolucao_Mensal'); }
function getConvMensal() { return _toObjects('Conv_Mensal'); }
function getConvencional() { return _toObjects('Convencional'); }
function getCaptacaoRede() { return _toObjects('Captacao_Rede'); }
function getCaptacaoClientes() { return _toObjects('Captacao_Clientes'); }

function getRedes() {
  var redes = _toObjects('Redes');
  var empresas = _toObjects('Empresas');
  var empMap = {};
  empresas.forEach(function(e) { empMap[String(e.empresa_id)] = e.empresa; });
  redes.forEach(function(r) { r.empresa_nome = empMap[String(r.empresa_id)] || 'ID: ' + r.empresa_id; });
  return redes;
}

function getAcoesCS() {
  var ss = SpreadsheetApp.openById(SHEETS_ID);
  var ws = ss.getSheetByName('Acoes_CS');
  if (!ws) return [];
  return _toObjects('Acoes_CS');
}

function addAcaoCS(dados) {
  var ss = SpreadsheetApp.openById(SHEETS_ID);
  var ws = ss.getSheetByName('Acoes_CS');
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

function _toObjects(sheetName) {
  var ss = SpreadsheetApp.openById(SHEETS_ID);
  var ws = ss.getSheetByName(sheetName);
  if (!ws) return [];
  var data = ws.getDataRange().getValues();
  if (data.length < 2) return [];
  var headers = data[0].map(String);
  return data.slice(1).map(function(row) {
    var obj = {};
    headers.forEach(function(h, i) { obj[h] = row[i]; });
    return obj;
  });
}