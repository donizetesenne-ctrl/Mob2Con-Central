"""
Demo: Análise Profunda de Dados com NVIDIA Nemotron Ultra 253B
Exemplos de uso para logística, varejo e dashboards Mob2Con.
"""

from nvidia_nim_client import NvidiaStack


def main():
    stack = NvidiaStack()
    print("🧠 NVIDIA Nemotron Ultra 253B — Análise Profunda")
    print("=" * 60)

    # Exemplo 1: Análise de KPIs
    print("\n📊 Exemplo 1: Análise de KPIs de logística")
    print("-" * 40)

    dados_exemplo = """
    | Rota | SLA Meta | SLA Real | Entregas | Devoluções |
    |------|----------|----------|----------|------------|
    | SP-RJ | 98% | 94.2% | 1.250 | 73 |
    | SP-MG | 97% | 96.8% | 890 | 28 |
    | SP-PR | 98% | 99.1% | 650 | 12 |
    | RJ-ES | 95% | 88.5% | 420 | 48 |
    | MG-BA | 93% | 91.2% | 380 | 33 |
    """

    resposta = stack.analisar(
        pergunta="Quais rotas estão abaixo da meta de SLA? Qual a causa provável e o que recomendar?",
        contexto=dados_exemplo
    )
    print(resposta)

    # Exemplo 2: Sugestão de medidas DAX
    print("\n\n📐 Exemplo 2: Sugestão de medidas DAX")
    print("-" * 40)

    resposta2 = stack.analisar(
        "Sugira 3 medidas DAX para um dashboard de Reposição Garantida "
        "que precisa mostrar: taxa de ruptura, tempo médio de reposição "
        "e percentual de lojas atendidas no prazo."
    )
    print(resposta2)

    # Exemplo 3: Interpretação de tendência
    print("\n\n📈 Exemplo 3: Interpretação de tendência")
    print("-" * 40)

    dados_tendencia = """
    Vendas mensais (últimos 6 meses):
    Jan: R$ 1.2M | Fev: R$ 1.1M | Mar: R$ 980K | Abr: R$ 1.05M | Mai: R$ 1.3M | Jun: R$ 1.45M
    Margem: Jan: 12% | Fev: 11% | Mar: 9% | Abr: 10% | Mai: 13% | Jun: 14%
    """

    resposta3 = stack.analisar(
        pergunta="Analise a tendência e identifique o ponto de inflexão. O que aconteceu em março?",
        contexto=dados_tendencia
    )
    print(resposta3)


if __name__ == "__main__":
    main()
