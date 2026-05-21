# Design: Biblioteca de Medidas DAX Padrão

## Estrutura da Tabela _Medidas

```
_Medidas (tabela calculada)
├── DisplayFolder: "Contagem"
│   ├── [Qtd] Total
│   ├── [Qtd] Distintos
│   └── [Qtd] Com Filtro
├── DisplayFolder: "Valor"
│   ├── [R$] Faturamento
│   ├── [R$] Custo
│   ├── [R$] Margem
│   └── [Avg] Ticket Médio
├── DisplayFolder: "Variação"
│   ├── [%] Var MoM
│   ├── [%] Var YoY
│   ├── [R$] Acumulado YTD
│   └── [R$] Média Móvel 3M
└── DisplayFolder: "Ranking"
    ├── [Rank] Top Produtos
    └── [Rank] Top Clientes
```

## Padrão de Código DAX

```dax
// Padrão: usar VAR/RETURN para legibilidade
[%] Var MoM = 
VAR _Atual = [R$] Faturamento
VAR _Anterior = CALCULATE(
    [R$] Faturamento,
    DATEADD(dCalendario[Data], -1, MONTH)
)
RETURN
    DIVIDE(_Atual - _Anterior, _Anterior, 0)
```

## MCPs Utilizados
- **powerbi-bridge**: Criar medidas via measure_operations
- **powerbi-bridge**: Validar via dax_query_operations (EVALUATE)
- **filesystem**: Atualizar documentação markdown

## Regras de Performance
1. SUM > SUMX (quando possível)
2. CALCULATE > FILTER (para filtros simples)
3. VAR/RETURN > expressões aninhadas
4. DIVIDE > divisão direta (trata zero)
5. Máximo 15 linhas por medida
6. Sem FILTER(ALL()) quando REMOVEFILTERS basta
