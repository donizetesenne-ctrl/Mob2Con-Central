# NVIDIA NIM — Stack de IA Gratuito Mob2Con

## Visão Geral

Stack de 3 modelos de IA gratuitos via NVIDIA Build para o ecossistema Mob2Con:

| Função | Modelo | Uso |
|--------|--------|-----|
| 🧠 Análise Profunda | `nvidia/llama-3.1-nemotron-ultra-253b-v1` | KPIs, insights, lógica de negócio, DAX |
| 💻 Criação de App | `nvidia/llama-3.3-nemotron-super-49b-v1` | Código Python, Streamlit, FastAPI, SQL |
| 🎨 Layout/UI | `nvidia/nemotron-nano-12b-v2-vl` | Leitura de imagens, wireframes, dashboards |

## Pré-requisitos

1. Criar conta gratuita em https://build.nvidia.com
2. Gerar API key em https://org.ngc.nvidia.com/setup/api-keys
3. Copiar `config_exemplo.json` para `config.json` e inserir sua key

## Instalação

```cmd
cd 06-MCP-Tools\nvidia-nim
pip install openai requests
```

## Uso Rápido

```python
from nvidia_nim_client import NvidiaStack

stack = NvidiaStack()

# Análise de dados
resposta = stack.analisar("Quais KPIs de SLA estão abaixo da meta?")

# Gerar código
codigo = stack.gerar_codigo("Crie um dashboard Streamlit com gráfico de barras")

# Analisar layout (imagem)
analise = stack.analisar_layout("caminho/para/screenshot.png")
```

## Créditos Gratuitos

- 1.000 créditos ao criar conta
- Até 5.000 no programa de desenvolvedor
- API compatível com padrão OpenAI (mesma sintaxe)

## Arquivos

```
nvidia-nim/
├── README.md                 ← este arquivo
├── config_exemplo.json       ← template de configuração
├── config.json               ← sua config (não commitar!)
├── nvidia_nim_client.py      ← cliente principal (3 modelos)
├── demo_analise.py           ← demo: análise de dados
├── demo_codigo.py            ← demo: geração de código
├── demo_layout.py            ← demo: análise de layout
└── .gitignore                ← ignora config.json com secrets
```
