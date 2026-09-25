"""Cliente HTTP da Evolution API.

Tolerante a variação de formato entre versões: quando a Evolution recusa o
payload novo com 400/404, o cliente tenta o formato antigo antes de falhar.
"""

from __future__ import annotations

import logging
import re
from typing import Any

import httpx

from .config import ConfigEvolution

logger = logging.getLogger(__name__)

SUFIXO_CONTATO = "@s.whatsapp.net"
SUFIXO_GRUPO = "@g.us"


class ErroEvolution(RuntimeError):
    """Falha em uma chamada à Evolution API."""

    def __init__(self, status: int, corpo: str, caminho: str) -> None:
        super().__init__(f"Evolution API {status} em {caminho}: {corpo[:400]}")
        self.status = status
        self.corpo = corpo
        self.caminho = caminho


def normalizar_numero(bruto: str) -> str:
    """Extrai só os dígitos de um JID ou telefone.

    '5511999998888@s.whatsapp.net' -> '5511999998888'
    '+55 (11) 99999-8888'          -> '5511999998888'
    """
    if not bruto:
        return ""
    sem_sufixo = bruto.split("@", 1)[0]
    sem_dispositivo = sem_sufixo.split(":", 1)[0]
    return re.sub(r"\D", "", sem_dispositivo)


def eh_grupo(jid: str) -> bool:
    return bool(jid) and jid.endswith(SUFIXO_GRUPO)


class ClienteEvolution:
    """Wrapper assíncrono das rotas da Evolution API que o bot usa."""

    def __init__(self, config: ConfigEvolution) -> None:
        self._config = config
        self._cliente: httpx.AsyncClient | None = None

    # ---------------------------------------------------------------- ciclo de vida

    async def abrir(self) -> None:
        if self._cliente is None or self._cliente.is_closed:
            self._cliente = httpx.AsyncClient(
                base_url=self._config.base_url,
                timeout=self._config.timeout,
            )

    async def fechar(self) -> None:
        if self._cliente is not None and not self._cliente.is_closed:
            await self._cliente.aclose()
        self._cliente = None

    async def __aenter__(self) -> ClienteEvolution:
        await self.abrir()
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.fechar()

    # ---------------------------------------------------------------- transporte

    def _headers(self, usar_token_instancia: bool) -> dict[str, str]:
        chave = self._config.api_key
        if usar_token_instancia and self._config.token_instancia:
            chave = self._config.token_instancia
        return {"apikey": chave, "Content-Type": "application/json"}

    async def _requisitar(
        self,
        metodo: str,
        caminho: str,
        *,
        payload: dict[str, Any] | None = None,
        usar_token_instancia: bool = True,
    ) -> dict[str, Any]:
        await self.abrir()
        assert self._cliente is not None
        resposta = await self._cliente.request(
            metodo,
            caminho,
            json=payload,
            headers=self._headers(usar_token_instancia),
        )
        if resposta.status_code >= 400:
            raise ErroEvolution(resposta.status_code, resposta.text, caminho)
        if not resposta.content:
            return {}
        try:
            corpo = resposta.json()
        except ValueError:
            return {"raw": resposta.text}
        return corpo if isinstance(corpo, dict) else {"data": corpo}

    async def _post_com_fallback(
        self,
        caminho: str,
        payload_novo: dict[str, Any],
        payload_legado: dict[str, Any],
        *,
        usar_token_instancia: bool = True,
    ) -> dict[str, Any]:
        """Tenta o payload atual; em 400/404 tenta o formato antigo."""
        try:
            return await self._requisitar(
                "POST",
                caminho,
                payload=payload_novo,
                usar_token_instancia=usar_token_instancia,
            )
        except ErroEvolution as erro:
            if erro.status not in (400, 404, 422):
                raise
            logger.warning(
                "Payload novo recusado em %s (%s). Tentando formato legado.",
                caminho,
                erro.status,
            )
            return await self._requisitar(
                "POST",
                caminho,
                payload=payload_legado,
                usar_token_instancia=usar_token_instancia,
            )

    # ---------------------------------------------------------------- instância

    async def criar_instancia(self) -> dict[str, Any]:
        payload = {
            "instanceName": self._config.instancia,
            "integration": "WHATSAPP-BAILEYS",
            "qrcode": True,
        }
        return await self._requisitar(
            "POST", "/instance/create", payload=payload, usar_token_instancia=False
        )

    async def conectar(self) -> dict[str, Any]:
        """Devolve QR Code em base64 e/ou código de pareamento."""
        return await self._requisitar(
            "GET",
            f"/instance/connect/{self._config.instancia}",
            usar_token_instancia=False,
        )

    async def estado_conexao(self) -> dict[str, Any]:
        return await self._requisitar(
            "GET",
            f"/instance/connectionState/{self._config.instancia}",
            usar_token_instancia=False,
        )

    async def listar_instancias(self) -> dict[str, Any]:
        return await self._requisitar(
            "GET", "/instance/fetchInstances", usar_token_instancia=False
        )

    async def definir_webhook(self, url: str, eventos: list[str]) -> dict[str, Any]:
        novo = {
            "webhook": {
                "enabled": True,
                "url": url,
                "webhookByEvents": False,
                "webhookBase64": False,
                "events": eventos,
            }
        }
        legado = {
            "enabled": True,
            "url": url,
            "webhook_by_events": False,
            "webhook_base64": False,
            "events": eventos,
        }
        return await self._post_com_fallback(
            f"/webhook/set/{self._config.instancia}",
            novo,
            legado,
            usar_token_instancia=False,
        )

    # ---------------------------------------------------------------- mensagens

    async def enviar_texto(
        self,
        numero: str,
        texto: str,
        *,
        delay_ms: int = 0,
        citar_id: str | None = None,
    ) -> dict[str, Any]:
        destino = normalizar_numero(numero)
        novo: dict[str, Any] = {"number": destino, "text": texto}
        if delay_ms > 0:
            novo["delay"] = delay_ms
        if citar_id:
            novo["quoted"] = {"key": {"id": citar_id}}

        legado: dict[str, Any] = {
            "number": destino,
            "textMessage": {"text": texto},
            "options": {"delay": delay_ms, "presence": "composing"},
        }
        return await self._post_com_fallback(
            f"/message/sendText/{self._config.instancia}", novo, legado
        )

    async def marcar_digitando(self, numero: str, duracao_ms: int) -> None:
        """Mostra 'digitando...' para o contato. Falha silenciosa: é cosmético."""
        if duracao_ms <= 0:
            return
        payload = {
            "number": normalizar_numero(numero),
            "delay": duracao_ms,
            "presence": "composing",
        }
        try:
            await self._requisitar(
                "POST",
                f"/chat/sendPresence/{self._config.instancia}",
                payload=payload,
            )
        except (ErroEvolution, httpx.HTTPError) as erro:
            logger.debug("Não foi possível enviar presença: %s", erro)
