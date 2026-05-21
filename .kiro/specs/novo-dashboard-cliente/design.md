# Design: Novo Dashboard para Cliente

## Arquitetura

```
Cliente.pbip
├── Cliente.SemanticModel/
│   ├── definition/
│   │   ├── tables/          → dCalendario, fVendas, dProduto, _Medidas
│   │   ├── relationships/   → star-schema
│   │   └── expressions/     → Power Query (M)
│   └── model.bim
├── Cliente.Report/
│   ├── definition/
│   │   ├── pages/           → Capa, Executivo, Operacional, Analitico, Mobile
│   │   └── report.json
│   └── StaticResources/
│       └── SharedResources/
│           └── BaseThemes/  → Mob2Con-Brand-Theme.json
└── Cliente.pbip
```

## MCPs Utilizados
- **powerbi-layout**: Posicionamento de visuais (x/y/width/height)
- **powerbi-bridge**: Criação de medidas, tabelas, relacionamentos
- **filesystem**: Criação de arquivos do projeto

## Fluxo de Execução
1. Criar estrutura de pastas .pbip
2. Definir modelo semântico (tabelas + relacionamentos)
3. Criar medidas DAX na tabela _Medidas
4. Configurar páginas com layout Mob2Con
5. Aplicar tema e validar brand compliance
6. Testar navegação e publicar

## Padrão de Layout (por página)

| Elemento | X | Y | Width | Height |
|----------|---|---|-------|--------|
| Header | 0 | 0 | 1280 | 80 |
| KPI Cards | 16 | 96 | 296 | 120 |
| Gráfico Principal | 16 | 232 | 624 | 400 |
| Gráfico Secundário | 656 | 232 | 608 | 400 |
| Footer/Nav | 0 | 648 | 1280 | 72 |
