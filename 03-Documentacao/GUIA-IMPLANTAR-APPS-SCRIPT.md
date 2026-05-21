# 🚀 Guia Completo: Implantar Dashboard no Google Apps Script

## ✅ Status Atual
- ✅ Planilhas Google Sheets acessíveis e com dados
- ✅ Arquivo HTML do dashboard no Drive (ID: `1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc`)
- ✅ Projeto Apps Script criado (ID: `1cjk2ifN8bPVaSylbIZFFZy_lTKilrTbMke5Pt1DCc_gbKoUB2QS3EUEP`)
- ⚠️ **Falta apenas fazer a implantação correta**

---

## 📋 Passo a Passo para Implantação

### **1. Abrir o Projeto Apps Script**

Clique neste link para abrir o projeto:
```
https://script.google.com/d/1cjk2ifN8bPVaSylbIZFFZy_lTKilrTbMke5Pt1DCc_gbKoUB2QS3EUEP/edit
```

---

### **2. Verificar o Código**

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

✅ **Se o código estiver diferente, copie e cole o código acima.**

---

### **3. Fazer a Implantação**

#### **3.1. Clicar em "Implantar"**
- No canto superior direito, clique no botão **"Implantar"**
- Selecione **"Nova implantação"**

#### **3.2. Configurar o Tipo**
- Clique no ícone de **engrenagem** ⚙️ ao lado de "Selecionar tipo"
- Escolha **"Aplicativo da Web"**

#### **3.3. Preencher os Campos**

| Campo | Valor |
|-------|-------|
| **Descrição** | `Dashboard Analítico RG 2.0 - Atualização Automática` |
| **Executar como** | `Eu (donizete.senne@mob2con.com.br)` |
| **Quem tem acesso** | `Qualquer pessoa` |

⚠️ **IMPORTANTE**: Certifique-se de selecionar **"Qualquer pessoa"** para que o link funcione publicamente.

#### **3.4. Clicar em "Implantar"**
- Clique no botão **"Implantar"**
- Se aparecer uma tela de autorização, clique em **"Autorizar acesso"**
- Faça login com sua conta Google (donizete.senne@mob2con.com.br)
- Clique em **"Permitir"** quando solicitado

#### **3.5. Copiar a URL**
Após a implantação, você verá uma tela com:
- ✅ **ID da implantação**: (um código longo)
- 🔗 **URL do aplicativo da Web**: `https://script.google.com/macros/s/[ID]/exec`

**COPIE ESSA URL!** Essa é a URL que funcionará.

---

### **4. Testar o Dashboard**

1. Abra a URL copiada no navegador
2. O dashboard deve carregar normalmente
3. Verifique se os dados estão sendo carregados das planilhas

---

## 🔧 Solução de Problemas

### **Problema: "Autorização necessária"**
**Solução:**
1. Clique em "Autorizar acesso"
2. Selecione sua conta Google
3. Clique em "Avançado" (se aparecer aviso de segurança)
4. Clique em "Ir para [nome do projeto] (não seguro)"
5. Clique em "Permitir"

### **Problema: "Arquivo não encontrado"**
**Solução:**
1. Verifique se o ID do arquivo HTML está correto: `1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc`
2. Verifique se você tem acesso ao arquivo no Drive
3. Tente abrir o arquivo diretamente: https://drive.google.com/file/d/1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc/view

### **Problema: "Dados não carregam"**
**Solução:**
1. Abra o arquivo de teste: `teste-sheets-dashboard.html`
2. Verifique se todas as planilhas estão acessíveis
3. Verifique as permissões das planilhas no Google Sheets

---

## 📊 Planilhas Configuradas

O dashboard busca dados automaticamente destas planilhas:

| Nome | ID da Planilha | Abas Usadas |
|------|----------------|-------------|
| **Dimensões** | `1r0K7XJ1XFjVPlXXFNoN33ZRFW8EXwoK3gYqeEZpRe8Q` | `dim_rede` |
| **Fatos** | `1LdJvbwsOhBh11Xgd5oUeQPaL4J_JTVfOgDMnM0EXJxs` | `fato_status_promotores`, `fato_contrato_pontual`, `fato_agg_status_documentacao_redes` |
| **Lookups** | `1g0jg93WC2axeyrzNHYhxsljrtXQLhdZwMPbbpnemJFI` | `tbl_scores_redes` |

---

## 🔄 Como Funciona a Atualização Automática

1. **Você atualiza as planilhas** no Google Sheets (manualmente ou via Redshift)
2. **O dashboard detecta automaticamente** os novos dados ao carregar
3. **Não precisa reimplantar** o Apps Script
4. **Os dados são atualizados em tempo real** toda vez que alguém abre o dashboard

---

## ✅ Checklist Final

- [ ] Projeto Apps Script aberto
- [ ] Código verificado e correto
- [ ] Nova implantação criada
- [ ] Tipo configurado como "Aplicativo da Web"
- [ ] Acesso configurado como "Qualquer pessoa"
- [ ] Autorização concedida
- [ ] URL copiada
- [ ] Dashboard testado e funcionando
- [ ] Dados carregando das planilhas

---

## 📞 Suporte

Se precisar de ajuda:
1. Verifique o arquivo de teste: `teste-sheets-dashboard.html`
2. Verifique os logs do Apps Script: Menu "Execuções" no editor
3. Verifique as permissões das planilhas no Google Sheets

---

**Última atualização:** 15/05/2026
**Criado por:** Kiro AI Assistant
