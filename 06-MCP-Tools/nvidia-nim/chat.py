"""
Chat Interativo — NVIDIA NIM Mob2Con
Abre no CMD e você conversa com os 3 modelos.
Comandos:
  /analise  → muda para modelo de análise de dados
  /codigo   → muda para modelo de geração de código
  /layout   → muda para modelo de layout/visual
  /sair     → encerra o chat
"""

from nvidia_nim_client import NvidiaStack


def main():
    print()
    print("=" * 60)
    print("  🤖 CHAT NVIDIA NIM — Mob2Con")
    print("  3 IAs gratuitas no seu terminal")
    print("=" * 60)
    print()
    print("  Modelos disponíveis:")
    print("    /analise  → Llama 3.3 70B (dados, KPIs, insights)")
    print("    /codigo   → Nemotron Super 49B (Python, SQL, DAX)")
    print("    /layout   → Nemotron Nano 12B VL (visual, UI)")
    print()
    print("  Comandos: /sair para encerrar")
    print("-" * 60)

    try:
        stack = NvidiaStack()
    except Exception as e:
        print(f"\n❌ Erro ao conectar: {e}")
        return

    modelo_atual = "analise"
    nomes = {
        "analise": "🧠 Análise (Llama 3.3 70B)",
        "codigo": "💻 Código (Nemotron Super 49B)",
        "layout": "🎨 Layout (Nemotron Nano 12B VL)"
    }

    historico = []

    print(f"\n  Modelo ativo: {nomes[modelo_atual]}")
    print()

    while True:
        try:
            pergunta = input("Você > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Até mais!")
            break

        if not pergunta:
            continue

        # Comandos
        if pergunta.lower() == "/sair":
            print("\n👋 Até mais!")
            break
        elif pergunta.lower() == "/analise":
            modelo_atual = "analise"
            historico = []
            print(f"\n  ✅ Mudou para: {nomes[modelo_atual]}\n")
            continue
        elif pergunta.lower() == "/codigo":
            modelo_atual = "codigo"
            historico = []
            print(f"\n  ✅ Mudou para: {nomes[modelo_atual]}\n")
            continue
        elif pergunta.lower() == "/layout":
            modelo_atual = "layout"
            historico = []
            print(f"\n  ✅ Mudou para: {nomes[modelo_atual]}\n")
            continue
        elif pergunta.lower() == "/limpar":
            historico = []
            print("\n  🗑️ Histórico limpo.\n")
            continue

        # Enviar para o modelo
        print(f"\n  [{nomes[modelo_atual]}] pensando...\n")

        try:
            resposta = stack.chat(
                mensagem=pergunta,
                modelo_tipo=modelo_atual,
                historico=historico
            )

            # Guardar no histórico
            historico.append({"role": "user", "content": pergunta})
            historico.append({"role": "assistant", "content": resposta})

            # Limitar histórico a 10 mensagens
            if len(historico) > 20:
                historico = historico[-20:]

            print(f"IA > {resposta}\n")

        except Exception as e:
            print(f"\n  ❌ Erro: {e}\n")


if __name__ == "__main__":
    main()
