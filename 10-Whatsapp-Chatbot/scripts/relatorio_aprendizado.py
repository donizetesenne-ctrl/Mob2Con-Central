"""Lista e classifica perguntas não respondidas gravadas pelo chatbot.

Uso:
    python scripts/relatorio_aprendizado.py
    python scripts/relatorio_aprendizado.py --limite 50 --json
    python scripts/relatorio_aprendizado.py --resolver 12
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from bot.config import carregar_config  # noqa: E402


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limite", type=int, default=20)
    parser.add_argument("--json", action="store_true", dest="como_json")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--resolver", type=int, metavar="ID")
    grupo.add_argument("--ignorar", type=int, metavar="ID")
    return parser.parse_args()


def horario(valor: float) -> str:
    return datetime.fromtimestamp(valor).astimezone().strftime("%d/%m/%Y %H:%M")


def main() -> int:
    args = argumentos()
    caminho = carregar_config().sqlite_path
    if str(caminho) == ":memory:" or not caminho.exists():
        print(f"Banco ainda não existe: {caminho}")
        return 0

    conexao = sqlite3.connect(caminho, timeout=5.0)
    conexao.row_factory = sqlite3.Row
    try:
        if args.resolver is not None or args.ignorar is not None:
            identificador = args.resolver if args.resolver is not None else args.ignorar
            status = "resolvida" if args.resolver is not None else "ignorada"
            cursor = conexao.execute(
                "UPDATE perguntas_nao_respondidas SET status = ? WHERE id = ?",
                (status, identificador),
            )
            conexao.commit()
            if cursor.rowcount != 1:
                print(f"Pergunta #{identificador} não encontrada.")
                return 1
            print(f"Pergunta #{identificador} marcada como {status}.")
            return 0

        limite = max(1, min(500, args.limite))
        linhas = conexao.execute(
            """
            SELECT id, pergunta, estado, frente, motivo, ocorrencias,
                   primeira_em, ultima_em
            FROM perguntas_nao_respondidas
            WHERE status = 'pendente'
            ORDER BY ocorrencias DESC, ultima_em DESC
            LIMIT ?
            """,
            (limite,),
        ).fetchall()
    except sqlite3.OperationalError as erro:
        print(f"Banco sem estrutura de aprendizado: {erro}")
        return 1
    finally:
        conexao.close()

    dados = [dict(linha) for linha in linhas]
    if args.como_json:
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        return 0

    if not dados:
        print("Nenhuma pergunta pendente.")
        return 0

    print(f"Perguntas pendentes: {len(dados)}\n")
    for item in dados:
        print(
            f"#{item['id']} · {item['ocorrencias']} ocorrência(s) · "
            f"última {horario(item['ultima_em'])}"
        )
        print(f"  Estado: {item['estado']} · Frente: {item['frente'] or 'geral'}")
        print(f"  Motivo: {item['motivo']}")
        print(f"  {item['pergunta']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
