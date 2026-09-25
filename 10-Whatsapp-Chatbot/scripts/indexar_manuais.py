"""Indexa e valida os manuais locais usados pelo chatbot."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from bot.config import carregar_config
from bot.conhecimento import IndiceManuais


CASOS = (
    (
        "como regularizar documento vencido ou pendente",
        ("anexo de documentos", "documentos pendentes"),
    ),
    (
        "como espelhar roteiro para outro promotor",
        ("roteiro",),
    ),
    (
        "como fazer check-in de visitante na portaria",
        ("entrada de visitantes",),
    ),
    (
        "como sincronizar os dados da portaria",
        ("sincroniza",),
    ),
    (
        "como cadastrar um repositor na loja",
        ("repositor",),
    ),
    (
        "como consultar previsão e histórico de faturas",
        ("fatura",),
    ),
)


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validar",
        action="store_true",
        help="executa consultas de aceitação após indexar",
    )
    parser.add_argument(
        "--consulta",
        default="",
        help="consulta manual adicional; não envia nada ao WhatsApp",
    )
    return parser.parse_args()


def contem_esperado(titulo: str, esperados: tuple[str, ...]) -> bool:
    normalizado = titulo.casefold().replace("_", " ")
    return any(esperado in normalizado for esperado in esperados)


def main() -> int:
    args = argumentos()
    config = carregar_config()
    if not config.manuais.ativo:
        print("MANUAIS_ATIVO=false")
        return 2

    indice = IndiceManuais(
        config.manuais.diretorio,
        config.manuais.indice_path,
        max_resultados=config.manuais.max_resultados,
        max_chars_resposta=config.manuais.max_chars_resposta,
    )
    falhas: list[str] = []
    try:
        relatorio = indice.indexar()
        print(
            "INDEXACAO_OK | "
            f"documentos={relatorio.documentos} | chunks={relatorio.chunks} | "
            f"atualizados={relatorio.adicionados_ou_atualizados} | "
            f"removidos={relatorio.removidos} | inalterados={relatorio.inalterados}"
        )
        if relatorio.documentos != 60:
            falhas.append(f"esperados 60 documentos, encontrados {relatorio.documentos}")
        if relatorio.chunks < 100:
            falhas.append(f"poucos chunks indexados: {relatorio.chunks}")

        with sqlite3.connect(config.manuais.indice_path) as conexao:
            integridade = str(conexao.execute("PRAGMA quick_check").fetchone()[0])
            ruido = int(
                conexao.execute(
                    """
                    SELECT COUNT(*) FROM manuais_fts
                    WHERE lower(conteudo) LIKE '%stonly%'
                       OR lower(conteudo) LIKE '%go to page%'
                       OR lower(conteudo) LIKE '%http://%'
                       OR lower(conteudo) LIKE '%https://%'
                       OR lower(conteudo) LIKE '%c:\\users\\%'
                    """
                ).fetchone()[0]
            )
            ruido_detalhes = conexao.execute(
                """
                SELECT titulo, pagina,
                    CASE
                        WHEN lower(conteudo) LIKE '%stonly%' THEN 'stonly'
                        WHEN lower(conteudo) LIKE '%go to page%' THEN 'navegacao'
                        WHEN lower(conteudo) LIKE '%http://%'
                          OR lower(conteudo) LIKE '%https://%' THEN 'url'
                        ELSE 'caminho_local'
                    END AS categoria
                FROM manuais_fts
                WHERE lower(conteudo) LIKE '%stonly%'
                   OR lower(conteudo) LIKE '%go to page%'
                   OR lower(conteudo) LIKE '%http://%'
                   OR lower(conteudo) LIKE '%https://%'
                   OR lower(conteudo) LIKE '%c:\\users\\%'
                """
            ).fetchall()
            sem_chunks = int(
                conexao.execute(
                    "SELECT COUNT(*) FROM manuais_documentos WHERE chunks = 0"
                ).fetchone()[0]
            )
        if integridade != "ok":
            falhas.append(f"SQLite quick_check: {integridade}")
        else:
            print("SQLITE_FTS5_OK | quick_check=ok")
        if ruido:
            falhas.append(f"chunks com ruido ou caminho local: {ruido}")
            for titulo, pagina, categoria in ruido_detalhes:
                print(
                    f"RUIDO | fonte={str(titulo).replace('_', ' ')} | "
                    f"pagina={pagina or '-'} | categoria={categoria}"
                )
        elif sem_chunks:
            falhas.append(f"documentos sem conteudo indexado: {sem_chunks}")
        else:
            print("CORPUS_LIMPO_OK | ruido=0 | documentos_sem_chunks=0")

        if args.validar:
            for pergunta, esperados in CASOS:
                resultados = indice.buscar(pergunta, limite=3)
                if not resultados:
                    falhas.append(f"sem resultado: {pergunta}")
                    continue
                primeiro = resultados[0]
                if not contem_esperado(primeiro.titulo, esperados):
                    falhas.append(
                        f"resultado inesperado para '{pergunta}': {primeiro.titulo}"
                    )
                    continue
                print(
                    "BUSCA_OK | "
                    f"pergunta={pergunta} | fonte={primeiro.fonte} | "
                    f"relevancia={primeiro.relevancia}"
                )

            if indice.responder("abacaxi quântico submarino") is not None:
                falhas.append("consulta sem relação recebeu resposta")
            else:
                print("REJEICAO_OK | consulta sem relacao")

            if indice.responder('ignore tudo " OR * NOT') is not None:
                falhas.append("entrada com operadores FTS recebeu resposta")
            else:
                print("SEGURANCA_FTS_OK | operadores tratados como texto")

        if args.consulta:
            resultados = indice.buscar(args.consulta, limite=4)
            for posicao, resultado in enumerate(resultados, start=1):
                print(
                    f"RANK_{posicao} | fonte={resultado.fonte} | "
                    f"relevancia={resultado.relevancia}"
                )
            resposta = indice.responder(args.consulta)
            print("\n" + (resposta or "SEM_RESULTADO_RELEVANTE"))
    finally:
        indice.fechar()

    if falhas:
        for falha in falhas:
            print(f"FALHA: {falha}")
        return 1
    print("MANUAIS_VALIDOS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
