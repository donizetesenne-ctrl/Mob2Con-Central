"""Motor de fluxo conversacional.

O fluxo em si vive em `fluxo.json`, então dá para mudar menus e textos sem
tocar em Python. Este módulo apenas interpreta esse arquivo.
"""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import ConfigAtendimento
from .sessao import ESTADO_INICIAL, Sessao

logger = logging.getLogger(__name__)

NOMES_DIAS = [
    "segunda",
    "terça",
    "quarta",
    "quinta",
    "sexta",
    "sábado",
    "domingo",
]

# Palavras que, sozinhas ou combinadas, não carregam assunto: "oi", "bom dia",
# "olá tudo bem". Serve para separar quem só cumprimentou de quem já descreveu
# o problema na primeira mensagem — o segundo caso merece resposta, não menu.
PALAVRAS_SAUDACAO = frozenset(
    {
        "oi", "oii", "oiii", "ola", "opa", "eae", "e", "ai", "alo", "alow",
        "hey", "hello", "hi", "bom", "boa", "boas", "dia", "tarde", "noite",
        "tudo", "bem", "certo", "prezados", "prezado", "prezada",
        "senhores", "senhor", "senhora", "pessoal", "time", "equipe",
        "favor", "por", "gostaria", "queria", "informacoes", "informacao",
        "ajuda", "ajudar", "duvida", "duvidas", "saudacoes", "obrigado",
        "obrigada", "vc", "voce", "preciso", "precisava", "de", "da", "do",
        "com", "um", "uma", "me", "pode", "poderia", "podem", "sobre",
    }
)


# Frentes que resolvem cada assunto. O fluxo grava a frente no campo 'frente'
# (ação 'definir') ao entrar no assunto, e o handoff usa isso para avisar quem
# de fato resolve, em vez de mandar tudo para um número só.
ROTULOS_FRENTE = {
    "suporte": "Suporte",
    "financeiro": "Financeiro",
    "comercial_industria": "Comercial — indústria e agências",
    "comercial_varejo": "Comercial — varejo e novas redes",
    "comercial_mobconnect": "Comercial — MobConnect",
    "promotor": "Promotor sem vínculo de gestão (orientar a agência/fornecedor)",
}


class _ContextoTolerante(dict):
    """dict que devolve string vazia em chave ausente, evitando KeyError."""

    def __missing__(self, chave: str) -> str:  # noqa: D105
        return ""


def normalizar(texto: str) -> str:
    """Minúsculas, sem acento, sem pontuação, espaços colapsados."""
    if not texto:
        return ""
    sem_acento = "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )
    limpo = re.sub(r"[^\w\s]", " ", sem_acento.lower())
    return re.sub(r"\s+", " ", limpo).strip()


@dataclass
class Resposta:
    """O que o bot deve fazer depois de processar uma mensagem."""

    mensagens: list[str] = field(default_factory=list)
    transferir: bool = False
    usar_llm: bool = False


class ErroFluxo(RuntimeError):
    """Arquivo de fluxo ausente ou inválido."""


class MotorFluxo:
    """Interpreta o fluxo declarado em JSON."""

    def __init__(self, caminho: Path, atendimento: ConfigAtendimento) -> None:
        self._atendimento = atendimento
        self._definicao = self._carregar(caminho)
        self._estados: dict[str, dict[str, Any]] = self._definicao["estados"]
        self._textos: dict[str, str] = self._definicao.get("textos", {})
        self._atalhos: dict[str, str] = {
            normalizar(gatilho): destino
            for gatilho, destino in self._definicao.get("atalhos_globais", {}).items()
        }
        self._validar()

    # ---------------------------------------------------------------- carga

    @staticmethod
    def _carregar(caminho: Path) -> dict[str, Any]:
        if not caminho.exists():
            raise ErroFluxo(f"Arquivo de fluxo não encontrado: {caminho}")
        try:
            definicao = json.loads(caminho.read_text(encoding="utf-8"))
        except json.JSONDecodeError as erro:
            raise ErroFluxo(f"JSON inválido em {caminho}: {erro}") from erro
        if not isinstance(definicao.get("estados"), dict):
            raise ErroFluxo(f"{caminho} precisa ter o objeto 'estados'.")
        return definicao

    def _validar(self) -> None:
        """Falha cedo se o fluxo aponta para estados que não existem."""
        if ESTADO_INICIAL not in self._estados:
            raise ErroFluxo(f"O fluxo precisa do estado '{ESTADO_INICIAL}'.")

        pendencias: list[str] = []
        for nome, estado in self._estados.items():
            destinos = list(estado.get("opcoes", {}).values())
            if estado.get("proximo"):
                destinos.append(estado["proximo"])
            for destino in destinos:
                if destino not in self._estados:
                    pendencias.append(f"{nome} -> {destino}")
            if estado.get("capturar") and not estado.get("proximo"):
                pendencias.append(f"{nome} captura texto mas não define 'proximo'")
            if not any(
                chave in estado for chave in ("mensagem", "acao")
            ):  # estado morto
                pendencias.append(f"{nome} não tem 'mensagem' nem 'acao'")

        for destino in self._atalhos.values():
            if destino not in self._estados:
                pendencias.append(f"atalho global -> {destino}")

        if pendencias:
            raise ErroFluxo("Fluxo inconsistente: " + "; ".join(pendencias))

    # ---------------------------------------------------------------- textos

    def _contexto(self, sessao: Sessao) -> _ContextoTolerante:
        primeiro_nome = sessao.nome.split(" ")[0] if sessao.nome else ""
        abertura = "%02d:%02d" % self._atendimento.hora_abertura
        fechamento = "%02d:%02d" % self._atendimento.hora_fechamento
        contexto = _ContextoTolerante(sessao.dados)
        empresa_contato = str(sessao.dados.get("empresa_contato") or "").strip()
        porte = str(sessao.dados.get("porte") or "").strip()
        if empresa_contato and porte:
            cenario_mobconnect = (
                f"No cenário da *{empresa_contato}*, com {porte}, já dá para "
                "pensar no MobConnect de forma bem prática.\n\n"
            )
        elif empresa_contato:
            cenario_mobconnect = (
                f"Pensando especificamente no cenário da *{empresa_contato}*, "
                "o MobConnect funciona assim.\n\n"
            )
        elif porte:
            cenario_mobconnect = (
                f"Para uma operação com {porte}, o MobConnect funciona assim.\n\n"
            )
        else:
            cenario_mobconnect = ""
        contexto.update(
            {
                "empresa": self._atendimento.nome_empresa,
                "nome": f", {primeiro_nome}" if primeiro_nome else "",
                "nome_puro": primeiro_nome,
                "abertura": abertura,
                "fechamento": fechamento,
                "dias": self._descrever_dias(),
                "cenario_mobconnect": cenario_mobconnect,
            }
        )
        return contexto

    def _descrever_dias(self) -> str:
        dias = sorted(self._atendimento.dias_uteis)
        if not dias:
            return "dias úteis"
        if dias == list(range(dias[0], dias[-1] + 1)) and len(dias) > 1:
            return f"{NOMES_DIAS[dias[0]]} a {NOMES_DIAS[dias[-1]]}"
        return ", ".join(NOMES_DIAS[dia] for dia in dias)

    def texto(self, chave: str, sessao: Sessao) -> str:
        bruto = self._textos.get(chave, "")
        return bruto.format_map(self._contexto(sessao)) if bruto else ""

    # ---------------------------------------------------------------- triagem

    LIMITE_PALAVRAS_SAUDACAO = 6

    def apenas_saudacao(self, texto: str) -> bool:
        """True quando a mensagem não carrega assunto algum.

        "oi", "bom dia", "preciso de ajuda" → o menu ajuda de verdade.
        "meu promotor foi barrado na portaria" → responder o problema; exibir
        menu aqui é fazer a pessoa repetir o que ela acabou de dizer.
        """
        normalizado = normalizar(texto)
        if not normalizado:
            return True
        palavras = normalizado.split()
        if len(palavras) > self.LIMITE_PALAVRAS_SAUDACAO:
            return False
        return all(palavra in PALAVRAS_SAUDACAO for palavra in palavras)

    # ---------------------------------------------------------------- navegação

    def iniciar(self, sessao: Sessao, *, dentro_do_horario: bool) -> Resposta:
        """Primeira interação da sessão: saúda e mostra o menu."""
        sessao.reiniciar()
        chave = "saudacao" if dentro_do_horario else "fora_horario"
        abertura = self.texto(chave, sessao)
        resposta = self._entrar(sessao, ESTADO_INICIAL)
        if abertura:
            resposta.mensagens.insert(0, abertura)
        return resposta

    def processar(self, sessao: Sessao, texto_recebido: str) -> Resposta:
        """Avança a conversa a partir da mensagem do contato."""
        texto = (texto_recebido or "").strip()
        normalizado = normalizar(texto)

        destino_atalho = self._atalhos.get(normalizado)
        if destino_atalho:
            return self._entrar(sessao, destino_atalho)

        estado = self._estados.get(sessao.estado)
        if estado is None:
            logger.warning("Estado desconhecido '%s'; voltando ao menu.", sessao.estado)
            return self._entrar(sessao, ESTADO_INICIAL)

        # MobConnect precisa de leitura composicional: a mesma frase pode conter
        # "execução" e "MobConnect" sem significar suporte. Ex.: "queria entender
        # se o MobConnect ajudaria a acompanhar execução" é descoberta do produto.
        # Esta camada local funciona mesmo sem LLM e evita cair no menu por
        # ambiguidade entre gatilhos isolados.
        resposta_mobconnect = self._rotear_mobconnect_local(sessao, texto, normalizado)
        if resposta_mobconnect is not None:
            return resposta_mobconnect

        # Cumprimentos durante uma conversa não são erro de entendimento.
        # Mantém o usuário no ponto atual sem consumir tentativa nem alimentar
        # a fila de aprendizado com "oi", "opa", "bom dia" etc.
        if self.apenas_saudacao(texto):
            sessao.tentativas_invalidas = 0
            if sessao.estado == ESTADO_INICIAL:
                return Resposta(mensagens=[self._mensagem_do_estado(estado, sessao)])
            if estado.get("opcoes") or estado.get("capturar"):
                return Resposta(
                    mensagens=[
                        "Oi! Podemos continuar de onde paramos.",
                        self._mensagem_do_estado(estado, sessao),
                    ]
                )
            return self._entrar(sessao, ESTADO_INICIAL)

        campo = estado.get("capturar")
        if campo:
            return self._capturar(sessao, estado, campo, texto)

        chave_opcao = self._resolver_opcao(estado, normalizado)
        if chave_opcao is not None:
            sessao.tentativas_invalidas = 0
            return self._entrar(sessao, estado["opcoes"][chave_opcao])

        # Menu é catálogo global de intenções, não trilho obrigatório. Se a
        # pessoa muda de assunto no meio da conversa (ex.: acesso -> fatura),
        # tentamos os gatilhos principais antes de recorrer aos manuais/IA.
        # Perguntas operacionais detalhadas ("como regularizar...", "onde
        # vejo...") seguem para os manuais: uma palavra genérica como
        # "documento" não pode reduzir a pergunta inteira ao menu Cadastro.
        palavras = normalizado.split()
        primeira = palavras[0] if palavras else ""
        pergunta_detalhada = len(palavras) >= 4 and (
            primeira in {"como", "onde", "qual", "quais", "quando", "quem", "porque"}
            or palavras[:2] == ["por", "que"]
            or "como" in palavras[:3]
        )
        if sessao.estado != ESTADO_INICIAL and not pergunta_detalhada:
            menu = self._estados[ESTADO_INICIAL]
            chave_menu = self._resolver_opcao(menu, normalizado)
            if chave_menu is not None:
                logger.info(
                    "Mudança de assunto por texto livre: %s -> %s",
                    sessao.estado,
                    menu["opcoes"][chave_menu],
                )
                sessao.tentativas_invalidas = 0
                return self._entrar(sessao, menu["opcoes"][chave_menu])

        return self._nao_entendi(sessao, estado)

    def _rotear_mobconnect_local(
        self,
        sessao: Sessao,
        texto: str,
        normalizado: str,
    ) -> Resposta | None:
        """Entende intenções comuns de MobConnect sem depender de LLM."""
        em_contexto = sessao.estado in {
            "mobconnect_intencao",
            "mobconnect_comercial",
            "mobconnect_seg_rede",
            "mobconnect_seg_industria",
            "mobconnect_seg_agencia",
            "mobconnect_exemplo",
        }
        if "mobconnect" not in normalizado and not em_contexto:
            return None

        suporte = any(
            marca in normalizado
            for marca in (
                "ja uso",
                "sou cliente",
                "preciso de suporte",
                "problema",
                "erro",
                "falha",
                "nao consigo",
                "nao funciona",
                "bug",
            )
        )
        comercial = any(
            marca in normalizado
            for marca in (
                "quero contratar",
                "contratar",
                "proposta",
                "orcamento",
                "preco",
                "valor",
                "demonstracao",
                "falar com comercial",
                "contato comercial",
            )
        )
        descoberta = any(
            marca in normalizado
            for marca in (
                "como funciona",
                "quero entender",
                "entender",
                "curiosidade",
                "ajudaria",
                "me ajudaria",
                "serve para",
                "acompanhar",
                "quero conhecer",
                "saber mais",
                "avaliar",
            )
        )
        operacional = any(
            marca in normalizado
            for marca in (
                "roteiro",
                "sortimento",
                "pesquisa",
                "ruptura",
                "declaracao",
                "atividade",
            )
        )

        # Preserva contexto espontâneo para um eventual handoff posterior.
        if (descoberta or comercial) and len(normalizado.split()) >= 5:
            sessao.dados.setdefault("contexto_comercial", texto[:600])

        empresa = re.search(
            r"\b(?:sou|somos|trabalho)\s+d[ao]\s+([^,.;!?]{2,80})",
            texto,
            flags=re.IGNORECASE,
        )
        if empresa and not sessao.dados.get("empresa_contato"):
            valor = re.split(
                r"\s+(?:e\s+)?(?:temos|tenho|com|possui|possuo)\b",
                empresa.group(1).strip(),
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip()
            if valor:
                sessao.dados["empresa_contato"] = valor[:120]

        if not sessao.dados.get("porte"):
            quantidades = re.findall(
                r"\b(?:\d+|um|uma)\s+(?:loja(?:s)?|promotor(?:es)?)\b",
                texto,
                flags=re.IGNORECASE,
            )
            if quantidades:
                sessao.dados["porte"] = " e ".join(quantidades)[:200]

        sessao.tentativas_invalidas = 0
        if suporte:
            return self._entrar(sessao, "mobconnect")
        if comercial:
            sessao.dados["frente"] = "comercial_mobconnect"
            return self._entrar(sessao, "lead_contexto_comercial")
        if descoberta:
            return self._entrar(sessao, "mobconnect_comercial")
        if operacional:
            return self._entrar(sessao, "mobconnect")

        # Dentro de uma tela MobConnect, números e palavras como "rede" precisam
        # continuar sendo resolvidos pelas opções/sinônimos daquele estado.
        if em_contexto and "mobconnect" not in normalizado:
            return None
        return self._entrar(sessao, "mobconnect_intencao")

    def _capturar(
        self,
        sessao: Sessao,
        estado: dict[str, Any],
        campo: str,
        texto: str,
    ) -> Resposta:
        if len(texto) < 2:
            return Resposta(
                mensagens=[
                    "Preciso de um pouco mais de detalhe para seguir.",
                    self._mensagem_do_estado(estado, sessao),
                ]
            )
        sessao.dados[campo] = texto[:600]
        sessao.tentativas_invalidas = 0
        return self._entrar(sessao, estado["proximo"])

    def _resolver_opcao(self, estado: dict[str, Any], normalizado: str) -> str | None:
        opcoes: dict[str, str] = estado.get("opcoes", {})
        if not opcoes or not normalizado:
            return None
        if normalizado in opcoes:
            return normalizado

        sinonimos = {
            normalizar(gatilho): chave
            for gatilho, chave in estado.get("sinonimos", {}).items()
        }

        # tolera "opcao 2", "quero a 2", "2." etc.
        numeros = re.findall(r"\d+", normalizado)
        if len(numeros) == 1 and numeros[0] in opcoes:
            return numeros[0]

        # Comparação por palavras, não substring crua: "rede" não pode casar
        # acidentalmente com "credenciamento". O fuzzy é conservador, aceita
        # typos como promotro/fatrura e devolve None quando duas intenções
        # ficam próximas demais.
        from .nlu import resolver_gatilhos

        return resolver_gatilhos(normalizado, sinonimos, opcoes)

    def ir_para(self, sessao: Sessao, nome_estado: str) -> Resposta:
        """Entrada pública controlada em um estado conhecido do fluxo."""
        return self._entrar(sessao, nome_estado)

    def _entrar(self, sessao: Sessao, nome_estado: str) -> Resposta:
        estado = self._estados.get(nome_estado)
        if estado is None:
            logger.error("Transição para estado inexistente: %s", nome_estado)
            estado = self._estados[ESTADO_INICIAL]
            nome_estado = ESTADO_INICIAL

        sessao.estado = nome_estado
        sessao.tentativas_invalidas = 0
        # a pessoa voltou a se entender com o bot: o desvio anterior não vale mais
        sessao.dados.pop("handoff_sem_frente", None)
        sessao.dados.pop("motivo_handoff", None)

        # 'definir' grava valores fixos ao entrar no estado. Serve para registrar
        # o que a pessoa escolheu no menu (ex.: segmento), já que a escolha por
        # número não passa por 'capturar' e sem isso não chegaria ao handoff.
        fixos = estado.get("definir")
        if isinstance(fixos, dict):
            for campo, valor in fixos.items():
                sessao.dados[str(campo)] = str(valor)[:600]

        if estado.get("acao") == "transferir":
            return Resposta(
                mensagens=[self.texto("transferido", sessao)], transferir=True
            )

        # Se a conversa/IA já capturou um campo, não pergunta de novo.
        # Isso permite que uma mensagem rica pule formulários intermediários.
        campo = estado.get("capturar")
        proximo = estado.get("proximo")
        if campo and proximo and str(sessao.dados.get(str(campo)) or "").strip():
            logger.info("Campo %s já conhecido; pulando estado %s", campo, nome_estado)
            return self._entrar(sessao, str(proximo))

        return Resposta(mensagens=[self._mensagem_do_estado(estado, sessao)])

    def _mensagem_do_estado(self, estado: dict[str, Any], sessao: Sessao) -> str:
        bruto = estado.get("mensagem", "")
        if isinstance(bruto, list):
            bruto = "\n\n".join(str(parte) for parte in bruto)
        return str(bruto).format_map(self._contexto(sessao))

    def _nao_entendi(self, sessao: Sessao, estado: dict[str, Any]) -> Resposta:
        sessao.tentativas_invalidas += 1
        if sessao.tentativas_invalidas >= self._atendimento.max_tentativas_invalidas:
            # Transferência por esgotamento não é o mesmo que pedir atendente:
            # quem digitou três coisas que o bot não entendeu costuma estar
            # perdido na navegação, não com problema daquele assunto. Vai ao
            # responsável geral, sem acionar a frente.
            sessao.dados["handoff_sem_frente"] = "1"
            sessao.dados["motivo_handoff"] = (
                "o bot nao entendeu 3 mensagens seguidas (nao foi pedido de atendente)"
            )
            return Resposta(
                mensagens=[self.texto("muitas_tentativas", sessao)],
                transferir=True,
            )
        # com IA ligada, tentamos entender texto livre antes de repetir o menu
        return Resposta(usar_llm=True, mensagens=[])

    def resposta_menu_apos_erro(
        self,
        sessao: Sessao,
        texto_recebido: str = "",
    ) -> Resposta:
        """Fallback honesto: diferencia número inválido de texto livre."""
        estado = self._estados.get(sessao.estado, self._estados[ESTADO_INICIAL])
        normalizado = normalizar(texto_recebido)
        somente_numero = bool(re.fullmatch(r"(?:opcao\s+)?\d+", normalizado))
        if somente_numero:
            return Resposta(
                mensagens=[
                    self.texto("opcao_invalida", sessao),
                    self._mensagem_do_estado(estado, sessao),
                ]
            )

        orientacao = self.texto("texto_livre_nao_entendido", sessao) or (
            "Ainda não consegui identificar o ponto exato. Descreva em uma "
            "frase o que aconteceu e, se apareceu, informe o nome da tela ou "
            "a mensagem de erro."
        )
        return Resposta(mensagens=[orientacao])

    # ---------------------------------------------------------------- utilidades

    def resumo_para_atendente(self, sessao: Sessao, *, frente: str = "") -> str:
        """Bloco de texto para avisar o time interno sobre o handoff."""
        linhas = ["*Novo atendimento humano solicitado*"]
        if frente:
            linhas.append(f"Frente: {ROTULOS_FRENTE.get(frente, frente)}")
        linhas += [
            f"Contato: +{sessao.numero}",
            f"WhatsApp: {sessao.nome or 'sem nome'}",
            f"Etapa: {sessao.estado}",
        ]
        rotulos = {
            "nome_contato": "Nome informado",
            "empresa_contato": "Empresa",
            "segmento": "Segmento",
            "redes_atendidas": "Redes envolvidas",
            "porte": "Operação",
            "necessidade": "Necessidade",
            "contexto_comercial": "Contexto comercial",
            "descricao_suporte": "Descrição do problema",
            "motivo_handoff": "Motivo da transferência",
        }
        for campo, rotulo in rotulos.items():
            valor = sessao.dados.get(campo)
            if valor:
                linhas.append(f"• *{rotulo}:* {valor}")
        return "\n".join(linhas)
