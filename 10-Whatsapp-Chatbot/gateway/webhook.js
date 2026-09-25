/**
 * Entrega de eventos para o bot, no mesmo formato que a Evolution API usa.
 *
 * Assim o serviço Python não sabe (nem precisa saber) que está falando com o
 * gateway em vez da Evolution.
 */

const TIMEOUT_MS = 15_000
const SUFIXO_LID = '@lid'

/** Descobre o messageType do jeito que a Evolution reporta. */
function detectarTipo(mensagem) {
  const conteudo = mensagem?.message ?? {}
  const chaves = Object.keys(conteudo).filter((chave) => chave !== 'messageContextInfo')
  return chaves[0] ?? 'unknown'
}

/**
 * Normaliza a chave da mensagem para que `remoteJid` seja sempre o telefone.
 *
 * O WhatsApp migrou para LID (@lid): um identificador interno que esconde o
 * número. Quando isso acontece, o telefone real vem em `senderPn` (conversa
 * individual) ou `participantPn` (grupo). Sem essa tradução, qualquer regra
 * baseada em número — lista de permitidos, bloqueio, sessão — deixa de casar.
 */
function normalizarChave(chave) {
  if (!chave || typeof chave !== 'object') return { chave, lid: null }

  const remoto = String(chave.remoteJid ?? '')
  if (!remoto.endsWith(SUFIXO_LID)) return { chave, lid: null }

  const telefone = chave.senderPn || chave.participantPn || ''
  if (!telefone) return { chave, lid: remoto }

  return {
    chave: { ...chave, remoteJid: telefone, remoteJidLid: remoto },
    lid: remoto,
  }
}

export class EntregadorWebhook {
  #url
  #token
  #instancia
  #apiKey
  #serverUrl
  #logger

  constructor({ url, token, instancia, apiKey, serverUrl, logger }) {
    this.#url = url
    this.#token = token
    this.#instancia = instancia
    this.#apiKey = apiKey
    this.#serverUrl = serverUrl
    this.#logger = logger
  }

  get url() {
    return this.#url
  }

  definirUrl(novaUrl) {
    this.#url = novaUrl
    this.#logger.info(`Webhook agora aponta para ${novaUrl}`)
  }

  /** Monta o payload messages.upsert e envia. Nunca lança. */
  async enviarMensagem(mensagem) {
    if (!this.#url) {
      this.#logger.warn('Nenhuma URL de webhook configurada; mensagem descartada.')
      return
    }

    const { chave, lid } = normalizarChave(mensagem.key)
    if (lid) {
      this.#logger.info(
        `LID traduzido: ${lid} -> ${chave.remoteJid}` +
        (chave.remoteJid === lid ? ' (SEM telefone no payload!)' : ''),
      )
    }

    const tipo = detectarTipo(mensagem)
    if (tipo === 'unknown') {
      // Baileys entrega a mensagem sem conteudo quando nao consegue decifrar.
      // Registrar as pistas aqui e a unica forma de distinguir isso de um tipo
      // de mensagem que o bot ainda nao trata.
      this.#logger.warn(
        `Mensagem sem conteudo de ${chave.remoteJid}` +
        ` | id=${mensagem.key?.id ?? '?'}` +
        ` | chaves=[${Object.keys(mensagem.message ?? {}).join(',') || 'vazio'}]` +
        ` | stub=${mensagem.messageStubType ?? '-'}`,
      )
    }

    const payload = {
      event: 'messages.upsert',
      instance: this.#instancia,
      data: {
        key: chave,
        pushName: mensagem.pushName ?? '',
        message: mensagem.message ?? {},
        messageType: tipo,
        messageTimestamp: Number(mensagem.messageTimestamp ?? 0),
      },
      destination: this.#url,
      date_time: new Date().toISOString(),
      sender: chave.remoteJid ?? '',
      server_url: this.#serverUrl,
      apikey: this.#apiKey,
    }

    const cabecalhos = { 'Content-Type': 'application/json' }
    if (this.#token) cabecalhos['X-Webhook-Token'] = this.#token

    const controle = AbortSignal.timeout(TIMEOUT_MS)
    try {
      const resposta = await fetch(this.#url, {
        method: 'POST',
        headers: cabecalhos,
        body: JSON.stringify(payload),
        signal: controle,
      })
      if (!resposta.ok) {
        const corpo = await resposta.text().catch(() => '')
        this.#logger.error(
          `Bot respondeu ${resposta.status} ao webhook: ${corpo.slice(0, 200)}`,
        )
      }
    } catch (erro) {
      this.#logger.error(
        `Não consegui entregar o webhook em ${this.#url}: ${erro.message}`,
      )
    }
  }
}
