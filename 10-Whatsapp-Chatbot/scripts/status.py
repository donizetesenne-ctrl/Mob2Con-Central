"""Diagnóstico completo: WhatsApp, bot e configuração de atendimento.

Uso:
    python scripts/status.py
"""

from __future__ import annotations

import asyncio
import os

import httpx

from _comum import carregar


def _linha(rotulo: str, valor: str) -> None:
    print(f"  {rotulo.ljust(26)}: {valor}")


async def executar() -> int:
    config, cliente = carregar()
    alertas: list[str] = []

    print("=" * 66)
    print(" WHATSAPP")
    print("=" * 66)
    _linha("instancia", config.evolution.instancia)
    _linha("motor", config.evolution.base_url)

    conectado = False
    async with cliente:
        try:
            estado = await cliente.estado_conexao()
            instancia = estado.get("instance") or {}
            situacao = str(instancia.get("state") or estado.get("state") or "?")
            conectado = situacao.lower() == "open"
            _linha(
                "conexao",
                {
                    "open": "conectado",
                    "connecting": "conectando - pareie o QR Code",
                    "close": "desconectado",
                }.get(situacao.lower(), situacao),
            )
            numero = instancia.get("number")
            if numero:
                _linha("numero pareado", f"+{numero}")
            else:
                _linha("numero pareado", "nao informado pelo motor")
            if instancia.get("profileName"):
                _linha("perfil", str(instancia["profileName"]))
            if not conectado:
                alertas.append("WhatsApp nao esta conectado: o bot nao vai responder.")
        except Exception as erro:  # noqa: BLE001
            _linha("conexao", f"erro ao consultar ({erro})")
            alertas.append(
                "Nao consegui falar com o motor do WhatsApp. Ele esta rodando?"
            )

    print()
    print("=" * 66)
    print(" BOT")
    print("=" * 66)
    url_bot = f"http://localhost:{config.porta}/health"
    bot_online = False
    try:
        async with httpx.AsyncClient(timeout=8) as http:
            resposta = await http.get(url_bot)
        if resposta.status_code == 200:
            corpo = resposta.json()
            bot_online = True
            _linha("servico", f"online ({corpo.get('status')})")
            _linha("motor alcancavel", str(corpo.get("evolution_alcancavel")))
            _linha("dentro do horario", str(corpo.get("dentro_do_horario")))
            _linha("IA de fallback", "ligada" if corpo.get("ia_ativa") else "desligada")
            if corpo.get("status") == "degradado":
                alertas.append("Bot vivo, mas sem alcancar o motor do WhatsApp.")
        else:
            _linha("servico", f"respondeu HTTP {resposta.status_code}")
            alertas.append(f"Bot respondeu {resposta.status_code} em /health.")
    except httpx.HTTPError:
        _linha("servico", f"offline (nada em {url_bot})")
        alertas.append("Bot nao esta rodando: ninguem vai processar as mensagens.")

    print()
    print("=" * 66)
    print(" ATENDIMENTO")
    print("=" * 66)
    atendimento = config.atendimento
    _linha("empresa", atendimento.nome_empresa)
    abertura = "%02d:%02d" % atendimento.hora_abertura
    fechamento = "%02d:%02d" % atendimento.hora_fechamento
    _linha("horario", f"{abertura} as {fechamento}")
    _linha("responde grupos", "sim" if atendimento.responder_grupos else "nao")
    _linha("pausa apos transferir", f"{atendimento.minutos_pausa_humano} min")

    if atendimento.numeros_permitidos:
        _linha(
            "MODO TESTE",
            "ativo - so responde " + ", ".join(sorted(atendimento.numeros_permitidos)),
        )
    else:
        _linha("MODO TESTE", "DESLIGADO - responde qualquer numero")
        if conectado and bot_online:
            alertas.append(
                "O bot esta ATENDENDO TODO MUNDO que mandar mensagem para este numero. "
                "Para testar com seguranca, preencha NUMEROS_PERMITIDOS no .env."
            )

    notificacao = os.environ.get("NUMERO_NOTIFICACAO", "").strip()
    _linha("aviso interno de lead", f"+{notificacao}" if notificacao else "nao configurado")
    if not notificacao:
        alertas.append(
            "NUMERO_NOTIFICACAO vazio: voce nao sera avisado quando alguem pedir atendente."
        )

    print()
    if alertas:
        print("=" * 66)
        print(f" ATENCAO ({len(alertas)})")
        print("=" * 66)
        for indice, alerta in enumerate(alertas, start=1):
            print(f"  {indice}. {alerta}")
    else:
        print("Tudo pronto. Mande 'oi' de outro numero para testar.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(executar()))
