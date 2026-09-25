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
            diagnostico = instancia.get("diagnostics") or estado.get("diagnostics") or {}
            if isinstance(diagnostico, dict) and diagnostico:
                _linha("quedas neste processo", str(diagnostico.get("quedas", 0)))
                _linha(
                    "tentativas reconexao",
                    str(diagnostico.get("tentativasReconexao", 0)),
                )
                if diagnostico.get("ultimaConexaoEm"):
                    _linha("ultima conexao", str(diagnostico["ultimaConexaoEm"]))
                if diagnostico.get("ultimaQuedaEm"):
                    _linha("ultima queda", str(diagnostico["ultimaQuedaEm"]))
                    _linha(
                        "motivo ultima queda",
                        str(diagnostico.get("ultimoMotivoQueda") or "desconhecido"),
                    )
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
            if corpo.get("ia_ativa"):
                _linha("IA conversacional", "ATIVA - interpretação semântica ligada")
            elif config.llm.ativo:
                _linha("IA conversacional", "PRONTA - aguardando chave ou modelo local")
            else:
                _linha("IA conversacional", "desligada por configuração")
            inteligencia = corpo.get("inteligencia") or {}
            if isinstance(inteligencia, dict):
                _linha("memoria estruturada", "ativa" if inteligencia.get("memoria_estruturada") else "nao")
                _linha("RAG hibrido", "ativo" if inteligencia.get("rag_hibrido") else "nao")
                _linha("motor de confianca", "ativo" if inteligencia.get("motor_confianca") else "nao")
                if inteligencia.get("modelo"):
                    _linha("modelo configurado", str(inteligencia["modelo"]))
            qualidade = corpo.get("qualidade_24h") or {}
            if isinstance(qualidade, dict) and qualidade:
                _linha("interacoes 24h", str(qualidade.get("total", 0)))
                _linha("handoffs 24h", str(qualidade.get("handoffs", 0)))
                _linha(
                    "latencia media 24h",
                    f"{qualidade.get('latencia_media_ms', 0)} ms",
                )
                fontes = qualidade.get("fontes") or {}
                if isinstance(fontes, dict) and fontes:
                    _linha(
                        "fontes 24h",
                        ", ".join(f"{k}={v}" for k, v in fontes.items()),
                    )
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
        _linha("MODO TESTE", "ABERTO - responde qualquer numero")
        _linha("coleta de casos reais", "ativa - todos podem testar o fluxo")

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
