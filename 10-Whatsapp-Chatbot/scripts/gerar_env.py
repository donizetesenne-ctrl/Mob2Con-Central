"""Cria o .env a partir do .env.example, com segredos aleatórios.

Nunca reaproveita a chave de exemplo pública da Evolution API — é justamente
o erro que expõe instâncias na internet.

Uso:
    python scripts/gerar_env.py
    python scripts/gerar_env.py --forcar     # sobrescreve o .env existente
"""

from __future__ import annotations

import argparse
import re
import secrets
import shutil
from datetime import datetime

from _comum import PROJETO_DIR

CHAVE_PUBLICA_EXEMPLO = "429683C4C977415CAAFCCE10F7D57E11"

SEGREDOS = {
    "EVOLUTION_API_KEY": lambda: secrets.token_hex(24),
    "WEBHOOK_TOKEN": lambda: secrets.token_urlsafe(24),
    "POSTGRES_PASSWORD": lambda: secrets.token_urlsafe(20).replace("-", "x"),
}


def _substituir(conteudo: str, chave: str, valor: str) -> str:
    padrao = re.compile(rf"^{re.escape(chave)}=.*$", re.MULTILINE)
    if padrao.search(conteudo):
        return padrao.sub(f"{chave}={valor}", conteudo)
    return conteudo.rstrip("\n") + f"\n{chave}={valor}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--forcar",
        action="store_true",
        help="sobrescreve o .env existente (faz backup antes)",
    )
    argumentos = parser.parse_args()

    exemplo = PROJETO_DIR / ".env.example"
    destino = PROJETO_DIR / ".env"

    if not exemplo.exists():
        print(f"[X] Não encontrei {exemplo}")
        return 1

    if destino.exists():
        if not argumentos.forcar:
            print(f"[!] {destino} já existe. Nada foi alterado.")
            print("    Use --forcar para regerar (um backup será criado).")
            return 0
        marca = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = destino.with_suffix(f".bak-{marca}")
        shutil.copy2(destino, backup)
        print(f"[i] Backup salvo em {backup.name}")

    conteudo = exemplo.read_text(encoding="utf-8")
    gerados: dict[str, str] = {}
    for chave, gerador in SEGREDOS.items():
        valor = gerador()
        gerados[chave] = valor
        conteudo = _substituir(conteudo, chave, valor)

    if CHAVE_PUBLICA_EXEMPLO in conteudo:
        print("[X] A chave pública de exemplo ainda está no arquivo. Abortando.")
        return 1

    destino.write_text(conteudo, encoding="utf-8")

    print(f"[OK] .env criado em {destino}")
    print()
    print("Segredos gerados (guarde a chave da API, você vai precisar dela):")
    for chave, valor in gerados.items():
        visivel = valor if chave == "EVOLUTION_API_KEY" else valor[:6] + "..."
        print(f"  {chave} = {visivel}")
    print()
    print("Próximo passo: docker compose up -d")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
