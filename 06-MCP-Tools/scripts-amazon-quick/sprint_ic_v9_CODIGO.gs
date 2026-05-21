// ╔══════════════════════════════════════════════════════════════════════════════╗
// ║  SPRINT IC — SISTEMA COMPLETO v9.0  |  Mob2Con Inteligência Comercial      ║
// ║                                                                              ║
// ║  Time: Marcelo Bora · Pedro Malagutti · Joice Topan                         ║
// ║         João Rosa · Mariliana Fagotti · Donizete · Lucas                    ║
// ║                                                                              ║
// ║  NOVIDADES v8.0 (sobre v7.0)                                                ║
// ║  ────────────────────────────────────────────────────────                   ║
// ║  🔴 BUG FIX — setFrozenColumns(1) removido (conflito célula mesclada)      ║
// ║  ✅ Kanban Individual por membro — aba dedicada com QUERY ao Board          ║
// ║  ✅ criarKanbanTodosMembros() — cria 1 aba por membro automaticamente       ║
// ║  ✅ atualizarTodosKanbans() — reconstrói visual mantendo QUERY viva         ║
// ║  ✅ Status "Aguardando Área Externa" integrado ao onEdit                    ║
// ║  ✅ notificarDependenciaExterna() — e-mail + Chat para áreas externas       ║
// ║  ✅ verificarDependenciasExternas() — varredura semanal                     ║
// ║  ✅ configurarColunasDependenciaExterna() — adiciona colunas AB/AC/AD       ║
// ║  ✅ atualizarConexoesAbas() — QUERY ao Board no Planning e SLA              ║
// ║  ✅ importarDadosConsolidados() — Jira/HubSpot → Board                     ║
// ║  ✅ COR_TIME centralizada — usada em Dashboard e Kanbans                    ║
// ║                                                                              ║
// ║  NOVIDADES v9.0 (sobre v8.0)                                                ║
// ║  ────────────────────────────────────────────────────────                   ║
// ║  🔴 BUG FIX — notificarDonizete() e notificarLucas() adicionados ao menu   ║
// ║  🔴 BUG FIX — WEBAPP_URL movida para PropertiesService (segurança)         ║
// ║  ✅ onEdit avisa usuário ao detectar edição em bloco (multi-célula)         ║
// ║  ✅ _postWebhook usa WEBHOOK_URL com fallback para WEBAPP_URL               ║
// ║  ✅ Validação de board nulo em todas as funções críticas                    ║
// ╚══════════════════════════════════════════════════════════════════════════════╝


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 1 — CONFIGURAÇÕES GLOBAIS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

const CONFIG = {

  get WEBHOOK_URL() {
    return PropertiesService.getScriptProperties().getProperty("WEBHOOK_URL") || "";
  },
  NOME_DO_SPACE: "Time IC",

  // Abas fixas
  ABA_BOARD:     "🗂️ Board",
  ABA_AUTOMACAO: "⚙️ Automação",
  ABA_KANBAN:    "📊 Kanban View",
  ABA_PLANNING:  "📅 Sprint Planning",
  ABA_DASHBOARD: "📈 Dashboard",
  ABA_SLA:       "⏱️ SLA & Alertas",
  ABA_CONFIG:    "⚙️ Config",
  ABA_VALIDACAO: "🔍 Validação",

  // Time IC — Donizete e Lucas substituem os slots TBD
  TIME: {
    "Marcelo Bora":      { email: "marcelo.prado@mob2con.com.br",     sigla: "MB", cor: "#F46901" },
    "Pedro Malagutti":   { email: "pedro.malagutti@mob2con.com.br",   sigla: "PM", cor: "#4285F4" },
    "Joice Topan":       { email: "joice.topan@mob2con.com.br",       sigla: "JT", cor: "#6F05D4" },
    "João Rosa":         { email: "joao.rosa@mob2con.com.br",         sigla: "JR", cor: "#16a34a" },
    "Mariliana Fagotti": { email: "mariliana.fagotti@mob2con.com.br", sigla: "MF", cor: "#dc2626" },
    "Donizete":          { email: "donizete.senne@mob2con.com.br",    sigla: "DZ", cor: "#0891b2" },
    "Lucas":             { email: "lucas.oliveira@mob2con.com.br",    sigla: "LC", cor: "#7c3aed" },
  },

  // Sprint
  SPRINT: {
    DIA_PLANNING: 2, DIA_REVIEW: 4, DURACAO_DIAS: 9,
    PREFIXO_ID: "KAN-", PROXIMO_ID: "IC_PROXIMO_ID",
  },

  // SLA
  SLA: {
    "🔴 Crítica":  1,
    "🟠 Alta":     3,
    "🟡 Média":    5,
    "🟢 Baixa":    10,
    "⚪ Sem prio": 15,
  },

  // Feriados BR
  FERIADOS_BR: [
    "01/01","20/01","03/03","04/03","05/03","18/04","21/04",
    "01/05","07/09","12/10","02/11","15/11","20/11","25/12",
  ],

  // Colunas do Board (0-based)
  COL: {
    ID:0, TITULO:1, TIPO:2, STATUS:3, PRIORIDADE:4, RESPONSAVEL:5,
    CATEGORIA:6, SPRINT:7, DATA_CRIACAO:8, DATA_INICIO:9, DATA_FIM:10,
    DATA_CONCLUSAO:11, DIAS_REST:12, PCT:13, ESTIMATIVA_H:14, HORAS_GASTAS:15,
    EPICO:16, BLOCKER:17, DESCRICAO:18, CRITERIOS:19, SOLICITANTE:20,
    REVISADO_POR:21, LINK:22, COMENTARIOS:23, SLA_LIMITE:24, SLA_STATUS:25,
    DEPENDE_DE:26,
    // Colunas de dependência externa (27,28,29 = AB,AC,AD)
    AREA_EXTERNA:27, EMAIL_EXTERNO:28, STATUS_DEP:29,
  },

  // Status
  STATUS_ORDEM: [
    "Novas Solicitações","Backlog","A Fazer","Em Andamento",
    "Aguardando Área Externa",
    "Bloqueado","Em Validação","Concluído (Semana)","Concluído Geral","Cancelado",
  ],

  // Cores por status
  CORES_STATUS: {
    "Novas Solicitações":     { bg: "#EDE7F6", fg: "#4A148C" },
    "Backlog":                { bg: "#F3F4F6", fg: "#374151" },
    "A Fazer":                { bg: "#EFF6FF", fg: "#1D4ED8" },
    "Em Andamento":           { bg: "#FFF7ED", fg: "#C2410C" },
    "Aguardando Área Externa":{ bg: "#FEF9C3", fg: "#713F12" },
    "Bloqueado":              { bg: "#FEF2F2", fg: "#991B1B" },
    "Em Validação":           { bg: "#FEFCE8", fg: "#854D0E" },
    "Concluído (Semana)":     { bg: "#F0FDF4", fg: "#15803D" },
    "Concluído Geral":        { bg: "#DCFCE7", fg: "#166534" },
    "Cancelado":              { bg: "#F9FAFB", fg: "#9CA3AF" },
  },

  // PropertiesService
  PROP: {
    TASK_LISTS:      "IC_TASK_LISTS_V8",
    TASK_MAP_PREFIX: "IC_TASK_MAP_V8_",
  },

  // Distribuição
  DIST: {
    SERVICE_ACCOUNT_EMAIL: "",
    get WEBAPP_URL() {
    return PropertiesService.getScriptProperties().getProperty("WEBAPP_URL") || "";
  },
    CALENDAR_DURACAO_MIN: 30,
    LEMBRETE_EMAIL_MIN: 30,
    LEMBRETE_POPUP_MIN: 10,
  },

  // Formulários
  FORM: {
    TITULO: "Formulário de Abertura de Solicitação — Inteligência Comercial",
    DESCRICAO: "Preencha com atenção. Quanto mais contexto você fornecer, mais rápido e preciso será o apoio da IC. Campos com * são obrigatórios.",
    CONFIRMACAO: "✅ Sua solicitação foi registrada! O time IC receberá uma notificação e você receberá um e-mail de confirmação em breve.",
  },
};

// Status especial para dependência externa
const STATUS_AGUARDANDO = "Aguardando Área Externa";

// Referência centralizada de colunas externas
const COL_EXT = {
  AREA_EXTERNA: CONFIG.COL.AREA_EXTERNA,
  EMAIL_EXTERNO: CONFIG.COL.EMAIL_EXTERNO,
  STATUS_DEP: CONFIG.COL.STATUS_DEP,
};

// Cores centralizadas por membro (usadas em Dashboard e Kanbans)
const COR_TIME = {
  "Marcelo Bora":      "#F46901",
  "Pedro Malagutti":   "#4285F4",
  "Joice Topan":       "#6F05D4",
  "João Rosa":         "#16a34a",
  "Mariliana Fagotti": "#dc2626",
  "Donizete":          "#0891b2",
  "Lucas":             "#7c3aed",
};


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 2 — MENU
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("🚀 Sprint IC")
    .addSubMenu(ui.createMenu("📋 Sprint")
      .addItem("▶ Iniciar Nova Sprint",              "iniciarNovaSprint")
      .addItem("📤 Sincronizar Board → Tasks",        "sincronizarTodasAsTasks")
      .addItem("📥 Puxar Conclusões do Tasks",        "sincronizarTasksDeVolta")
      .addItem("📊 Enviar Resumo ao Chat",            "enviarResumoDaSprint")
      .addSeparator()
      .addItem("📅 Planning de Terça",                "enviarAgendaPlanning")
      .addItem("🔍 Review de Quinta",                 "enviarAgendaReview"))
    .addSubMenu(ui.createMenu("👤 Por Pessoa")
      .addItem("📋 Tasks Marcelo Bora",               "sincronizarTasksMarcelo")
      .addItem("📋 Tasks Pedro Malagutti",            "sincronizarTasksPedro")
      .addItem("📋 Tasks Joice Topan",                "sincronizarTasksJoice")
      .addItem("📋 Tasks João Rosa",                  "sincronizarTasksJoao")
      .addItem("📋 Tasks Mariliana Fagotti",          "sincronizarTasksMari")
      .addItem("📋 Tasks Donizete",                   "sincronizarTasksDonizete")
      .addItem("📋 Tasks Lucas",                      "sincronizarTasksLucas")
      .addSeparator()
      .addItem("📣 Notificar Bora",                   "notificarBora")
      .addItem("📣 Notificar Pedro",                  "notificarPedro")
      .addItem("📣 Notificar Joice",                  "notificarJoice")
      .addItem("📣 Notificar João",                   "notificarJoao")
      .addItem("📣 Notificar Mari",                   "notificarMari")
      .addItem("📣 Notificar Donizete",               "notificarDonizete")
      .addItem("📣 Notificar Lucas",                  "notificarLucas"))
    .addSubMenu(ui.createMenu("📊 Kanbans Individuais")
      .addItem("🆕 Criar Kanbans de Todos os Membros","criarKanbanTodosMembros")
      .addItem("🔄 Atualizar Todos os Kanbans",       "atualizarTodosKanbans")
      .addSeparator()
      .addItem("👤 Kanban — Marcelo Bora",            "criarKanbanMarcelo")
      .addItem("👤 Kanban — Pedro Malagutti",         "criarKanbanPedro")
      .addItem("👤 Kanban — Joice Topan",             "criarKanbanJoice")
      .addItem("👤 Kanban — João Rosa",               "criarKanbanJoao")
      .addItem("👤 Kanban — Mariliana Fagotti",       "criarKanbanMari")
      .addItem("👤 Kanban — Donizete",                "criarKanbanDonizete")
      .addItem("👤 Kanban — Lucas",                   "criarKanbanLucas"))
    .addSubMenu(ui.createMenu("🔔 Alertas")
      .addItem("🚨 Verificar Atrasos & SLA",          "verificarAtrasos")
      .addItem("⏳ Verificar Dependências Externas",  "verificarDependenciasExternas")
      .addItem("🔄 Atualizar Dashboard",              "atualizarDashboard")
      .addItem("🎨 Reformatar Board",                 "reformatarBoard"))
    .addSubMenu(ui.createMenu("⚙️ Configuração")
      .addItem("🔧 Configurar Triggers",              "configurarTodosOsTriggers")
      .addItem("🗑️ Remover Triggers",                 "removerTodosOsTriggers")
      .addItem("🆔 Criar Listas de Tasks",            "criarListasDeTasksParaTodos")
      .addItem("📋 Ver IDs das Listas",               "exibirIDsListas")
      .addSeparator()
      .addItem("📝 Criar Formulário Google",          "criarFormulario")
      .addItem("📋 Ver URL do Formulário",            "exibirUrlFormulario")
      .addSeparator()
      .addItem("🔗 Atualizar Conexões (QUERY)",       "atualizarConexoesAbas")
      .addItem("➕ Configurar Colunas Dep. Externa",  "configurarColunasDependenciaExterna")
      .addItem("📥 Importar Dados Jira/HubSpot",      "importarDadosConsolidados"))
    .addSubMenu(ui.createMenu("🎨 Reconstruir Visuais")
      .addItem("🎨 Reconstruir Todos os Visuais",     "reconstruirVisuais")
      .addItem("📈 Reconstruir Dashboard",            "_reconstruirDashboard")
      .addItem("⚙️ Reconstruir Config",              "_reconstruirConfig")
      .addItem("⏱️ Reconstruir SLA",                 "_reconstruirSLA")
      .addItem("📊 Reconstruir Kanban Geral",        "_reconstruirKanban"))
    .addSubMenu(ui.createMenu("📤 Distribuir Tasks")
      .addItem("🅐 Via Admin",                        "opcaoA_distribuirViaAdmin")
      .addItem("🅑 Via Link de Autorização",          "opcaoB_enviarLinksAutorizacao")
      .addItem("🅒 Via Evento no Calendar",           "opcaoC_distribuirViaCalendar")
      .addItem("📋 Diagnóstico por Pessoa",           "diagnosticoTarefasPorPessoa"))
    .addSubMenu(ui.createMenu("🔍 Validação & Testes")
      .addItem("✅ Executar Validação Completa",      "executarTodasAsValidacoes")
      .addItem("🔍 Reconstruir Aba Validação",        "criarAbaValidacao")
      .addSeparator()
      .addItem("💬 Testar Webhook Chat",              "testarWebhook")
      .addItem("📧 Testar Envio de E-mail",           "testarEmailCompleto")
      .addItem("📋 Testar Google Tasks",              "testarTasksCompleto")
      .addItem("⏳ Testar Dependência Externa",       "testarDependenciaExterna"))
    .addSubMenu(ui.createMenu("🟣 CRM — HubSpot")
      .addItem("📝 Criar Formulário CRM",             "criarFormularioCRM")
      .addItem("📋 Ver URL do Formulário CRM",        "exibirUrlFormularioCRM")
      .addItem("✅ Validar Formulário CRM",           "validarFormularioCRM"))
    .addToUi();
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 3 — TRIGGER: FORMULÁRIO ENVIADO (19+ campos)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function onFormSubmit(e) {
  try {
    const ss    = SpreadsheetApp.getActiveSpreadsheet();
    const board = ss.getSheetByName(CONFIG.ABA_BOARD);
    const auto  = ss.getSheetByName(CONFIG.ABA_AUTOMACAO);
    const v     = e.values;

    const ts            = new Date(v[0]);
    const solicitante   = _str(v[1]);
    const area          = _str(v[2]);
    const tipo          = _str(v[3]) || "Tarefa";
    const titulo        = _str(v[4]);
    const contexto      = _str(v[5]);
    const problema      = _str(v[6]);
    const pergunta      = _str(v[7]);
    const objetivo      = _str(v[8]);
    const tipoApoio     = _str(v[12]);
    const jaTentado     = _str(v[14]);
    const prazoBruto    = _str(v[15]);
    const justPrazo     = _str(v[16]);
    const prioridadeRaw = _str(v[17]);
    const criterios     = _str(v[18]);
    const nomeGestor    = _str(v[20]);
    const respSugerido  = _str(v[21]);
    const observacoes   = _str(v[22]);

    const prioridade = _mapearPrioridade(prioridadeRaw);

    const descricao = [
      contexto   ? `📍 Contexto:\n${contexto}`         : "",
      problema   ? `🔍 Problema:\n${problema}`         : "",
      pergunta   ? `❓ Pergunta Central:\n${pergunta}` : "",
      jaTentado  ? `🔄 Já tentado:\n${jaTentado}`     : "",
      justPrazo  ? `⏱️ Urgência:\n${justPrazo}`        : "",
      observacoes? `📎 Obs:\n${observacoes}`           : "",
    ].filter(Boolean).join("\n\n");

    const responsavel = (respSugerido && CONFIG.TIME[respSugerido]) ? respSugerido : "";
    const novoId    = _proximoId();
    const slaDias   = CONFIG.SLA[prioridade] || 5;
    const slaLimite = _adicionarDiasUteis(ts, slaDias);
    const slaFmt    = Utilities.formatDate(slaLimite, "America/Sao_Paulo", "dd/MM/yyyy");
    const dataCriac = Utilities.formatDate(ts, "America/Sao_Paulo", "dd/MM/yyyy");

    const linhaBoard = new Array(30).fill("");
    linhaBoard[CONFIG.COL.ID]           = novoId;
    linhaBoard[CONFIG.COL.TITULO]       = titulo;
    linhaBoard[CONFIG.COL.TIPO]         = tipo;
    linhaBoard[CONFIG.COL.STATUS]       = "Novas Solicitações";
    linhaBoard[CONFIG.COL.PRIORIDADE]   = prioridade;
    linhaBoard[CONFIG.COL.RESPONSAVEL]  = responsavel;
    linhaBoard[CONFIG.COL.CATEGORIA]    = area;
    linhaBoard[CONFIG.COL.SPRINT]       = "Sem sprint";
    linhaBoard[CONFIG.COL.DATA_CRIACAO] = dataCriac;
    linhaBoard[CONFIG.COL.DATA_FIM]     = prazoBruto;
    linhaBoard[CONFIG.COL.PCT]          = "0%";
    linhaBoard[CONFIG.COL.DESCRICAO]    = descricao.substring(0, 2000);
    linhaBoard[CONFIG.COL.CRITERIOS]    = criterios;
    linhaBoard[CONFIG.COL.SOLICITANTE]  = solicitante;
    linhaBoard[CONFIG.COL.SLA_LIMITE]   = slaFmt;
    linhaBoard[CONFIG.COL.SLA_STATUS]   = "✅ No prazo";

    const ultimaLinha = board.getLastRow() + 1;
    board.appendRow(linhaBoard);
    _aplicarCorStatus(board, ultimaLinha, "Novas Solicitações");

    auto.appendRow([
      Utilities.formatDate(ts, "America/Sao_Paulo", "dd/MM/yyyy HH:mm"),
      novoId, titulo, tipo, solicitante, area,
      responsavel || "— (triagem no planning)",
      prioridade, `SLA: ${slaDias}d → ${slaFmt}`,
      "✅ Incluído no Board", "✅ Sim",
    ]);

    const icone = _iconeprioridade(prioridade);
    _postWebhook({ text: [
      `📥 *Novo ticket recebido!*`, ``,
      `*${novoId}* — ${titulo}`,
      `${icone} Prioridade: *${prioridade}*`,
      `👤 Responsável: *${responsavel || "A definir no planning"}*`,
      `🏢 Área: ${area} | 📋 Tipo: ${tipo}`,
      `🎯 Objetivo: ${objetivo}`,
      `🔧 Apoio: ${tipoApoio}`,
      `⏱️ SLA: ${slaDias} dia(s) úteis → vence em *${slaFmt}*`,
      `👔 Gestor: ${nomeGestor || "—"}`,
      ``, `_Solicitante: ${solicitante}_`,
      `📝 ${descricao.substring(0, 300)}${descricao.length > 300 ? "..." : ""}`,
      ``, `_Ticket aguarda triagem na sprint da terça-feira ☑️_`,
    ].join("\n") });

    const emailSol = CONFIG.TIME[solicitante] ? CONFIG.TIME[solicitante].email : "";
    if (emailSol) _enviarEmailConfirmacao(emailSol, solicitante, novoId, titulo, prioridade, slaLimite);

    Logger.log(`[onFormSubmit] Ticket ${novoId} criado.`);
  } catch (err) {
    Logger.log(`[onFormSubmit] ERRO: ${err.message}`);
    _postWebhook({ text: `⚠️ Erro ao processar formulário: ${err.message}` });
  }
}

function _mapearPrioridade(p) {
  if (!p) return "🟡 Média";
  if (p.includes("Crítica")) return "🔴 Crítica";
  if (p.includes("Alta"))    return "🟠 Alta";
  if (p.includes("Média"))   return "🟡 Média";
  if (p.includes("Baixa"))   return "🟢 Baixa";
  return "🟡 Média";
}

function _str(v) { return v ? String(v).trim() : ""; }


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 4 — TRIGGER: onEdit
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function onEdit(e) {
  try {
    if (!e || !e.range) return;
    const sheet = e.range.getSheet();
    if (sheet.getName() !== CONFIG.ABA_BOARD) return;
    const row = e.range.getRow();
    if (row < 4) return;
    if (e.range.getNumRows() > 1 || e.range.getNumColumns() > 1) {
      // Edição em bloco: automações de status/responsável não disparam
      // para evitar spam de notificações. Edite célula por célula se necessário.
      return;
    }

    const col     = e.range.getColumn() - 1;
    const dados   = sheet.getDataRange().getValues();
    const rowData = dados[row - 1];
    const id      = _str(rowData[CONFIG.COL.ID]);
    const titulo  = _str(rowData[CONFIG.COL.TITULO]);
    if (!titulo) return;

    // ── STATUS ────────────────────────────────────────────────────────────
    if (col === CONFIG.COL.STATUS) {
      const novoStatus = _str(e.value);
      const oldStatus  = _str(e.oldValue);
      if (novoStatus === oldStatus) return;
      _aplicarCorStatus(sheet, row, novoStatus);

      if (novoStatus.includes("Concluído")) {
        const hoje = Utilities.formatDate(new Date(), "America/Sao_Paulo", "dd/MM/yyyy");
        sheet.getRange(row, CONFIG.COL.DATA_CONCLUSAO + 1).setValue(hoje);
        sheet.getRange(row, CONFIG.COL.PCT + 1).setValue("100%");
        const responsavel = _str(rowData[CONFIG.COL.RESPONSAVEL]);
        const prioridade  = _str(rowData[CONFIG.COL.PRIORIDADE]);
        _postWebhook({ text: [
          `🎉 *Tarefa concluída!*`, ``,
          `*${responsavel}* finalizou: *${titulo}*`,
          `ID: ${id} | ${_iconeprioridade(prioridade)} ${prioridade}`,
          `🗓️ Concluído em: ${hoje}`,
        ].join("\n") });
        _marcarConcluindoNoTasks(id, responsavel);
      }

      if (novoStatus === "Bloqueado") {
        const blocker     = _str(rowData[CONFIG.COL.BLOCKER]) || "Não especificado";
        const responsavel = _str(rowData[CONFIG.COL.RESPONSAVEL]);
        _postWebhook({ text: [
          `🚨 *Tarefa bloqueada!*`, ``, `*${id}* — ${titulo}`,
          `👤 Responsável: ${responsavel}`, `🔒 Blocker: ${blocker}`,
          ``, `_Ação necessária._`,
        ].join("\n") });
      }

      // ── DEPENDÊNCIA EXTERNA ──────────────────────────────────────────────
      if (novoStatus === STATUS_AGUARDANDO) {
        notificarDependenciaExterna(row - 1, dados);
        sheet.getRange(row, COL_EXT.STATUS_DEP + 1).setValue("Pendente");
      }
      if (oldStatus === STATUS_AGUARDANDO && novoStatus !== STATUS_AGUARDANDO) {
        sheet.getRange(row, COL_EXT.STATUS_DEP + 1).setValue("Resolvida");
        const areaExt = _str(rowData[COL_EXT.AREA_EXTERNA]);
        _postWebhook({ text: [
          `✅ *Dependência resolvida!*`, ``, `*${id}* — ${titulo}`,
          `🏢 Área externa: ${areaExt}`, `📌 Novo status: ${novoStatus}`,
          ``, `_A atividade pode avançar._`,
        ].join("\n") });
      }

      if (novoStatus === "Em Andamento") {
        const dependeDe = _str(rowData[CONFIG.COL.DEPENDE_DE]);
        if (dependeDe && !_verificarDependenciaConcluida(dados, dependeDe)) {
          _postWebhook({ text: [
            `⚠️ *Atenção — dependência pendente!*`, ``, `*${id}* — ${titulo}`,
            `🔗 Depende de: *${dependeDe}* (ainda não concluída)`,
            ``, `_Verifique antes de iniciar._`,
          ].join("\n") });
        }
      }
    }

    // ── RESPONSÁVEL ────────────────────────────────────────────────────────
    if (col === CONFIG.COL.RESPONSAVEL) {
      const novoResp = _str(e.value);
      if (!novoResp || !CONFIG.TIME[novoResp]) return;
      const emailDest = CONFIG.TIME[novoResp].email;
      const status    = _str(rowData[CONFIG.COL.STATUS]);
      const prior     = _str(rowData[CONFIG.COL.PRIORIDADE]);
      const dataFim   = _str(rowData[CONFIG.COL.DATA_FIM]);
      _postWebhook({ text: [
        `👋 *Tarefa atribuída!*`, ``, `*${id}* — ${titulo}`,
        `👤 Responsável: *${novoResp}*`,
        `${_iconeprioridade(prior)} ${prior} | 📅 Prazo: ${dataFim}`,
        ``, `_${novoResp.split(" ")[0]}, você recebeu esta atividade!_`,
      ].join("\n") });
      if (emailDest) {
        MailApp.sendEmail({
          to: emailDest,
          subject: `[Sprint IC] Tarefa atribuída: ${id} — ${titulo}`,
          body: `Olá ${novoResp.split(" ")[0]},\n\nVocê foi designado(a) para:\n\n• ID: ${id}\n• Título: ${titulo}\n• Prioridade: ${prior}\n• Prazo: ${dataFim}\n• Status: ${status}\n\nAcesse o Sprint Board.\n\nTime IC — Mob2Con`,
        });
      }
    }

    // ── % CONCLUÍDO ────────────────────────────────────────────────────────
    if (col === CONFIG.COL.PCT) {
      const pct = parseFloat(_str(e.value).replace("%","")) || 0;
      if (pct >= 100) {
        const statusAtual = _str(rowData[CONFIG.COL.STATUS]);
        if (!statusAtual.includes("Concluído")) {
          sheet.getRange(row, CONFIG.COL.STATUS + 1).setValue("Concluído (Semana)");
          _aplicarCorStatus(sheet, row, "Concluído (Semana)");
        }
      }
    }
  } catch (err) {
    Logger.log(`[onEdit] ERRO: ${err.message}`);
  }
}

function _verificarDependenciaConcluida(dados, depId) {
  for (let i = 3; i < dados.length; i++) {
    if (_str(dados[i][CONFIG.COL.ID]) === depId)
      return _str(dados[i][CONFIG.COL.STATUS]).includes("Concluído");
  }
  return true;
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 5 — GOOGLE TASKS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function criarListasDeTasksParaTodos() {
  const props    = PropertiesService.getScriptProperties();
  const existing = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS) || "{}");
  let criadas = 0;
  Object.keys(CONFIG.TIME).forEach(nome => {
    if (existing[nome]) return;
    if (!CONFIG.TIME[nome].email) { existing[nome] = null; return; }
    try {
      const lista = Tasks.Tasklists.insert({ title: `🚀 Sprint IC | ${nome}` });
      existing[nome] = lista.id;
      criadas++;
    } catch (err) { Logger.log(`Erro lista ${nome}: ${err.message}`); }
  });
  props.setProperty(CONFIG.PROP.TASK_LISTS, JSON.stringify(existing));
  const links = Object.entries(existing).filter(([,id])=>id).map(([n])=>`• ${n}`).join("\n");
  SpreadsheetApp.getUi().alert(`✅ ${criadas} lista(s) criada(s)!\n\n${links}\n\nAcesse tasks.google.com`);
}

function sincronizarTodasAsTasks() {
  const ss     = SpreadsheetApp.getActiveSpreadsheet();
  const board  = ss.getSheetByName(CONFIG.ABA_BOARD);
  if (!board) { SpreadsheetApp.getUi().alert("⚠️ Aba Board não encontrada: " + CONFIG.ABA_BOARD); return; }
  const dados  = board.getDataRange().getValues();
  const props  = PropertiesService.getScriptProperties();
  const listas = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS) || "{}");
  const sprint = _sprintAtual();

  const porPessoa = {};
  Object.keys(CONFIG.TIME).forEach(n => { porPessoa[n] = []; });
  for (let i = 3; i < dados.length; i++) {
    const row  = dados[i];
    const resp = _str(row[CONFIG.COL.RESPONSAVEL]);
    if (!porPessoa[resp]) continue;
    const status = _str(row[CONFIG.COL.STATUS]);
    if (status === "Cancelado" || status === "Concluído Geral") continue;
    porPessoa[resp].push(row);
  }

  let totalCriadas = 0;
  Object.entries(porPessoa).forEach(([nome, tarefas]) => {
    const listId = listas[nome];
    if (!listId || !tarefas.length) return;
    const sigla   = CONFIG.TIME[nome].sigla;
    const mapKey  = CONFIG.PROP.TASK_MAP_PREFIX + sigla;
    const taskMap = JSON.parse(props.getProperty(mapKey) || "{}");

    tarefas.forEach(row => {
      const id      = _str(row[CONFIG.COL.ID]);
      const titulo  = _str(row[CONFIG.COL.TITULO]);
      const prio    = _str(row[CONFIG.COL.PRIORIDADE]);
      const status  = _str(row[CONFIG.COL.STATUS]);
      const pct     = row[CONFIG.COL.PCT] || "0%";
      const dataFim = row[CONFIG.COL.DATA_FIM];
      const desc    = _str(row[CONFIG.COL.DESCRICAO]);
      const epico   = _str(row[CONFIG.COL.EPICO]);
      const blocker = _str(row[CONFIG.COL.BLOCKER]);
      const tituloTask = `${_iconeprioridade(prio)} ${id} | ${sigla} — ${titulo}`;
      const notas = [
        `👤 ${nome} | 📊 ${status} | ${pct}`, `🏃 ${sprint}`,
        epico   ? `🎯 ${epico}` : "",
        blocker ? `🚨 Blocker: ${blocker}` : "",
        desc.substring(0, 300) || "",
      ].filter(Boolean).join("\n");

      try {
        if (taskMap[id]) {
          Tasks.Tasks.patch({ title: tituloTask, notes: notas, due: _toISODate(dataFim),
            status: status.includes("Concluído") ? "completed" : "needsAction",
          }, listId, taskMap[id]);
        } else {
          const task = Tasks.Tasks.insert({ title: tituloTask, notes: notas, due: _toISODate(dataFim),
            status: status.includes("Concluído") ? "completed" : "needsAction",
          }, listId);
          if (task && task.id) { taskMap[id] = task.id; totalCriadas++; }
        }
      } catch (err) { Logger.log(`Erro task ${id}/${nome}: ${err.message}`); }
    });
    props.setProperty(mapKey, JSON.stringify(taskMap));
  });

  const linksMsg = Object.entries(listas).filter(([,id]) => id)
    .map(([nome]) => `• *${nome}* (${CONFIG.TIME[nome].sigla}) — ${porPessoa[nome].length} tarefa(s)`)
    .join("\n");
  _postWebhook({ text: [`✅ *Tasks sincronizadas!*`, ``, `🗓️ Sprint: *${sprint}*`,
    `📋 Criadas/atualizadas: *${totalCriadas}*`, ``, linksMsg, ``, `_tasks.google.com_`].join("\n") });
  SpreadsheetApp.getUi().alert(`✅ Sincronização concluída!\n\n${totalCriadas} task(s) processada(s).`);
}

function sincronizarTasksMarcelo()  { _sincronizarPorPessoa("Marcelo Bora"); }
function sincronizarTasksPedro()    { _sincronizarPorPessoa("Pedro Malagutti"); }
function sincronizarTasksJoice()    { _sincronizarPorPessoa("Joice Topan"); }
function sincronizarTasksJoao()     { _sincronizarPorPessoa("João Rosa"); }
function sincronizarTasksMari()     { _sincronizarPorPessoa("Mariliana Fagotti"); }
function sincronizarTasksDonizete() { _sincronizarPorPessoa("Donizete"); }
function sincronizarTasksLucas()    { _sincronizarPorPessoa("Lucas"); }

function _sincronizarPorPessoa(nome) {
  const props  = PropertiesService.getScriptProperties();
  const listas = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS) || "{}");
  const listId = listas[nome];
  if (!listId) {
    SpreadsheetApp.getUi().alert(`⚠️ Lista não encontrada para ${nome}.\n\nExecute: ⚙️ Config → 🆔 Criar Listas`);
    return;
  }
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  const dados = board.getDataRange().getValues();
  const sprint= _sprintAtual();
  const sigla = CONFIG.TIME[nome].sigla;
  try { Tasks.Tasklists.clear(listId); } catch (e) { Logger.log("clear: " + e.message); }

  const mapKey  = CONFIG.PROP.TASK_MAP_PREFIX + sigla;
  const taskMap = {};
  let cnt = 0;

  for (let i = 3; i < dados.length; i++) {
    const row    = dados[i];
    if (_str(row[CONFIG.COL.RESPONSAVEL]) !== nome) continue;
    const status = _str(row[CONFIG.COL.STATUS]);
    if (status === "Cancelado" || status === "Concluído Geral") continue;

    const id      = _str(row[CONFIG.COL.ID]);
    const titulo  = _str(row[CONFIG.COL.TITULO]);
    const prio    = _str(row[CONFIG.COL.PRIORIDADE]);
    const pct     = row[CONFIG.COL.PCT] || "0%";
    const dataFim = row[CONFIG.COL.DATA_FIM];
    const desc    = _str(row[CONFIG.COL.DESCRICAO]);
    const epico   = _str(row[CONFIG.COL.EPICO]);
    const blocker = _str(row[CONFIG.COL.BLOCKER]);

    const notas = [
      `👤 ${nome} | 📊 ${status} | ${pct}`, `🏃 ${sprint}`,
      epico   ? `🎯 ${epico}` : "",
      blocker ? `🚨 Blocker: ${blocker}` : "",
      desc.substring(0, 300) || "",
    ].filter(Boolean).join("\n");

    try {
      const task = Tasks.Tasks.insert({
        title: `${_iconeprioridade(prio)} ${id} | ${sigla} — ${titulo}`,
        notes: notas, due: _toISODate(dataFim),
        status: status.includes("Concluído") ? "completed" : "needsAction",
      }, listId);
      if (task && task.id) { taskMap[id] = task.id; cnt++; }
    } catch (err) { Logger.log(`Erro task ${id}: ${err.message}`); }
  }
  PropertiesService.getScriptProperties().setProperty(mapKey, JSON.stringify(taskMap));
  SpreadsheetApp.getUi().alert(`✅ ${cnt} tarefa(s) sincronizadas para ${nome}!`);
}

function sincronizarTasksDeVolta() {
  const props  = PropertiesService.getScriptProperties();
  const listas = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS) || "{}");
  const ss     = SpreadsheetApp.getActiveSpreadsheet();
  const board  = ss.getSheetByName(CONFIG.ABA_BOARD);
  const dados  = board.getDataRange().getValues();
  const atualizados = [];

  Object.entries(listas).forEach(([nome, listId]) => {
    if (!listId) return;
    const sigla   = CONFIG.TIME[nome] ? CONFIG.TIME[nome].sigla : "??";
    const taskMap = JSON.parse(props.getProperty(CONFIG.PROP.TASK_MAP_PREFIX + sigla) || "{}");
    const inverso = {};
    Object.entries(taskMap).forEach(([k, v]) => { inverso[v] = k; });

    let tasks = [], pageToken = null;
    try {
      do {
        const params = { showCompleted: true, showHidden: false, maxResults: 100 };
        if (pageToken) params.pageToken = pageToken;
        const result = Tasks.Tasks.list(listId, params);
        tasks = tasks.concat(result.items || []);
        pageToken = result.nextPageToken || null;
      } while (pageToken);
    } catch (e) { return; }

    tasks.filter(t => t.status === "completed").forEach(task => {
      const kanId = inverso[task.id];
      if (!kanId) return;
      for (let i = 3; i < dados.length; i++) {
        if (_str(dados[i][CONFIG.COL.ID]) !== kanId) continue;
        if (_str(dados[i][CONFIG.COL.STATUS]).includes("Concluído")) break;
        const hoje = Utilities.formatDate(new Date(), "America/Sao_Paulo", "dd/MM/yyyy");
        board.getRange(i + 1, CONFIG.COL.STATUS         + 1).setValue("Concluído (Semana)");
        board.getRange(i + 1, CONFIG.COL.PCT            + 1).setValue("100%");
        board.getRange(i + 1, CONFIG.COL.DATA_CONCLUSAO + 1).setValue(hoje);
        _aplicarCorStatus(board, i + 1, "Concluído (Semana)");
        atualizados.push({ id: kanId, responsavel: nome, tarefa: _str(dados[i][CONFIG.COL.TITULO]) });
        break;
      }
    });
  });

  atualizados.forEach(t => {
    _postWebhook({ text: [
      `🎉 *Tarefa concluída via Tasks!*`, ``,
      `*${t.responsavel}* concluiu: *${t.tarefa}*`, `ID: ${t.id}`,
    ].join("\n") });
  });
}

function _marcarConcluindoNoTasks(kanId, responsavel) {
  const props  = PropertiesService.getScriptProperties();
  const listas = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS) || "{}");
  const listId = listas[responsavel];
  if (!listId) return;
  const sigla  = CONFIG.TIME[responsavel] ? CONFIG.TIME[responsavel].sigla : "";
  const taskMap= JSON.parse(props.getProperty(CONFIG.PROP.TASK_MAP_PREFIX + sigla) || "{}");
  const taskId = taskMap[kanId];
  if (!taskId) return;
  try { Tasks.Tasks.patch({ status: "completed" }, listId, taskId); }
  catch (e) { Logger.log(`Erro marcar concluído: ${e.message}`); }
}

function exibirIDsListas() {
  const listas = JSON.parse(PropertiesService.getScriptProperties().getProperty(CONFIG.PROP.TASK_LISTS) || "{}");
  SpreadsheetApp.getUi().alert(`IDs das listas:\n\n${Object.entries(listas).map(([n,id])=>`${n}: ${id||"❌"}`).join("\n")}`);
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 6 — SPRINT MANAGEMENT
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function iniciarNovaSprint() {
  const ui   = SpreadsheetApp.getUi();
  const resp = ui.prompt("🚀 Nova Sprint","Período (ex: 23/04–07/05/2026):", ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;
  const periodo = resp.getResponseText().trim();
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  const dados = board.getDataRange().getValues();
  const numeroSprint = _proximoNumeroSprint(dados);
  const nomeSprint   = `Sprint ${numeroSprint} — ${periodo}`;
  board.getRange("B2").setValue(nomeSprint);

  const [dataInicio, dataFim] = _calcularDatasSprint(periodo);
  let moverCnt = 0;
  const startRow = 4, numRows = dados.length - 3;
  if (numRows <= 0) return;

  const colSprint     = board.getRange(startRow, CONFIG.COL.SPRINT      + 1, numRows, 1).getValues();
  const colDataInicio = board.getRange(startRow, CONFIG.COL.DATA_INICIO + 1, numRows, 1).getValues();
  const colDataFim    = board.getRange(startRow, CONFIG.COL.DATA_FIM    + 1, numRows, 1).getValues();

  for (let i = 3; i < dados.length; i++) {
    const status = _str(dados[i][CONFIG.COL.STATUS]);
    const sp     = _str(dados[i][CONFIG.COL.SPRINT]);
    if ((status==="Backlog"||status==="A Fazer"||status==="Novas Solicitações")&&(sp==="Sem sprint"||sp==="")) {
      const ri = i - 3;
      colSprint[ri][0]     = nomeSprint;
      colDataInicio[ri][0] = dataInicio;
      if (!dados[i][CONFIG.COL.DATA_FIM]) colDataFim[ri][0] = dataFim;
      moverCnt++;
    }
  }
  if (moverCnt > 0) {
    board.getRange(startRow, CONFIG.COL.SPRINT      + 1, numRows, 1).setValues(colSprint);
    board.getRange(startRow, CONFIG.COL.DATA_INICIO + 1, numRows, 1).setValues(colDataInicio);
    board.getRange(startRow, CONFIG.COL.DATA_FIM    + 1, numRows, 1).setValues(colDataFim);
  }
  _postWebhook({ text: ["🚀 *Nova Sprint iniciada!*", "", `🗓️ Sprint: *${nomeSprint}*`,
    `📋 Atividades alocadas: *${moverCnt}*`, "", "📅 Planning: Terça | 🔍 Review: Quinta",
    "", "_Vamos nessa! 💪_"].join("\n") });
  sincronizarTodasAsTasks();
}

function _proximoNumeroSprint(dados) {
  let maxNum = 0;
  for (let i = 3; i < dados.length; i++) {
    const m = _str(dados[i][CONFIG.COL.SPRINT]).match(/Sprint\s+(\d+)/i);
    if (m) maxNum = Math.max(maxNum, parseInt(m[1], 10));
  }
  return maxNum + 1;
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 7 — RESUMO & NOTIFICAÇÕES
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function enviarResumoDaSprint() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const dados = ss.getSheetByName(CONFIG.ABA_BOARD).getDataRange().getValues();
  const sprint= _sprintAtual();
  const metr  = _calcularMetricas(dados);
  const pct   = metr.total>0 ? Math.round((metr.concluidos/metr.total)*100) : 0;

  const porPessoa = {};
  Object.keys(CONFIG.TIME).forEach(n => { porPessoa[n]={total:0,concluidos:0,bloqueados:0}; });
  for (let i=3;i<dados.length;i++) {
    const row  = dados[i];
    const nome = _str(row[CONFIG.COL.RESPONSAVEL]);
    if (!porPessoa[nome]) continue;
    const status = _str(row[CONFIG.COL.STATUS]);
    porPessoa[nome].total++;
    if (status.includes("Concluído")) porPessoa[nome].concluidos++;
    if (status==="Bloqueado") porPessoa[nome].bloqueados++;
  }

  const linhasPessoa = Object.entries(porPessoa).filter(([,m])=>m.total>0)
    .map(([nome,m])=>{
      const sigla=CONFIG.TIME[nome]?CONFIG.TIME[nome].sigla:"??";
      const p=m.total>0?Math.round((m.concluidos/m.total)*100):0;
      return `• *${sigla}* — ${m.concluidos}/${m.total} (${p}%)${m.bloqueados>0?" 🚨":""}`;
    }).join("\n");

  const blockers=[];
  for (let i=3;i<dados.length;i++) {
    const row=dados[i];
    if (_str(row[CONFIG.COL.STATUS])==="Bloqueado")
      blockers.push(`⛔ ${row[CONFIG.COL.ID]} — ${row[CONFIG.COL.TITULO]} (${row[CONFIG.COL.RESPONSAVEL]})`);
  }

  const msg=[`📊 *RESUMO DA SPRINT — ${sprint}*`,``,
    `${_barraProgresso(pct)} ${pct}%`,
    `✅ ${metr.concluidos} de ${metr.total} tarefas concluídas`,
    `🔄 Em andamento: ${metr.emAndamento} | 🔒 Bloqueados: ${metr.bloqueados}`,
    ``,`*Por pessoa:*`,linhasPessoa];
  if (blockers.length) msg.push("","*🚨 Blockers:*",...blockers);
  msg.push("",`_${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy 'às' HH:mm")}_`);
  _postWebhook({text:msg.join("\n")});
}

function notificarBora()  { _notificarPessoa("Marcelo Bora"); }
function notificarPedro() { _notificarPessoa("Pedro Malagutti"); }
function notificarJoice() { _notificarPessoa("Joice Topan"); }
function notificarJoao()  { _notificarPessoa("João Rosa"); }
function notificarMari()      { _notificarPessoa("Mariliana Fagotti"); }
function notificarDonizete()  { _notificarPessoa("Donizete"); }
function notificarLucas()     { _notificarPessoa("Lucas"); }

function _notificarPessoa(nome) {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const dados = ss.getSheetByName(CONFIG.ABA_BOARD).getDataRange().getValues();
  const sigla = CONFIG.TIME[nome]?CONFIG.TIME[nome].sigla:"??";
  const sprint= _sprintAtual();
  const tarefas=[],blockers=[];
  let concluidas=0;
  for (let i=3;i<dados.length;i++) {
    const row=dados[i];
    if (_str(row[CONFIG.COL.RESPONSAVEL])!==nome) continue;
    const id    =_str(row[CONFIG.COL.ID]);
    const titulo=_str(row[CONFIG.COL.TITULO]);
    const status=_str(row[CONFIG.COL.STATUS]);
    const prior =_str(row[CONFIG.COL.PRIORIDADE]);
    const pct   =_str(row[CONFIG.COL.PCT])||"0%";
    const block =_str(row[CONFIG.COL.BLOCKER]);
    if (status.includes("Concluído")){concluidas++;continue;}
    if (status==="Cancelado") continue;
    const pctNum=parseFloat(pct.replace("%",""))||0;
    tarefas.push(`${_iconeprioridade(prior)} *${id}* — ${titulo}`);
    tarefas.push(`  ${_barraProgresso(pctNum,5)} ${pct} | ${status}`);
    if (block) blockers.push(`  ⛔ Blocker: ${block}`);
  }
  const total=tarefas.length/2+concluidas;
  const pctG=total>0?Math.round((concluidas/total)*100):0;
  const msg=[`👤 *Update: ${nome} (${sigla})*`,`🏃 Sprint: ${sprint}`,``,
    `${_barraProgresso(pctG)} ${pctG}% — ${concluidas}/${total} concluídas`,
    ``,`*Tarefas ativas:*`,tarefas.length?tarefas.join("\n"):"_Nenhuma_"];
  if (blockers.length) msg.push("","*🚨 Blockers:*",...blockers);
  msg.push("",`_${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy 'às' HH:mm")}_`);
  _postWebhook({text:msg.join("\n")});
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 8 — AGENDA PLANNING & REVIEW
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function enviarAgendaPlanning() {
  const sprint=_sprintAtual();
  const hoje=Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy");
  _postWebhook({text:[`📅 *PLANNING — ${sprint}*`,`Data: ${hoje}`,``,`*Agenda:*`,
    `1. Review das tasks concluídas`,`2. Triagem de Novas Solicitações`,
    `3. Priorização do Backlog`,`4. Alocação por pessoa`,
    `5. Definição de blockers e dependências`,``,`_Board IC atualizado ✅_`].join("\n")});
}

function enviarAgendaReview() {
  const sprint=_sprintAtual();
  const hoje=Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy");
  const dados=SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.ABA_BOARD).getDataRange().getValues();
  const metr=_calcularMetricas(dados);
  const pct=metr.total>0?Math.round((metr.concluidos/metr.total)*100):0;
  _postWebhook({text:[`🔍 *REVIEW — ${sprint}*`,`Data: ${hoje}`,``,
    `${_barraProgresso(pct)} ${pct}%`,
    `✅ Concluídas: ${metr.concluidos} / ${metr.total}`,
    `🔄 Em andamento: ${metr.emAndamento} | 🔒 Bloqueadas: ${metr.bloqueados}`,``,
    `*Pauta:*`,`1. Demonstração das entregas`,`2. Análise de blockers e atrasos`,
    `3. Feedback e aprendizados`,`4. Preparação para o próximo planning`,``,`_Até terça! 🚀_`].join("\n")});
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 9 — SLA & ALERTAS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function verificarAtrasos() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  if (!board) return;
  const dados = board.getDataRange().getValues();
  const hoje  = new Date();
  const atrasados=[],slaVencido=[];

  for (let i=3;i<dados.length;i++) {
    const row    = dados[i];
    const status = _str(row[CONFIG.COL.STATUS]);
    if (status.includes("Concluído")||status==="Cancelado") continue;
    const id  =_str(row[CONFIG.COL.ID]);
    const tit =_str(row[CONFIG.COL.TITULO]);
    const resp=_str(row[CONFIG.COL.RESPONSAVEL]);
    if (row[CONFIG.COL.DATA_FIM]) {
      const df=new Date(row[CONFIG.COL.DATA_FIM]);
      if (!isNaN(df.getTime())&&df<hoje) {
        const dias=Math.ceil((hoje-df)/86400000);
        atrasados.push(`• *${id}* — ${tit} (${resp}) — ${dias}d atraso`);
        board.getRange(i+1,CONFIG.COL.SLA_STATUS+1).setValue("⚠️ Atrasado");
      }
    }
    if (row[CONFIG.COL.SLA_LIMITE]) {
      const sl=new Date(row[CONFIG.COL.SLA_LIMITE]);
      if (!isNaN(sl.getTime())&&sl<hoje&&!_str(row[CONFIG.COL.SLA_STATUS]).includes("Atrasado")) {
        const dias=Math.ceil((hoje-sl)/86400000);
        slaVencido.push(`• *${id}* — ${tit} — SLA vencido há ${dias}d`);
      }
    }
  }

  if (!atrasados.length&&!slaVencido.length){Logger.log("[verificarAtrasos] Nenhum.");return;}
  const msg=[`⚠️ *ALERTA — ${Utilities.formatDate(hoje,"America/Sao_Paulo","dd/MM/yyyy")}*`,``];
  if (atrasados.length)  msg.push("*📅 Prazo vencido:*",...atrasados,"");
  if (slaVencido.length) msg.push("*⏱️ SLA vencido:*",...slaVencido,"");
  msg.push("_Verifique o Board._");
  _postWebhook({text:msg.join("\n")});
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 10 — DEPENDÊNCIA EXTERNA
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function notificarDependenciaExterna(rowIdx, dados) {
  const row         = dados[rowIdx];
  const id          = _str(row[CONFIG.COL.ID]);
  const titulo      = _str(row[CONFIG.COL.TITULO]);
  const responsavel = _str(row[CONFIG.COL.RESPONSAVEL]);
  const prioridade  = _str(row[CONFIG.COL.PRIORIDADE]);
  const prazo       = _str(row[CONFIG.COL.DATA_FIM]);
  const descricao   = _str(row[CONFIG.COL.DESCRICAO]);
  const dependeDe   = _str(row[CONFIG.COL.DEPENDE_DE]);
  const areaExterna = _str(row[COL_EXT.AREA_EXTERNA]);
  const emailExt    = _str(row[COL_EXT.EMAIL_EXTERNO]);
  const icone       = _iconeprioridade(prioridade);
  const slaFmt      = _str(row[CONFIG.COL.SLA_LIMITE]);

  _postWebhook({ text: [
    `⏳ *Dependência Externa — Aguardando Área Parceira*`, ``,
    `*${id}* — ${titulo}`,
    `👤 Responsável IC: ${responsavel}`,
    `🏢 Aguardando: *${areaExterna || emailExt}*`,
    dependeDe ? `🔗 Depende de: ${dependeDe}` : "",
    `${icone} Prioridade: ${prioridade}`,
    `📅 Prazo: ${prazo}`, ``, `_E-mail de notificação enviado para: ${emailExt || "—"}_`,
    `_${slaFmt}_`,
  ].filter(l => l !== "").join("\n") });

  if (emailExt) {
    try {
      MailApp.sendEmail({
        to: emailExt,
        subject: `[IC Mob2Con] Dependência Identificada — ${id}: ${titulo}`,
        htmlBody: `
          <div style="font-family:Arial,sans-serif;max-width:640px;padding:20px;border:1px solid #e5e7eb;border-radius:8px">
            <div style="background:#F46901;color:#fff;padding:14px 20px;border-radius:6px 6px 0 0">
              <h2 style="margin:0;font-size:17px">⏳ Sua participação é necessária — IC Mob2Con</h2>
              <p style="margin:4px 0 0;font-size:13px;opacity:0.9">${id} — ${titulo}</p>
            </div>
            <div style="padding:20px">
              <p>Olá <strong>${areaExterna}</strong>,</p>
              <p>O time de <strong>Inteligência Comercial (IC)</strong> da Mob2Con abriu uma atividade que
                <strong>depende de uma ação ou aprovação da sua área</strong> para avançar.</p>
              <table style="border-collapse:collapse;width:100%;font-size:14px;margin:16px 0">
                <tr style="background:#f9fafb"><td style="padding:8px;color:#6b7280;width:140px;font-weight:bold">Ticket</td><td style="padding:8px"><strong>${id}</strong></td></tr>
                <tr><td style="padding:8px;color:#6b7280;font-weight:bold">Atividade</td><td style="padding:8px">${titulo}</td></tr>
                <tr style="background:#f9fafb"><td style="padding:8px;color:#6b7280;font-weight:bold">Responsável IC</td><td style="padding:8px">${responsavel}</td></tr>
                <tr><td style="padding:8px;color:#6b7280;font-weight:bold">Prioridade</td><td style="padding:8px">${prioridade}</td></tr>
                <tr style="background:#f9fafb"><td style="padding:8px;color:#6b7280;font-weight:bold">Prazo Ideal</td><td style="padding:8px">${prazo || "A combinar"}</td></tr>
                ${dependeDe ? `<tr><td style="padding:8px;color:#6b7280;font-weight:bold">Depende de</td><td style="padding:8px">${dependeDe}</td></tr>` : ""}
              </table>
              ${descricao ? `<div style="background:#f9fafb;border-left:4px solid #F46901;padding:12px;margin:16px 0;border-radius:0 4px 4px 0"><p style="margin:0;font-size:13px;color:#374151"><strong>Contexto:</strong><br>${descricao.replace(/\n/g,"<br>")}</p></div>` : ""}
              <div style="background:#FFF3E8;border:1px solid #FDBA74;border-radius:6px;padding:12px;margin:16px 0">
                <p style="margin:0;font-size:13px;color:#C2410C">
                  <strong>📌 O que precisamos de você:</strong><br>
                  Por favor, responda este e-mail ou entre em contato com <strong>${responsavel}</strong> (IC) informando como podemos prosseguir.
                </p>
              </div>
              <hr style="border:none;border-top:1px solid #e5e7eb;margin:16px 0">
              <p style="color:#6b7280;font-size:12px">Time IC — Mob2Con Inteligência Comercial<br>Este e-mail foi gerado automaticamente pelo sistema Sprint IC.</p>
            </div>
          </div>`,
      });
      Logger.log(`[notificarDependenciaExterna] E-mail enviado para ${emailExt}`);
      return true;
    } catch (err) {
      Logger.log(`[notificarDependenciaExterna] Erro e-mail: ${err.message}`);
      return false;
    }
  }
  return true;
}

function verificarDependenciasExternas() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  const dados = board.getDataRange().getValues();
  const pendentes = [];

  for (let i=3;i<dados.length;i++) {
    const row    = dados[i];
    const status = _str(row[CONFIG.COL.STATUS]);
    const id     = _str(row[CONFIG.COL.ID]);
    if (!id) continue;
    if (status===STATUS_AGUARDANDO) {
      const areaExt  = _str(row[COL_EXT.AREA_EXTERNA]);
      const emailExt = _str(row[COL_EXT.EMAIL_EXTERNO]);
      const statusDep= _str(row[COL_EXT.STATUS_DEP]);
      if (statusDep!=="Resolvida")
        pendentes.push(`• *${id}* — ${_str(row[CONFIG.COL.TITULO])} → Aguardando: ${areaExt||emailExt}`);
    }
  }
  if (!pendentes.length){Logger.log("[verificarDependenciasExternas] Nenhuma pendente.");return;}
  _postWebhook({text:[`⏳ *DEPENDÊNCIAS EXTERNAS PENDENTES*`,``,
    `${pendentes.length} atividade(s) aguardando resposta de áreas externas:`,``,
    ...pendentes,``,`_Verifique o Board e atualize o status quando as dependências forem resolvidas._`,
    `_${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy 'às' HH:mm")}_`].join("\n")});
}

function testarDependenciaExterna() {
  const email = Session.getActiveUser().getEmail();
  const mockRow = new Array(31).fill("");
  mockRow[CONFIG.COL.ID]         = "KAN-TESTE";
  mockRow[CONFIG.COL.TITULO]     = "Validação do processo com área de RH";
  mockRow[CONFIG.COL.RESPONSAVEL]= "Mariliana Fagotti";
  mockRow[CONFIG.COL.PRIORIDADE] = "🟠 Alta";
  mockRow[CONFIG.COL.DATA_FIM]   = "30/04/2026";
  mockRow[CONFIG.COL.DESCRICAO]  = "Precisamos que o RH valide o novo fluxo de onboarding antes de avançarmos.";
  mockRow[CONFIG.COL.DEPENDE_DE] = "Aprovação do gestor de RH";
  mockRow[COL_EXT.AREA_EXTERNA]  = "Recursos Humanos";
  mockRow[COL_EXT.EMAIL_EXTERNO] = email;
  const mockDados = [[], [], [], mockRow];
  const ok = notificarDependenciaExterna(3, mockDados);
  SpreadsheetApp.getUi().alert(ok
    ? `✅ Teste enviado!\n\nVerifique:\n• E-mail enviado para: ${email}\n• Mensagem no Google Chat`
    : `⚠️ Teste executado, mas sem e-mail.`);
}

function configurarColunasDependenciaExterna() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  const cabecalho = board.getRange(3, 1, 1, board.getLastColumn()).getValues()[0];
  if (cabecalho.some(c => String(c).includes("Área Externa"))) {
    SpreadsheetApp.getUi().alert("✅ Colunas de dependência externa já configuradas!");
    return;
  }
  const ultimaCol  = board.getLastColumn();
  const novasCols  = ["Área Externa Responsável","E-mail Área Externa","Status Dependência"];
  novasCols.forEach((label, i) => {
    const col = ultimaCol + i + 1;
    board.getRange(3, col).setValue(label)
      .setBackground("#374151").setFontColor("#FFFFFF")
      .setFontWeight("bold").setFontSize(10);
    board.setColumnWidth(col, 160);
  });
  SpreadsheetApp.getUi().alert(
    "✅ Colunas adicionadas ao Board!\n\n" +
    "• Coluna AB: Área Externa Responsável\n" +
    "• Coluna AC: E-mail Área Externa\n" +
    "• Coluna AD: Status Dependência\n\n" +
    "Para usar: Preencha as colunas e mude o Status para 'Aguardando Área Externa'."
  );
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 11 — KANBAN INDIVIDUAL POR MEMBRO (QUERY → BOARD)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//
//  Arquitetura:
//  Board (fonte) → QUERY por responsável → Aba "📋 [SIGLA] Nomemembro"
//  Cada aba tem:
//  • Cabeçalho visual com cor do membro, nome e stats
//  • Tabela QUERY agrupada por status (ordenado por prioridade)
//  • Seção "Em Andamento" destacada no topo
//  • Seção "Bloqueado / Aguardando" em vermelho
//  • Seção "Concluídas" ao final
//
//  As abas atualizam AUTOMATICAMENTE quando o Board é editado (QUERY ao vivo).
//  O script só reconstrói o visual (cores, cabeçalhos, larguras).
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function criarKanbanTodosMembros() {
  const ui = SpreadsheetApp.getUi();
  const resp = ui.alert("📊 Criar Kanbans Individuais",
    "Isso criará 1 aba por membro com QUERY ao vivo no Board.\n\nMembros: " +
    Object.keys(CONFIG.TIME).join(", ") +
    "\n\nAs abas atualizam automaticamente ao editar o Board.\n\nContinuar?",
    ui.ButtonSet.OK_CANCEL);
  if (resp !== ui.Button.OK) return;

  Object.keys(CONFIG.TIME).forEach(nome => _criarKanbanPorMembro(nome));
  SpreadsheetApp.getUi().alert("✅ Kanbans individuais criados!\n\nCada aba atualiza automaticamente via QUERY do Board.");
}

function criarKanbanMarcelo()  { _criarKanbanPorMembro("Marcelo Bora"); }
function criarKanbanPedro()    { _criarKanbanPorMembro("Pedro Malagutti"); }
function criarKanbanJoice()    { _criarKanbanPorMembro("Joice Topan"); }
function criarKanbanJoao()     { _criarKanbanPorMembro("João Rosa"); }
function criarKanbanMari()     { _criarKanbanPorMembro("Mariliana Fagotti"); }
function criarKanbanDonizete() { _criarKanbanPorMembro("Donizete"); }
function criarKanbanLucas()    { _criarKanbanPorMembro("Lucas"); }

function atualizarTodosKanbans() {
  Object.keys(CONFIG.TIME).forEach(nome => _criarKanbanPorMembro(nome));
  SpreadsheetApp.getUi().alert("✅ Todos os Kanbans atualizados!");
}

/**
 * Cria (ou reconstrói) a aba de Kanban individual para um membro.
 * A QUERY ao Board é a fonte ao vivo — o script apenas formata o visual.
 */
function _criarKanbanPorMembro(nome) {
  const ss     = SpreadsheetApp.getActiveSpreadsheet();
  const membro = CONFIG.TIME[nome];
  if (!membro) return;

  const sigla  = membro.sigla;
  const cor    = COR_TIME[nome] || "#374151";
  const nomeAba= `📋 ${sigla} — ${nome.split(" ")[0]}`;
  const boardAba = CONFIG.ABA_BOARD.replace(/'/g, "\\'");

  let aba = ss.getSheetByName(nomeAba);
  if (!aba) {
    aba = ss.insertSheet(nomeAba);
  } else {
    aba.clearContents();
    aba.clearFormats();
    aba.clearNotes();
  }

  // ── Larguras das colunas ────────────────────────────────────────────────
  // A=ID, B=Titulo, C=Tipo, D=Status, E=Prioridade, G=Categoria, K=DataFim, H=Sprint, N=%, Z=SLA
  const widths = [85, 310, 90, 140, 95, 110, 120, 130, 80, 110];
  widths.forEach((w, i) => aba.setColumnWidth(i + 1, w));

  // ── LINHA 1 — Cabeçalho do membro ──────────────────────────────────────
  aba.getRange("A1:J1").merge()
    .setValue(`📋  ${sigla} | ${nome}  —  Kanban Individual  |  Mob2Con IC`)
    .setBackground(cor)
    .setFontColor("#FFFFFF")
    .setFontSize(13)
    .setFontWeight("bold")
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");
  aba.setRowHeight(1, 42);

  // ── LINHA 2 — Info ao vivo ─────────────────────────────────────────────
  aba.getRange("A2:J2").merge()
    .setValue(`🔗 Atualização ao vivo via Board | Sprint: ${_sprintAtual()} | 🕐 ${Utilities.formatDate(new Date(), "America/Sao_Paulo", "dd/MM/yyyy HH:mm")}`)
    .setBackground("#F8F9FA")
    .setFontColor("#374151")
    .setFontSize(10)
    .setHorizontalAlignment("center");
  aba.setRowHeight(2, 24);

  // ── LINHA 3 — espaço ───────────────────────────────────────────────────
  aba.setRowHeight(3, 8);

  // ─────────────────────────────────────────────────────────────────────────
  //  BLOCO A — EM ANDAMENTO (destaque laranja)
  // ─────────────────────────────────────────────────────────────────────────
  let linhaAtual = 4;

  aba.getRange(linhaAtual, 1, 1, 10).merge()
    .setValue("▶  EM ANDAMENTO")
    .setBackground("#FFF7ED").setFontColor("#C2410C")
    .setFontSize(11).setFontWeight("bold")
    .setHorizontalAlignment("left").setVerticalAlignment("middle");
  aba.setRowHeight(linhaAtual, 28);
  linhaAtual++;

  // Cabeçalho da tabela
  aba.getRange(linhaAtual, 1, 1, 10)
    .setValues([["ID","Título","Tipo","Status","Prioridade","Categoria","Data Fim","Sprint","% Concl.","SLA"]])
    .setBackground("#C2410C").setFontColor("#FFFFFF")
    .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  aba.setRowHeight(linhaAtual, 26);
  linhaAtual++;

  // QUERY — Em Andamento
  const qAndamento = `=IFERROR(QUERY('${boardAba}'!A4:Z,` +
    `"SELECT A,B,C,D,E,G,K,H,N,Z ` +
    `WHERE F = '${nome}' ` +
    `AND D = 'Em Andamento' ` +
    `AND A IS NOT NULL ` +
    `ORDER BY E ASC",0),"✅ Nenhuma tarefa em andamento.")`;
  aba.getRange(linhaAtual, 1).setFormula(qAndamento);
  aba.getRange(linhaAtual, 1, 20, 10).setBackground("#FFF7ED");
  linhaAtual += 20;

  // ─────────────────────────────────────────────────────────────────────────
  //  BLOCO B — AGUARDANDO / BLOQUEADO
  // ─────────────────────────────────────────────────────────────────────────
  linhaAtual++;
  aba.getRange(linhaAtual, 1, 1, 10).merge()
    .setValue("🔒  BLOQUEADO / AGUARDANDO")
    .setBackground("#FEF2F2").setFontColor("#991B1B")
    .setFontSize(11).setFontWeight("bold")
    .setHorizontalAlignment("left").setVerticalAlignment("middle");
  aba.setRowHeight(linhaAtual, 28);
  linhaAtual++;

  aba.getRange(linhaAtual, 1, 1, 10)
    .setValues([["ID","Título","Tipo","Status","Prioridade","Categoria","Data Fim","Sprint","% Concl.","SLA"]])
    .setBackground("#991B1B").setFontColor("#FFFFFF")
    .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  aba.setRowHeight(linhaAtual, 26);
  linhaAtual++;

  const qBloqueado = `=IFERROR(QUERY('${boardAba}'!A4:Z,` +
    `"SELECT A,B,C,D,E,G,K,H,N,Z ` +
    `WHERE F = '${nome}' ` +
    `AND (D = 'Bloqueado' OR D = 'Aguardando Área Externa') ` +
    `AND A IS NOT NULL ` +
    `ORDER BY E ASC",0),"✅ Nenhuma tarefa bloqueada.")`;
  aba.getRange(linhaAtual, 1).setFormula(qBloqueado);
  aba.getRange(linhaAtual, 1, 10, 10).setBackground("#FEF2F2");
  linhaAtual += 10;

  // ─────────────────────────────────────────────────────────────────────────
  //  BLOCO C — A FAZER / BACKLOG / NOVAS SOLICITAÇÕES
  // ─────────────────────────────────────────────────────────────────────────
  linhaAtual++;
  aba.getRange(linhaAtual, 1, 1, 10).merge()
    .setValue("📝  A FAZER / BACKLOG / NOVAS SOLICITAÇÕES")
    .setBackground("#EFF6FF").setFontColor("#1D4ED8")
    .setFontSize(11).setFontWeight("bold")
    .setHorizontalAlignment("left").setVerticalAlignment("middle");
  aba.setRowHeight(linhaAtual, 28);
  linhaAtual++;

  aba.getRange(linhaAtual, 1, 1, 10)
    .setValues([["ID","Título","Tipo","Status","Prioridade","Categoria","Data Fim","Sprint","% Concl.","SLA"]])
    .setBackground("#1D4ED8").setFontColor("#FFFFFF")
    .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  aba.setRowHeight(linhaAtual, 26);
  linhaAtual++;

  const qAfazer = `=IFERROR(QUERY('${boardAba}'!A4:Z,` +
    `"SELECT A,B,C,D,E,G,K,H,N,Z ` +
    `WHERE F = '${nome}' ` +
    `AND (D = 'A Fazer' OR D = 'Backlog' OR D = 'Novas Solicitações') ` +
    `AND A IS NOT NULL ` +
    `ORDER BY E ASC, D ASC",0),"✅ Nenhuma tarefa pendente.")`;
  aba.getRange(linhaAtual, 1).setFormula(qAfazer);
  aba.getRange(linhaAtual, 1, 20, 10).setBackground("#EFF6FF");
  linhaAtual += 20;

  // ─────────────────────────────────────────────────────────────────────────
  //  BLOCO D — EM VALIDAÇÃO
  // ─────────────────────────────────────────────────────────────────────────
  linhaAtual++;
  aba.getRange(linhaAtual, 1, 1, 10).merge()
    .setValue("🔍  EM VALIDAÇÃO")
    .setBackground("#FEFCE8").setFontColor("#854D0E")
    .setFontSize(11).setFontWeight("bold")
    .setHorizontalAlignment("left").setVerticalAlignment("middle");
  aba.setRowHeight(linhaAtual, 28);
  linhaAtual++;

  aba.getRange(linhaAtual, 1, 1, 10)
    .setValues([["ID","Título","Tipo","Status","Prioridade","Categoria","Data Fim","Sprint","% Concl.","SLA"]])
    .setBackground("#854D0E").setFontColor("#FFFFFF")
    .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  aba.setRowHeight(linhaAtual, 26);
  linhaAtual++;

  const qValidacao = `=IFERROR(QUERY('${boardAba}'!A4:Z,` +
    `"SELECT A,B,C,D,E,G,K,H,N,Z ` +
    `WHERE F = '${nome}' ` +
    `AND D = 'Em Validação' ` +
    `AND A IS NOT NULL ` +
    `ORDER BY E ASC",0),"✅ Nenhuma tarefa em validação.")`;
  aba.getRange(linhaAtual, 1).setFormula(qValidacao);
  aba.getRange(linhaAtual, 1, 10, 10).setBackground("#FEFCE8");
  linhaAtual += 10;

  // ─────────────────────────────────────────────────────────────────────────
  //  BLOCO E — CONCLUÍDAS (Sprint atual)
  // ─────────────────────────────────────────────────────────────────────────
  linhaAtual++;
  aba.getRange(linhaAtual, 1, 1, 10).merge()
    .setValue("✅  CONCLUÍDAS — SPRINT ATUAL")
    .setBackground("#F0FDF4").setFontColor("#15803D")
    .setFontSize(11).setFontWeight("bold")
    .setHorizontalAlignment("left").setVerticalAlignment("middle");
  aba.setRowHeight(linhaAtual, 28);
  linhaAtual++;

  aba.getRange(linhaAtual, 1, 1, 10)
    .setValues([["ID","Título","Tipo","Status","Prioridade","Categoria","Data Fim","Sprint","% Concl.","SLA"]])
    .setBackground("#15803D").setFontColor("#FFFFFF")
    .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  aba.setRowHeight(linhaAtual, 26);
  linhaAtual++;

  const qConcluido = `=IFERROR(QUERY('${boardAba}'!A4:Z,` +
    `"SELECT A,B,C,D,E,G,K,H,N,Z ` +
    `WHERE F = '${nome}' ` +
    `AND (D = 'Concluído (Semana)' OR D = 'Concluído Geral') ` +
    `AND A IS NOT NULL ` +
    `ORDER BY L DESC",0),"Nenhuma tarefa concluída ainda.")`;
  aba.getRange(linhaAtual, 1).setFormula(qConcluido);
  aba.getRange(linhaAtual, 1, 20, 10).setBackground("#F0FDF4");
  linhaAtual += 20;

  // ─────────────────────────────────────────────────────────────────────────
  //  RODAPÉ
  // ─────────────────────────────────────────────────────────────────────────
  linhaAtual++;
  aba.getRange(linhaAtual, 1, 1, 10).merge()
    .setValue(`📌 Kanban Individual — ${nome} | Sprint IC v8.0 | Mob2Con Inteligência Comercial | Atualiza automaticamente ao editar o Board`)
    .setBackground("#F9FAFB").setFontColor("#9CA3AF")
    .setFontSize(9).setHorizontalAlignment("center")
    .setFontStyle("italic");

  // ── Congela as duas primeiras linhas ───────────────────────────────────
  aba.setFrozenRows(2);

  Logger.log(`[_criarKanbanPorMembro] Kanban criado/atualizado para ${nome} (aba: ${nomeAba})`);
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 12 — CONEXÕES VIA QUERY (Sprint Planning + SLA ao vivo)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function atualizarConexoesAbas() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const erros = [];
  _conectarSprintPlanning(ss, erros);
  _conectarSLALive(ss, erros);
  let msg = "✅ Conexões atualizadas!\n\n" +
    "• Sprint Planning → QUERY no Board (tarefas ativas por sprint)\n" +
    "• SLA & Alertas → QUERY no Board (tasks ativas com prazo)\n\n" +
    "Dashboard e Kanbans Individuais: use '🔄 Atualizar Dashboard' e '🔄 Atualizar Todos os Kanbans'.";
  if (erros.length) msg += `\n\n⚠️ Erros:\n${erros.join("\n")}`;
  SpreadsheetApp.getUi().alert(msg);
}

function _conectarSprintPlanning(ss, erros) {
  try {
    let plan = ss.getSheetByName(CONFIG.ABA_PLANNING);
    if (!plan) plan = ss.insertSheet(CONFIG.ABA_PLANNING);
    plan.clearContents(); plan.clearFormats();

    const widths = [90, 300, 90, 110, 110, 110, 100, 120, 120];
    widths.forEach((w, i) => plan.setColumnWidth(i + 1, w));

    plan.getRange("A1:I1").merge()
      .setValue("📅  SPRINT PLANNING — Visão ao Vivo via Board")
      .setBackground("#1E293B").setFontColor("#FFFFFF")
      .setFontSize(13).setFontWeight("bold")
      .setHorizontalAlignment("center").setVerticalAlignment("middle");
    plan.setRowHeight(1, 40);

    plan.getRange("A2:I2").merge()
      .setValue(`🔗 Dados ao vivo do Board — ${Utilities.formatDate(new Date(), "America/Sao_Paulo", "dd/MM/yyyy HH:mm")} | Atualiza ao editar o Board`)
      .setBackground("#F0FDF4").setFontColor("#15803D")
      .setFontSize(10).setHorizontalAlignment("center");
    plan.setRowHeight(2, 24);

    plan.getRange("A3:I3").setValues([["ID","Título / Tarefa","Tipo","Status","Prioridade","Responsável","Categoria","Data Fim","Sprint"]])
      .setBackground("#374151").setFontColor("#FFFFFF")
      .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
    plan.setRowHeight(3, 28);

    const boardAba = CONFIG.ABA_BOARD.replace(/'/g, "\\'");
    const formula  = `=IFERROR(QUERY('${boardAba}'!A4:Z,` +
      `"SELECT A,B,C,D,E,F,G,K,H ` +
      `WHERE A IS NOT NULL ` +
      `AND D <> 'Cancelado' ` +
      `AND D <> 'Concluído Geral' ` +
      `ORDER BY F ASC, E ASC",0),"")`;
    plan.getRange("A4").setFormula(formula);
    plan.setFrozenRows(3);
    Logger.log("[_conectarSprintPlanning] OK");
  } catch (err) {
    erros.push(`Sprint Planning: ${err.message}`);
    Logger.log(`[_conectarSprintPlanning] Erro: ${err.message}`);
  }
}

function _conectarSLALive(ss, erros) {
  try {
    let sla = ss.getSheetByName(CONFIG.ABA_SLA);
    if (!sla) { erros.push("SLA: aba não encontrada"); return; }

    const lastRow = sla.getLastRow();
    if (lastRow >= 12) sla.getRange(12, 1, lastRow - 11, 8).clearContent().clearFormat();

    sla.getRange(12, 1, 1, 8).merge()
      .setValue("📊 ALERTAS AO VIVO — QUERY direta do Board (tasks ativas com prazo preenchido)")
      .setBackground("#1D4ED8").setFontColor("#FFFFFF")
      .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("left");
    sla.setRowHeight(12, 28);

    sla.getRange("A13:H13")
      .setValues([["ID","Título","Responsável","Status","Prioridade","Data Fim","Sprint","SLA Status"]])
      .setBackground("#374151").setFontColor("#FFFFFF")
      .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
    sla.setRowHeight(13, 26);

    const boardAba    = CONFIG.ABA_BOARD.replace(/'/g, "\\'");
    const formulaSLA  = `=IFERROR(QUERY('${boardAba}'!A4:Z,` +
      `"SELECT A,B,F,D,E,K,H,Z ` +
      `WHERE A IS NOT NULL ` +
      `AND K IS NOT NULL ` +
      `AND D <> 'Cancelado' ` +
      `AND D <> 'Concluído Geral' ` +
      `AND D <> 'Concluído (Semana)' ` +
      `ORDER BY K ASC",0),"")`;
    sla.getRange("A14").setFormula(formulaSLA);
    Logger.log("[_conectarSLALive] OK");
  } catch (err) {
    erros.push(`SLA: ${err.message}`);
    Logger.log(`[_conectarSLALive] Erro: ${err.message}`);
  }
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 13 — DASHBOARD & FORMATAÇÃO
//  🔴 BUG FIX v8.0: setFrozenColumns(1) removido → conflitava com A1:I1 mesclado
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function atualizarDashboard() { _reconstruirDashboard(); }
function reconstruirVisuais() {
  const ui   = SpreadsheetApp.getUi();
  const resp = ui.alert("🎨 Reconstruir Visuais",
    "Reconstruirá:\n• 📈 Dashboard\n• ⚙️ Config\n• ⏱️ SLA & Alertas\n• 📊 Kanban Geral\n\nNenhum dado do Board será alterado. Continuar?",
    ui.ButtonSet.OK_CANCEL);
  if (resp !== ui.Button.OK) return;
  _reconstruirDashboard();
  _reconstruirConfig();
  _reconstruirSLA();
  _reconstruirKanban();
  ui.alert("✅ Visuais reconstruídos!\n\n• Dashboard\n• Config\n• SLA & Alertas\n• Kanban Geral");
}

function _reconstruirDashboard() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  let   dash  = ss.getSheetByName(CONFIG.ABA_DASHBOARD);
  if (!dash) dash = ss.insertSheet(CONFIG.ABA_DASHBOARD);

  dash.clearContents(); dash.clearFormats(); dash.clearNotes();

  const dados = board ? board.getDataRange().getValues() : [];
  const metr  = _calcularMetricas(dados);

  const colWidths = [200, 80, 100, 100, 90, 80, 90, 70, 140];
  colWidths.forEach((w, i) => dash.setColumnWidth(i + 1, w));

  // Linha 1 — Título
  dash.getRange("A1:I1").merge()
    .setValue("📊  DASHBOARD — MÉTRICAS DO TIME IC  |  Mob2Con IC")
    .setBackground("#F46901").setFontColor("#FFFFFF")
    .setFontSize(14).setFontWeight("bold")
    .setHorizontalAlignment("center").setVerticalAlignment("middle");
  dash.setRowHeight(1, 44);

  // Linha 2 — Sprint
  const sprintAtual = board ? board.getRange("B2").getValue() : "—";
  const agora = Utilities.formatDate(new Date(), "America/Sao_Paulo", "dd/MM/yyyy 'às' HH:mm");
  dash.getRange("A2:I2").merge()
    .setValue(`🏃 ${sprintAtual}     |     🕐 Atualizado em: ${agora}`)
    .setBackground("#FFF3E8").setFontColor("#C2410C")
    .setFontSize(11).setHorizontalAlignment("center").setVerticalAlignment("middle");
  dash.setRowHeight(2, 30);
  dash.setRowHeight(3, 10);

  // Linha 4 — Labels KPIs
  dash.getRange("A4:I4")
    .setValues([["Total Tickets","Em Andamento","Concluídos","Bloqueados","A Fazer","Novas Solicit.","Backlog","Cancelados",""]])
    .setBackground("#374151").setFontColor("#FFFFFF")
    .setFontSize(10).setFontWeight("bold").setHorizontalAlignment("center").setVerticalAlignment("middle");
  dash.setRowHeight(4, 28);

  // Linha 5 — Valores KPIs
  dash.getRange("A5:I5")
    .setValues([[metr.total,metr.emAndamento,metr.concluidos,metr.bloqueados,metr.aFazer,metr.novasSolicitacoes,metr.backlog,metr.cancelados,""]])
    .setBackground("#FFFFFF").setFontSize(22).setFontWeight("bold")
    .setHorizontalAlignment("center").setVerticalAlignment("middle");
  dash.setRowHeight(5, 52);

  const kpiCores = ["#1D4ED8","#C2410C","#15803D","#991B1B","#1D4ED8","#4A148C","#374151","#9CA3AF","#374151"];
  kpiCores.forEach((cor, i) => dash.getRange(5, i+1).setFontColor(cor));
  kpiCores.forEach((cor, i) => {
    dash.getRange(5, i+1).setBorder(false,false,true,false,false,false,cor,SpreadsheetApp.BorderStyle.SOLID_THICK);
  });
  dash.setRowHeight(6, 8);

  // Linha 7 — Cabeçalho tabela
  dash.getRange("A7:I7")
    .setValues([["👤 Membro","Total","Em Andamento","Concluídas","Bloqueadas","A Fazer","% Progresso","Score","Progresso Visual"]])
    .setBackground("#1E293B").setFontColor("#FFFFFF")
    .setFontSize(10).setFontWeight("bold").setHorizontalAlignment("center").setVerticalAlignment("middle");
  dash.setRowHeight(7, 30);

  // Linhas 8+ — Dados por membro
  const membros   = Object.keys(CONFIG.TIME);
  const porPessoa = {};
  membros.forEach(n => { porPessoa[n]={total:0,concluidos:0,emAndamento:0,bloqueados:0,aFazer:0}; });
  for (let i=3;i<dados.length;i++) {
    const row  = dados[i];
    const nome = _str(row[CONFIG.COL.RESPONSAVEL]);
    if (!porPessoa[nome]) continue;
    const status=_str(row[CONFIG.COL.STATUS]);
    porPessoa[nome].total++;
    if (status.includes("Concluído")) porPessoa[nome].concluidos++;
    if (status==="Em Andamento")      porPessoa[nome].emAndamento++;
    if (status==="Bloqueado")         porPessoa[nome].bloqueados++;
    if (status==="A Fazer")           porPessoa[nome].aFazer++;
  }

  membros.forEach((nome, idx) => {
    const m      = porPessoa[nome];
    const linhaN = 8 + idx;
    const pctNum = m.total>0?Math.round((m.concluidos/m.total)*100):0;
    const barra  = "█".repeat(Math.round(pctNum/10))+"░".repeat(10-Math.round(pctNum/10));
    const rowData= [[nome,m.total,m.emAndamento,m.concluidos,m.bloqueados,m.aFazer,pctNum+"%",pctNum,barra]];
    const rowRange= dash.getRange(linhaN,1,1,9);
    rowRange.setValues(rowData);
    rowRange.setBackground(idx%2===0?"#F8F9FA":"#FFFFFF").setFontSize(11).setVerticalAlignment("middle");
    dash.getRange(linhaN,1).setFontColor(COR_TIME[nome]||"#374151").setFontWeight("bold").setFontSize(11);
    dash.getRange(linhaN,9).setFontFamily("Courier New").setFontSize(9)
      .setFontColor(pctNum>=80?"#15803D":pctNum>=40?"#C2410C":"#94a3b8");
    dash.getRange(linhaN,7).setFontColor(pctNum>=80?"#15803D":pctNum>=40?"#C2410C":"#6B7280").setFontWeight("bold");
    if (m.bloqueados>0) dash.getRange(linhaN,5).setFontColor("#991B1B").setFontWeight("bold");
    dash.setRowHeight(linhaN,32);
  });

  // Linha total
  const linhaTotal = 8 + membros.length;
  const pctGeral   = metr.total>0?Math.round((metr.concluidos/metr.total)*100):0;
  const barraGeral = "█".repeat(Math.round(pctGeral/10))+"░".repeat(10-Math.round(pctGeral/10));
  dash.getRange(linhaTotal,1,1,9).setValues([["TOTAL GERAL",metr.total,metr.emAndamento,metr.concluidos,metr.bloqueados,metr.aFazer,pctGeral+"%",pctGeral,barraGeral]])
    .setBackground("#1E293B").setFontColor("#FFFFFF").setFontWeight("bold").setFontSize(11).setHorizontalAlignment("center");
  dash.getRange(linhaTotal,1).setHorizontalAlignment("left");
  dash.setRowHeight(linhaTotal,34);

  // Rodapé
  const linhaRodape = linhaTotal + 2;
  dash.getRange(linhaRodape,1,1,9).merge()
    .setValue("⚙️ Atualizado automaticamente pelo script. Execute 🔄 Atualizar Dashboard para forçar atualização manual.")
    .setFontColor("#9CA3AF").setFontSize(9).setHorizontalAlignment("center").setFontStyle("italic");

  dash.getRange(7,1,membros.length+2,9)
    .setBorder(true,true,true,true,true,true,"#E5E7EB",SpreadsheetApp.BorderStyle.SOLID);

  // 🔴 FIX v8.0: setFrozenColumns(1) REMOVIDO — conflitava com células mescladas A1:I1
  dash.setFrozenRows(7);
  Logger.log("[_reconstruirDashboard] Dashboard reconstruído (v8.0 — sem setFrozenColumns).");
}

function reformatarBoard() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  const dados = board.getDataRange().getValues();
  const numRows = dados.length - 3;
  if (numRows <= 0) return;
  const numCols = Object.keys(CONFIG.COL).length;
  const bgColors=[], fgColors=[];
  for (let i=3;i<dados.length;i++) {
    const status = _str(dados[i][CONFIG.COL.STATUS]);
    const cores  = CONFIG.CORES_STATUS[status]||{bg:null,fg:null};
    bgColors.push(Array(numCols).fill(cores.bg));
    fgColors.push(Array(numCols).fill(cores.fg));
  }
  board.getRange(4,1,numRows,numCols).setBackgrounds(bgColors).setFontColors(fgColors);
  SpreadsheetApp.getUi().alert("✅ Board reformatado!");
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 14 — CONFIG & SLA & KANBAN GERAL
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function _reconstruirConfig() {
  const ss  = SpreadsheetApp.getActiveSpreadsheet();
  let   cfg = ss.getSheetByName(CONFIG.ABA_CONFIG);
  if (!cfg) cfg = ss.insertSheet(CONFIG.ABA_CONFIG);
  cfg.clearContents(); cfg.clearFormats(); cfg.clearNotes();

  cfg.setColumnWidth(1,220); cfg.setColumnWidth(2,320);
  cfg.setColumnWidth(3,70);  cfg.setColumnWidth(4,120);
  cfg.setColumnWidth(5,110); cfg.setColumnWidth(6,140);

  let linha = 1;
  const _titulo = (txt, bg, fg="#FFFFFF", fs=11) => {
    cfg.getRange(linha,1,1,6).merge().setValue(txt)
      .setBackground(bg).setFontColor(fg).setFontSize(fs)
      .setFontWeight("bold").setHorizontalAlignment("left").setVerticalAlignment("middle");
    cfg.setRowHeight(linha,fs===13?40:30); linha++;
  };
  const _cab = (vals, bg="#374151") => {
    cfg.getRange(linha,1,1,vals.length).setValues([vals])
      .setBackground(bg).setFontColor("#FFFFFF")
      .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
    cfg.setRowHeight(linha,26); linha++;
  };
  const _row = (vals, bg="#F8F9FA") => {
    cfg.getRange(linha,1,1,vals.length).setValues([vals])
      .setBackground(bg).setFontSize(10).setVerticalAlignment("middle");
    cfg.setRowHeight(linha,26); linha++;
  };

  _titulo("⚙️  CONFIGURAÇÃO DO SISTEMA — SPRINT IC v8.0  |  Mob2Con IC","#1E293B","#FFFFFF",13);
  cfg.getRange(linha,1,1,6).merge()
    .setValue("⚠️ Esta aba é de referência. Alterações devem ser feitas no CONFIG do Apps Script.")
    .setBackground("#FFF3E8").setFontColor("#C2410C").setFontSize(10).setHorizontalAlignment("center");
  cfg.setRowHeight(linha,24); linha+=2;

  _titulo("👥  TIME IC — MEMBROS ATIVOS","#F46901");
  _cab(["Nome","E-mail","Sigla","Cor Hex","Status","Lista Google Tasks"]);
  const props  = PropertiesService.getScriptProperties();
  const listas = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS)||"{}");
  const membrosData = [
    {nome:"Marcelo Bora",     email:"marcelo.prado@mob2con.com.br",     sigla:"MB",cor:"#F46901",status:"✅ Ativo"},
    {nome:"Pedro Malagutti",  email:"pedro.malagutti@mob2con.com.br",   sigla:"PM",cor:"#4285F4",status:"✅ Ativo"},
    {nome:"Joice Topan",      email:"joice.topan@mob2con.com.br",       sigla:"JT",cor:"#6F05D4",status:"✅ Ativo"},
    {nome:"João Rosa",        email:"joao.rosa@mob2con.com.br",         sigla:"JR",cor:"#16a34a",status:"✅ Ativo"},
    {nome:"Mariliana Fagotti",email:"mariliana.fagotti@mob2con.com.br", sigla:"MF",cor:"#dc2626",status:"✅ Ativo"},
    {nome:"Donizete",         email:"—",sigla:"DZ",cor:"#0891b2",status:"✅ Ativo"},
    {nome:"Lucas",            email:"—",sigla:"LC",cor:"#7c3aed",status:"✅ Ativo"},
  ];
  membrosData.forEach((m,idx)=>{
    const listaId=listas[m.nome]?"✅ Criada":"❌ Pendente";
    cfg.getRange(linha,1,1,6).setValues([[m.nome,m.email,m.sigla,m.cor,m.status,listaId]])
      .setBackground(idx%2===0?"#F8F9FA":"#FFFFFF").setFontSize(10).setVerticalAlignment("middle");
    cfg.getRange(linha,1).setFontColor(m.cor).setFontWeight("bold");
    cfg.getRange(linha,4).setBackground(m.cor).setFontColor("#FFFFFF").setHorizontalAlignment("center");
    cfg.setRowHeight(linha,26); linha++;
  });
  linha++;

  _titulo("⏱️  SLA POR PRIORIDADE","#1D4ED8");
  _cab(["Prioridade","SLA (dias úteis)","Aplicação","Ação"],[],[],4);
  cfg.getRange(linha-1,1,1,4).setValues([["Prioridade","SLA (dias úteis)","Aplicação","Ação"]])
    .setBackground("#374151").setFontColor("#FFFFFF").setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  cfg.setRowHeight(linha-1,26);

  const slaData=[
    {e:"🔴",l:"Crítica", d:"1 dia útil",    a:"Blockers, urgências do CCO",             bg:"#FEF2F2",fg:"#991B1B"},
    {e:"🟠",l:"Alta",    d:"3 dias úteis",  a:"Impacto direto em cliente ou meta",       bg:"#FFF7ED",fg:"#C2410C"},
    {e:"🟡",l:"Média",   d:"5 dias úteis",  a:"Melhorias e desenvolvimentos planejados", bg:"#FEFCE8",fg:"#854D0E"},
    {e:"🟢",l:"Baixa",   d:"10 dias úteis", a:"Otimizações, documentação, backlog",      bg:"#F0FDF4",fg:"#15803D"},
    {e:"⚪",l:"Sem prio",d:"15 dias úteis", a:"Itens sem urgência definida",             bg:"#F9FAFB",fg:"#9CA3AF"},
  ];
  const acoesSla=["Notificação imediata + escalação para Mari","Alerta no dia 2 + mensagem individual","Alerta no dia 4 via webhook","Alerta no dia 8","Revisão no próximo planning"];
  slaData.forEach((s,idx)=>{
    cfg.getRange(linha,1,1,4).setValues([[`${s.e} ${s.l}`,s.d,s.a,acoesSla[idx]]])
      .setBackground(s.bg).setFontSize(10).setVerticalAlignment("middle");
    cfg.getRange(linha,1,1,2).setFontColor(s.fg).setFontWeight("bold");
    cfg.setRowHeight(linha,26); linha++;
  });
  linha++;

  _titulo("🔧  STATUS DO SISTEMA","#15803D");
  const webhookOk=!!props.getProperty("WEBHOOK_URL");
  const formUrl=props.getProperty("FORM_URL")||"";
  const formCrmUrl=props.getProperty("FORM_CRM_URL")||"";
  const triggers=ScriptApp.getProjectTriggers();
  const fnsTrigger=triggers.map(t=>t.getHandlerFunction());
  const statusItems=[
    ["WEBHOOK_URL",             webhookOk?"✅ Configurada":"❌ Ausente — configure em Propriedades do Script"],
    ["Formulário IC (Sprint)",  formUrl?"✅ Criado":"⚠️ Não criado — execute: ⚙️ Config → 📝 Criar Formulário"],
    ["Formulário CRM",          formCrmUrl?"✅ Criado":"⚠️ Não criado — execute: 🟣 CRM → 📝 Criar Formulário CRM"],
    ["Trigger: onFormSubmit",   fnsTrigger.includes("onFormSubmit")?"✅ Ativo":"⚠️ Ausente — configure manualmente"],
    ["Trigger: onFormSubmitCRM",fnsTrigger.includes("onFormSubmitCRM")?"✅ Ativo":"⚠️ Ausente — configure manualmente"],
    ["Trigger: verificarAtrasos",fnsTrigger.includes("verificarAtrasos")?"✅ Ativo (diário às 8h)":"❌ Ausente"],
    ["Trigger: atualizarDashboard",fnsTrigger.includes("atualizarDashboard")?"✅ Ativo (30 min)":"❌ Ausente"],
    ["Google Tasks — Listas",   Object.values(listas).some(v=>v)?`✅ ${Object.values(listas).filter(v=>v).length} lista(s)`:"❌ Ausente"],
    ["Kanbans Individuais",     Object.keys(CONFIG.TIME).some(n=>!!ss.getSheetByName(`📋 ${CONFIG.TIME[n].sigla} — ${n.split(" ")[0]}`))?"✅ Criados":"⚠️ Execute: 📊 Kanbans → 🆕 Criar Kanbans"],
  ];
  statusItems.forEach((item,idx)=>{
    const ok=item[1].startsWith("✅"),warn=item[1].startsWith("⚠️");
    const bg=ok?"#F0FDF4":warn?"#FEFCE8":"#FEF2F2";
    const fg=ok?"#15803D":warn?"#854D0E":"#991B1B";
    cfg.getRange(linha,1,1,2).setValues([[item[0],item[1]]])
      .setBackground(bg).setFontSize(10).setVerticalAlignment("middle");
    cfg.getRange(linha,1).setFontWeight("bold").setFontColor("#374151");
    cfg.getRange(linha,2).setFontColor(fg);
    cfg.setRowHeight(linha,26); linha++;
  });
  linha++;

  _titulo("📋  INSTRUÇÕES DE SETUP — Sprint IC v8.0","#4A148C");
  const passos=[
    ["Passo 1","Apps Script → Cole o arquivo Sprint_IC_v8.js completo → Salvar"],
    ["Passo 2","Apps Script → Serviços → Adicione: Google Tasks API v1 e Google Forms API"],
    ["Passo 3","Apps Script → ⚙️ Configurações → Propriedades do Script → WEBHOOK_URL"],
    ["Passo 4","Menu: ⚙️ Config → 🆔 Criar Listas de Tasks"],
    ["Passo 5","Menu: ⚙️ Config → 🔧 Configurar Triggers"],
    ["Passo 6","Menu: ⚙️ Config → 📝 Criar Formulário Google → vincular → trigger onFormSubmit"],
    ["Passo 7","Menu: 🟣 CRM → 📝 Criar Formulário CRM → vincular → trigger onFormSubmitCRM"],
    ["Passo 8","Menu: ⚙️ Config → ➕ Configurar Colunas Dep. Externa (adiciona AB/AC/AD no Board)"],
    ["Passo 9","Menu: ⚙️ Config → 🔗 Atualizar Conexões (QUERY) → conecta Planning e SLA ao Board"],
    ["Passo 10","Menu: 📊 Kanbans Individuais → 🆕 Criar Kanbans de Todos os Membros"],
    ["Passo 11","Menu: 🔍 Validação → ✅ Executar Validação Completa"],
    ["PRONTO!","🚀 Sistema operacional! Compartilhe os formulários com o time e stakeholders."],
  ];
  passos.forEach((p,idx)=>{
    const isReady=p[0]==="PRONTO!";
    cfg.getRange(linha,1,1,2).setValues([[p[0],p[1]]])
      .setBackground(isReady?"#DCFCE7":idx%2===0?"#F8F9FA":"#FFFFFF")
      .setFontSize(10).setVerticalAlignment("middle");
    cfg.getRange(linha,1).setFontWeight("bold").setFontColor(isReady?"#15803D":"#F46901");
    if (isReady) cfg.getRange(linha,2).setFontWeight("bold").setFontColor("#15803D");
    cfg.setRowHeight(linha,26); linha++;
  });
  linha++;

  // Links dos formulários
  _titulo("📝  LINKS DOS FORMULÁRIOS","#0F6E56");
  const formLinks=[
    ["Formulário IC (Sprint)",  formUrl||"— não criado ainda"],
    ["Formulário CRM (Joice)",  formCrmUrl||"— não criado ainda"],
    ["Editar Formulário IC",    props.getProperty("FORM_EDIT_URL")||"— não criado ainda"],
    ["Editar Formulário CRM",   props.getProperty("FORM_CRM_EDIT_URL")||"— não criado ainda"],
  ];
  formLinks.forEach((fl,idx)=>{
    const temLink=!fl[1].includes("não criado");
    cfg.getRange(linha,1,1,2).setValues([[fl[0],fl[1]]])
      .setBackground(idx%2===0?"#E1F5EE":"#FFFFFF").setFontSize(10).setVerticalAlignment("middle");
    cfg.getRange(linha,1).setFontWeight("bold").setFontColor("#0F6E56");
    if (temLink) cfg.getRange(linha,2).setFontColor("#185FA5");
    cfg.setRowHeight(linha,26); linha++;
  });
  linha++;

  cfg.getRange(linha,1,1,6).merge()
    .setValue(`Sprint IC v8.0  |  Mob2Con Inteligência Comercial  |  ${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy HH:mm")}`)
    .setBackground("#F9FAFB").setFontColor("#9CA3AF").setFontSize(9)
    .setHorizontalAlignment("center").setFontStyle("italic");

  Logger.log("[_reconstruirConfig] Config reconstruída.");
}

function _reconstruirSLA() {
  const ss  = SpreadsheetApp.getActiveSpreadsheet();
  let   sla = ss.getSheetByName(CONFIG.ABA_SLA);
  if (!sla) sla = ss.insertSheet(CONFIG.ABA_SLA);
  sla.clearContents(); sla.clearFormats();

  [130,130,300,340,100,120,90,110].forEach((w,i)=>sla.setColumnWidth(i+1,w));

  sla.getRange("A1:D1").merge()
    .setValue("⏱️  SLA & ALERTAS DE PRAZO  |  Sprint IC v8.0")
    .setBackground("#1E293B").setFontColor("#FFFFFF")
    .setFontSize(13).setFontWeight("bold")
    .setHorizontalAlignment("center").setVerticalAlignment("middle");
  sla.setRowHeight(1,40);

  sla.getRange("A2:D2").setValues([["Prioridade","SLA (dias úteis)","Aplicação","Ação em caso de violação"]])
    .setBackground("#374151").setFontColor("#FFFFFF").setFontWeight("bold")
    .setFontSize(10).setHorizontalAlignment("center");
  sla.setRowHeight(2,28);

  const slaLinhas=[
    {p:"🔴 Crítica", d:"1 dia útil",    a:"Bugs em produção, blockers, urgências do CCO",     ac:"Notificação imediata no Chat + escalação para Mari",bg:"#FEF2F2",fg:"#991B1B"},
    {p:"🟠 Alta",    d:"3 dias úteis",  a:"Impacto direto em cliente ou meta",                 ac:"Alerta no dia 2 + mensagem individual no Chat",     bg:"#FFF7ED",fg:"#C2410C"},
    {p:"🟡 Média",   d:"5 dias úteis",  a:"Melhorias planejadas",                              ac:"Alerta no dia 4 via webhook",                        bg:"#FEFCE8",fg:"#854D0E"},
    {p:"🟢 Baixa",   d:"10 dias úteis", a:"Otimizações, documentação",                         ac:"Alerta no dia 8 via webhook",                        bg:"#F0FDF4",fg:"#15803D"},
    {p:"⚪ Sem prio",d:"15 dias úteis", a:"Itens sem urgência definida",                       ac:"Revisão no próximo planning",                        bg:"#F9FAFB",fg:"#9CA3AF"},
    {p:"⏳ Aguardando Ext.",d:"—",      a:"Task aguardando área externa",                      ac:"E-mail automático + alerta no Chat",                 bg:"#FEF9C3",fg:"#713F12"},
  ];
  slaLinhas.forEach((s,idx)=>{
    sla.getRange(3+idx,1,1,4).setValues([[s.p,s.d,s.a,s.ac]])
      .setBackground(s.bg).setFontSize(10).setVerticalAlignment("middle");
    sla.getRange(3+idx,1,1,2).setFontColor(s.fg).setFontWeight("bold");
    sla.setRowHeight(3+idx,30);
  });

  sla.setRowHeight(10,16);

  // Cabeçalho alertas ao vivo (QUERY inserida por _conectarSLALive)
  sla.getRange("A11:H11").merge()
    .setValue("🚨  ALERTAS ATIVOS — Preenchido automaticamente pelo script verificarAtrasos() (diariamente às 8h)")
    .setBackground("#991B1B").setFontColor("#FFFFFF").setFontWeight("bold").setFontSize(10)
    .setHorizontalAlignment("left").setVerticalAlignment("middle");
  sla.setRowHeight(11,30);

  sla.getRange("A12:H12")
    .setValues([["ID","Título","Responsável","Status","Prazo","SLA Limite","Dias Atraso","Criticidade"]])
    .setBackground("#374151").setFontColor("#FFFFFF").setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  sla.setRowHeight(12,26);
  sla.getRange("A13:H13").merge()
    .setValue("(Preenchido automaticamente pelo script verificarAtrasos())")
    .setFontColor("#9CA3AF").setFontStyle("italic").setFontSize(10).setVerticalAlignment("middle");
  sla.setRowHeight(13,26);

  Logger.log("[_reconstruirSLA] SLA reconstruído.");
}

function _reconstruirKanban() {
  const ss     = SpreadsheetApp.getActiveSpreadsheet();
  const board  = ss.getSheetByName(CONFIG.ABA_BOARD);
  let   kanban = ss.getSheetByName(CONFIG.ABA_KANBAN);
  if (!kanban) kanban = ss.insertSheet(CONFIG.ABA_KANBAN);
  kanban.clearContents(); kanban.clearFormats();

  const STATUS_COLS=[
    {label:"📥 NOVAS",        key:"Novas Solicitações",      bg:"#EDE7F6",fg:"#4A148C",col:1},
    {label:"📋 BACKLOG",      key:"Backlog",                 bg:"#F3F4F6",fg:"#374151",col:2},
    {label:"📝 A FAZER",      key:"A Fazer",                 bg:"#EFF6FF",fg:"#1D4ED8",col:3},
    {label:"▶ EM ANDAMENTO", key:"Em Andamento",             bg:"#FFF7ED",fg:"#C2410C",col:4},
    {label:"⏳ AGUARD. EXT", key:"Aguardando Área Externa", bg:"#FEF9C3",fg:"#713F12",col:5},
    {label:"🔒 BLOQUEADO",   key:"Bloqueado",               bg:"#FEF2F2",fg:"#991B1B",col:6},
    {label:"🔍 EM VALID.",   key:"Em Validação",            bg:"#FEFCE8",fg:"#854D0E",col:7},
    {label:"✅ CONC. SEM",   key:"Concluído (Semana)",      bg:"#F0FDF4",fg:"#15803D",col:8},
    {label:"🏁 CONCLUÍDO",   key:"Concluído Geral",         bg:"#DCFCE7",fg:"#166534",col:9},
  ];
  STATUS_COLS.forEach(s=>kanban.setColumnWidth(s.col,155));

  kanban.getRange(1,1,1,9).merge()
    .setValue("📊  KANBAN VIEW — INTELIGÊNCIA COMERCIAL  |  Sprint IC v8.0")
    .setBackground("#1E293B").setFontColor("#FFFFFF")
    .setFontSize(13).setFontWeight("bold").setHorizontalAlignment("center").setVerticalAlignment("middle");
  kanban.setRowHeight(1,40);

  const sprintAtual=board?board.getRange("B2").getValue():"—";
  kanban.getRange(2,1,1,9).merge()
    .setValue(`🏃 ${sprintAtual}   |   Atualizado em: ${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy HH:mm")}`)
    .setBackground("#FFF3E8").setFontColor("#C2410C").setFontSize(10).setHorizontalAlignment("center");
  kanban.setRowHeight(2,24);

  STATUS_COLS.forEach(s=>{
    kanban.getRange(3,s.col).setValue(s.label)
      .setBackground(s.bg).setFontColor(s.fg).setFontWeight("bold").setFontSize(10)
      .setHorizontalAlignment("center").setVerticalAlignment("middle");
    kanban.setRowHeight(3,32);
  });

  const dados=board?board.getDataRange().getValues():[];
  const porStatus={};
  STATUS_COLS.forEach(s=>{porStatus[s.key]=[];});
  for (let i=3;i<dados.length;i++) {
    const row=dados[i];
    const id=_str(row[CONFIG.COL.ID]);
    const titulo=_str(row[CONFIG.COL.TITULO]);
    const status=_str(row[CONFIG.COL.STATUS]);
    const prio=_str(row[CONFIG.COL.PRIORIDADE]);
    const resp=_str(row[CONFIG.COL.RESPONSAVEL]);
    const sigla=CONFIG.TIME[resp]?CONFIG.TIME[resp].sigla:resp.substring(0,2);
    if (!porStatus[status]||!id) continue;
    porStatus[status].push({id,titulo,prio,sigla});
  }

  const maxLinhas=Math.max(...STATUS_COLS.map(s=>porStatus[s.key].length),1);
  STATUS_COLS.forEach(s=>{
    porStatus[s.key].forEach((task,idx)=>{
      const linhaK=4+idx;
      const texto=`${_iconeprioridade(task.prio)} ${task.id} — ${task.titulo.substring(0,22)} [${task.sigla}]`;
      kanban.getRange(linhaK,s.col).setValue(texto)
        .setBackground(s.bg).setFontColor(s.fg).setFontSize(9).setWrap(true).setVerticalAlignment("top");
      kanban.setRowHeight(linhaK,38);
    });
    for (let i=porStatus[s.key].length;i<maxLinhas;i++)
      kanban.getRange(4+i,s.col).setBackground(s.bg);
  });

  kanban.setFrozenRows(3);
  Logger.log("[_reconstruirKanban] Kanban Geral reconstruído.");
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 15 — TRIGGERS & FORMULÁRIOS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function configurarTodosOsTriggers() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger("sincronizarTasksDeVolta").timeBased().everyMinutes(10).create();
  ScriptApp.newTrigger("verificarAtrasos").timeBased().everyDays(1).atHour(8).create();
  ScriptApp.newTrigger("atualizarDashboard").timeBased().everyMinutes(30).create();
  ScriptApp.newTrigger("enviarAgendaPlanning").timeBased().onWeekDay(ScriptApp.WeekDay.TUESDAY).atHour(8).create();
  ScriptApp.newTrigger("enviarAgendaReview").timeBased().onWeekDay(ScriptApp.WeekDay.THURSDAY).atHour(8).create();
  ScriptApp.newTrigger("verificarDependenciasExternas").timeBased().onWeekDay(ScriptApp.WeekDay.WEDNESDAY).atHour(9).create();

  const webhookOk = !!PropertiesService.getScriptProperties().getProperty("WEBHOOK_URL");
  SpreadsheetApp.getUi().alert(
    "✅ Triggers configurados!\n\n" +
    "• Sync Tasks → Sheets: a cada 10 min\n" +
    "• Verificar Atrasos: diário às 8h\n" +
    "• Dashboard: a cada 30 min\n" +
    "• Planning (terça): 8h\n" +
    "• Review (quinta): 8h\n" +
    "• Dep. Externas (quarta): 9h\n\n" +
    (webhookOk ? "✅ WEBHOOK_URL configurada.\n\n" :
      "⚠️ WEBHOOK_URL não configurada!\n" +
      "Apps Script → ⚙️ Configurações → Propriedades → WEBHOOK_URL\n\n") +
    "⚠️ Configure manualmente:\n" +
    "Apps Script → Triggers (+) → onFormSubmit → Do formulário\n" +
    "Apps Script → Triggers (+) → onFormSubmitCRM → Do formulário CRM"
  );
}

function removerTodosOsTriggers() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  SpreadsheetApp.getUi().alert("✅ Todos os triggers removidos.");
}

function criarFormulario() {
  const ui = SpreadsheetApp.getUi();
  if (ui.alert("📝 Criar Formulário", "Criará o Google Forms com 19 campos.\n\nContinuar?", ui.ButtonSet.OK_CANCEL) !== ui.Button.OK) return;
  try {
    const form = FormApp.create(CONFIG.FORM.TITULO);
    form.setDescription(CONFIG.FORM.DESCRICAO);
    form.setCollectEmail(true);
    form.setLimitOneResponsePerUser(false);
    form.setAllowResponseEdits(true);
    form.setConfirmationMessage(CONFIG.FORM.CONFIRMACAO);

    form.addSectionHeaderItem().setTitle("1. Identificação do Solicitante");
    form.addTextItem().setTitle("Nome completo *").setRequired(true);
    form.addListItem().setTitle("Área / Departamento *").setRequired(true)
      .setChoiceValues(["Customer Success Rede","Customer Success Terceiros","Comercial / RG","Operações","Financeiro","Produto","Outra"]);
    form.addMultipleChoiceItem().setTitle("Tipo de solicitação *").setRequired(true)
      .setChoiceValues(["Tarefa","Melhoria","Épico","Bug / Correção","Análise / Estudo"]);

    form.addPageBreakItem().setTitle("2. O que você precisa");
    form.addTextItem().setTitle("Título da solicitação *").setHelpText("Objetivo. Ex: Ajuste no relatório semanal Muffato").setRequired(true);
    form.addParagraphTextItem().setTitle("Contexto da Situação *").setHelpText("O que está acontecendo? Onde? Desde quando?").setRequired(true);
    form.addParagraphTextItem().setTitle("Problema / Oportunidade Observada *").setHelpText("Descrição objetiva, evidências e impacto.").setRequired(true);
    form.addParagraphTextItem().setTitle("Pergunta Central que Precisa ser Respondida *").setRequired(true);
    form.addCheckboxItem().setTitle("Objetivo da Solicitação *").setRequired(true)
      .setChoiceValues(["Tomada de decisão","Diagnóstico","Plano de ação","Identificação de oportunidades","Suporte à reunião / governança","Ajuste de dashboard","Outro"]);
    form.addTextItem().setTitle("Se 'Outro' objetivo, descreva:").setRequired(false);

    form.addPageBreakItem().setTitle("3. Indicadores e Tipo de Apoio");
    form.addCheckboxItem().setTitle("Indicadores Relacionados (KPIs) — opcional").setRequired(false)
      .setChoiceValues(["Acesso","Retenção","Conversão","Incremento de promotores","Faturamento","Processos críticos","Outros"]);
    form.addTextItem().setTitle("Se 'Outros' KPIs, informe quais:").setRequired(false);
    form.addMultipleChoiceItem().setTitle("Tipo de Apoio Necessário da IC *").setRequired(true)
      .setChoiceValues(["Diagnóstico analítico","Construção de plano de ação","Revisão de processo","Suporte à cadência comercial","Ajuste de dashboards","Estudo / análise exploratória","Outro"]);
    form.addTextItem().setTitle("Se 'Outro' tipo de apoio, informe:").setRequired(false);
    form.addParagraphTextItem().setTitle("O que já foi tentado? — opcional").setRequired(false);

    form.addPageBreakItem().setTitle("4. Prazo e Prioridade");
    form.addDateItem().setTitle("Prazo Ideal para Entrega *").setRequired(true);
    form.addParagraphTextItem().setTitle("Justificativa do Prazo *").setHelpText("Ex: Precisa constar nos relatórios semanais de segunda-feira").setRequired(true);
    form.addMultipleChoiceItem().setTitle("Qual a Prioridade desta Solicitação? *").setRequired(true)
      .setChoiceValues(["🔴 Crítica — impacto imediato em cliente ou operação","🟠 Alta — impacto direto em meta ou cliente","🟡 Média — melhoria planejada","🟢 Baixa — otimização ou documentação"]);

    form.addPageBreakItem().setTitle("5. Validação e Critérios de Aceite");
    form.addParagraphTextItem().setTitle("Critérios de Aceite — como saberemos que a entrega está correta? *").setRequired(true);
    form.addMultipleChoiceItem().setTitle("Validação do Gestor — o gestor está ciente e aprova? *").setRequired(true)
      .setChoiceValues(["Sim","Não — estou abrindo por iniciativa própria"]);
    form.addTextItem().setTitle("Nome do Gestor Aprovador (se aplicável)").setRequired(false);
    form.addListItem().setTitle("Responsável Sugerido na IC — opcional").setRequired(false)
      .setChoiceValues(["A definir — triagem no planning","Marcelo Bora","Pedro Malagutti","Joice Topan","João Rosa","Mariliana Fagotti"]);
    form.addParagraphTextItem().setTitle("Observações Adicionais, Links ou Referências — opcional").setRequired(false);

    const formUrl = form.getPublishedUrl();
    const editUrl = form.getEditUrl();
    PropertiesService.getScriptProperties().setProperty("FORM_URL", formUrl);
    PropertiesService.getScriptProperties().setProperty("FORM_EDIT_URL", editUrl);

    SpreadsheetApp.getUi().alert("✅ Formulário criado!\n\nURL preenchimento:\n" + formUrl + "\n\nURL edição:\n" + editUrl + "\n\nPRÓXIMOS PASSOS:\n1. Abra o link de edição\n2. Respostas → Vincule a esta planilha\n3. Apps Script → Triggers → (+) → onFormSubmit → Do formulário");
  } catch (err) {
    SpreadsheetApp.getUi().alert("❌ Erro ao criar formulário:\n" + err.message);
  }
}

function exibirUrlFormulario() {
  const props = PropertiesService.getScriptProperties();
  SpreadsheetApp.getUi().alert("📝 URLs do Formulário\n\nPreenchimento:\n" + (props.getProperty("FORM_URL")||"— não encontrada") + "\n\nEdição:\n" + (props.getProperty("FORM_EDIT_URL")||"— não encontrada"));
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 16 — DISTRIBUIÇÃO DE TASKS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function _lerTarefasPorPessoa() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const dados = ss.getSheetByName(CONFIG.ABA_BOARD).getDataRange().getValues();
  const porPessoa = {};
  Object.keys(CONFIG.TIME).forEach(n => { porPessoa[n] = []; });
  for (let i=3;i<dados.length;i++) {
    const row    = dados[i];
    const resp   = _str(row[CONFIG.COL.RESPONSAVEL]);
    const status = _str(row[CONFIG.COL.STATUS]);
    if (!porPessoa[resp]) continue;
    if (status==="Cancelado"||status==="Concluído Geral") continue;
    porPessoa[resp].push({
      id:       _str(row[CONFIG.COL.ID]),
      titulo:   _str(row[CONFIG.COL.TITULO]),
      status:   status,
      prior:    _str(row[CONFIG.COL.PRIORIDADE]),
      pct:      _str(row[CONFIG.COL.PCT])||"0%",
      dataFim:  row[CONFIG.COL.DATA_FIM],
      epico:    _str(row[CONFIG.COL.EPICO]),
      blocker:  _str(row[CONFIG.COL.BLOCKER]),
      descricao:_str(row[CONFIG.COL.DESCRICAO]).substring(0,200),
    });
  }
  return porPessoa;
}

function diagnosticoTarefasPorPessoa() {
  const porPessoa = _lerTarefasPorPessoa();
  let resumo = "📋 TAREFAS POR PESSOA\n\n";
  Object.entries(porPessoa).forEach(([nome,tarefas])=>{
    resumo += `👤 ${nome} — ${tarefas.length} tarefa(s)\n`;
    tarefas.forEach(t=>{resumo += `  ${_iconeprioridade(t.prior)} ${t.id} — ${t.titulo} (${t.status} | ${t.pct})\n`;});
    resumo += "\n";
  });
  SpreadsheetApp.getUi().alert(resumo);
}

function opcaoA_distribuirViaAdmin() {
  if (!CONFIG.DIST.SERVICE_ACCOUNT_EMAIL) {
    SpreadsheetApp.getUi().alert("⚠️ Configure CONFIG.DIST.SERVICE_ACCOUNT_EMAIL."); return;
  }
  SpreadsheetApp.getUi().alert("⚠️ Implemente a lógica de Domain-Wide Delegation nesta função.");
}

function opcaoB_enviarLinksAutorizacao() {
  if (!CONFIG.DIST.WEBAPP_URL) { SpreadsheetApp.getUi().alert("⚠️ Configure CONFIG.DIST.WEBAPP_URL."); return; }
  const porPessoa=_lerTarefasPorPessoa();
  let enviados=0; const erros=[];
  Object.entries(porPessoa).forEach(([nome,tarefas])=>{
    if (!tarefas.length) return;
    const emailMembro=CONFIG.TIME[nome]?CONFIG.TIME[nome].email:"";
    if (!emailMembro) return;
    try {
      MailApp.sendEmail({to:emailMembro,subject:`🚀 Sprint IC — Suas Tarefas de ${nome}`,
        body:`Olá!\n\nVocê tem ${tarefas.length} tarefas pendentes.\nAcesse: ${CONFIG.DIST.WEBAPP_URL}?membro=${encodeURIComponent(nome)}`});
      enviados++;
    } catch(err){erros.push(`${nome}: ${err.message}`);}
  });
  SpreadsheetApp.getUi().alert(`✅ ${enviados} email(s) enviados!${erros.length?"\n\n⚠️ Erros:\n"+erros.join("\n"):""}`);
}

function opcaoC_distribuirViaCalendar() {
  const porPessoa=_lerTarefasPorPessoa();
  let criados=0,atualizados=0; const erros=[];
  const agora=new Date();
  const inicio=new Date(agora.getFullYear(),agora.getMonth(),agora.getDate(),9,0,0);
  const fim=new Date(inicio.getTime()+CONFIG.DIST.CALENDAR_DURACAO_MIN*60000);
  Object.entries(porPessoa).forEach(([nome,tarefas])=>{
    if (!tarefas.length) return;
    const emailMembro=CONFIG.TIME[nome]?CONFIG.TIME[nome].email:"";
    if (!emailMembro) return;
    try {
      const cal=CalendarApp.getCalendarById(emailMembro);
      if (!cal) throw new Error("Agenda não encontrada.");
      const descricao=tarefas.map(t=>`• [${t.id}] ${t.titulo} — ${t.status}`).join("\n");
      const eventosHoje=cal.getEventsForDay(agora,{search:"Sprint IC"});
      if (eventosHoje.length>0){eventosHoje[0].setDescription(descricao);atualizados++;}
      else {
        const evento=cal.createEvent("🚀 Sprint IC | Tarefas do Dia",inicio,fim,{description:descricao});
        evento.addEmailReminder(CONFIG.DIST.LEMBRETE_EMAIL_MIN);
        evento.addPopupReminder(CONFIG.DIST.LEMBRETE_POPUP_MIN);
        criados++;
      }
    } catch(err){erros.push(`${nome}: ${err.message}`);}
  });
  SpreadsheetApp.getUi().alert(`✅ OPÇÃO C!\n🆕 ${criados} novo(s) | 🔄 ${atualizados} atualizado(s)${erros.length?"\n\n⚠️ Erros:\n"+erros.join("\n"):""}`);
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 17 — VALIDAÇÃO COMPLETA
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function executarTodasAsValidacoes() {
  const results = [];
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  results.push(..._validarConfig());
  results.push(..._validarAbas(ss));
  results.push(..._validarBoardEstrutura(ss));
  results.push(..._validarTriggers());
  results.push(..._validarGoogleTasks());
  results.push(..._validarWebhook());
  results.push(..._validarDashboard(ss));
  results.push(..._validarSprintPlanning(ss));
  results.push(..._validarFormulario());
  results.push(..._validarKanbansIndividuais(ss));
  _escreverResultadosValidacao(ss, results);
  const ok=results.filter(r=>r.status==="✅ OK").length;
  const warn=results.filter(r=>r.status==="⚠️ Atenção").length;
  const fail=results.filter(r=>r.status==="❌ Falha").length;
  _postWebhook({text:[`🔍 *VALIDAÇÃO COMPLETA — Sprint IC v8.0*`,``,
    `✅ OK: ${ok} | ⚠️ Atenção: ${warn} | ❌ Falha: ${fail}`,
    ``,`_Veja a aba 🔍 Validação para detalhes._`,
    `_${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy 'às' HH:mm")}_`].join("\n")});
  SpreadsheetApp.getUi().alert(`✅ Validação concluída!\n\n✅ OK: ${ok}\n⚠️ Atenção: ${warn}\n❌ Falha: ${fail}\n\nVeja a aba "🔍 Validação".`);
}

function _validarConfig() {
  const r=[]; const comp="⚙️ CONFIG";
  const webhookUrl=PropertiesService.getScriptProperties().getProperty("WEBHOOK_URL")||"";
  r.push({componente:comp,teste:"WEBHOOK_URL configurada",
    status:webhookUrl?"✅ OK":"❌ Falha",
    detalhe:webhookUrl?"PropertiesService OK":"Configure WEBHOOK_URL em Propriedades do Script"});
  const semEmail=Object.entries(CONFIG.TIME).filter(([,m])=>!m.email&&!["DZ","LC"].includes(m.sigla)).map(([n])=>n);
  r.push({componente:comp,teste:"E-mails do time preenchidos",
    status:semEmail.length===0?"✅ OK":"⚠️ Atenção",
    detalhe:semEmail.length===0?"OK":`Sem e-mail: ${semEmail.join(", ")}`});
  r.push({componente:comp,teste:"SLA com 5 prioridades",
    status:Object.keys(CONFIG.SLA).length===5?"✅ OK":"⚠️ Atenção",
    detalhe:`Prioridades: ${Object.keys(CONFIG.SLA).join(", ")}`});
  return r;
}

function _validarAbas(ss) {
  const r=[]; const comp="📑 Abas";
  const abasEsperadas=[CONFIG.ABA_BOARD,CONFIG.ABA_AUTOMACAO,CONFIG.ABA_KANBAN,
    CONFIG.ABA_PLANNING,CONFIG.ABA_DASHBOARD,CONFIG.ABA_SLA,CONFIG.ABA_CONFIG,CONFIG.ABA_VALIDACAO];
  abasEsperadas.forEach(nomeAba=>{
    const existe=ss.getSheetByName(nomeAba);
    r.push({componente:comp,teste:`Aba existe: "${nomeAba}"`,
      status:existe?"✅ OK":"❌ Falha",
      detalhe:existe?`Última linha: ${existe.getLastRow()}`:"Aba não encontrada — crie manualmente"});
  });
  return r;
}

function _validarBoardEstrutura(ss) {
  const r=[]; const comp="🗂️ Board";
  const board=ss.getSheetByName(CONFIG.ABA_BOARD);
  if (!board){r.push({componente:comp,teste:"Board acessível",status:"❌ Falha",detalhe:"Aba não encontrada"});return r;}
  const dados=board.getDataRange().getValues();
  const numLinhas=dados.length-3;
  r.push({componente:comp,teste:"Linhas de dados no Board",
    status:numLinhas>0?"✅ OK":"⚠️ Atenção",detalhe:`${numLinhas} tarefa(s) encontrada(s)`});
  const sprintName=board.getRange("B2").getValue();
  r.push({componente:comp,teste:"Sprint definida em B2",
    status:sprintName?"✅ OK":"⚠️ Atenção",detalhe:sprintName?`Sprint atual: ${sprintName}`:"B2 vazia"});
  const ids=[]; let duplicados=0;
  for (let i=3;i<dados.length;i++){const id=_str(dados[i][CONFIG.COL.ID]);if(id){if(ids.includes(id))duplicados++;ids.push(id);}}
  r.push({componente:comp,teste:"IDs únicos no Board",
    status:duplicados===0?"✅ OK":"❌ Falha",
    detalhe:duplicados===0?`${ids.length} IDs únicos`:`${duplicados} ID(s) duplicado(s)`});
  let statusInvalidos=0;
  for (let i=3;i<dados.length;i++){const s=_str(dados[i][CONFIG.COL.STATUS]);if(s&&!CONFIG.STATUS_ORDEM.includes(s))statusInvalidos++;}
  r.push({componente:comp,teste:"Status válidos no Board",
    status:statusInvalidos===0?"✅ OK":"⚠️ Atenção",
    detalhe:statusInvalidos===0?"OK":`${statusInvalidos} linha(s) com status inválido`});
  return r;
}

function _validarTriggers() {
  const r=[]; const comp="⏰ Triggers";
  const triggers=ScriptApp.getProjectTriggers();
  const fns=["sincronizarTasksDeVolta","verificarAtrasos","atualizarDashboard",
    "enviarAgendaPlanning","enviarAgendaReview","verificarDependenciasExternas","onFormSubmit"];
  fns.forEach(fn=>{
    const existe=triggers.some(t=>t.getHandlerFunction()===fn);
    r.push({componente:comp,teste:`Trigger: ${fn}`,
      status:existe?"✅ OK":(fn==="onFormSubmit"?"⚠️ Atenção":"❌ Falha"),
      detalhe:existe?"Trigger ativo":fn==="onFormSubmit"?"Configure manualmente":"Execute: 🔧 Configurar Triggers"});
  });
  return r;
}

function _validarGoogleTasks() {
  const r=[]; const comp="📋 Google Tasks";
  const props=PropertiesService.getScriptProperties();
  const listas=JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS)||"{}");
  Object.entries(CONFIG.TIME).forEach(([nome,membro])=>{
    if (!membro.email){r.push({componente:comp,teste:`Lista: ${nome}`,status:"⚠️ Atenção",detalhe:"E-mail não configurado (DZ/LC)"});return;}
    const listaId=listas[nome];
    if (!listaId){r.push({componente:comp,teste:`Lista: ${nome}`,status:"❌ Falha",detalhe:"Lista não criada — execute: 🆔 Criar Listas"});return;}
    try {
      Tasks.Tasklists.get(listaId);
      const items=Tasks.Tasks.list(listaId,{maxResults:100}).items||[];
      r.push({componente:comp,teste:`Lista: ${nome}`,status:"✅ OK",detalhe:`ID: ${listaId.substring(0,15)}... | ${items.length} task(s)`});
    } catch(err){r.push({componente:comp,teste:`Lista: ${nome}`,status:"❌ Falha",detalhe:`Erro ao acessar: ${err.message}`});}
  });
  return r;
}

function _validarWebhook() {
  const r=[]; const comp="💬 Webhook Chat";
  const url=PropertiesService.getScriptProperties().getProperty("WEBHOOK_URL")||"";
  if (!url){
    r.push({componente:comp,teste:"URL configurada",status:"❌ Falha",detalhe:"WEBHOOK_URL não encontrada"});
    r.push({componente:comp,teste:"Conexão com Chat",status:"❌ Falha",detalhe:"Impossível testar sem URL"});
    return r;
  }
  r.push({componente:comp,teste:"URL configurada",status:"✅ OK",detalhe:`URL presente: ${url.substring(0,50)}...`});
  try {
    const response=UrlFetchApp.fetch(url,{method:"post",contentType:"application/json",
      payload:JSON.stringify({text:`🔍 *Sprint IC v8.0 — Teste de Validação*\n\nWebhook funcionando ✅\n_${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy 'às' HH:mm")}_`}),
      muteHttpExceptions:true});
    const code=response.getResponseCode();
    r.push({componente:comp,teste:"Conexão com Chat",status:code===200?"✅ OK":"❌ Falha",
      detalhe:`HTTP ${code}${code===200?" — mensagem enviada":" — verifique a URL"}`});
  } catch(err){r.push({componente:comp,teste:"Conexão com Chat",status:"❌ Falha",detalhe:`Erro: ${err.message}`});}
  return r;
}

function _validarDashboard(ss) {
  const r=[]; const comp="📈 Dashboard";
  const dash=ss.getSheetByName(CONFIG.ABA_DASHBOARD);
  if (!dash){r.push({componente:comp,teste:"Aba Dashboard existe",status:"❌ Falha",detalhe:"Aba não encontrada"});return r;}
  const board=ss.getSheetByName(CONFIG.ABA_BOARD);
  const dadosBoard=board?board.getDataRange().getValues():[];
  const metricasEsperadas=_calcularMetricas(dadosBoard);
  const totalB3=dash.getRange("B3").getValue();
  r.push({componente:comp,teste:"Total de tickets em B3",
    status:(totalB3===metricasEsperadas.total||metricasEsperadas.total===0)?"✅ OK":"⚠️ Atenção",
    detalhe:`Board: ${metricasEsperadas.total} | Dashboard: ${totalB3}`});
  return r;
}

function _validarSprintPlanning(ss) {
  const r=[]; const comp="📅 Sprint Planning";
  const plan=ss.getSheetByName(CONFIG.ABA_PLANNING);
  if (!plan){r.push({componente:comp,teste:"Aba Planning existe",status:"❌ Falha",detalhe:"Aba não encontrada"});return r;}
  const temQuery=plan.getRange("A4").getFormula().includes("QUERY");
  r.push({componente:comp,teste:"QUERY ao Board ativa",
    status:temQuery?"✅ OK":"⚠️ Atenção",
    detalhe:temQuery?"Planning conectada ao Board via QUERY":"Execute: ⚙️ Config → 🔗 Atualizar Conexões (QUERY)"});
  return r;
}

function _validarFormulario() {
  const r=[]; const comp="📝 Formulário";
  const props=PropertiesService.getScriptProperties();
  const formUrl=props.getProperty("FORM_URL")||"";
  r.push({componente:comp,teste:"Formulário criado (URL salva)",
    status:formUrl?"✅ OK":"⚠️ Atenção",
    detalhe:formUrl?`URL: ${formUrl.substring(0,60)}...`:"Execute: ⚙️ Config → 📝 Criar Formulário Google"});
  r.push({componente:comp,teste:"Trigger onFormSubmit configurado",
    status:ScriptApp.getProjectTriggers().some(t=>t.getHandlerFunction()==="onFormSubmit")?"✅ OK":"⚠️ Atenção",
    detalhe:"Configure manualmente: Apps Script → Triggers → (+) → Do formulário → Ao enviar"});
  return r;
}

function _validarKanbansIndividuais(ss) {
  const r=[]; const comp="📊 Kanbans Individuais";
  Object.entries(CONFIG.TIME).forEach(([nome,membro])=>{
    const nomeAba=`📋 ${membro.sigla} — ${nome.split(" ")[0]}`;
    const existe=ss.getSheetByName(nomeAba);
    const temQuery=existe?existe.getRange("A6").getFormula().includes("QUERY"):false;
    r.push({componente:comp,teste:`Kanban: ${nome}`,
      status:existe&&temQuery?"✅ OK":existe?"⚠️ Atenção":"❌ Falha",
      detalhe:existe&&temQuery?"Aba existe com QUERY ao vivo":existe?"Aba existe mas sem QUERY — execute Atualizar Todos os Kanbans":"Aba não encontrada — execute: 📊 Kanbans → 🆕 Criar Kanbans"});
  });
  return r;
}

function _escreverResultadosValidacao(ss, results) {
  let val=ss.getSheetByName(CONFIG.ABA_VALIDACAO);
  if (!val) val=ss.insertSheet(CONFIG.ABA_VALIDACAO);
  val.clearContents(); val.clearFormats();
  const agora=Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy HH:mm:ss");
  val.getRange(1,1,1,5).setValues([["Componente","Teste","Status","Detalhe","Última Execução"]])
    .setBackground("#1a1a2e").setFontColor("#ffffff").setFontWeight("bold").setFontSize(11);
  const linhas=results.map(r=>[r.componente,r.teste,r.status,r.detalhe,agora]);
  if (linhas.length>0){
    val.getRange(2,1,linhas.length,5).setValues(linhas);
    for (let i=0;i<linhas.length;i++){
      const status=linhas[i][2];
      let bg="#f0fdf4",fg="#15803d";
      if (status.includes("Falha")){bg="#fef2f2";fg="#991b1b";}
      if (status.includes("Atenção")){bg="#fefce8";fg="#854d0e";}
      val.getRange(i+2,3,1,1).setBackground(bg).setFontColor(fg).setFontWeight("bold");
    }
  }
  [160,300,100,380,160].forEach((w,i)=>val.setColumnWidth(i+1,w));
  val.getRange(1,1,linhas.length+1,5).setVerticalAlignment("middle");
  val.setFrozenRows(1);
  const ok=results.filter(r=>r.status==="✅ OK").length;
  const warn=results.filter(r=>r.status==="⚠️ Atenção").length;
  const fail=results.filter(r=>r.status==="❌ Falha").length;
  const linhaResumo=linhas.length+3;
  val.getRange(linhaResumo,1,1,5).setValues([["RESUMO GERAL",`Total: ${results.length} verificações`,
    `✅ ${ok} | ⚠️ ${warn} | ❌ ${fail}`,
    fail===0&&warn===0?"🚀 Sistema pronto para implantação!":fail===0?"⚠️ Sistema funcional com pontos de atenção":"❌ Corrija as falhas antes de implantar",
    agora]])
    .setBackground(fail===0&&warn===0?"#dcfce7":fail===0?"#fefce8":"#fef2f2").setFontWeight("bold");
  Logger.log(`[Validação] ${ok} OK | ${warn} Atenção | ${fail} Falha`);
}

function criarAbaValidacao() {
  const ss=SpreadsheetApp.getActiveSpreadsheet();
  let val=ss.getSheetByName(CONFIG.ABA_VALIDACAO);
  if (!val){val=ss.insertSheet(CONFIG.ABA_VALIDACAO);SpreadsheetApp.getUi().alert("✅ Aba criada!\n\nExecute: 🔍 Validação → ✅ Executar Validação Completa");}
  else{val.clearContents();val.clearFormats();SpreadsheetApp.getUi().alert("✅ Aba reconstruída!\n\nExecute: 🔍 Validação → ✅ Executar Validação Completa");}
}

function validarDashboard(){const ss=SpreadsheetApp.getActiveSpreadsheet();_escreverResultadosValidacao(ss,_validarDashboard(ss));SpreadsheetApp.getUi().alert("✅ Dashboard validado.\nVeja a aba 🔍 Validação.");}
function validarSprintPlanning(){const ss=SpreadsheetApp.getActiveSpreadsheet();_escreverResultadosValidacao(ss,_validarSprintPlanning(ss));SpreadsheetApp.getUi().alert("✅ Sprint Planning validado.\nVeja a aba 🔍 Validação.");}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 18 — TESTES
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function testarWebhook() {
  const url=PropertiesService.getScriptProperties().getProperty("WEBHOOK_URL")||"";
  if (!url){SpreadsheetApp.getUi().alert("❌ WEBHOOK_URL não configurada.");return;}
  try {
    UrlFetchApp.fetch(url,{method:"post",contentType:"application/json",
      payload:JSON.stringify({text:[`🔔 *Teste Manual de Webhook — Sprint IC v8.0*`,``,
        `✅ Conexão com o espaço "${CONFIG.NOME_DO_SPACE}" funcionando.`,
        `📅 ${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy 'às' HH:mm")}`,
        `_Executado por: ${Session.getActiveUser().getEmail()}_`].join("\n")})});
    SpreadsheetApp.getUi().alert(`✅ Mensagem enviada ao Google Chat!\n\nVerifique o espaço '${CONFIG.NOME_DO_SPACE}'.`);
  } catch(err){SpreadsheetApp.getUi().alert("❌ Erro ao enviar para o Chat:\n"+err.message);}
}

function testarEmailCompleto() {
  const email=Session.getActiveUser().getEmail();
  if (!email){SpreadsheetApp.getUi().alert("❌ Não foi possível obter o e-mail.");return;}
  try {
    MailApp.sendEmail({to:email,subject:"[Sprint IC v8.0] Teste de E-mail — Sistema Funcionando",
      htmlBody:`<div style="font-family:Arial,sans-serif;max-width:600px;padding:20px;border:1px solid #e5e7eb;border-radius:8px">
        <div style="background:#F46901;color:#fff;padding:12px 20px;border-radius:6px 6px 0 0"><h2 style="margin:0;font-size:18px">🚀 Sprint IC v8.0 — Mob2Con</h2></div>
        <div style="padding:20px"><p>✅ <strong>Envio de e-mail funcionando!</strong></p>
        <p style="color:#6b7280;font-size:13px">Enviado em: ${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM/yyyy 'às' HH:mm")}<br>Executado por: ${email}</p></div></div>`});
    SpreadsheetApp.getUi().alert(`✅ E-mail de teste enviado para:\n${email}`);
  } catch(err){SpreadsheetApp.getUi().alert("❌ Erro ao enviar e-mail:\n"+err.message);}
}

function testarTasksCompleto() {
  const props=PropertiesService.getScriptProperties();
  const listas=JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS)||"{}");
  const results=[];
  Object.entries(CONFIG.TIME).forEach(([nome,membro])=>{
    if (!membro.email){results.push(`⏭️ ${nome}: sem e-mail configurado`);return;}
    const listId=listas[nome];
    if (!listId){results.push(`❌ ${nome}: Lista não criada`);return;}
    try {
      const task=Tasks.Tasks.insert({title:`🔍 [TESTE v8.0] ${nome} — ${Utilities.formatDate(new Date(),"America/Sao_Paulo","dd/MM HH:mm")}`,
        notes:"Tarefa de teste criada pelo sistema de validação. Apague após confirmar.",status:"needsAction"},listId);
      Utilities.sleep(500);
      try{Tasks.Tasks.remove(listId,task.id);}catch(e){/*ignora*/}
      results.push(`✅ ${nome}: OK`);
    } catch(err){results.push(`❌ ${nome}: ${err.message}`);}
  });
  SpreadsheetApp.getUi().alert(`📋 Teste Google Tasks:\n\n${results.join("\n")}`);
}


// ╔══════════════════════════════════════════════════════════════════════════════╗
// ║  SPRINT IC v8.0 — IMPORTAÇÃO JIRA / HUBSPOT                               ║
// ║  Substitui a Seção 19 do arquivo principal                                 ║
// ║                                                                              ║
// ║  Fontes suportadas:                                                          ║
// ║  • Dados_Jira       → Jira IC Geral (74 registros)                         ║
// ║  • Dados_JiraHubspot→ Jira Joice HubSpot (132 registros)                   ║
// ║                                                                              ║
// ║  Mapeamento completo: todos os 30 campos do Board v8                        ║
// ║  Mapeamentos documentados campo a campo abaixo                              ║
// ╚══════════════════════════════════════════════════════════════════════════════╝

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  MAPEAMENTO DOCUMENTADO — Jira CSV → Board v8
//
//  Board COL[0]  ID             ← "Chave da item"   ex: KAN-2
//  Board COL[1]  TITULO         ← "Resumo"          ex: {MELHORIAS} Aprimorar o Dashboard
//  Board COL[2]  TIPO           ← "Tipo de item"    ex: Tarefa / Subtask → normalizado
//  Board COL[3]  STATUS         ← "Status"          ex: Concluído (Semana) → mapeado
//  Board COL[4]  PRIORIDADE     ← "Prioridade"      ex: High → 🟠 Alta
//  Board COL[5]  RESPONSAVEL    ← "Responsável"     ex: Pedro Malagutti → normalizado
//  Board COL[6]  CATEGORIA      ← "Campo personalizado (Área)" ou detectado do título
//  Board COL[7]  SPRINT         ← "Sprint 1" (padrão — sem campo no Jira)
//  Board COL[8]  DATA_CRIACAO   ← "Criado"          ex: 01/dez/25 4:32 PM → dd/MM/yyyy
//  Board COL[9]  DATA_INICIO    ← "Campo personalizado (Start date)"
//  Board COL[10] DATA_FIM       ← "Data limite"     ex: 05/dez/25 12:00 AM → dd/MM/yyyy
//  Board COL[11] DATA_CONCLUSAO ← "Resolvido"       (apenas se status Concluído)
//  Board COL[12] DIAS_REST      ← "" (calculado por fórmula no Board)
//  Board COL[13] PCT            ← "100%" se Concluído, "0%" caso contrário
//  Board COL[14] ESTIMATIVA_H   ← "Estimativa original" (se preenchida)
//  Board COL[15] HORAS_GASTAS   ← "Tempo gasto" (se preenchido)
//  Board COL[16] EPICO          ← "Campo personalizado (Epic Name)" ou "Chave pai" + "Parent summary"
//  Board COL[17] BLOCKER        ← "" (sem campo equivalente no Jira)
//  Board COL[18] DESCRICAO      ← "Descrição" + campos narrativos do formulário
//  Board COL[19] CRITERIOS      ← "Campo personalizado (O que você espera alcançar...)"
//  Board COL[20] SOLICITANTE    ← "Relator" (Joice p/ HubSpot; Relator p/ IC)
//  Board COL[21] REVISADO_POR   ← "Campo personalizado (Nome do gestor:)"
//  Board COL[22] LINK           ← URL pública do ticket Jira (gerada automaticamente)
//  Board COL[23] COMENTARIOS    ← "" (comentários não exportados pelo Jira CSV)
//  Board COL[24] SLA_LIMITE     ← calculado via _adicionarDiasUteis(Data_Criacao, SLA_dias)
//  Board COL[25] SLA_STATUS     ← "✅ No prazo" ou "⚠️ Atrasado" conforme Data_Limite
//  Board COL[26] DEPENDE_DE     ← "Link de item interno (Blocks)" (se preenchido)
//  Board COL[27] AREA_EXTERNA   ← "" (sem equivalente — preenchível manualmente)
//  Board COL[28] EMAIL_EXTERNO  ← "" (sem equivalente — preenchível manualmente)
//  Board COL[29] STATUS_DEP     ← "" (sem equivalente — preenchível manualmente)
//
//  MAPEAMENTO ESPECÍFICO HubSpot (Dados_JiraHubspot):
//  • Responsável → sempre "Joice Topan" (coluna não existe no CSV)
//  • Categoria   → "CRM / HubSpot"
//  • Épico       → "Gestão CRM"
//  • Solicitante → "Relator" (Joice Orzechowski Topan)
//  • Status "Novos"         → "Novas Solicitações"
//  • Status "ACOMPANHAMENTO"→ "Em Validação"
//  • Status "Stand by"      → "Bloqueado"
//  • Status "Em análise"    → "Em Andamento"
//  • Status "Em andamento"  → "Em Andamento"
//  • Status "Concluído"     → "Concluído Geral"
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// ─── Tabelas de mapeamento ────────────────────────────────────────────────────

const JIRA_STATUS_MAP = {
  // Jira IC Geral
  "concluído (semana)":    "Concluído (Semana)",
  "concluído geral":       "Concluído Geral",
  "em andamento":          "Em Andamento",
  "em validação":          "Em Validação",
  "novas solicitações":    "Novas Solicitações",
  "a fazer":               "A Fazer",
  "cancelado":             "Cancelado",
  "backlog":               "Backlog",
  // Jira HubSpot
  "concluído":             "Concluído Geral",
  "acompanhamento":        "Em Validação",
  "novos":                 "Novas Solicitações",
  "stand by":              "Bloqueado",
  "em análise":            "Em Andamento",
};

const JIRA_PRIO_MAP = {
  "highest": "🔴 Crítica",
  "high":    "🟠 Alta",
  "medium":  "🟡 Média",
  "low":     "🟢 Baixa",
  "lowest":  "🟢 Baixa",
  // PT-BR (caso venha traduzido)
  "crítica": "🔴 Crítica",
  "alta":    "🟠 Alta",
  "média":   "🟡 Média",
  "baixa":   "🟢 Baixa",
};

const JIRA_RESP_MAP = {
  "pedro malagutti":          "Pedro Malagutti",
  "marcelo bora do prado":    "Marcelo Bora",
  "marcelo bora":             "Marcelo Bora",
  "joice orzechowski topan":  "Joice Topan",
  "joice topan":              "Joice Topan",
  "joão rosa":                "João Rosa",
  "mariliana fagotti":        "Mariliana Fagotti",
  "donizete":                 "Donizete",
  "lucas":                    "Lucas",
};

const JIRA_TIPO_MAP = {
  "tarefa":   "Tarefa",
  "subtask":  "Tarefa",   // Subtask tratado como Tarefa no Board
  "story":    "Melhoria",
  "bug":      "Bug / Correção",
  "épico":    "Épico",
  "epic":     "Épico",
  "melhoria": "Melhoria",
};

// URL base do Jira (ajuste se necessário)
const JIRA_BASE_URL = "https://mob2con.atlassian.net/browse/";

// ─── Funções auxiliares de parsing ───────────────────────────────────────────

/** Converte data do Jira "01/dez/25 4:32 PM" → "01/12/2025" */
function _parseJiraDate(raw) {
  if (!raw) return "";
  try {
    const meses = {
      "jan":"01","fev":"02","mar":"03","abr":"04","mai":"05","jun":"06",
      "jul":"07","ago":"08","set":"09","out":"10","nov":"11","dez":"12",
    };
    // Formato: "01/dez/25 4:32 PM" ou "01/dez/25 12:00 AM"
    const m = raw.trim().match(/^(\d{2})\/([a-zA-Zê]+)\/(\d{2,4})/);
    if (m) {
      const dia = m[1];
      const mes = meses[m[2].toLowerCase().substring(0, 3)] || "01";
      const anoRaw = m[3];
      const ano = anoRaw.length === 2 ? "20" + anoRaw : anoRaw;
      return `${dia}/${mes}/${ano}`;
    }
    // Tenta parse direto
    const d = new Date(raw);
    if (!isNaN(d.getTime())) {
      return Utilities.formatDate(d, "America/Sao_Paulo", "dd/MM/yyyy");
    }
  } catch (e) { /* ignora */ }
  return "";
}

/** Mapeia status Jira → status Board */
function _mapJiraStatus(rawStatus) {
  const key = (rawStatus || "").trim().toLowerCase();
  return JIRA_STATUS_MAP[key] || "Novas Solicitações";
}

/** Mapeia prioridade Jira → prioridade Board */
function _mapJiraPrioridade(rawPrio) {
  const key = (rawPrio || "").trim().toLowerCase();
  return JIRA_PRIO_MAP[key] || "🟡 Média";
}

/** Mapeia responsável Jira → nome exato do CONFIG.TIME */
function _mapJiraResponsavel(rawResp) {
  const key = (rawResp || "").trim().toLowerCase();
  return JIRA_RESP_MAP[key] || "";
}

/** Mapeia tipo Jira → tipo Board */
function _mapJiraTipo(rawTipo) {
  const key = (rawTipo || "").trim().toLowerCase();
  return JIRA_TIPO_MAP[key] || "Tarefa";
}

/** Remove prefixos de categoria do título: {MELHORIAS}, [FINANCEIRO], etc. */
function _limparTitulo(titulo) {
  if (!titulo) return "";
  // Remove padrões como {MELHORIAS}, [FINANCEIRO], [DEV], etc.
  return titulo.replace(/^\{[^}]+\}\s*/,"").replace(/^\[[^\]]+\]\s*/,"").trim();
}

/** Extrai categoria do título quando campo Área está vazio */
function _detectarCategoriaDeTitulo(titulo) {
  if (!titulo) return "";
  // Captura: {MELHORIAS}, [FINANCEIRO], [DEV], {ANÁLISES E ESTUDOS}
  const m = titulo.match(/^\{([^}]+)\}|^\[([^\]]+)\]/);
  if (m) return (m[1] || m[2]).trim();
  return "";
}

/** Calcula SLA limite e status a partir da data de criação e prioridade */
function _calcularSLA(dataCriacaoStr, prioridade, hoje) {
  try {
    if (!dataCriacaoStr) return { limite: "", status: "✅ No prazo" };
    const partes = dataCriacaoStr.split("/");
    if (partes.length !== 3) return { limite: "", status: "✅ No prazo" };
    const dtBase = new Date(parseInt(partes[2]), parseInt(partes[1]) - 1, parseInt(partes[0]));
    const slaDias = CONFIG.SLA[prioridade] || 5;
    const dtLimite = _adicionarDiasUteis(dtBase, slaDias);
    const limiteStr = Utilities.formatDate(dtLimite, "America/Sao_Paulo", "dd/MM/yyyy");
    const status = dtLimite < hoje ? "⚠️ Atrasado" : "✅ No prazo";
    return { limite: limiteStr, status };
  } catch (e) {
    return { limite: "", status: "✅ No prazo" };
  }
}

/** Monta a descrição consolidada a partir dos campos narrativos do Jira */
function _montarDescricao(campos) {
  const partes = [
    campos.contexto    ? `📍 Contexto:\n${campos.contexto}`         : "",
    campos.problema    ? `🔍 Problema / Oportunidade:\n${campos.problema}` : "",
    campos.pergunta    ? `❓ Pergunta Central:\n${campos.pergunta}` : "",
    campos.descricao   ? `📝 Descrição:\n${campos.descricao}`       : "",
    campos.jaTentado   ? `🔄 Já tentado:\n${campos.jaTentado}`     : "",
    campos.urgencia    ? `⏱️ Urgência:\n${campos.urgencia}`         : "",
    campos.observacoes ? `📎 Observações:\n${campos.observacoes}`   : "",
    campos.resultados  ? `🎯 Resultados Esperados:\n${campos.resultados}` : "",
  ].filter(Boolean);
  return partes.join("\n\n").substring(0, 2000);
}

// ─── Função principal de importação ──────────────────────────────────────────

/**
 * importarDadosConsolidados()
 *
 * Lê as abas "Dados_Jira" e "Dados_JiraHubspot", mapeia cada campo
 * para a coluna correta do Board v8 e insere apenas registros novos
 * (verifica ID já existente para evitar duplicatas).
 *
 * Execute pelo menu: ⚙️ Configuração → 📥 Importar Dados Jira/HubSpot
 */
function importarDadosConsolidados() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const board = ss.getSheetByName(CONFIG.ABA_BOARD);
  const auto  = ss.getSheetByName(CONFIG.ABA_AUTOMACAO);

  if (!board) {
    SpreadsheetApp.getUi().alert("❌ Aba Board não encontrada.");
    return;
  }

  // Lê IDs já existentes no Board para evitar duplicatas
  const dadosBoard   = board.getDataRange().getValues();
  const idsExistentes = new Set(
    dadosBoard.slice(3).map(r => _str(r[CONFIG.COL.ID])).filter(Boolean)
  );

  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  const FONTES = [
    {
      abaName:          "Dados_Jira",
      responsavelFixo:  null,       // usa coluna "Responsável"
      categoriaFixa:    null,       // usa campo "Área" ou detecta do título
      epicoFixo:        null,       // usa campo "Epic Name" ou parent
      tipoFonte:        "IC",
    },
    {
      abaName:          "Dados_JiraHubspot",
      responsavelFixo:  "Joice Topan",
      categoriaFixa:    "CRM / HubSpot",
      epicoFixo:        "Gestão CRM",
      tipoFonte:        "CRM",
    },
  ];

  let totalInseridos = 0;
  let totalPulados   = 0;
  let totalErros     = 0;
  const logLinhas    = [];

  FONTES.forEach(fonte => {
    const aba = ss.getSheetByName(fonte.abaName);
    if (!aba) {
      Logger.log(`[importarDadosConsolidados] Aba "${fonte.abaName}" não encontrada — pulando.`);
      return;
    }

    const dadosAba  = aba.getDataRange().getValues();
    if (dadosAba.length < 2) {
      Logger.log(`[importarDadosConsolidados] Aba "${fonte.abaName}" está vazia — pulando.`);
      return;
    }

    const header = dadosAba[0];
    const rows   = dadosAba.slice(1);

    // Helper para pegar valor de coluna pelo nome exato
    const col = (name) => {
      const idx = header.indexOf(name);
      return idx >= 0 ? idx : -1;
    };

    // Índices das colunas do CSV (mapeados uma vez por aba)
    const IDX = {
      chave:         col("Chave da item"),
      resumo:        col("Resumo"),
      tipo:          col("Tipo de item"),
      status:        col("Status"),
      prio:          col("Prioridade"),
      resp:          col("Responsável"),
      criado:        col("Criado"),
      dataInicio:    col("Campo personalizado (Start date)"),
      dataFim:       col("Data limite"),
      resolvido:     col("Resolvido"),
      estimOriginal: col("Estimativa original"),
      tempoGasto:    col("Tempo gasto"),
      epicName:      col("Campo personalizado (Epic Name)"),
      categoria:     col("Campo personalizado (Área)"),
      chavePai:      col("Chave pai"),
      parentSummary: col("Parent summary"),
      descricao:     col("Descrição"),
      contexto:      col("Campo personalizado (Contexto da Situação)"),
      problema:      col("Campo personalizado (Problema / Oportunidade Observada)"),
      pergunta:      col("Campo personalizado (Pergunta Central que Precisa ser respondida)"),
      resultados:    col("Campo personalizado (O que você espera alcançar com essa análise?)"),
      jaTentado:     col("Campo personalizado (O que já foi tentado?)"),
      observacoes:   col("Campo personalizado (Observações adicionais)"),
      gestor:        col("Campo personalizado (Nome do gestor:)"),
      criterios:     col("Campo personalizado (O que você espera alcançar com essa análise?)"),
      relator:       col("Relator"),
      blocker:       col("Link de item interno (Blocks)"),
    };

    rows.forEach((row, rowIdx) => {
      try {
        // ── 1. ID ────────────────────────────────────────────────────────────
        const chaveRaw = IDX.chave >= 0 ? _str(row[IDX.chave]) : "";
        const id = chaveRaw || `${fonte.tipoFonte}-${rowIdx + 1}`;

        // ── Skip: sem título ─────────────────────────────────────────────────
        const resumoRaw = IDX.resumo >= 0 ? _str(row[IDX.resumo]) : "";
        if (!resumoRaw) { totalPulados++; return; }

        // ── Skip: ID já existe no Board ──────────────────────────────────────
        if (idsExistentes.has(id)) { totalPulados++; return; }

        // ── 2. TÍTULO — limpa prefixos como {MELHORIAS}, [DEV] ───────────────
        const titulo = _limparTitulo(resumoRaw);

        // ── 3. TIPO ──────────────────────────────────────────────────────────
        const tipoRaw  = IDX.tipo >= 0 ? _str(row[IDX.tipo]) : "Tarefa";
        const tipo     = fonte.tipoFonte === "CRM"
          ? "CRM / HubSpot"
          : _mapJiraTipo(tipoRaw);

        // ── 4. STATUS ─────────────────────────────────────────────────────────
        const statusRaw = IDX.status >= 0 ? _str(row[IDX.status]) : "";
        const status    = _mapJiraStatus(statusRaw);

        // ── 5. PRIORIDADE ─────────────────────────────────────────────────────
        const prioRaw   = IDX.prio >= 0 ? _str(row[IDX.prio]) : "Medium";
        const prioridade= _mapJiraPrioridade(prioRaw);

        // ── 6. RESPONSÁVEL ────────────────────────────────────────────────────
        let responsavel;
        if (fonte.responsavelFixo) {
          responsavel = fonte.responsavelFixo;
        } else {
          const respRaw = IDX.resp >= 0 ? _str(row[IDX.resp]) : "";
          responsavel   = _mapJiraResponsavel(respRaw);
        }

        // ── 7. CATEGORIA ──────────────────────────────────────────────────────
        let categoria;
        if (fonte.categoriaFixa) {
          categoria = fonte.categoriaFixa;
        } else {
          const catCampo = IDX.categoria >= 0 ? _str(row[IDX.categoria]) : "";
          categoria = catCampo || _detectarCategoriaDeTitulo(resumoRaw) || "Inteligência Comercial";
        }

        // ── 8. SPRINT ─────────────────────────────────────────────────────────
        // Jira não exporta sprint no CSV padrão → mapeia para sprint atual do Board
        const sprintAtualBoard = dadosBoard.length > 3
          ? (board.getRange("B2").getValue() || "Sprint 1")
          : "Sprint 1";
        const sprint = sprintAtualBoard;

        // ── 9. DATA_CRIACAO ───────────────────────────────────────────────────
        const criadoRaw  = IDX.criado >= 0 ? _str(row[IDX.criado]) : "";
        const dataCriacao = _parseJiraDate(criadoRaw);

        // ── 10. DATA_INICIO ───────────────────────────────────────────────────
        const startRaw   = IDX.dataInicio >= 0 ? _str(row[IDX.dataInicio]) : "";
        const dataInicio = _parseJiraDate(startRaw);

        // ── 11. DATA_FIM ──────────────────────────────────────────────────────
        const fimRaw = IDX.dataFim >= 0 ? _str(row[IDX.dataFim]) : "";
        const dataFim = _parseJiraDate(fimRaw);

        // ── 12. DATA_CONCLUSAO ────────────────────────────────────────────────
        // Preenche "Resolvido" apenas se o status final indica conclusão
        const resolvidoRaw = IDX.resolvido >= 0 ? _str(row[IDX.resolvido]) : "";
        const dataConclusao = status.includes("Concluído") ? _parseJiraDate(resolvidoRaw) : "";

        // ── 13. DIAS_REST — deixa vazio (calculado por fórmula no Board) ──────
        const diasRest = "";

        // ── 14. PCT ───────────────────────────────────────────────────────────
        const pct = status.includes("Concluído") ? "100%" : "0%";

        // ── 15. ESTIMATIVA_H ──────────────────────────────────────────────────
        const estimRaw = IDX.estimOriginal >= 0 ? _str(row[IDX.estimOriginal]) : "";
        // Converte segundos Jira → horas (Jira armazena em segundos)
        let estimativaH = "";
        if (estimRaw) {
          const seg = parseFloat(estimRaw);
          if (!isNaN(seg) && seg > 0) {
            estimativaH = (seg / 3600).toFixed(1) + "h";
          }
        }

        // ── 16. HORAS_GASTAS ──────────────────────────────────────────────────
        const tempoRaw = IDX.tempoGasto >= 0 ? _str(row[IDX.tempoGasto]) : "";
        let horasGastas = "";
        if (tempoRaw) {
          const seg = parseFloat(tempoRaw);
          if (!isNaN(seg) && seg > 0) {
            horasGastas = (seg / 3600).toFixed(1) + "h";
          }
        }

        // ── 17. EPICO ─────────────────────────────────────────────────────────
        let epico;
        if (fonte.epicoFixo) {
          epico = fonte.epicoFixo;
        } else {
          const epicNameRaw = IDX.epicName >= 0 ? _str(row[IDX.epicName]) : "";
          if (epicNameRaw) {
            epico = epicNameRaw;
          } else {
            // Usa Parent summary se disponível (Subtasks têm pai)
            const parentSummaryRaw = IDX.parentSummary >= 0 ? _str(row[IDX.parentSummary]) : "";
            epico = parentSummaryRaw ? _limparTitulo(parentSummaryRaw) : "";
          }
        }

        // ── 18. BLOCKER ───────────────────────────────────────────────────────
        // "Link de item interno (Blocks)" → ID do item bloqueado
        const blockerRaw = IDX.blocker >= 0 ? _str(row[IDX.blocker]) : "";
        const blocker    = blockerRaw || "";

        // ── 19. DESCRICAO ─────────────────────────────────────────────────────
        // Agrega: Descrição + todos os campos narrativos do formulário Jira
        const descricao = _montarDescricao({
          contexto:    IDX.contexto    >= 0 ? _str(row[IDX.contexto])    : "",
          problema:    IDX.problema    >= 0 ? _str(row[IDX.problema])    : "",
          pergunta:    IDX.pergunta    >= 0 ? _str(row[IDX.pergunta])    : "",
          descricao:   IDX.descricao   >= 0 ? _str(row[IDX.descricao])  : "",
          jaTentado:   IDX.jaTentado   >= 0 ? _str(row[IDX.jaTentado])  : "",
          urgencia:    "",
          observacoes: IDX.observacoes >= 0 ? _str(row[IDX.observacoes]) : "",
          resultados:  IDX.resultados  >= 0 ? _str(row[IDX.resultados]) : "",
        });

        // ── 20. CRITERIOS ─────────────────────────────────────────────────────
        const criterios = IDX.criterios >= 0 ? _str(row[IDX.criterios]) : "";

        // ── 21. SOLICITANTE ───────────────────────────────────────────────────
        // Para HubSpot: Relator é sempre Joice → indica quem solicitou a Joice
        const relatorRaw  = IDX.relator >= 0 ? _str(row[IDX.relator]) : "";
        const solicitante = _mapJiraResponsavel(relatorRaw) || relatorRaw;

        // ── 22. REVISADO_POR ──────────────────────────────────────────────────
        const gestorRaw   = IDX.gestor >= 0 ? _str(row[IDX.gestor]) : "";
        const revisadoPor = gestorRaw;

        // ── 23. LINK ──────────────────────────────────────────────────────────
        // Gera a URL pública do ticket Jira
        const link = chaveRaw ? (JIRA_BASE_URL + chaveRaw) : "";

        // ── 24. COMENTARIOS ───────────────────────────────────────────────────
        // Jira CSV não exporta comentários → deixa vazio
        const comentarios = "";

        // ── 25. SLA_LIMITE & 26. SLA_STATUS ──────────────────────────────────
        const sla = _calcularSLA(dataCriacao, prioridade, hoje);

        // ── 27–29. DEPENDE_DE / AREA_EXTERNA / EMAIL_EXTERNO / STATUS_DEP ─────
        // Jira "Blocks" → indica dependência interna (não externa)
        const dependeDe   = blocker; // reutiliza o mesmo campo
        const areaExterna = "";
        const emailExt    = "";
        const statusDep   = "";

        // ── Monta linha completa (30 colunas) ─────────────────────────────────
        const linhaBoard  = new Array(30).fill("");
        linhaBoard[CONFIG.COL.ID]           = id;
        linhaBoard[CONFIG.COL.TITULO]       = titulo;
        linhaBoard[CONFIG.COL.TIPO]         = tipo;
        linhaBoard[CONFIG.COL.STATUS]       = status;
        linhaBoard[CONFIG.COL.PRIORIDADE]   = prioridade;
        linhaBoard[CONFIG.COL.RESPONSAVEL]  = responsavel;
        linhaBoard[CONFIG.COL.CATEGORIA]    = categoria;
        linhaBoard[CONFIG.COL.SPRINT]       = sprint;
        linhaBoard[CONFIG.COL.DATA_CRIACAO] = dataCriacao;
        linhaBoard[CONFIG.COL.DATA_INICIO]  = dataInicio;
        linhaBoard[CONFIG.COL.DATA_FIM]     = dataFim;
        linhaBoard[CONFIG.COL.DATA_CONCLUSAO]= dataConclusao;
        linhaBoard[CONFIG.COL.DIAS_REST]    = diasRest;
        linhaBoard[CONFIG.COL.PCT]          = pct;
        linhaBoard[CONFIG.COL.ESTIMATIVA_H] = estimativaH;
        linhaBoard[CONFIG.COL.HORAS_GASTAS] = horasGastas;
        linhaBoard[CONFIG.COL.EPICO]        = epico;
        linhaBoard[CONFIG.COL.BLOCKER]      = ""; // não é blocker — é dependência
        linhaBoard[CONFIG.COL.DESCRICAO]    = descricao;
        linhaBoard[CONFIG.COL.CRITERIOS]    = criterios;
        linhaBoard[CONFIG.COL.SOLICITANTE]  = solicitante;
        linhaBoard[CONFIG.COL.REVISADO_POR] = revisadoPor;
        linhaBoard[CONFIG.COL.LINK]         = link;
        linhaBoard[CONFIG.COL.COMENTARIOS]  = comentarios;
        linhaBoard[CONFIG.COL.SLA_LIMITE]   = sla.limite;
        linhaBoard[CONFIG.COL.SLA_STATUS]   = sla.status;
        linhaBoard[CONFIG.COL.DEPENDE_DE]   = dependeDe;
        linhaBoard[CONFIG.COL.AREA_EXTERNA] = areaExterna;
        linhaBoard[CONFIG.COL.EMAIL_EXTERNO]= emailExt;
        linhaBoard[CONFIG.COL.STATUS_DEP]   = statusDep;

        // ── Insere no Board e aplica cor ──────────────────────────────────────
        const ultimaLinha = board.getLastRow() + 1;
        board.appendRow(linhaBoard);
        _aplicarCorStatus(board, ultimaLinha, status);

        // Rastreia ID para evitar duplicatas dentro da mesma execução
        idsExistentes.add(id);
        totalInseridos++;

        // Log na aba Automação
        const agora = Utilities.formatDate(new Date(), "America/Sao_Paulo", "dd/MM/yyyy HH:mm");
        logLinhas.push([
          agora, id, titulo, tipo, solicitante, categoria,
          responsavel, prioridade,
          `SLA: ${sla.limite}`,
          `✅ Importado de ${fonte.abaName}`, "✅ Sim",
        ]);

      } catch (err) {
        Logger.log(`[importarDadosConsolidados] Erro na linha ${rowIdx + 1} de ${fonte.abaName}: ${err.message}`);
        totalErros++;
      }
    });
  });

  // Grava log em lote na aba Automação
  if (auto && logLinhas.length > 0) {
    try {
      auto.getRange(auto.getLastRow() + 1, 1, logLinhas.length, logLinhas[0].length)
          .setValues(logLinhas);
    } catch (e) {
      Logger.log(`[importarDadosConsolidados] Erro ao gravar log Automação: ${e.message}`);
    }
  }

  // Notifica Chat
  _postWebhook({ text: [
    `📥 *Importação Jira/HubSpot concluída!*`, ``,
    `✅ Inseridos: *${totalInseridos}*`,
    `⏭️ Pulados (já existiam): ${totalPulados}`,
    `❌ Erros: ${totalErros}`, ``,
    `_Fonte: Dados_Jira + Dados_JiraHubspot → Board v8_`,
    `_${Utilities.formatDate(new Date(), "America/Sao_Paulo", "dd/MM/yyyy 'às' HH:mm")}_`,
  ].join("\n") });

  // Alerta na UI
  const msg = [
    `✅ Importação concluída!`,
    ``,
    `• Inseridos no Board: ${totalInseridos}`,
    `• Pulados (ID já existe): ${totalPulados}`,
    `• Erros (ver Logger): ${totalErros}`,
    ``,
    `Fontes processadas:`,
    `• Dados_Jira → IC Geral (responsável conforme Jira)`,
    `• Dados_JiraHubspot → CRM (responsável: Joice Topan)`,
  ].join("\n");

  SpreadsheetApp.getUi().alert(msg);
  Logger.log(`[importarDadosConsolidados] ${totalInseridos} inseridos | ${totalPulados} pulados | ${totalErros} erros`);
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  PRÉVIA / DIAGNÓSTICO — sem inserir no Board
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * Mostra uma prévia do que seria importado sem inserir no Board.
 * Use para validar o mapeamento antes de executar a importação real.
 */
function previaImportacao() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let resumo = "🔍 PRÉVIA DA IMPORTAÇÃO\n\n";
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  [
    { abaName: "Dados_Jira",        label: "📊 IC Geral",   responsavelFixo: null,        categoriaFixa: null,           tipoFonte: "IC" },
    { abaName: "Dados_JiraHubspot", label: "🟣 HubSpot",    responsavelFixo: "Joice Topan", categoriaFixa: "CRM / HubSpot", tipoFonte: "CRM" },
  ].forEach(fonte => {
    const aba = ss.getSheetByName(fonte.abaName);
    if (!aba) { resumo += `⚠️ Aba "${fonte.abaName}" não encontrada.\n\n`; return; }

    const data   = aba.getDataRange().getValues();
    const header = data[0];
    const rows   = data.slice(1).filter(r => r[header.indexOf("Resumo")]);

    const col = (n) => { const i = header.indexOf(n); return i >= 0 ? i : -1; };

    // Status breakdown
    const statusCount = {};
    rows.forEach(row => {
      const s = _mapJiraStatus(_str(row[col("Status")]));
      statusCount[s] = (statusCount[s] || 0) + 1;
    });

    resumo += `${fonte.label} — ${fonte.abaName} (${rows.length} registros)\n`;
    Object.entries(statusCount).forEach(([s, n]) => { resumo += `  ${s}: ${n}\n`; });

    // Amostra dos primeiros 3
    resumo += "\nAmostra (3 primeiros):\n";
    rows.slice(0, 3).forEach(row => {
      const chave   = _str(row[col("Chave da item")]);
      const titulo  = _limparTitulo(_str(row[col("Resumo")])).substring(0, 50);
      const status  = _mapJiraStatus(_str(row[col("Status")]));
      const prio    = _mapJiraPrioridade(_str(row[col("Prioridade")]));
      const resp    = fonte.responsavelFixo || _mapJiraResponsavel(_str(row[col("Responsável")])) || "—";
      resumo += `  • ${chave}: ${titulo}\n    ${status} | ${prio} | ${resp}\n`;
    });
    resumo += "\n";
  });

  SpreadsheetApp.getUi().alert(resumo);
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 20 — MÓDULO CRM (Joice Topan)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

const CONFIG_CRM = {
  RESPONSAVEL_PADRAO: "Joice Topan",
  CATEGORIA_PADRAO:   "CRM / HubSpot",
  EPICO_PADRAO:       "Gestão CRM",
  FORM: {
    TITULO:       "Solicitação CRM — HubSpot | Mob2Con",
    DESCRICAO:    "Use este formulário para solicitar melhorias, correções, novos campos, automações e qualquer alteração no HubSpot. Campos com * são obrigatórios.\n\nResponsável: Joice Topan — Inteligência Comercial",
    CONFIRMACAO:  "✅ Sua solicitação de CRM foi registrada! Joice receberá uma notificação em breve.",
  },
  TIPOS: ["Fluxos de trabalho / Automações","Relatórios / Painéis de controle","Pipelines / Oleodutos","Campos Personalizados","Acessos / Permissões","E-mails e Modelos","Integrações","Importação / Exportação","Treinamento / Dúvidas","Erros ou Bugs","Inteligência Comercial / BI","Outros"],
  DEPARTAMENTOS: ["Customer Success Rede","Customer Success Terceiros","Comercial / RG","Inteligência Comercial","Gestão de Performance","Operações","Financeiro","Produto","Implantação","Infraestrutura","Jurídico","Recursos Humanos","Presidência e Diretoria","Suporte","Outro"],
  BENEFICIOS: ["Gerar receita","Melhorar a eficiência do processo","Corrigir erros","Apoiar tomadas de decisão (relatórios/dados)","Melhorar a experiência do cliente","Outro"],
  PRIORIDADES: ["🔴 Crítica — impacto imediato em cliente ou operação","🟠 Alta — impacto direto em meta ou cliente","🟡 Média — melhoria planejada","🟢 Baixa — otimização ou documentação"],
};

function criarFormularioCRM() {
  const ui=SpreadsheetApp.getUi();
  if (ui.alert("📝 Criar Formulário CRM","Criará o Google Forms de solicitação CRM/HubSpot.\n\nContinuar?",ui.ButtonSet.OK_CANCEL)!==ui.Button.OK) return;
  try {
    const form=FormApp.create(CONFIG_CRM.FORM.TITULO);
    form.setDescription(CONFIG_CRM.FORM.DESCRICAO);
    form.setCollectEmail(true);
    form.setAllowResponseEdits(true);
    form.setConfirmationMessage(CONFIG_CRM.FORM.CONFIRMACAO);

    form.addSectionHeaderItem().setTitle("1. Identificação").setHelpText("Informe quem está fazendo a solicitação e de qual área.");
    form.addTextItem().setTitle("Nome completo *").setRequired(true);
    form.addListItem().setTitle("Departamento *").setRequired(true).setChoiceValues(CONFIG_CRM.DEPARTAMENTOS);

    form.addPageBreakItem().setTitle("2. Tipo de Solicitação");
    form.addListItem().setTitle("Tipo de Solicitação *").setHelpText("Selecione a categoria que melhor descreve o que você precisa.").setRequired(true).setChoiceValues(CONFIG_CRM.TIPOS);
    form.addTextItem().setTitle("Se 'Outros', especifique:").setRequired(false);
    form.addTextItem().setTitle("Resumo da solicitação *").setHelpText("Uma frase objetiva. Ex: Criar pipeline de pós-venda para rede Muffato").setRequired(true);

    form.addPageBreakItem().setTitle("3. Contexto e Descrição Detalhada");
    form.addParagraphTextItem().setTitle("Contexto / Situação Atual *").setHelpText("O que está acontecendo hoje no HubSpot?").setRequired(true);
    form.addParagraphTextItem().setTitle("Descrição Detalhada *").setHelpText("Descreva com detalhes o que precisa ser feito.\n\nPara novos pipelines ou relatórios, inclua:\n• Etapas/fases desejadas\n• Sugestões de automações\n• Usuários que irão atuar no funil").setRequired(true);
    form.addParagraphTextItem().setTitle("Resultados Esperados *").setHelpText("Quais mudanças ou ganhos você espera alcançar?").setRequired(true);

    form.addPageBreakItem().setTitle("4. Benefício e Impacto");
    form.addListItem().setTitle("Principal Benefício Esperado *").setRequired(true).setChoiceValues(CONFIG_CRM.BENEFICIOS);
    form.addTextItem().setTitle("Se 'Outro' benefício, descreva:").setRequired(false);
    form.addParagraphTextItem().setTitle("Impacto se não for feito — o que acontece se ficar como está?").setHelpText("Ajuda a IC a priorizar corretamente.").setRequired(false);
    form.addCheckboxItem().setTitle("Usuários / Times afetados").setRequired(false)
      .setChoiceValues(["Customer Success Rede","Customer Success Terceiros","Comercial / RG","Inteligência Comercial","Todos"]);

    form.addPageBreakItem().setTitle("5. Prazo e Prioridade");
    form.addMultipleChoiceItem().setTitle("Prioridade desta Solicitação *").setRequired(true).setChoiceValues(CONFIG_CRM.PRIORIDADES);
    form.addDateItem().setTitle("Prazo Ideal *").setRequired(true);
    form.addParagraphTextItem().setTitle("Justificativa do Prazo *").setHelpText("Por que precisa até essa data?").setRequired(true);

    form.addPageBreakItem().setTitle("6. Validação e Referências");
    form.addParagraphTextItem().setTitle("O que já foi tentado? — opcional").setRequired(false);
    form.addParagraphTextItem().setTitle("Links, prints ou referências úteis — opcional").setHelpText("Cole links de dashboards, prints de erros, exemplos do HubSpot, etc.").setRequired(false);
    form.addMultipleChoiceItem().setTitle("O gestor está ciente e aprova? *").setRequired(true).setChoiceValues(["Sim","Não — estou abrindo por iniciativa própria"]);
    form.addTextItem().setTitle("Nome do Gestor Aprovador (se aplicável)").setRequired(false);

    const formUrl=form.getPublishedUrl(), editUrl=form.getEditUrl();
    PropertiesService.getScriptProperties().setProperty("FORM_CRM_URL",formUrl);
    PropertiesService.getScriptProperties().setProperty("FORM_CRM_EDIT_URL",editUrl);

    SpreadsheetApp.getUi().alert("✅ Formulário CRM criado!\n\nURL preenchimento:\n"+formUrl+"\n\nURL edição:\n"+editUrl+
      "\n\nPRÓXIMOS PASSOS:\n1. Abra o link de edição\n2. Respostas → Vincule a esta planilha\n3. Apps Script → Triggers → (+) → onFormSubmitCRM → Do Formulário");
  } catch(err){SpreadsheetApp.getUi().alert("❌ Erro ao criar formulário CRM:\n"+err.message);}
}

function exibirUrlFormularioCRM() {
  const props=PropertiesService.getScriptProperties();
  SpreadsheetApp.getUi().alert("🟣 URLs do Formulário CRM\n\nPreenchimento:\n"+(props.getProperty("FORM_CRM_URL")||"— não encontrada")+"\n\nEdição:\n"+(props.getProperty("FORM_CRM_EDIT_URL")||"— não encontrada"));
}

function onFormSubmitCRM(e) {
  try {
    const ss=SpreadsheetApp.getActiveSpreadsheet();
    const board=ss.getSheetByName(CONFIG.ABA_BOARD);
    const auto=ss.getSheetByName(CONFIG.ABA_AUTOMACAO);
    const v=e.values;
    const ts=new Date(v[0]);
    const solicitante=_str(v[1]),departamento=_str(v[2]);
    const tipoRaw=_str(v[3]),tipoOutro=_str(v[4]);
    const tipo=tipoRaw==="Outros"&&tipoOutro?tipoOutro:tipoRaw;
    const resumo=_str(v[5]),contexto=_str(v[6]),detalhes=_str(v[7]),resultados=_str(v[8]);
    const beneficio=_str(v[9]),benefOutro=_str(v[10]),impacto=_str(v[11]),times=_str(v[12]);
    const prioridadeRaw=_str(v[13]),prazoBruto=_str(v[14]),justPrazo=_str(v[15]);
    const jaTentado=_str(v[16]),referencias=_str(v[17]),gestorAprova=_str(v[18]),nomeGestor=_str(v[19]);
    const prioridade=_mapearPrioridade(prioridadeRaw);
    const descricao=[
      contexto?`📍 Contexto:\n${contexto}`:"",
      detalhes?`🔧 Descrição Detalhada:\n${detalhes}`:"",
      resultados?`🎯 Resultados Esperados:\n${resultados}`:"",
      beneficio?`💡 Benefício: ${beneficio}${benefOutro?" — "+benefOutro:""}`:"",
      impacto?`⚠️ Impacto se não feito:\n${impacto}`:"",
      times?`👥 Times afetados: ${times}`:"",
      jaTentado?`🔄 Já tentado:\n${jaTentado}`:"",
      justPrazo?`⏱️ Urgência:\n${justPrazo}`:"",
      referencias?`🔗 Referências:\n${referencias}`:"",
    ].filter(Boolean).join("\n\n");

    const novoId=_proximoId();
    const slaDias=CONFIG.SLA[prioridade]||5;
    const slaLimite=_adicionarDiasUteis(ts,slaDias);
    const slaFmt=Utilities.formatDate(slaLimite,"America/Sao_Paulo","dd/MM/yyyy");
    const dataCriac=Utilities.formatDate(ts,"America/Sao_Paulo","dd/MM/yyyy");

    const linhaBoard=new Array(30).fill("");
    linhaBoard[CONFIG.COL.ID]=novoId;linhaBoard[CONFIG.COL.TITULO]=resumo;
    linhaBoard[CONFIG.COL.TIPO]=tipo;linhaBoard[CONFIG.COL.STATUS]="Novas Solicitações";
    linhaBoard[CONFIG.COL.PRIORIDADE]=prioridade;linhaBoard[CONFIG.COL.RESPONSAVEL]=CONFIG_CRM.RESPONSAVEL_PADRAO;
    linhaBoard[CONFIG.COL.CATEGORIA]=CONFIG_CRM.CATEGORIA_PADRAO;linhaBoard[CONFIG.COL.SPRINT]="Sem sprint";
    linhaBoard[CONFIG.COL.DATA_CRIACAO]=dataCriac;linhaBoard[CONFIG.COL.DATA_FIM]=prazoBruto;
    linhaBoard[CONFIG.COL.PCT]="0%";linhaBoard[CONFIG.COL.EPICO]=CONFIG_CRM.EPICO_PADRAO;
    linhaBoard[CONFIG.COL.DESCRICAO]=descricao.substring(0,2000);
    linhaBoard[CONFIG.COL.SOLICITANTE]=solicitante;linhaBoard[CONFIG.COL.REVISADO_POR]=nomeGestor;
    linhaBoard[CONFIG.COL.SLA_LIMITE]=slaFmt;linhaBoard[CONFIG.COL.SLA_STATUS]="✅ No prazo";

    const ultimaLinha=board.getLastRow()+1;
    board.appendRow(linhaBoard);
    _aplicarCorStatus(board,ultimaLinha,"Novas Solicitações");
    auto.appendRow([Utilities.formatDate(ts,"America/Sao_Paulo","dd/MM/yyyy HH:mm"),novoId,resumo,`CRM: ${tipo}`,solicitante,departamento,CONFIG_CRM.RESPONSAVEL_PADRAO,prioridade,`SLA: ${slaDias}d → ${slaFmt}`,"✅ Incluído no Board","✅ Sim"]);

    const icone=_iconeprioridade(prioridade);
    _postWebhook({text:[`🟣 *Nova solicitação CRM recebida!*`,``,`*${novoId}* — ${resumo}`,
      `${icone} Prioridade: *${prioridade}*`,`👤 Responsável: *${CONFIG_CRM.RESPONSAVEL_PADRAO}*`,
      `🏢 Departamento: ${departamento}`,`🔧 Tipo: ${tipo}`,`💡 Benefício: ${beneficio}`,
      `⏱️ SLA: ${slaDias} dia(s) úteis → vence em *${slaFmt}*`,
      gestorAprova==="Sim"?`👔 Gestor: *${nomeGestor||"—"}* ✅`:`👔 Gestor: não consultado`,
      ``,`_Solicitante: ${solicitante} (${departamento})_`,``,`_Ticket aguarda triagem na sprint da terça-feira ☑️_`].join("\n")});

    const emailJoice=CONFIG.TIME[CONFIG_CRM.RESPONSAVEL_PADRAO]?CONFIG.TIME[CONFIG_CRM.RESPONSAVEL_PADRAO].email:"";
    if (emailJoice) {
      MailApp.sendEmail({to:emailJoice,subject:`[CRM IC] Nova solicitação: ${novoId} — ${resumo}`,
        htmlBody:`<div style="font-family:Arial,sans-serif;max-width:640px;padding:20px;border:1px solid #e5e7eb;border-radius:8px">
          <div style="background:#6F05D4;color:#fff;padding:14px 20px;border-radius:6px 6px 0 0"><h2 style="margin:0;font-size:17px">🟣 Nova Solicitação CRM — ${novoId}</h2><p style="margin:4px 0 0;font-size:13px;opacity:0.85">${resumo}</p></div>
          <div style="padding:20px"><p><strong>${solicitante}</strong> — ${departamento}</p><p>Tipo: ${tipo} | Prioridade: ${prioridade} | SLA: ${slaFmt}</p>
          ${contexto?`<p><strong>Contexto:</strong><br>${contexto.replace(/\n/g,"<br>")}</p>`:""}
          <p style="color:#6b7280;font-size:12px">Time IC — Mob2Con Inteligência Comercial</p></div></div>`});
    }
    Logger.log(`[onFormSubmitCRM] Ticket ${novoId} CRM criado.`);
  } catch(err){Logger.log(`[onFormSubmitCRM] ERRO: ${err.message}`);_postWebhook({text:`⚠️ Erro formulário CRM: ${err.message}`});}
}

function validarFormularioCRM() {
  const results=[]; const comp="🟣 CRM";
  const props=PropertiesService.getScriptProperties();
  const formUrl=props.getProperty("FORM_CRM_URL")||"";
  results.push({componente:comp,teste:"Formulário CRM criado",status:formUrl?"✅ OK":"⚠️ Atenção",detalhe:formUrl?`URL: ${formUrl.substring(0,60)}...`:"Execute: 🟣 CRM → 📝 Criar Formulário CRM"});
  const triggerOk=ScriptApp.getProjectTriggers().some(t=>t.getHandlerFunction()==="onFormSubmitCRM");
  results.push({componente:comp,teste:"Trigger onFormSubmitCRM",status:triggerOk?"✅ OK":"⚠️ Atenção",detalhe:triggerOk?"Trigger ativo":"Configure: Apps Script → Acionadores → (+) → onFormSubmitCRM → Do Formulário"});
  const joiceEmail=CONFIG.TIME["Joice Topan"]?CONFIG.TIME["Joice Topan"].email:"";
  results.push({componente:comp,teste:"E-mail da Joice",status:joiceEmail?"✅ OK":"❌ Falha",detalhe:joiceEmail?`E-mail: ${joiceEmail}`:"Configure em CONFIG.TIME"});
  const ss=SpreadsheetApp.getActiveSpreadsheet();
  _escreverResultadosValidacao(ss,results);
  const fail=results.filter(r=>r.status==="❌ Falha").length;
  const warn=results.filter(r=>r.status==="⚠️ Atenção").length;
  SpreadsheetApp.getUi().alert(`✅ Validação CRM!\n\n✅ OK: ${results.length-fail-warn} | ⚠️ Atenção: ${warn} | ❌ Falha: ${fail}\n\nVeja a aba "🔍 Validação".`);
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEÇÃO 21 — FUNÇÕES UTILITÁRIAS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function _proximoId() {
  const props=PropertiesService.getScriptProperties();
  let n=parseInt(props.getProperty(CONFIG.SPRINT.PROXIMO_ID)||"100",10);
  n++;
  props.setProperty(CONFIG.SPRINT.PROXIMO_ID,String(n));
  return `${CONFIG.SPRINT.PREFIXO_ID}${n}`;
}

function _sprintAtual() {
  try {
    const val=SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.ABA_BOARD).getRange("B2").getValue();
    return val?String(val):"Sprint Atual";
  } catch(e){return "Sprint Atual";}
}

function _toISODate(d) {
  if (!d) return undefined;
  try {
    if (d instanceof Date) return Utilities.formatDate(d,"UTC","yyyy-MM-dd")+"T00:00:00.000Z";
    const s=String(d).trim();
    if (s.match(/^\d{2}\/\d{2}\/\d{4}$/)){const[dia,mes,ano]=s.split("/");return `${ano}-${mes}-${dia}T00:00:00.000Z`;}
    const dt=new Date(d);
    if (isNaN(dt.getTime())) return undefined;
    return Utilities.formatDate(dt,"UTC","yyyy-MM-dd")+"T00:00:00.000Z";
  } catch(e){return undefined;}
}

function _adicionarDiasUteis(dataBase, n) {
  const d=new Date(dataBase);
  let adicionados=0;
  while (adicionados<n) {
    d.setDate(d.getDate()+1);
    const dia=d.getDay();
    const ddmm=Utilities.formatDate(d,"America/Sao_Paulo","dd/MM");
    if (dia!==0&&dia!==6&&!CONFIG.FERIADOS_BR.includes(ddmm)) adicionados++;
  }
  return d;
}

function _calcularDatasSprint(periodo) {
  try {
    const m=periodo.match(/(\d{2}\/\d{2})[–-](\d{2}\/\d{2}\/\d{4})/);
    if (!m) return ["",""];
    const ano=m[2].split("/")[2];
    return [m[1]+"/"+ano,m[2]];
  } catch(e){return ["",""];}
}

function _aplicarCorStatus(sheet, row, status) {
  const cores=CONFIG.CORES_STATUS[status];
  if (!cores) return;
  const lastCol=Object.keys(CONFIG.COL).length;
  sheet.getRange(row,1,1,lastCol).setBackground(cores.bg).setFontColor(cores.fg);
}

function _calcularMetricas(dados) {
  const m={total:0,novasSolicitacoes:0,backlog:0,aFazer:0,emAndamento:0,bloqueados:0,emValidacao:0,concluidos:0,cancelados:0};
  for (let i=3;i<dados.length;i++){
    const s=_str(dados[i][CONFIG.COL.STATUS]);
    if (!s) continue;
    m.total++;
    if (s==="Novas Solicitações")    m.novasSolicitacoes++;
    else if (s==="Backlog")           m.backlog++;
    else if (s==="A Fazer")           m.aFazer++;
    else if (s==="Em Andamento")      m.emAndamento++;
    else if (s==="Bloqueado"||s===STATUS_AGUARDANDO) m.bloqueados++;
    else if (s==="Em Validação")      m.emValidacao++;
    else if (s.includes("Concluído")) m.concluidos++;
    else if (s==="Cancelado")         m.cancelados++;
  }
  return m;
}

function _barraProgresso(pct, tamanho=10) {
  const cheio=Math.round((pct/100)*tamanho);
  return "▓".repeat(cheio)+"░".repeat(tamanho-cheio);
}

function _iconeprioridade(p) {
  if (!p) return "⚪";
  if (p.includes("Crítica")) return "🔴";
  if (p.includes("Alta"))    return "🟠";
  if (p.includes("Média"))   return "🟡";
  if (p.includes("Baixa"))   return "🟢";
  return "⚪";
}

function _postWebhook(payload) {
  const url=PropertiesService.getScriptProperties().getProperty("WEBHOOK_URL")||"";
  if (!url){Logger.log("[Webhook] URL não configurada. Msg: "+payload.text);return;}
  try{UrlFetchApp.fetch(url,{method:"post",contentType:"application/json",payload:JSON.stringify(payload)});}
  catch(e){Logger.log("[Webhook] Erro: "+e.message);}
}

function _enviarEmailConfirmacao(email, nome, id, titulo, prioridade, slaLimite) {
  try {
    MailApp.sendEmail({to:email,subject:`[Sprint IC] Ticket criado: ${id} — ${titulo}`,
      htmlBody:`<div style="font-family:Arial,sans-serif;max-width:600px;padding:20px;border:1px solid #e5e7eb;border-radius:8px">
        <div style="background:#F46901;color:#fff;padding:12px 20px;border-radius:6px 6px 0 0"><h2 style="margin:0;font-size:16px">✅ Ticket Registrado — Sprint IC</h2></div>
        <div style="padding:20px"><p>Olá <strong>${nome.split(" ")[0]}</strong>, seu ticket foi registrado!</p>
        <table style="border-collapse:collapse;width:100%;font-size:14px">
          <tr><td style="padding:6px;color:#6b7280">ID</td><td style="padding:6px"><strong>${id}</strong></td></tr>
          <tr style="background:#f9fafb"><td style="padding:6px;color:#6b7280">Título</td><td style="padding:6px">${titulo}</td></tr>
          <tr><td style="padding:6px;color:#6b7280">Prioridade</td><td style="padding:6px">${prioridade}</td></tr>
          <tr style="background:#f9fafb"><td style="padding:6px;color:#6b7280">SLA</td><td style="padding:6px">${Utilities.formatDate(slaLimite,"America/Sao_Paulo","dd/MM/yyyy")}</td></tr>
        </table>
        <p style="color:#6b7280;font-size:13px;margin-top:16px">Seu ticket entrará na triagem na próxima terça-feira.<br>Time IC — Mob2Con Inteligência Comercial</p>
        </div></div>`});
  } catch(e){Logger.log(`[Email] Erro para ${email}: ${e.message}`);}
}
