"""Busca local nos manuais Mob2Con com SQLite FTS5.

A camada e totalmente local: indexa Markdown de forma incremental, remove ruido
da extracao Stonly e devolve somente trechos existentes no corpus. Nao usa API,
modelo generativo nem envia documentos para terceiros.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import logging
from pathlib import Path
import re
import sqlite3
import threading
import time
import unicodedata
from typing import Iterable, Sequence

logger = logging.getLogger(__name__)

_PARSER_VERSION = "5"
_MAX_FILE_BYTES = 5_000_000
_TARGET_CHUNK_CHARS = 850
_MIN_CHUNK_ALNUM = 30

_PAGINA_RE = re.compile(r"(?im)^##\s+P[aá]gina\s+(\d+)\s*$")
_SECAO_RE = re.compile(r"(?im)^##\s+(.+?)\s*$")
_H1_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_ORIGEM_RE = re.compile(r"(?im)^>\s*Origem:\s*`?([^`\n]+)`?\s*$")
_LINK_RE = re.compile(r"\[([^\]]+)]\([^)]*\)")
_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
_CONTROLE_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

_BOILERPLATE = (
    re.compile(r"^the explanation was created in stonly$", re.IGNORECASE),
    re.compile(r"^version\s*\d+$", re.IGNORECASE),
    re.compile(r"^page\s*\d+$", re.IGNORECASE),
    re.compile(r"^go to page\s*(?:\d+|undefined)$", re.IGNORECASE),
    re.compile(r"^(pr[oó]ximo|anterior)$", re.IGNORECASE),
    re.compile(r"^you have reached the end of this guide$", re.IGNORECASE),
    re.compile(r"^try out\s+https?://stonly\.com.*$", re.IGNORECASE),
)

_STOPWORDS = frozenset(
    {
        "a", "ao", "aos", "aquela", "aquele", "aquilo", "as", "ate", "com",
        "como", "da", "das", "de", "dela", "dele", "deles", "do", "dos", "e",
        "ela", "ele", "eles", "em", "essa", "esse", "esta", "estao", "estar",
        "este", "eu", "faz", "fazer", "foi", "me", "meu", "minha", "na", "nas",
        "no", "nos", "o", "os", "ou", "para", "pela", "pelo", "por", "qual",
        "quando", "que", "quem", "se", "sem", "ser", "seu", "sua", "tem", "ter",
        "um", "uma", "vai", "vejo", "ver", "voce", "vocês", "onde", "porque",
        "preciso", "quero", "gostaria", "ajuda", "ajudar", "duvida", "duvidas",
        "sistema", "plataforma", "mob2con",
    }
)

_STEM_PREFIXES: tuple[tuple[str, str], ...] = (
    ("document", "documento"),
    ("docume", "documento"),
    ("cadastr", "cadastro"),
    ("promot", "promotor"),
    ("visit", "visitante"),
    ("aloca", "alocacao"),
    ("vincul", "vinculo"),
    ("entrad", "entrada"),
    ("entrar", "entrada"),
    ("checkin", "entrada"),
    ("check", "entrada"),
    ("said", "saida"),
    ("checkout", "saida"),
    ("fatur", "financeiro"),
    ("cobranc", "financeiro"),
    ("finance", "financeiro"),
    ("roteir", "roteiro"),
    ("rota", "roteiro"),
    ("pesquis", "pesquisa"),
    ("sortim", "sortimento"),
    ("sincron", "sincronizacao"),
    ("bloque", "bloqueio"),
    ("imped", "bloqueio"),
    ("barrad", "bloqueio"),
    ("vencid", "vencido"),
    ("penden", "pendente"),
    ("reposi", "reposicao"),
    ("declara", "declaracao"),
    ("agend", "agendamento"),
    ("contrat", "contrato"),
    ("relator", "relatorio"),
    ("export", "exportar"),
    ("supervis", "supervisor"),
    ("fornec", "fornecedor"),
    ("industr", "fornecedor"),
    ("prestador", "fornecedor"),
    ("agenc", "agencia"),
)

_FTS_ALIASES: dict[str, tuple[str, ...]] = {
    "documento": ("document", "anexo", "arquivo"),
    "cadastro": ("cadastr", "visitante", "promotor"),
    "entrada": ("entrada", "acesso", "check-in", "impedido"),
    "saida": ("saida", "check-out"),
    "bloqueio": ("bloqueado", "impedido", "acesso"),
    "alocacao": ("alocacao", "vinculo", "rota"),
    "financeiro": ("fatura", "cobranca", "financeiro"),
    "roteiro": ("roteiro", "rota", "visita", "evento"),
    "sincronizacao": ("sincronizar", "sincronizacao", "dados"),
    "reposicao": ("repositor", "reposicao"),
}

_PERSONAS = {
    "agência": "agency",
    "agencia": "agency",
    "loja": "store",
    "rede": "retailer",
    "prestadores": "supplier",
    "prestador": "supplier",
    "fornecedores": "supplier",
    "fornecedor": "supplier",
    "portaria": "store,portaria",
    "guias indústrias agências": "agency,supplier",
    "guias industrias agencias": "agency,supplier",
}

_GENERIC_SINGLE_ROOTS = frozenset(
    {"mobcontrol", "mobconnect", "produto", "menu", "informacao"}
)


@dataclass(frozen=True)
class ResultadoManual:
    """Trecho recuperado e seus metadados públicos."""

    titulo: str
    secao: str
    pagina: int | None
    produto: str
    persona: str
    conteudo: str
    origem: str
    caminho: str
    relevancia: float

    @property
    def fonte(self) -> str:
        pagina = f", página {self.pagina}" if self.pagina else ""
        titulo = self.titulo.replace("_", " ")
        return f"{titulo}{pagina}"


@dataclass(frozen=True)
class RelatorioIndexacao:
    documentos: int
    chunks: int
    adicionados_ou_atualizados: int
    removidos: int
    inalterados: int


@dataclass(frozen=True)
class _Documento:
    caminho: str
    titulo: str
    origem: str
    produto: str
    persona: str
    digest: str
    tamanho: int
    modificado_ns: int
    chunks: tuple[tuple[str, int | None, str], ...]


def _normalizar(texto: str) -> str:
    sem_acento = "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto or "")
        if unicodedata.category(caractere) != "Mn"
    )
    limpo = re.sub(r"[^a-zA-Z0-9\s-]", " ", sem_acento.lower())
    return re.sub(r"\s+", " ", limpo).strip()


def _raiz(token: str) -> str:
    normalizado = _normalizar(token).replace("-", "")
    for prefixo, raiz in _STEM_PREFIXES:
        if normalizado.startswith(prefixo):
            return raiz
    if len(normalizado) >= 8:
        return normalizado[:7]
    return normalizado


def _termos_significativos(texto: str) -> list[str]:
    vistos: set[str] = set()
    termos: list[str] = []
    for token in _normalizar(texto).split():
        token = token.strip("-")
        if len(token) < 3 or token in _STOPWORDS or token.isdigit():
            continue
        if token not in vistos:
            vistos.add(token)
            termos.append(token)
    return termos[:200]


def _limpar_linha_tabela(linha: str) -> str | None:
    if not linha.startswith("|"):
        return None
    celulas = [re.sub(r"\s+", " ", item.strip(" *`")) for item in linha.split("|")[1:-1]]
    if not celulas or all(not item for item in celulas):
        return ""
    if all(re.fullmatch(r":?-{2,}:?", item or "-") for item in celulas):
        return ""
    if any(item.lower() == "false" for item in celulas):
        return ""
    ignorar = {
        "produto", "módulo", "modulo", "menus e submenus de navegação",
        "funcionalidades", "ações", "acoes", "check", "tenant", "owner type",
        "feature title",
    }
    uteis: list[str] = []
    for item in celulas:
        if not item or item.lower() == "true" or item.lower() in ignorar:
            continue
        if not uteis or uteis[-1] != item:
            uteis.append(item)
    return " > ".join(uteis)


def _eh_boilerplate(linha: str) -> bool:
    texto = linha.strip()
    if not texto:
        return False
    if texto.startswith("> Origem:") or texto.startswith("> Paginas:"):
        return True
    return any(padrao.fullmatch(texto) for padrao in _BOILERPLATE)


def _titulo_segmento(texto: str) -> str:
    """Primeira linha curta da página, quando funciona como cabeçalho."""
    for bruta in texto.splitlines():
        linha = _CONTROLE_RE.sub(" ", bruta).strip()
        if not linha or _eh_boilerplate(linha):
            continue
        if linha.startswith(("#", "|", "![", ">")):
            continue
        linha = _LINK_RE.sub(r"\1", linha)
        linha = _URL_RE.sub("", linha).strip(" *`")
        if (
            2 <= len(linha) <= 70
            and not re.search(r"[.!?;:]$", linha)
            and not re.match(r"^(?:[-•]|\d+[.)-])\s*", linha)
        ):
            return re.sub(r"\s+", " ", linha)
        return ""
    return ""


def _remover_titulo_duplicado(paragrafos: list[str], titulo: str) -> list[str]:
    if not titulo or not paragrafos:
        return paragrafos
    primeiro = paragrafos[0]
    if _normalizar(primeiro).startswith(_normalizar(titulo)):
        restante = primeiro[len(titulo) :].strip(" -–—:.")
        return ([restante] if restante else []) + paragrafos[1:]
    return paragrafos


def _limpar_segmento(texto: str) -> list[str]:
    texto = _CONTROLE_RE.sub(" ", texto)
    texto = re.sub(
        r"(?im)^[^\n.!?]{2,100}\r?\n\s*Go to Page\s+(?:\d+|undefined)\s*$",
        "",
        texto,
    )
    texto = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", texto)
    texto = _LINK_RE.sub(r"\1", texto)

    paragrafos: list[str] = []
    corrente: list[str] = []

    def descarregar() -> None:
        if not corrente:
            return
        paragrafo = re.sub(r"\s+", " ", " ".join(corrente)).strip()
        corrente.clear()
        if paragrafo:
            paragrafos.append(paragrafo)

    for bruta in texto.splitlines():
        linha = bruta.strip()
        if not linha:
            descarregar()
            continue
        if _eh_boilerplate(linha) or linha.startswith("!["):
            continue
        if linha.startswith("#"):
            descarregar()
            continue

        tabela = _limpar_linha_tabela(linha)
        if tabela is not None:
            descarregar()
            if tabela:
                paragrafos.append(tabela)
            continue

        linha = _URL_RE.sub("", linha).strip()
        linha = re.sub(r"^[>*]+\s*", "", linha)
        linha = re.sub(r"\s+", " ", linha).strip()
        if not linha:
            continue

        if re.match(r"^(?:[-•]|\d+[.)-])\s*", linha):
            descarregar()
            paragrafos.append(linha)
        else:
            corrente.append(linha)

    descarregar()
    return paragrafos


def _dividir_texto_longo(texto: str, limite: int) -> list[str]:
    if len(texto) <= limite:
        return [texto]
    frases = re.split(r"(?<=[.!?])\s+", texto)
    if len(frases) == 1:
        palavras = texto.split()
        partes: list[str] = []
        atual: list[str] = []
        for palavra in palavras:
            candidato = " ".join((*atual, palavra))
            if atual and len(candidato) > limite:
                partes.append(" ".join(atual))
                atual = [palavra]
            else:
                atual.append(palavra)
        if atual:
            partes.append(" ".join(atual))
        return partes

    partes = []
    atual = ""
    for frase in frases:
        candidato = f"{atual} {frase}".strip()
        if atual and len(candidato) > limite:
            partes.append(atual)
            atual = frase
        else:
            atual = candidato
    if atual:
        partes.append(atual)
    return partes


def _empacotar(paragrafos: Sequence[str]) -> tuple[str, ...]:
    unidades: list[str] = []
    for paragrafo in paragrafos:
        unidades.extend(_dividir_texto_longo(paragrafo, _TARGET_CHUNK_CHARS))

    chunks: list[str] = []
    atual: list[str] = []
    tamanho = 0
    for unidade in unidades:
        extra = len(unidade) + (2 if atual else 0)
        if atual and tamanho + extra > _TARGET_CHUNK_CHARS:
            conteudo = "\n\n".join(atual).strip()
            if sum(char.isalnum() for char in conteudo) >= _MIN_CHUNK_ALNUM:
                chunks.append(conteudo)
            atual = [unidade]
            tamanho = len(unidade)
        else:
            atual.append(unidade)
            tamanho += extra
    if atual:
        conteudo = "\n\n".join(atual).strip()
        if sum(char.isalnum() for char in conteudo) >= _MIN_CHUNK_ALNUM:
            chunks.append(conteudo)
    return tuple(chunks)


def _metadados_caminho(relativo: Path) -> tuple[str, str]:
    partes = relativo.parts
    produto = partes[0] if partes and partes[0] in {"MobControl", "MobConnect"} else ""
    persona = ""
    if len(partes) > 1:
        persona = _PERSONAS.get(partes[1].lower(), "")
    return produto, persona


def _segmentos_documento(texto: str) -> Iterable[tuple[str, int | None, str]]:
    paginas = list(_PAGINA_RE.finditer(texto))
    if paginas:
        for indice, marcador in enumerate(paginas):
            inicio = marcador.end()
            fim = paginas[indice + 1].start() if indice + 1 < len(paginas) else len(texto)
            bruto = texto[inicio:fim]
            secao = _titulo_segmento(bruto)
            paragrafos = _remover_titulo_duplicado(
                _limpar_segmento(bruto),
                secao,
            )
            if not paragrafos:
                continue
            for chunk in _empacotar(paragrafos):
                yield secao, int(marcador.group(1)), chunk
        return

    secoes = list(_SECAO_RE.finditer(texto))
    if not secoes:
        paragrafos = _limpar_segmento(texto)
        for chunk in _empacotar(paragrafos):
            yield "", None, chunk
        return

    for indice, marcador in enumerate(secoes):
        inicio = marcador.end()
        fim = secoes[indice + 1].start() if indice + 1 < len(secoes) else len(texto)
        secao = re.sub(r"\s+", " ", marcador.group(1)).strip()
        paragrafos = _limpar_segmento(texto[inicio:fim])
        for chunk in _empacotar(paragrafos):
            yield secao, None, chunk


def _ler_documento(raiz: Path, caminho: Path) -> _Documento:
    dados = caminho.read_bytes()
    if len(dados) > _MAX_FILE_BYTES:
        raise ValueError(f"manual excede {_MAX_FILE_BYTES} bytes: {caminho.name}")
    texto = dados.decode("utf-8", errors="replace")
    relativo = caminho.relative_to(raiz)
    titulo_match = _H1_RE.search(texto)
    titulo = (
        re.sub(r"\s+", " ", titulo_match.group(1)).strip()
        if titulo_match
        else caminho.stem.replace("_", " ")
    )
    origem_match = _ORIGEM_RE.search(texto)
    origem = origem_match.group(1).strip() if origem_match else caminho.name
    produto, persona = _metadados_caminho(relativo)
    chunks = tuple(_segmentos_documento(texto))
    stat = caminho.stat()
    return _Documento(
        caminho=relativo.as_posix(),
        titulo=titulo,
        origem=origem,
        produto=produto,
        persona=persona,
        digest=hashlib.sha256(dados).hexdigest(),
        tamanho=len(dados),
        modificado_ns=stat.st_mtime_ns,
        chunks=chunks,
    )


class IndiceManuais:
    """Indice FTS5 incremental e resposta extrativa local."""

    def __init__(
        self,
        diretorio: Path,
        indice_path: Path,
        *,
        max_resultados: int = 2,
        max_chars_resposta: int = 1200,
    ) -> None:
        self.diretorio = diretorio.resolve()
        self.indice_path = indice_path
        self.max_resultados = max(1, min(4, int(max_resultados)))
        self.max_chars_resposta = max(400, min(2500, int(max_chars_resposta)))
        self._trava = threading.RLock()
        self._fechado = False
        self._ultimo_relatorio: RelatorioIndexacao | None = None

        if not self.diretorio.is_dir():
            raise FileNotFoundError(f"diretorio de manuais ausente: {self.diretorio}")
        if str(indice_path) != ":memory:":
            indice_path.parent.mkdir(parents=True, exist_ok=True)
        self._conexao = sqlite3.connect(
            str(indice_path),
            timeout=10.0,
            check_same_thread=False,
        )
        self._conexao.row_factory = sqlite3.Row
        self._preparar()

    def _preparar(self) -> None:
        with self._trava, self._conexao:
            self._conexao.execute("PRAGMA busy_timeout = 10000")
            if str(self.indice_path) != ":memory:":
                self._conexao.execute("PRAGMA journal_mode = WAL")
                self._conexao.execute("PRAGMA synchronous = NORMAL")
            self._conexao.executescript(
                """
                CREATE TABLE IF NOT EXISTS manuais_meta (
                    chave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS manuais_documentos (
                    caminho TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    origem TEXT NOT NULL,
                    produto TEXT NOT NULL,
                    persona TEXT NOT NULL,
                    digest TEXT NOT NULL,
                    tamanho INTEGER NOT NULL,
                    modificado_ns INTEGER NOT NULL,
                    chunks INTEGER NOT NULL,
                    indexado_em REAL NOT NULL
                );

                CREATE VIRTUAL TABLE IF NOT EXISTS manuais_fts USING fts5(
                    caminho UNINDEXED,
                    titulo,
                    secao,
                    pagina UNINDEXED,
                    produto,
                    persona,
                    conteudo,
                    tokenize = 'unicode61 remove_diacritics 2'
                );
                """
            )
            versao = self._conexao.execute(
                "SELECT valor FROM manuais_meta WHERE chave = 'parser_version'"
            ).fetchone()
            if versao is None or str(versao["valor"]) != _PARSER_VERSION:
                self._conexao.execute("DELETE FROM manuais_fts")
                self._conexao.execute("DELETE FROM manuais_documentos")
                self._conexao.execute(
                    """
                    INSERT INTO manuais_meta(chave, valor)
                    VALUES ('parser_version', ?)
                    ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor
                    """,
                    (_PARSER_VERSION,),
                )

    def indexar(self) -> RelatorioIndexacao:
        """Sincroniza arquivos novos, alterados e removidos por SHA-256."""
        arquivos = sorted(
            caminho
            for caminho in self.diretorio.rglob("*.md")
            if caminho.is_file() and not caminho.is_symlink()
        )
        atuais = {caminho.relative_to(self.diretorio).as_posix(): caminho for caminho in arquivos}

        with self._trava:
            self._garantir_aberto()
            existentes = {
                str(linha["caminho"]): dict(linha)
                for linha in self._conexao.execute(
                    "SELECT caminho, digest, chunks FROM manuais_documentos"
                ).fetchall()
            }
            total_declarado = sum(int(item["chunks"]) for item in existentes.values())
            total_fts = int(
                self._conexao.execute("SELECT COUNT(*) FROM manuais_fts").fetchone()[0]
            )
            if total_declarado != total_fts:
                logger.warning(
                    "Indice de manuais inconsistente (%s != %s); reconstruindo.",
                    total_declarado,
                    total_fts,
                )
                with self._conexao:
                    self._conexao.execute("DELETE FROM manuais_fts")
                    self._conexao.execute("DELETE FROM manuais_documentos")
                existentes = {}

            removidos = 0
            atualizados = 0
            inalterados = 0
            with self._conexao:
                for relativo in sorted(set(existentes) - set(atuais)):
                    self._conexao.execute(
                        "DELETE FROM manuais_fts WHERE caminho = ?", (relativo,)
                    )
                    self._conexao.execute(
                        "DELETE FROM manuais_documentos WHERE caminho = ?", (relativo,)
                    )
                    removidos += 1

                for relativo, caminho in atuais.items():
                    dados = caminho.read_bytes()
                    digest = hashlib.sha256(dados).hexdigest()
                    anterior = existentes.get(relativo)
                    if anterior and str(anterior["digest"]) == digest:
                        inalterados += 1
                        continue

                    documento = _ler_documento(self.diretorio, caminho)
                    self._conexao.execute(
                        "DELETE FROM manuais_fts WHERE caminho = ?", (relativo,)
                    )
                    for secao, pagina, conteudo in documento.chunks:
                        self._conexao.execute(
                            """
                            INSERT INTO manuais_fts(
                                caminho, titulo, secao, pagina,
                                produto, persona, conteudo
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                documento.caminho,
                                documento.titulo,
                                secao,
                                "" if pagina is None else str(pagina),
                                documento.produto,
                                documento.persona,
                                conteudo,
                            ),
                        )
                    self._conexao.execute(
                        """
                        INSERT INTO manuais_documentos(
                            caminho, titulo, origem, produto, persona, digest,
                            tamanho, modificado_ns, chunks, indexado_em
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(caminho) DO UPDATE SET
                            titulo = excluded.titulo,
                            origem = excluded.origem,
                            produto = excluded.produto,
                            persona = excluded.persona,
                            digest = excluded.digest,
                            tamanho = excluded.tamanho,
                            modificado_ns = excluded.modificado_ns,
                            chunks = excluded.chunks,
                            indexado_em = excluded.indexado_em
                        """,
                        (
                            documento.caminho,
                            documento.titulo,
                            documento.origem,
                            documento.produto,
                            documento.persona,
                            documento.digest,
                            documento.tamanho,
                            documento.modificado_ns,
                            len(documento.chunks),
                            time.time(),
                        ),
                    )
                    atualizados += 1

            relatorio = self._relatorio(atualizados, removidos, inalterados)
            self._ultimo_relatorio = relatorio
            logger.info(
                "Manuais indexados | documentos=%s | chunks=%s | atualizados=%s | removidos=%s",
                relatorio.documentos,
                relatorio.chunks,
                relatorio.adicionados_ou_atualizados,
                relatorio.removidos,
            )
            return relatorio

    def _relatorio(
        self, atualizados: int = 0, removidos: int = 0, inalterados: int = 0
    ) -> RelatorioIndexacao:
        documentos = int(
            self._conexao.execute(
                "SELECT COUNT(*) FROM manuais_documentos"
            ).fetchone()[0]
        )
        chunks = int(self._conexao.execute("SELECT COUNT(*) FROM manuais_fts").fetchone()[0])
        return RelatorioIndexacao(
            documentos=documentos,
            chunks=chunks,
            adicionados_ou_atualizados=atualizados,
            removidos=removidos,
            inalterados=inalterados,
        )

    def status(self) -> dict[str, int | bool]:
        with self._trava:
            self._garantir_aberto()
            relatorio = self._relatorio()
            return {
                "ativo": True,
                "documentos": relatorio.documentos,
                "chunks": relatorio.chunks,
                "fts5": True,
            }

    def buscar(
        self,
        pergunta: str,
        *,
        limite: int | None = None,
        persona: str = "",
    ) -> list[ResultadoManual]:
        """Busca e reordena resultados; devolve vazio quando relevancia e fraca."""
        termos = _termos_significativos(pergunta)[:10]
        if not termos:
            return []
        raizes_consulta = {_raiz(termo) for termo in termos if _raiz(termo)}
        if not raizes_consulta:
            return []

        termos_fts: list[str] = []
        for termo in termos:
            base = _normalizar(termo).replace("-", "")
            if len(base) >= 7:
                base = base[:6]
            if base and base not in termos_fts:
                termos_fts.append(base)
            for alias in _FTS_ALIASES.get(_raiz(termo), ()):
                alias_limpo = _normalizar(alias).replace("-", "")
                if len(alias_limpo) >= 7:
                    alias_limpo = alias_limpo[:6]
                if alias_limpo and alias_limpo not in termos_fts:
                    termos_fts.append(alias_limpo)
        termos_fts = termos_fts[:16]
        consulta_fts = " OR ".join(f'"{termo}"*' for termo in termos_fts)
        limite_final = max(1, min(4, int(limite or self.max_resultados)))
        limite_sql = max(20, limite_final * 10)

        with self._trava:
            self._garantir_aberto()
            try:
                linhas = self._conexao.execute(
                    """
                    SELECT
                        f.caminho, f.titulo, f.secao, f.pagina,
                        f.produto, f.persona, f.conteudo,
                        d.origem,
                        bm25(manuais_fts, 0.0, 5.0, 4.0, 0.0, 1.0, 2.0, 1.0)
                            AS bm25_score
                    FROM manuais_fts AS f
                    JOIN manuais_documentos AS d ON d.caminho = f.caminho
                    WHERE manuais_fts MATCH ?
                    ORDER BY bm25_score
                    LIMIT ?
                    """,
                    (consulta_fts, limite_sql),
                ).fetchall()
            except sqlite3.OperationalError as erro:
                logger.warning("Consulta FTS invalida foi descartada: %s", erro)
                return []

        persona_limpa = _normalizar(persona)
        produto_consulta = ""
        pergunta_normalizada = _normalizar(pergunta)
        if "mobconnect" in pergunta_normalizada:
            produto_consulta = "MobConnect"
        elif "mobcontrol" in pergunta_normalizada:
            produto_consulta = "MobControl"

        candidatos: list[ResultadoManual] = []
        for linha in linhas:
            corpo = f"{linha['titulo']} {linha['secao']} {linha['conteudo']}"
            raizes_corpo = {_raiz(token) for token in _termos_significativos(corpo)}
            raizes_cabecalho = {
                _raiz(token)
                for token in _termos_significativos(
                    f"{linha['titulo']} {linha['secao']}"
                )
            }
            correspondencias = raizes_consulta & raizes_corpo
            cabecalho = raizes_consulta & raizes_cabecalho
            total_raizes = len(raizes_consulta)

            if total_raizes == 1:
                unica = next(iter(raizes_consulta))
                if (
                    unica in _GENERIC_SINGLE_ROOTS
                    or len(unica) < 5
                    or unica not in raizes_corpo
                ):
                    continue
            else:
                minimo = min(2, total_raizes)
                if len(correspondencias) < minimo:
                    continue

            cobertura = len(correspondencias) / total_raizes
            if total_raizes > 2 and cobertura < 0.34:
                continue

            relevancia = len(correspondencias) * 3.0 + len(cabecalho) * 2.0
            relevancia += min(3.0, max(0.0, -float(linha["bm25_score"])))
            persona_resultado = _normalizar(str(linha["persona"]))
            if persona_limpa and persona_limpa in persona_resultado:
                relevancia += 3.0
            titulo_normalizado = _normalizar(str(linha["titulo"]))
            if any(
                marcador in titulo_normalizado
                for marcador in ("o modulo", "o menu", "onboard")
            ):
                relevancia -= 3.0
            if not str(linha["produto"]):
                # As duas planilhas são catálogo de capacidades. Servem como
                # fallback, mas não devem vencer um manual operacional que
                # explica tela, regra e procedimento.
                relevancia -= 5.0
            if produto_consulta:
                if str(linha["produto"]) == produto_consulta:
                    relevancia += 2.0
                elif linha["produto"]:
                    relevancia -= 1.0

            pagina_texto = str(linha["pagina"] or "").strip()
            candidatos.append(
                ResultadoManual(
                    titulo=str(linha["titulo"]),
                    secao=str(linha["secao"]),
                    pagina=int(pagina_texto) if pagina_texto.isdigit() else None,
                    produto=str(linha["produto"]),
                    persona=str(linha["persona"]),
                    conteudo=str(linha["conteudo"]),
                    origem=str(linha["origem"]),
                    caminho=str(linha["caminho"]),
                    relevancia=round(relevancia, 4),
                )
            )

        candidatos.sort(
            key=lambda item: (
                bool(item.produto),
                item.relevancia,
                -(item.pagina if item.pagina is not None else 9999),
            ),
            reverse=True,
        )
        resultados: list[ResultadoManual] = []
        vistos: set[str] = set()
        for candidato in candidatos:
            chave = _normalizar(candidato.conteudo)[:350]
            if not chave or chave in vistos:
                continue
            vistos.add(chave)
            resultados.append(candidato)
            if len(resultados) >= limite_final:
                break
        return resultados

    def responder(
        self,
        pergunta: str,
        *,
        persona: str = "",
    ) -> str | None:
        """Monta resposta curta apenas com sentencas recuperadas do corpus."""
        resultados = self.buscar(pergunta, persona=persona)
        if not resultados:
            return None

        prefixo = "Encontrei esta orientação nos manuais da Mob2Con."
        normalizada = _normalizar(pergunta)
        termos_conta = {"meu", "minha", "status", "situacao", "pendente"}
        if termos_conta & set(normalizada.split()):
            prefixo = (
                "Não consigo consultar sua conta daqui, mas o manual orienta "
                "este caminho."
            )

        blocos = [prefixo]
        fontes: list[str] = []
        espaco_restante = self.max_chars_resposta - len(prefixo) - 120
        for resultado in resultados:
            trecho = self._extrair_trecho(pergunta, resultado.conteudo)
            if not trecho:
                continue
            if len(trecho) > espaco_restante:
                trecho = trecho[: max(0, espaco_restante - 1)].rsplit(" ", 1)[0] + "…"
            if trecho:
                blocos.append(trecho)
                espaco_restante -= len(trecho) + 2
            if resultado.fonte not in fontes:
                fontes.append(resultado.fonte)
            if espaco_restante < 180:
                break

        if len(blocos) == 1:
            return None
        fonte = "; ".join(fontes[:2])
        blocos.append(f"*Fonte:* {fonte}.")
        return "\n\n".join(blocos)

    @staticmethod
    def _extrair_trecho(pergunta: str, conteudo: str) -> str:
        if len(conteudo) <= 650:
            return conteudo.strip()
        raizes = {_raiz(item) for item in _termos_significativos(pergunta)}
        partes = [
            item.strip()
            for item in re.split(r"(?<=[.!?])\s+|\n+", conteudo)
            if item.strip()
        ]
        pontuadas: list[tuple[int, int, str]] = []
        for indice, parte in enumerate(partes):
            raizes_parte = {_raiz(item) for item in _termos_significativos(parte)}
            pontuadas.append((len(raizes & raizes_parte), indice, parte))
        escolhidas = sorted(
            pontuadas,
            key=lambda item: (-item[0], item[1]),
        )[:3]
        escolhidas.sort(key=lambda item: item[1])
        trecho = " ".join(item[2] for item in escolhidas).strip()
        return trecho[:800].rsplit(" ", 1)[0] if len(trecho) > 800 else trecho

    def fechar(self) -> None:
        with self._trava:
            if not self._fechado:
                self._conexao.close()
                self._fechado = True

    def _garantir_aberto(self) -> None:
        if self._fechado:
            raise RuntimeError("Indice de manuais ja foi fechado.")
