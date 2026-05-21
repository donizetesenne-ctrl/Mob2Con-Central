import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

# --- CONFIGURAÇÃO ---
# Recomenda-se definir a variável de ambiente GEMINI_API_KEY
API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_CHAVE_AQUI")
genai.configure(api_key=API_KEY)

# Modelo otimizado para código e com janela de contexto de 1M de tokens
MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

# --- MAPA DE CONTEXTO ---
BASE_PATHS = {
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "projetos_bi": os.path.join(os.path.expanduser("~"), "Desktop", "projetos BI"),
    "universal_mcp": os.path.join(os.path.expanduser("~"), "Desktop", "Mob2Con_MCP_Setup", "universal-control-mcp")
}

def carregar_contexto_projeto() -> str:
    """Carrega arquivos chave para dar contexto à IA sobre as regras de negócio."""
    contexto = ""
    
    # Tenta carregar o plano do Nordestão
    plano_nordestao = os.path.join(BASE_PATHS["desktop"], "NORDESTAO_DASHBOARD_PLAN.md")
    if os.path.exists(plano_nordestao):
        with open(plano_nordestao, 'r', encoding='utf-8') as f:
            contexto += f"\n--- PLANO NORDESTÃO ---\n{f.read()}\n"
            
    # Tenta carregar o README do Mob2Con Bridge
    readme_bi = os.path.join(BASE_PATHS["projetos_bi"], "README.md")
    if os.path.exists(readme_bi):
        with open(readme_bi, 'r', encoding='utf-8') as f:
            contexto += f"\n--- README PROJETOS BI ---\n{f.read()}\n"
            
    return contexto

def analisar_codigo_e_corrigir(caminho_arquivo: str, instrucao_extra: str = ""):
    """Analisa um arquivo e sugere correções baseadas nas MCPs disponíveis."""
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        return

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    contexto_negocio = carregar_contexto_projeto()
    
    prompt = f"""
Você é um Engenheiro de IA especialista em Mob2Con, Power BI e Google Cloud.
Sua missão é verificar o código abaixo e identificar erros ou melhorias.

--- CONTEXTO DO PROJETO ---
{contexto_negocio}

--- CÓDIGO PARA ANÁLISE ---
Arquivo: {os.path.basename(caminho_arquivo)}
Conteúdo:
{codigo}

--- FERRAMENTAS DISPONÍVEIS (via MCP) ---
Você pode sugerir o uso das seguintes ferramentas do 'universal-control-mcp':
- smart_edit_google: Para atualizar Sheets/Docs.
- review_file (reviewType='dax'): Para analisar medidas Power BI.
- powerbi-layout (server.js): Para ajustar temas e cores Mob2Con.

--- INSTRUÇÃO EXTRA ---
{instrucao_extra}

Por favor, forneça:
1. Lista de erros encontrados.
2. Sugestão de correção (em código).
3. Qual ferramenta MCP usar para aplicar a correção.
"""

    print(f"🚀 Analisando {os.path.basename(caminho_arquivo)}...")
    response = model.generate_content(prompt)
    
    relatorio_path = caminho_arquivo + ".analise.md"
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print(f"✅ Análise concluída! Relatório salvo em: {relatorio_path}")
    print("\n--- RESUMO DA IA ---\n")
    print(response.text[:1000] + "...")

if __name__ == "__main__":
    # Exemplo de uso: Analisando o script de correção de sprint
    script_alvo = os.path.join(BASE_PATHS["desktop"], "fix_sprint_ic.py")
    analisar_codigo_e_corrigir(script_alvo, "Verifique se a lógica de integração com Google Sheets está correta conforme as novas MCPs.")
