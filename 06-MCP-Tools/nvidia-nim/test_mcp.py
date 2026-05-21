"""Testa se o MCP server responde ao initialize corretamente."""
import subprocess
import json
import sys

# Mensagem initialize do protocolo MCP
init_msg = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    }
})

# Formata com Content-Length header
payload = f"Content-Length: {len(init_msg.encode('utf-8'))}\r\n\r\n{init_msg}"

# Executa o servidor e envia a mensagem
proc = subprocess.Popen(
    [sys.executable, "mcp_nvidia_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd=r"C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\nvidia-nim"
)

stdout, stderr = proc.communicate(input=payload.encode("utf-8"), timeout=10)

print("=== STDOUT ===")
print(stdout.decode("utf-8", errors="replace"))
print("\n=== STDERR ===")
print(stderr.decode("utf-8", errors="replace"))
print(f"\n=== Exit code: {proc.returncode} ===")
