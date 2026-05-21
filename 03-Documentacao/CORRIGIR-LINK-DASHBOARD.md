# 🚨 CORREÇÃO URGENTE: Link do Dashboard

## ❌ Problema Identificado

**Link antigo (não funciona mais):**
```
https://script.google.com/macros/s/AKfycbzVJneXlqv4iwIeJ0YSVkTrhLyeMy1smetn-8wAdUnnzwC0hNA1sAujKYvC9WU62sqi/exec
```

**Motivo:** O projeto Apps Script original foi deletado ou a implantação foi removida.

---

## ✅ Solução: Usar o Projeto Backup Correto

Encontrei o projeto correto com backup automático:
- **ID do Projeto**: `1lh1BffvyiRMEV4wHpAXQLw05gLx7jIKO7qxGOSNcWfaF9O7otZOUpFtF`
- **Nome**: "Projeto sem título backup 20260515170543"
- **Status**: ✅ Código correto, configuração webapp OK

---

## 🎯 PASSO A PASSO DEFINITIVO

### **PASSO 1: Abrir o Projeto Correto**

**Clique neste link:**
```
https://script.google.com/d/1lh1BffvyiRMEV4wHpAXQLw05gLx7jIKO7qxGOSNcWfaF9O7otZOUpFtF/edit
```

### **PASSO 2: Verificar o Código**

O código deve estar assim (já está correto):

```javascript
var HTML_FILE_ID = '1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc';

function doGet() {
  var file = DriveApp.getFileById(HTML_FILE_ID);
  var html = file.getBlob().getDataAsString('UTF-8');
  return HtmlService.createHtmlOutput(html)
    .setTitle('Dashboard Mob2Con — Analítico RG 2.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
```

✅ **Não precisa alterar nada!**

### **PASSO 3: Fazer a Implantação**

#### 3.1. Clicar em "Implantar"
- Botão azul no canto superior direito
- Selecione **"Nova implantação"**

#### 3.2. Configurar o Tipo
- Clique no ícone de **engrenagem** ⚙️
- Selecione **"Aplicativo da Web"**

#### 3.3. Preencher os Campos

**IMPORTANTE: Use exatamente estas configurações:**

| Campo | Valor |
|-------|-------|
| **Nova descrição** | `Dashboard Analítico RG 2.0 - Produção` |
| **Executar como** | `Eu (donizete.senne@mob2con.com.br)` |
| **Quem tem acesso** | `Qualquer pessoa` ⚠️ **CRÍTICO!** |

⚠️ **ATENÇÃO**: Se não selecionar "Qualquer pessoa", o link não funcionará publicamente!

#### 3.4. Clicar em "Implantar"
- Clique no botão **"Implantar"**
- Se aparecer tela de autorização:
  1. Clique em **"Autorizar acesso"**
  2. Selecione sua conta: `donizete.senne@mob2con.com.br`
  3. Se aparecer "Este app não foi verificado":
     - Clique em **"Avançado"**
     - Clique em **"Ir para [nome do projeto] (não seguro)"**
  4. Clique em **"Permitir"**

#### 3.5. Copiar a Nova URL
Após a implantação, você verá:

```
✅ Implantação criada com sucesso

ID da implantação: AKfycby...
URL do aplicativo da Web: https://script.google.com/macros/s/[NOVO_ID]/exec
```

**COPIE ESSA URL!** Essa é a nova URL do dashboard.

---

## 📋 Checklist de Verificação

Antes de fechar, verifique:

- [ ] Projeto correto aberto (ID: `1lh1BffvyiRMEV4wHpAXQLw05gLx7jIKO7qxGOSNcWfaF9O7otZOUpFtF`)
- [ ] Código verificado (não alterado)
- [ ] Nova implantação criada
- [ ] Tipo: "Aplicativo da Web"
- [ ] Acesso: "Qualquer pessoa" ✅
- [ ] Autorização concedida
- [ ] Nova URL copiada
- [ ] Dashboard testado (abrir a URL no navegador)
- [ ] Dados carregando das planilhas

---

## 🔄 Atualizar Links em Todos os Lugares

Depois de gerar a nova URL, substitua o link antigo em:

1. ✅ Documentação interna
2. ✅ E-mails enviados
3. ✅ Favoritos do navegador
4. ✅ Apresentações PowerPoint
5. ✅ Planilhas de controle
6. ✅ Wiki/Confluence da empresa

---

## 🧪 Testar o Dashboard

Após copiar a nova URL:

1. **Abra em uma aba anônima** (Ctrl+Shift+N no Chrome)
2. Cole a URL
3. Verifique se:
   - ✅ Dashboard carrega
   - ✅ Dados aparecem
   - ✅ Filtros funcionam
   - ✅ Gráficos renderizam
   - ✅ Abas trocam corretamente

---

## 📊 Como Funciona a Atualização Automática

**Você não precisa fazer nada!** O dashboard:

1. ✅ Busca dados automaticamente das planilhas Google Sheets
2. ✅ Atualiza toda vez que alguém abre o link
3. ✅ Usa dados hardcoded como fallback se Sheets estiver offline
4. ✅ Não precisa reimplantar o Apps Script

**Planilhas configuradas:**
- Dimensões: `1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q`
- Fatos: `1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs`
- Lookups: `1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI`

---

## 🆘 Solução de Problemas

### Erro: "Autorização necessária"
**Solução:**
1. Clique em "Autorizar acesso"
2. Selecione sua conta Google
3. Clique em "Avançado" → "Ir para [projeto]"
4. Clique em "Permitir"

### Erro: "Arquivo não encontrado"
**Solução:**
1. Verifique se o arquivo HTML existe: https://drive.google.com/file/d/1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc/view
2. Verifique se você tem acesso ao arquivo

### Dashboard carrega mas sem dados
**Solução:**
1. Abra o arquivo de teste: `teste-sheets-dashboard.html`
2. Verifique se as planilhas estão acessíveis
3. Verifique as permissões das planilhas

### Link não funciona para outras pessoas
**Solução:**
1. Verifique se selecionou "Qualquer pessoa" na implantação
2. Refaça a implantação com a configuração correta

---

## ✅ Resultado Final

Após seguir todos os passos, você terá:

✅ **Nova URL pública funcionando**
✅ **Dashboard com atualização automática**
✅ **Dados ao vivo das planilhas**
✅ **Acesso para qualquer pessoa**

---

## 📞 Suporte

Se precisar de ajuda:
1. Verifique o arquivo de teste: `teste-sheets-dashboard.html`
2. Verifique os logs do Apps Script: Menu "Execuções"
3. Entre em contato com o suporte técnico

---

**Criado em:** 15/05/2026
**Última atualização:** 15/05/2026
**Autor:** Kiro AI Assistant
**Projeto:** Dashboard Analítico RG 2.0 - Mob2Con
