"""Teste rápido do provedor de IA configurado, sem imprimir segredos."""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from bot.config import carregar_config
from bot.llm import ClienteLLM


PERGUNTA = (
    "Sou da Uau, temos 10 promotores em uma loja e quero entender "
    "se o MobConnect ajuda a acompanhar execução."
)


async def executar() -> int:
    config = carregar_config()
    cliente = ClienteLLM(config.llm)
    if not cliente.ativo:
        print("IA_INATIVA")
        return 1

    inicio = time.perf_counter()
    analise = await cliente.analisar(
        PERGUNTA,
        estado="menu",
        dados_sessao={
            "empresa_contato": "Uau",
            "porte": "10 promotores e uma loja",
            "produto": "MobConnect",
        },
        historico=[],
        contexto_fluxo="Menu geral do atendimento Mob2Con.",
        contexto_conhecimento="",
    )
    duracao = time.perf_counter() - inicio
    await cliente.fechar()

    print(f"MODELO={config.llm.modelo}")
    print(f"SEGUNDOS={duracao:.2f}")
    if analise is None:
        print("ANALISE=NULA")
        return 2
    print(f"INTENCAO={analise.intencao}")
    print(f"ACAO={analise.acao}")
    print(f"CONFIANCA={analise.confianca:.2f}")
    print(f"RESPOSTA={analise.resposta[:500]}")
    print(f"CAMPOS={analise.campos}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(executar()))
