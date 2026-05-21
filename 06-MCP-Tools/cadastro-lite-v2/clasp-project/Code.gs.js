var SHEETS_ID = '1piHmDHrTdoOS6gFkSVQ3xVH3InBV3CPjndmsPJkuAFU';
var ss_ = null;
function SS_() { if (!ss_) ss_ = SpreadsheetApp.openById(SHEETS_ID); return ss_; }

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Cadastro Lite - Monitoramento Mob2Con')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getKpis() {
  var ws = SS_().getSheetByName('README');
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
  return _toObjects('Redes');
}

function getAcoesCS() {
  var ws = SS_().getSheetByName('Acoes_CS');
  if (!ws) return [];
  return _toObjects('Acoes_CS');
}

function getFunil() { return []; }

function addAcaoCS(dados) {
  var ws = SS_().getSheetByName('Acoes_CS');
  if (!ws) {
    ws = SS_().insertSheet('Acoes_CS');
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
  var ws = SS_().getSheetByName(sheetName);
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
