### Exemplo de Fix

Se você encontrar um problema específico que precisa ser corrigido no código, você pode seguir os seguintes passos:

1. **Encontre o Problema**: Verifique qual parte do código está causando o problema. Por exemplo, se você descobrir que a versão no cabeçalho está incorreta, precisará procurar onde isso é definido.

2. **Corrija o Código**: Após encontrar o problema, faça ocorrência da correção necessária. Para o exemplo acima, você pode alterar a linha com a versão do código para "v9.0".

3. **Verifique as Mudanças**: Certifique-se que as mudanças foram aplicadas corretamente e que o comportamento do código ainda é esperado.

4. **Teste o Código**: Execute a lógica originalmente no script para garantir que nada esteja estourando.

### Exemplo de Check

Você pode usar um exemplo de check para confirmar se as correções foram aplicadas corretamente:

```json
{
  "label": "v9.0 no cabeçalho",
  "token": "SPRINT IC — SISTEMA COMPLETO v9.0"
}
```

### Exemplo de Função MCP

Para aplicar uma correção específica, você pode usar o 'smart_edit_google' para atualizar a planilha Google Sheets ou o 'review_file' para analisar medidas Power BI.

#### smart_edit_google

```mcp
function main() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName("Sheet1");
  
  // Correção de versão no cabeçalho
  const headerCell = sheet.getRange(1, 1);
  headerCell.setValue("SPRINT IC — SISTEMA COMPLETO v9.0");
  
  Logger.log("Versão atualizada!");
}
```

#### review_file

```mcp
function main() {
  const file = DriveApp.getFileById("fileId");
  const content = file.getBlob().getDataAsString();
  
  // Correção de medidas Power BI
  const startIndex = content.indexOf("// NOVIDADES v9.0");
  if (startIndex != -1) {
    content = content.substring(0, startIndex + "NOVIDADES v9.0".length + 1);
    content += "\n// NOVA VERSÃO\n";
    file.setContent(content);
    
    Logger.log("Correção de medidas Power BI aplicada!");
  } else {
    Logger.log("Nenhuma correção necessária para medidas Power BI");
  }
}
```

### Verificação

Para verificar se as mudanças foram aplicadas corretamente, você pode usar o 'review_file' para analisar a medida específica que foi alterada.

```mcp
function main() {
  const file = DriveApp.getFileById("fileId");
  const content = file.getBlob().getDataAsString();
  
  // Correção de medidas Power BI
  const startIndex = content.indexOf("// NOVIDADES v9.0");
  if (startIndex != -1) {
    content = content.substring(0, startIndex + "NOVIDADES v9.0".length + 1);
    content += "\n// NOVA VERSÃO\n";
    file.setContent(content);
    
    Logger.log("Correção de medidas Power BI aplicada!");
  } else {
    Logger.log("Nenhuma correção necessária para medidas Power BI");
  }
}
```

### Suporte

Se você precisar mais ajuda, você pode abrir um novo issue no repositório do projeto ou entrar em contato com os desenvolvedores da Mob2Con Inteligência Comercial.