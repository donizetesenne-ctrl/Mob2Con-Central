# Spec: Relatório Semanal Automático

## Objetivo
Gerar automaticamente um relatório HTML de produção semanal com métricas de entregas, dashboards criados/editados e status dos pipelines.

## Requisitos Funcionais

### REQ-1: Coleta de Dados
- Listar arquivos criados/modificados na semana (git log ou filesystem)
- Contar dashboards editados (por .Report/ modificado)
- Contar medidas DAX criadas (por .SemanticModel/ modificado)
- Status dos syncs Redshift→Sheets (logs/)

### REQ-2: Geração do Relatório
- Template HTML com identidade Mob2Con
- Seções: Resumo, Entregas, Métricas, Próximos Passos
- Gráficos simples (barras CSS, sem JS externo)
- Cor primária #F46901, fonte Raleway

### REQ-3: Distribuição
- Salvar em `03-Documentacao/Relatorio_Semanal_YYYY-MM-DD.html`
- Upload para Google Drive (pasta Relatórios)
- Opção de enviar por email via Gmail API

### REQ-4: Agendamento
- Executar toda sexta-feira às 17:00
- Ou sob demanda via comando manual

## Requisitos Não-Funcionais
- Geração < 30 segundos
- HTML standalone (sem dependências externas)
- Compatível com visualização no navegador e no Drive
