# Requirements Document

## Introduction

Esta especificação amplia o servidor MCP `powerbi-layout` (atualmente em `C:\Users\Donizete Senne\Downloads\Mob2Con-Bridge-v2.0.0\mcp\powerbi-layout-mcp\server.js`) para permitir que um agente de IA monte layouts de Power BI do zero, respeitando as convenções Mob2Con, sem necessidade de abrir o Power BI Desktop até a validação visual final.

Hoje o MCP apenas LÊ projeto, páginas e visuais e MOVE/REDIMENSIONA visuais existentes (tools: `get_brand_context`, `get_layout_base`, `set_project_path`, `list_report_folders`, `list_pages`, `list_visuals`, `update_visual_layout`, `align_visuals`, `validate_project`).

A expansão acrescenta nove frentes de capacidade: criação de elementos PBIR, binding de dados, composição de alto nível com templates Mob2Con, estilo e marca, validação semântica, pré-visualização antes de aplicar, camada conversacional intent → layout, steering persistente das convenções Mob2Con e robustez (dry-run, backup versionado, compatibilidade PBIR/PBIP).

A escrita PBIR é o coração do recurso; portanto, integridade do projeto, idempotência das operações de criação, conformidade visual com o playbook Mob2Con, ausência de sobreposições e reversibilidade via backup são propriedades obrigatórias e testáveis.

## Glossary

- **MCP_Layout**: servidor MCP `powerbi-layout` (arquivo `server.js`) que expõe tools para autoria de layouts Power BI.
- **Agente_IA**: cliente MCP (Kiro, Claude, Amazon Q, etc.) que invoca as tools do MCP_Layout.
- **PBIP_Project**: pasta-raiz de um projeto Power BI no formato Power BI Project (`*.pbip`).
- **PBIR_Report**: pasta `*.Report` dentro do PBIP_Project, no formato Power BI Enhanced Report Format.
- **Pagina_PBIR**: subpasta em `definition/pages/` que representa uma página do relatório, com `page.json` e visuais.
- **Visual_PBIR**: arquivo `visual.json` dentro de uma página, descrevendo um único visual e seu posicionamento.
- **Modelo_Semantico**: pasta `*.SemanticModel` ou arquivo `model.bim` do PBIP_Project, contendo tabelas, colunas e medidas DAX.
- **Tabela_Medidas**: tabela do Modelo_Semantico chamada `_Medidas`, padrão Mob2Con para agrupar medidas DAX.
- **Tema_Mob2Con**: arquivo `Mob2Con-Theme.json` aplicado ao PBIR_Report como tema oficial Mob2Con.
- **Cor_Primaria**: cor laranja Mob2Con `#F46901`, usada como cor semântica `"primary"`.
- **Cor_MobConnect**: cor azul `#4285F4`, usada como cor semântica `"mobconnect"`.
- **Cor_Terceiros**: cor roxa `#6F05D4`, usada como cor semântica `"terceiros"`.
- **Cor_Fundo_Geral**: cor cinza `#F5F5F5`, fundo padrão de páginas Mob2Con.
- **Canvas**: área útil da página em pixels, definida por `width` e `height` em `page.json`.
- **Template_Mob2Con**: layout pré-definido (Executivo, Operacional, Analítico, Capa, Mobile) descrito em `Mob2con-layout-base.md` e exposto por `get_layout_base`.
- **Plano_de_Layout**: estrutura JSON com lista de visuais a criar (tipo, posição, tamanho, bindings) gerada por `plan_page_from_intent` antes de aplicar.
- **Backup_PBIR**: cópia versionada com timestamp de arquivos PBIR antes de qualquer escrita.
- **Modo_Dry_Run**: modo de execução em que a tool calcula o resultado e devolve diff/preview sem gravar arquivos.
- **Steering_Mob2Con**: arquivo `.kiro/steering/mob2con-layout.md` com glossário, paleta e templates Mob2Con para inclusão automática em agentes.
- **Round_Trip_PBIR**: ciclo ler → escrever → ler que deve preservar a estrutura semântica do PBIR_Report.
- **Sobreposicao**: condição em que dois visuais da mesma Pagina_PBIR têm interseção de retângulos `(x, y, width, height)` maior que zero.

## Requirements

### Requirement 1: Criação de páginas PBIR

**User Story:** Como agente de IA, quero criar páginas novas no PBIR_Report, para que eu possa montar relatórios do zero sem editar arquivos manualmente.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `create_page` com nome, dimensões e tema, THE MCP_Layout SHALL gravar uma nova pasta de Pagina_PBIR contendo `page.json` válido em `definition/pages/`.
2. WHEN o Agente_IA invoca `create_page` sem informar dimensões, THE MCP_Layout SHALL aplicar o canvas padrão Mob2Con de 1280x720 pixels.
3. IF já existe uma Pagina_PBIR com o mesmo nome técnico, THEN THE MCP_Layout SHALL retornar erro `PAGE_ALREADY_EXISTS` e não gravar arquivos.
4. WHEN `create_page` é executado com sucesso, THE MCP_Layout SHALL atualizar `definition/pages/pages.json` para incluir a nova página na ordem de exibição.
5. WHERE o parâmetro `dryRun` é verdadeiro, THE MCP_Layout SHALL retornar o conteúdo previsto do `page.json` sem gravar nenhum arquivo.
6. WHEN o Agente_IA invoca `delete_page` com um nome existente, THE MCP_Layout SHALL remover a pasta da Pagina_PBIR e atualizar `pages.json` para refletir a remoção.

### Requirement 2: Criação de visuais PBIR

**User Story:** Como agente de IA, quero criar visuais (cartão, barras, colunas, linhas, pizza, rosca, tabela, matriz, slicer, mapa) em uma página, para que eu possa compor dashboards completos via tools do MCP.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `create_visual` com `pageName`, `visualType`, `x`, `y`, `width`, `height`, THE MCP_Layout SHALL gravar um arquivo `visual.json` válido na Pagina_PBIR informada.
2. THE MCP_Layout SHALL aceitar os tipos de visual: `card`, `bar`, `column`, `line`, `pie`, `donut`, `table`, `matrix`, `slicer`, `map`.
3. IF o `visualType` informado não está na lista suportada, THEN THE MCP_Layout SHALL retornar erro `UNSUPPORTED_VISUAL_TYPE` e não gravar arquivos.
4. IF as coordenadas `x, y, width, height` posicionam o visual fora do Canvas da Pagina_PBIR, THEN THE MCP_Layout SHALL retornar erro `OUT_OF_CANVAS` e não gravar arquivos.
5. WHEN `create_visual` grava um novo Visual_PBIR, THE MCP_Layout SHALL gerar um identificador técnico único de visual no escopo da Pagina_PBIR.
6. WHEN o Agente_IA invoca `delete_visual` com o identificador de um Visual_PBIR existente, THE MCP_Layout SHALL remover o arquivo `visual.json` correspondente.
7. WHERE o parâmetro `dryRun` é verdadeiro em `create_visual` ou `delete_visual`, THE MCP_Layout SHALL retornar o diff previsto sem gravar nenhum arquivo.

### Requirement 3: Criação de elementos auxiliares (texto, forma, imagem, botão)

**User Story:** Como agente de IA, quero criar caixas de texto, formas, imagens e botões de navegação, para que eu possa montar cabeçalhos, rodapés e fluxos de navegação entre páginas.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `create_text_box` com `pageName`, texto, posição e estilo, THE MCP_Layout SHALL gravar um Visual_PBIR do tipo texto na Pagina_PBIR informada.
2. WHEN o Agente_IA invoca `create_shape` com tipo de forma, posição e estilo, THE MCP_Layout SHALL gravar um Visual_PBIR do tipo forma na Pagina_PBIR informada.
3. WHEN o Agente_IA invoca `create_image` com caminho de arquivo de imagem, posição e tamanho, THE MCP_Layout SHALL gravar um Visual_PBIR do tipo imagem referenciando a imagem na Pagina_PBIR informada.
4. WHEN o Agente_IA invoca `create_button` com `buttonType` igual a `navigation` e `targetPage` informado, THE MCP_Layout SHALL gravar um Visual_PBIR do tipo botão configurado para navegar para a Pagina_PBIR alvo.
5. IF `create_button` recebe `targetPage` igual a uma Pagina_PBIR inexistente, THEN THE MCP_Layout SHALL retornar erro `TARGET_PAGE_NOT_FOUND` e não gravar arquivos.
6. IF a gravação do Visual_PBIR em `create_text_box`, `create_shape`, `create_image` ou `create_button` falha por erro de I/O ou parâmetro inválido, THEN THE MCP_Layout SHALL retornar a falha ao Agente_IA com código `WRITE_FAILED` e não deixar arquivos parciais na Pagina_PBIR.

### Requirement 4: Leitura e binding de campos do modelo semântico

**User Story:** Como agente de IA, quero listar tabelas, colunas e medidas do Modelo_Semantico e associá-los aos papéis dos visuais, para que cada visual exiba dados reais do projeto.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `list_model_fields` apontando para um PBIP_Project válido, THE MCP_Layout SHALL retornar a lista de tabelas, colunas e medidas presentes no Modelo_Semantico.
2. THE MCP_Layout SHALL identificar a Tabela_Medidas (`_Medidas`) e marcar suas medidas com a flag `isMeasure` igual a verdadeiro no resultado de `list_model_fields`.
3. WHEN o Agente_IA invoca `bind_field` com `visualId`, `role` (`axis`, `value`, `legend`, `filter` ou `tooltip`) e `field`, THE MCP_Layout SHALL atualizar o Visual_PBIR para associar o campo ao papel informado.
4. IF o campo informado em `bind_field` não existe no Modelo_Semantico, THEN THE MCP_Layout SHALL retornar erro `FIELD_NOT_FOUND` e não modificar o Visual_PBIR.
5. WHEN o Agente_IA invoca `apply_measure` com `visualId` igual a um cartão e `measureName` existente na Tabela_Medidas, THE MCP_Layout SHALL associar a medida ao papel `value` do cartão.
6. WHERE o parâmetro `dryRun` é verdadeiro em `bind_field` ou `apply_measure`, THE MCP_Layout SHALL retornar o diff previsto sem gravar nenhum arquivo.

### Requirement 5: Composição de alto nível com templates Mob2Con

**User Story:** Como agente de IA, quero aplicar templates Mob2Con prontos a uma página, para que eu monte rapidamente layouts Executivo, Operacional, Analítico, Capa ou Mobile sem posicionar visual por visual.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `apply_template` com `pageName` e `templateName` igual a `Executivo`, `Operacional`, `Analitico`, `Capa` ou `Mobile`, THE MCP_Layout SHALL criar todos os visuais previstos pelo Template_Mob2Con correspondente nas coordenadas definidas em `get_layout_base`.
2. WHEN `apply_template` recebe a lista `measures`, THE MCP_Layout SHALL associar cada medida da lista ao próximo cartão de KPI livre do template, na ordem informada.
3. IF `templateName` não corresponde a nenhum Template_Mob2Con conhecido, THEN THE MCP_Layout SHALL retornar erro `TEMPLATE_NOT_FOUND` e não gravar arquivos.
4. WHEN o Agente_IA invoca `create_section` com `sectionType` igual a `header`, `kpis` ou `details`, THE MCP_Layout SHALL aplicar padding e alinhamento padrão Mob2Con à seção criada.
5. WHEN o Agente_IA invoca `create_header_strip` em uma Pagina_PBIR, THE MCP_Layout SHALL criar uma faixa superior contendo logo, título da página e indicador de data de atualização, alinhados conforme `Mob2con-layout-proporcoes.md`.
6. WHEN o Agente_IA invoca `create_footer_strip` em uma Pagina_PBIR, THE MCP_Layout SHALL criar um rodapé contendo lista de filtros ativos e data, alinhados conforme `Mob2con-layout-proporcoes.md`.
7. WHEN o Agente_IA invoca `create_kpi_row` com `count` igual a N e `measures` de tamanho N, THE MCP_Layout SHALL criar N cartões de KPI de mesma altura e largura, distribuídos com espaçamento horizontal de 16 pixels, na Cor_Primaria.

### Requirement 6: Aplicação de tema, fundo e estilo Mob2Con

**User Story:** Como agente de IA, quero aplicar o tema Mob2Con, definir fundos e estilizar visuais por papel semântico, para que o relatório siga o padrão visual da marca sem manipular cores hexadecimais diretamente.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `apply_theme` com caminho para o Tema_Mob2Con, THE MCP_Layout SHALL referenciar o tema no PBIR_Report e copiar o arquivo para a pasta `StaticResources/RegisteredResources` do PBIR_Report.
2. WHEN o Agente_IA invoca `set_page_background` com `pageName` e `color` igual a `Cor_Fundo_Geral`, THE MCP_Layout SHALL aplicar o fundo `#F5F5F5` à Pagina_PBIR.
3. WHEN o Agente_IA invoca `set_page_background` com `pageName` e `imagePath`, THE MCP_Layout SHALL aplicar a imagem informada como plano de fundo da Pagina_PBIR.
4. WHEN o Agente_IA invoca `style_visual` com `visualId` e `semanticColor` igual a `primary`, `mobconnect` ou `terceiros`, THE MCP_Layout SHALL traduzir o nome semântico para o hexadecimal correspondente da paleta Mob2Con e aplicá-lo ao Visual_PBIR.
5. THE MCP_Layout SHALL aceitar em `style_visual` os atributos `border`, `shadow` e `padding` conforme convenções de `Mob2con-efeitos-powerbi.md`.
6. WHEN o Agente_IA invoca `validate_brand_compliance` em uma Pagina_PBIR, THE MCP_Layout SHALL retornar a lista de desvios em relação à paleta Mob2Con, fontes e espaçamentos definidos no playbook.
7. IF um Visual_PBIR usa cor fora da paleta Mob2Con declarada, THEN THE MCP_Layout SHALL incluir o desvio no relatório de `validate_brand_compliance` com severidade `warning`.
8. IF a cópia ou referência do Tema_Mob2Con em `apply_theme` falha por erro de I/O, THEN THE MCP_Layout SHALL retornar a falha ao Agente_IA com código `THEME_APPLY_FAILED` e não deixar arquivos parciais em `StaticResources/RegisteredResources`.

### Requirement 7: Validação semântica de layout

**User Story:** Como agente de IA, quero validar semanticamente o layout antes de entregar ao usuário, para que eu não publique relatórios com sobreposição, visual fora do canvas ou bindings inválidos.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `validate_layout` em uma Pagina_PBIR, THE MCP_Layout SHALL retornar a lista de pares de visuais com Sobreposicao detectada.
2. WHEN o Agente_IA invoca `validate_layout`, THE MCP_Layout SHALL identificar visuais cuja área extrapola o Canvas da Pagina_PBIR e listá-los com código `OUT_OF_CANVAS`.
3. WHEN o Agente_IA invoca `validate_layout`, THE MCP_Layout SHALL identificar pares de visuais adjacentes cujo espaçamento horizontal ou vertical difere em mais de 4 pixels do espaçamento dominante da página e listá-los com código `INCONSISTENT_SPACING`.
4. WHEN o Agente_IA invoca `validate_layout`, THE MCP_Layout SHALL identificar visuais cujas coordenadas `x` ou `y` divergem em mais de 4 pixels do alinhamento dominante de seus vizinhos e listá-los com código `BROKEN_ALIGNMENT`.
5. WHEN o Agente_IA invoca `validate_accessibility` em uma Pagina_PBIR, THE MCP_Layout SHALL retornar a lista de visuais com contraste de texto inferior à razão 4.5:1 e a lista de visuais com tamanho de fonte inferior a 10 pontos.
6. WHEN o Agente_IA invoca `validate_data_bindings` em uma Pagina_PBIR, THE MCP_Layout SHALL listar Visuais_PBIR sem nenhum campo associado e Visuais_PBIR cujo binding aponta para medida ausente do Modelo_Semantico.

### Requirement 8: Pré-visualização e diff antes da escrita

**User Story:** Como agente de IA, quero visualizar e revisar mudanças antes de gravar arquivos PBIR, para que o usuário aprove o layout sem precisar abrir o Power BI Desktop.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `render_preview` para uma Pagina_PBIR, THE MCP_Layout SHALL retornar um documento SVG contendo retângulos posicionados na escala do Canvas, com cores e títulos dos visuais.
2. WHERE o parâmetro `format` em `render_preview` é igual a `html`, THE MCP_Layout SHALL retornar um documento HTML estático equivalente ao SVG.
3. WHEN `render_preview` é executado para uma Pagina_PBIR ainda não persistida, THE MCP_Layout SHALL aceitar um Plano_de_Layout em memória como entrada e renderizar a partir dele.
4. WHEN o Agente_IA invoca `diff_layout` com a Pagina_PBIR atual e um Plano_de_Layout candidato, THE MCP_Layout SHALL retornar a lista de visuais a criar, remover ou modificar com seus campos antes/depois.
5. THE MCP_Layout SHALL emitir o diff de `diff_layout` sem gravar arquivos no PBIR_Report.

### Requirement 9: Camada conversacional intent → layout

**User Story:** Como agente de IA, quero traduzir uma intenção em linguagem natural em um Plano_de_Layout, para que o usuário aprove o plano antes de qualquer escrita.

#### Acceptance Criteria

1. WHEN o Agente_IA invoca `plan_page_from_intent` com `objective`, `availableMeasures` e `templateName`, THE MCP_Layout SHALL retornar um Plano_de_Layout contendo lista de visuais com tipo, posição, tamanho e bindings propostos.
2. THE MCP_Layout SHALL emitir o Plano_de_Layout sem gravar arquivos no PBIR_Report.
3. IF `templateName` informado em `plan_page_from_intent` não existe, THEN THE MCP_Layout SHALL retornar erro `TEMPLATE_NOT_FOUND`.
4. WHEN o Agente_IA invoca `apply_plan` com um Plano_de_Layout aprovado, THE MCP_Layout SHALL executar criação de página, visuais, bindings e estilo conforme o plano.
5. IF qualquer passo de `apply_plan` falha, THEN THE MCP_Layout SHALL reverter as escritas já efetuadas usando o Backup_PBIR criado no início da operação.

### Requirement 10: Steering persistente das convenções Mob2Con

**User Story:** Como Agente_IA, quero acessar o glossário, a paleta e os templates Mob2Con como contexto persistente, para que eu aplique as convenções da marca em todas as decisões de layout.

#### Acceptance Criteria

1. WHEN `get_brand_context` é invocado, THE MCP_Layout SHALL retornar o glossário Mob2Con, a paleta de cores `Cor_Primaria`, `Cor_MobConnect`, `Cor_Terceiros`, `Cor_Fundo_Geral` e a referência à Tabela_Medidas.
2. WHEN `get_layout_base` é invocado, THE MCP_Layout SHALL retornar as coordenadas e dimensões dos cinco Templates_Mob2Con (Executivo, Operacional, Analítico, Capa, Mobile).
3. THE MCP_Layout SHALL gravar e manter sincronizado o arquivo Steering_Mob2Con (`.kiro/steering/mob2con-layout.md`) com `inclusion: auto`, contendo o mesmo glossário e paleta retornados por `get_brand_context`.
4. WHEN `get_brand_context` é alterado em conteúdo, THE MCP_Layout SHALL atualizar o Steering_Mob2Con para refletir o novo conteúdo dentro da mesma operação.

### Requirement 11: Dry-run, backup versionado e compatibilidade PBIR

**User Story:** Como usuário, quero que toda operação de escrita seja reversível e compatível com o Power BI Desktop, para que eu não perca trabalho nem corrompa o projeto piloto.

#### Acceptance Criteria

1. THE MCP_Layout SHALL aceitar o parâmetro booleano `dryRun` em todas as tools que modificam arquivos do PBIR_Report.
2. WHEN uma tool é chamada com `dryRun` igual a verdadeiro, THE MCP_Layout SHALL retornar o diff resultante e não gravar nenhum arquivo.
3. WHEN uma tool é chamada com `dryRun` igual a falso ou ausente, THE MCP_Layout SHALL criar um Backup_PBIR dos arquivos a serem modificados antes da escrita, em `.kiro/backups/powerbi-layout/{timestamp}/`.
4. THE MCP_Layout SHALL nomear o Backup_PBIR usando o formato `YYYYMMDD-HHmmss` em UTC.
5. IF a criação do Backup_PBIR falha por erro de I/O, THEN THE MCP_Layout SHALL prosseguir com a operação de escrita e incluir o aviso `BACKUP_FAILED` na resposta da tool.
5. WHEN o Agente_IA invoca `restore_backup` com um identificador de Backup_PBIR existente, THE MCP_Layout SHALL restaurar todos os arquivos do PBIR_Report ao estado registrado no backup.
6. THE MCP_Layout SHALL gravar arquivos em conformidade com a especificação Power BI Enhanced Report Format (PBIR), preservando codificação UTF-8 sem BOM e finais de linha LF.
7. WHEN `validate_project` é executado após qualquer operação de escrita, THE MCP_Layout SHALL ler todos os JSONs do PBIR_Report sem erros de parsing.

### Requirement 12: Integridade do PBIR após escrita (round-trip)

**User Story:** Como usuário, quero garantia de que os arquivos PBIR escritos pelo MCP são idênticos em estrutura aos lidos depois, para que o Power BI Desktop continue abrindo o projeto sem aviso.

#### Acceptance Criteria

1. FOR ALL Pagina_PBIR criada por `create_page`, ler a página com `list_pages` seguido de `list_visuals` SHALL retornar metadados consistentes com os parâmetros usados na criação (propriedade de round-trip).
2. FOR ALL Visual_PBIR criado por `create_visual`, ler o visual com `list_visuals` SHALL retornar `x`, `y`, `width` e `height` iguais aos informados na criação, com tolerância zero.
3. WHEN um PBIR_Report é gravado pelo MCP_Layout e em seguida lido por `validate_project`, THE MCP_Layout SHALL reportar zero erros de parsing.

### Requirement 13: Idempotência das operações de criação e estilo

**User Story:** Como Agente_IA, quero que repetir uma operação de criação ou estilização produza o mesmo estado final, para que falhas parciais e reexecuções sejam seguras.

#### Acceptance Criteria

1. FOR ALL Plano_de_Layout aplicado por `apply_plan`, aplicar o mesmo plano duas vezes consecutivas em um PBIR_Report SHALL produzir o mesmo conjunto final de Pagina_PBIR e Visual_PBIR após a primeira aplicação (propriedade de idempotência).
2. FOR ALL invocação de `apply_theme` com o mesmo tema, executar duas vezes consecutivas SHALL produzir o mesmo conteúdo final de tema referenciado pelo PBIR_Report.
3. FOR ALL invocação de `style_visual` com os mesmos parâmetros sobre o mesmo Visual_PBIR, executar duas vezes consecutivas SHALL produzir o mesmo `visual.json` resultante.

### Requirement 14: Conformidade visual com Mob2Con

**User Story:** Como gestor de marca, quero que todo layout produzido pelo MCP siga as cores, fontes e espaçamentos Mob2Con, para que dashboards permaneçam visualmente coerentes entre projetos.

#### Acceptance Criteria

1. FOR ALL Visual_PBIR criado pelas tools de composição (`apply_template`, `create_section`, `create_header_strip`, `create_footer_strip`, `create_kpi_row`), as cores aplicadas SHALL pertencer à paleta `{Cor_Primaria, Cor_MobConnect, Cor_Terceiros, Cor_Fundo_Geral}` ou às cores neutras declaradas no Tema_Mob2Con.
2. FOR ALL Pagina_PBIR criada por `create_page` sem `backgroundColor` explícito, o fundo aplicado SHALL ser igual à `Cor_Fundo_Geral`.
3. FOR ALL linha de cartões criada por `create_kpi_row`, a diferença de altura e largura entre cartões SHALL ser zero.
4. WHEN `validate_brand_compliance` é executado sobre um PBIR_Report criado integralmente pelas tools de composição, THE MCP_Layout SHALL retornar zero desvios de severidade `error`.

### Requirement 15: Ausência de sobreposições

**User Story:** Como usuário, quero garantia de que visuais criados pelo MCP nunca se sobreponham, para que o relatório seja legível sem ajuste manual.

#### Acceptance Criteria

1. FOR ALL Pagina_PBIR resultante de `apply_template`, `create_section`, `create_header_strip`, `create_footer_strip`, `create_kpi_row` ou `apply_plan`, executar `validate_layout` na página SHALL retornar lista vazia de Sobreposicao.
2. FOR ALL chamada de `create_visual` cujas coordenadas resultariam em Sobreposicao com um Visual_PBIR existente na mesma Pagina_PBIR, THE MCP_Layout SHALL retornar erro `OVERLAP_DETECTED` e não gravar arquivos.
3. FOR ALL chamada de `update_visual_layout` cujas novas coordenadas resultariam em Sobreposicao com outro Visual_PBIR da mesma página, THE MCP_Layout SHALL retornar erro `OVERLAP_DETECTED` e não gravar arquivos.

### Requirement 16: Reversibilidade via backup

**User Story:** Como usuário, quero poder reverter qualquer escrita feita pelo MCP, para que eu retorne ao estado anterior caso o resultado não atenda à expectativa.

#### Acceptance Criteria

1. FOR ALL operação de escrita executada com `dryRun` igual a falso, executar `restore_backup` com o Backup_PBIR criado por essa operação SHALL produzir um PBIR_Report byte-a-byte igual ao estado anterior à operação (propriedade de round-trip via backup).
2. THE MCP_Layout SHALL preservar Backups_PBIR pelo período mínimo de 30 dias antes de qualquer rotina de limpeza automática.
3. WHEN o Agente_IA invoca `list_backups`, THE MCP_Layout SHALL retornar a lista de Backups_PBIR existentes com seu timestamp e a tool de origem.
4. IF `restore_backup` é invocado com um identificador inexistente, THEN THE MCP_Layout SHALL retornar erro `BACKUP_NOT_FOUND` e não modificar o PBIR_Report.
