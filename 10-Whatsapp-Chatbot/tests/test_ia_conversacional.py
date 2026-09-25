from __future__ import annotations

import dataclasses
import unittest
from pathlib import Path

from bot.config import carregar_config
from bot.llm import AnaliseConversa, ClienteLLM
from bot.main import Aplicacao
from bot.sessao import Sessao


class FakeLLM:
    ativo = True

    def __init__(self, analise: AnaliseConversa) -> None:
        self.analise = analise

    async def analisar(self, *_args, **_kwargs) -> AnaliseConversa:
        return self.analise

    async def fechar(self) -> None:
        return None


class TestParserIA(unittest.TestCase):
    def test_json_estruturado_e_tolerante_a_markdown(self) -> None:
        bruto = """```json
{"intencao":"mobconnect_conhecer","confianca":0.91,
"acao":"responder","resposta":"MobConnect organiza a execução em campo.",
"campos":{"empresa_contato":"Uau Supermarket","invalido":"x"}}
```"""
        analise = ClienteLLM._analise_do_json(bruto)
        self.assertIsNotNone(analise)
        assert analise is not None
        self.assertEqual(analise.acao, "responder")
        self.assertEqual(analise.campos["empresa_contato"], "Uau Supermarket")
        self.assertNotIn("invalido", analise.campos)


class TestIAEstruturadaAplicacao(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        base = carregar_config()
        config = dataclasses.replace(
            base,
            sqlite_path=Path(":memory:"),
            manuais=dataclasses.replace(base.manuais, ativo=False),
        )
        self.app = Aplicacao(config)

    async def asyncTearDown(self) -> None:
        await self.app.encerrar()

    async def test_curiosidade_responde_sem_virar_formulario(self) -> None:
        self.app.llm = FakeLLM(
            AnaliseConversa(
                intencao="mobconnect_conhecer",
                confianca=0.94,
                acao="responder",
                resposta=(
                    "O MobConnect organiza planejamento, execução em campo "
                    "e leitura dos resultados."
                ),
                campos={"empresa_contato": "Uau Supermarket"},
            )
        )
        sessao = Sessao(numero="5511999999999", estado="menu")

        resposta = await self.app._tentar_ia_estruturada(
            sessao, "Tenho curiosidade sobre o MobConnect"
        )

        self.assertIsNotNone(resposta)
        assert resposta is not None
        self.assertFalse(resposta.transferir)
        self.assertIn("planejamento", resposta.mensagens[0])
        self.assertEqual(sessao.dados["empresa_contato"], "Uau Supermarket")
        self.assertEqual(sessao.estado, "mobconnect_comercial")

    async def test_comercial_com_contexto_nao_repete_cadastro(self) -> None:
        self.app.llm = FakeLLM(
            AnaliseConversa(
                intencao="mobconnect_comercial",
                confianca=0.96,
                acao="encaminhar_comercial",
                resposta="Entendi o cenário e posso encaminhar ao comercial.",
                campos={
                    "empresa_contato": "Uau Supermarket",
                    "segmento": "Rede varejista",
                    "porte": "1 loja e 10 promotores",
                },
            )
        )
        sessao = Sessao(numero="5511999999999", estado="mobconnect_comercial")

        resposta = await self.app._tentar_ia_estruturada(
            sessao,
            "Sou da Uau Supermarket, temos 1 loja e 10 promotores. Quero proposta.",
        )

        self.assertIsNotNone(resposta)
        assert resposta is not None
        self.assertTrue(resposta.transferir)
        self.assertEqual(sessao.dados["empresa_contato"], "Uau Supermarket")
        self.assertIn("1 loja", sessao.dados["porte"])
        self.assertIn("Uau Supermarket", sessao.dados["contexto_comercial"])


if __name__ == "__main__":
    unittest.main()
