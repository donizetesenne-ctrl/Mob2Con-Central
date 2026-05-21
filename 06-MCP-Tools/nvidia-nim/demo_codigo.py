"""
Demo: Geração de Código com NVIDIA Nemotron Super 49B
Exemplos de geração de apps, SQL, DAX e integrações.
"""

from nvidia_nim_client import NvidiaStack


def main():
    stack = NvidiaStack()
    print("💻 NVIDIA Nemotron Super 49B — Geração de Código")
    print("=" * 60)

    # Exemplo 1: Gerar app Streamlit
    print("\n🖥️ Exemplo 1: App Streamlit para dashboard")
    print("-" * 40)

    codigo1 = stack.gerar_codigo(
        "Crie um app Streamlit simples que lê um CSV com colunas "
        "'data', 'vendas', 'meta' e mostra: um gráfico de linha comparando "
        "vendas vs meta, e um card com o percentual de atingimento.",
        linguagem="python"
    )
    print(codigo1)

    # Exemplo 2: Gerar medida DAX
    print("\n\n📐 Exemplo 2: Medida DAX")
    print("-" * 40)

    codigo2 = stack.gerar_codigo(
        "Crie uma medida DAX chamada 'Taxa Ruptura %' que calcula "
        "o percentual de SKUs com estoque zero dividido pelo total de SKUs, "
        "filtrado pelo mês selecionado no slicer.",
        linguagem="dax"
    )
    print(codigo2)

    # Exemplo 3: Gerar query SQL para Redshift
    print("\n\n🗄️ Exemplo 3: Query SQL Redshift")
    print("-" * 40)

    codigo3 = stack.gerar_codigo(
        "Crie uma query SQL para Amazon Redshift que retorna as top 10 lojas "
        "com maior taxa de ruptura no último mês, incluindo nome_loja, "
        "total_skus, skus_ruptura e percentual. Tabelas: dim_loja, fato_estoque.",
        linguagem="sql"
    )
    print(codigo3)

    # Exemplo 4: Gerar API FastAPI
    print("\n\n🚀 Exemplo 4: Endpoint FastAPI")
    print("-" * 40)

    codigo4 = stack.gerar_codigo(
        "Crie um endpoint FastAPI POST /api/analisar que recebe um JSON "
        "com campo 'pergunta' (string) e 'dados' (string opcional), "
        "chama a API NVIDIA NIM e retorna a resposta.",
        linguagem="python"
    )
    print(codigo4)


if __name__ == "__main__":
    main()
