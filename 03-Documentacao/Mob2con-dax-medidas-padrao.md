# 📊 Mob2Con — Biblioteca DAX Padrão

> Medidas DAX reutilizáveis para dashboards Mob2Con.
> Copie e cole direto na tab **Measures** do Power BI.

---

## 💰 KPIs Financeiros

### Receita Total
```DAX
Receita Total = 
SUM('fVendas'[ValorLiquido])
```

### Receita Ano Anterior (YoY)
```DAX
Receita AA = 
CALCULATE(
    [Receita Total],
    SAMEPERIODLASTYEAR('dCalendario'[Data])
)
```

### Crescimento % YoY
```DAX
Crescimento YoY % = 
VAR Atual = [Receita Total]
VAR Anterior = [Receita AA]
RETURN
IF(
    Anterior = 0 || ISBLANK(Anterior),
    BLANK(),
    DIVIDE(Atual - Anterior, Anterior)
)
```

### Meta de Receita (mensal)
```DAX
Meta Receita = 
SUM('fMetas'[ValorMeta])
```

### % Atingimento Meta
```DAX
% Atingimento = 
DIVIDE([Receita Total], [Meta Receita], 0)
```

---

## 📦 KPIs Operacionais (Varejo / Promotores)

### Total de Promotores Ativos
```DAX
Promotores Ativos = 
CALCULATE(
    DISTINCTCOUNT('fVisitas'[IdPromotor]),
    'fVisitas'[Status] = "Ativo"
)
```

### Visitas no Período
```DAX
Total Visitas = 
COUNTROWS('fVisitas')
```

### Tempo Médio de Visita (minutos)
```DAX
Tempo Médio Visita (min) = 
AVERAGE('fVisitas'[DuracaoMinutos])
```

### % Ruptura
```DAX
% Ruptura = 
VAR ItensRuptura = 
    CALCULATE(
        COUNTROWS('fEstoque'),
        'fEstoque'[Situacao] = "Ruptura"
    )
VAR ItensTotal = COUNTROWS('fEstoque')
RETURN
DIVIDE(ItensRuptura, ItensTotal, 0)
```

### Sell Out por Loja
```DAX
Sell Out Total = 
SUM('fSellOut'[QuantidadeVendida])
```

---

## 📅 Medidas de Tempo (Time Intelligence)

### Receita MTD (Month To Date)
```DAX
Receita MTD = 
CALCULATE(
    [Receita Total],
    DATESMTD('dCalendario'[Data])
)
```

### Receita YTD (Year To Date)
```DAX
Receita YTD = 
CALCULATE(
    [Receita Total],
    DATESYTD('dCalendario'[Data])
)
```

### Média Móvel 3 Meses
```DAX
Receita Média 3M = 
AVERAGEX(
    DATESINPERIOD(
        'dCalendario'[Data],
        LASTDATE('dCalendario'[Data]),
        -3,
        MONTH
    ),
    [Receita Total]
)
```

### Rank de Produto por Vendas
```DAX
Rank Produto = 
RANKX(
    ALL('dProduto'[Produto]),
    [Receita Total],
    ,
    DESC,
    Dense
)
```

---

## 🚦 Medidas Condicionais (Semáforos / Alertas)

### Status Meta (Verde/Amarelo/Vermelho)
```DAX
Status Meta = 
VAR Atingimento = [% Atingimento]
RETURN
SWITCH(
    TRUE(),
    Atingimento >= 1,      "🟢 Atingida",
    Atingimento >= 0.8,    "🟡 Em risco",
    Atingimento < 0.8,     "🔴 Abaixo"
)
```

### Cor Dinâmica (para conditional formatting)
```DAX
Cor Status = 
VAR Atingimento = [% Atingimento]
RETURN
SWITCH(
    TRUE(),
    Atingimento >= 1,      "#107C41",
    Atingimento >= 0.8,    "#F46901",
    "#C00000"
)
```

Uso: Campo → Conditional formatting → Background color → Field value → `Cor Status`

### Alerta Ruptura Alta
```DAX
Alerta Ruptura = 
IF(
    [% Ruptura] > 0.15,
    "⚠ ALERTA: Ruptura acima de 15%",
    ""
)
```

---

## 🔢 Formatadores de Texto

### Valor em formato compacto (K/M/B)
```DAX
Receita Compacta = 
VAR V = [Receita Total]
RETURN
SWITCH(
    TRUE(),
    V >= 1000000000, FORMAT(V/1000000000, "0.0") & " B",
    V >= 1000000,    FORMAT(V/1000000, "0.0") & " M",
    V >= 1000,       FORMAT(V/1000, "0.0") & " K",
    FORMAT(V, "0")
)
```

### Variação formatada com seta
```DAX
Variação Formatada = 
VAR Diff = [Receita Total] - [Receita AA]
VAR Pct = DIVIDE(Diff, [Receita AA], 0)
VAR Seta = IF(Diff >= 0, "▲", "▼")
RETURN
Seta & " " & FORMAT(ABS(Pct), "0.0%")
```

---

## 📊 Medidas Auxiliares de Modelagem

### Contagem Distinta Segura
```DAX
Clientes Únicos = 
DISTINCTCOUNTNOBLANK('fVendas'[IdCliente])
```

### Última Data de Atualização
```DAX
Última Atualização = 
FORMAT(
    MAX('dAtualizacao'[DataHora]),
    "dd/MM/yyyy HH:mm"
)
```

### Título Dinâmico da Página
```DAX
Título Página = 
"Análise de " & SELECTEDVALUE('dPeriodo'[Periodo], "Todos os períodos")
```

---

## 🎯 Padrões de Nomeclatura

### Tabelas
- `f<Nome>` → fato (ex: `fVendas`, `fEstoque`)
- `d<Nome>` → dimensão (ex: `dCalendario`, `dProduto`, `dLoja`)
- `_<Nome>` → auxiliar/medida sem dados (ex: `_Medidas`)

### Medidas
- Usar **espaços** nos nomes (o DAX permite com colchetes)
- Indicadores % sempre terminam em ` %`
- Valores monetários NUNCA têm "R$" no nome (é formato)
- Contagens: "Total de X" ou "X Único(s)"

### Colunas calculadas
- PascalCase sem espaço (ex: `AnoMes`, `FaixaEtaria`)

---

## 🔗 Relacionamentos padrão

Para projeto Mob2Con típico:

```
dCalendario[Data] ─1:*─→ fVendas[Data]
dCalendario[Data] ─1:*─→ fVisitas[DataVisita]
dCalendario[Data] ─1:*─→ fEstoque[DataSnapshot]

dLoja[IdLoja] ─1:*─→ fVendas[IdLoja]
dLoja[IdLoja] ─1:*─→ fVisitas[IdLoja]
dLoja[IdLoja] ─1:*─→ fEstoque[IdLoja]

dProduto[IdProduto] ─1:*─→ fVendas[IdProduto]
dProduto[IdProduto] ─1:*─→ fEstoque[IdProduto]

dPromotor[IdPromotor] ─1:*─→ fVisitas[IdPromotor]

dRede[IdRede] ─1:*─→ dLoja[IdRede]      (hierarquia)
dCategoria[IdCategoria] ─1:*─→ dProduto[IdCategoria]  (hierarquia)
```

### Cardinalidade
- **1:\*** = sempre que possível (dimensão → fato)
- **\*:\*** = evitar, só se absolutamente necessário
- **Direção do filtro:** sempre `Single` (Both só em casos específicos)

---

## ⚡ Performance — Dicas

1. **Evitar `FILTER()` desnecessário** — usar filtros booleanos no CALCULATE
2. **Usar `SUMX` com cuidado** — prefira `SUM` quando possível
3. **Medidas em tabela `_Medidas`** — fica mais organizado que medidas em tabelas fato
4. **Relacionamentos inativos** — usar `USERELATIONSHIP` quando precisar de calendário alternativo
5. **`DIVIDE(a, b, 0)`** em vez de `a/b` — evita erro de divisão por zero
