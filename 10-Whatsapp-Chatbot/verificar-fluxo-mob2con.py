"""Verificacao do fluxo Mob2Con. Rode antes de subir o bot.

    python verificar-fluxo-mob2con.py

Sai com codigo 1 se algo falhar, entao serve em pipeline. Cobre o que da para
checar sem WhatsApp:
  1. os dois fluxos carregam e passam pela validacao do motor
  2. conversas simuladas chegam onde deveriam
  3. o segmento escolhido no menu chega ao resumo do handoff
  4. nenhuma mensagem ao cliente tem emoji
  5. o prompt de sistema vem do arquivo, sem comentario HTML
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from bot.config import ConfigAtendimento, _prompt_sistema  # noqa: E402
from bot.fluxo import ErroFluxo, MotorFluxo  # noqa: E402
from bot.sessao import Sessao  # noqa: E402

ATENDIMENTO = ConfigAtendimento(
    nome_empresa="Mob2Con",
    fuso_horario="America/Sao_Paulo",
    hora_abertura=(8, 0),
    hora_fechamento=(17, 0),
    dias_uteis=frozenset({0, 1, 2, 3, 4}),
    minutos_sessao=30,
    minutos_pausa_humano=60,
    max_tentativas_invalidas=3,
    responder_grupos=False,
    numeros_bloqueados=frozenset(),
    numeros_permitidos=frozenset(),
    delay_digitando_ms=1200,
)

falhas: list[str] = []
oks: list[str] = []


def checar(condicao: bool, rotulo: str, detalhe: str = "") -> None:
    if condicao:
        oks.append(rotulo)
    else:
        falhas.append(f"{rotulo}{(' -> ' + detalhe) if detalhe else ''}")


def tem_emoji(texto: str) -> list[str]:
    achados = []
    for ch in texto:
        cp = ord(ch)
        if (
            0x1F300 <= cp <= 0x1FAFF
            or 0x2600 <= cp <= 0x27BF
            or cp in (0x2B50, 0x2B55, 0xFE0F, 0x203C, 0x2049)
            or 0x1F000 <= cp <= 0x1F2FF
        ):
            achados.append(f"U+{cp:04X} {ch}")
    return achados


# ------------------------------------------------------------ 1. carga
print("=" * 62)
print("1. CARGA E VALIDACAO DOS FLUXOS")
print("=" * 62)

motores = {}
for rotulo, arquivo in (
    ("mob2con", "bot/fluxo-mob2con.json"),
    ("bi (regressao)", "bot/fluxo.json"),
):
    try:
        motores[rotulo] = MotorFluxo(RAIZ / arquivo, ATENDIMENTO)
        print(f"  OK    {rotulo}: carregou e validou")
        oks.append(f"carga {rotulo}")
    except ErroFluxo as erro:
        print(f"  FALHA {rotulo}: {erro}")
        falhas.append(f"carga {rotulo} -> {erro}")

motor = motores.get("mob2con")
if motor is None:
    print("\nFluxo Mob2Con nao carregou; interrompendo.")
    sys.exit(1)

definicao = json.loads((RAIZ / "bot/fluxo-mob2con.json").read_text(encoding="utf-8"))
estados = definicao["estados"]
print(f"  {len(estados)} estados, {len(definicao['atalhos_globais'])} atalhos globais")


# ------------------------------------------------------------ 2. conversas
print()
print("=" * 62)
print("2. CONVERSAS SIMULADAS")
print("=" * 62)


def conversar(titulo: str, entradas: list[str], mostrar: bool = False):
    sessao = Sessao(numero="5519999999999", nome="Teste")
    resposta = motor.iniciar(sessao, dentro_do_horario=True)
    trilha = [sessao.estado]
    for entrada in entradas:
        resposta = motor.processar(sessao, entrada)
        trilha.append(sessao.estado)
    print(f"\n  {titulo}")
    print(f"    entradas: {entradas}")
    print(f"    trilha:   {' -> '.join(trilha)}")
    if mostrar:
        for msg in resposta.mensagens:
            print(f"    | {msg[:150]}")
    return sessao, resposta


# lead de industria: explica primeiro e coleta contexto em uma mensagem
contexto_lead = (
    "Acme Alimentos. Atendemos Carrefour e Pao de Acucar, "
    "300 lojas em SP e MG. Queremos evidência de execução."
)
sessao, resposta = conversar(
    "Lead industria sem formulario sequencial",
    ["5", "2", "1", contexto_lead],
)
checar(resposta.transferir, "lead industria transfere apos contexto unico")
checar(
    sessao.dados.get("segmento") == "Indústria ou fornecedor",
    "segmento gravado pelo menu",
    f"veio {sessao.dados.get('segmento')!r}",
)
checar(
    sessao.dados.get("contexto_comercial") == contexto_lead,
    "contexto comercial preservado integralmente",
)
resumo = motor.resumo_para_atendente(sessao)
for campo in ("Segmento", "Contexto comercial"):
    checar(campo in resumo, f"handoff traz {campo}")
checar("Acme Alimentos" in resumo, "handoff leva empresa dentro do contexto")
checar("300 lojas" in resumo, "handoff leva porte dentro do contexto")
print("\n    --- resumo entregue ao time ---")
for linha in resumo.splitlines():
    print(f"    | {linha}")

# curiosidade sobre MobConnect precisa ensinar antes de vender
sessao, resposta = conversar(
    "Curiosidade sobre MobConnect",
    ["como funciona mobconnect"],
)
texto_mobconnect = " ".join(resposta.mensagens).lower()
checar(sessao.estado == "mobconnect_comercial", "curiosidade entra na explicacao")
checar("planejar" in texto_mobconnect, "explicacao cobre planejamento")
checar("mobcontrol" in texto_mobconnect, "explicacao diferencia MobControl")
checar("qual é o seu nome" not in texto_mobconnect, "curiosidade nao vira formulario")

# texto livre cai no sinonimo certo, e promotor recebe o caminho dele
sessao, resposta = conversar(
    "Promotor barrado, texto livre + persona promotor",
    ["meu promotor nao consegue entrar na loja", "3"],
    mostrar=True,
)
checar(sessao.estado == "acesso_promotor", "texto livre roteia para acesso e persona promotor")
texto_promotor = " ".join(resposta.mensagens).lower()
checar(
    "agência ou o fornecedor que te emprega" in texto_promotor,
    "promotor e mandado ao empregador, nao a uma tela que ele nao tem",
)
checar(
    "documentos pendentes" not in texto_promotor,
    "nao manda o promotor abrir Documentos Pendentes",
)

# gestor recebe o checklist de 3 passos
sessao, resposta = conversar("Gestor com promotor barrado", ["1", "1"], mostrar=True)
gestor = " ".join(resposta.mensagens).lower()
for termo in ("documentos pendentes", "vermelho", "amarelo", "alocação", "bloquear acesso"):
    checar(termo in gestor, f"checklist do gestor cita {termo}")

# fatura entrega o canal do Financeiro
sessao, resposta = conversar("Fatura por texto livre", ["quero ver minha fatura"])
fatura = " ".join(resposta.mensagens)
checar(sessao.estado == "financeiro", "sinonimo de fatura roteia ao financeiro")
checar("99886-8868" in fatura, "financeiro entrega o canal proprio")
checar("cr@mob2con.com.br" in fatura, "financeiro entrega o e-mail")

# tres tentativas invalidas transferem
sessao = Sessao(numero="5519999999999")
motor.iniciar(sessao, dentro_do_horario=True)
ultima = None
for _ in range(3):
    ultima = motor.processar(sessao, "xyzabc sem sentido nenhum")
checar(ultima.transferir, "tres tentativas invalidas transferem ao humano")

# atalho global 9 a qualquer momento
sessao = Sessao(numero="5519999999999")
motor.iniciar(sessao, dentro_do_horario=True)
motor.processar(sessao, "2")
r9 = motor.processar(sessao, "9")
checar(r9.transferir, "atalho 9 transfere de qualquer estado")

# fora de horario avisa a janela humana
sessao = Sessao(numero="5519999999999")
fora = motor.iniciar(sessao, dentro_do_horario=False)
txt_fora = " ".join(fora.mensagens)
checar("17:00" in txt_fora, "fora de horario informa o fechamento configurado")
checar("qualquer hora" in txt_fora, "fora de horario separa robo de time humano")


# ------------------------------------------------------------ 3. tom
print()
print("=" * 62)
print("3. REGRAS DE TOM NO FLUXO")
print("=" * 62)

todos_textos: list[tuple[str, str]] = []
for chave, valor in definicao["textos"].items():
    todos_textos.append((f"textos.{chave}", valor))
for nome, estado in estados.items():
    if "mensagem" in estado:
        todos_textos.append((f"estados.{nome}", estado["mensagem"]))

com_emoji = [(o, tem_emoji(t)) for o, t in todos_textos if tem_emoji(t)]
checar(not com_emoji, "nenhuma mensagem tem emoji", str(com_emoji[:3]))
print(f"  mensagens inspecionadas: {len(todos_textos)}")
print(f"  com emoji: {len(com_emoji)}")

termina_dois_pontos = [o for o, t in todos_textos if t.rstrip().endswith(":")]
checar(not termina_dois_pontos, "nenhuma mensagem termina em dois-pontos", str(termina_dois_pontos))

proibidas = ("preço", "preco", "valor do", "quanto custa", "sla", "prazo de entrega")
com_preco = [o for o, t in todos_textos for p in proibidas if p in t.lower()]
checar(not com_preco, "nenhuma mensagem cita preco ou SLA", str(com_preco))

longas = [(o, len(t)) for o, t in todos_textos if len(t) > 900]
checar(not longas, "nenhuma mensagem passa de 900 caracteres", str(longas))

# uma pergunta por mensagem (ignorando as linhas de menu numerado)
muitas_perguntas = []
for origem, texto in todos_textos:
    corpo = "\n".join(
        linha for linha in texto.splitlines() if not linha.strip().startswith("*")
    )
    if corpo.count("?") > 1:
        muitas_perguntas.append((origem, corpo.count("?")))
checar(not muitas_perguntas, "no maximo uma pergunta por mensagem", str(muitas_perguntas))


# ------------------------------------------------------------ 4. prompt
print()
print("=" * 62)
print("4. PROMPT DE SISTEMA POR ARQUIVO")
print("=" * 62)

os.environ["LLM_PROMPT_ARQUIVO"] = "bot/conhecimento-mob2con.md"
prompt = _prompt_sistema()
print(f"  tamanho: {len(prompt)} caracteres")
checar(len(prompt) > 4000, "prompt carregou do arquivo", f"{len(prompt)} chars")
checar("<!--" not in prompt, "comentario HTML removido do prompt")
checar("C:\\Users" not in prompt, "caminho local nao vaza para o prompt")
checar("MobControl" in prompt and "supplier" in prompt, "prompt tem o conteudo Mob2Con")
checar("Power BI" not in prompt, "prompt nao mistura o negocio de BI")
checar("8h às 17h" in prompt, "prompt informa o horario humano correto")

os.environ["LLM_PROMPT_ARQUIVO"] = "bot/nao-existe.md"
fallback = _prompt_sistema()
checar(len(fallback) < 1000, "arquivo ausente cai no padrao sem quebrar")


# ------------------------------------------------------------ 5. .env real
print()
print("=" * 62)
print("5. COERENCIA DO .env REAL (nenhum segredo e impresso)")
print("=" * 62)

os.environ.pop("LLM_PROMPT_ARQUIVO", None)
for chave in list(os.environ):
    if chave.startswith(("LLM_", "MANUAIS_", "CAMINHO_", "HORA_")):
        os.environ.pop(chave, None)

if not (RAIZ / ".env").exists():
    print("  .env ausente; secao ignorada")
else:
    import importlib

    import bot.config as modulo_config

    importlib.reload(modulo_config)
    cfg = modulo_config.carregar_config()

    from bot.llm import ClienteLLM

    cliente = ClienteLLM(cfg.llm)

    print(f"  fluxo em uso:      {cfg.caminho_fluxo.name}")
    print(f"  LLM_ATIVO:         {cfg.llm.ativo}")
    print(f"  IA operante:       {cliente.ativo}  (exige chave ou endpoint local)")
    documentos_manuais = (
        len(list(cfg.manuais.diretorio.rglob("*.md")))
        if cfg.manuais.diretorio.is_dir()
        else 0
    )
    print(f"  prompt carregado:  {len(cfg.llm.prompt_sistema)} caracteres")
    print(
        f"  manuais locais:    ativo={cfg.manuais.ativo}, "
        f"documentos={documentos_manuais}"
    )
    print(f"  horario humano:    %02d:%02d as %02d:%02d" % (
        *cfg.atendimento.hora_abertura, *cfg.atendimento.hora_fechamento))
    print(f"  modo teste:        {'sim, ' + str(len(cfg.atendimento.numeros_permitidos)) + ' numero(s)' if cfg.atendimento.numeros_permitidos else 'nao, responde qualquer numero'}")

    checar(
        cfg.caminho_fluxo.name == "fluxo-mob2con.json",
        "'.env' aponta para o fluxo Mob2Con",
        f"aponta para {cfg.caminho_fluxo.name}",
    )
    checar(
        MotorFluxo(cfg.caminho_fluxo, ATENDIMENTO) is not None,
        "fluxo apontado pelo .env carrega",
    )
    checar(
        len(cfg.llm.prompt_sistema) > 4000,
        "'.env' carrega a base Mob2Con no prompt",
        f"{len(cfg.llm.prompt_sistema)} chars",
    )
    checar(
        "MobControl" in cfg.llm.prompt_sistema,
        "prompt vindo do .env tem conteudo Mob2Con",
    )
    checar(
        cfg.manuais.ativo,
        "busca local nos manuais esta ativa",
        "MANUAIS_ATIVO=false",
    )
    checar(
        documentos_manuais == 60,
        "corpus local contem os 60 manuais",
        f"encontrados {documentos_manuais}",
    )
    checar(
        cfg.atendimento.hora_fechamento == (17, 0),
        "horario de fechamento e 17:00",
        str(cfg.atendimento.hora_fechamento),
    )
    if cfg.llm.ativo and not cliente.ativo:
        print()
        print("  AVISO: LLM_ATIVO=true mas a IA nao vai responder — falta")
        print("         LLM_API_KEY (ou um LLM_BASE_URL local). O bot segue")
        print("         funcionando com menu e busca local nos manuais.")


# ------------------------------------------------------------ 6. os tres defeitos
print()
print("=" * 62)
print("6. CORRECOES DE COMPORTAMENTO")
print("=" * 62)

# 6a. classificacao de saudacao pura
casos_saudacao = [
    ("oi", True),
    ("Bom dia", True),
    ("olá, tudo bem?", True),
    ("preciso de ajuda", True),
    ("boa tarde, pode me ajudar", True),
    ("", True),
    ("meu promotor nao consegue entrar na loja", False),
    ("quero ver minha fatura", False),
    ("como cadastro um promotor novo", False),
    ("1", False),
    ("9", False),
    ("bom dia, meu promotor foi barrado na portaria", False),
]
erros_saudacao = [
    (t, esperado, motor.apenas_saudacao(t))
    for t, esperado in casos_saudacao
    if motor.apenas_saudacao(t) != esperado
]
checar(not erros_saudacao, "classificacao de saudacao pura", str(erros_saudacao))
print(f"  casos de saudacao conferidos: {len(casos_saudacao)}")

# 6b/6c. atender() de verdade, com envio capturado
import asyncio  # noqa: E402
import dataclasses  # noqa: E402

import bot.config as cfg_mod  # noqa: E402
from bot.main import Aplicacao  # noqa: E402
from bot.mensagem import MensagemRecebida  # noqa: E402

os.environ["NUMERO_NOTIFICACAO"] = ""
config_real = cfg_mod.carregar_config()
base = dataclasses.replace(
    config_real,
    sqlite_path=Path(":memory:"),
    llm=dataclasses.replace(config_real.llm, ativo=False, api_key=""),
)
cfg_ia = dataclasses.replace(
    base,
    llm=dataclasses.replace(
        base.llm,
        ativo=True,
        base_url="https://teste-invalido.local/v1",
        api_key="chave-de-teste",
    ),
)


def msg(texto: str, numero: str, ident: str) -> MensagemRecebida:
    return MensagemRecebida(
        id=ident,
        jid=f"{numero}@s.whatsapp.net",
        numero=numero,
        nome="Prospere",
        texto=texto,
        de_mim=False,
        grupo=False,
        tem_midia=False,
        instancia="mob2con",
        tipo="conversation",
    )


async def cenarios():
    app = Aplicacao(cfg_ia)
    enviados: list[list[str]] = []

    async def capturar(_numero, mensagens):
        enviados.append(list(mensagens))

    async def nao_notificar(_sessao):
        return None

    app._enviar = capturar
    app._notificar_time = nao_notificar
    app.llm.responder = lambda pergunta, historico=None: _resposta_ia()

    async def _resposta_ia():
        return "Provavelmente é documentação: em Documentos Pendentes, vermelho é vencido."

    resultados = {}

    # primeira mensagem com problema descrito
    enviados.clear()
    await app.atender(msg("meu promotor nao consegue entrar na loja", "5511000000001", "m1"))
    resultados["primeira_com_conteudo"] = list(enviados)
    s = await app.sessoes.obter("5511000000001")
    resultados["estado_apos_conteudo"] = s.estado if s else None

    # primeira mensagem que e so saudacao
    enviados.clear()
    await app.atender(msg("bom dia", "5511000000002", "m2"))
    resultados["primeira_saudacao"] = list(enviados)

    # saudacao com erro de digitacao, IA DESLIGADA: nao pode virar "nao
    # identifiquei essa opcao" na primeira mensagem da conversa
    app_sem_ia = Aplicacao(base)
    enviados_sem_ia: list[list[str]] = []

    async def capturar_sem_ia(_numero, mensagens):
        enviados_sem_ia.append(list(mensagens))

    app_sem_ia._enviar = capturar_sem_ia
    app_sem_ia._notificar_time = nao_notificar
    await app_sem_ia.atender(msg("Boom dia", "5511000000009", "m9"))
    resultados["saudacao_com_typo"] = list(enviados_sem_ia)
    s9 = await app_sem_ia.sessoes.obter("5511000000009")
    resultados["typo_tentativas"] = s9.tentativas_invalidas if s9 else -1
    resultados["typo_estado"] = s9.estado if s9 else None
    await app_sem_ia.encerrar()

    # quatro mensagens livres seguidas, todas respondidas pela IA.
    # Texto sem sinonimo do menu e sem digito, senao casaria com uma opcao.
    enviados.clear()
    for rotulo in ("alpha", "beta", "gama", "delta"):
        await app.atender(
            msg(f"explique o funcionamento geral por favor caso {rotulo}",
                "5511000000003", f"m3{rotulo}")
        )
    s3 = await app.sessoes.obter("5511000000003")
    resultados["livre_4_turnos"] = list(enviados)
    resultados["pausada_apos_livre"] = bool(s3 and s3.pausada)
    resultados["tentativas"] = s3.tentativas_invalidas if s3 else -1

    try:
        await app.encerrar()
    except Exception:  # noqa: BLE001
        pass
    return resultados


res = asyncio.run(cenarios())

# 6b. primeira mensagem lida
primeira = res["primeira_com_conteudo"]
achatado = [m for lote in primeira for m in lote]
checar(
    res["estado_apos_conteudo"] == "acesso_quem",
    "primeira mensagem com problema vai direto ao assunto",
    f"estado={res['estado_apos_conteudo']}",
)
checar(
    any("atendimento virtual" in m for m in achatado),
    "saudacao preservada na primeira resposta",
)
checar(
    not any("Promotor não consegue entrar na loja" in m for m in achatado),
    "menu generico NAO e exibido para quem ja descreveu o problema",
)
print(f"  primeira com conteudo -> {len(achatado)} mensagem(ns), estado {res['estado_apos_conteudo']}")

saud = [m for lote in res["primeira_saudacao"] for m in lote]
checar(
    any("Promotor não consegue entrar na loja" in m for m in saud),
    "quem so cumprimenta continua recebendo o menu",
)

typo = [m for lote in res["saudacao_com_typo"] for m in lote]
checar(
    not any("identifiquei" in m.lower() for m in typo),
    "saudacao com typo na 1a mensagem NAO devolve 'nao identifiquei a opcao'",
    str(typo[:1]),
)
checar(
    any("Promotor não consegue entrar na loja" in m for m in typo),
    "saudacao com typo recebe o menu normalmente",
)
checar(
    any("atendimento virtual" in m for m in typo),
    "saudacao com typo recebe a saudacao uma vez",
)
checar(
    sum(1 for m in typo if "atendimento virtual" in m) == 1,
    "saudacao nao vem duplicada no caso do typo",
)
checar(
    res["typo_tentativas"] == 0,
    "saudacao com typo nao gasta tentativa",
    f"tentativas={res['typo_tentativas']}",
)
print(f"  'Boom dia' sem IA -> {len(typo)} mensagem(ns), estado {res['typo_estado']}, tentativas {res['typo_tentativas']}")

# 6c. texto livre nao e punido, e a dica aparece uma vez
livres = [m for lote in res["livre_4_turnos"] for m in lote]
checar(
    not res["pausada_apos_livre"],
    "quatro trocas em texto livre NAO transferem ao humano",
    f"pausada={res['pausada_apos_livre']}",
)
checar(
    res["tentativas"] == 0,
    "contador de tentativas zera em resposta bem-sucedida",
    f"tentativas={res['tentativas']}",
)
dicas = [m for m in livres if "digite *9*" in m.lower()]
checar(len(dicas) == 1, "dica de humano aparece uma unica vez", f"{len(dicas)} vezes")
checar(
    not any("Digite *0* para ver o menu" in m for m in livres),
    "rodape fixo antigo foi removido",
)
print(f"  4 turnos livres -> {len(livres)} mensagem(ns), {len(dicas)} dica(s), pausada={res['pausada_apos_livre']}")


# ------------------------------------------------------------ 6. roteamento
print()
print("=" * 62)
print("7. ROTEAMENTO DO HANDOFF POR FRENTE")
print("=" * 62)

import asyncio

from bot.evolution import normalizar_numero
from bot.fluxo import ROTULOS_FRENTE
from bot.main import Aplicacao


def caminhar(entradas: list[str]) -> Sessao:
    sessao = Sessao(numero="5519999999999", nome="Teste")
    motor.iniciar(sessao, dentro_do_horario=True)
    for entrada in entradas:
        motor.processar(sessao, entrada)
    return sessao


CAMINHOS = [
    ("promotor barrado, quem fala e gestor", ["1", "1"], "suporte"),
    ("promotor barrado, quem fala e a loja", ["1", "2"], "suporte"),
    ("promotor barrado, o proprio promotor", ["1", "3"], "promotor"),
    ("cadastro e documentos", ["2"], "suporte"),
    ("fatura e cobranca", ["3"], "financeiro"),
    ("cliente ja usa MobConnect", ["4"], "suporte"),
    ("MobConnect ambiguo confirmado como suporte", ["mobconnect", "1"], "suporte"),
    ("lead MobConnect pelo numero", ["6"], "comercial_mobconnect"),
    (
        "lead MobConnect por texto livre",
        ["quero contratar o MobConnect"],
        "comercial_mobconnect",
    ),
    ("lead rede varejista", ["5", "1"], "comercial_varejo"),
    ("lead industria", ["5", "2"], "comercial_industria"),
    ("lead agencia", ["5", "3"], "comercial_industria"),
    ("pediu 9 sem dizer o assunto", ["9"], ""),
]

for titulo, entradas, frente in CAMINHOS:
    obtida = caminhar(entradas).dados.get("frente", "")
    checar(
        obtida == frente,
        f"{titulo} -> {ROTULOS_FRENTE.get(frente, 'responsavel geral')}",
        f"veio {obtida!r}, esperado {frente!r}",
    )


class _EvolutionFalsa:
    def __init__(self) -> None:
        self.enviados: list[tuple[str, str]] = []

    async def enviar_texto(self, numero, texto, **_):  # noqa: ANN001
        self.enviados.append((numero, texto))


def _do_env_arquivo(chave: str) -> str:
    """Le uma chave direto do .env: secoes anteriores mexem em os.environ."""
    arquivo = RAIZ / ".env"
    if not arquivo.exists():
        return ""
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if linha.strip().startswith(f"{chave}="):
            return linha.split("=", 1)[1].strip()
    return ""


stub = Aplicacao.__new__(Aplicacao)
stub.motor = motor
stub.evolution = _EvolutionFalsa()
stub.numero_notificacao = normalizar_numero(_do_env_arquivo("NUMERO_NOTIFICACAO"))
stub.notificacao_modo_teste = False  # o modo teste tem checagem propria adiante
stub.notificacao_por_frente = {}
for _frente in ROTULOS_FRENTE:
    _destino = normalizar_numero(_do_env_arquivo(f"NOTIFICACAO_{_frente.upper()}"))
    if _destino:
        stub.notificacao_por_frente[_frente] = _destino

checar(
    bool(stub.numero_notificacao),
    "'.env' define o responsavel geral (NUMERO_NOTIFICACAO)",
)

print()
print("  destino configurado por frente:")
for _frente, _rotulo in ROTULOS_FRENTE.items():
    _d = stub.notificacao_por_frente.get(_frente)
    print(f"    {_rotulo:<52} {_d or '(responsavel geral ' + stub.numero_notificacao + ')'}")

for titulo, entradas, frente in CAMINHOS:
    sessao = caminhar(entradas)
    esperado = stub.notificacao_por_frente.get(frente, stub.numero_notificacao)
    antes = len(stub.evolution.enviados)
    asyncio.run(Aplicacao._notificar_time(stub, sessao))
    enviou = len(stub.evolution.enviados) > antes
    checar(enviou, f"handoff de '{titulo}' gera aviso")
    if enviou:
        numero, texto = stub.evolution.enviados[-1]
        checar(
            numero == esperado,
            f"aviso de '{titulo}' vai para {esperado}",
            f"foi para {numero}",
        )
        if frente:
            checar(
                ROTULOS_FRENTE[frente] in texto,
                f"aviso de '{titulo}' declara a frente no texto",
            )

# quem pede atendente sendo o proprio destino nao recebe o resumo de volta
sessao = caminhar(["3"])
sessao.numero = stub.notificacao_por_frente.get("financeiro", stub.numero_notificacao)
antes = len(stub.evolution.enviados)
asyncio.run(Aplicacao._notificar_time(stub, sessao))
checar(
    len(stub.evolution.enviados) == antes,
    "nao devolve o resumo interno para o proprio contato",
)

checar(
    stub.notificacao_por_frente.get("suporte") != stub.numero_notificacao,
    "suporte tem destino proprio, diferente do responsavel geral",
)
checar(
    "promotor" not in stub.notificacao_por_frente,
    "promotor sem vinculo fica com o responsavel geral (Mob2Con nao atende direto)",
)

# esgotar tentativas dentro de um assunto NAO deve acionar a frente
sessao = caminhar(["1", "1"])
for _ in range(ATENDIMENTO.max_tentativas_invalidas):
    ultima = motor.processar(sessao, "asdfgh qwerty")
checar(ultima.transferir, "tres tentativas invalidas ainda transferem")
checar(
    sessao.dados.get("frente") == "suporte",
    "frente do assunto continua registrada para contexto",
)
antes = len(stub.evolution.enviados)
asyncio.run(Aplicacao._notificar_time(stub, sessao))
numero, texto = stub.evolution.enviados[-1]
checar(
    len(stub.evolution.enviados) > antes and numero == stub.numero_notificacao,
    "handoff por esgotamento vai ao responsavel geral, nao ao Suporte",
    f"foi para {numero}",
)
checar("Motivo da transferência" in texto, "aviso explica que o bot nao entendeu")
checar("Suporte" in texto, "aviso preserva a frente do assunto como contexto")

# voltar ao menu limpa o desvio: pedir atendente depois volta a acionar a frente
motor.processar(sessao, "0")
motor.processar(sessao, "3")
checar(
    "handoff_sem_frente" not in sessao.dados,
    "retomar a navegacao limpa o desvio por esgotamento",
)
antes = len(stub.evolution.enviados)
asyncio.run(Aplicacao._notificar_time(stub, sessao))
checar(
    stub.evolution.enviados[-1][0] == stub.notificacao_por_frente["financeiro"],
    "depois de retomar, o handoff volta a ir para a frente certa",
    f"foi para {stub.evolution.enviados[-1][0]}",
)

# modo teste desvia tudo para o responsavel geral, declarando o destino real
stub.notificacao_modo_teste = True
sessao = caminhar(["3"])
asyncio.run(Aplicacao._notificar_time(stub, sessao))
numero, texto = stub.evolution.enviados[-1]
checar(
    numero == stub.numero_notificacao,
    "modo teste nao envia nada para as frentes",
    f"foi para {numero}",
)
checar(
    stub.notificacao_por_frente["financeiro"] in texto,
    "modo teste declara qual seria o destino real",
)
stub.notificacao_modo_teste = False
checar(
    _do_env_arquivo("NOTIFICACAO_MODO_TESTE").lower() in {"true", "false"},
    "'.env' declara NOTIFICACAO_MODO_TESTE",
    f"veio {_do_env_arquivo('NOTIFICACAO_MODO_TESTE')!r}",
)
print(f"\n  NOTIFICACAO_MODO_TESTE no .env: {_do_env_arquivo('NOTIFICACAO_MODO_TESTE')}")


# ------------------------------------------------------------ resultado
print()
print("=" * 62)
print(f"RESULTADO: {len(oks)} passaram, {len(falhas)} falharam")
print("=" * 62)
for falha in falhas:
    print(f"  FALHA: {falha}")
sys.exit(1 if falhas else 0)
