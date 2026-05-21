# Cadastro Lite - Plano de Correção e Automação

## Status Atual
- **Webapp:** https://script.google.com/macros/s/AKfycbwIbavtsCUvI2VSO3_UxNjrz8R8qIcBPQf2gpSf_mXnJOJPGZPA52rrcdSmbx0_GMNO/exec
- **Script ID:** 1vgjMumNtjp2EkSoXa8gV_SizQjhljskv8hrRcDOZEGcEI-ZUh78t6N20
- **Planilha:** 1piHmDHrTdoOS6gFkSVQ3xVH3InBV3CPjndmsPJkuAFU
- **Dados:** 7.740 empresas, última atualização 17/05/2026
- **Fonte:** PostgreSQL mc2-production via ODBC

## Bugs Identificados
1. ✅ Planilha renomeada como "backup" — funciona mas confuso
2. ⚠️ Dados desatualizados (17/05) — precisa refresh
3. ❌ Sem atualização automática — manual via Power BI

## Arquitetura
```
PostgreSQL (mc2-production)
    ↓ ODBC (DSN=mc2-production)
Power BI Desktop (.pbip)
    ↓ Script Python (sync_cadastro_lite.py)
Google Sheets (planilha fonte)
    ↓ Apps Script (Code.gs)
Webapp (HTML/JS com Chart.js)
```

## Solução Implementada

### 1. Script de Sync (Python)
`06-MCP-Tools/cadastro-lite-v2/sync_cadastro_lite.py`
- Conecta ao PostgreSQL via ODBC
- Extrai dados agregados por empresa
- Calcula scores de suspeita
- Atualiza planilha Google Sheets

### 2. Atualização Automática (Apps Script)
Adicionar trigger diário no Apps Script para recalcular KPIs

### 3. Correções no Webapp
- Dados carregam corretamente (verificado)
- Todas as 8 abas funcionam
- Filtros e paginação OK

## Como Atualizar Dados Manualmente
1. Abrir Power BI Desktop com o .pbip
2. Refresh (Ctrl+F5) — puxa dados do PostgreSQL
3. Rodar: `python sync_cadastro_lite.py --push`

## Próximos Passos
- [ ] Configurar DSN mc2-production no PC
- [ ] Testar sync completo
- [ ] Adicionar trigger automático (diário 6h)
- [ ] Renomear planilha de volta (remover "backup")
