"""Fallback de IA para texto livre (opcional).

Fala com qualquer endpoint compatível com a API de chat completions da OpenAI:
OpenAI, NVIDIA NIM, Groq, OpenRouter, Ollama, vLLM etc. Basta apontar
LLM_BASE_URL para o provedor.

Se a IA estiver desligada ou falhar, o bot volta para o menu — nunca fica mudo.
"""

from __future__ import annotations

import logging

import httpx

from .config import ConfigLLM

logger = logging.getLogger(__name__)


class ClienteLLM:
    """Cliente mínimo de chat completions."""

    def __init__(self, config: ConfigLLM) -> None:
        self._config = config
        self._cliente: httpx.AsyncClient | None = None

    @property
    def ativo(self) -> bool:
        return self._config.ativo and bool(self._config.api_key or self._eh_local())

    def _eh_local(self) -> bool:
        """Endpoints locais (Ollama, vLLM) normalmente não pedem chave."""
        return any(
            marca in self._config.base_url for marca in ("localhost", "127.0.0.1", "host.docker.internal")
        )

    async def abrir(self) -> None:
        if self._cliente is None or self._cliente.is_closed:
            self._cliente = httpx.AsyncClient(timeout=self._config.timeout)

    async def fechar(self) -> None:
        if self._cliente is not None and not self._cliente.is_closed:
            await self._cliente.aclose()
        self._cliente = None

    async def responder(
        self,
        pergunta: str,
        historico: list[dict[str, str]] | None = None,
    ) -> str | None:
        """Devolve a resposta da IA, ou None se não foi possível gerar."""
        if not self.ativo:
            return None

        await self.abrir()
        assert self._cliente is not None

        mensagens: list[dict[str, str]] = [
            {"role": "system", "content": self._config.prompt_sistema}
        ]
        if historico:
            mensagens.extend(historico[-self._config.max_historico :])
        mensagens.append({"role": "user", "content": pergunta})

        cabecalhos = {"Content-Type": "application/json"}
        if self._config.api_key:
            cabecalhos["Authorization"] = f"Bearer {self._config.api_key}"

        corpo = {
            "model": self._config.modelo,
            "messages": mensagens,
            "max_tokens": self._config.max_tokens,
            "temperature": self._config.temperatura,
            "stream": False,
        }

        try:
            resposta = await self._cliente.post(
                f"{self._config.base_url}/chat/completions",
                json=corpo,
                headers=cabecalhos,
            )
            if resposta.status_code >= 400:
                logger.warning(
                    "LLM devolveu %s: %s", resposta.status_code, resposta.text[:300]
                )
                return None
            dados = resposta.json()
        except (httpx.HTTPError, ValueError) as erro:
            logger.warning("Falha ao consultar a LLM: %s", erro)
            return None

        try:
            conteudo = dados["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            logger.warning("Resposta da LLM em formato inesperado: %s", str(dados)[:300])
            return None

        texto = (conteudo or "").strip()
        return texto or None
