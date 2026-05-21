# 📊 PLANO DE OTIMIZAÇÃO - NORDESTÃO EXCLUSIVO DN

## 🎨 IDENTIDADE VISUAL MOB2CON
- **Laranja Principal**: #f46901 (destaques, KPIs)
- **Grafite**: #434343 (texto, estrutura)
- **Preto**: #111111 (títulos)
- **Azul MobConnect**: #4285f4 (MobConnect apenas)
- **Fonte**: Raleway (títulos), Raleway Regular (corpo)

---

## 📄 DASHBOARD 1: VENDAS

### Objetivo
Monitorar performance de vendas, tendências e comparativos mensais.

### Layout (Grid 4x4)
```
┌─────────────────────────────────────────────────────────────┐
│ VENDAS - NORDESTÃO EXCLUSIVO DN                             │
├─────────────────────────────────────────────────────────────┤
│ [KPI Venda M-1]    [KPI Venda M-Atual]  [KPI Venda YTD]    │
│ [Status Tendência] [Variação MoM]       [Lojas com Venda]  │
├─────────────────────────────────────────────────────────────┤
│ [Gráfico Vendas 3M]                                         │
│ [Comparativo M-1 vs M-2 vs M-3]                             │
├─────────────────────────────────────────────────────────────┤
│ [Ranking Lojas por Venda]  [Distribuição por Fornecedor]   │
└─────────────────────────────────────────────────────────────┘
```

### Medidas Principais
- NE | Venda (R$) M-1
- NE | Venda (R$) M-Atual
- NE | Venda YTD (R$)
- NE | Variação Vendas MoM
- NE | Status Tendência Vendas
- NE | Lojas com Venda M-1
- NE | Venda Média por Loja (R$)

### Cores
- KPIs: Laranja #f46901
- Gráficos: Gradiente Laranja → Grafite
- Texto: Grafite #434343

---

## 📄 DASHBOARD 2: RUPTURA

### Objetivo
Monitorar rupturas operacionais, comerciais e administrativas com alertas.

### Layout (Grid 4x4)
```
┌─────────────────────────────────────────────────────────────┐
│ RUPTURA - NORDESTÃO EXCLUSIVO DN                            │
├─────────────────────────────────────────────────────────────┤
│ [KPI Ruptura Op]   [KPI Ruptura Com]   [KPI Ruptura Adm]   │
│ [Alerta Ruptura]   [% Ruptura Op]      [Receita Recuper.]  │
├─────────────────────────────────────────────────────────────┤
│ [Evolução Ruptura Op 3M]                                    │
│ [Comparativo Op vs Com vs Adm]                              │
├─────────────────────────────────────────────────────────────┤
│ [Ranking Lojas Ruptura Op]  [Produtos com Ruptura]         │
│ [Forecast Próx. Mês]        [Contagem Ruptura]             │
└─────────────────────────────────────────────────────────────┘
```

### Medidas Principais
- NE | Ruptura Operacional (R$)
- NE | Ruptura Comercial (R$)
- NE | Ruptura Administrativa (R$)
- NE | % Ruptura Operacional
- NE | Semáforo Ruptura Op
- NE | Receita Recuperável Total
- NE | Forecast Ruptura Op Próx. Mês
- NE | Ranking Loja Ruptura Op

### Cores
- Crítico: Vermelho #d32f2f
- Atenção: Amarelo #f57c00
- Normal: Verde #388e3c
- Destaques: Laranja #f46901

---

## 📄 DASHBOARD 3: OPERAÇÃO

### Objetivo
Monitorar eficiência operacional, horas, visitas e atividades MobConnect.

### Layout (Grid 4x4)
```
┌─────────────────────────────────────────────────────────────┐
│ OPERAÇÃO - NORDESTÃO EXCLUSIVO DN                           │
├─────────────────────────────────────────────────────────────┤
│ [KPI Eficiência]   [KPI Execução Visitas] [KPI Atividades] │
│ [Status Horas]     [GAP Visitas]          [Tarefas Concl.]  │
├─────────────────────────────────────────────────────────────┤
│ [Horas Ideais vs Realizadas]                                │
│ [Visitas Planejadas vs Realizadas]                          │
├─────────────────────────────────────────────────────────────┤
│ [Atividades por Status]        [Problemas Reportados]       │
│ [Promotores com Acesso]        [Tendência Eficiência]       │
└─────────────────────────────────────────────────────────────┘
```

### Medidas Principais
- NE | Horas Ideais
- NE | Horas Realizadas
- NE | % Eficiência Horas
- NE | Semáforo Eficiência Horas
- NE | Visitas Planejadas
- NE | Visitas Realizadas
- NE | % Execução Visitas
- NE | Atividades (Qtd)
- NE | Tarefas Concluídas
- NE | % Tarefas Concluídas
- NE | Promotores com Acesso

### Cores
- Excelente: Verde #388e3c
- Bom: Azul #1976d2
- Crítico: Vermelho #d32f2f
- Destaques: Laranja #f46901

---

## 🎯 PADRÕES DE DESIGN

### Tamanhos Padrão
- **KPI Card**: 200x150px
- **Gráfico Pequeno**: 400x250px
- **Gráfico Grande**: 800x400px
- **Tabela**: 800x300px

### Espaçamento
- Gap entre visuais: 16px
- Margem externa: 20px
- Padding interno: 10px

### Tipografia
- **Título Dashboard**: Raleway Black 28px, Preto #111111
- **Título Visual**: Raleway Bold 14px, Grafite #434343
- **Valor KPI**: Raleway Bold 24px, Laranja #f46901
- **Texto Corpo**: Raleway Regular 11px, Grafite #434343

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [ ] Criar página "Dashboard Vendas"
- [ ] Criar página "Dashboard Ruptura"
- [ ] Criar página "Dashboard Operação"
- [ ] Aplicar tema Mob2Con (cores, fontes)
- [ ] Adicionar KPI cards com alertas
- [ ] Organizar gráficos em grid
- [ ] Adicionar filtros globais (Data, Rede, Loja, Fornecedor)
- [ ] Validar relacionamentos
- [ ] Testar interatividade
- [ ] Documentar métricas

---

## 📌 PRÓXIMOS PASSOS

1. Abrir Nordestão no Power BI Desktop
2. Criar as 3 páginas conforme layout
3. Adicionar visuais e medidas
4. Aplicar formatação Mob2Con
5. Testar filtros e drill-through
6. Exportar para web/mobile

