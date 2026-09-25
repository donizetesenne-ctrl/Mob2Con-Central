"""Persistência SQLite local para sessões e aprendizado operacional.

Usa apenas a biblioteca padrão. Sessões sobrevivem a reinícios dentro do TTL
configurado. Mensagens que o bot não resolveu são agregadas para revisão, sem
armazenar número ou nome do contato e com redação de dados pessoais comuns.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import re
import sqlite3
import time
from pathlib import Path
from typing import Any

from .sessao import Sessao

logger = logging.getLogger(__name__)

_EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_CPF = re.compile(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)")
_TELEFONE = re.compile(
    r"(?<!\d)(?:\+?55[\s.-]?)?(?:\(?\d{2}\)?[\s.-]?)?"
    r"(?:9[\s.-]?)?\d{4}[\s.-]?\d{4}(?!\d)"
)


class BancoSQLite:
    """Banco local único para sessões e perguntas não respondidas."""

    def __init__(self, caminho: Path, ttl_segundos: int) -> None:
        self.caminho = caminho
        self._ttl = max(60, ttl_segundos)
        self._trava = asyncio.Lock()
        self._fechado = False

        alvo = str(caminho)
        if alvo != ":memory:":
            caminho.parent.mkdir(parents=True, exist_ok=True)

        self._conexao = sqlite3.connect(
            alvo,
            timeout=5.0,
            isolation_level=None,
            check_same_thread=False,
        )
        self._conexao.row_factory = sqlite3.Row
        self._preparar()

    def _preparar(self) -> None:
        cursor = self._conexao.cursor()
        cursor.execute("PRAGMA busy_timeout = 5000")
        cursor.execute("PRAGMA foreign_keys = ON")
        if str(self.caminho) != ":memory:":
            cursor.execute("PRAGMA journal_mode = WAL")
            cursor.execute("PRAGMA synchronous = NORMAL")
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessoes (
                numero TEXT PRIMARY KEY,
                conteudo_json TEXT NOT NULL,
                atualizado_em REAL NOT NULL,
                expira_em REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_sessoes_expira_em
                ON sessoes(expira_em);

            CREATE TABLE IF NOT EXISTS perguntas_nao_respondidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chave TEXT NOT NULL UNIQUE,
                pergunta TEXT NOT NULL,
                estado TEXT NOT NULL,
                frente TEXT NOT NULL DEFAULT '',
                motivo TEXT NOT NULL,
                ocorrencias INTEGER NOT NULL DEFAULT 1,
                primeira_em REAL NOT NULL,
                ultima_em REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pendente'
                    CHECK (status IN ('pendente', 'resolvida', 'ignorada'))
            );

            CREATE INDEX IF NOT EXISTS idx_perguntas_status_ultima
                ON perguntas_nao_respondidas(status, ultima_em DESC);

            CREATE TABLE IF NOT EXISTS eventos_atendimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversa_hash TEXT NOT NULL,
                criado_em REAL NOT NULL,
                estado_antes TEXT NOT NULL,
                estado_depois TEXT NOT NULL,
                fonte TEXT NOT NULL,
                resultado TEXT NOT NULL,
                confianca REAL,
                latencia_ms INTEGER NOT NULL DEFAULT 0,
                mensagem_redigida TEXT NOT NULL DEFAULT ''
            );

            CREATE INDEX IF NOT EXISTS idx_eventos_criado
                ON eventos_atendimento(criado_em DESC);
            CREATE INDEX IF NOT EXISTS idx_eventos_fonte
                ON eventos_atendimento(fonte, criado_em DESC);
            """
        )

    async def obter(self, numero: str) -> Sessao | None:
        """Obtém sessão válida; remove registros vencidos no mesmo passo."""
        agora = time.time()
        async with self._trava:
            self._garantir_aberto()
            self._conexao.execute(
                "DELETE FROM sessoes WHERE expira_em <= ?", (agora,)
            )
            linha = self._conexao.execute(
                "SELECT conteudo_json FROM sessoes WHERE numero = ?", (numero,)
            ).fetchone()
            if linha is None:
                return None
            try:
                return Sessao.de_json(str(linha["conteudo_json"]))
            except (ValueError, TypeError, KeyError) as erro:
                logger.warning("Sessão SQLite inválida para %s: %s", numero, erro)
                self._conexao.execute(
                    "DELETE FROM sessoes WHERE numero = ?", (numero,)
                )
                return None

    async def salvar(self, sessao: Sessao) -> None:
        """Faz UPSERT atômico da sessão e renova seu TTL."""
        agora = time.time()
        sessao.atualizado_em = agora
        expira_em = max(agora + self._ttl, sessao.pausado_ate)
        async with self._trava:
            self._garantir_aberto()
            self._conexao.execute(
                """
                INSERT INTO sessoes(numero, conteudo_json, atualizado_em, expira_em)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(numero) DO UPDATE SET
                    conteudo_json = excluded.conteudo_json,
                    atualizado_em = excluded.atualizado_em,
                    expira_em = excluded.expira_em
                """,
                (sessao.numero, sessao.para_json(), agora, expira_em),
            )

    async def remover(self, numero: str) -> None:
        async with self._trava:
            self._garantir_aberto()
            self._conexao.execute(
                "DELETE FROM sessoes WHERE numero = ?", (numero,)
            )

    async def registrar_pergunta_nao_respondida(
        self,
        pergunta: str,
        *,
        estado: str,
        frente: str = "",
        motivo: str,
    ) -> None:
        """Agrega uma pergunta pendente sem guardar identidade do contato."""
        texto = self.redigir(pergunta)[:600].strip()
        if not texto or sum(caractere.isalnum() for caractere in texto) < 3:
            return
        estado_limpo = (estado or "desconhecido")[:100]
        frente_limpa = (frente or "")[:100]
        motivo_limpo = (motivo or "nao_informado")[:100]
        base_chave = f"{estado_limpo.lower()}|{' '.join(texto.lower().split())}"
        chave = hashlib.sha256(base_chave.encode("utf-8")).hexdigest()
        agora = time.time()

        async with self._trava:
            self._garantir_aberto()
            self._conexao.execute(
                """
                INSERT INTO perguntas_nao_respondidas(
                    chave, pergunta, estado, frente, motivo,
                    ocorrencias, primeira_em, ultima_em, status
                ) VALUES (?, ?, ?, ?, ?, 1, ?, ?, 'pendente')
                ON CONFLICT(chave) DO UPDATE SET
                    ocorrencias = perguntas_nao_respondidas.ocorrencias + 1,
                    ultima_em = excluded.ultima_em,
                    frente = excluded.frente,
                    motivo = excluded.motivo,
                    status = CASE
                        WHEN perguntas_nao_respondidas.status = 'ignorada'
                            THEN 'ignorada'
                        ELSE 'pendente'
                    END
                """,
                (
                    chave,
                    texto,
                    estado_limpo,
                    frente_limpa,
                    motivo_limpo,
                    agora,
                    agora,
                ),
            )

    async def contar_perguntas_pendentes(self) -> int:
        async with self._trava:
            self._garantir_aberto()
            linha = self._conexao.execute(
                """
                SELECT COUNT(*) AS total
                FROM perguntas_nao_respondidas
                WHERE status = 'pendente'
                """
            ).fetchone()
            return int(linha["total"] if linha else 0)

    async def listar_perguntas_pendentes(self, limite: int = 20) -> list[dict[str, Any]]:
        limite_seguro = max(1, min(500, int(limite)))
        async with self._trava:
            self._garantir_aberto()
            linhas = self._conexao.execute(
                """
                SELECT id, pergunta, estado, frente, motivo, ocorrencias,
                       primeira_em, ultima_em, status
                FROM perguntas_nao_respondidas
                WHERE status = 'pendente'
                ORDER BY ocorrencias DESC, ultima_em DESC
                LIMIT ?
                """,
                (limite_seguro,),
            ).fetchall()
            return [dict(linha) for linha in linhas]

    async def registrar_evento(
        self,
        *,
        numero: str,
        estado_antes: str,
        estado_depois: str,
        fonte: str,
        resultado: str,
        mensagem: str = "",
        confianca: float | None = None,
        latencia_ms: int = 0,
    ) -> None:
        """Registra replay operacional com identidade pseudonimizada."""
        conversa_hash = hashlib.sha256(
            (numero or "sem-numero").encode("utf-8")
        ).hexdigest()[:16]
        texto = self.redigir(mensagem)[:600].strip()
        async with self._trava:
            self._garantir_aberto()
            self._conexao.execute(
                """
                INSERT INTO eventos_atendimento(
                    conversa_hash, criado_em, estado_antes, estado_depois,
                    fonte, resultado, confianca, latencia_ms, mensagem_redigida
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    conversa_hash,
                    time.time(),
                    (estado_antes or "desconhecido")[:100],
                    (estado_depois or "desconhecido")[:100],
                    (fonte or "desconhecida")[:80],
                    (resultado or "desconhecido")[:80],
                    confianca,
                    max(0, int(latencia_ms)),
                    texto,
                ),
            )

    async def resumo_eventos(self, horas: int = 24) -> dict[str, Any]:
        """Resumo agregado para observabilidade sem expor conversas inteiras."""
        desde = time.time() - max(1, horas) * 3600
        async with self._trava:
            self._garantir_aberto()
            total = self._conexao.execute(
                "SELECT COUNT(*) AS n FROM eventos_atendimento WHERE criado_em >= ?",
                (desde,),
            ).fetchone()
            fontes = self._conexao.execute(
                """
                SELECT fonte, COUNT(*) AS n
                FROM eventos_atendimento
                WHERE criado_em >= ?
                GROUP BY fonte
                ORDER BY n DESC
                """,
                (desde,),
            ).fetchall()
            handoffs = self._conexao.execute(
                """
                SELECT COUNT(*) AS n FROM eventos_atendimento
                WHERE criado_em >= ? AND resultado = 'handoff'
                """,
                (desde,),
            ).fetchone()
            latencia = self._conexao.execute(
                """
                SELECT AVG(latencia_ms) AS media
                FROM eventos_atendimento
                WHERE criado_em >= ?
                """,
                (desde,),
            ).fetchone()
            return {
                "horas": max(1, horas),
                "total": int(total["n"] if total else 0),
                "fontes": {str(l["fonte"]): int(l["n"]) for l in fontes},
                "handoffs": int(handoffs["n"] if handoffs else 0),
                "latencia_media_ms": round(float(latencia["media"] or 0), 1)
                if latencia
                else 0.0,
            }

    async def listar_eventos(self, limite: int = 50) -> list[dict[str, Any]]:
        """Replay recente redigido para diagnóstico."""
        limite_seguro = max(1, min(500, int(limite)))
        async with self._trava:
            self._garantir_aberto()
            linhas = self._conexao.execute(
                """
                SELECT id, conversa_hash, criado_em, estado_antes, estado_depois,
                       fonte, resultado, confianca, latencia_ms, mensagem_redigida
                FROM eventos_atendimento
                ORDER BY criado_em DESC
                LIMIT ?
                """,
                (limite_seguro,),
            ).fetchall()
            return [dict(linha) for linha in linhas]

    async def fechar(self) -> None:
        async with self._trava:
            if not self._fechado:
                self._conexao.close()
                self._fechado = True

    @staticmethod
    def redigir(texto: str) -> str:
        """Remove CPF, telefone e e-mail antes do registro analítico."""
        limpo = _EMAIL.sub("[EMAIL REDIGIDO]", texto or "")
        limpo = _CPF.sub("[CPF REDIGIDO]", limpo)
        return _TELEFONE.sub("[TELEFONE REDIGIDO]", limpo)

    def _garantir_aberto(self) -> None:
        if self._fechado:
            raise RuntimeError("Banco SQLite já foi fechado.")
