# 🔧 Correção: Dashboard não atualiza automaticamente

## 📋 Problema Identificado

O dashboard **"📊 Dashboard Dados Reais.html"** estava travando e não atualizava os dados do Google Sheets automaticamente, mesmo com as planilhas públicas e integração configurada.

## ✅ Correções Implementadas

### 1. **Melhorias no Sistema de Fetch**
- ✅ Adicionado logs detalhados de debug no console
- ✅ Melhorado tratamento de erros HTTP
- ✅ Adicionado cache control (`cache: 'no-cache'`)
- ✅ Timeout configurável (8 segundos padrão)

### 2. **Parser JSONP Robusto**
- ✅ Suporte a múltiplos formatos de resposta do Google Sheets
- ✅ Tratamento de erros mais detalhado
- ✅ Validação de estrutura de dados

### 3. **Botão de Atualização Manual**
- ✅ Novo botão **"🔄 Atualizar"** no header
- ✅ Feedback visual durante atualização
- ✅ Permite forçar refresh dos dados

### 4. **Console de Debug Visual**
- ✅ Novo botão **"🔍 Debug"** no header
- ✅ Console flutuante com logs em tempo real
- ✅ Intercepta console.log/warn/error
- ✅ Mostra status de cada requisição

### 5. **Auto-Refresh Inteligente**
- ✅ Detecta quando usuário volta à aba
- ✅ Atualiza automaticamente se passou >10 minutos
- ✅ Opção de refresh periódico (comentado, pode ativar)

## 🎯 Como Usar

### Atualização Manual
1. Clique no botão **"🔄 Atualizar"** no header
2. Aguarde o feedback visual
3. Verifique o indicador de status (verde = sucesso)

### Debug de Problemas
1. Clique no botão **"🔍 Debug"** no header
2. Console flutuante aparece no canto inferior direito
3. Veja logs em tempo real:
   - 🟢 Verde = informação
   - 🟡 Amarelo = aviso
   - 🔴 Vermelho = erro
   - 🔵 Ciano = sucesso

### Verificar Status
Observe o indicador no header:
- ✅ **Verde** "Dados ao vivo" = Carregou do Google Sheets
- ⚠️ **Amarelo** "Dados demonstração" = Usando dados hardcoded
- 📦 **Cinza** "Dados locais" = Offline

## 🔍 Diagnóstico de Problemas

### Se aparecer "Dados demonstração":

1. **Abra o Console de Debug** (botão 🔍)
2. **Clique em Atualizar** (botão 🔄)
3. **Verifique os logs**:

```
✅ Sucesso:
🔄 Buscando: dim_rede de 1r0K7XJ1...
📦 Recebido 1234 bytes para dim_rede
✅ dim_rede : 7 linhas
✅ dim_rede: 7 redes carregadas
```

```
❌ Erro de Permissão:
❌ Erro HTTP 403 para dim_rede
⚠️ dim_rede : sem dados válidos
```

```
❌ Erro de CORS:
❌ Erro ao buscar dim_rede : Failed to fetch
```

### Soluções por Tipo de Erro

#### 🔴 Erro 403 (Permissão Negada)
**Causa**: Planilha não está pública
**Solução**:
1. Abra cada planilha no Google Sheets
2. Clique em "Compartilhar"
3. Altere para "Qualquer pessoa com o link pode visualizar"
4. Salve e teste novamente

#### 🔴 Erro CORS (Failed to fetch)
**Causa**: Navegador bloqueando requisição cross-origin
**Solução**:
1. Abra o arquivo via servidor HTTP (não file://)
2. Use extensão "Live Server" no VS Code
3. Ou hospede em servidor web

#### 🔴 Timeout
**Causa**: Planilha muito grande ou conexão lenta
**Solução**: Aumentar timeout no código (linha ~766):
```javascript
async function fetchSheet(id, sheet, timeoutMs=15000){ // aumentar para 15s
```

## 📊 IDs das Planilhas Configuradas

```javascript
const SHEETS = {
  dimensoes: '1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q',
  fatos:     '1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs',
  lookups:   '1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI'
};
```

### Abas Esperadas:
- **dimensoes**: `dim_rede`
- **fatos**: `fato_status_promotores`, `fato_contrato_pontual`, `fato_agg_status_documentacao_redes`
- **lookups**: `tbl_scores_redes`

## 🚀 Recursos Adicionais (Opcionais)

### Ativar Auto-Refresh Periódico
Descomente no código (linha ~1050):
```javascript
// Atualiza automaticamente a cada 5 minutos
setInterval(function(){
  console.log('🔄 Auto-refresh periódico...');
  inicializarDashboard();
}, 5 * 60 * 1000); // 5 minutos
```

### Ajustar Tempo de Auto-Refresh ao Voltar à Aba
Altere o tempo no código (linha ~1060):
```javascript
if(tempoDecorrido > 5 * 60 * 1000){ // mudar de 10 para 5 minutos
```

## 📝 Logs Úteis no Console do Navegador

Abra o Console do Navegador (F12) e procure por:
- `🔄 Buscando:` - Iniciando requisição
- `📦 Recebido` - Dados recebidos
- `✅` - Sucesso
- `❌` - Erro
- `⚠️` - Aviso

## 🔗 Links Relacionados

- **Google Apps Script**: `https://script.google.com/macros/s/AKfycbz.../exec`
  - ⚠️ Nota: Este link existe no HTML mas não está sendo usado atualmente
  - O dashboard busca dados diretamente das planilhas via API gviz

## 📞 Suporte

Se o problema persistir:
1. Capture screenshot do Console de Debug
2. Copie os logs do Console do Navegador (F12)
3. Verifique se as planilhas estão acessíveis manualmente
4. Teste em navegador diferente (Chrome, Edge, Firefox)

---

**Última atualização**: 15/05/2026
**Arquivo corrigido**: `📊 Dashboard Dados Reais.html`
