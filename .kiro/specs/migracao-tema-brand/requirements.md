# Spec: Migração de Tema para Padrão Mob2Con

## Objetivo
Migrar todos os dashboards existentes para o novo tema Mob2Con-Brand-Theme.json, eliminando cores e fontes fora do padrão.

## Requisitos Funcionais

### REQ-1: Auditoria de Dashboards
- Listar todos os .pbip/.pbix no workspace
- Identificar tema atual aplicado em cada um
- Mapear cores fora do padrão (#0078D4, #333333, etc.)
- Mapear fontes fora do padrão (Segoe UI, Arial, etc.)

### REQ-2: Substituição de Cores
- Substituir #0078D4 (Microsoft blue) → #F46901 (laranja Mob2Con)
- Substituir #333333 → #2D2D2D (cinza escuro padrão)
- Manter #4285F4 apenas em dashboards MobConnect
- Gerar relatório de mudanças por arquivo

### REQ-3: Substituição de Fontes
- Substituir Segoe UI → Raleway
- Substituir Arial → Raleway
- Manter pesos: Regular→400, Bold→700, Black→900
- Ajustar tamanhos se necessário (Raleway é ligeiramente maior)

### REQ-4: Aplicação do Tema
- Copiar Mob2Con-Brand-Theme.json para cada projeto
- Atualizar referência no report.json
- Validar que o tema foi aplicado corretamente

### REQ-5: Documentação
- Gerar CHANGELOG-brand-migration.md com todas as mudanças
- Antes/depois de cada dashboard
- Data da migração

## Requisitos Não-Funcionais
- Backup de cada arquivo antes de alterar
- Processo reversível (manter .bak)
- Executar em lote (todos os projetos de uma vez)
