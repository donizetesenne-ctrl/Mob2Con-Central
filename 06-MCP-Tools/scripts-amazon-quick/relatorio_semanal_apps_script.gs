/**
 * ═══════════════════════════════════════════════════════════════
 * 📊 APPS SCRIPT — GERADOR DE RELATÓRIO HTML SEMANAL
 * ═══════════════════════════════════════════════════════════════
 * 
 * INTEGRAÇÃO COM PYTHON:
 * 1. Python processa Google Docs → gera JSON estruturado
 * 2. JSON é salvo no Drive (pasta Mob2Con - Relatórios Semanais)
 * 3. Este script lê o JSON mais recente
 * 4. Gera HTML formatado igual ao modelo
 * 5. Envia por email para gestora
 * 
 * SETUP:
 * 1. Abra qualquer Google Sheets
 * 2. Extensions → Apps Script
 * 3. Cole este código
 * 4. Preencha CONFIG abaixo
 * 5. Execute gerarRelatorioSemanal() uma vez para autorizar
 * 6. Triggers → + → gerarRelatorioSemanal → Semanal → Sexta → 17:00-18:00
 */

// ═══════════════════════════════════════════════════════════════
// CONFIGURAÇÃO
// ═══════════════════════════════════════════════════════════════

const CONFIG = {
  FOLDER_ID: '1sc90vFM_Jghjlv0p7LCuePqrwfUFhQlt',  // Pasta Drive (Relatórios Gerados)
  EMAIL_GESTORA: 'mariliana.fagotti@mob2con.com.br',
  NOME_GESTORA: 'Mariliana Fagotti',
  EMPRESA: 'Mob2Con',
  RESPONSAVEL: 'Donizete Senne',
  
  // Webhook Google Chat (opcional)
  WEBHOOK_CHAT: '',  // Se quiser notificar no Chat também
  
  // Modo debug
  DEBUG: false
};

// ═══════════════════════════════════════════════════════════════
// BUSCAR JSON MAIS RECENTE
// ═══════════════════════════════════════════════════════════════

function buscarJsonMaisRecente_() {
  try {
    const pasta = DriveApp.getFolderById(CONFIG.FOLDER_ID);
    const arquivos = pasta.getFilesByType(MimeType.PLAIN_TEXT);
    
    let maisRecente = null;
    let dataRecente = new Date(0);
    
    while (arquivos.hasNext()) {
      const arquivo = arquivos.next();
      if (arquivo.getName().startsWith('relatorio_dados_') && arquivo.getName().endsWith('.json')) {
        const dataArquivo = arquivo.getLastUpdated();
        if (dataArquivo > dataRecente) {
          dataRecente = dataArquivo;
          maisRecente = arquivo;
        }
      }
    }
    
    if (!maisRecente) {
      throw new Error('Nenhum JSON de relatório encontrado na pasta');
    }
    
    Logger.log('✅ JSON encontrado: ' + maisRecente.getName());
    
    const conteudo = maisRecente.getBlob().getDataAsString();
    return JSON.parse(conteudo);
    
  } catch (e) {
    Logger.log('❌ Erro ao buscar JSON: ' + e.message);
    throw e;
  }
}

// ═══════════════════════════════════════════════════════════════
// GERAÇÃO DO HTML
// ═══════════════════════════════════════════════════════════════

function gerarHTML_(dados) {
  const meta = dados.metadata;
  const registros = dados.registros || [];
  const porCategoria = dados.por_categoria || {};
  const pendencias = dados.pendencias || [];
  const config = dados.config || {};
  const cores = config.cores || {};
  const icones = config.icones || {};
  
  const fmt = (d) => Utilities.formatDate(new Date(d), 'America/Sao_Paulo', 'dd/MM');
  const periodo = `${fmt(meta.periodo_inicio)} – ${fmt(meta.periodo_fim)}`;
  
  // Agrupar registros por categoria
  const registrosPorCat = {};
  registros.forEach(r => {
    if (!registrosPorCat[r.categoria]) registrosPorCat[r.categoria] = [];
    registrosPorCat[r.categoria].push(r);
  });
  
  // TIMELINE HTML
  let timelineHTML = '';
  Object.entries(registrosPorCat).forEach(([cat, items]) => {
    const cor = cores[cat] || '#605E5C';
    const icone = icones[cat] || '📋';
    
    items.forEach(item => {
      const tags = (item.tags || []).map(t => 
        `<span style="font-size:11px;padding:2px 8px;border-radius:100px;font-weight:600;border:1px solid ${cor};color:${cor}">${t}</span>`
      ).join(' ');
      
      const statusCor = item.status === 'Concluído' ? '#D1FAE5' : '#FEF3C7';
      const statusTexto = item.status === 'Concluído' ? '#065F46' : '#92400E';
      
      timelineHTML += `
      <div style="display:flex;gap:16px;margin-bottom:14px;padding-left:50px;position:relative;">
        <div style="position:absolute;left:10px;top:10px;width:22px;height:22px;border-radius:50%;background:${cor};display:flex;align-items:center;justify-content:center;font-size:11px;">${icone}</div>
        <div style="flex:1;background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:14px 18px;transition:box-shadow .2s,transform .2s;">
          <span style="font-size:11px;font-weight:700;padding:2px 8px;border-radius:100px;background:${cor}15;color:${cor}">${fmt(item.data)} — ${cat}</span>
          <h3 style="font-size:14px;font-weight:700;margin:6px 0 4px;">${item.titulo}</h3>
          <p style="font-size:12px;color:#605E5C;line-height:1.6;">${item.descricao}</p>
          ${tags ? `<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;">${tags}</div>` : ''}
          <span style="font-size:10px;padding:2px 8px;border-radius:4px;background:${statusCor};color:${statusTexto};font-weight:600;margin-top:6px;display:inline-block;">${item.status}</span>
        </div>
      </div>`;
    });
  });
  
  // CARDS RESUMO
  let cardsHTML = '';
  Object.entries(porCategoria).forEach(([cat, count]) => {
    const cor = cores[cat] || '#605E5C';
    const icone = icones[cat] || '📋';
    cardsHTML += `
    <div style="background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:16px;text-align:center;border-top:4px solid ${cor}">
      <div style="font-size:24px;margin-bottom:4px;">${icone}</div>
      <div style="font-size:20px;font-weight:800;color:${cor}">${count}</div>
      <div style="font-size:11px;color:#605E5C;font-weight:600;">${cat}</div>
    </div>`;
  });
  
  // PENDÊNCIAS
  let pendenciasHTML = '';
  if (pendencias.length > 0) {
    pendenciasHTML = `
    <div style="background:#FFF9F0;border:1px solid #F2C811;border-radius:12px;padding:16px 20px;margin-top:20px;">
      <h4 style="font-size:13px;font-weight:700;color:#856404;margin-bottom:10px;display:flex;align-items:center;gap:8px;">
        <i class="fa-solid fa-triangle-exclamation"></i> Pendências / Em Andamento
      </h4>
      ${pendencias.map(p => `
        <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #fde68a;font-size:12px;">
          <span style="background:${cores[p.categoria] || '#605E5C'};color:#fff;padding:3px 10px;border-radius:100px;font-size:11px;font-weight:700;">${p.categoria}</span>
          <span style="color:#78350F"><strong>${p.titulo}</strong> — ${p.descricao}</span>
        </div>
      `).join('')}
    </div>`;
  }
  
  // HTML COMPLETO
  return `<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Relatório Semanal — ${CONFIG.EMPRESA} ${periodo}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800&display=swap');
:root{--mob-laranja:#F46901;--mob-grafite:#434343;--mob-preto:#111111;--mob-roxo:#6F05D4;--mob-azul:#4285F4;--mob-verde:#107C41;--mob-bg:#F3F6FA;--mob-surface:#ffffff;--mob-border:#E2E8F0;--mob-text:#323130;--mob-text-muted:#605E5C;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Raleway',sans-serif;background:var(--mob-bg);color:var(--mob-text);padding:24px;min-height:100vh;}
</style></head><body>

<!-- HEADER -->
<div style="background:linear-gradient(135deg,#111 0%,#2d2d2d 100%);border-radius:16px;padding:28px 32px;margin-bottom:24px;display:flex;justify-content:space-between;align-items:center;border-left:6px solid #F46901;flex-wrap:wrap;gap:16px;">
  <div>
    <h1 style="color:#fff;font-size:22px;font-weight:800;">Relatório Semanal de Produção <span style="color:#F46901">${CONFIG.EMPRESA}</span></h1>
    <p style="color:#aaa;font-size:13px;margin-top:4px;">Período: ${periodo} &nbsp;|&nbsp; Responsável: ${CONFIG.RESPONSAVEL}</p>
  </div>
  <div style="background:#F46901;color:#fff;padding:8px 20px;border-radius:100px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:8px;">
    <i class="fa-solid fa-check-double"></i> ${meta.concluidos}/${meta.total_registros} Concluídos
  </div>
</div>

<!-- RESUMO POR CATEGORIA -->
<p style="font-size:13px;font-weight:700;color:#605E5C;text-transform:uppercase;letter-spacing:.1em;margin-bottom:16px;display:flex;align-items:center;gap:8px;">
  <i class="fa-solid fa-chart-pie"></i> Resumo por Categoria
</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:24px;">
  ${cardsHTML}
</div>

<!-- TIMELINE -->
<p style="font-size:13px;font-weight:700;color:#605E5C;text-transform:uppercase;letter-spacing:.1em;margin-bottom:16px;display:flex;align-items:center;gap:8px;">
  <i class="fa-solid fa-clock-rotate-left"></i> Entregas da Semana
</p>
<div style="position:relative;margin-bottom:32px;">
  <div style="position:absolute;left:20px;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,#F46901,#6F05D4,#4285F4);border-radius:4px;"></div>
  ${timelineHTML}
</div>

${pendenciasHTML}

<!-- FOOTER -->
<div style="text-align:center;padding:20px;color:#605E5C;font-size:12px;border-top:1px solid #E2E8F0;margin-top:24px;">
  Gerado automaticamente em ${Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm')} &nbsp;|&nbsp; 
  <span style="color:#F46901;font-weight:700;">${CONFIG.EMPRESA}</span> &nbsp;|&nbsp; ${CONFIG.RESPONSAVEL} &nbsp;|&nbsp;
  <i class="fa-solid fa-robot"></i> Python + Apps Script
</div>

</body></html>`;
}

// ═══════════════════════════════════════════════════════════════
// FUNÇÃO PRINCIPAL
// ═══════════════════════════════════════════════════════════════

function gerarRelatorioSemanal() {
  try {
    Logger.log('═══════════════════════════════════════════════════════════════');
    Logger.log('📊 GERADOR DE RELATÓRIO SEMANAL — Mob2Con');
    Logger.log('═══════════════════════════════════════════════════════════════');
    
    // 1. Buscar JSON
    Logger.log('🔍 Buscando JSON mais recente...');
    const dados = buscarJsonMaisRecente_();
    
    if (!dados || !dados.registros || dados.registros.length === 0) {
      Logger.log('⚠️ Nenhum registro encontrado. Relatório não gerado.');
      return;
    }
    
    Logger.log(`✅ ${dados.metadata.total_registros} registros encontrados`);
    
    // 2. Gerar HTML
    Logger.log('🎨 Gerando HTML...');
    const html = gerarHTML_(dados);
    
    // 3. Salvar no Drive
    const hoje = new Date();
    const nomeArquivo = `Relatorio_Semanal_${Utilities.formatDate(hoje, 'America/Sao_Paulo', 'yyyy-MM-dd')}.html`;
    
    const pasta = DriveApp.getFolderById(CONFIG.FOLDER_ID);
    const arquivo = pasta.createFile(nomeArquivo, html, MimeType.HTML);
    Logger.log('💾 HTML salvo: ' + arquivo.getUrl());
    
    // 4. Enviar email
    if (!CONFIG.EMAIL_GESTORA || CONFIG.EMAIL_GESTORA === 'gestora@empresa.com') {
      Logger.log('⚠️ EMAIL_GESTORA não configurado. Relatório salvo mas não enviado.');
      Logger.log('   Configure CONFIG.EMAIL_GESTORA no início do script.');
      return;
    }
    
    const meta = dados.metadata;
    const fmt = (d) => Utilities.formatDate(new Date(d), 'America/Sao_Paulo', 'dd/MM');
    const periodo = `${fmt(meta.periodo_inicio)} – ${fmt(meta.periodo_fim)}`;
    
    const assunto = `📊 Relatório Semanal ${CONFIG.EMPRESA} — ${periodo} (${meta.total_registros} entregas)`;
    
    MailApp.sendEmail({
      to: CONFIG.EMAIL_GESTORA,
      subject: assunto,
      htmlBody: html,
      name: CONFIG.RESPONSAVEL,
      attachments: [arquivo.getAs(MimeType.HTML)]
    });
    
    Logger.log('✅ Email enviado para: ' + CONFIG.EMAIL_GESTORA);
    
    // 5. Notificar no Google Chat (opcional)
    if (CONFIG.WEBHOOK_CHAT) {
      notificarChat_(dados);
    }
    
    Logger.log('═══════════════════════════════════════════════════════════════');
    Logger.log('✅ RELATÓRIO GERADO E ENVIADO COM SUCESSO');
    Logger.log('═══════════════════════════════════════════════════════════════');
    
  } catch (e) {
    Logger.log('❌ ERRO: ' + e.message);
    Logger.log(e.stack);
    
    // Enviar email de erro
    if (CONFIG.EMAIL_GESTORA && CONFIG.EMAIL_GESTORA !== 'gestora@empresa.com') {
      MailApp.sendEmail({
        to: CONFIG.EMAIL_GESTORA,
        subject: '❌ Erro ao gerar relatório semanal',
        body: `Erro ao processar relatório:\n\n${e.message}\n\n${e.stack}`
      });
    }
  }
}

// ═══════════════════════════════════════════════════════════════
// NOTIFICAÇÃO GOOGLE CHAT (OPCIONAL)
// ═══════════════════════════════════════════════════════════════

function notificarChat_(dados) {
  if (!CONFIG.WEBHOOK_CHAT) return;
  
  try {
    const meta = dados.metadata;
    const fmt = (d) => Utilities.formatDate(new Date(d), 'America/Sao_Paulo', 'dd/MM');
    const periodo = `${fmt(meta.periodo_inicio)} – ${fmt(meta.periodo_fim)}`;
    
    const mensagem = {
      text: `📊 *Relatório Semanal ${CONFIG.EMPRESA}*\n\n` +
            `📅 Período: ${periodo}\n` +
            `✅ Concluídos: ${meta.concluidos}/${meta.total_registros}\n` +
            `⏳ Pendentes: ${meta.pendentes}\n\n` +
            `Enviado para: ${CONFIG.NOME_GESTORA}`
    };
    
    UrlFetchApp.fetch(CONFIG.WEBHOOK_CHAT, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(mensagem)
    });
    
    Logger.log('✅ Notificação enviada ao Google Chat');
  } catch (e) {
    Logger.log('⚠️ Erro ao notificar Chat: ' + e.message);
  }
}

// ═══════════════════════════════════════════════════════════════
// MENU CUSTOMIZADO (se usar com Sheets)
// ═══════════════════════════════════════════════════════════════

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('📊 Relatório Mob2Con')
    .addItem('Gerar e Enviar Agora', 'gerarRelatorioSemanal')
    .addItem('Testar Busca JSON', 'testarBuscaJSON')
    .addToUi();
}

function testarBuscaJSON() {
  try {
    const dados = buscarJsonMaisRecente_();
    Logger.log('✅ JSON encontrado e parseado com sucesso');
    Logger.log('Total de registros: ' + dados.metadata.total_registros);
    SpreadsheetApp.getUi().alert('✅ JSON encontrado!\n\nTotal: ' + dados.metadata.total_registros + ' registros');
  } catch (e) {
    Logger.log('❌ Erro: ' + e.message);
    SpreadsheetApp.getUi().alert('❌ Erro ao buscar JSON:\n\n' + e.message);
  }
}
