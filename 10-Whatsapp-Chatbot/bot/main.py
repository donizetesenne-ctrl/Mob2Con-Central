"""Serviço do chatbot: recebe webhooks da Evolution API e responde no WhatsApp.

Suba com:
    uvicorn bot.main:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import asyncio
import logging
import os
import sqlite3
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request, status

from .config import Config, carregar_config
from .conhecimento import IndiceManuais
from .evolution import ClienteEvolution, ErroEvolution, normalizar_numero
from .fluxo import ROTULOS_FRENTE, MotorFluxo, Resposta, normalizar
from .llm import AnaliseConversa, ClienteLLM
from .mensagem import MensagemRecebida, interpretar
from .persistencia import BancoSQLite
from .sessao import Sessao, criar_repositorio

logger = logging.getLogger("chatbot")

RETOMAR_BOT = {"menu", "bot", "0", "voltar", "inicio", "atendimento automatico"}
LIMITE_DEDUPE = 2000
ESTADOS_IA_MOBCONNECT = {
    "mobconnect_intencao",
    "mobconnect_comercial",
    "mobconnect_seg_rede",
    "mobconnect_seg_industria",
    "mobconnect_seg_agencia",
    "mobconnect_exemplo",
    "lead_contexto_comercial",
}


class ControleDuplicidade:
    """Evita processar a mesma mensagem duas vezes.

    A Evolution reenvia o webhook quando não recebe 200 rápido, e o WhatsApp
    às vezes duplica eventos. Sem isso, o bot responde em dobro.
    """

    def __init__(self, limite: int = LIMITE_DEDUPE) -> None:
        self._vistos: set[str] = set()
        self._ordem: deque[str] = deque(maxlen=limite)
        self._trava = asyncio.Lock()

    async def novo(self, identificador: str) -> bool:
        if not identificador:
            return True
        async with self._trava:
            if identificador in self._vistos:
                return False
            if len(self._ordem) == self._ordem.maxlen:
                self._vistos.discard(self._ordem[0])
            self._ordem.append(identificador)
            self._vistos.add(identificador)
            return True


class Aplicacao:
    """Reúne configuração e dependências de longa duração."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.evolution = ClienteEvolution(config.evolution)
        self.llm = ClienteLLM(config.llm)
        self.motor = MotorFluxo(config.caminho_fluxo, config.atendimento)
        self.manuais: IndiceManuais | None = None
        if config.manuais.ativo:
            indice: IndiceManuais | None = None
            try:
                indice = IndiceManuais(
                    config.manuais.diretorio,
                    config.manuais.indice_path,
                    max_resultados=config.manuais.max_resultados,
                    max_chars_resposta=config.manuais.max_chars_resposta,
                )
                relatorio = indice.indexar()
                self.manuais = indice
                logger.info(
                    "Busca nos manuais pronta | documentos=%s | chunks=%s",
                    relatorio.documentos,
                    relatorio.chunks,
                )
            except (OSError, ValueError, sqlite3.Error, RuntimeError) as erro:
                if indice is not None:
                    indice.fechar()
                logger.error("Busca nos manuais indisponível: %s", erro)
        ttl_sessao = config.atendimento.minutos_sessao * 60
        self.banco_sqlite: BancoSQLite | None = None
        try:
            self.banco_sqlite = BancoSQLite(config.sqlite_path, ttl_sessao)
        except (OSError, sqlite3.Error) as erro:
            # Atendimento continua em memória se disco/permissão falhar. O log
            # deixa explícito que persistência e aprendizado estão degradados.
            logger.error("SQLite indisponível em %s: %s", config.sqlite_path, erro)
        self.sessoes = criar_repositorio(
            config.redis_url,
            ttl_sessao,
            fallback_persistente=self.banco_sqlite,
        )
        self.dedupe = ControleDuplicidade()
        # Responsável geral: recebe o que não tem frente definida.
        self.numero_notificacao = normalizar_numero(
            os.environ.get("NUMERO_NOTIFICACAO", "")
        )
        # Destino do handoff por frente responsável (NOTIFICACAO_SUPORTE,
        # NOTIFICACAO_FINANCEIRO, ...). Frente vazia ou sem número configurado
        # cai no responsável geral.
        # Modo teste: nada sai para as frentes; tudo cai no responsável geral,
        # com o destino real declarado no texto para conferir o roteamento.
        self.notificacao_modo_teste = os.environ.get(
            "NOTIFICACAO_MODO_TESTE", ""
        ).strip().lower() in {"1", "true", "sim", "yes"}
        self.notificacao_por_frente: dict[str, str] = {}
        for frente in ROTULOS_FRENTE:
            destino = normalizar_numero(
                os.environ.get(f"NOTIFICACAO_{frente.upper()}", "")
            )
            if destino:
                self.notificacao_por_frente[frente] = destino

    async def encerrar(self) -> None:
        await self.evolution.fechar()
        await self.llm.fechar()
        await self.sessoes.fechar()
        if self.banco_sqlite is not None and self.sessoes is not self.banco_sqlite:
            await self.banco_sqlite.fechar()
        if self.manuais is not None:
            self.manuais.fechar()

    # ---------------------------------------------------------------- horário

    def _agora_local(self) -> datetime:
        fuso = self.config.atendimento.fuso_horario
        try:
            from zoneinfo import ZoneInfo

            return datetime.now(ZoneInfo(fuso))
        except Exception:  # noqa: BLE001 - Windows sem tzdata cai aqui
            logger.debug("Fuso '%s' indisponível; usando UTC-3.", fuso)
            return datetime.now(timezone(timedelta(hours=-3)))

    def dentro_do_horario(self) -> bool:
        atendimento = self.config.atendimento
        agora = self._agora_local()
        if agora.weekday() not in atendimento.dias_uteis:
            return False
        minutos_agora = agora.hour * 60 + agora.minute
        abertura = atendimento.hora_abertura[0] * 60 + atendimento.hora_abertura[1]
        fechamento = atendimento.hora_fechamento[0] * 60 + atendimento.hora_fechamento[1]
        return abertura <= minutos_agora < fechamento

    # ---------------------------------------------------------------- filtros

    def deve_ignorar(self, mensagem: MensagemRecebida) -> str | None:
        """Devolve o motivo para ignorar, ou None para processar."""
        atendimento = self.config.atendimento
        if not mensagem.valida:
            return "payload sem número ou id"
        if mensagem.de_mim:
            return "mensagem enviada pelo próprio número"
        if mensagem.grupo and not atendimento.responder_grupos:
            return "mensagem de grupo"
        if mensagem.numero in atendimento.numeros_bloqueados:
            return "número na lista de bloqueio"
        if atendimento.numeros_permitidos and (
            mensagem.numero not in atendimento.numeros_permitidos
        ):
            return "número fora da lista de permitidos"
        return None

    # ---------------------------------------------------------------- envio

    async def _enviar(self, numero: str, mensagens: list[str]) -> None:
        atendimento = self.config.atendimento
        for indice, texto in enumerate(mensagens):
            if not texto or not texto.strip():
                continue
            if atendimento.delay_digitando_ms > 0:
                await self.evolution.marcar_digitando(
                    numero, atendimento.delay_digitando_ms
                )
            try:
                await self.evolution.enviar_texto(
                    numero, texto, delay_ms=atendimento.delay_digitando_ms
                )
            except (ErroEvolution, httpx.HTTPError, OSError) as erro:
                logger.error("Falha ao enviar para %s: %s", numero, erro)
                return  # não insiste nas próximas: provável instância desconectada
            if indice < len(mensagens) - 1:
                await asyncio.sleep(0.6)

    def _destino_do_handoff(self, sessao: Sessao) -> tuple[str, str]:
        """Número que recebe o aviso e a frente que ele representa."""
        frente = str(sessao.dados.get("frente") or "").strip().lower()
        if sessao.dados.get("handoff_sem_frente"):
            return self.numero_notificacao, frente
        destino = self.notificacao_por_frente.get(frente, "")
        if destino:
            return destino, frente
        # sem número para a frente, vai ao responsável geral — mas levando a
        # frente no texto, senão ele recebe o caso sem saber de que assunto é.
        return self.numero_notificacao, frente

    async def _notificar_time(self, sessao: Sessao) -> None:
        destino, frente = self._destino_do_handoff(sessao)
        if not destino:
            return
        nota_teste = ""
        if self.notificacao_modo_teste and destino != self.numero_notificacao:
            nota_teste = (
                f"\n\n_Modo teste: em produção este aviso iria para +{destino}._"
            )
            destino = self.numero_notificacao
        if destino == sessao.numero:
            # quem pediu atendimento é o próprio destino: devolver o resumo
            # interno para ele é ruído, não aviso.
            logger.info(
                "Handoff de %s sem aviso: destino configurado é o próprio contato",
                sessao.numero,
            )
            return
        logger.info(
            "Handoff de %s encaminhado para %s (frente=%s)",
            sessao.numero,
            destino,
            frente or "geral",
        )
        try:
            await self.evolution.enviar_texto(
                destino,
                self.motor.resumo_para_atendente(sessao, frente=frente) + nota_teste,
            )
        except (ErroEvolution, httpx.HTTPError, OSError) as erro:
            logger.error("Não foi possível notificar o time: %s", erro)

    # ---------------------------------------------------------------- fluxo

    @staticmethod
    def _persona_para_manuais(sessao: Sessao) -> str | None:
        """Persona para reranking; None bloqueia telas de gestor ao promotor."""
        frente = normalizar(str(sessao.dados.get("frente") or ""))
        if frente == "promotor" or sessao.estado == "acesso_promotor":
            return None

        segmento = normalizar(str(sessao.dados.get("segmento") or ""))
        if "agencia" in segmento:
            return "agency"
        if "industria" in segmento or "fornecedor" in segmento:
            return "supplier"
        if "rede" in segmento:
            return "retailer"
        if "loja" in segmento:
            return "store"
        return ""

    def _responder_com_manuais(
        self,
        sessao: Sessao,
        pergunta: str,
    ) -> Resposta | None:
        """Recupera orientação extrativa; nunca inventa além do trecho."""
        if self.manuais is None:
            return None
        persona = self._persona_para_manuais(sessao)
        if persona is None:
            return None
        try:
            texto = self.manuais.responder(pergunta, persona=persona)
        except (OSError, sqlite3.Error, RuntimeError) as erro:
            logger.error("Falha ao buscar nos manuais: %s", erro)
            return None
        if not texto:
            return None

        sessao.tentativas_invalidas = 0
        mensagens = [texto]
        if not sessao.dados.get("_dica_humano"):
            sessao.dados["_dica_humano"] = "1"
            mensagens.append("Se preferir falar com uma pessoa do time, digite *9*.")
        logger.info("Pergunta respondida pela busca local nos manuais.")
        return Resposta(mensagens=mensagens)

    def _deve_usar_ia_estruturada(self, sessao: Sessao, texto: str) -> bool:
        """IA atua onde agrega contexto; números/menu continuam determinísticos."""
        if not self.llm.ativo:
            return False
        normalizado = normalizar(texto)
        if not normalizado:
            return False
        if normalizado in RETOMAR_BOT or normalizado in {
            "9",
            "atendente",
            "humano",
            "pessoa",
            "time",
        }:
            return False
        if normalizado.isdigit():
            return False
        return (
            "mobconnect" in normalizado
            or sessao.estado in ESTADOS_IA_MOBCONNECT
        )

    def _contexto_manuais_para_ia(self, sessao: Sessao, pergunta: str) -> str:
        """Recupera evidência curta dos manuais para aterrar a análise da IA."""
        if self.manuais is None:
            return ""
        persona = self._persona_para_manuais(sessao)
        if persona is None:
            return ""
        try:
            resultados = self.manuais.buscar(pergunta, persona=persona, limite=2)
        except (OSError, sqlite3.Error, RuntimeError) as erro:
            logger.error("Falha ao montar contexto da IA: %s", erro)
            return ""
        blocos: list[str] = []
        for item in resultados:
            blocos.append(
                f"Documento: {item.titulo}\n"
                f"Seção: {item.secao}\n"
                f"Trecho: {item.conteudo[:1800]}"
            )
        return "\n\n".join(blocos)[:5000]

    @staticmethod
    def _aplicar_campos_ia(sessao: Sessao, analise: AnaliseConversa) -> None:
        """Guarda somente contexto novo; a IA não sobrescreve dado confirmado."""
        for campo, valor in analise.campos.items():
            atual = str(sessao.dados.get(campo) or "").strip()
            if not atual and valor.strip():
                sessao.dados[campo] = valor.strip()[:600]

    async def _tentar_ia_estruturada(
        self,
        sessao: Sessao,
        pergunta: str,
    ) -> Resposta | None:
        """Usa IA como roteador seguro; fluxo tradicional é o fallback."""
        if not self._deve_usar_ia_estruturada(sessao, pergunta):
            return None
        analise = await self.llm.analisar(
            pergunta,
            estado=sessao.estado,
            dados_sessao=sessao.dados,
            historico=sessao.historico,
            contexto_conhecimento=self._contexto_manuais_para_ia(sessao, pergunta),
        )
        if analise is None or analise.confianca < 0.58:
            return None

        self._aplicar_campos_ia(sessao, analise)
        logger.info(
            "IA estruturada | intenção=%s | ação=%s | confiança=%.2f",
            analise.intencao,
            analise.acao,
            analise.confianca,
        )

        if analise.acao == "continuar_fluxo":
            return None

        if analise.acao == "responder":
            # Mantém o estado coerente com a conversa para que a próxima
            # mensagem continue no contexto MobConnect, em vez de voltar ao menu.
            if analise.intencao == "mobconnect_conhecer":
                self.motor.ir_para(sessao, "mobconnect_comercial")
            texto = analise.resposta.strip()
            pergunta_faltante = analise.pergunta_faltante.strip()
            if pergunta_faltante and pergunta_faltante.lower() not in texto.lower():
                texto = f"{texto}\n\n{pergunta_faltante}".strip()
            if not texto:
                return None
            sessao.tentativas_invalidas = 0
            return Resposta(mensagens=[texto])

        if analise.acao == "suporte_mobconnect":
            resposta = self.motor.ir_para(sessao, "mobconnect")
            if analise.resposta:
                resposta.mensagens.insert(0, analise.resposta)
            return resposta

        if analise.acao == "encaminhar_comercial":
            sessao.dados["frente"] = "comercial_mobconnect"
            campos_contexto = {
                "empresa_contato",
                "segmento",
                "redes_atendidas",
                "porte",
                "necessidade",
            }
            tem_contexto = any(
                str(sessao.dados.get(campo) or "").strip()
                for campo in campos_contexto
            )
            if not tem_contexto:
                resposta = self.motor.ir_para(sessao, "lead_contexto_comercial")
                if analise.resposta:
                    resposta.mensagens.insert(0, analise.resposta)
                return resposta
            sessao.dados.setdefault("contexto_comercial", pergunta[:600])
            mensagens = [analise.resposta] if analise.resposta else []
            mensagens.append(self.motor.texto("transferido", sessao))
            return Resposta(mensagens=mensagens, transferir=True)

        if analise.acao == "humano":
            resposta = self.motor.ir_para(sessao, "atendente")
            if analise.resposta:
                resposta.mensagens.insert(0, analise.resposta)
            return resposta

        return None

    async def _registrar_pergunta_nao_respondida(
        self,
        sessao: Sessao,
        pergunta: str,
        motivo: str,
    ) -> None:
        if self.banco_sqlite is None:
            return
        try:
            await self.banco_sqlite.registrar_pergunta_nao_respondida(
                pergunta,
                estado=sessao.estado,
                frente=str(sessao.dados.get("frente") or ""),
                motivo=motivo,
            )
        except (OSError, sqlite3.Error, RuntimeError) as erro:
            # Aprendizado é observabilidade, não caminho crítico. Falha nele
            # nunca pode impedir resposta ao contato.
            logger.error("Falha ao registrar pergunta não respondida: %s", erro)

    async def atender(self, mensagem: MensagemRecebida) -> None:
        """Processa uma mensagem já filtrada e responde ao contato."""
        atendimento = self.config.atendimento
        sessao = await self.sessoes.obter(mensagem.numero)
        nova = sessao is None
        if sessao is None:
            sessao = Sessao(numero=mensagem.numero)
        if mensagem.nome:
            sessao.nome = mensagem.nome

        normalizado = normalizar(mensagem.texto)

        # atendimento humano em andamento: o bot fica calado
        if sessao.pausada:
            if normalizado in RETOMAR_BOT:
                sessao.retomar()
                resposta = self.motor.iniciar(
                    sessao, dentro_do_horario=self.dentro_do_horario()
                )
                resposta.mensagens.insert(0, self.motor.texto("retomado", sessao))
                await self.sessoes.salvar(sessao)
                await self._enviar(sessao.numero, resposta.mensagens)
            else:
                logger.info(
                    "Sessão de %s em atendimento humano; mensagem não respondida.",
                    sessao.numero,
                )
                await self.sessoes.salvar(sessao)
            return

        # mídia sem legenda: não há texto para interpretar
        if not mensagem.texto and mensagem.tem_midia:
            await self.sessoes.salvar(sessao)
            await self._enviar(
                sessao.numero, [self.motor.texto("midia_nao_suportada", sessao)]
            )
            return

        if not mensagem.texto:
            # INFO, nao DEBUG: sem isso um descarte aqui fica invisivel e
            # parece que o bot "simplesmente nao respondeu".
            logger.info(
                "Sem texto para interpretar | numero=%s | tipo=%s | id=%s",
                sessao.numero,
                mensagem.tipo or "desconhecido",
                mensagem.id,
            )
            await self.sessoes.salvar(sessao)
            return

        abertura: list[str] = []
        inicial: Resposta | None = None
        primeiro_texto_nao_reconhecido = False
        resposta_ia: Resposta | None = None

        if nova:
            inicial = self.motor.iniciar(
                sessao, dentro_do_horario=self.dentro_do_horario()
            )
            if mensagem.texto and not self.motor.apenas_saudacao(mensagem.texto):
                # A primeira mensagem também é conteúdo. A IA estruturada pode
                # responder/rotear direto; se não assumir, o fluxo tradicional
                # continua exatamente como antes.
                abertura = inicial.mensagens[:1]
                resposta_ia = await self._tentar_ia_estruturada(
                    sessao, mensagem.texto
                )
                if resposta_ia is not None:
                    resposta = resposta_ia
                else:
                    resposta = self.motor.processar(sessao, mensagem.texto)
                    primeiro_texto_nao_reconhecido = resposta.usar_llm
            else:
                resposta = inicial
        else:
            resposta_ia = await self._tentar_ia_estruturada(
                sessao, mensagem.texto
            )
            resposta = (
                resposta_ia
                if resposta_ia is not None
                else self.motor.processar(sessao, mensagem.texto)
            )

        if resposta.usar_llm:
            resposta_manual = self._responder_com_manuais(sessao, mensagem.texto)
            if resposta_manual is not None:
                resposta = resposta_manual
            elif primeiro_texto_nao_reconhecido and inicial and not self.llm.ativo:
                # Sem manual relevante nem IA, a primeira mensagem que o fluxo
                # não reconhece não merece "opção inválida": a pessoa ainda
                # não escolheu nada. Abre com saudação e menu, sem punição.
                await self._registrar_pergunta_nao_respondida(
                    sessao,
                    mensagem.texto,
                    "primeira_mensagem_nao_classificada",
                )
                sessao.tentativas_invalidas = 0
                resposta = inicial
                abertura = []
            else:
                resposta = await self._responder_com_llm(sessao, mensagem.texto)

        if abertura:
            resposta.mensagens[0:0] = abertura

        if resposta.transferir and sessao.dados.get("handoff_sem_frente"):
            await self._registrar_pergunta_nao_respondida(
                sessao,
                mensagem.texto,
                "esgotou_tentativas",
            )

        if resposta.transferir:
            sessao.pausar(atendimento.minutos_pausa_humano)

        sessao.registrar_turno("user", mensagem.texto, self.config.llm.max_historico)
        for texto in resposta.mensagens:
            sessao.registrar_turno("assistant", texto, self.config.llm.max_historico)

        await self.sessoes.salvar(sessao)
        await self._enviar(sessao.numero, resposta.mensagens)

        if resposta.transferir:
            await self._notificar_time(sessao)

    async def _responder_com_llm(self, sessao: Sessao, pergunta: str) -> Resposta:
        """Tenta a IA; se não houver resposta, registra e repete o menu."""
        if not self.llm.ativo:
            await self._registrar_pergunta_nao_respondida(
                sessao, pergunta, "ia_inativa"
            )
            return self.motor.resposta_menu_apos_erro(sessao, pergunta)
        texto = await self.llm.responder(pergunta, sessao.historico)
        if not texto:
            await self._registrar_pergunta_nao_respondida(
                sessao, pergunta, "ia_sem_resposta"
            )
            return self.motor.resposta_menu_apos_erro(sessao, pergunta)

        # Conversa em texto livre respondida com sucesso não é tentativa
        # inválida. Sem zerar aqui, quem escreve naturalmente em vez de digitar
        # números é transferido ao humano após MAX_TENTATIVAS_INVALIDAS trocas,
        # justamente o comportamento que se quer incentivar.
        sessao.tentativas_invalidas = 0

        mensagens = [texto]
        # A dica de atendimento humano aparece uma vez por conversa. Colada em
        # toda resposta, ela vira ruído e faz a IA soar como menu.
        if not sessao.dados.get("_dica_humano"):
            sessao.dados["_dica_humano"] = "1"
            mensagens.append("Se preferir falar com uma pessoa do time, digite *9*.")
        return Resposta(mensagens=mensagens)


aplicacao: Aplicacao | None = None


def obter_aplicacao() -> Aplicacao:
    if aplicacao is None:  # pragma: no cover - só ocorre fora do lifespan
        raise RuntimeError("Aplicação não inicializada.")
    return aplicacao


@asynccontextmanager
async def ciclo_de_vida(_app: FastAPI):
    global aplicacao
    config = carregar_config()
    formato = "%(asctime)s %(levelname)-7s %(name)s | %(message)s"
    logging.basicConfig(
        level=getattr(logging, config.nivel_log, logging.INFO),
        format=formato,
    )
    # Log em arquivo além do console: sem isso, "por que o bot nao respondeu?"
    # so tem resposta enquanto a janela do terminal estiver aberta, e o motivo
    # do descarte (que ja e registrado em INFO) se perde no fechamento.
    try:
        from logging.handlers import RotatingFileHandler

        arquivo = RotatingFileHandler(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.log"),
            maxBytes=2_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        arquivo.setFormatter(logging.Formatter(formato))
        logging.getLogger().addHandler(arquivo)
    except OSError as erro:  # disco cheio, permissao: nao impede o bot de subir
        logger.warning("Sem log em arquivo: %s", erro)

    if not config.evolution.api_key:
        logger.warning(
            "EVOLUTION_API_KEY vazio. Rode 'python scripts/gerar_env.py' antes de usar."
        )
    aplicacao = Aplicacao(config)
    await aplicacao.evolution.abrir()
    logger.info(
        "Chatbot pronto | instância=%s | evolution=%s | IA=%s",
        config.evolution.instancia,
        config.evolution.base_url,
        "on" if aplicacao.llm.ativo else "off",
    )
    try:
        yield
    finally:
        await aplicacao.encerrar()
        aplicacao = None


app = FastAPI(
    title="Chatbot WhatsApp Mob2Con",
    description="Atendimento automático no WhatsApp via Evolution API.",
    version="1.0.0",
    lifespan=ciclo_de_vida,
)


@app.get("/health")
async def health() -> dict[str, Any]:
    """Checagem simples de vida do serviço e da conexão do WhatsApp."""
    atual = obter_aplicacao()
    conexao: dict[str, Any] = {}
    alcancavel = True
    try:
        conexao = await atual.evolution.estado_conexao()
    except (ErroEvolution, httpx.HTTPError, OSError) as erro:
        # health precisa responder 200 mesmo com a Evolution fora do ar,
        # senão o monitoramento perde a informação mais importante
        alcancavel = False
        conexao = {"erro": str(erro)}
    perguntas_pendentes: int | None = None
    if atual.banco_sqlite is not None:
        try:
            perguntas_pendentes = (
                await atual.banco_sqlite.contar_perguntas_pendentes()
            )
        except (OSError, sqlite3.Error, RuntimeError) as erro:
            logger.error("Falha ao consultar aprendizado no health: %s", erro)

    manuais_status: dict[str, Any] = {
        "ativo": False,
        "documentos": 0,
        "chunks": 0,
        "fts5": False,
    }
    if atual.manuais is not None:
        try:
            manuais_status = atual.manuais.status()
        except (OSError, sqlite3.Error, RuntimeError) as erro:
            logger.error("Falha ao consultar status dos manuais: %s", erro)

    return {
        "status": "ok" if alcancavel else "degradado",
        "evolution_alcancavel": alcancavel,
        "instancia": atual.config.evolution.instancia,
        "dentro_do_horario": atual.dentro_do_horario(),
        "ia_ativa": atual.llm.ativo,
        "persistencia_sessoes": type(atual.sessoes).__name__,
        "perguntas_pendentes": perguntas_pendentes,
        "manuais": manuais_status,
        "whatsapp": conexao,
    }


async def _processar_em_segundo_plano(payload: dict[str, Any]) -> None:
    """Executa o atendimento fora do ciclo da requisição do webhook."""
    atual = obter_aplicacao()
    mensagem = interpretar(payload)
    if mensagem is None:
        dados = payload.get("data")
        dados = dados[0] if isinstance(dados, list) and dados else dados
        chave = dados.get("key") if isinstance(dados, dict) else None
        logger.info(
            "Payload nao interpretado como mensagem | jid=%s | tipo=%s",
            (chave or {}).get("remoteJid") if isinstance(chave, dict) else "?",
            (dados or {}).get("messageType") if isinstance(dados, dict) else "?",
        )
        return

    motivo = atual.deve_ignorar(mensagem)
    if motivo:
        # INFO de propósito: "por que o bot não respondeu?" é a pergunta mais
        # comum em operação, e a resposta precisa estar no log padrão.
        logger.info(
            "Mensagem ignorada (%s) | numero=%s | jid=%s",
            motivo,
            mensagem.numero or "?",
            mensagem.jid,
        )
        return

    # Mensagem que chega sem conteúdo (tipo 'unknown', message vazio) é quase
    # sempre falha de decifragem: o WhatsApp reenvia a MESMA mensagem, agora
    # legível. Se ela consumisse o dedupe aqui, a cópia boa seria descartada
    # como duplicada e a pessoa ficaria sem resposta para sempre.
    if not mensagem.texto and not mensagem.tem_midia:
        logger.info(
            "Mensagem sem conteudo | numero=%s | tipo=%s | id=%s | "
            "id NAO consumido: aguardando reenvio decifrado",
            mensagem.numero or "?",
            mensagem.tipo or "desconhecido",
            mensagem.id,
        )
        return

    if not await atual.dedupe.novo(mensagem.id):
        logger.info(
            "Mensagem %s ja processada (duplicada) | numero=%s",
            mensagem.id,
            mensagem.numero or "?",
        )
        return

    try:
        await atual.atender(mensagem)
    except Exception:  # noqa: BLE001 - o webhook nunca deve derrubar o serviço
        logger.exception("Erro ao atender %s", mensagem.numero)
        try:
            sessao = Sessao(numero=mensagem.numero, nome=mensagem.nome)
            await atual._enviar(  # noqa: SLF001 - caminho de erro interno
                mensagem.numero, [atual.motor.texto("erro_interno", sessao)]
            )
        except Exception:  # noqa: BLE001
            logger.exception("Falha ao avisar o contato sobre o erro.")


def _validar_token(recebido: str | None) -> None:
    esperado = obter_aplicacao().config.webhook_token
    if esperado and recebido != esperado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token inválido"
        )


@app.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
async def webhook(
    request: Request,
    tarefas: BackgroundTasks,
    x_webhook_token: str | None = Header(default=None),
) -> dict[str, str]:
    """Endpoint que a Evolution API chama a cada evento."""
    _validar_token(x_webhook_token or request.query_params.get("token"))
    try:
        payload = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="corpo não é JSON") from None

    evento = str(payload.get("event") or "").lower().replace("_", ".")
    if evento and evento != "messages.upsert":
        logger.debug("Evento ignorado: %s", evento)
        return {"status": "ignorado"}

    tarefas.add_task(_processar_em_segundo_plano, payload)
    return {"status": "recebido"}


@app.post("/webhook/{evento}", status_code=status.HTTP_202_ACCEPTED)
async def webhook_por_evento(
    evento: str,
    request: Request,
    tarefas: BackgroundTasks,
    x_webhook_token: str | None = Header(default=None),
) -> dict[str, str]:
    """Rota usada quando a Evolution está com webhookByEvents ligado."""
    _validar_token(x_webhook_token or request.query_params.get("token"))
    if evento.lower().replace("_", "-") not in {"messages-upsert", "messages.upsert"}:
        return {"status": "ignorado"}
    try:
        payload = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="corpo não é JSON") from None
    tarefas.add_task(_processar_em_segundo_plano, payload)
    return {"status": "recebido"}
