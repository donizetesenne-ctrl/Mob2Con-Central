# Mob2Con-Central Workspace Rules

## Contexto do Projeto
- Workspace: C:\Users\Donizete Senne\Desktop\Mob2Con-Central
- Empresa: Mob2Con (consultoria BI e automação)
- Cor primária: #F46901 (laranja), Grafite: #434343, Azul MobConnect: #4285F4
- Tipografia: Raleway (Black, Bold, Regular)

## Estrutura
- 01-Brand-Guidelines/ → identidade visual, design tokens, temas PBI
- 02-Powerbi-Projetos/ → projetos .pbip (Nordestão, Analítico RG, Captação RG)
- 03-Documentacao/ → docs, relatórios, guias
- 04-Dados-Fontes/ → bases Excel
- 05-Apresentacoes/ → PPTx
- 06-MCP-Tools/ → MCPs, scripts, agent-manager
- 07-AI-Tools/ → compressão de prompt, cache, observabilidade, AI agents
- 08-Automacao/ → wexflow, maestro, n8n-workflows, steel-mcp-server
- 09-Integracao-Dados/ → airbyte

## MCPs Ativos (Kiro + Amazon Q)
- powerbi (nativo MS) → modelagem semântica
- powerbi-layout → posicionamento x/y/width/height de visuais
- powerbi-bridge → 60+ tools de branding, medidas, visuais
- universal_control → Google Sheets, Drive, Gmail, Calendar
- aws-docs → documentação AWS
- filesystem → acesso a arquivos locais
- shell-command → execução de comandos

## Ferramentas Python Disponíveis
- LLMLingua → compressão de prompt (até 20x)
- Langfuse → observabilidade de tokens
- Tiktoken → contagem de tokens
- PyTorch + Transformers → modelos locais
- Cache semântico → 07-AI-Tools/cache.py

## Regras de Código
- Sempre usar caminhos absolutos para Mob2Con-Central
- DAX: seguir padrões em 03-Documentacao/Mob2con-dax-medidas-padrao.md
- Temas PBI: usar 02-Powerbi-Projetos/Mob2Con-Brand-Theme.json
- Design tokens: 01-Brand-Guidelines/design-system/design-tokens.json
