"""
NVIDIA NIM - Gerador de Medidas DAX para Mob2Con
Usa IA gratuita para gerar medidas DAX otimizadas

Uso:
    python nvidia_dax_generator.py "variação mês anterior de faturamento"
    python nvidia_dax_generator.py "ranking top 10 produtos por venda"
    python nvidia_dax_generator.py "acumulado ano até a data"
"""

import sys
from nvidia_chat import chat, load_config

SYSTEM_PROMPT_DAX = """Você é um especialista senior em DAX (Data Analysis Expressions) para Power BI.

REGRAS OBRIGATÓRIAS:
1. Nomenclatura Mob2Con: prefixo [Qtd], [R$], [%], [Avg], [Max], [Min], [Rank]
2. Use VAR/RETURN para legibilidade
3. Use DIVIDE() em vez de divisão direta (trata zero)
4. Prefira SUM sobre SUMX quando possível
5. Prefira CALCULATE sobre FILTER para filtros simples
6. Máximo 15 linhas por medida
7. Comente o que a medida faz

FORMATO DE RESPOSTA:
```dax
// Descrição da medida
[Prefixo] Nome da Medida = 
VAR _variavel = expressão
RETURN
    resultado
```

FormatString sugerido: (ex: "#,##0", "0.0%", "R$ #,##0.00")
"""


def gerar_dax(descricao):
    """Gera medida DAX a partir de descrição em linguagem natural"""
    prompt = f"Crie uma medida DAX para: {descricao}"
    return chat(prompt, system_prompt=SYSTEM_PROMPT_DAX)


def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("  NVIDIA NIM - Gerador de Medidas DAX Mob2Con")
        print("=" * 60)
        print()
        print("Uso: python nvidia_dax_generator.py \"descrição da medida\"")
        print()
        print("Exemplos:")
        print('  "variação percentual mês anterior"')
        print('  "ranking top 10 lojas por faturamento"')
        print('  "acumulado do ano até a data atual"')
        print('  "média móvel 3 meses de vendas"')
        print('  "contagem de lojas com venda > 0"')
        sys.exit(0)
    
    descricao = " ".join(sys.argv[1:])
    
    print(f"🎯 Gerando medida DAX para: {descricao}")
    print("-" * 60)
    
    resultado = gerar_dax(descricao)
    print(resultado)
    print("-" * 60)
    print("✅ Copie a medida e cole no Power BI Desktop")


if __name__ == "__main__":
    main()
