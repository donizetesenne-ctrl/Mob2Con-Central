"""Estado de conversa por contato.

Guarda em memória por padrão. Se REDIS_URL estiver definido e a lib `redis`
estiver instalada, persiste no Redis — necessário quando você roda mais de uma
réplica do bot ou quer sobreviver a restart.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

logger = logging.getLogger(__name__)

ESTADO_INICIAL = "menu"
MEMORIA_META_CHAVE = "_memoria_meta"


@dataclass
class Sessao:
    """Conversa de um contato."""

    numero: str
    estado: str = ESTADO_INICIAL
    nome: str = ""
    tentativas_invalidas: int = 0
    pausado_ate: float = 0.0
    atualizado_em: float = field(default_factory=time.time)
    dados: dict[str, Any] = field(default_factory=dict)
    historico: list[dict[str, str]] = field(default_factory=list)

    @property
    def pausada(self) -> bool:
        """True enquanto um humano estiver com o atendimento."""
        return self.pausado_ate > time.time()

    def pausar(self, minutos: int) -> None:
        self.pausado_ate = time.time() + minutos * 60

    def retomar(self) -> None:
        self.pausado_ate = 0.0

    def lembrar(
        self,
        campo: str,
        valor: Any,
        *,
        origem: str,
        confianca: float = 1.0,
        sobrescrever: bool = False,
    ) -> bool:
        """Guarda memória estruturada sem degradar um dado mais confiável."""
        chave = str(campo or "").strip()
        texto = str(valor or "").strip()
        if not chave or not texto:
            return False

        confianca_limpa = max(0.0, min(1.0, float(confianca)))
        meta = self.dados.get(MEMORIA_META_CHAVE)
        if not isinstance(meta, dict):
            meta = {}
            self.dados[MEMORIA_META_CHAVE] = meta

        atual = str(self.dados.get(chave) or "").strip()
        meta_atual = meta.get(chave)
        confianca_atual = 0.0
        if isinstance(meta_atual, dict):
            try:
                confianca_atual = float(meta_atual.get("confianca", 0.0))
            except (TypeError, ValueError):
                confianca_atual = 0.0

        if atual and atual != texto and not sobrescrever:
            if confianca_atual >= confianca_limpa:
                return False

        self.dados[chave] = texto[:600]
        meta[chave] = {
            "origem": str(origem or "desconhecida")[:80],
            "confianca": round(confianca_limpa, 3),
            "atualizado_em": time.time(),
        }
        return True

    def memoria_estruturada(self) -> dict[str, Any]:
        """Snapshot de dados úteis para IA/RAG, excluindo chaves internas."""
        return {
            chave: valor
            for chave, valor in self.dados.items()
            if not str(chave).startswith("_") and str(valor).strip()
        }

    def confianca_campo(self, campo: str) -> float:
        meta = self.dados.get(MEMORIA_META_CHAVE)
        if not isinstance(meta, dict):
            return 0.0
        item = meta.get(campo)
        if not isinstance(item, dict):
            return 0.0
        try:
            return max(0.0, min(1.0, float(item.get("confianca", 0.0))))
        except (TypeError, ValueError):
            return 0.0

    def reiniciar(self) -> None:
        self.estado = ESTADO_INICIAL
        self.tentativas_invalidas = 0
        self.dados.clear()
        self.historico.clear()

    def registrar_turno(self, papel: str, conteudo: str, maximo: int) -> None:
        """Mantém uma janela curta de histórico para o fallback de IA."""
        self.historico.append({"role": papel, "content": conteudo})
        if maximo > 0 and len(self.historico) > maximo:
            del self.historico[: len(self.historico) - maximo]

    def para_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def de_json(cls, bruto: str) -> Sessao:
        dados = json.loads(bruto)
        campos = {chave: dados[chave] for chave in dados if chave in cls.__annotations__}
        return cls(**campos)


class RepositorioSessao(Protocol):
    """Contrato mínimo de um armazenamento de sessão."""

    async def obter(self, numero: str) -> Sessao | None: ...

    async def salvar(self, sessao: Sessao) -> None: ...

    async def remover(self, numero: str) -> None: ...

    async def fechar(self) -> None: ...


class RepositorioMemoria:
    """Armazenamento em processo, com expiração por inatividade."""

    def __init__(self, ttl_segundos: int) -> None:
        self._ttl = max(60, ttl_segundos)
        self._itens: dict[str, Sessao] = {}
        self._trava = asyncio.Lock()

    async def obter(self, numero: str) -> Sessao | None:
        async with self._trava:
            self._limpar_expiradas()
            return self._itens.get(numero)

    async def salvar(self, sessao: Sessao) -> None:
        sessao.atualizado_em = time.time()
        async with self._trava:
            self._itens[sessao.numero] = sessao

    async def remover(self, numero: str) -> None:
        async with self._trava:
            self._itens.pop(numero, None)

    async def fechar(self) -> None:
        async with self._trava:
            self._itens.clear()

    def _limpar_expiradas(self) -> None:
        limite = time.time() - self._ttl
        expiradas = [
            numero
            for numero, sessao in self._itens.items()
            # sessão pausada por humano não expira antes da pausa terminar
            if sessao.atualizado_em < limite and not sessao.pausada
        ]
        for numero in expiradas:
            del self._itens[numero]


class RepositorioRedis:
    """Armazenamento no Redis, com TTL nativo por chave."""

    PREFIXO = "chatbot:sessao:"

    def __init__(self, url: str, ttl_segundos: int) -> None:
        import redis.asyncio as redis  # import tardio: dependência opcional

        self._redis = redis.from_url(url, decode_responses=True)
        self._ttl = max(60, ttl_segundos)

    def _chave(self, numero: str) -> str:
        return f"{self.PREFIXO}{numero}"

    async def obter(self, numero: str) -> Sessao | None:
        bruto = await self._redis.get(self._chave(numero))
        if not bruto:
            return None
        try:
            return Sessao.de_json(bruto)
        except (ValueError, TypeError) as erro:
            logger.warning("Sessão inválida no Redis para %s: %s", numero, erro)
            return None

    async def salvar(self, sessao: Sessao) -> None:
        sessao.atualizado_em = time.time()
        # se estiver em atendimento humano, o TTL acompanha a pausa
        ttl = self._ttl
        restante = int(sessao.pausado_ate - time.time())
        if restante > ttl:
            ttl = restante
        await self._redis.set(self._chave(sessao.numero), sessao.para_json(), ex=ttl)

    async def remover(self, numero: str) -> None:
        await self._redis.delete(self._chave(numero))

    async def fechar(self) -> None:
        await self._redis.aclose()


def criar_repositorio(
    redis_url: str,
    ttl_segundos: int,
    fallback_persistente: RepositorioSessao | None = None,
) -> RepositorioSessao:
    """Escolhe Redis, depois o fallback persistente e por último memória."""
    if redis_url:
        try:
            repositorio = RepositorioRedis(redis_url, ttl_segundos)
            logger.info("Sessões no Redis (%s)", redis_url)
            return repositorio
        except ImportError:
            logger.warning(
                "REDIS_URL definido mas a lib 'redis' não está instalada. "
                "Usando o fallback local. Instale com: pip install redis"
            )
        except Exception as erro:  # noqa: BLE001 - queremos degradar, não quebrar
            logger.warning("Falha ao conectar no Redis (%s). Usando fallback local.", erro)

    if fallback_persistente is not None:
        logger.info(
            "Sessões no fallback persistente %s (TTL de %ss)",
            type(fallback_persistente).__name__,
            ttl_segundos,
        )
        return fallback_persistente

    logger.warning("Sessões em memória (TTL de %ss)", ttl_segundos)
    return RepositorioMemoria(ttl_segundos)
