from __future__ import annotations

import dataclasses
import tempfile
import unittest
from pathlib import Path

from bot.config import carregar_config
from bot.main import Aplicacao
from bot.mensagem import MensagemRecebida
from bot.sessao import Sessao


MANUAL = """# Anexo de Documentos

> Origem: `MobControl/Guias/Anexo de Documentos.pdf`
> Paginas: 2

## Pagina 1

Status da Documentação
A marcação vermelha identifica documentos vencidos e a amarela identifica
documentos pendentes.

## Pagina 2

Regularizando Documentação
Selecione o promotor, abra o painel de documentos e clique em Arquivos para
realizar o upload. Informe a data de emissão quando houver validade.
"""


def mensagem(texto: str, identificador: str = "manual-1") -> MensagemRecebida:
    return MensagemRecebida(
        id=identificador,
        jid="5511777777777@s.whatsapp.net",
        numero="5511777777777",
        nome="Contato Teste",
        texto=texto,
        de_mim=False,
        grupo=False,
        tem_midia=False,
        instancia="mob2con",
        tipo="conversation",
    )


class TestIntegracaoManuais(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        docs = raiz / "docs" / "MobControl" / "Guias Indústrias Agências"
        docs.mkdir(parents=True)
        (docs / "Anexo de Documentos.md").write_text(MANUAL, encoding="utf-8")

        base = carregar_config()
        config = dataclasses.replace(
            base,
            sqlite_path=raiz / "chatbot.sqlite3",
            llm=dataclasses.replace(base.llm, ativo=False, api_key=""),
            manuais=dataclasses.replace(
                base.manuais,
                ativo=True,
                diretorio=raiz / "docs",
                indice_path=raiz / "manuais.sqlite3",
            ),
        )
        self.app = Aplicacao(config)
        self.enviadas: list[str] = []

        async def capturar(_numero: str, textos: list[str]) -> None:
            self.enviadas.extend(textos)

        async def sem_notificacao(_sessao: Sessao) -> None:
            return None

        self.app._enviar = capturar
        self.app._notificar_time = sem_notificacao

    async def asyncTearDown(self) -> None:
        await self.app.encerrar()
        self.tmp.cleanup()

    async def test_responde_pelo_manual_sem_opcao_invalida(self) -> None:
        sessao = Sessao(
            numero="5511777777777",
            estado="acesso_motivos",
            dados={"frente": "suporte"},
        )
        await self.app.sessoes.salvar(sessao)

        await self.app.atender(
            mensagem("como regularizar documento vencido pelo anexo?")
        )

        resposta = "\n".join(self.enviadas)
        self.assertIn("manuais da Mob2Con", resposta)
        self.assertIn("Arquivos", resposta)
        self.assertIn("*Fonte:* Anexo de Documentos", resposta)
        self.assertNotIn("Não identifiquei essa opção", resposta)

        restaurada = await self.app.sessoes.obter("5511777777777")
        assert restaurada is not None
        self.assertEqual(restaurada.tentativas_invalidas, 0)
        assert self.app.banco_sqlite is not None
        self.assertEqual(await self.app.banco_sqlite.contar_perguntas_pendentes(), 0)

    async def test_promotor_nao_recebe_tela_de_gestor(self) -> None:
        sessao = Sessao(
            numero="5511777777777",
            estado="acesso_promotor",
            dados={"frente": "promotor"},
        )
        await self.app.sessoes.salvar(sessao)

        await self.app.atender(mensagem("como faço upload do documento?", "manual-2"))

        resposta = "\n".join(self.enviadas)
        self.assertNotIn("*Fonte:*", resposta)
        self.assertNotIn("clique em Arquivos", resposta)


if __name__ == "__main__":
    unittest.main()
