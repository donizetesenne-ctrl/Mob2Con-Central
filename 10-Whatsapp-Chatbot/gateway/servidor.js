/**
 * API HTTP compatível com a Evolution API v2.
 *
 * Implementa apenas as rotas que o chatbot usa, com os mesmos caminhos, o mesmo
 * header `apikey` e os mesmos formatos de resposta. Assim o serviço Python e os
 * scripts de operação funcionam sem nenhuma alteração.
 */

import { createServer } from 'node:http'

const LIMITE_CORPO_BYTES = 1_000_000

function responder(res, status, corpo) {
  const texto = JSON.stringify(corpo)
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(texto),
  })
  res.end(texto)
}

function erro(res, status, mensagem) {
  responder(res, status, {
    status,
    error: true,
    response: { message: mensagem },
  })
}

async function lerCorpo(req) {
  const partes = []
  let tamanho = 0
  for await (const parte of req) {
    tamanho += parte.length
    if (tamanho > LIMITE_CORPO_BYTES) throw new Error('corpo muito grande')
    partes.push(parte)
  }
  if (!partes.length) return {}
  const bruto = Buffer.concat(partes).toString('utf8')
  if (!bruto.trim()) return {}
  return JSON.parse(bruto)
}

/** Extrai o texto do payload, aceitando o formato novo e o legado. */
function extrairTexto(corpo) {
  if (typeof corpo?.text === 'string') return corpo.text
  if (typeof corpo?.textMessage?.text === 'string') return corpo.textMessage.text
  return ''
}

function extrairDelay(corpo) {
  const bruto = corpo?.delay ?? corpo?.options?.delay ?? 0
  const numero = Number(bruto)
  return Number.isFinite(numero) && numero > 0 ? numero : 0
}

export function criarServidor({ conexao, entregador, apiKey, porta, logger }) {
  const autorizado = (req) => {
    if (!apiKey) return true
    const enviada = req.headers.apikey ?? req.headers.Apikey
    return enviada === apiKey
  }

  async function despachar(req, res) {
    const url = new URL(req.url, `http://localhost:${porta}`)
    const caminho = url.pathname.replace(/\/+$/, '') || '/'
    const metodo = req.method?.toUpperCase() ?? 'GET'

    // --- rotas públicas -----------------------------------------------------

    if (metodo === 'GET' && (caminho === '/' || caminho === '/health')) {
      return responder(res, 200, {
        status: 200,
        message: 'Gateway WhatsApp Mob2Con (compatível com Evolution API v2)',
        version: '1.0.0',
        instance: conexao.instancia,
        state: conexao.estado,
        number: conexao.numero,
        profileName: conexao.nomePerfil,
        webhook: entregador.url || null,
      })
    }

    // --- daqui pra baixo exige apikey --------------------------------------

    if (!autorizado(req)) {
      return erro(res, 401, 'apikey inválida ou ausente')
    }

    // POST /instance/create
    if (metodo === 'POST' && caminho === '/instance/create') {
      return responder(res, 201, {
        instance: {
          instanceName: conexao.instancia,
          status: conexao.estado === 'open' ? 'open' : 'created',
        },
        hash: { apikey: apiKey },
      })
    }

    // GET /instance/connect/:instancia
    if (metodo === 'GET' && caminho.startsWith('/instance/connect/')) {
      if (conexao.conectado) {
        return responder(res, 200, {
          instance: { instanceName: conexao.instancia, state: 'open' },
          message: 'já conectado',
        })
      }
      // o QR pode levar 1-2s para ser gerado após o start
      const base64 = await aguardarQr(conexao, 12_000)
      if (!base64) {
        return erro(
          res,
          503,
          'QR Code ainda não disponível. Veja o terminal do gateway ou tente de novo.',
        )
      }
      return responder(res, 200, { base64, code: null, pairingCode: null })
    }

    // GET /instance/connectionState/:instancia
    if (metodo === 'GET' && caminho.startsWith('/instance/connectionState/')) {
      return responder(res, 200, {
        instance: {
          instanceName: conexao.instancia,
          state: conexao.estado,
          number: conexao.numero,
          profileName: conexao.nomePerfil,
        },
      })
    }

    // GET /instance/fetchInstances
    if (metodo === 'GET' && caminho === '/instance/fetchInstances') {
      return responder(res, 200, [
        {
          name: conexao.instancia,
          instanceName: conexao.instancia,
          connectionStatus: conexao.estado,
          integration: 'WHATSAPP-BAILEYS',
          ownerJid: conexao.numero ? `${conexao.numero}@s.whatsapp.net` : null,
          profileName: conexao.nomePerfil,
        },
      ])
    }

    // POST /webhook/set/:instancia  (aceita formato novo e legado)
    if (metodo === 'POST' && caminho.startsWith('/webhook/set/')) {
      let corpo
      try {
        corpo = await lerCorpo(req)
      } catch (falha) {
        return erro(res, 400, falha.message)
      }
      const config = corpo.webhook ?? corpo
      const novaUrl = config?.url
      if (!novaUrl || typeof novaUrl !== 'string') {
        return erro(res, 400, 'informe webhook.url')
      }
      entregador.definirUrl(novaUrl)
      return responder(res, 200, {
        webhook: {
          instanceName: conexao.instancia,
          webhook: { url: novaUrl, enabled: true, events: config?.events ?? [] },
        },
      })
    }

    // GET /webhook/find/:instancia
    if (metodo === 'GET' && caminho.startsWith('/webhook/find/')) {
      return responder(res, 200, {
        enabled: Boolean(entregador.url),
        url: entregador.url ?? '',
        events: ['MESSAGES_UPSERT'],
      })
    }

    // POST /message/sendText/:instancia
    if (metodo === 'POST' && caminho.startsWith('/message/sendText/')) {
      let corpo
      try {
        corpo = await lerCorpo(req)
      } catch (falha) {
        return erro(res, 400, falha.message)
      }
      const numero = corpo?.number
      const texto = extrairTexto(corpo)
      if (!numero) return erro(res, 400, 'campo "number" é obrigatório')
      if (!texto) return erro(res, 400, 'campo "text" é obrigatório')

      try {
        const enviada = await conexao.enviarTexto(numero, texto, {
          delayMs: extrairDelay(corpo),
        })
        return responder(res, 201, {
          key: enviada?.key ?? null,
          status: 'PENDING',
          message: { conversation: texto },
          messageTimestamp: String(enviada?.messageTimestamp ?? ''),
        })
      } catch (falha) {
        logger.error(`Falha ao enviar para ${numero}: ${falha.message}`)
        return erro(res, 503, falha.message)
      }
    }

    // POST /chat/sendPresence/:instancia
    if (metodo === 'POST' && caminho.startsWith('/chat/sendPresence/')) {
      let corpo
      try {
        corpo = await lerCorpo(req)
      } catch (falha) {
        return erro(res, 400, falha.message)
      }
      if (!corpo?.number) return erro(res, 400, 'campo "number" é obrigatório')
      try {
        // não bloqueia a resposta: presença é cosmética
        conexao
          .enviarPresenca(corpo.number, corpo.presence ?? 'composing', 0)
          .catch(() => { })
        return responder(res, 200, { presence: corpo.presence ?? 'composing' })
      } catch (falha) {
        return erro(res, 503, falha.message)
      }
    }

    // DELETE /instance/logout/:instancia
    if (metodo === 'DELETE' && caminho.startsWith('/instance/logout/')) {
      await conexao.encerrar()
      return responder(res, 200, { status: 'SUCCESS', message: 'sessão encerrada' })
    }

    return erro(res, 404, `rota não implementada: ${metodo} ${caminho}`)
  }

  const servidor = createServer((req, res) => {
    despachar(req, res).catch((falha) => {
      logger.error({ falha }, 'Erro não tratado no servidor')
      if (!res.headersSent) erro(res, 500, 'erro interno do gateway')
    })
  })

  return servidor
}

/** Espera o QR Code aparecer, com timeout. */
async function aguardarQr(conexao, timeoutMs) {
  const limite = Date.now() + timeoutMs
  while (Date.now() < limite) {
    if (conexao.qrBase64) return conexao.qrBase64
    if (conexao.conectado) return null
    await new Promise((resolve) => setTimeout(resolve, 400))
  }
  return conexao.qrBase64
}
