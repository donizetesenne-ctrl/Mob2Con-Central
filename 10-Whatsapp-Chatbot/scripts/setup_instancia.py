"""Cria a instância, registra o webhook e mostra o QR Code para pareamento.

Uso:
    python scripts/setup_instancia.py
    python scripts/setup_instancia.py --webhook https://meu-tunel.trycloudflare.com/webhook
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import os
import sys
from pathlib import Path

from _comum import PROJETO_DIR, carregar

sys.path.insert(0, str(Path(__file__).resolve().parent))

EVENTOS = ["MESSAGES_UPSERT"]


def _salvar_qrcode(base64_bruto: str) -> Path | None:
    """Grava o QR Code em PNG e devolve o caminho."""
    if not base64_bruto:
        return None
    dados = base64_bruto.split(",", 1)[-1]
    try:
        binario = base64.b64decode(dados)
    except (ValueError, TypeError):
        return None
    destino = PROJETO_DIR / "qrcode.png"
    destino.write_bytes(binario)
    return destino


async def executar(url_webhook: str, aguardar: int) -> int:
    config, cliente = carregar()
    instancia = config.evolution.instancia

    async with cliente:
        # 1. instância
        print(f"[1/4] Garantindo a instância '{instancia}'...")
        try:
            await cliente.criar_instancia()
            print("      criada.")
        except Exception as erro:  # noqa: BLE001 - já existir não é problema
            texto = str(erro).lower()
            if "already in use" in texto or "already exists" in texto or "409" in texto:
                print("      já existia, seguindo.")
            else:
                print(f"[X] Falha ao criar a instância: {erro}")
                return 1

        # 2. webhook
        print(f"[2/4] Apontando o webhook para {url_webhook}")
        try:
            await cliente.definir_webhook(url_webhook, EVENTOS)
            print("      registrado.")
        except Exception as erro:  # noqa: BLE001
            print(f"[!] Não foi possível registrar o webhook: {erro}")
            print("    Configure manualmente no Manager depois.")

        # 3. estado / QR
        print("[3/4] Verificando conexão...")
        estado = await cliente.estado_conexao()
        situacao = str(
            (estado.get("instance") or {}).get("state") or estado.get("state") or ""
        ).lower()
        if situacao == "open":
            print("      WhatsApp ja conectado. Nada a parear.")
            return 0

        conexao = await cliente.conectar()
        caminho = _salvar_qrcode(str(conexao.get("base64") or ""))
        codigo = conexao.get("pairingCode") or conexao.get("code")

        print("[4/4] Pareamento")
        if caminho:
            print(f"      QR Code salvo em: {caminho}")
            if os.name == "nt":
                os.startfile(caminho)  # noqa: S606 - abre o visualizador de imagens
        if codigo:
            print(f"      Código de pareamento: {codigo}")
        print()
        print("      No celular: WhatsApp > Configurações > Dispositivos conectados")
        print("      > Conectar dispositivo > escaneie o QR (ou use o código).")
        print()

        if aguardar <= 0:
            return 0

        print(f"      Aguardando conexão por até {aguardar}s...")
        for _ in range(aguardar):
            await asyncio.sleep(1)
            estado = await cliente.estado_conexao()
            situacao = str(
                (estado.get("instance") or {}).get("state") or estado.get("state") or ""
            ).lower()
            if situacao == "open":
                print("      Conectado!")
                if caminho and caminho.exists():
                    caminho.unlink(missing_ok=True)
                return 0
        print("      Tempo esgotado. Rode o script de novo para gerar outro QR.")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # Modo A (gateway local) usa localhost; no Modo B (Docker) o host é o
    # nome do serviço, então lá passe --webhook http://bot:8000/webhook
    padrao_webhook = (
        os.environ.get("WEBHOOK_URL")
        or os.environ.get("GATEWAY_WEBHOOK_URL")
        or "http://localhost:8000/webhook"
    )
    parser.add_argument(
        "--webhook",
        default=padrao_webhook,
        help=f"URL que o motor vai chamar (padrão: {padrao_webhook})",
    )
    parser.add_argument(
        "--aguardar",
        type=int,
        default=120,
        help="segundos aguardando o pareamento (0 = não aguardar)",
    )
    argumentos = parser.parse_args()
    return asyncio.run(executar(argumentos.webhook, argumentos.aguardar))


if __name__ == "__main__":
    raise SystemExit(main())
