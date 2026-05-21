# 🌐 Como Publicar o Dashboard Online

**Objetivo**: Criar um link online para o dashboard (tipo: `https://script.google.com/macros/s/...`)

---

## 🚀 MÉTODO 1: Google Apps Script (RECOMENDADO)

### **Passo 1: Abrir o Google Apps Script**
1. Acesse: https://script.google.com
2. Clique em **"+ Novo projeto"**
3. Renomeie para: **"Dashboard RG 2.0 Web App"**

### **Passo 2: Criar o Arquivo Code.gs**
1. No editor, você verá um arquivo `Code.gs`
2. **Apague todo o conteúdo** que está lá
3. Cole este código:

```javascript
function doGet() {
  return HtmlService.createHtmlOutputFromFile('dashboard')
    .setTitle('Analítico RG 2.0 — Dashboard Mob2Con')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
```

4. Clique em **💾 Salvar** (Ctrl+S)

### **Passo 3: Criar o Arquivo HTML**
1. Clique no **+** ao lado de "Files" (Arquivos)
2. Escolha **"HTML"**
3. Nome do arquivo: **`dashboard`** (sem extensão)
4. Clique em **"Create"**

### **Passo 4: Copiar o Conteúdo do Dashboard**
1. Abra o arquivo no seu computador:
   ```
   C:\Users\Donizete Senne\Desktop\Mob2Con-Central\03-Documentacao\📊 Dashboard Dados Reais.html
   ```

2. **Selecione TUDO** (Ctrl+A)
3. **Copie** (Ctrl+C)
4. Volte para o Google Apps Script
5. No arquivo `dashboard.html`, **apague tudo** que está lá
6. **Cole** o conteúdo copiado (Ctrl+V)
7. Clique em **💾 Salvar** (Ctrl+S)

### **Passo 5: Implantar como Web App**
1. No topo, clique em **"Deploy"** (Implantar) → **"New deployment"** (Nova implantação)
2. Clique no ícone de **engrenagem ⚙️** ao lado de "Select type"
3. Escolha **"Web app"**
4. Configure:
   - **Description**: "Dashboard RG 2.0 - Versão 1.0"
   - **Execute as**: **Me** (seu email)
   - **Who has access**: **Anyone** (Qualquer pessoa)
5. Clique em **"Deploy"** (Implantar)
6. **Autorize** o acesso (vai pedir permissão)
7. **COPIE A URL** que aparecer (algo como: `https://script.google.com/macros/s/AKfycby.../exec`)

### **Passo 6: Testar o Link**
1. Cole a URL no navegador
2. O dashboard deve abrir online! 🎉

---

## 🔄 ATUALIZAÇÕES FUTURAS

Quando você quiser atualizar o dashboard:

1. Abra o projeto no Apps Script
2. Edite o arquivo `dashboard.html`
3. Salve (Ctrl+S)
4. Clique em **"Deploy"** → **"Manage deployments"**
5. Clique no ícone de **lápis ✏️** ao lado da implantação ativa
6. Mude a versão para **"New version"**
7. Clique em **"Deploy"**
8. **O link continua o mesmo!** Não precisa copiar de novo

---

## 🌐 MÉTODO 2: GitHub Pages (ALTERNATIVO)

Se você preferir usar GitHub:

### **Passo 1: Criar Repositório**
1. Acesse: https://github.com
2. Clique em **"New repository"**
3. Nome: `dashboard-rg-20`
4. Marque **"Public"**
5. Clique em **"Create repository"**

### **Passo 2: Upload do Arquivo**
1. Clique em **"uploading an existing file"**
2. Arraste o arquivo `📊 Dashboard Dados Reais.html`
3. Renomeie para: `index.html`
4. Clique em **"Commit changes"**

### **Passo 3: Ativar GitHub Pages**
1. Vá em **Settings** (Configurações)
2. No menu lateral, clique em **"Pages"**
3. Em **"Source"**, escolha **"main"** branch
4. Clique em **"Save"**
5. Aguarde 1-2 minutos
6. O link aparecerá: `https://seu-usuario.github.io/dashboard-rg-20/`

---

## 🌐 MÉTODO 3: Google Drive (MAIS SIMPLES)

### **Passo 1: Upload para o Drive**
1. Acesse: https://drive.google.com
2. Clique em **"+ Novo"** → **"Upload de arquivo"**
3. Selecione: `📊 Dashboard Dados Reais.html`
4. Aguarde o upload

### **Passo 2: Compartilhar**
1. Clique com o botão direito no arquivo
2. Escolha **"Compartilhar"**
3. Em **"Acesso geral"**, escolha **"Qualquer pessoa com o link"**
4. Clique em **"Copiar link"**
5. **IMPORTANTE**: Modifique o link:
   - Link original: `https://drive.google.com/file/d/ID_DO_ARQUIVO/view?usp=sharing`
   - Link modificado: `https://drive.google.com/uc?export=download&id=ID_DO_ARQUIVO`

### **Passo 3: Visualizar**
- Cole o link modificado no navegador
- O arquivo será baixado
- Abra o arquivo baixado no navegador

**⚠️ LIMITAÇÃO**: O Google Drive não serve HTML diretamente como página web, então esse método não é ideal.

---

## ✅ RECOMENDAÇÃO FINAL

**Use o MÉTODO 1 (Google Apps Script)** porque:
- ✅ Cria um link online permanente
- ✅ Fácil de atualizar
- ✅ Não precisa baixar nada
- ✅ Funciona em qualquer dispositivo
- ✅ Você já tem experiência com Apps Script

---

## 🆘 PRECISA DE AJUDA?

Se tiver dúvidas em algum passo, me avise! Posso:
- Criar um vídeo tutorial
- Fazer passo a passo com você
- Criar uma versão simplificada

---

**Criado por**: Kiro AI  
**Data**: 15/05/2026
