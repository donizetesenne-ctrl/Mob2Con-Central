/**
 * Conexão com o WhatsApp via Baileys.
 *
 * Guarda a sessão em uma pasta local — não precisa de Postgres nem Redis.
 * Reconecta sozinho com backoff e detecta logout para pedir novo QR Code.
 */

import { createRequire } from 'node:module'
import { rm } from 'node:fs/promises'
import qrcode from 'qrcode'

// Baileys é publicado em CommonJS. createRequire evita as armadilhas de
// interop do import default entre ESM e CJS.
const require = createRequire(import.meta.url)
const baileys = require('@whiskeysockets/baileys')

const makeWASocket = baileys.makeWASocket ?? baileys.default
const {
  DisconnectReason,
  useMultiFileAuthState,
  fetchLatestBaileysVersion,
  makeCacheableSignalKeyStore,
  Browsers,
} = baileys

const ESPERA_MINIMA_MS = 2_000
const ESPERA_MAXIMA_MS = 60_000
const LIMITE_MENSAGENS_ENVIADAS = 500

const dormir = (ms) => new Promise((resolve) => setTimeout(resolve, ms))
const SUFIXO_LID = '@lid'

function numeroDoJid(jid) {
  return String(jid ?? '').split('@')[0].split(':')[0].replace(/\D/g, '')
}

function ehJidLid(jid) {
  return typeof jid === 'string' && jid.endsWith(SUFIXO_LID)
}

/**
 * Extrai o vínculo PN -> LID de uma mensagem direta recebida.
 * Responder pelo mesmo LID evita abrir uma sessão Signal paralela no JID PN.
 */
export function mapearIdentidadeRecebida(chave) {
  const remoto = String(chave?.remoteJid ?? '')
  if (!ehJidLid(remoto)) return null

  const numero = numeroDoJid(chave?.senderPn)
  if (!numero) return null
  return { numero, jid: remoto }
}

/** Grava no cache a identidade exata usada pela conversa recebida. */
export function registrarIdentidadeRecebida(mapa, chave) {
  const identidade = mapearIdentidadeRecebida(chave)
  if (!identidade) return null

  mapa.set(identidade.numero, identidade.jid)
  return identidade
}

/** Prefere a identidade LID atual informada pelo USync; PN é fallback legado. */
export function escolherJidDaConsulta(encontrado, fallback) {
  const lid = String(encontrado?.lid ?? '')
  if (ehJidLid(lid)) return lid

  const jid = String(encontrado?.jid ?? '')
  return jid || fallback
}

export class ConexaoWhatsApp {
  #config
  #logger
  #aoReceberMensagem
  #sock = null
  #estado = 'close'
  #qr = null
  #qrBase64 = null
  #tentativas = 0
  #encerrando = false
  #quedas = 0
  #ultimaConexaoEm = null
  #ultimaQuedaEm = null
  #ultimoMotivoQueda = null
  #enviadas = new Map()
  #jids = new Map()

  /**
   * @param {object} opcoes
   * @param {string} opcoes.instancia   nome lógico da instância
   * @param {string} opcoes.dirSessao   pasta onde a sessão é persistida
   * @param {Function} opcoes.aoReceberMensagem  callback(mensagemBaileys)
   * @param {object} opcoes.logger      logger pino
   */
  constructor({ instancia, dirSessao, aoReceberMensagem, logger }) {
    this.#config = { instancia, dirSessao }
    this.#aoReceberMensagem = aoReceberMensagem
    this.#logger = logger
  }

  get estado() {
    return this.#estado
  }

  get instancia() {
    return this.#config.instancia
  }

  get qrBase64() {
    return this.#qrBase64
  }

  get conectado() {
    return this.#estado === 'open'
  }

  /** Telemetria operacional sem expor credenciais da sessão. */
  get diagnostico() {
    return {
      estado: this.#estado,
      quedas: this.#quedas,
      tentativasReconexao: this.#tentativas,
      ultimaConexaoEm: this.#ultimaConexaoEm,
      ultimaQuedaEm: this.#ultimaQuedaEm,
      ultimoMotivoQueda: this.#ultimoMotivoQueda,
    }
  }

  /** Número do WhatsApp pareado (só dígitos), ou null se não conectado. */
  get numero() {
    const bruto = this.#sock?.user?.id
    if (!bruto) return null
    return bruto.split(':')[0].split('@')[0].replace(/\D/g, '') || null
  }

  /** Nome do perfil pareado. */
  get nomePerfil() {
    return this.#sock?.user?.name ?? this.#sock?.user?.verifiedName ?? null
  }

  /** Sobe a conexão e mantém o loop de reconexão. */
  async iniciar() {
    this.#encerrando = false
    await this.#conectar()
  }

  async #conectar() {
    if (this.#encerrando) return

    const { state, saveCreds } = await useMultiFileAuthState(this.#config.dirSessao)

    let version
    try {
      const info = await fetchLatestBaileysVersion()
      version = info.version
      this.#logger.info(`Protocolo WhatsApp Web ${version?.join('.')}`)
    } catch {
      this.#logger.warn('Não consegui checar a versão do WhatsApp Web; usando a padrão.')
    }

    this.#estado = 'connecting'
    this.#sock = makeWASocket({
      version,
      logger: this.#logger,
      auth: {
        creds: state.creds,
        keys: makeCacheableSignalKeyStore(state.keys, this.#logger),
      },
      browser: Browsers.ubuntu('Chrome'),
      // não marca o celular como online: as notificações continuam chegando nele
      markOnlineOnConnect: false,
      syncFullHistory: false,
      generateHighQualityLinkPreview: false,
      // permite ao WhatsApp reenviar mensagens nossas que falharam
      getMessage: async (chave) => this.#enviadas.get(chave?.id)?.message,
    })

    this.#sock.ev.on('creds.update', saveCreds)
    this.#sock.ev.on('connection.update', (evento) => this.#aoAtualizarConexao(evento))
    this.#sock.ev.on('messages.upsert', (evento) => this.#aoChegarMensagens(evento))
  }

  async #aoAtualizarConexao({ connection, lastDisconnect, qr }) {
    if (qr) {
      this.#qr = qr
      this.#qrBase64 = await qrcode.toDataURL(qr, { margin: 1, width: 512 })
      const emTexto = await qrcode.toString(qr, { type: 'terminal', small: true })
      console.log('\n=== Escaneie o QR Code abaixo no WhatsApp ===\n')
      console.log(emTexto)
      console.log('WhatsApp > Configuracoes > Dispositivos conectados > Conectar dispositivo\n')
    }

    if (connection === 'open') {
      this.#estado = 'open'
      this.#ultimaConexaoEm = new Date().toISOString()
      this.#tentativas = 0
      this.#qr = null
      this.#qrBase64 = null
      const meu = this.#sock?.user?.id?.split(':')[0] ?? '?'
      this.#logger.info(`WhatsApp conectado como ${meu}`)
      console.log(`\n[OK] WhatsApp conectado (${meu}). Gateway pronto.\n`)
      return
    }

    if (connection === 'connecting') {
      this.#estado = 'connecting'
      return
    }

    if (connection !== 'close') return

    this.#estado = 'close'
    const motivo = lastDisconnect?.error?.output?.statusCode
    this.#quedas += 1
    this.#ultimaQuedaEm = new Date().toISOString()
    this.#ultimoMotivoQueda = motivo ?? 'desconhecido'

    if (this.#encerrando) {
      this.#logger.info('Conexão encerrada por pedido do processo.')
      return
    }

    if (motivo === DisconnectReason.loggedOut) {
      this.#logger.warn('Sessão encerrada no celular. Apagando credenciais.')
      console.log('\n[!] O dispositivo foi desconectado no celular.')
      console.log('    Vou gerar um novo QR Code para parear de novo.\n')
      await this.#apagarSessao()
      this.#tentativas = 0
      await dormir(ESPERA_MINIMA_MS)
      return this.#conectar()
    }

    // qualquer outro motivo: reconecta com backoff exponencial
    this.#tentativas += 1
    const espera = Math.min(
      ESPERA_MINIMA_MS * 2 ** (this.#tentativas - 1),
      ESPERA_MAXIMA_MS,
    )
    this.#logger.warn(
      `Conexão caiu (código ${motivo ?? 'desconhecido'}). ` +
      `Tentativa ${this.#tentativas} em ${Math.round(espera / 1000)}s.`,
    )
    await dormir(espera)
    return this.#conectar()
  }

  #aoChegarMensagens({ messages, type }) {
    // 'notify' = mensagem nova de verdade.
    // 'append' costuma ser sincronização de histórico — responder isso faria o
    // bot atender conversas antigas ao reconectar.
    if (type !== 'notify' || !Array.isArray(messages)) return

    for (const mensagem of messages) {
      const chave = mensagem?.key ?? {}
      const jid = chave.remoteJid
      if (!jid || jid === 'status@broadcast') continue

      const identidade = registrarIdentidadeRecebida(this.#jids, chave)
      if (identidade) {
        this.#logger.info(
          `Identidade preservada: ${identidade.numero} -> ${identidade.jid}`,
        )
      }

      // uma linha por mensagem: é o que permite diagnosticar "o bot não respondeu"
      this.#logger.info(
        `<- ${jid}` +
        (chave.senderPn ? ` (pn ${chave.senderPn})` : '') +
        (chave.participantPn ? ` (participante ${chave.participantPn})` : '') +
        ` | fromMe=${Boolean(chave.fromMe)} | id=${chave.id}`,
      )

      try {
        this.#aoReceberMensagem(mensagem)
      } catch (erro) {
        this.#logger.error({ erro }, 'Falha ao encaminhar mensagem recebida')
      }
    }
  }

  async #apagarSessao() {
    try {
      await rm(this.#config.dirSessao, { recursive: true, force: true })
    } catch (erro) {
      this.#logger.error({ erro }, 'Não consegui apagar a pasta de sessão')
    }
  }

  /** Resolve o JID real de um número, tratando LID e o 9º dígito brasileiro. */
  async resolverJid(numero) {
    const limpo = String(numero ?? '').replace(/\D/g, '')
    if (!limpo) throw new Error('número vazio')

    const cacheado = this.#jids.get(limpo)
    if (cacheado) {
      if (ehJidLid(cacheado)) {
        this.#logger.info(`Destino LID reutilizado: ${limpo} -> ${cacheado}`)
      }
      return cacheado
    }

    const fallback = `${limpo}@s.whatsapp.net`
    let jid = fallback
    try {
      const resultado = await this.#sock?.onWhatsApp(limpo)
      const encontrado = Array.isArray(resultado) ? resultado[0] : null
      if (encontrado?.exists) {
        jid = escolherJidDaConsulta(encontrado, fallback)
        if (ehJidLid(jid)) {
          this.#logger.info(`Destino LID consultado: ${limpo} -> ${jid}`)
        }
      } else if (encontrado?.exists === false) {
        this.#logger.warn(`${limpo} não parece ter WhatsApp.`)
      }
    } catch (erro) {
      this.#logger.debug({ erro }, 'onWhatsApp falhou; usando o JID direto')
    }

    this.#jids.set(limpo, jid)
    return jid
  }

  #exigirConexao() {
    if (!this.#sock || this.#estado !== 'open') {
      throw new Error(
        `WhatsApp não está conectado (estado: ${this.#estado}). Pareie o QR Code primeiro.`,
      )
    }
  }

  /** Envia texto e devolve a chave da mensagem, no formato da Evolution. */
  async enviarTexto(numero, texto, { delayMs = 0 } = {}) {
    this.#exigirConexao()
    const jid = await this.resolverJid(numero)

    if (delayMs > 0) {
      try {
        await this.#sock.presenceSubscribe(jid)
        await this.#sock.sendPresenceUpdate('composing', jid)
        await dormir(Math.min(delayMs, 15_000))
        await this.#sock.sendPresenceUpdate('paused', jid)
      } catch (erro) {
        this.#logger.debug({ erro }, 'Falha ao simular digitação')
      }
    }

    const enviada = await this.#sock.sendMessage(jid, { text: texto })
    if (enviada?.key?.id) {
      this.#enviadas.set(enviada.key.id, enviada)
      if (this.#enviadas.size > LIMITE_MENSAGENS_ENVIADAS) {
        this.#enviadas.delete(this.#enviadas.keys().next().value)
      }
    }
    return enviada
  }

  async enviarPresenca(numero, presenca = 'composing', duracaoMs = 0) {
    this.#exigirConexao()
    const jid = await this.resolverJid(numero)
    await this.#sock.presenceSubscribe(jid)
    await this.#sock.sendPresenceUpdate(presenca, jid)
    if (duracaoMs > 0) {
      await dormir(Math.min(duracaoMs, 15_000))
      await this.#sock.sendPresenceUpdate('paused', jid)
    }
  }

  async encerrar() {
    this.#encerrando = true
    try {
      this.#sock?.end(undefined)
    } catch {
      /* já estava fechado */
    }
    this.#estado = 'close'
  }
}
