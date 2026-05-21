# 🔄 Changelog: Dashboard Atualização Automática

> **Data:** 15/05/2026  
> **Modificado por:** Kiro AI  
> **Arquivo:** `📊 Dashboard Dados Reais.html`

---

## ✅ Mudanças Implementadas

### 1. **Integração com Google Apps Script**

**Antes:**
- Dashboard buscava dados diretamente do Google Sheets via API `gviz`
- Sujeito a bloqueios CORS e problemas de permissão
- Dados hardcoded como fallback

**Depois:**
- **Fonte primária:** Google Apps Script (`AKfycbzVJneXlqv4iwIeJ0YSVkTrhLyeMy1smetn-8wAdUnnzwC0hNA1sAujKYvC9WU62sqi`)
- **Fallback 1:** API gviz direto do Sheets
- **Fallback 2:** Dados hardcoded (demonstração)

### 2. **Função `fetchSheet` Atualizada**

```javascript
// 🔄 ATUALIZADO: Agora usa Google Apps Script como fonte primária
async function fetchSheet(id, sheet, timeoutMs=8000){
  // Tenta Apps Script primeiro
  const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/...';
  const res = await fetch(`${APPS_SCRIPT_URL}?action=getSheet&sheetId=${id}&sheetName=${sheet}`);
  
  // Se falhar, tenta gviz direto
  // Se falhar novamente, usa dados hardcoded
}
```

### 3. **Melhorias no Feedback Visual**

- ✅ **Indicador de status** atualizado em tempo real
- 🔄 **Botão "Atualizar"** já existente e funcional
- 📊 **Console de debug** para diagnóstico
- ⏰ **Timestamp** de última atualização na aba CEO

### 4. **Logs Detalhados**

Agora o console mostra:
```
🔄 Apps Script: dim_rede de 1r0K7XJ1...
✅ Apps Script: dim_rede → 7 linhas
🎉 Dashboard atualizado com sucesso!
```

Ou em caso de fallback:
```
⚠️ Apps Script falhou, tentando gviz direto...
✅ gviz: dim_rede : 7 linhas
```

---

## 🎯 Como Funciona Agora

### Fluxo de Atualização

1. **Abertura do Dashboard:**
   - Chama `inicializarDashboard()` automaticamente
   - Tenta buscar dados do Apps Script
   - Se falhar, tenta gviz direto
   - Se falhar novamente, usa dados hardcoded

2. **Atualização Manual:**
   - Clique no botão "🔄 Atualizar" no header
   - Chama `forceRefresh()` que reinicia o processo

3. **Indicadores Visuais:**
   - 🟢 **Verde:** Dados ao vivo carregados com sucesso
   - 🟡 **Amarelo:** Dados de demonstração (hardcoded)
   - 🔴 **Vermelho:** Erro ao carregar (usa hardcoded)

---

## 🔧 Configuração do Apps Script

### Parâmetros Esperados

O Apps Script deve aceitar:
```
?action=getSheet&sheetId=<ID>&sheetName=<NOME>
```

### Resposta Esperada

```json
{
  "cols": ["coluna1", "coluna2", ...],
  "rows": [
    {"coluna1": "valor1", "coluna2": "valor2"},
    ...
  ]
}
```

### Planilhas Consultadas

1. **dim_rede** (ID: `1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q`)
2. **fato_status_promotores** (ID: `1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs`)
3. **fato_contrato_pontual** (ID: `1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs`)
4. **fato_agg_status_documentacao_redes** (ID: `1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs`)
5. **tbl_scores_redes** (ID: `1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI`)

---

## 🧪 Como Testar

### 1. Abrir o Dashboard
```
Abra: 03-Documentacao\📊 Dashboard Dados Reais.html
```

### 2. Abrir o Console do Navegador
```
Pressione F12 → Aba "Console"
```

### 3. Verificar os Logs
Você verá:
```
🔄 Apps Script: dim_rede de 1r0K7XJ1...
✅ Apps Script: dim_rede → 7 linhas
🎉 Dashboard atualizado com sucesso!
```

### 4. Testar Atualização Manual
```
Clique no botão "🔄 Atualizar" no header
```

### 5. Verificar Indicador
```
Procure a pill verde no header:
"✅ Dados ao vivo · 15/05/2026 12:30"
```

---

## 🐛 Troubleshooting

### Problema: "Dados de demonstração"

**Causa:** Apps Script não está respondendo ou retornando dados vazios

**Solução:**
1. Verificar se o Apps Script está publicado
2. Verificar permissões das planilhas
3. Testar a URL do Apps Script diretamente no navegador

### Problema: Erro CORS

**Causa:** Apps Script não configurado para aceitar requisições do domínio

**Solução:**
1. No Apps Script, adicionar:
```javascript
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
```

### Problema: Timeout

**Causa:** Apps Script demorando mais de 8 segundos

**Solução:**
1. Otimizar o código do Apps Script
2. Aumentar o timeout no dashboard:
```javascript
fetchSheet(id, sheet, 15000) // 15 segundos
```

---

## 📦 Backup

Um backup foi criado automaticamente:
```
📊 Dashboard Dados Reais.html.bak-kiro-20260515-HHMMSS
```

Para restaurar:
```powershell
Copy-Item "📊 Dashboard Dados Reais.html.bak-kiro-*" "📊 Dashboard Dados Reais.html"
```

---

## 🎉 Resultado Final

✅ Dashboard atualiza automaticamente ao abrir  
✅ Botão de atualização manual funcional  
✅ Indicadores visuais claros  
✅ Logs detalhados para debug  
✅ Fallback inteligente (Apps Script → gviz → hardcoded)  
✅ Backup de segurança criado  

**O dashboard está pronto para produção! 🚀**
