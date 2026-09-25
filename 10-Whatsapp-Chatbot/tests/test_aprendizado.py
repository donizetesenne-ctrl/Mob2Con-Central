from __future__ import annotations

import dataclasses
import unittest
from pathlib import Path

from bot.config import carregar_config
from bot.main import Aplicacao
from bot.mensagem import MensagemRecebida


def mensagem(texto: str, identificador: str) -> MensagemRecebida:
    return MensagemRecebida(
        id=identificador,
        jid="5511777777777@s.whatsapp.net",
        numero="5511777777777",
        nome="Contato Privado",
        texto=texto,
        de_mim=False,
        grupo=False,
        tem_midia=False,
        instancia="mob2con",
        tipo="conversation",
    )


class TestAprendizadoAplicacao(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        base = carregar_config()
        config = dataclasses.replace(
            base,
            sqlite_path=Path(":memory:"),
            llm=dataclasses.replace(base.llm, ativo=False, api_key=""),
            manuais=dataclasses.replace(base.manuais, ativo=False),
        )
        self.app = Aplicacao(config)
        self.enviadas: list[str] = []

        async def capturar(_numero: str, textos: list[str]) -> None:
            self.enviadas.extend(textos)

        async def sem_notificacao(_sessao) -> None:
            return None

        self.app._enviar = capturar
        self.app._notificar_time = sem_notificacao

    async def asyncTearDown(self) -> None:
        await self.app.encerrar()

    async def test_mensagens_nao_resolvidas_sao_agregadas(self) -> None:
        pergunta = "Como configuro uma regra inédita do projeto X?"
        for indice in range(4):
            await self.app.atender(mensagem(pergunta, f"m{indice}"))

        assert self.app.banco_sqlite is not None
        pendentes = await self.app.banco_sqlite.listar_perguntas_pendentes()
        self.assertEqual(len(pendentes), 1)
        self.assertEqual(pendentes[0]["ocorrencias"], 4)
        self.assertEqual(pendentes[0]["motivo"], "esgotou_tentativas")
        self.assertNotIn("5511777777777", pendentes[0]["pergunta"])
        self.assertNotIn("Contato Privado", pendentes[0]["pergunta"])

        sessao = await self.app.sessoes.obter("5511777777777")
        self.assertIsNotNone(sessao)
        assert sessao is not None
        self.assertTrue(sessao.pausada)


if __name__ == "__main__":
    unittest.main()
