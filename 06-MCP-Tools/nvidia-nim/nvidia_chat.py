"""
NVIDIA NIM - Cliente de Chat para Mob2Con
Usa a API gratuita da NVIDIA (OpenAI-compatible)

Uso:
    python nvidia_chat.py "Crie uma medida DAX de variação MoM"
    python nvidia_chat.py --model deepseek-ai/deepseek-v4-flash "Explique CALCULATE"
"""

import json
import sys
import os
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Instalando openai...")
    os.system("pip install openai")
    from openai import OpenAI


def load_config():
    """Carrega configuração do nvidia_config.json"""
    config_path = Path(__file__).parent / "nvidia_config.json"
    if not config_path.exists():
        print("ERRO: nvidia_config.json não encontrado!")
        print("Cole sua API key no arquivo nvidia_config.json")
        sys.exit(1)
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)["nvidia_nim"]


def chat(prompt, model=None, system_prompt=None):
    """Envia mensagem para a API NVIDIA NIM"""
    config = load_config()
    
    if config["api_key"] == "COLE_SUA_NVAPI_KEY_AQUI":
        print("ERRO: Configure sua API key em nvidia_config.json")
        print("Obtenha grátis em: https://build.nvidia.com/ → Avatar → API Keys")
        sys.exit(1)
    
    client = OpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"]
    )
    
    model = model or config["models"]["chat_principal"]
    
    if system_prompt is None:
        system_prompt = (
            "Você é um especialista em Power BI, DAX e análise de dados. "
            "Responda em português brasileiro. Seja direto e prático."
        )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=config["defaults"]["max_tokens"],
            temperature=config["defaults"]["temperature"],
            top_p=config["defaults"]["top_p"]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERRO: {e}"


def main():
    if len(sys.argv) < 2:
        print("Uso: python nvidia_chat.py \"sua pergunta aqui\"")
        print("     python nvidia_chat.py --model MODEL \"pergunta\"")
        print("\nModelos disponíveis (grátis):")
        config = load_config()
        for nome, modelo in config["models"].items():
            print(f"  {nome}: {modelo}")
        sys.exit(0)
    
    model = None
    prompt_args = sys.argv[1:]
    
    if "--model" in prompt_args:
        idx = prompt_args.index("--model")
        model = prompt_args[idx + 1]
        prompt_args = prompt_args[:idx] + prompt_args[idx + 2:]
    
    prompt = " ".join(prompt_args)
    
    print(f"🤖 Modelo: {model or 'nemotron-3-super-120b'}")
    print(f"📝 Pergunta: {prompt}")
    print("-" * 60)
    
    resposta = chat(prompt, model=model)
    print(resposta)


if __name__ == "__main__":
    main()
