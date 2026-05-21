# 📄 Mob2Con Doc Converters

Módulo unificado com **3 engines** para converter documentos em Markdown/JSON otimizado para LLMs.

## Engines

| # | Engine | Melhor para | GitHub |
|---|--------|-------------|--------|
| 1 | **Docling** | Tabelas complexas, Office, web pages | [DS4SD/docling](https://github.com/DS4SD/docling) |
| 2 | **Marker** | PDFs com imagens, equações, artefatos | [VikParuchuri/marker](https://github.com/VikParuchuri/marker) |
| 3 | **MinerU** | Documentos científicos, fórmulas, gráficos | [opendatalab/MinerU](https://github.com/opendatalab/MinerU) |

## Instalação

```cmd
INSTALAR.bat
```

Ou manual:
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
# Arquivo único
python converter.py relatorio.pdf --engine docling --output md
python converter.py planilha.xlsx --engine docling --output json

# PDF com imagens
python converter.py dashboard.pdf --engine marker

# Documento científico
python converter.py paper.pdf --engine mineru

# Pasta inteira (batch)
python converter.py "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\04-Dados-Fontes" --batch
```

## Quando usar cada engine

- **Docling** → Default. Excel, Word, PPT, tabelas complexas, páginas web
- **Marker** → PDFs pesados com imagens embutidas, cabeçalhos/rodapés para remover, equações
- **MinerU** → Papers acadêmicos, relatórios com fórmulas matemáticas e gráficos científicos

## Integração com Mob2Con

Converta os arquivos de `04-Dados-Fontes/` para Markdown antes de alimentar o agente:

```bash
python converter.py "..\..\04-Dados-Fontes\Mob2Con_Base_Consolidada_PowerBI.xlsx" --engine docling --output md
```

O resultado em Markdown pode ser usado diretamente pelo Amazon Q ou qualquer LLM.
