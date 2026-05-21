# 🤖 Guia Completo: Agentes Amazon Q + Kiro

> Criado em 15/05/2026 - Donizete Senne

---

## ✅ Status Atual

### Agentes Customizados Criados
Você tem **3 agentes customizados** configurados em:
`C:\Users\Donizete Senne\.aws\amazonq\agents\`

1. **google_ucm_expert.json** ☁️
   - Automação Google Workspace (Drive, Sheets, Docs, Gmail)
   - Universal Control MCP integrado
   - Backup automático ativado

2. **powerbi_expert.json** 📊
   - Especialista Power BI + DAX
   - Padrões Mob2Con integrados
   - Layout PBIP automatizado

3. **systems_engineer.json** 💻
   - Automação Windows + Python
   - Shell commands + Filesystem
   - AWS Docs integrado

### Extensão Agent Manager
✅ **Instalada e compilada** em:
`C:\Users\Donizete Senne\Desktop\Mob2Con-Central\agent-manager-for-q-cli\`

---

## 🚀 Como Usar no VS Code

### 1. Instalar a Extensão

1. Abra o VS Code
2. Pressione `Ctrl+Shift+P`
3. Digite: `Extensions: Install from VSIX...`
4. Navegue até: `agent-manager-for-q-cli\`
5. Selecione o arquivo `.vsix` (se existir) OU:

**Alternativa - Modo Desenvolvimento:**
```
1. Pressione F5 no VS Code com a pasta agent-manager-for-q-cli aberta
2. Isso abrirá uma nova janela do VS Code com a extensão carregada
```

### 2. Acessar o Agent Manager

1. No VS Code, procure o ícone 🤖 na barra lateral
2. Ou pressione `Ctrl+Shift+P` e digite: `Open Agent Manager for Q CLI`
3. Você verá seus 3 agentes listados!

### 3. Usar os Agentes

**Via Interface:**
- Clique com botão direito no agente
- Selecione "Run Agent in Terminal"

**Via Terminal:**
```bash
# Se o Q CLI estiver instalado:
q agent run google_ucm_expert
q agent run powerbi_expert
q agent run systems_engineer
```

---

## 🔧 Aqui no Kiro

### O que o Kiro pode fazer:

✅ **Gerenciar arquivos** (ler, escrever, editar)
✅ **Executar comandos** PowerShell/CMD
✅ **Instalar dependências** (npm, pip, etc)
✅ **Compilar projetos**
✅ **Integrar com MCPs** (Power BI, Google, etc)
✅ **Criar e editar código**
✅ **Buscar na web** e documentação

### O que o Kiro NÃO pode fazer:

❌ Abrir aplicativos GUI (Amazon Q, VS Code)
❌ Clicar em botões de interface
❌ Instalar extensões do VS Code diretamente

**Mas:** O Kiro pode preparar TUDO para você instalar manualmente!

---

## 📊 Dashboard - Problema e Solução

### Problema Identificado
O dashboard `📊 Dashboard Dados Reais.html` está com dados **hardcoded** (fixos).

O link do Google Apps Script existe mas **não é usado** pelo código JavaScript.

### Solução
O Kiro pode corrigir o código para:
1. Buscar dados do Google Apps Script automaticamente
2. Atualizar a cada abertura do dashboard
3. Mostrar indicador de "dados ao vivo" vs "dados locais"

---

## 🎯 Próximos Passos

### Opção 1: Focar nos Agentes
1. Abrir VS Code
2. Pressionar F5 na pasta `agent-manager-for-q-cli`
3. Testar os agentes na nova janela

### Opção 2: Corrigir o Dashboard
1. Deixar o Kiro corrigir o código JavaScript
2. Testar a atualização automática
3. Validar os dados

### Opção 3: Fazer Tudo! 🚀
1. Kiro corrige o dashboard AGORA
2. Você testa os agentes no VS Code
3. Integramos tudo!

---

## 💡 Dicas

- Os agentes já estão configurados corretamente
- A extensão está compilada e pronta
- O dashboard só precisa de um ajuste no JavaScript
- Todos os MCPs estão funcionando

**Você está a 1 passo de ter tudo funcionando! 🎉**

---

## 📞 Suporte

Se algo não funcionar:
1. Verifique se o Amazon Q está instalado
2. Confirme que o Q CLI está no PATH
3. Teste os MCPs individualmente
4. Peça ajuda ao Kiro! 😊
