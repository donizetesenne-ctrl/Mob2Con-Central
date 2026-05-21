/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║  DASHBOARD ANALÍTICO RG 2.0 — GOOGLE APPS SCRIPT                            ║
 * ║  Mob2Con · Maio 2026                                                         ║
 * ║                                                                              ║
 * ║  FUNÇÃO: Servir dados das planilhas Google Sheets para o dashboard HTML     ║
 * ║  MÉTODO: Web App que responde a requisições GET com dados em JSON           ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  CONFIGURAÇÃO — IDs das Planilhas
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

const SHEET_IDS = {
  dimensoes: '1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q',
  fatos:     '1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs',
  lookups:   '1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI'
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  FUNÇÃO PRINCIPAL — doGet (Web App)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function doGet(e) {
  try {
    // Parâmetros da requisição
    const action = e.parameter.action || 'help';
    const sheetId = e.parameter.sheetId || '';
    const sheetName = e.parameter.sheetName || '';
    
    // Log da requisição
    Logger.log(`[doGet] action=${action}, sheetId=${sheetId.substring(0,8)}..., sheetName=${sheetName}`);
    
    // Roteamento
    if (action === 'help') {
      return ContentService.createTextOutput(JSON.stringify({
        status: 'ok',
        message: 'Dashboard Analítico RG 2.0 — Apps Script',
        version: '1.0.0',
        usage: {
          getSheet: '?action=getSheet&sheetId=<ID>&sheetName=<NOME>',
          example: '?action=getSheet&sheetId=1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q&sheetName=dim_rede'
        },
        sheets: SHEET_IDS
      }, null, 2))
      .setMimeType(ContentService.MimeType.JSON);
    }
    
    if (action === 'getSheet') {
      if (!sheetId || !sheetName) {
        return createErrorResponse('Parâmetros obrigatórios: sheetId e sheetName');
      }
      
      const data = getSheetData(sheetId, sheetName);
      
      if (!data || !data.rows || data.rows.length === 0) {
        return createErrorResponse(`Nenhum dado encontrado em ${sheetName}`);
      }
      
      Logger.log(`[doGet] Retornando ${data.rows.length} linhas de ${sheetName}`);
      
      return ContentService.createTextOutput(JSON.stringify(data))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    return createErrorResponse('Ação inválida. Use action=help para ver opções.');
    
  } catch (error) {
    Logger.log(`[doGet] ERRO: ${error.message}`);
    return createErrorResponse(error.message);
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  FUNÇÃO — Buscar Dados da Planilha
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function getSheetData(sheetId, sheetName) {
  try {
    // Abre a planilha
    const spreadsheet = SpreadsheetApp.openById(sheetId);
    const sheet = spreadsheet.getSheetByName(sheetName);
    
    if (!sheet) {
      Logger.log(`[getSheetData] Aba "${sheetName}" não encontrada em ${sheetId}`);
      return { cols: [], rows: [], error: `Aba "${sheetName}" não encontrada` };
    }
    
    // Pega todos os dados
    const range = sheet.getDataRange();
    const values = range.getValues();
    
    if (values.length === 0) {
      Logger.log(`[getSheetData] Aba "${sheetName}" está vazia`);
      return { cols: [], rows: [] };
    }
    
    // Primeira linha = cabeçalhos
    const headers = values[0].map(h => String(h).trim());
    
    // Demais linhas = dados
    const rows = [];
    for (let i = 1; i < values.length; i++) {
      const row = {};
      for (let j = 0; j < headers.length; j++) {
        const header = headers[j];
        const value = values[i][j];
        
        // Converte valores vazios para null
        if (value === '' || value === null || value === undefined) {
          row[header] = null;
        } else {
          row[header] = value;
        }
      }
      rows.push(row);
    }
    
    Logger.log(`[getSheetData] ${sheetName}: ${headers.length} colunas, ${rows.length} linhas`);
    
    return {
      cols: headers,
      rows: rows,
      sheetName: sheetName,
      sheetId: sheetId,
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    Logger.log(`[getSheetData] ERRO: ${error.message}`);
    return {
      cols: [],
      rows: [],
      error: error.message
    };
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  FUNÇÃO — Criar Resposta de Erro
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function createErrorResponse(message) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'error',
    message: message,
    timestamp: new Date().toISOString()
  }))
  .setMimeType(ContentService.MimeType.JSON);
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  FUNÇÃO DE TESTE — Testar Localmente
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function testarAppsScript() {
  Logger.log('=== TESTE DO APPS SCRIPT ===');
  
  // Teste 1: dim_rede
  Logger.log('\n--- Teste 1: dim_rede ---');
  const data1 = getSheetData(SHEET_IDS.dimensoes, 'dim_rede');
  Logger.log(`Colunas: ${data1.cols ? data1.cols.length : 0}`);
  Logger.log(`Linhas: ${data1.rows ? data1.rows.length : 0}`);
  if (data1.error) Logger.log(`ERRO: ${data1.error}`);
  
  // Teste 2: fato_status_promotores
  Logger.log('\n--- Teste 2: fato_status_promotores ---');
  const data2 = getSheetData(SHEET_IDS.fatos, 'fato_status_promotores');
  Logger.log(`Colunas: ${data2.cols ? data2.cols.length : 0}`);
  Logger.log(`Linhas: ${data2.rows ? data2.rows.length : 0}`);
  if (data2.error) Logger.log(`ERRO: ${data2.error}`);
  
  // Teste 3: tbl_scores_redes
  Logger.log('\n--- Teste 3: tbl_scores_redes ---');
  const data3 = getSheetData(SHEET_IDS.lookups, 'tbl_scores_redes');
  Logger.log(`Colunas: ${data3.cols ? data3.cols.length : 0}`);
  Logger.log(`Linhas: ${data3.rows ? data3.rows.length : 0}`);
  if (data3.error) Logger.log(`ERRO: ${data3.error}`);
  
  Logger.log('\n=== FIM DO TESTE ===');
}

/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║  INSTRUÇÕES DE IMPLANTAÇÃO                                                   ║
 * ╠══════════════════════════════════════════════════════════════════════════════╣
 * ║                                                                              ║
 * ║  1. Abra o Google Apps Script Editor:                                       ║
 * ║     https://script.google.com                                                ║
 * ║                                                                              ║
 * ║  2. Crie um novo projeto: "Dashboard Analítico RG 2.0"                      ║
 * ║                                                                              ║
 * ║  3. Cole este código no editor                                               ║
 * ║                                                                              ║
 * ║  4. Teste localmente:                                                        ║
 * ║     - Execute a função: testarAppsScript()                                   ║
 * ║     - Verifique os logs (View → Logs)                                       ║
 * ║                                                                              ║
 * ║  5. Implante como Web App:                                                   ║
 * ║     - Deploy → New deployment                                                ║
 * ║     - Type: Web app                                                          ║
 * ║     - Execute as: Me                                                         ║
 * ║     - Who has access: Anyone                                                 ║
 * ║     - Deploy                                                                 ║
 * ║                                                                              ║
 * ║  6. Copie a URL do Web App                                                   ║
 * ║     Exemplo: https://script.google.com/macros/s/AKfyc.../exec               ║
 * ║                                                                              ║
 * ║  7. Atualize o dashboard HTML com a nova URL                                 ║
 * ║                                                                              ║
 * ║  8. Teste no navegador:                                                      ║
 * ║     https://script.google.com/.../exec?action=help                           ║
 * ║                                                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */
