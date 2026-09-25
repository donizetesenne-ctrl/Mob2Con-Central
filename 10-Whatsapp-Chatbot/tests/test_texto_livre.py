from __future__ import annotations

import unittest
from pathlib import Path

from bot.config import carregar_config
from bot.fluxo import MotorFluxo
from bot.sessao import Sessao


RAIZ = Path(__file__).resolve().parents[1]


class TestTextoLivre(unittest.TestCase):
    def setUp(self) -> None:
        self.motor = MotorFluxo(
            RAIZ / "bot" / "fluxo-mob2con.json",
            carregar_config().atendimento,
        )

    def nova_sessao(self) -> Sessao:
        sessao = Sessao(numero="5511999999999", nome="Teste")
        self.motor.iniciar(sessao, dentro_do_horario=True)
        return sessao

    def test_frase_do_print_vira_desambiguacao_util(self) -> None:
        sessao = self.nova_sessao()

        resposta = self.motor.processar(sessao, "quewro ajudar promotor")
        texto = "\n".join(resposta.mensagens)

        self.assertEqual(sessao.estado, "promotor_ajuda")
        self.assertIn("o que está acontecendo com o promotor", texto.lower())
        self.assertNotIn("Não identifiquei essa opção", texto)
        self.assertNotIn("Quero conhecer a plataforma", texto)

    def test_typos_fortes_ainda_identificam_acesso(self) -> None:
        sessao = self.nova_sessao()

        resposta = self.motor.processar(
            sessao,
            "meu promotro nao comsegue acessa a loha",
        )
        texto = "\n".join(resposta.mensagens)

        self.assertEqual(sessao.estado, "acesso_quem")
        self.assertIn("documentação", texto.lower())
        self.assertFalse(resposta.usar_llm)

    def test_typo_em_fatura_chega_ao_financeiro(self) -> None:
        sessao = self.nova_sessao()

        resposta = self.motor.processar(
            sessao,
            "pressiso da seguda via da fatrura",
        )
        texto = "\n".join(resposta.mensagens)

        self.assertEqual(sessao.estado, "financeiro")
        self.assertIn("99886-8868", texto)
        self.assertFalse(resposta.usar_llm)

    def test_texto_livre_pode_trocar_assunto_sem_voltar_ao_menu(self) -> None:
        sessao = self.nova_sessao()
        self.motor.processar(sessao, "1")
        self.assertEqual(sessao.estado, "acesso_quem")

        resposta = self.motor.processar(sessao, "agora quero ver minha fatrura")

        self.assertEqual(sessao.estado, "financeiro")
        self.assertIn("Financeiro", "\n".join(resposta.mensagens))

    def test_fallback_de_texto_nao_acusa_opcao_invalida(self) -> None:
        sessao = self.nova_sessao()
        pendente = self.motor.processar(sessao, "abacaxi quântico submarino")
        self.assertTrue(pendente.usar_llm)

        resposta = self.motor.resposta_menu_apos_erro(
            sessao,
            "abacaxi quântico submarino",
        )
        texto = "\n".join(resposta.mensagens)

        self.assertNotIn("Não identifiquei essa opção", texto)
        self.assertIn("descreva", texto.lower())

    def test_numero_invalido_continua_sendo_tratado_como_numero(self) -> None:
        sessao = self.nova_sessao()

        resposta = self.motor.resposta_menu_apos_erro(sessao, "77")

        self.assertIn("Não identifiquei essa opção", "\n".join(resposta.mensagens))


if __name__ == "__main__":
    unittest.main()
