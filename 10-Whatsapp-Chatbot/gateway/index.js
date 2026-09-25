/**
 * Gateway WhatsApp Mob2Con — alternativa à Evolution API sem Docker.
 *
 * Sobe uma conexão Baileys e expõe uma API HTTP compatível com a Evolution
 * API v2, de forma que o bot em Python funcione sem alteração.
 *
 * Não precisa de Postgres, Redis nem Docker: a sessão fica em uma pasta local.
 *
 * Rodar:
 *   npm start          (usa o ../.env do projeto)
 */

import { fileURLToPath } from 'node:url'
import { dirname, isAbsolute, resolve } from 'node:path'
import pino from 'pino'

import { ConexaoWhatsApp } from './whatsapp.js'
import { EntregadorWebhook } from './webhook.js'
import { criarServidor } from './servidor.js'

const AQUI = dirname(fileURLToPath(import.meta.url))

function texto(chave, padrao = '') {
  const valor = process.env[chave]
  return valor === undefined || valor === null ? padrao : String(valor).trim()
}

function inteiro(chave, padrao) {
  const numero = Number.parseInt(texto(chave), 10)
  return Number.isFinite(numero) ? numero : padrao
}

const config = {
  porta: inteiro('GATEWAY_PORTA', 8080),
  instancia: texto('EVOLUTION_INSTANCIA', 'mob2con'),
  apiKey: texto('EVOLUTION_API_KEY'),
  webhookToken: texto('WEBHOOK_TOKEN'),
  webhookUrl: texto('GATEWAY_WEBHOOK_URL', 'http://localhost:8000/webhook'),
  dirSessao: texto('GATEWAY_SESSAO_DIR', 'sessao'),
  nivelLog: texto('GATEWAY_NIVEL_LOG', 'info'),
}

if (!isAbsolute(config.dirSessao)) {
  config.dirSessao = resolve(AQUI, config.dirSessao)
}

// Em terminal interativo, o QR continua no console. Sob Tarefa Agendada,
// stdout/stderr podem existir sem consumidor e bloquear o event loop. Nesse
// modo, toda telemetria vai direto ao arquivo, sem worker de transporte.
const CAMINHO_LOG = fileURLToPath(new URL('../gateway.log', import.meta.url))
const destinoLog = pino.destination({
  dest: CAMINHO_LOG,
  mkdir: true,
  sync: false,
})
const logger = pino({ level: config.nivelLog }, destinoLog)

if (!process.stdout.isTTY) {
  console.log = () => {}
  console.error = (...partes) => {
    logger.error(partes.map((parte) => String(parte)).join(' '))
  }
}

if (!config.apiKey) {
  console.error('\n[X] EVOLUTION_API_KEY está vazio.')
  console.error('    Rode antes:  python scripts\\gerar_env.py\n')
  process.exit(1)
}

console.log('============================================================')
console.log('  Gateway WhatsApp Mob2Con (sem Docker)')
console.log('============================================================')
console.log(`  Instancia : ${config.instancia}`)
console.log(`  API HTTP  : http://localhost:${config.porta}`)
console.log(`  Webhook   : ${config.webhookUrl}`)
console.log(`  Sessao    : ${config.dirSessao}`)
console.log('============================================================\n')

const entregador = new EntregadorWebhook({
  url: config.webhookUrl,
  token: config.webhookToken,
  instancia: config.instancia,
  apiKey: config.apiKey,
  serverUrl: `http://localhost:${config.porta}`,
  logger,
})

const conexao = new ConexaoWhatsApp({
  instancia: config.instancia,
  dirSessao: config.dirSessao,
  logger,
  aoReceberMensagem: (mensagem) => {
    // dispara sem await: o Baileys não deve esperar o bot responder
    void entregador.enviarMensagem(mensagem)
  },
})

const servidor = criarServidor({
  conexao,
  entregador,
  apiKey: config.apiKey,
  porta: config.porta,
  logger,
})

servidor.listen(config.porta, '127.0.0.1', () => {
  logger.info(`API do gateway ouvindo em http://127.0.0.1:${config.porta}`)
})

servidor.on('error', (falha) => {
  if (falha.code === 'EADDRINUSE') {
    console.error(`\n[X] A porta ${config.porta} já está em uso.`)
    console.error('    Feche o outro processo ou mude GATEWAY_PORTA no .env\n')
    process.exit(1)
  }
  logger.error({ falha }, 'Erro no servidor HTTP')
})

await conexao.iniciar()

let encerrando = false
async function encerrar(sinal) {
  if (encerrando) return
  encerrando = true
  console.log(`\n[i] Recebi ${sinal}. Encerrando...`)
  servidor.close()
  await conexao.encerrar()
  process.exit(0)
}

process.on('SIGINT', () => void encerrar('SIGINT'))
process.on('SIGTERM', () => void encerrar('SIGTERM'))
process.on('unhandledRejection', (motivo) => {
  logger.error({ motivo }, 'Promise rejeitada sem tratamento')
})
