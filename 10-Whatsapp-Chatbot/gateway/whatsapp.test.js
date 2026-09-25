import test from 'node:test'
import assert from 'node:assert/strict'

import {
  escolherJidDaConsulta,
  mapearIdentidadeRecebida,
  registrarIdentidadeRecebida,
} from './whatsapp.js'

const PN = '5519971075405'
const JID_PN = `${PN}@s.whatsapp.net`
const JID_LID = '278223820726453@lid'

test('extrai vínculo PN para LID da mensagem recebida', () => {
  assert.deepEqual(
    mapearIdentidadeRecebida({ remoteJid: JID_LID, senderPn: JID_PN }),
    { numero: PN, jid: JID_LID },
  )
})

test('registra e atualiza a identidade usada pelo envio', () => {
  const mapa = new Map([[PN, JID_PN]])
  const identidade = registrarIdentidadeRecebida(mapa, {
    remoteJid: JID_LID,
    senderPn: `${PN}:0@s.whatsapp.net`,
  })

  assert.deepEqual(identidade, { numero: PN, jid: JID_LID })
  assert.equal(mapa.get(PN), JID_LID)
})

test('não inventa vínculo quando o telefone não acompanha o LID', () => {
  const mapa = new Map()
  assert.equal(
    registrarIdentidadeRecebida(mapa, { remoteJid: JID_LID }),
    null,
  )
  assert.equal(mapa.size, 0)
})

test('USync prefere LID e mantém PN como fallback legado', () => {
  assert.equal(
    escolherJidDaConsulta({ exists: true, jid: JID_PN, lid: JID_LID }, JID_PN),
    JID_LID,
  )
  assert.equal(
    escolherJidDaConsulta({ exists: true, jid: JID_PN }, JID_PN),
    JID_PN,
  )
  assert.equal(escolherJidDaConsulta(null, JID_PN), JID_PN)
})
