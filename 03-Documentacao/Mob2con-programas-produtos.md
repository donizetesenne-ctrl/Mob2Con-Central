# 🚀 Mob2Con — Programas e Produtos

> Catálogo dos produtos/soluções Mob2Con e suas características
> Use como referência ao montar relatórios específicos de cada solução

---

## 🏢 Sobre a Mob2Con

- **Fundação:** 2015
- **Sede:** Brasil
- **Segmento:** Tecnologia para varejo (RetailTech)
- **Founders:** Carlos Wayand (CEO), Lucas Bittencourt (Co-Founder / COO / CPO)
- **Missão:** Trazer transparência ao abastecimento de gôndolas via dados
- **Propósito:** Revolucionar a última milha (last mile) da reposição

---

## 🧩 Soluções (Produtos)

### 1️⃣ MobControl
**Descrição curta:** Plataforma de registro e gestão de visitantes, promotores e prestadores de serviços em redes varejistas.

**Principais funcionalidades:**
- Check-in/check-out de promotores
- Registro de visitas por loja
- Gestão de tempo de permanência
- Relatórios de produtividade
- Integração com MobConnect

**Métricas-chave:**
- Total de visitas
- Tempo médio de permanência
- Promotores ativos
- Lojas cobertas
- Produtividade (visitas/promotor/dia)

**Paleta no Power BI:** cores Mob2Con padrão (laranja `#F46901`)

---

### 2️⃣ MobConnect 🔵
**Descrição curta:** Conecta varejo e fornecedores, direcionando operacionalmente equipes de reposição (promotores e repositores).

**Principais funcionalidades:**
- Direcionamento inteligente baseado em Sell Out
- Captura e análise de dados de reposição
- Eliminação de ociosidade
- Redução de rupturas operacionais
- Integração com sistemas de ERP do varejo

**Métricas-chave:**
- Taxa de ruptura
- Cobertura de SKUs
- Sell Out por loja/categoria
- Eficiência operacional
- Alertas gerados / resolvidos

> ⚠️ **IMPORTANTE:** Relatórios de MobConnect devem usar o tema **azul `#4285F4`** em vez do laranja padrão.

---

### 3️⃣ Combate à Ruptura
**Descrição curta:** Aplicativo operacional integrado ao MobControl que direciona atividades de reposição baseadas em dados de Sell Out do varejo.

**Principais funcionalidades:**
- Alertas de ruptura em tempo real
- Priorização de SKUs críticos
- Workflow de reposição
- Integração com dados de Sell Out
- Gestão de tarefas por promotor

**Métricas-chave:**
- % de ruptura (geral / por categoria / por SKU)
- Tempo de resposta à ruptura
- SKUs repostos/dia
- Recuperação de venda perdida

**Paleta:** Mob2Con padrão + vermelho `#C00000` para alertas

---

## 👥 Perfis de Usuário / Personas

### Gerente de Varejo
- Dashboards executivos (macro)
- Foco em: receita, ruptura, cobertura
- Frequência: diária/semanal

### Supervisor Operacional
- Dashboards operacionais (detalhados)
- Foco em: promotores, visitas, tempo
- Frequência: em tempo real

### Indústria (fornecedor)
- Dashboards de Sell Out
- Foco em: performance de SKU, market share
- Frequência: semanal/mensal

### Agência de Promotores
- Dashboards de produtividade
- Foco em: eficiência, presença, SLA
- Frequência: diária

---

## 📊 Relatórios padrão sugeridos

| Relatório | Produto | Páginas típicas |
|-----------|---------|-----------------|
| **Executivo Mob2Con** | Todos | Home, Visão Geral, Análise, Ações |
| **Operacional MobControl** | MobControl | Home, Promotores, Visitas, Lojas, Detalhes |
| **Combate Ruptura** | Ruptura | Home, Alertas, SKUs, Categorias, Ações |
| **Sell Out Industry** | MobConnect | Home, Market Share, Performance, Regional |
| **Acompanhamento Captação** | MobControl | Home, Captação, Pipeline, Conversão |
| **Analítico RG (Rede)** | MobControl | Home, Rede, Lojas, Categorias, Top N |

---

## 🗂️ Projetos Power BI do cliente (atual)

Localização: `C:\Users\Donizete Senne\Desktop\projetos BI\`
Consolidado em: `Mob2Con-Central\02-Powerbi-Projetos\`

| Arquivo | Tipo | Solução associada |
|---------|------|-------------------|
| `Nortestão Exclusivo dn.pbip` | Operacional | MobControl |
| `Analítico RG 2.0.pbip` | Analítico | MobControl |
| `Acompanhamento Captação RG 2.0.pbip` | Pipeline | MobControl |
| `Mockup Dash Implantação.pbip` | Mockup | Todos |

---

## 🔗 Integrações típicas

- **Fontes de dados de varejo:** SAP, TOTVS, Linx, Oracle Retail
- **Data warehouse:** Redshift, BigQuery, Azure SQL
- **BI:** Power BI, Tableau
- **ERP:** varia por cliente
- **CRM:** HubSpot (uso interno Mob2Con)

---

## 📞 Quando usar cada tema

| Contexto | Tema | Arquivo |
|----------|------|---------|
| Relatório geral Mob2Con | Mob2Con Corporate | `Mob2Con-Theme.json` |
| Relatório MobControl | Mob2Con Corporate | `Mob2Con-Theme.json` |
| Relatório MobConnect | MobConnect (azul) | `MobConnect-Theme.json` |
| Relatório Ruptura | Mob2Con Corporate | `Mob2Con-Theme.json` |
| Indústria / Cliente externo | Mob2Con Corporate | `Mob2Con-Theme.json` |

Para aplicar tema: **Power BI Desktop → View → Themes → Browse for themes → selecionar o .json**
