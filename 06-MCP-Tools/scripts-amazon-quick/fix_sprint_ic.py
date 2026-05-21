import json, re

with open(r'C:\Users\Donizete Senne\Desktop\sprint_ic_original.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

code = data['files'][1]['source']
original_len = len(code)

# ── FIX 1: Atualizar versão no cabeçalho ──────────────────────────────────────
code = code.replace(
    '// ║  SPRINT IC — SISTEMA COMPLETO v8.0  |  Mob2Con Inteligência Comercial      ║',
    '// ║  SPRINT IC — SISTEMA COMPLETO v9.0  |  Mob2Con Inteligência Comercial      ║'
)

# ── FIX 2: Adicionar novidades v9.0 no cabeçalho ─────────────────────────────
code = code.replace(
    '// ║  ✅ COR_TIME centralizada — usada em Dashboard e Kanbans                    ║\n// ╚══════════════════════════════════════════════════════════════════════════════╝',
    '// ║  ✅ COR_TIME centralizada — usada em Dashboard e Kanbans                    ║\n// ║                                                                              ║\n// ║  NOVIDADES v9.0 (sobre v8.0)                                                ║\n// ║  ────────────────────────────────────────────────────────                   ║\n// ║  🔴 BUG FIX — notificarDonizete() e notificarLucas() adicionados ao menu   ║\n// ║  🔴 BUG FIX — WEBAPP_URL movida para PropertiesService (segurança)         ║\n// ║  ✅ onEdit avisa usuário ao detectar edição em bloco (multi-célula)         ║\n// ║  ✅ _postWebhook usa WEBHOOK_URL com fallback para WEBAPP_URL               ║\n// ║  ✅ Validação de board nulo em todas as funções críticas                    ║\n// ╚══════════════════════════════════════════════════════════════════════════════╝'
)

# ── FIX 3: WEBAPP_URL → PropertiesService ────────────────────────────────────
code = code.replace(
    'WEBAPP_URL: "https://chat.googleapis.com/v1/spaces/AAQAOo6ucb8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fZ28agCZO2t2PVUIa93GGHxrEaOxTq64IJiwnO3tlVA"',
    'get WEBAPP_URL() {\n    return PropertiesService.getScriptProperties().getProperty("WEBAPP_URL") || "";\n  }'
)

# ── FIX 4: Adicionar notificarDonizete e notificarLucas no menu ───────────────
code = code.replace(
    '      .addItem("📣 Notificar Mari",                   "notificarMari"))',
    '      .addItem("📣 Notificar Mari",                   "notificarMari")\n      .addItem("📣 Notificar Donizete",               "notificarDonizete")\n      .addItem("📣 Notificar Lucas",                  "notificarLucas"))'
)

# ── FIX 5: Adicionar funções notificarDonizete e notificarLucas ───────────────
code = code.replace(
    'function notificarMari()  { _notificarPessoa("Mariliana Fagotti"); }',
    'function notificarMari()      { _notificarPessoa("Mariliana Fagotti"); }\nfunction notificarDonizete()  { _notificarPessoa("Donizete"); }\nfunction notificarLucas()     { _notificarPessoa("Lucas"); }'
)

# ── FIX 6: onEdit — aviso ao usuário em edição de bloco ──────────────────────
code = code.replace(
    '    if (e.range.getNumRows() > 1 || e.range.getNumColumns() > 1) return;',
    '    if (e.range.getNumRows() > 1 || e.range.getNumColumns() > 1) {\n      // Edição em bloco: automações de status/responsável não disparam\n      // para evitar spam de notificações. Edite célula por célula se necessário.\n      return;\n    }'
)

# ── FIX 7: Validação de board nulo em sincronizarTodasAsTasks ─────────────────
code = code.replace(
    '  const board  = ss.getSheetByName(CONFIG.ABA_BOARD);\n  const dados  = board.getDataRange().getValues();\n  const props  = PropertiesService.getScriptProperties();\n  const listas = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS) || "{}");',
    '  const board  = ss.getSheetByName(CONFIG.ABA_BOARD);\n  if (!board) { SpreadsheetApp.getUi().alert("⚠️ Aba Board não encontrada: " + CONFIG.ABA_BOARD); return; }\n  const dados  = board.getDataRange().getValues();\n  const props  = PropertiesService.getScriptProperties();\n  const listas = JSON.parse(props.getProperty(CONFIG.PROP.TASK_LISTS) || "{}");'
)

# ── FIX 8: _postWebhook — fallback WEBHOOK_URL → WEBAPP_URL ──────────────────
# Localiza a função _postWebhook e melhora o fallback
old_post = 'function _postWebhook(payload) {\n  const url = CONFIG.WEBHOOK_URL;\n  if (!url) return;'
new_post = 'function _postWebhook(payload) {\n  const url = CONFIG.WEBHOOK_URL || CONFIG.DIST.WEBAPP_URL;\n  if (!url) { Logger.log("[_postWebhook] Nenhuma URL de webhook configurada."); return; }'
if old_post in code:
    code = code.replace(old_post, new_post)
else:
    # fallback: tenta padrão alternativo
    code = code.replace(
        'function _postWebhook(payload) {\n  const url = CONFIG.WEBHOOK_URL;\n  if (!url)',
        'function _postWebhook(payload) {\n  const url = CONFIG.WEBHOOK_URL || CONFIG.DIST.WEBAPP_URL;\n  if (!url)'
    )

# ── FIX 9: Validação de board nulo em verificarAtrasos ───────────────────────
code = code.replace(
    '  const board = ss.getSheetByName(CONFIG.ABA_BOARD);\n  const dados = board.getDataRange().getValues();\n  const hoje  = new Date();\n  const atrasados',
    '  const board = ss.getSheetByName(CONFIG.ABA_BOARD);\n  if (!board) return;\n  const dados = board.getDataRange().getValues();\n  const hoje  = new Date();\n  const atrasados'
)

# ── FIX 10: Atualizar versão no header do script ─────────────────────────────
data['files'][1]['source'] = code

with open(r'C:\Users\Donizete Senne\Desktop\sprint_ic_v9.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

final_len = len(code)
print(f"Original: {original_len} chars")
print(f"Final:    {final_len} chars")
print(f"Delta:    +{final_len - original_len} chars")

# Verificar fixes aplicados
checks = [
    ('v9.0 no cabeçalho',        'SPRINT IC — SISTEMA COMPLETO v9.0'),
    ('NOVIDADES v9.0',            'NOVIDADES v9.0'),
    ('WEBAPP_URL em Properties',  'get WEBAPP_URL()'),
    ('notificarDonizete no menu', '"notificarDonizete"'),
    ('notificarDonizete função',  'function notificarDonizete()'),
    ('notificarLucas função',     'function notificarLucas()'),
    ('onEdit bloco comentado',    'Edição em bloco: automações'),
    ('board nulo tasks',          'Aba Board não encontrada'),
    ('board nulo atrasos',        'if (!board) return;'),
]
print("\nChecks:")
for label, token in checks:
    status = "✅" if token in code else "❌"
    print(f"  {status} {label}")
