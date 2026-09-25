"""Sonda interna de persistencia usada pelo teste de recuperacao automatica.

Nao envia mensagens e nao armazena dados pessoais. O registro sintetico sempre
usa a chave reservada ``__mob2con_recovery_probe__``.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from bot.config import carregar_config
from bot.persistencia import BancoSQLite
from bot.sessao import Sessao

NUMERO_SONDA = "__mob2con_recovery_probe__"


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("acao", choices=("gravar", "verificar", "limpar"))
    parser.add_argument("--marcador", default="")
    return parser.parse_args()


async def executar(acao: str, marcador: str) -> int:
    config = carregar_config()
    ttl_segundos = config.atendimento.minutos_sessao * 60
    banco = BancoSQLite(config.sqlite_path, ttl_segundos)
    try:
        if acao == "gravar":
            if not marcador:
                print("Marcador obrigatorio para gravar.")
                return 2
            sessao = Sessao(
                numero=NUMERO_SONDA,
                estado="menu",
                dados={"sonda_recuperacao": marcador},
            )
            await banco.salvar(sessao)
            print("SONDA_GRAVADA")
            return 0

        if acao == "verificar":
            sessao = await banco.obter(NUMERO_SONDA)
            if sessao is None:
                print("SONDA_AUSENTE")
                return 1
            if sessao.dados.get("sonda_recuperacao") != marcador:
                print("SONDA_DIVERGENTE")
                return 1
            print("SONDA_PERSISTIU")
            return 0

        await banco.remover(NUMERO_SONDA)
        print("SONDA_REMOVIDA")
        return 0
    finally:
        await banco.fechar()


def main() -> int:
    args = argumentos()
    return asyncio.run(executar(args.acao, args.marcador))


if __name__ == "__main__":
    raise SystemExit(main())
