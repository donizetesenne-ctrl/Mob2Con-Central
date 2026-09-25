from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path

from bot.conhecimento import IndiceManuais


MANUAL_DOCUMENTOS = """# Anexo de Documentos

> Origem: `MobControl/Guias/Anexo de Documentos.pdf`
> Paginas: 3

## Pagina 1

The explanation was created in Stonly
Version 5
Page 1

## Pagina 2

Status da Documentação
Caso o status esteja irregular, a marcação será vermelha para documentos
vencidos e amarela para documentos pendentes.
Go to Page 3

## Pagina 3

Regularizando Documentação
Selecione o promotor e clique em Arquivos para realizar o upload da foto do
documento. Informe a data de emissão quando o documento possuir validade.
You have reached the end of this guide
Try out https://stonly.com to create interactive step-by-step guides
"""

MANUAL_ROTEIROS = """# Agência_Roteiros

> Origem: `MobConnect/Agência/Agência_Roteiros.pdf`
> Paginas: 2

## Pagina 1

Roteiros
Na Página de Roteiros você pode editar as rotas dos promotores e pesquisar o
roteiro semanal.

## Pagina 2

Espelhamento de Roteiro
Selecione o roteiro de origem, escolha o promotor de destino e clique em Salvar.
Você pode substituir o roteiro atual ou apenas adicionar novas visitas.
"""

PLANILHA = """# Funcionalidades

> Origem: `Funcionalidades.xlsx`

## Aba: Check

| tenant | owner type | feature title | Check |
|---|---|---|---|
| mobcontrol | supplier | Consultar documentos pendentes | True |
| mobcontrol | supplier | Funcionalidade secreta não entregue | False |
"""


class TestIndiceManuais(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name) / "docs"
        (self.raiz / "MobControl" / "Guias Indústrias Agências").mkdir(
            parents=True
        )
        (self.raiz / "MobConnect" / "Agência").mkdir(parents=True)
        self.documentos = (
            self.raiz
            / "MobControl"
            / "Guias Indústrias Agências"
            / "Anexo de Documentos.md"
        )
        self.roteiros = (
            self.raiz / "MobConnect" / "Agência" / "Agência_Roteiros.md"
        )
        self.planilha = self.raiz / "Funcionalidades.md"
        self.documentos.write_text(MANUAL_DOCUMENTOS, encoding="utf-8")
        self.roteiros.write_text(MANUAL_ROTEIROS, encoding="utf-8")
        self.planilha.write_text(PLANILHA, encoding="utf-8")
        self.indice = IndiceManuais(
            self.raiz,
            Path(self.tmp.name) / "manuais.sqlite3",
        )

    def tearDown(self) -> None:
        self.indice.fechar()
        self.tmp.cleanup()

    def test_indexa_limpa_e_recupera_documentos(self) -> None:
        relatorio = self.indice.indexar()
        self.assertEqual(relatorio.documentos, 3)
        self.assertGreaterEqual(relatorio.chunks, 4)
        self.assertEqual(relatorio.adicionados_ou_atualizados, 3)

        resultados = self.indice.buscar("documento vencido ou pendente")
        self.assertTrue(resultados)
        self.assertEqual(
            resultados[0].titulo,
            "Anexo de Documentos",
            [(item.titulo, item.produto, item.relevancia) for item in resultados],
        )
        self.assertNotIn("Stonly", resultados[0].conteudo)
        self.assertNotIn("Go to Page", resultados[0].conteudo)

        resposta = self.indice.responder("como regularizar documento vencido?")
        self.assertIsNotNone(resposta)
        assert resposta is not None
        self.assertIn("*Fonte:*", resposta)
        self.assertIn("Anexo de Documentos", resposta)
        self.assertNotIn(str(self.raiz), resposta)
        self.assertNotIn("stonly.com", resposta)

    def test_recupera_procedimento_de_roteiro(self) -> None:
        self.indice.indexar()
        resposta = self.indice.responder("como espelhar roteiro para outro promotor")
        self.assertIsNotNone(resposta)
        assert resposta is not None
        self.assertIn("Selecione o roteiro de origem", resposta)
        self.assertIn("Agência Roteiros", resposta)

    def test_nao_responde_ruido_nem_linha_false(self) -> None:
        self.indice.indexar()
        self.assertIsNone(self.indice.responder("abacaxi quântico submarino"))
        self.assertIsNone(self.indice.responder("funcionalidade secreta não entregue"))
        self.assertEqual(self.indice.buscar('" OR * NOT'), [])

    def test_planilha_true_permanece_pesquisavel(self) -> None:
        self.indice.indexar()
        resultados = self.indice.buscar("consultar documentos pendentes")
        self.assertTrue(resultados)
        self.assertNotIn("Funcionalidade secreta", " ".join(r.conteudo for r in resultados))

    def test_indexacao_incremental_e_remocao(self) -> None:
        primeira = self.indice.indexar()
        segunda = self.indice.indexar()
        self.assertEqual(segunda.adicionados_ou_atualizados, 0)
        self.assertEqual(segunda.inalterados, primeira.documentos)

        time.sleep(0.01)
        self.roteiros.write_text(
            MANUAL_ROTEIROS + "\nNovo procedimento de visita planejada.\n",
            encoding="utf-8",
        )
        terceira = self.indice.indexar()
        self.assertEqual(terceira.adicionados_ou_atualizados, 1)

        self.planilha.unlink()
        quarta = self.indice.indexar()
        self.assertEqual(quarta.removidos, 1)
        self.assertEqual(quarta.documentos, 2)

    def test_resposta_de_conta_nao_ecoa_pii_nem_inventa_status(self) -> None:
        self.indice.indexar()
        resposta = self.indice.responder(
            "meu CPF 123.456.789-09 está com documento pendente?"
        )
        self.assertIsNotNone(resposta)
        assert resposta is not None
        self.assertIn("Não consigo consultar sua conta daqui", resposta)
        self.assertNotIn("123.456.789-09", resposta)
        self.assertLessEqual(len(resposta), 1350)

    def test_status_declara_fts5(self) -> None:
        self.indice.indexar()
        status = self.indice.status()
        self.assertTrue(status["fts5"])
        self.assertEqual(status["documentos"], 3)
        self.assertGreater(status["chunks"], 0)


if __name__ == "__main__":
    unittest.main()
