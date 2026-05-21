# Design: Migração de Tema para Padrão Mob2Con

## Estratégia

```
[Auditoria] → [Backup] → [Substituição em lote] → [Validação] → [Documentação]
```

## Mapeamento de Substituições

| De | Para | Contexto |
|----|------|----------|
| #0078D4 | #F46901 | Cor primária (Microsoft → Mob2Con) |
| #0078d4 | #F46901 | Mesmo, lowercase |
| Segoe UI | Raleway | Fonte padrão |
| Arial | Raleway | Fonte fallback |
| fontWeight: "Normal" | fontWeight: 400 | Peso numérico |
| fontWeight: "Bold" | fontWeight: 700 | Peso numérico |

## MCPs Utilizados
- **powerbi-layout**: validate_project para checar integridade
- **filesystem**: Buscar/substituir em arquivos JSON
- **shell-command**: Executar scripts de migração em lote

## Script de Migração (pseudocódigo)
```python
for project in list_pbip_projects():
    backup(project)
    for json_file in find_json_files(project):
        content = read(json_file)
        content = replace_colors(content)
        content = replace_fonts(content)
        write(json_file, content)
    validate_project(project)
    log_changes(project)
```

## Riscos
- Cores hardcoded em expressões DAX (HTML measures) — tratar separadamente
- Fontes em tooltips customizados — verificar manualmente
- Projetos com tema inline (sem arquivo .json) — converter para arquivo
