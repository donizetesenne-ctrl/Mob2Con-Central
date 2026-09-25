"""Fallback de IA para texto livre (opcional).

Fala com qualquer endpoint compatível com a API de chat completions da OpenAI:
OpenAI, NVIDIA NIM, Groq, OpenRouter, Ollama, vLLM etc. Basta apontar
LLM_BASE_URL para o provedor.

Se a IA estiver desligada ou falhar, o bot volta para o menu — nunca fica mudo.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any

import httpx

from .config import ConfigLLM

logger = logging.getLogger(__name__)

ACOES_IA = {
    "responder",
    "encaminhar_comercial",
    "suporte_mobconnect",
    "humano",
    "continuar_fluxo",
}
CAMPOS_IA = {
    "nome_contato",
    "empresa_contato",
    "segmento",
    "redes_atendidas",
    "porte",
    "necessidade",
    "contexto_comercial",
}


@dataclass(frozen=True)
class AnaliseConversa:
    """Plano estruturado devolvido pela IA antes do fluxo determinístico."""

    intencao: str = "outro"
    confianca: float = 0.0
    acao: str = "continuar_fluxo"
    resposta: str = ""
    pergunta_faltante: str = ""
    campos: dict[str, str] = field(default_factory=dict)


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

    @staticmethod
    def _analise_do_json(conteudo: str) -> AnaliseConversa | None:
        """Converte JSON tolerando cercas markdown e campos extras."""
        bruto = (conteudo or "").strip()
        bruto = re.sub(r"^\`\`\`(?:json)?\s*", "", bruto, flags=re.IGNORECASE)
        bruto = re.sub(r"\s*\`\`\`$", "", bruto)
        inicio, fim = bruto.find("{"), bruto.rfind("}")
        if inicio < 0 or fim <= inicio:
            return None
        try:
            dados: Any = json.loads(bruto[inicio : fim + 1])
        except (json.JSONDecodeError, TypeError):
            return None
        if not isinstance(dados, dict):
            return None

        acao = str(dados.get("acao") or "continuar_fluxo").strip().lower()
        if acao not in ACOES_IA:
            acao = "continuar_fluxo"
        try:
            confianca = max(0.0, min(1.0, float(dados.get("confianca", 0.0))))
        except (TypeError, ValueError):
            confianca = 0.0

        campos_brutos = dados.get("campos")
        campos: dict[str, str] = {}
        if isinstance(campos_brutos, dict):
            for chave, valor in campos_brutos.items():
                if chave in CAMPOS_IA and valor is not None:
                    texto = str(valor).strip()
                    if texto:
                        campos[chave] = texto[:600]

        return AnaliseConversa(
            intencao=str(dados.get("intencao") or "outro")[:80],
            confianca=confianca,
            acao=acao,
            resposta=str(dados.get("resposta") or "").strip()[:1800],
            pergunta_faltante=str(dados.get("pergunta_faltante") or "").strip()[:500],
            campos=campos,
        )

    async def _chat(
        self,
        mensagens: list[dict[str, str]],
        *,
        temperatura: float | None = None,
        max_tokens: int | None = None,
    ) -> str | None:
        if not self.ativo:
            return None
        await self.abrir()
        assert self._cliente is not None

        cabecalhos = {"Content-Type": "application/json"}
        if self._config.api_key:
            cabecalhos["Authorization"] = f"Bearer {self._config.api_key}"
        corpo = {
            "model": self._config.modelo,
            "messages": mensagens,
            "max_tokens": max_tokens or self._config.max_tokens,
            "temperature": (
                self._config.temperatura if temperatura is None else temperatura
            ),
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
            conteudo = dados["choices"][0]["message"]["content"]
        except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError) as erro:
            logger.warning("Falha ao consultar/interpretar a LLM: %s", erro)
            return None
        texto = str(conteudo or "").strip()
        return texto or None

    async def analisar(
        self,
        pergunta: str,
        *,
        estado: str,
        dados_sessao: dict[str, Any] | None = None,
        historico: list[dict[str, str]] | None = None,
        contexto_conhecimento: str = "",
    ) -> AnaliseConversa | None:
        """Entende intenção, extrai contexto e propõe a próxima ação."""
        if not self.ativo:
            return None

        conhecido = json.dumps(
            dados_sessao or {}, ensure_ascii=False, separators=(",", ":")
        )[:2400]
        instrucao = f"""
{self._config.prompt_sistema}

Você também atua como cérebro de roteamento conversacional.
Analise a última mensagem considerando o estado atual e o que já sabemos.

REGRAS:
- Responda primeiro quando a pessoa quer entender um produto. Não transforme
  curiosidade em formulário comercial.
- Nunca pergunte de novo algo já presente em DADOS_CONHECIDOS ou na mensagem.
- Extraia informações espontâneas úteis sem inventar.
- No máximo uma pergunta de esclarecimento.
- Para MobConnect, explique execução em campo: planejamento, roteiro, atividades,
  pesquisas, registro da visita e leitura dos resultados. Diferencie MobControl,
  que trata cadastro, documentos e acesso.
- Não invente preço, prazo, cliente, cobertura contratada, estoque ou ruptura.
- Se houver contexto dos manuais, use-o como evidência e não contradiga-o.
- Só use encaminhar_comercial quando a pessoa explicitamente pedir proposta,
  contratação, demonstração ou contato comercial.
- Só use humano quando a pessoa pedir atendimento humano.
- Se for suporte de quem já usa MobConnect, use suporte_mobconnect.
- Quando não houver ganho claro em usar IA, use continuar_fluxo.

Retorne SOMENTE JSON válido:
{{
  "intencao": "mobconnect_conhecer|mobconnect_comercial|mobconnect_suporte|mobcontrol|outro",
  "confianca": 0.0,
  "acao": "responder|encaminhar_comercial|suporte_mobconnect|humano|continuar_fluxo",
  "resposta": "texto curto para WhatsApp ou vazio",
  "pergunta_faltante": "uma pergunta opcional ou vazio",
  "campos": {{
    "nome_contato": "",
    "empresa_contato": "",
    "segmento": "",
    "redes_atendidas": "",
    "porte": "",
    "necessidade": "",
    "contexto_comercial": ""
  }}
}}

ESTADO_ATUAL: {estado}
DADOS_CONHECIDOS: {conhecido}
CONTEXTO_DOS_MANUAIS:
{contexto_conhecimento[:5000]}
"""
        mensagens: list[dict[str, str]] = [{"role": "system", "content": instrucao}]
        if historico:
            mensagens.extend(historico[-self._config.max_historico :])
        mensagens.append({"role": "user", "content": pergunta})
        conteudo = await self._chat(
            mensagens,
            temperatura=0.1,
            max_tokens=max(500, self._config.max_tokens),
        )
        if not conteudo:
            return None
        analise = self._analise_do_json(conteudo)
        if analise is None:
            logger.warning("LLM não devolveu JSON de análise válido.")
        return analise

    async def responder(
        self,
        pergunta: str,
        historico: list[dict[str, str]] | None = None,
    ) -> str | None:
        """Devolve resposta livre da IA quando o fluxo e o RAG não resolveram."""
        mensagens: list[dict[str, str]] = [
            {"role": "system", "content": self._config.prompt_sistema}
        ]
        if historico:
            mensagens.extend(historico[-self._config.max_historico :])
        mensagens.append({"role": "user", "content": pergunta})
        return await self._chat(mensagens)
