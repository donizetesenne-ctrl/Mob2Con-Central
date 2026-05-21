"""
Teste local do servidor MCP NVIDIA
Simula o que o Kiro faz para debugar problemas
"""

import subprocess
import json
import sys

def testar_servidor():
    print("=" * 60)
    print("TESTE LOCAL — Servidor MCP NVIDIA")
    print("=" * 60)
    
    # Inicia o servidor
    cmd = [
        "python", "-u",
        r"C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\nvidia-nim\mcp_nvidia_server.py"
    ]
    
    print(f"\n1. Iniciando servidor: {' '.join(cmd)}")
    
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    def enviar(msg):
        linha = json.dumps(msg) + "\n"
        print(f"\n>> Enviando: {msg.get('method', 'response')}")
        proc.stdin.write(linha)
        proc.stdin.flush()
    
    def receber():
        linha = proc.stdout.readline()
        if linha:
            print(f"<< Recebido: {linha[:100]}...")
            return json.loads(linha)
        return None
    
    try:
        # 1. Initialize
        print("\n2. Enviando initialize...")
        enviar({
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "teste-local", "version": "1.0"}
            }
        })
        
        resp = receber()
        if resp and resp.get("result"):
            print("✅ Initialize OK!")
            print(f"   Servidor: {resp['result'].get('serverInfo', {}).get('name')}")
        else:
            print("❌ Initialize falhou!")
            return
        
        # 2. Tools list
        print("\n3. Enviando tools/list...")
        enviar({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        })
        
        resp = receber()
        if resp and resp.get("result"):
            tools = resp["result"].get("tools", [])
            print(f"✅ Tools list OK! {len(tools)} ferramentas:")
            for t in tools:
                print(f"   - {t['name']}")
        else:
            print("❌ Tools list falhou!")
            return
        
        # 3. Tool call (teste rápido)
        print("\n4. Testando nvidia_analisar...")
        enviar({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "nvidia_analisar",
                "arguments": {
                    "pergunta": "O que é SLA em logística? Responda em 1 frase."
                }
            }
        })
        
        resp = receber()
        if resp and resp.get("result"):
            content = resp["result"].get("content", [])
            if content:
                texto = content[0].get("text", "")
                print(f"✅ Tool call OK!")
                print(f"   Resposta: {texto[:200]}...")
            else:
                print("❌ Tool call sem conteúdo!")
        else:
            print("❌ Tool call falhou!")
        
        print("\n" + "=" * 60)
        print("TESTE CONCLUÍDO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Lê stderr para ver logs
        print("\n--- LOGS DO SERVIDOR (stderr) ---")
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=2)
        
        stderr = proc.stderr.read()
        if stderr:
            print(stderr)
        else:
            print("(sem logs)")


if __name__ == "__main__":
    testar_servidor()
