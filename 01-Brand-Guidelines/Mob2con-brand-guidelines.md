# 🎨 Mob2Con — Guia de Identidade Visual Consolidado

> Fonte: extraído de "Apresentação Modelo Mob2con (1).pptx" — 39 slides
> Uso: referência para Power BI, Apresentações, Materiais visuais

---

## 🎨 Paleta de Cores Oficial

| Cor | HEX | Uso |
|-----|-----|-----|
| **Laranja Mob2Con** | `#F46901` | Cor primária da marca, destaques, CTAs |
| **Cinza escuro** | `#434343` | Texto principal, títulos |
| **Preto** | `#111111` | Fundos escuros, texto em alto contraste |
| **Azul MobConnect** | `#4285F4` | **EXCLUSIVO** — só usar quando for sobre MobConnect |
| **Roxo** | `#6F05D4` | Acento, elementos secundários |

### ⚠️ Regras importantes

> **1. O azul `#4285F4` é exclusivo e só deve ser usado quando falar de MobConnect.** Em outros contextos Power BI/relatórios, usar laranja + cinza escuro.

> **2. NUNCA usar padrões Microsoft/Fabric no lugar dos Mob2Con.** Mesmo que seja "mais rápido" ou "default do Power BI":
> - ❌ NÃO usar `#0078D4` (Microsoft blue) → usar `#4285F4` (MobConnect) quando for MobConnect
> - ❌ NÃO usar `Segoe UI` → usar `Raleway` (baixar e instalar no sistema antes)
> - ❌ NÃO usar temas padrão do Power BI Desktop → criar tema custom com estas cores
>
> Se a fonte Raleway não estiver instalada, **instalar ela é o primeiro passo**, não substituir por outra.

---

## 🔤 Tipografia

| Elemento | Fonte | Peso |
|----------|-------|------|
| **Título** | Raleway | Preto (Black) |
| **Subtítulo** | Raleway | Negrito (Bold) |
| **Corpo de texto** | Raleway | Regular |

### Download da fonte
- Google Fonts: https://fonts.google.com/specimen/Raleway
- Pesos recomendados no Power BI: Raleway (400), Raleway Bold (700), Raleway Black (900)

---

## 🏢 Sobre a Mob2Con

**Fundação:** 2015
**Founders:** Carlos Wayand (CEO), Lucas Bittencourt (COO/CPO)

**Missão:** Trazer transparência ao processo e fortalecer a conexão entre varejo, indústria e agência de promotores no abastecimento de lojas, via captura e análise de dados, contribuindo para redução de perdas, rupturas e má alocação de mão-de-obra.

**Propósito:** Desenvolver soluções tecnológicas que revolucionem a última milha (last mile) do processo de reposição de gôndolas.

### Soluções da casa
1. **MobControl** — plataforma de registro/gestão de visitantes, promotores e prestadores nas redes varejistas
2. **MobConnect** — conecta varejo e fornecedores, direcionamento operacional de promotores (usar azul `#4285F4`)
3. **Combate à Ruptura** — solução integrada ao MobControl, fluxo baseado em dados de Sell Out

---

## 🎯 Aplicação em Power BI

### Cores por tipo de visual
- **KPIs principais:** `#F46901` (laranja) com texto branco ou `#111111`
- **Títulos de seção:** `#434343` (cinza escuro) ou `#111111` (preto)
- **Gráficos de barras/colunas:** `#F46901` como cor principal, `#434343` como secundária
- **Indicadores de alerta:** vermelho `#C00000` (padrão) — se falar de ruptura
- **Indicadores positivos:** verde `#107C41` (padrão)
- **Tema "MobConnect":** trocar laranja por `#4285F4` em todo o relatório

### Hierarquia tipográfica sugerida
- **Título da página:** Raleway Black, 20pt, `#111111`
- **Título de visual:** Raleway Bold, 14pt, `#434343`
- **Rótulos/eixos:** Raleway Regular, 10pt, `#434343`
- **Valores de KPI:** Raleway Black, 28pt, cor da marca

### Checklist de validação visual de dashboard
- [ ] Usa Raleway (não Segoe UI, Arial, etc.)
- [ ] Laranja `#F46901` como destaque principal (ou `#4285F4` se MobConnect)
- [ ] Textos longos truncados (títulos curtos, sem "...")
- [ ] Contraste adequado (texto escuro em fundo claro)
- [ ] Bordas/separadores em `#434343` suave (não preto puro)
- [ ] Espaçamento consistente entre visuais (grid 16px ou 24px)

---

## 📐 Grid e Layout (templates da apresentação)

- **Capa:** logo centralizado, slogan em Raleway Black
- **Conteúdo:** grid de 12 colunas, imagens à direita ou esquerda, texto respeitando respiro
- **Modelos vazios disponíveis:** texto + imagem lado a lado (slides 27-33 do pptx)

---

## 🔗 Referências

- Apresentação original: `C:\Users\Donizete Senne\Downloads\Apresentação Modelo Mob2con (1).pptx`
- Contexto de marca (MCP): `Mob2Con-Bridge-v2.0.0\mcp\powerbi-layout-mcp\Mob2con-brand-context.md`
- Layout base (MCP): `Mob2Con-Bridge-v2.0.0\mcp\powerbi-layout-mcp\Mob2con-layout-base.md`
