"""Utilidades compartilhadas pelos scripts de operação."""

from __future__ import annotations

import sys
from pathlib import Path

PROJETO_DIR = Path(__file__).resolve().parent.parent

# permite rodar os scripts direto, sem instalar o pacote
if str(PROJETO_DIR) not in sys.path:
    sys.path.insert(0, str(PROJETO_DIR))


def exigir_env() -> None:
    """Aborta com mensagem clara se o .env ainda não existe."""
    if not (PROJETO_DIR / ".env").exists():
        print("[X] Arquivo .env não encontrado.")
        print("    Rode primeiro: python scripts/gerar_env.py")
        raise SystemExit(1)


def carregar() -> tuple[object, object]:
    """Devolve (config, ClienteEvolution) prontos para uso."""
    exigir_env()
    from bot.config import carregar_config
    from bot.evolution import ClienteEvolution

    config = carregar_config()
    if not config.evolution.api_key:
        print("[X] EVOLUTION_API_KEY está vazio no .env.")
        raise SystemExit(1)
    return config, ClienteEvolution(config.evolution)
