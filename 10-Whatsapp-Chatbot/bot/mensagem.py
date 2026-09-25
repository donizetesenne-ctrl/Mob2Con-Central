"""Leitura do payload de webhook da Evolution API.

O formato do evento `messages.upsert` aninha o conteúdo em vários lugares
diferentes conforme o tipo de mensagem. Este módulo normaliza tudo em uma
estrutura simples.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .evolution import eh_grupo, normalizar_numero

# envelopes que embrulham a mensagem real
ENVELOPES = (
    "ephemeralMessage",
    "viewOnceMessage",
    "viewOnceMessageV2",
    "viewOnceMessageV2Extension",
    "documentWithCaptionMessage",
    "editedMessage",
)

# campos de texto simples, em ordem de prioridade
CAMPOS_TEXTO = (
    ("conversation", None),
    ("extendedTextMessage", "text"),
    ("imageMessage", "caption"),
    ("videoMessage", "caption"),
    ("documentMessage", "caption"),
    ("buttonsResponseMessage", "selectedDisplayText"),
    ("templateButtonReplyMessage", "selectedId"),
)

# tipos que chegam sem texto utilizável
TIPOS_MIDIA = (
    "audioMessage",
    "imageMessage",
    "videoMessage",
    "documentMessage",
    "stickerMessage",
    "locationMessage",
    "contactMessage",
    "contactsArrayMessage",
    "ptvMessage",
)


@dataclass(frozen=True)
class MensagemRecebida:
    """Mensagem de entrada já normalizada."""

    id: str
    jid: str
    numero: str
    nome: str
    texto: str
    de_mim: bool
    grupo: bool
    tem_midia: bool
    instancia: str
    tipo: str = ""

    @property
    def valida(self) -> bool:
        return bool(self.numero) and bool(self.id)


def _desembrulhar(mensagem: dict[str, Any], profundidade: int = 0) -> dict[str, Any]:
    """Remove envelopes (efêmera, visualização única, etc.)."""
    if profundidade > 5 or not isinstance(mensagem, dict):
        return mensagem if isinstance(mensagem, dict) else {}
    for envelope in ENVELOPES:
        interno = mensagem.get(envelope)
        if isinstance(interno, dict):
            alvo = interno.get("message", interno)
            if isinstance(alvo, dict):
                return _desembrulhar(alvo, profundidade + 1)
    return mensagem


def extrair_texto(mensagem: dict[str, Any]) -> str:
    """Encontra o texto da mensagem, qualquer que seja o tipo."""
    conteudo = _desembrulhar(mensagem)
    if not conteudo:
        return ""

    for campo, subcampo in CAMPOS_TEXTO:
        valor = conteudo.get(campo)
        if subcampo is None:
            if isinstance(valor, str) and valor.strip():
                return valor.strip()
            continue
        if isinstance(valor, dict):
            texto = valor.get(subcampo)
            if isinstance(texto, str) and texto.strip():
                return texto.strip()

    # resposta de lista: prioriza o id da linha, que é estável
    lista = conteudo.get("listResponseMessage")
    if isinstance(lista, dict):
        reply = lista.get("singleSelectReply")
        if isinstance(reply, dict) and reply.get("selectedRowId"):
            return str(reply["selectedRowId"]).strip()
        if lista.get("title"):
            return str(lista["title"]).strip()

    # botões nativos / interativos mais novos
    interativo = conteudo.get("interactiveResponseMessage")
    if isinstance(interativo, dict):
        corpo = interativo.get("body")
        if isinstance(corpo, dict) and corpo.get("text"):
            return str(corpo["text"]).strip()

    botao = conteudo.get("buttonsResponseMessage")
    if isinstance(botao, dict) and botao.get("selectedButtonId"):
        return str(botao["selectedButtonId"]).strip()

    return ""


def tem_midia(mensagem: dict[str, Any]) -> bool:
    conteudo = _desembrulhar(mensagem)
    return any(isinstance(conteudo.get(tipo), dict) for tipo in TIPOS_MIDIA)


def _nome_utilizavel(bruto: Any) -> str:
    """Devolve o pushName só se der para usar numa saudação.

    Muita gente usa emoji, símbolo ou frase como nome de perfil no WhatsApp.
    Saudar com "Olá, 🎣!" parece defeito. Só aceitamos se houver letra.
    """
    nome = str(bruto or "").strip()
    if not nome or len(nome) > 60:
        return ""
    if not any(caractere.isalpha() for caractere in nome):
        return ""
    # remove emoji e símbolos, preservando letras, espaços, hífen e apóstrofo
    limpo = "".join(
        caractere
        for caractere in nome
        if caractere.isalpha() or caractere in " -'."
    ).strip()
    return limpo if any(c.isalpha() for c in limpo) else ""


def _jid_de_telefone(chave: dict[str, Any]) -> str:
    """Devolve o JID de telefone, traduzindo LID quando necessário.

    O WhatsApp migrou para LID (`@lid`), um identificador que esconde o número.
    Nesse caso o telefone real vem em `senderPn` (conversa individual) ou
    `participantPn` (grupo). Sem traduzir, nenhuma regra por número funciona:
    lista de permitidos, bloqueio e sessão passam a usar um id que muda de
    significado.

    O gateway já normaliza isso, mas a Evolution API pode repassar o LID cru —
    então a defesa fica aqui também.
    """
    remoto = str(chave.get("remoteJid") or "")
    if not remoto.endswith("@lid"):
        return remoto
    for campo in ("senderPn", "participantPn", "remoteJidAlt"):
        alternativo = chave.get(campo)
        if isinstance(alternativo, str) and alternativo.strip():
            return alternativo.strip()
    return remoto


def interpretar(payload: dict[str, Any]) -> MensagemRecebida | None:
    """Converte o corpo do webhook em MensagemRecebida.

    Devolve None quando o payload não é uma mensagem de texto de contato.
    """
    if not isinstance(payload, dict):
        return None

    dados = payload.get("data")
    # alguns eventos entregam uma lista de mensagens
    if isinstance(dados, list):
        dados = dados[0] if dados else None
    if not isinstance(dados, dict):
        return None

    chave = dados.get("key")
    if not isinstance(chave, dict):
        return None

    jid = _jid_de_telefone(chave)
    if not jid or jid.startswith("status@"):
        return None

    mensagem = dados.get("message")
    mensagem = mensagem if isinstance(mensagem, dict) else {}

    tipo = str(dados.get("messageType") or "")
    if not tipo and mensagem:
        candidatos = [c for c in mensagem if c != "messageContextInfo"]
        tipo = candidatos[0] if candidatos else ""

    return MensagemRecebida(
        id=str(chave.get("id") or ""),
        jid=jid,
        numero=normalizar_numero(jid),
        nome=_nome_utilizavel(dados.get("pushName")),
        texto=extrair_texto(mensagem),
        de_mim=bool(chave.get("fromMe")),
        grupo=eh_grupo(jid),
        tem_midia=tem_midia(mensagem),
        instancia=str(payload.get("instance") or ""),
        tipo=tipo,
    )
