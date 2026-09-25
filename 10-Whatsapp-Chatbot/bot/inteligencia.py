"""Políticas de confiança da camada inteligente do chatbot."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisaoConfianca:
    """Resultado operacional da confiança devolvida pela IA."""

    valor: float
    faixa: str
    executar: bool
    esclarecer: bool
    usar_fallback: bool
    motivo: str


_LIMIARES_EXECUCAO = {
    "responder": 0.78,
    "suporte_mobconnect": 0.76,
    "encaminhar_comercial": 0.84,
    "humano": 0.82,
    "continuar_fluxo": 1.01,
}
def avaliar_confianca(
    valor: float,
    *,
    acao: str,
    tem_evidencia: bool,
) -> DecisaoConfianca:
    """Decide se a IA pode agir, deve esclarecer ou ceder ao fallback."""
    confianca = max(0.0, min(1.0, float(valor)))
    limiar = _LIMIARES_EXECUCAO.get(acao, 0.84)

    # Resposta ancorada em manual pode operar com um pouco menos de confiança,
    # pois a geração está limitada por evidência local.
    if acao == "responder" and tem_evidencia:
        limiar = max(0.72, limiar - 0.06)

    if confianca >= limiar:
        return DecisaoConfianca(
            confianca, "alta", True, False, False, "acima do limiar operacional"
        )

    if confianca >= 0.60:
        return DecisaoConfianca(
            confianca,
            "media",
            False,
            True,
            False,
            "ambiguidade moderada: pedir no máximo uma confirmação",
        )
    return DecisaoConfianca(
        confianca,
        "baixa",
        False,
        False,
        True,
        "confiança insuficiente: usar fluxo/RAG determinístico",
    )


def pergunta_de_esclarecimento(intencao: str, acao: str) -> str:
    """Pergunta conservadora quando a intenção ficou provável, mas não segura."""
    chave = (intencao or "").strip().lower()
    if "suporte" in chave or acao == "suporte_mobconnect":
        return "Você já usa o MobConnect e está com um problema, ou está conhecendo a solução agora?"
    if "comercial" in chave or acao == "encaminhar_comercial":
        return "Você quer apenas entender como funciona ou já quer conversar com o comercial?"
    if "mobconnect" in chave:
        return "Você quer entender como o MobConnect funciona ou precisa de suporte em algo que já usa?"
    return "Você consegue me dizer em uma frase o que pretende resolver?"
