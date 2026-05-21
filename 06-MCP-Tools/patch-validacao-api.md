# Patch: executarTodasAsValidacoes compatível com API

## Problema
A função usa `SpreadsheetApp.getUi().alert()` que só funciona quando o usuário está com a planilha aberta. Via API (scripts.run) isso causa erro.

## Solução
Substituir a última linha da função por um guard que detecta se está rodando via API.

### Código original (última linha da função):
```javascript
  SpreadsheetApp.getUi().alert('Validação concluída. Veja a aba ' + CONFIG.ABAS.VALIDACAO);
```

### Substituir por:
```javascript
  // Guard: getUi() não funciona via API
  try { SpreadsheetApp.getUi().alert('Validação concluída. Veja a aba ' + CONFIG.ABAS.VALIDACAO); } catch(uiErr) {}
  return { falhas, atencao, total: testes.length, resultado: falhas ? 'FALHA' : atencao ? 'ATENCAO' : 'OK' };
```

## Deploy necessário
1. Implantar → Nova implantação → API Executável
2. Acesso: "Qualquer pessoa da organização"
