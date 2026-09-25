from __future__ import annotations

import unittest

from bot.inteligencia import avaliar_confianca
from bot.sessao import Sessao


class TestMemoriaEstruturada(unittest.TestCase):
    def test_dado_confirmado_nao_e_rebaixado_por_inferencia(self) -> None:
        sessao = Sessao(numero="5511999999999")
        self.assertTrue(
            sessao.lembrar(
                "empresa_contato",
                "Uau Supermarket",
                origem="usuario_captura",
                confianca=1.0,
            )
        )
        self.assertFalse(
            sessao.lembrar(
                "empresa_contato",
                "Outra Empresa",
                origem="ia_estruturada",
                confianca=0.82,
            )
        )
        self.assertEqual(sessao.dados["empresa_contato"], "Uau Supermarket")
        self.assertEqual(sessao.confianca_campo("empresa_contato"), 1.0)
    def test_memoria_exclui_metadados_internos(self) -> None:
        sessao = Sessao(numero="5511999999999")
        sessao.lembrar("produto", "MobConnect", origem="detector_local", confianca=1.0)

        memoria = sessao.memoria_estruturada()

        self.assertEqual(memoria["produto"], "MobConnect")
        self.assertNotIn("_memoria_meta", memoria)


class TestConfianca(unittest.TestCase):
    def test_alta_confiança_executa(self) -> None:
        decisao = avaliar_confianca(
            0.91, acao="encaminhar_comercial", tem_evidencia=True
        )
        self.assertTrue(decisao.executar)
        self.assertEqual(decisao.faixa, "alta")

    def test_media_confiança_pede_esclarecimento(self) -> None:
        decisao = avaliar_confianca(
            0.70, acao="responder", tem_evidencia=False
        )
        self.assertTrue(decisao.esclarecer)
        self.assertFalse(decisao.executar)
    def test_baixa_confiança_usa_fallback(self) -> None:
        decisao = avaliar_confianca(
            0.41, acao="responder", tem_evidencia=True
        )
        self.assertTrue(decisao.usar_fallback)
        self.assertFalse(decisao.executar)


if __name__ == "__main__":
    unittest.main()
