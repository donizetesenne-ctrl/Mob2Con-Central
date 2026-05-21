"""
NVIDIA NIM Client — Stack de IA Gratuito Mob2Con
Conecta em 3 modelos gratuitos via NVIDIA Build:
  - Análise profunda (Nemotron Ultra 253B)
  - Geração de código (Nemotron Super 49B)
  - Layout/Visual (Nemotron Nano 12B VL)

Uso:
    from nvidia_nim_client import NvidiaStack
    stack = NvidiaStack()
    resposta = stack.analisar("Quais rotas tiveram pior SLA?")
"""

import json
import base64
import os
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Instale o pacote openai: pip install openai")


class NvidiaStack:
    """Cliente unificado para os 3 modelos NVIDIA NIM gratuitos."""

    def __init__(self, config_path: str = None):
        """Inicializa o stack carregando configuração."""
        if config_path is None:
            config_path = Path(__file__).parent / "config.json"

        if not Path(config_path).exists():
            raise FileNotFoundError(
                f"Config não encontrada: {config_path}\n"
                "Copie config_exemplo.json para config.json e insira sua API key."
            )

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.api_key = self.config["nvidia_api_key"]
        self.base_url = self.config["base_url"]

        if self.api_key.startswith("nvapi-COLE"):
            raise ValueError("Configure sua API key em config.json!")

        # Cliente OpenAI apontando para NVIDIA
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        self.modelos = self.config["modelos"]
        self.prompts = self.config["system_prompts"]

    def analisar(self, pergunta: str, contexto: str = "") -> str:
        """
        Análise profunda de dados usando Nemotron Ultra 253B.
        
        Args:
            pergunta: Pergunta sobre dados, KPIs, tendências
            contexto: Dados adicionais (tabela, CSV, métricas)
        
        Returns:
            Resposta analítica em português
        """
        modelo = self.modelos["analise"]
        messages = [
            {"role": "system", "content": self.prompts["analise"]},
        ]

        if contexto:
            messages.append({
                "role": "user",
                "content": f"Contexto dos dados:\n{contexto}\n\nPergunta: {pergunta}"
            })
        else:
            messages.append({"role": "user", "content": pergunta})

        response = self.client.chat.completions.create(
            model=modelo["nome"],
            messages=messages,
            max_tokens=modelo["max_tokens"],
            temperature=modelo["temperature"]
        )

        return response.choices[0].message.content

    def gerar_codigo(self, instrucao: str, linguagem: str = "python") -> str:
        """
        Gera código usando Nemotron Super 49B.
        
        Args:
            instrucao: O que o código deve fazer
            linguagem: Linguagem alvo (python, sql, dax, javascript)
        
        Returns:
            Código gerado
        """
        modelo = self.modelos["codigo"]
        messages = [
            {"role": "system", "content": self.prompts["codigo"]},
            {
                "role": "user",
                "content": f"Gere código {linguagem} para: {instrucao}"
            }
        ]

        response = self.client.chat.completions.create(
            model=modelo["nome"],
            messages=messages,
            max_tokens=modelo["max_tokens"],
            temperature=modelo["temperature"]
        )

        return response.choices[0].message.content

    def analisar_layout(self, imagem_path: str = None, imagem_base64: str = None,
                        pergunta: str = "Analise este layout e sugira melhorias.") -> str:
        """
        Analisa layout/imagem usando Nemotron Nano 12B VL (multimodal).
        
        Args:
            imagem_path: Caminho para arquivo de imagem (PNG, JPG)
            imagem_base64: Imagem já em base64
            pergunta: O que analisar na imagem
        
        Returns:
            Análise visual em português
        """
        modelo = self.modelos["layout"]

        if imagem_path and not imagem_base64:
            with open(imagem_path, "rb") as f:
                imagem_base64 = base64.b64encode(f.read()).decode("utf-8")

            # Detectar mime type
            ext = Path(imagem_path).suffix.lower()
            mime_map = {".png": "image/png", ".jpg": "image/jpeg",
                       ".jpeg": "image/jpeg", ".webp": "image/webp"}
            mime_type = mime_map.get(ext, "image/png")
        else:
            mime_type = "image/png"

        if imagem_base64:
            messages = [
                {"role": "system", "content": self.prompts["layout"]},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": pergunta},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{imagem_base64}"
                            }
                        }
                    ]
                }
            ]
        else:
            # Sem imagem — análise textual de layout
            messages = [
                {"role": "system", "content": self.prompts["layout"]},
                {"role": "user", "content": pergunta}
            ]

        response = self.client.chat.completions.create(
            model=modelo["nome"],
            messages=messages,
            max_tokens=modelo["max_tokens"],
            temperature=modelo["temperature"]
        )

        return response.choices[0].message.content

    def chat(self, mensagem: str, modelo_tipo: str = "analise",
             historico: list = None) -> str:
        """
        Chat genérico com qualquer um dos 3 modelos.
        
        Args:
            mensagem: Mensagem do usuário
            modelo_tipo: "analise", "codigo" ou "layout"
            historico: Lista de mensagens anteriores (opcional)
        
        Returns:
            Resposta do modelo
        """
        modelo = self.modelos[modelo_tipo]
        messages = [
            {"role": "system", "content": self.prompts[modelo_tipo]}
        ]

        if historico:
            messages.extend(historico)

        messages.append({"role": "user", "content": mensagem})

        response = self.client.chat.completions.create(
            model=modelo["nome"],
            messages=messages,
            max_tokens=modelo["max_tokens"],
            temperature=modelo["temperature"]
        )

        return response.choices[0].message.content

    def listar_modelos(self) -> dict:
        """Retorna informações sobre os modelos configurados."""
        return {
            tipo: {
                "modelo": info["nome"],
                "descricao": info["descricao"]
            }
            for tipo, info in self.modelos.items()
        }


# --- Execução direta para teste rápido ---
if __name__ == "__main__":
    print("=" * 60)
    print("NVIDIA NIM Stack — Mob2Con")
    print("=" * 60)

    try:
        stack = NvidiaStack()
        print("\n✅ Conexão configurada com sucesso!")
        print("\nModelos disponíveis:")
        for tipo, info in stack.listar_modelos().items():
            print(f"  [{tipo}] {info['modelo']}")
            print(f"          {info['descricao']}")

        print("\n--- Teste rápido: Análise ---")
        resp = stack.analisar("Explique em 2 frases o que é SLA em logística.")
        print(f"Resposta: {resp}")

    except FileNotFoundError as e:
        print(f"\n❌ {e}")
    except ValueError as e:
        print(f"\n❌ {e}")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
