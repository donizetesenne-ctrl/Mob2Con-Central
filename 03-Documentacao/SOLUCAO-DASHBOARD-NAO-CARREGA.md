# 🔧 Solução: Dashboard Não Carrega Dados

**Data:** 15/05/2026  
**Status:** 🔴 PROBLEMA IDENTIFICADO

## 🎯 Problema

O dashboard `📊 Dashboard Dados Reais.html` não está carregando dados reais das planilhas Google Sheets.

### Causa Raiz

O **Google Apps Script não está implantado corretamente** ou o link está incorreto.

## ✅ Solução em 3 Passos

### Passo 1: Implantar o Apps Script

1. **Abra o Google Apps Script:**
   - Acesse: https://script.google.com
   - Clique em **"Novo projeto"**
   - Nome: `Dashboard Analítico RG 2.0`

2. **Cole o código:**
   - Abra o arquivo: `06-MCP-Tools\dashboard-apps-script.gs`
   - Copie TODO o conteúdo
   - Cole no editor do Apps Script

3. **Teste localmente:**
   - No menu superior, selecione a função: `testarAppsScript`
   - Clique em **▶ Executar**
   - Autorize o acesso quando solicitado
   - Verifique os logs: **View → Logs**
   - Deve mostrar: "X colunas, Y linhas" para cada aba

4. **Implante como Web App:**
   - Clique em **Deploy → New deployment**
   - Tipo: **Web app**
   - Execute as: **Me (seu email)**
   - Who has access: **Anyone**
   - Clique em **Deploy**
   - **COPIE A URL** que aparece (exemplo: `https://script.google.com/macros/s/AKfycb.../exec`)

### Passo 2: Atualizar o Dashboard

1. **Abra o arquivo:**
   ```
   03-Documentacao\📊 Dashboard Dados Reais.html
   ```

2. **Procure a linha 800** (aproximadamente):
   ```javascript
   const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/...';
   ```

3. **Substitua pela nova URL** que você copiou no Passo 1

4. **Salve o arquivo**

### Passo 3: Testar

1. **Abra o arquivo de teste:**
   ```
   03-Documentacao\teste-apps-script.html
   ```

2. **Clique em "🚀 Testar Apps Script"**

3. **Verifique o resultado:**
   - ✅ Verde = Funcionando!
   - ❌ Vermelho = Erro (veja o console)

## 📋 Checklist

- [ ] Apps Script criado no Google
- [ ] Código colado e testado localmente
- [ ] Web App implantado
- [ ] URL copiada
- [ ] Dashboard atualizado com nova URL
- [ ] Teste executado com sucesso
- [ ] Dados reais aparecem no dashboard

## 🔍 Diagnóstico

Se ainda não funcionar:

1. **Verifique as permissões das planilhas:**
   - Dimensões: `1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q`
   - Fatos: `1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs`
   - Lookups: `1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI`
   - Todas devem estar com "Qualquer pessoa com o link"

2. **Teste o Apps Script diretamente:**
   ```
   https://script.google.com/macros/s/SUA_URL_AQUI/exec?action=help
   ```
   - Deve retornar um JSON com informações

3. **Verifique o console do navegador (F12):**
   - Procure por erros em vermelho
   - Verifique se há bloqueio de CORS

## 📁 Arquivos Importantes

- `06-MCP-Tools\dashboard-apps-script.gs` - Código do Apps Script
- `03-Documentacao\📊 Dashboard Dados Reais.html` - Dashboard principal
- `03-Documentacao\teste-apps-script.html` - Ferramenta de teste
- `03-Documentacao\CORRECAO-DASHBOARD-CONCLUIDA.md` - Documentação anterior

## 🆘 Precisa de Ajuda?

Se continuar com problemas, me avise e forneça:
1. Mensagens de erro do console (F12)
2. Resultado do teste do Apps Script
3. URL do Apps Script implantado
