# Tasks: Relatório Semanal Automático

## Task 1: Coletor de métricas
- [ ] Criar `gerar_relatorio_semanal.py`
- [ ] Implementar coleta de arquivos modificados (os.walk + stat)
- [ ] Implementar leitura de logs de sync
- [ ] Implementar contagem de medidas DAX criadas
- [ ] Calcular totais e percentuais

## Task 2: Template HTML
- [ ] Criar template base com identidade Mob2Con
- [ ] Seção header (logo, título, período)
- [ ] Seção cards de métricas (4 KPIs)
- [ ] Seção tabela de entregas
- [ ] Seção próximos passos
- [ ] CSS inline (standalone)

## Task 3: Geração do relatório
- [ ] Preencher template com dados coletados
- [ ] Salvar em `03-Documentacao/Relatorio_Semanal_YYYY-MM-DD.html`
- [ ] Validar que abre corretamente no navegador

## Task 4: Integração Google Drive
- [ ] Upload do HTML para pasta no Drive
- [ ] Criar link compartilhável
- [ ] Opção de envio por email (Gmail API)

## Task 5: Agendamento
- [ ] Criar `relatorio_semanal.bat` para Task Scheduler
- [ ] Configurar execução sexta 17:00
- [ ] Testar execução manual
- [ ] Documentar processo
