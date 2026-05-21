# Design: Relatório Semanal Automático

## Arquitetura

```
[Git log / Filesystem] → [Python collector] → [Template HTML] → [Arquivo local + Drive]
```

## Componentes

### gerar_relatorio_semanal.py
- Coleta métricas da semana (arquivos modificados, logs de sync)
- Preenche template HTML com dados
- Salva localmente e faz upload via universal-control

### Template HTML
- Header com logo Mob2Con e data
- Cards de métricas (dashboards, medidas, syncs)
- Tabela de entregas detalhada
- Footer com próximos passos

### Estilo
```css
:root {
  --primary: #F46901;
  --bg: #FFFFFF;
  --text: #2D2D2D;
  --font: 'Raleway', sans-serif;
}
```

## MCPs Utilizados
- **universal-control**: Upload para Drive, envio por Gmail
- **filesystem**: Ler logs, listar arquivos modificados
- **shell-command**: Executar git log para histórico

## Dados Coletados
| Métrica | Fonte | Método |
|---------|-------|--------|
| Dashboards editados | 02-Powerbi-Projetos/ | Arquivos modificados na semana |
| Medidas criadas | .SemanticModel/ | Novos .json em measures/ |
| Syncs executados | logs/ | Contar arquivos sync_*.log |
| Erros | logs/ | Grep por "ERROR" nos logs |
| Horas trabalhadas | Git commits | Timestamps dos commits |
