"""Classificação determinística de texto curto com tolerância a digitação.

Não tenta gerar resposta nem adivinhar assunto sem evidência. Compara somente
os gatilhos declarados no fluxo e exige vantagem clara sobre a segunda intenção.
"""

from __future__ import annotations

from collections.abc import Collection, Mapping
from difflib import SequenceMatcher


_MARGEM_AMBIGUIDADE = 0.055


def _limiar_token(token: str) -> float:
    if len(token) <= 4:
        return 0.87
    if len(token) <= 6:
        return 0.83
    return 0.79


def _frase_contida(texto: list[str], gatilho: list[str]) -> bool:
    tamanho = len(gatilho)
    if tamanho > len(texto):
        return False
    return any(
        texto[inicio : inicio + tamanho] == gatilho
        for inicio in range(len(texto) - tamanho + 1)
    )


def _melhor_janela(texto: list[str], gatilho: list[str]) -> float:
    """Similaridade da frase contra janelas próximas do mesmo tamanho."""
    if not texto or not gatilho:
        return 0.0
    if len(gatilho) == 1:
        alvo = gatilho[0]
        melhor = max(SequenceMatcher(None, alvo, token).ratio() for token in texto)
        return melhor if melhor >= _limiar_token(alvo) else 0.0

    melhor = 0.0
    minimo = max(1, len(gatilho) - 1)
    maximo = min(len(texto), len(gatilho) + 2)
    alvo = " ".join(gatilho)
    for tamanho in range(minimo, maximo + 1):
        for inicio in range(len(texto) - tamanho + 1):
            janela = " ".join(texto[inicio : inicio + tamanho])
            melhor = max(melhor, SequenceMatcher(None, alvo, janela).ratio())

    # Também tolera pequena mudança de ordem e palavras de ligação extras.
    notas_tokens = [
        max(SequenceMatcher(None, alvo_token, token).ratio() for token in texto)
        for alvo_token in gatilho
    ]
    casados = sum(
        nota >= _limiar_token(token)
        for token, nota in zip(gatilho, notas_tokens, strict=True)
    )
    cobertura_minima = max(1, (len(gatilho) * 2 + 2) // 3)
    if casados >= cobertura_minima:
        melhor = max(melhor, sum(notas_tokens) / len(notas_tokens))

    return melhor if melhor >= 0.80 else 0.0


def resolver_gatilhos(
    texto: str,
    gatilhos: Mapping[str, str],
    destinos_validos: Collection[str],
) -> str | None:
    """Retorna destino mais provável ou ``None`` quando houver ambiguidade.

    Gatilho específico recebe pequeno bônus. Assim, uma frase aproximada como
    ``quero contratar mobconect`` vence o gatilho genérico exato ``contratar``.
    """
    palavras_texto = texto.split()
    validos = set(destinos_validos)
    candidatos: dict[str, float] = {}

    for frase, destino in gatilhos.items():
        if destino not in validos:
            continue
        palavras_gatilho = frase.split()
        if not palavras_gatilho:
            continue

        if _frase_contida(palavras_texto, palavras_gatilho):
            similaridade = 1.0
        else:
            similaridade = _melhor_janela(palavras_texto, palavras_gatilho)
        if not similaridade:
            continue

        especificidade = min(0.16, max(0, len(palavras_gatilho) - 1) * 0.035)
        nota = similaridade + especificidade
        candidatos[destino] = max(candidatos.get(destino, 0.0), nota)

    if not candidatos:
        return None

    ordenados = sorted(candidatos.items(), key=lambda item: item[1], reverse=True)
    if len(ordenados) > 1 and ordenados[0][1] - ordenados[1][1] < _MARGEM_AMBIGUIDADE:
        return None
    return ordenados[0][0]
