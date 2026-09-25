"""Avalia rapidamente o roteamento do modelo configurado."""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from bot.config import carregar_config
from bot.llm import ClienteLLM


CASOS = [
    (
        "conhecer",
        "Queria entender como o MobConnect ajudaria minha operação.",
        "responder",
    ),
    (
        "suporte",
        "Já uso MobConnect e meu roteiro não abre, preciso de ajuda.",
        "suporte_mobconnect",
    ),
    (
        "comercial",
        "Gostei do MobConnect e quero uma proposta para minha empresa.",
        "encaminhar_comercial",
    ),
    (
        "humano",
        "Quero falar com uma pessoa do time.",
        "humano",
    ),
]


async def executar() -> int:
    config = carregar_config()
    cliente = ClienteLLM(config.llm)
    if not cliente.ativo:
        print("IA_INATIVA")
        return 1

    acertos = 0
    inicio_total = time.perf_counter()
    for nome, pergunta, esperado in CASOS:
        inicio = time.perf_counter()
        analise = await cliente.analisar(
            pergunta,
            estado="menu",
            dados_sessao={"produto": "MobConnect"} if nome != "humano" else {},
            historico=[],
            contexto_fluxo="Menu geral do atendimento Mob2Con.",
            contexto_conhecimento="",
        )
        segundos = time.perf_counter() - inicio
        recebido = analise.acao if analise else "NULA"
        confianca = analise.confianca if analise else 0.0
        ok = recebido == esperado
        acertos += int(ok)
        print(
            f"{nome.upper()} | esperado={esperado} | recebido={recebido} | "
            f"conf={confianca:.2f} | {segundos:.2f}s | {'OK' if ok else 'FALHA'}"
        )

    await cliente.fechar()
    total = time.perf_counter() - inicio_total
    print(f"RESULTADO={acertos}/{len(CASOS)} | TOTAL={total:.2f}s")
    return 0 if acertos == len(CASOS) else 2


if __name__ == "__main__":
    raise SystemExit(asyncio.run(executar()))
