# Spec: Biblioteca de Medidas DAX Padrão Mob2Con

## Objetivo
Criar e manter uma biblioteca de medidas DAX reutilizáveis que seguem o padrão de nomenclatura e performance Mob2Con.

## Requisitos Funcionais

### REQ-1: Nomenclatura Padrão
- Prefixo por tipo: [Qtd], [R$], [%], [Avg], [Max], [Min], [Rank]
- Nome descritivo em português
- Sem espaços extras ou caracteres especiais
- Exemplos: [Qtd] Total Vendas, [R$] Faturamento, [%] Var MoM

### REQ-2: Categorias de Medidas
- **Contagem**: COUNTROWS, DISTINCTCOUNT
- **Soma**: SUM, SUMX
- **Percentual**: DIVIDE com tratamento de divisão por zero
- **Variação**: Período anterior (MoM, YoY, WoW)
- **Ranking**: RANKX com empates
- **Acumulado**: Running total (DATESYTD, TOTALYTD)
- **Condicional**: CALCULATE com filtros dinâmicos

### REQ-3: Performance
- Evitar iteradores desnecessários (SUMX quando SUM basta)
- Usar variáveis (VAR/RETURN) para cálculos intermediários
- Evitar FILTER() quando CALCULATETABLE basta
- Medidas não devem exceder 15 linhas

### REQ-4: Organização
- Todas as medidas na tabela _Medidas
- DisplayFolder por categoria (Vendas, Performance, Tempo)
- Descrição obrigatória em cada medida
- FormatString definido (0, #,##0, 0.0%, R$ #,##0.00)

### REQ-5: Documentação
- Manter `Mob2con-dax-medidas-padrao.md` atualizado
- Cada medida com: nome, expressão, descrição, uso

## Requisitos Não-Funcionais
- Compatível com Power BI Desktop e Service
- Testável via DAX query (EVALUATE)
- Reutilizável entre projetos (copiar tabela _Medidas)
