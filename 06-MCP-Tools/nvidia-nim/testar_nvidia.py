"""
Teste rápido da conexão com NVIDIA NIM
Execute: python testar_nvidia.py
"""

import json
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Instalando openai...")
    import os
    os.system("pip install openai")
    from openai import OpenAI


def main():
    config_path = Path(__file__).parent / "nvidia_config.json"
    
    if not config_path.exists():
        print("❌ nvidia_config.json não encontrado!")
        sys.exit(1)
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)["nvidia_nim"]
    
    if config["api_key"] == "COLE_SUA_NVAPI_KEY_AQUI":
        print("⚠️  API Key não configurada!")
        print()
        print("Para obter sua chave GRÁTIS:")
        print("  1. Acesse: https://build.nvidia.com/")
        print("  2. Faça login (Google/GitHub)")
        print("  3. Avatar → API Keys → Generate")
        print("  4. Cole no nvidia_config.json")
        sys.exit(1)
    
    print("🔌 Testando conexão com NVIDIA NIM...")
    print(f"   Base URL: {config['base_url']}")
    print(f"   Modelo: {config['models']['chat_principal']}")
    print()
    
    client = OpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"]
    )
    
    try:
        response = client.chat.completions.create(
            model=config["models"]["chat_principal"],
            messages=[
                {"role": "user", "content": "Responda apenas: OK"}
            ],
            max_tokens=5
        )
        
        resposta = response.choices[0].message.content.strip()
        print(f"✅ Conexão OK! Resposta: {resposta}")
        print(f"   Modelo usado: {response.model}")
        print(f"   Tokens: {response.usage.total_tokens}")
        print()
        print("🎉 NVIDIA NIM configurado com sucesso!")
        print("   Use: python nvidia_chat.py \"sua pergunta\"")
        print("   Use: python nvidia_dax_generator.py \"medida que precisa\"")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
        print("Verifique:")
        print("  - API key está correta?")
        print("  - Tem conexão com internet?")
        sys.exit(1)


if __name__ == "__main__":
    main()
