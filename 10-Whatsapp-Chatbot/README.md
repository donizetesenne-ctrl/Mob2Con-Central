# Chatbot WhatsApp Mob2Con

Atendimento automático no WhatsApp. O bot é **determinístico por padrão**: menu
numerado, sem custo por mensagem. Quando o fluxo não resolve, ele pesquisa
localmente os 60 manuais com SQLite FTS5 e responde com trecho e fonte. A IA é
um fallback posterior e opcional.

Dois modos de execução, o **mesmo bot** nos dois:

| | Modo A — sem Docker | Modo B — Docker |
|---|---|---|
| Motor WhatsApp | `gateway/` em Node (Baileys) | Evolution API v2 |
| Banco de dados | SQLite local | Postgres |
| Sessões do bot | SQLite (Redis opcional) | Redis |
| Processos | watchdog + bot + gateway | 4 containers |
| RAM aproximada | ~150 MB | ~900 MB |
| Instalar | Node (já tem) | Docker Desktop |
| Integrações prontas (Chatwoot, Typebot) | não | sim |
| Vários números na mesma stack | não | sim |

**Nesta máquina o Modo A é o caminho.** Node 24 e Python 3.11 já estão
instalados; Docker não está.

---

## Modo A — sem Docker (recomendado aqui)

Um processo Node conversa com o WhatsApp e expõe uma API HTTP **compatível com
a Evolution API v2**. O bot Python não sabe a diferença: mesmas rotas, mesmo
header `apikey`, mesmo formato de webhook.

A sessão criptográfica do WhatsApp fica em `gateway/sessao/`. O contexto curto
de atendimento e as perguntas não respondidas ficam em `dados/chatbot.sqlite3`.
Ambos estão fora do Git.

### Subir

```powershell
cd "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\10-Whatsapp-Chatbot"
.\INICIAR-SEM-DOCKER.bat
```

O instalador registra o watchdog no `HKCU Run`. Ele inicia no logon do usuário,
roda oculto e verifica bot e gateway a cada 30 segundos. Se um endpoint cair, o
watchdog encerra somente processos cujo comando pertence a este projeto e sobe o
serviço novamente. Nenhuma janela precisa ficar aberta.

O Task Scheduler não é usado nesta máquina: o Bitdefender suspendeu processos
iniciados por tarefas, deixando estado `Running` sem heartbeat. As definições
antigas ficam desativadas para não disputar as portas 8000 e 8080.

No primeiro pareamento, escaneie o QR: **WhatsApp > Configurações > Dispositivos
conectados > Conectar dispositivo**. Depois mande "oi" de outro número.

### Ou passo a passo, sem automação

```powershell
python scripts\gerar_env.py          # só na primeira vez
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd gateway; npm install; cd ..

# janela 1
.\.venv\Scripts\python.exe -m uvicorn bot.main:app --host 127.0.0.1 --port 8000

# janela 2
cd gateway; node --env-file=../.env index.js
```

### O que o gateway implementa

```
GET    /                                  info e estado
POST   /instance/create
GET    /instance/connect/:instancia       QR Code em base64
GET    /instance/connectionState/:i       open | connecting | close
GET    /instance/fetchInstances
DELETE /instance/logout/:instancia
POST   /webhook/set/:instancia            aceita formato novo e legado
GET    /webhook/find/:instancia
POST   /message/sendText/:instancia
POST   /chat/sendPresence/:instancia
```

Cuidados que ele já resolve:

- **Não responde histórico.** Só processa eventos `notify`. Sem isso, ao
  reconectar o bot atenderia conversas antigas em massa.
- **9º dígito brasileiro.** Resolve o JID real via `onWhatsApp` com cache, então
  não erra número de celular de SP.
- **Reconexão com backoff** exponencial de 2s até 60s.
- **Logout detectado.** Se você remover o dispositivo no celular, ele apaga as
  credenciais e gera um QR novo em vez de ficar em loop.
- **Celular continua notificando** (`markOnlineOnConnect: false`).
- **Retry de mensagem** com cache das últimas 500 enviadas.

### Limites do Modo A

- **Um número por processo.** Para dois números, suba dois gateways em portas
  diferentes.
- **Sem as integrações nativas** da Evolution (Chatwoot, Typebot, Dify, filas).
- **Sem arquivo completo de conversa.** O SQLite guarda só o contexto curto
  necessário ao fluxo e agrega perguntas não respondidas com redação de CPF,
  telefone e e-mail.
- **Só texto.** Envio de mídia não está implementado no gateway.

Se algum desses virar requisito, migre para o Modo B: o bot Python continua
igual, muda só o `EVOLUTION_URL`.

---

## Modo B — Docker

Precisa do [Docker Desktop](https://www.docker.com/products/docker-desktop/)
instalado e rodando.

```powershell
python scripts\gerar_env.py
docker compose up -d
python scripts\setup_instancia.py
```

Ou `.\INICIAR-CHATBOT.bat`.

Sobe Postgres 16, Redis 7, `evoapicloud/evolution-api:v2.3.7` e o bot.
Manager web em <http://localhost:8080/manager> (login com o valor de
`EVOLUTION_API_KEY`).

### Alternativas ao Docker Desktop, se quiser o Modo B

| Opção | Observação |
|---|---|
| **Podman Desktop** | Gratuito, rootless. `podman compose up -d` usa o mesmo `docker-compose.yml` |
| **Docker Engine no WSL2** | O WSL 2 já está nesta máquina. Instala o engine dentro do Ubuntu, sem Docker Desktop |
| **VPS** | A partir de ~R$ 20/mês com a Evolution pré-instalada. Melhor para produção: fica online 24/7 |
| **Railway / Render** | Deploy por template, cobrança por consumo |

---

## Antes de apontar para o número da empresa

Coloque **seu número pessoal** em `NUMEROS_PERMITIDOS` no `.env` e reinicie o
bot. Assim ele só responde você enquanto valida o fluxo, sem risco de atender
cliente com menu pela metade.

```env
NUMEROS_PERMITIDOS=5511999998888
```

Quando aprovar o fluxo, apague o valor e reinicie.

---

## Estrutura

```
10-Whatsapp-Chatbot/
├── INICIAR-SEM-DOCKER.bat   instala/inicia watchdog e valida serviços
├── INICIAR-GATEWAY.bat      reinicia somente o gateway
├── REINICIAR-BOT.bat        reinicia somente o bot
├── REINICIAR-SERVICO.ps1    reinício com validação do processo alvo
├── SUPERVISOR-SERVICOS.ps1  worker de saúde e recuperação
├── INSTALAR-INICIALIZACAO-AUTOMATICA.ps1
├── STATUS-AUTOMACAO.ps1
├── REMOVER-INICIALIZACAO-AUTOMATICA.ps1
├── TESTAR-RECUPERACAO-AUTOMATICA.ps1
├── TESTAR-RECUPERACAO-GATEWAY.ps1
├── INICIAR-CHATBOT.bat      Modo B: stack Docker completa
├── docker-compose.yml       Modo B
├── Dockerfile               imagem do bot (roda sem root)
├── .env.example             modelo de configuração
├── requirements.txt
├── bot/                     >>> o bot, igual nos dois modos <<<
│   ├── main.py              FastAPI: webhook, /health, filtros, dedupe
│   ├── config.py            leitura do .env
│   ├── conhecimento.py      índice FTS5 e resposta extrativa local
│   ├── evolution.py         cliente HTTP (Evolution ou gateway)
│   ├── mensagem.py          parser do payload do webhook
│   ├── fluxo.py             motor do fluxo conversacional
│   ├── fluxo-mob2con.json   roteiro ativo do atendimento Mob2Con
│   ├── sessao.py            estado e repositórios (memória/Redis/SQLite)
│   ├── persistencia.py      SQLite: sessões + perguntas não respondidas
│   └── llm.py               fallback de IA (opcional)
├── gateway/                 Modo A: substitui a Evolution API
│   ├── index.js             bootstrap e configuração
│   ├── whatsapp.js          conexão Baileys, reconexão, envio
│   ├── servidor.js          API HTTP compatível com Evolution v2
│   ├── webhook.js           entrega de eventos para o bot
│   └── sessao/              credenciais do WhatsApp (NÃO versionar)
├── tests/
│   ├── test_conhecimento.py          índice, relevância e segurança
│   ├── test_integracao_manuais.py    integração com fluxo e personas
│   └── validar_automacao.ps1         gate dos scripts Windows
└── scripts/
    ├── watchdog_servicos.py watchdog persistente + heartbeat
    ├── indexar_manuais.py   indexa e valida os 60 manuais
    ├── gerar_env.py         cria .env com segredos aleatórios
    ├── setup_instancia.py   instância, webhook e QR Code (Modo B)
    ├── status.py            diagnóstico dos dois serviços
    ├── relatorio_aprendizado.py  revisa perguntas pendentes no SQLite
    └── enviar.py            envia mensagem de teste
```

---

## Editar o atendimento

Todo o roteiro Mob2Con está em `bot/fluxo-mob2con.json`. Um estado se parece
com isto:

```json
"menu": {
  "mensagem": "Como posso ajudar?\n\n*1* — Dashboards\n*2* — Automação",
  "opcoes": { "1": "servicos", "2": "automacao" },
  "sinonimos": { "dashboard": "1", "power bi": "1", "automatizar": "2" }
}
```

| Chave | Para que serve |
|---|---|
| `mensagem` | Texto enviado ao entrar no estado. Aceita `*negrito*` e `\n` |
| `opcoes` | `{"resposta": "estado_destino"}` |
| `sinonimos` | `{"palavra": "opção"}` — mapeia texto livre para uma opção |
| `capturar` | Nome do campo onde guardar a resposta livre do cliente |
| `proximo` | Estado seguinte depois de capturar |
| `acao` | `"transferir"` passa para atendimento humano |

Placeholders em qualquer mensagem: `{empresa}`, `{nome}`, `{nome_puro}`,
`{abertura}`, `{fechamento}`, `{dias}` e qualquer campo capturado
(ex.: `{nome_contato}`).

Depois de editar, reinicie o bot. Ele **valida o fluxo ao subir**: se uma opção
aponta para um estado que não existe, falha na inicialização com a lista de
problemas em vez de quebrar no meio de um atendimento real.

---

## Busca local nos 60 manuais

`MANUAIS_ATIVO=true` ativa a recuperação extrativa sem chave de IA. O índice
fica em `dados/manuais.sqlite3`; os Markdown permanecem no diretório configurado
por `MANUAIS_DIRETORIO`.

Na inicialização, o bot calcula SHA-256 de cada arquivo e atualiza somente
manuais novos, alterados ou removidos. O parser separa páginas e seções, remove
navegação Stonly, URLs e linhas de catálogo com `Check=False`. A busca usa FTS5,
BM25 e limiar lexical: se não houver correspondência suficiente, não responde
com trecho aleatório.

Ordem de atendimento: fluxo determinístico → manuais locais → IA opcional →
menu ou handoff. A resposta documental informa a fonte e nunca consulta status
real de conta.

```powershell
.\.venv\Scripts\python.exe scripts\indexar_manuais.py --validar
```

---

## Ligar a IA (opcional)

Com `LLM_ATIVO=false`, fluxo e manuais locais continuam funcionando. Com IA
ativa, o bot usa uma camada estruturada: intenção, memória da conversa, contexto
do fluxo e trechos dos manuais são avaliados antes de qualquer resposta gerativa.

A ordem operacional é: regras rápidas → IA estruturada quando necessário → RAG
nos manuais → fallback seguro. Ações como handoff comercial ou humano exigem
intenção explícita do usuário; confiança média gera no máximo uma pergunta de
esclarecimento e confiança baixa devolve o controle ao fluxo/RAG.

```env
LLM_ATIVO=true
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...
LLM_MODELO=gpt-4o-mini
```

| Provedor | `LLM_BASE_URL` |
|---|---|
| OpenAI | `https://api.openai.com/v1` |
| NVIDIA NIM | `https://integrate.api.nvidia.com/v1` |
| Groq | `https://api.groq.com/openai/v1` |
| Ollama local | `http://localhost:11434/v1` |

Se a IA falhar ou estourar timeout, o bot cai para manuais/fluxo. Nunca fica mudo.
Para modelos locais lentos, `LLM_TIMEOUT_LOCAL` limita a tentativa estruturada;
o mesmo modelo não é chamado duas vezes no mesmo turno.

O diagnóstico operacional mostra memória estruturada, RAG, motor de confiança,
modelo configurado e métricas das últimas 24 horas. Para replay redigido:

```powershell
.\.venv\Scripts\python.exe scripts\relatorio_qualidade.py
.\.venv\Scripts\python.exe scripts\relatorio_qualidade.py --horas 72 --replay 50
```

A trilha analítica usa hash do contato e redige CPF, telefone e e-mail.

---

## Persistência e aprendizado

`SQLITE_PATH=dados/chatbot.sqlite3` ativa o banco local. Reiniciar bot não apaga
estado, campos capturados, pausa humana nem histórico curto; o TTL continua sendo
controlado por `MINUTOS_SESSAO`. Se `REDIS_URL` estiver preenchido, Redis tem
prioridade para sessões e SQLite continua guardando a fila de aprendizado.

Quando fluxo e IA não resolvem uma mensagem, o bot agrega a ocorrência em
`perguntas_nao_respondidas`. Número e nome do contato não entram nessa tabela;
CPF, telefone e e-mail encontrados no texto são redigidos.

```powershell
.\.venv\Scripts\python.exe scripts\relatorio_aprendizado.py
.\.venv\Scripts\python.exe scripts\relatorio_aprendizado.py --resolver 12
```

## Inicialização automática no Windows

O instalador grava `Mob2ConChatbotWatchdog` em
`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`. No próximo logon, o
Explorer inicia `scripts/watchdog_servicos.py` oculto. O watchdog chama o worker
de saúde a cada 30 segundos; bot e gateway são recuperados sem apagar SQLite ou
`gateway/sessao/`.

```powershell
.\INSTALAR-INICIALIZACAO-AUTOMATICA.bat
.\STATUS-AUTOMACAO.bat
.\REMOVER-INICIALIZACAO-AUTOMATICA.bat
```

A remoção exclui o valor de autostart e mantém `.env`, banco, logs e pareamento.
Os processos atuais não são encerrados automaticamente.

---

## Comandos do dia a dia

```powershell
.\STATUS-AUTOMACAO.bat
.\.venv\Scripts\python.exe scripts\indexar_manuais.py --validar
.\REINICIAR-BOT.bat
.\INICIAR-GATEWAY.bat
.\.venv\Scripts\python.exe scripts\status.py
.\.venv\Scripts\python.exe scripts\relatorio_aprendizado.py

# Gates sem enviar mensagem
powershell -ExecutionPolicy Bypass -File tests\validar_automacao.ps1
.\.venv\Scripts\python.exe -m unittest tests.test_persistencia tests.test_aprendizado -v
.\.venv\Scripts\python.exe verificar-fluxo-mob2con.py

# Provas controladas: interrompem um serviço por alguns segundos
powershell -ExecutionPolicy Bypass -File TESTAR-RECUPERACAO-AUTOMATICA.ps1 -Executar
powershell -ExecutionPolicy Bypass -File TESTAR-RECUPERACAO-GATEWAY.ps1 -Executar

# Modo B
docker compose ps
docker compose logs -f bot
docker compose restart bot
docker compose down
```

---

## Segurança aplicada de fábrica

O `.env.example` oficial da Evolution API traz a chave
`429683C4C977415CAAFCCE10F7D57E11` — **a mesma para todo mundo no mundo**,
copiada em quase todo tutorial. Quem sobe com ela e expõe a porta entrega
controle total do WhatsApp para qualquer um que ache o endereço.

Este projeto já vem com:

- `gerar_env.py` cria chave aleatória e **aborta** se detectar a chave pública
- Gateway e bot escutam só em `127.0.0.1`
- No Modo B, portas publicadas só em `127.0.0.1`
- `AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=false`, telemetria desligada,
  CORS restrito, persistência de mensagens desligada
- Webhook protegido por `X-Webhook-Token`
- Container do bot roda sem root

**`gateway/sessao/` são as credenciais do seu WhatsApp.** Quem tem essa pasta
entra na sua conta. Já está no `.gitignore` — não tire de lá, não mande por
e-mail, não coloque em backup público.

---

## Problemas comuns

| Sintoma | Causa provável |
|---|---|
| `503 WhatsApp não está conectado` | QR não foi pareado; confira `gateway.log` |
| Bot não responde | Execute `STATUS-AUTOMACAO.bat` e confira heartbeat/porta 8000 |
| `401` nas chamadas | `EVOLUTION_API_KEY` diferente entre `.env` e o serviço |
| Porta 8080 em uso | Outro gateway está ativo; o watchdog não encerra processo desconhecido |
| Responde duas vezes | Dois bots manuais rodando ao mesmo tempo |
| QR não conecta | O QR expira em ~40s; reinicie o gateway para gerar outro |
| Reautentica sempre | `gateway/sessao/` sem permissão de escrita |
| Watchdog não inicia no boot | O `HKCU Run` inicia no logon do usuário, não antes dele |
| Fuso errado nos horários | Falta `tzdata` (já está no `requirements.txt`) |

---

## Limitação que você precisa aceitar

Os dois modos usam Baileys, que conecta um número comum ao WhatsApp por um
cliente não oficial. Isso **contraria os termos de uso do WhatsApp** e o número
pode ser banido — principalmente com disparo em massa ou mensagens para quem
não iniciou a conversa.

Na prática:

- Use um **número dedicado**, nunca o principal da empresa
- Só responda quem falou primeiro (é exatamente o que este bot faz)
- Aqueça o número: comece com pouco volume
- Para disparo ativo em escala, migre para a **Cloud API oficial** da Meta

A Evolution API (Modo B) suporta os dois modos, então trocar depois não exige
reescrever o bot.

---

## Sobre a Evolution API

Licença Apache 2.0 com duas condições extras: não remover logo/copyright dos
componentes de frontend, e **exibir aviso de que o sistema usa Evolution API**
em qualquer projeto, inclusive proprietário.

A **v3 (Evolution Go)** exige ativação de licença com heartbeat e retorna 503
até ser ativada. O Modo B usa a **v2 (Node)**, que não tem essa trava. O Modo A
não usa Evolution API — só a biblioteca
[Baileys](https://github.com/WhiskeySockets/Baileys) (MIT).
