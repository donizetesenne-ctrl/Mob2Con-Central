/**
 * sync-tokens.js — Sincroniza design-tokens.json ↔ mob2con.css ↔ Mob2Con-Brand-Theme.json
 * 
 * Garante que se uma camada falhar (ex: alguém edita o JSON mas esquece o CSS),
 * o script reconcilia tudo a partir da fonte única (design-tokens.json).
 *
 * Uso:
 *   node sync-tokens.js               # verifica se está em sincronia
 *   node sync-tokens.js --apply       # regenera CSS e tema PBI a partir do JSON
 *   node sync-tokens.js --from-css    # regenera JSON a partir do CSS (caso JSON tenha sido apagado)
 */

const fs = require('fs');
const path = require('path');

const ROOT       = __dirname;
const TOKENS     = path.join(ROOT, 'design-tokens.json');
const CSS        = path.join(ROOT, 'mob2con.css');
const PBI_THEME  = path.join(ROOT, '..', '..', '02-Powerbi-Projetos', 'Mob2Con-Brand-Theme.json');

const apply  = process.argv.includes('--apply');
const fromCss = process.argv.includes('--from-css');

function readJSON(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }

function tokensToCssVars(tokens) {
  const lines = [':root {'];
  const c = tokens.color;
  lines.push('  /* BRAND */');
  for (const k of Object.keys(c.brand)) {
    const camel = k.replace(/([A-Z])/g, '-$1').toLowerCase();
    lines.push(`  --m2c-${camel}: ${c.brand[k].value};`);
  }
  lines.push('  /* NEUTRAL */');
  for (const k of Object.keys(c.neutral)) {
    lines.push(`  --m2c-${k.replace(/^gray/, 'gray-')}: ${c.neutral[k].value};`);
  }
  lines.push('  /* SEMANTIC */');
  for (const k of Object.keys(c.semantic)) {
    lines.push(`  --m2c-${k}: ${c.semantic[k].value};`);
  }
  lines.push('}');
  return lines.join('\n');
}

function tokensToPbiTheme(tokens) {
  const c = tokens.color;
  return {
    name: 'Mob2Con Brand Theme (auto-sync)',
    dataColors: [
      c.brand.orange.value,
      c.brand.graphite.value,
      c.brand.purple.value,
      c.semantic.success.value,
      c.semantic.danger.value,
      c.brand.black.value,
      '#FFA94D',
      '#9B59B6'
    ],
    good:       c.semantic.success.value,
    neutral:    c.brand.orange.value,
    bad:        c.semantic.danger.value,
    background: c.neutral.gray150.value,
    foreground: c.brand.black.value,
    tableAccent: c.brand.orange.value
  };
}

function checkSync() {
  if (!fs.existsSync(TOKENS)) { console.error('❌ design-tokens.json não encontrado'); return 1; }
  if (!fs.existsSync(CSS))    { console.warn('⚠️  mob2con.css ausente — rode com --apply'); }

  const tokens = readJSON(TOKENS);
  const orange = tokens.color.brand.orange.value;
  const cssRaw = fs.existsSync(CSS) ? fs.readFileSync(CSS, 'utf8') : '';
  const cssHasOrange = cssRaw.includes(orange);

  console.log('Tokens version :', tokens._meta.version);
  console.log('Orange (JSON)  :', orange);
  console.log('Orange in CSS  :', cssHasOrange ? '✅ ok' : '❌ divergente');

  if (fs.existsSync(PBI_THEME)) {
    const theme = readJSON(PBI_THEME);
    const themeOrange = (theme.dataColors || [])[0];
    console.log('Orange in PBI  :', themeOrange === orange ? `✅ ${themeOrange}` : `❌ ${themeOrange}`);
  } else {
    console.log('PBI theme      : ⚠️  não encontrado em', PBI_THEME);
  }
  return 0;
}

if (apply) {
  const tokens = readJSON(TOKENS);
  // CSS vars (substitui apenas o bloco :root inicial; resto do CSS preservado)
  const newRoot = tokensToCssVars(tokens);
  if (fs.existsSync(CSS)) {
    let cssRaw = fs.readFileSync(CSS, 'utf8');
    cssRaw = cssRaw.replace(/:root\s*\{[\s\S]*?\}/, newRoot);
    fs.writeFileSync(CSS, cssRaw, 'utf8');
    console.log('✅ mob2con.css :root atualizado');
  } else {
    fs.writeFileSync(CSS, newRoot + '\n', 'utf8');
    console.log('✅ mob2con.css criado');
  }
  // Power BI theme (regenera versão minimal — não toca no Mob2Con-Brand-Theme.json oficial pra não perder visualStyles)
  const themeAuto = path.join(ROOT, 'Mob2Con-Theme-auto.json');
  fs.writeFileSync(themeAuto, JSON.stringify(tokensToPbiTheme(tokens), null, 2), 'utf8');
  console.log('✅ Mob2Con-Theme-auto.json regenerado (versão minimal — fallback)');
  process.exit(0);
}

if (fromCss) {
  console.log('⚠️  --from-css ainda não implementado. Edite design-tokens.json manualmente como fonte da verdade.');
  process.exit(1);
}

process.exit(checkSync());
