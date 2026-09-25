"""Relatório operacional e replay redigido do chatbot.

Uso:
    python scripts/relatorio_qualidade.py
    python scripts/relatorio_qualidade.py --horas 72 --replay 30
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from bot.config import carregar_config
from bot.persistencia import BancoSQLite


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--horas", type=int, default=24)
    parser.add_argument("--replay", type=int, default=20)
    return parser.parse_args()


def horario(valor: float) -> str:
    return datetime.fromtimestamp(valor).astimezone().strftime("%d/%m %H:%M:%S")
async def executar() -> int:
    args = argumentos()
    config = carregar_config()
    caminho = config.sqlite_path
    if str(caminho) == ":memory:" or not caminho.exists():
        print(f"Banco ainda não existe: {caminho}")
        return 1

    banco = BancoSQLite(
        caminho,
        ttl_segundos=config.atendimento.minutos_sessao * 60,
    )
    try:
        resumo = await banco.resumo_eventos(args.horas)
        eventos = await banco.listar_eventos(args.replay)
    finally:
        await banco.fechar()

    print("=" * 72)
    print(f" QUALIDADE DO CHATBOT — ÚLTIMAS {resumo['horas']}H")
    print("=" * 72)
    print(f"  interações registradas : {resumo['total']}")
    print(f"  handoffs               : {resumo['handoffs']}")
    print(f"  latência média         : {resumo['latencia_media_ms']} ms")
    print("  fontes:")
    for fonte, total in resumo["fontes"].items():
        print(f"    - {fonte.ljust(20)} {total}")

    print()
    print("=" * 72)
    print(" REPLAY REDIGIDO")
    print("=" * 72)
    if not eventos:
        print("  Nenhum evento registrado ainda.")
        return 0

    for item in reversed(eventos):
        conf = item["confianca"]
        conf_txt = "-" if conf is None else f"{float(conf):.2f}"
        print(
            f"[{horario(item['criado_em'])}] {item['conversa_hash']} | "
            f"{item['estado_antes']} -> {item['estado_depois']} | "
            f"fonte={item['fonte']} | resultado={item['resultado']} | "
            f"conf={conf_txt} | {item['latencia_ms']}ms"
        )
        if item["mensagem_redigida"]:
            print(f"  > {item['mensagem_redigida']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(executar()))
