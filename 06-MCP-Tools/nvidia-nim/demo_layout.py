"""
Demo: Análise de Layout com NVIDIA Nemotron Nano 12B VL (Multimodal)
Exemplos de análise visual de dashboards, wireframes e interfaces.
"""

from nvidia_nim_client import NvidiaStack
from pathlib import Path


def main():
    stack = NvidiaStack()
    print("🎨 NVIDIA Nemotron Nano 12B VL — Análise de Layout")
    print("=" * 60)

    # Exemplo 1: Análise textual (sem imagem)
    print("\n📋 Exemplo 1: Consultoria de layout (sem imagem)")
    print("-" * 40)

    resposta1 = stack.analisar_layout(
        pergunta=(
            "Tenho um dashboard Power BI 1280x720 com: "
            "header no topo (altura 80px), 4 cards KPI em linha abaixo, "
            "um gráfico de barras grande no centro, e uma tabela no rodapé. "
            "O fundo é branco e os cards usam laranja. "
            "Está seguindo o padrão Z-pattern? O que melhorar?"
        )
    )
    print(resposta1)

    # Exemplo 2: Análise de imagem (se existir screenshot)
    print("\n\n🖼️ Exemplo 2: Análise de screenshot")
    print("-" * 40)

    # Procura por screenshots no workspace
    screenshots_possiveis = [
        Path(__file__).parent.parent.parent / "03-Documentacao" / "screenshot_dashboard.png",
        Path(__file__).parent / "exemplo_layout.png",
    ]

    imagem_encontrada = None
    for path in screenshots_possiveis:
        if path.exists():
            imagem_encontrada = str(path)
            break

    if imagem_encontrada:
        print(f"Analisando: {imagem_encontrada}")
        resposta2 = stack.analisar_layout(
            imagem_path=imagem_encontrada,
            pergunta=(
                "Analise este dashboard Power BI. Verifique: "
                "1) Alinhamento dos visuais, "
                "2) Uso correto da cor laranja como primária, "
                "3) Hierarquia visual (Z-pattern), "
                "4) Espaçamento entre elementos. "
                "Dê nota de 1 a 10 e sugira 3 melhorias."
            )
        )
        print(resposta2)
    else:
        print("Nenhum screenshot encontrado para análise.")
        print("Para testar, coloque um PNG de dashboard nesta pasta como 'exemplo_layout.png'")
        print("\nTestando com descrição textual...")

        resposta2 = stack.analisar_layout(
            pergunta=(
                "Descreva o layout ideal para um dashboard executivo Mob2Con "
                "em canvas 1280x720, usando Z-pattern, com header, "
                "4 KPIs, 2 gráficos e filtros laterais. "
                "Dê as coordenadas x, y, width, height de cada elemento."
            )
        )
        print(resposta2)

    # Exemplo 3: Sugestão de paleta
    print("\n\n🎨 Exemplo 3: Validação de paleta de cores")
    print("-" * 40)

    resposta3 = stack.analisar_layout(
        pergunta=(
            "Valide esta paleta para um dashboard de logística: "
            "Primária: #F46901 (laranja), Secundária: #2D2D2D (cinza escuro), "
            "Background: #F5F5F5, Sucesso: #28A745, Alerta: #FFC107, "
            "Erro: #DC3545. A fonte é Raleway. "
            "Está acessível (WCAG AA)? Sugira ajustes se necessário."
        )
    )
    print(resposta3)


if __name__ == "__main__":
    main()
