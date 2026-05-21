"""
MCP Server — NVIDIA NIM Mob2Con
Protocolo: JSON-RPC over stdio (newline-delimited JSON)
"""

import json
import sys
import os
from pathlib import Path

# Força unbuffered mode
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Log para stderr
def log(msg):
    sys.stderr.write(f"[nvidia-nim] {msg}\n")
    sys.stderr.flush()

# Adiciona o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

log("Servidor iniciado v2.0")

# Cliente NVIDIA (pré-carregado)
_stack = None

def init_stack():
    """Inicializa o stack NVIDIA na startup."""
    global _stack
    try:
        log("Carregando Stack NVIDIA...")
        from nvidia_nim_client import NvidiaStack
        _stack = NvidiaStack()
        log("Stack NVIDIA carregado com sucesso!")
        return True
    except Exception as e:
        log(f"ERRO ao carregar stack: {e}")
        _stack = None
        return False

def get_stack():
    global _stack
    if _stack is None:
        raise RuntimeError("Stack NVIDIA não foi inicializado. Verifique os logs de startup.")
    return _stack


def send_response(msg):
    """Envia resposta JSON + newline para stdout."""
    try:
        out = json.dumps(msg, ensure_ascii=False)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
        log(f">> {msg.get('method', 'response')} id={msg.get('id')}")
    except Exception as e:
        log(f"Erro ao enviar resposta: {e}")


def handle_initialize(request_id, params):
    proto = params.get("protocolVersion", "2024-11-05")
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": proto,
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "nvidia-nim-mob2con",
                "version": "1.0.0"
            }
        }
    }


def handle_tools_list(request_id):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "nvidia_analisar",
                    "description": "Analise profunda de dados usando Llama 3.3 70B via NVIDIA NIM. Interpreta KPIs, tendencias, SLA, gera insights e sugere medidas DAX.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "pergunta": {
                                "type": "string",
                                "description": "Pergunta sobre dados, KPIs ou logica de negocio"
                            },
                            "contexto": {
                                "type": "string",
                                "description": "Dados adicionais para contextualizar. Opcional."
                            }
                        },
                        "required": ["pergunta"]
                    }
                },
                {
                    "name": "nvidia_gerar_codigo",
                    "description": "Geracao de codigo usando Nemotron Super 49B via NVIDIA NIM. Cria apps Streamlit, FastAPI, SQL, DAX, Python.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "instrucao": {
                                "type": "string",
                                "description": "O que o codigo deve fazer"
                            },
                            "linguagem": {
                                "type": "string",
                                "description": "python, sql, dax, javascript",
                                "default": "python"
                            }
                        },
                        "required": ["instrucao"]
                    }
                },
                {
                    "name": "nvidia_analisar_layout",
                    "description": "Analise de layout usando Nemotron Nano 12B VL (multimodal) via NVIDIA NIM. Avalia dashboards e sugere melhorias de UX.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "pergunta": {
                                "type": "string",
                                "description": "O que analisar sobre o layout"
                            },
                            "imagem_path": {
                                "type": "string",
                                "description": "Caminho para imagem PNG/JPG. Opcional."
                            }
                        },
                        "required": ["pergunta"]
                    }
                }
            ]
        }
    }


def handle_tool_call(request_id, tool_name, arguments):
    try:
        stack = get_stack()
        if tool_name == "nvidia_analisar":
            resultado = stack.analisar(
                pergunta=arguments["pergunta"],
                contexto=arguments.get("contexto", "")
            )
        elif tool_name == "nvidia_gerar_codigo":
            resultado = stack.gerar_codigo(
                instrucao=arguments["instrucao"],
                linguagem=arguments.get("linguagem", "python")
            )
        elif tool_name == "nvidia_analisar_layout":
            resultado = stack.analisar_layout(
                imagem_path=arguments.get("imagem_path"),
                pergunta=arguments["pergunta"]
            )
        else:
            resultado = f"Ferramenta desconhecida: {tool_name}"

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{"type": "text", "text": resultado}]
            }
        }
    except Exception as e:
        log(f"Erro tool {tool_name}: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{"type": "text", "text": f"Erro: {str(e)}"}],
                "isError": True
            }
        }


def main():
    log("Aguardando mensagens MCP...")
    
    # Pré-carrega o stack NVIDIA para evitar timeout no primeiro uso
    if not init_stack():
        log("AVISO: Stack NVIDIA não carregou. Ferramentas podem falhar.")

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                log("Linha vazia, ignorando")
                continue

            log(f"Recebido: {line[:100]}...")

            try:
                message = json.loads(line)
            except json.JSONDecodeError as e:
                log(f"JSON invalido: {e}")
                continue

            method = message.get("method", "")
            request_id = message.get("id")
            params = message.get("params", {})

            log(f"<< {method} id={request_id}")

            response = None

            if method == "initialize":
                response = handle_initialize(request_id, params)
            elif method == "notifications/initialized":
                log("Cliente inicializado")
            elif method == "notifications/cancelled":
                log(f"Requisição cancelada: {params}")
            elif method == "tools/list":
                response = handle_tools_list(request_id)
            elif method == "tools/call":
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                response = handle_tool_call(request_id, tool_name, arguments)
            elif method == "ping":
                response = {"jsonrpc": "2.0", "id": request_id, "result": {}}
            else:
                log(f"Método desconhecido: {method}")
                if request_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Not found: {method}"}
                    }

            if response is not None:
                send_response(response)

    except KeyboardInterrupt:
        log("Interrompido pelo usuário")
    except Exception as e:
        log(f"Erro fatal: {e}")
        import traceback
        log(traceback.format_exc())

    log("Servidor encerrado")


if __name__ == "__main__":
    main()
