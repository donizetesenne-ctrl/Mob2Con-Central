# Tasks: Migração de Tema para Padrão Mob2Con

## Task 1: Auditoria
- [ ] Listar todos os projetos em `02-Powerbi-Projetos/`
- [ ] Para cada .Report/, ler report.json e identificar tema
- [ ] Buscar ocorrências de #0078D4, Segoe UI, Arial nos JSONs
- [ ] Gerar relatório de auditoria (arquivo + linha + valor atual)

## Task 2: Backup
- [ ] Criar pasta `backups/pre-migration-YYYY-MM-DD/`
- [ ] Copiar todos os .Report/ e .SemanticModel/ para backup
- [ ] Verificar integridade dos backups

## Task 3: Substituição de cores
- [ ] Buscar e substituir #0078D4 → #F46901 em todos os visual.json
- [ ] Buscar e substituir #0078d4 (lowercase) → #F46901
- [ ] Verificar se #4285F4 está apenas em projetos MobConnect
- [ ] Validar que nenhuma cor ficou fora do padrão

## Task 4: Substituição de fontes
- [ ] Buscar e substituir "Segoe UI" → "Raleway" em todos os JSONs
- [ ] Buscar e substituir "Arial" → "Raleway"
- [ ] Ajustar fontWeight: "Normal"→400, "Bold"→700
- [ ] Validar renderização

## Task 5: Aplicar tema oficial
- [ ] Copiar Mob2Con-Brand-Theme.json para cada projeto
- [ ] Atualizar referência em report.json de cada .Report/
- [ ] Validar via MCP powerbi-layout (validate_project)

## Task 6: Documentação
- [ ] Gerar CHANGELOG-brand-migration.md
- [ ] Listar: arquivo, mudança, antes, depois
- [ ] Commit com mensagem descritiva
