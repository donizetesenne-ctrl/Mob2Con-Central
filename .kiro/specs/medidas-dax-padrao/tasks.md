# Tasks: Biblioteca de Medidas DAX Padrão

## Task 1: Criar tabela _Medidas
- [ ] Criar tabela calculada vazia: `_Medidas = {BLANK()}`
- [ ] Ocultar a coluna Value
- [ ] Definir como tabela de medidas padrão

## Task 2: Medidas de Contagem
- [ ] [Qtd] Total = COUNTROWS(fTabela)
- [ ] [Qtd] Distintos = DISTINCTCOUNT(fTabela[ID])
- [ ] [Qtd] Com Filtro = CALCULATE([Qtd] Total, filtro)

## Task 3: Medidas de Valor
- [ ] [R$] Faturamento = SUM(fTabela[Valor])
- [ ] [R$] Custo = SUM(fTabela[Custo])
- [ ] [R$] Margem = [R$] Faturamento - [R$] Custo
- [ ] [Avg] Ticket Médio = DIVIDE([R$] Faturamento, [Qtd] Total)

## Task 4: Medidas de Variação
- [ ] [%] Var MoM = DIVIDE([R$] Atual - [R$] Anterior, [R$] Anterior)
- [ ] [%] Var YoY = variação ano anterior
- [ ] [R$] Acumulado YTD = TOTALYTD([R$] Faturamento, dCalendario[Data])
- [ ] [R$] Média Móvel 3M = AVERAGEX(últimos 3 meses)

## Task 5: Medidas de Ranking
- [ ] [Rank] Top Produtos = RANKX(ALL(dProduto), [R$] Faturamento)
- [ ] [Rank] Top Clientes = RANKX(ALL(dCliente), [R$] Faturamento)
- [ ] Filtro Top N dinâmico com parâmetro

## Task 6: Validação e documentação
- [ ] Testar cada medida via EVALUATE no MCP powerbi-bridge
- [ ] Verificar performance (< 1s por medida)
- [ ] Atualizar `Mob2con-dax-medidas-padrao.md`
- [ ] Definir FormatString para cada medida
