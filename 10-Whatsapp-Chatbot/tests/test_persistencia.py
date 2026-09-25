from __future__ import annotations

import asyncio
import sqlite3
import tempfile
import time
import unittest
from contextlib import closing
from pathlib import Path

from bot.persistencia import BancoSQLite
from bot.sessao import Sessao


class TestBancoSQLite(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self._temporario = tempfile.TemporaryDirectory()
        self.caminho = Path(self._temporario.name) / "chatbot.sqlite3"
        self.banco = BancoSQLite(self.caminho, ttl_segundos=300)

    async def asyncTearDown(self) -> None:
        await self.banco.fechar()
        self._temporario.cleanup()

    async def test_sessao_sobrevive_fechamento_e_reabertura(self) -> None:
        sessao = Sessao(
            numero="5511999999999",
            estado="lead_empresa",
            nome="Pessoa Teste",
            tentativas_invalidas=1,
            dados={"frente": "comercial_mobconnect", "segmento": "Indústria"},
            historico=[{"role": "user", "content": "Quero contratar"}],
        )
        await self.banco.salvar(sessao)
        await self.banco.fechar()

        self.banco = BancoSQLite(self.caminho, ttl_segundos=300)
        restaurada = await self.banco.obter(sessao.numero)

        self.assertIsNotNone(restaurada)
        assert restaurada is not None
        self.assertEqual(restaurada.estado, "lead_empresa")
        self.assertEqual(restaurada.nome, "Pessoa Teste")
        self.assertEqual(restaurada.tentativas_invalidas, 1)
        self.assertEqual(restaurada.dados["frente"], "comercial_mobconnect")
        self.assertEqual(restaurada.historico[0]["content"], "Quero contratar")

    async def test_sessao_expirada_e_removida(self) -> None:
        sessao = Sessao(numero="5511888888888", estado="financeiro")
        await self.banco.salvar(sessao)
        with closing(sqlite3.connect(self.caminho)) as conexao:
            conexao.execute(
                "UPDATE sessoes SET expira_em = ? WHERE numero = ?",
                (time.time() - 1, sessao.numero),
            )
            conexao.commit()
        self.assertIsNone(await self.banco.obter(sessao.numero))
        with closing(sqlite3.connect(self.caminho)) as conexao:
            total = conexao.execute(
                "SELECT COUNT(*) FROM sessoes WHERE numero = ?", (sessao.numero,)
            ).fetchone()[0]
        self.assertEqual(total, 0)

    async def test_pergunta_agrega_ocorrencias_e_redige_pii(self) -> None:
        pergunta = (
            "CPF 123.456.789-09, telefone (11) 99999-8888 e "
            "email pessoa@example.com: onde vejo meu documento?"
        )
        await asyncio.gather(
            *(
                self.banco.registrar_pergunta_nao_respondida(
                    pergunta,
                    estado="documentos",
                    frente="suporte",
                    motivo="ia_inativa",
                )
                for _ in range(5)
            )
        )

        itens = await self.banco.listar_perguntas_pendentes()
        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0]["ocorrencias"], 5)
        texto = itens[0]["pergunta"]
        self.assertIn("[CPF REDIGIDO]", texto)
        self.assertIn("[TELEFONE REDIGIDO]", texto)
        self.assertIn("[EMAIL REDIGIDO]", texto)
        self.assertNotIn("123.456.789-09", texto)
        self.assertNotIn("pessoa@example.com", texto)
        self.assertEqual(await self.banco.contar_perguntas_pendentes(), 1)

    async def test_perguntas_distintas_nao_sao_mescladas(self) -> None:
        await self.banco.registrar_pergunta_nao_respondida(
            "Como altero o roteiro?",
            estado="mobconnect",
            frente="suporte",
            motivo="ia_inativa",
        )
        await self.banco.registrar_pergunta_nao_respondida(
            "Como altero o roteiro?",
            estado="menu",
            frente="suporte",
            motivo="ia_inativa",
        )
        self.assertEqual(await self.banco.contar_perguntas_pendentes(), 2)

    async def test_mensagem_curta_demais_nao_vira_aprendizado(self) -> None:
        await self.banco.registrar_pergunta_nao_respondida(
            "O",
            estado="menu",
            motivo="primeira_mensagem_nao_classificada",
        )
        self.assertEqual(await self.banco.contar_perguntas_pendentes(), 0)



if __name__ == "__main__":
    unittest.main()
