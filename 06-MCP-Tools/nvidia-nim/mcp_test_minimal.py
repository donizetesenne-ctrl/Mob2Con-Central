"""MCP Server minimo para teste de conexao."""
import sys
import json

def log(msg):
    sys.stderr.write(f"[test] {msg}\n")
    sys.stderr.flush()

log("iniciado")

while True:
    log("lendo header...")
    line = sys.stdin.readline()
    log(f"header line: {repr(line)}")
    if not line:
        log("EOF")
        break
    if line.strip().startswith("Content-Length"):
        length = int(line.strip().split(":")[1])
        log(f"content-length={length}")
        # le linha vazia
        sys.stdin.readline()
        log("lendo body...")
        body = sys.stdin.read(length)
        log(f"body={body[:100]}")
        msg = json.loads(body)
        method = msg.get("method", "")
        rid = msg.get("id")
        log(f"method={method} id={rid}")

        if method == "initialize":
            resp = {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"test","version":"0.1"}}}
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            resp = {"jsonrpc":"2.0","id":rid,"result":{"tools":[]}}
        elif method == "ping":
            resp = {"jsonrpc":"2.0","id":rid,"result":{}}
        else:
            resp = {"jsonrpc":"2.0","id":rid,"result":{}}

        out = json.dumps(resp)
        sys.stdout.write(f"Content-Length: {len(out)}\r\n\r\n{out}")
        sys.stdout.flush()
        log(f"enviado id={rid}")
