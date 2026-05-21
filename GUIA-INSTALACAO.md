# 📦 Mob2Con Central — Guia de Instalação

## ⚡ Instalação Rápida (1 clique)

1. **Duplo-clique** em `INSTALAR.bat`
2. Siga as instruções na tela
3. Reinicie o Kiro / Amazon Quick
4. Pronto!

---

## 🔧 Instalação Manual (passo a passo)

### Pré-requisitos

| Software | Versão mínima | Download |
|----------|---------------|----------|
| **Node.js** | v18+ | https://nodejs.org |
| **Python + uv** | 3.10+ | `pip install uv` |
| **Power BI Desktop** | Qualquer | Microsoft Store |
| **VS Code ou Kiro** | Qualquer | https://kiro.dev |
| **Extensão Power BI MCP** | 0.4.0+ | Marketplace do VS Code: "Power BI Modeling MCP" |

### Passo 1: Copiar a pasta

Copie a pasta `Mob2Con-Central` inteira para sua **Área de Trabalho**:
```
C:\Users\<SEU_USUARIO>\Desktop\Mob2Con-Central\
```

### Passo 2: Configurar Kiro

Crie/edite o arquivo `C:\Users\<SEU_USUARIO>\.kiro\settings\mcp.json`:

```json
{
  "mcpServers": {
    "aws-docs": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": { "FASTMCP_LOG_LEVEL": "ERROR" },
      "disabled": false
    },
    "powerbi-layout": {
      "command": "node",
      "args": ["<CAMINHO_CURTO>\\Downloads\\Mob2Con-Bridge-v2.0.0\\mcp\\powerbi-layout-mcp\\server.js"],
      "type": "stdio",
      "env": {
        "POWERBI_PROJECT_PATH": "<CAMINHO_CURTO>\\Desktop\\Mob2Con-Central\\02-Powerbi-Projetos",
        "MOB2CON_BRAND_CONTEXT": "<CAMINHO_CURTO>\\Desktop\\Mob2Con-Central\\01-Brand-Guidelines\\Mob2con-brand-guidelines.md",
        "MOB2CON_LAYOUT_BASE": "<CAMINHO_CURTO>\\Desktop\\Mob2Con-Central\\01-Brand-Guidelines\\Mob2con-layout-base.md"
      }
    }
  }
}
```

> ⚠️ **IMPORTANTE:** Se seu nome de usuário tem espaço (ex: "Donizete Senne"), use o caminho curto 8.3.
> Para descobrir: abra CMD e digite `dir /x C:\Users\`
> Exemplo: `C:\Users\DONIZE~1` em vez de `C:\Users\Donizete Senne`

### Passo 3: Aplicar tema no Power BI

1. Abra seu projeto `.pbip` no Power BI Desktop
2. Vá em **View → Themes → Browse for themes**
3. Navegue até `Mob2Con-Central\01-Brand-Guidelines\`
4. Selecione o tema desejado:
   - `Mob2Con-Theme.json` (institucional, laranja)
   - `MobConnect-Theme.json` (azul, só para MobConnect)
   - `ReposicaoGarantida-Theme.json` (tripla cor)
5. Salve o projeto (Ctrl+S)

### Passo 4: Reiniciar apps

- Feche e abra o **Kiro**
- Feche e abra o **Amazon Quick** (se usar)
- Verifique que as MCPs aparecem como "Connected"

---

## ✅ Verificação

Após instalar, verifique:

- [ ] Pasta `Mob2Con-Central` está no Desktop
- [ ] Kiro mostra MCPs `aws-docs` e `powerbi-layout` como ativas
- [ ] Power BI Desktop aceita o tema (cores laranja Mob2Con aparecem)
- [ ] Fonte Raleway está instalada no sistema (opcional mas recomendado)

### Instalar fonte Raleway (opcional)

1. Baixe de: https://fonts.google.com/specimen/Raleway
2. Extraia o ZIP
3. Selecione todos os `.ttf` → clique direito → "Instalar para todos os usuários"
4. Reinicie o Power BI Desktop

---

## 📋 Conteúdo incluído

| Pasta | O que contém |
|-------|-------------|
| `01-Brand-Guidelines/` | Paleta, fontes, 3 temas .json, layouts, botões, efeitos |
| `02-Powerbi-Projetos/` | Projetos .pbip de exemplo |
| `03-Documentacao/` | Biblioteca DAX, produtos Mob2Con, guia de capacidades |
| `04-Dados-Fontes/` | Bases Excel consolidadas |
| `05-Apresentacoes/` | Template PPT oficial |
| `06-MCP-Tools/` | Scripts e configs de MCP |

---

## 🆘 Problemas comuns

### "MCP com erro no Amazon Quick"
→ Verifique se o caminho do `node` e dos arquivos `.js` estão corretos
→ Use caminho curto 8.3 se seu usuário tem espaço no nome

### "Tema não aplica no Power BI"
→ Verifique se o JSON é válido (abra no VS Code, sem erros de sintaxe)
→ Reinicie o Power BI Desktop após aplicar

### "Fonte Raleway não aparece"
→ Instale a fonte no sistema (não basta ter o arquivo)
→ Reinicie o Power BI Desktop após instalar a fonte

### "powerbi-layout não conecta"
→ Verifique se `node_modules` existe na pasta do MCP
→ Execute: `cd <pasta-do-mcp> && npm install`

---

## 📞 Suporte

Criado por: Mob2Con + Kiro AI Assistant
Data: Maio 2026
Versão: 1.0
