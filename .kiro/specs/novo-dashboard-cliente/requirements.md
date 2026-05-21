# Spec: Novo Dashboard para Cliente

## Objetivo
Criar um dashboard Power BI completo seguindo o padrão Mob2Con para um novo cliente.

## Requisitos Funcionais

### REQ-1: Estrutura de Páginas
- Página de Capa (1600x900) com logo do cliente e navegação
- Página Executiva (1600x900) com KPIs principais
- Página Operacional (1280x720) com detalhamento
- Página Analítica (1920x1080) com tabelas e filtros avançados
- Página Mobile (320x568) com visão resumida

### REQ-2: Modelo de Dados
- Importar base consolidada do Excel ou Redshift
- Criar tabela de calendário (dCalendario)
- Criar tabela de medidas (_Medidas)
- Relacionamentos star-schema

### REQ-3: Medidas DAX Padrão
- [Qtd] Total de registros
- [R$] Faturamento total
- [%] Variação período anterior
- [Avg] Média por período
- Medidas de ranking e Top N

### REQ-4: Identidade Visual Mob2Con
- Tema: Mob2Con-Brand-Theme.json aplicado
- Cor primária: #F46901 (laranja)
- Fonte: Raleway (400/700/900)
- Layout Z-pattern com grid 8px
- Nunca usar azul Microsoft #0078D4

### REQ-5: Navegação
- Botões de navegação entre páginas
- Tooltips customizados
- Bookmarks para estados de filtro

## Requisitos Não-Funcionais
- Performance: refresh < 30 segundos
- Formato: .pbip (Power BI Project)
- Compatível com Power BI Service para publicação
