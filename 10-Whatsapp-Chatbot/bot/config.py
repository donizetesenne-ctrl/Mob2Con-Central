"""Configuração central lida de variáveis de ambiente (ou do arquivo .env)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

try:  # carrega .env quando disponível; em Docker as vars já vêm do compose
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent
PROJETO_DIR = BASE_DIR.parent

if load_dotenv is not None:
    load_dotenv(PROJETO_DIR / ".env", override=False)


def _texto(chave: str, padrao: str = "") -> str:
    return os.environ.get(chave, padrao).strip()


def _booleano(chave: str, padrao: bool = False) -> bool:
    bruto = os.environ.get(chave)
    if bruto is None or not bruto.strip():
        return padrao
    return bruto.strip().lower() in {"1", "true", "t", "sim", "s", "yes", "y", "on"}


def _inteiro(chave: str, padrao: int) -> int:
    bruto = os.environ.get(chave, "").strip()
    try:
        return int(bruto)
    except (TypeError, ValueError):
        return padrao


def _lista(chave: str, padrao: str = "") -> list[str]:
    bruto = os.environ.get(chave, padrao)
    return [item.strip() for item in bruto.split(",") if item.strip()]


def _hora(chave: str, padrao: str) -> tuple[int, int]:
    """Converte 'HH:MM' em (hora, minuto). Cai no padrão se inválido."""
    bruto = _texto(chave, padrao) or padrao
    try:
        horas, _, minutos = bruto.partition(":")
        return max(0, min(23, int(horas))), max(0, min(59, int(minutos or 0)))
    except ValueError:
        horas, _, minutos = padrao.partition(":")
        return int(horas), int(minutos or 0)


def _caminho(chave: str, padrao: str) -> Path:
    bruto = _texto(chave, padrao) or padrao
    caminho = Path(bruto)
    if not caminho.is_absolute() and str(caminho) != ":memory:":
        caminho = PROJETO_DIR / caminho
    return caminho


PROMPT_SISTEMA_PADRAO = (
    "Você é o atendimento virtual da Mob2Con no WhatsApp. Responda em português "
    "do Brasil, em no máximo três parágrafos curtos, sem emoji, com no máximo "
    "uma pergunta. Se não souber, oriente a digitar 0 para o menu ou 9 para "
    "falar com uma pessoa do time."
)


def _prompt_sistema() -> str:
    """Prompt de sistema da IA, de arquivo (preferido) ou de variável.

    Uma base de conhecimento não cabe numa linha de .env: LLM_PROMPT_ARQUIVO
    aponta para um arquivo de texto ou markdown. Caminho relativo é resolvido a
    partir da raiz do projeto. Comentários HTML são removidos, para o arquivo
    poder documentar a si mesmo sem gastar tokens nem expor caminho local.
    """
    caminho_bruto = _texto("LLM_PROMPT_ARQUIVO")
    if caminho_bruto:
        caminho = Path(caminho_bruto)
        if not caminho.is_absolute():
            caminho = PROJETO_DIR / caminho
        try:
            conteudo = caminho.read_text(encoding="utf-8")
        except OSError:
            print(f"AVISO: nao foi possivel ler LLM_PROMPT_ARQUIVO em {caminho}")
        else:
            limpo = re.sub(r"<!--.*?-->", "", conteudo, flags=re.DOTALL).strip()
            if limpo:
                return limpo

    return _texto("LLM_PROMPT_SISTEMA", PROMPT_SISTEMA_PADRAO) or PROMPT_SISTEMA_PADRAO


@dataclass(frozen=True)
class ConfigEvolution:
    """Endereço e credenciais da Evolution API."""

    base_url: str
    api_key: str
    instancia: str
    token_instancia: str
    timeout: int


@dataclass(frozen=True)
class ConfigLLM:
    """Fallback de IA para mensagens fora do menu (opcional)."""

    ativo: bool
    base_url: str
    api_key: str
    modelo: str
    prompt_sistema: str
    max_tokens: int
    temperatura: float
    timeout: int
    timeout_local: int
    max_historico: int


@dataclass(frozen=True)
class ConfigManuais:
    """Busca extrativa local nos manuais Markdown."""

    ativo: bool
    diretorio: Path
    indice_path: Path
    max_resultados: int
    max_chars_resposta: int


@dataclass(frozen=True)
class ConfigAtendimento:
    """Regras de comportamento do atendimento."""

    nome_empresa: str
    fuso_horario: str
    hora_abertura: tuple[int, int]
    hora_fechamento: tuple[int, int]
    dias_uteis: frozenset[int]
    minutos_sessao: int
    minutos_pausa_humano: int
    max_tentativas_invalidas: int
    responder_grupos: bool
    numeros_bloqueados: frozenset[str]
    numeros_permitidos: frozenset[str]
    delay_digitando_ms: int


@dataclass(frozen=True)
class Config:
    """Configuração completa da aplicação."""

    evolution: ConfigEvolution
    llm: ConfigLLM
    manuais: ConfigManuais
    atendimento: ConfigAtendimento
    webhook_token: str
    caminho_fluxo: Path
    redis_url: str
    sqlite_path: Path
    nivel_log: str
    porta: int = 8000
    eventos_webhook: list[str] = field(default_factory=lambda: ["MESSAGES_UPSERT"])


def carregar_config() -> Config:
    """Monta a configuração a partir do ambiente."""
    caminho_fluxo = _texto("CAMINHO_FLUXO")

    return Config(
        evolution=ConfigEvolution(
            base_url=_texto("EVOLUTION_URL", "http://localhost:8080").rstrip("/"),
            api_key=_texto("EVOLUTION_API_KEY"),
            instancia=_texto("EVOLUTION_INSTANCIA", "mob2con"),
            token_instancia=_texto("EVOLUTION_TOKEN_INSTANCIA"),
            timeout=_inteiro("EVOLUTION_TIMEOUT", 30),
        ),
        llm=ConfigLLM(
            ativo=_booleano("LLM_ATIVO", False),
            base_url=_texto("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            api_key=_texto("LLM_API_KEY"),
            modelo=_texto("LLM_MODELO", "gpt-4o-mini"),
            prompt_sistema=_prompt_sistema(),
            max_tokens=_inteiro("LLM_MAX_TOKENS", 300),
            temperatura=float(_texto("LLM_TEMPERATURA", "0.3") or 0.3),
            timeout=_inteiro("LLM_TIMEOUT", 25),
            timeout_local=_inteiro("LLM_TIMEOUT_LOCAL", 12),
            max_historico=_inteiro("LLM_MAX_HISTORICO", 6),
        ),
        manuais=ConfigManuais(
            ativo=_booleano("MANUAIS_ATIVO", False),
            diretorio=_caminho("MANUAIS_DIRETORIO", "knowledge/mob2con/docs"),
            indice_path=_caminho("MANUAIS_INDICE", "dados/manuais.sqlite3"),
            max_resultados=_inteiro("MANUAIS_MAX_RESULTADOS", 2),
            max_chars_resposta=_inteiro("MANUAIS_MAX_CARACTERES", 1200),
        ),
        atendimento=ConfigAtendimento(
            nome_empresa=_texto("NOME_EMPRESA", "Mob2Con"),
            fuso_horario=_texto("FUSO_HORARIO", "America/Sao_Paulo"),
            hora_abertura=_hora("HORA_ABERTURA", "08:00"),
            hora_fechamento=_hora("HORA_FECHAMENTO", "18:00"),
            dias_uteis=frozenset(
                int(dia) for dia in _lista("DIAS_UTEIS", "0,1,2,3,4") if dia.isdigit()
            )
            or frozenset({0, 1, 2, 3, 4}),
            minutos_sessao=_inteiro("MINUTOS_SESSAO", 30),
            minutos_pausa_humano=_inteiro("MINUTOS_PAUSA_HUMANO", 60),
            max_tentativas_invalidas=_inteiro("MAX_TENTATIVAS_INVALIDAS", 3),
            responder_grupos=_booleano("RESPONDER_GRUPOS", False),
            numeros_bloqueados=frozenset(_lista("NUMEROS_BLOQUEADOS")),
            numeros_permitidos=frozenset(_lista("NUMEROS_PERMITIDOS")),
            delay_digitando_ms=_inteiro("DELAY_DIGITANDO_MS", 1200),
        ),
        webhook_token=_texto("WEBHOOK_TOKEN"),
        caminho_fluxo=Path(caminho_fluxo) if caminho_fluxo else BASE_DIR / "fluxo.json",
        redis_url=_texto("REDIS_URL"),
        sqlite_path=_caminho("SQLITE_PATH", "dados/chatbot.sqlite3"),
        nivel_log=_texto("NIVEL_LOG", "INFO").upper(),
        porta=_inteiro("PORTA", 8000),
        eventos_webhook=_lista("EVENTOS_WEBHOOK", "MESSAGES_UPSERT"),
    )
