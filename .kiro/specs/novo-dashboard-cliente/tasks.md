# Tasks: Novo Dashboard para Cliente

## Task 1: Criar estrutura do projeto .pbip
- [ ] Criar pasta `NomeCliente.SemanticModel/definition/`
- [ ] Criar pasta `NomeCliente.Report/definition/pages/`
- [ ] Criar arquivo `.pbip` com referências
- [ ] Copiar tema Mob2Con-Brand-Theme.json

## Task 2: Modelagem de dados
- [ ] Criar tabela dCalendario via DAX (CALENDAR)
- [ ] Importar tabela fato principal (Power Query M)
- [ ] Criar dimensões necessárias
- [ ] Definir relacionamentos (1:N, star-schema)
- [ ] Marcar dCalendario como tabela de datas

## Task 3: Medidas DAX
- [ ] Criar tabela _Medidas (vazia, só para organizar)
- [ ] [Qtd] Total = COUNTROWS(fTabela)
- [ ] [R$] Faturamento = SUM(fTabela[Valor])
- [ ] [%] Var MoM = DIVIDE([R$] Atual - [R$] Anterior, [R$] Anterior)
- [ ] [Avg] Ticket Médio = DIVIDE([R$] Faturamento, [Qtd] Total)
- [ ] Medidas de ranking (RANKX)

## Task 4: Layout das páginas
- [ ] Página Capa: logo, título, botões de navegação
- [ ] Página Executiva: 4 KPI cards + gráfico de tendência
- [ ] Página Operacional: tabela detalhada + filtros
- [ ] Página Analítica: matrix + slicers avançados
- [ ] Página Mobile: cards empilhados verticalmente

## Task 5: Validação e publicação
- [ ] Aplicar tema e validar cores/fontes
- [ ] Testar navegação entre páginas
- [ ] Verificar performance (< 30s refresh)
- [ ] Documentar no CHANGELOG
