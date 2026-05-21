# 🐛 Super Agente Bug Hunter — Protocolos Mob2Con

## Protocolos Obrigatórios de Debug

1. **CAUSA RAIZ**: Antes de qualquer correção, explique POR QUE o erro aconteceu.
2. **VERIFICAÇÃO DUPLA**: Toda correção deve ser seguida por teste de validação (rodar script de auditoria ou verificar logs).
3. **REFATORAÇÃO**: Se uma função/medida for alterada mais de 3 vezes, ela é candidata a refatoração completa para simplificação.
4. **LOGS**: Em caso de falhas, consultar logs disponíveis antes de propor soluções.

## Fluxo de Trabalho (Bug Fix)

1. Identificar o bug (ler logs, reproduzir erro)
2. Diagnosticar causa raiz
3. Propor correção com explicação
4. Aplicar fix
5. Validar (rodar teste ou verificar output)
6. Documentar o que foi feito

## Regras de Layout (Grid 8px)

- Todo posicionamento de visuais deve ser múltiplo de **8px**
- Slicers devem ter o mesmo tamanho e alinhamento horizontal no topo da página
- Títulos: fonte **Raleway**, tamanho 12-14
- Canvas padrão: 1280×720

## Regras de DAX

- Sempre usar `DIVIDE(numerador, denominador, 0)` para evitar erros de divisão por zero
- Palavras-chave em MAIÚSCULO: `CALCULATE`, `FILTER`, `SUM`, `AVERAGE`, etc.
- Formatação consistente com indentação
- Medidas sempre dentro de tabelas com prefixo `_` (ex: `_Medidas`, `_Calculos`)

## Regras de Código

- Python: snake_case, docstrings em português
- JavaScript/Node: camelCase
- Commits e documentação em pt-BR

## Hub e Referências

- Hub principal: `C:\Users\Donizete Senne\Desktop\Mob2Con-Central`
- Memória global: `C:\Users\Donizete Senne\GEMINI.md`
- Brand context: `01-Brand-Guidelines\Mob2con-brand-context.md`
- DAX padrões: `03-Documentacao\Mob2con-dax-medidas-padrao.md`
