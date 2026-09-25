"""Envia uma mensagem de teste pela instância configurada.

Uso:
    python scripts/enviar.py 5511999998888 "Teste do chatbot Mob2Con"
"""

from __future__ import annotations

import argparse
import asyncio

from _comum import carregar


async def executar(numero: str, texto: str) -> int:
    _config, cliente = carregar()
    async with cliente:
        try:
            resposta = await cliente.enviar_texto(numero, texto)
        except Exception as erro:  # noqa: BLE001
            print(f"[X] Falha no envio: {erro}")
            return 1
    identificador = (resposta.get("key") or {}).get("id", "?")
    print(f"[OK] Enviado para {numero} (id={identificador})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numero", help="DDI+DDD+número, ex: 5511999998888")
    parser.add_argument("texto", help="mensagem a enviar")
    argumentos = parser.parse_args()
    return asyncio.run(executar(argumentos.numero, argumentos.texto))


if __name__ == "__main__":
    raise SystemExit(main())
