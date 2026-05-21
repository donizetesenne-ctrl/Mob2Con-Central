def write_page_modelo(f):
    f.write('''<div id="pg-modelo" class="page">
<h2 class="section-title">Modelo de Dados</h2>
<div class="grid g3">
<div class="card"><div class="card-title">Tabelas Fato</div><div class="card-value">12</div></div>
<div class="card"><div class="card-title">Dimens\u00f5es</div><div class="card-value">16</div></div>
<div class="card"><div class="card-title">Auxiliares + CS</div><div class="card-value">18</div></div>
</div>
<h3 class="section-title">Tabelas Fato</h3>
<div class="tbl-wrap"><table><thead><tr><th>Tabela</th><th>Tipo</th><th>Relacionamentos</th></tr></thead><tbody>
<tr><td>fato_status_contratantes</td><td><span class="tag tag-info">Fato Principal</span></td><td>dim_agencia, dim_fornecedor, dim_rede, dim_contratante, Data</td></tr>
<tr><td>fato_acesso</td><td><span class="tag tag-info">Fato</span></td><td>dim_visitante, dim_loja, Data</td></tr>
<tr><td>fato_status_promotores_alocacao_vinculo</td><td><span class="tag tag-info">Fato</span></td><td>dim_contratante, dim_visitante</td></tr>
<tr><td>fato_agg_status_documento_redes</td><td><span class="tag tag-info">Fato Agg</span></td><td>dim_rede, dim_documento</td></tr>
<tr><td>fato_declaracao</td><td><span class="tag tag-info">Fato</span></td><td>dim_contratante</td></tr>
<tr><td>fato_horas_ideais</td><td><span class="tag tag-info">Fato</span></td><td>dim_loja</td></tr>
<tr><td>fato_mobconnect_atividades</td><td><span class="tag tag-info">Fato</span></td><td>dim_contratante</td></tr>
<tr><td>fato_status_documento_redes</td><td><span class="tag tag-info">Fato</span></td><td>dim_rede, dim_documento</td></tr>
<tr><td>fato_agg_status_documentacao_colaboradores_redes</td><td><span class="tag tag-info">Fato Agg</span></td><td>dim_rede</td></tr>
<tr><td>fato_status_documento_colaboradores_redes</td><td><span class="tag tag-info">Fato</span></td><td>dim_rede</td></tr>
<tr><td>fato_acesso_prestador_servico</td><td><span class="tag tag-info">Fato</span></td><td>dim_prestador_servico</td></tr>
<tr><td>fato_status_lojas</td><td><span class="tag tag-info">Fato</span></td><td>dim_loja</td></tr>
</tbody></table></div>
<h3 class="section-title">Dimens\u00f5es</h3>
<div class="tbl-wrap"><table><thead><tr><th>Tabela</th><th>Tipo</th><th>Chave</th></tr></thead><tbody>
<tr><td>dim_agencia</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_agencia</td></tr>
<tr><td>dim_fornecedor</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_fornecedor</td></tr>
<tr><td>dim_rede</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_rede</td></tr>
<tr><td>dim_contratante</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_contratante</td></tr>
<tr><td>dim_visitante</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_visitante</td></tr>
<tr><td>dim_loja</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_loja</td></tr>
<tr><td>dim_documento</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_documento</td></tr>
<tr><td>dim_status_aprovacao</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_status</td></tr>
<tr><td>dim_fornecedor_vinculo</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_vinculo</td></tr>
<tr><td>dim_time</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_time</td></tr>
<tr><td>dim_prestador_servico</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_prestador</td></tr>
<tr><td>dim_funcao_prestador_servico</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_funcao</td></tr>
<tr><td>dim_mobconnect_status_atividade</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_status_ativ</td></tr>
<tr><td>dim_app</td><td><span class="tag tag-wn">Dimens\u00e3o</span></td><td>sk_app</td></tr>
<tr><td>Data</td><td><span class="tag tag-wn">Calend\u00e1rio</span></td><td>Date</td></tr>
<tr><td>Estado</td><td><span class="tag tag-wn">Geogr\u00e1fica</span></td><td>ds_estado</td></tr>
</tbody></table></div>
<h3 class="section-title">Tabelas Auxiliares &amp; CS</h3>
<div class="tbl-wrap"><table><thead><tr><th>Tabela</th><th>Tipo</th><th>Prop\u00f3sito</th></tr></thead><tbody>
<tr><td>_CS_Cluster</td><td><span class="tag" style="background:#FED7AA;color:#C45500">CS</span></td><td>Defini\u00e7\u00e3o dos clusters CS</td></tr>
<tr><td>_CS_Owner</td><td><span class="tag" style="background:#FED7AA;color:#C45500">CS</span></td><td>Respons\u00e1veis por cluster</td></tr>
<tr><td>_CS_Medidas</td><td><span class="tag" style="background:#FED7AA;color:#C45500">CS</span></td><td>Cat\u00e1logo de medidas CS</td></tr>
<tr><td>Subject</td><td><span class="tag">Aux</span></td><td>Assuntos/categorias</td></tr>
<tr><td>Indicadores</td><td><span class="tag">Aux</span></td><td>KPIs e indicadores</td></tr>
<tr><td>Planos</td><td><span class="tag">Aux</span></td><td>Planos comerciais</td></tr>
<tr><td>Par\u00e2metro</td><td><span class="tag">Aux</span></td><td>Par\u00e2metros din\u00e2micos</td></tr>
<tr><td>Measure Range</td><td><span class="tag">Aux</span></td><td>Faixas de medidas</td></tr>
<tr><td>Service Selection</td><td><span class="tag">Aux</span></td><td>Sele\u00e7\u00e3o de servi\u00e7os</td></tr>
<tr><td>Score Benchmark</td><td><span class="tag">Aux</span></td><td>Benchmarks de score</td></tr>
<tr><td>Tipo de Contratante</td><td><span class="tag">Aux</span></td><td>Ag\u00eancia/Fornecedor/Rede</td></tr>
<tr><td>Tipo de Promotor</td><td><span class="tag">Aux</span></td><td>Classifica\u00e7\u00e3o promotores</td></tr>
<tr><td>lkp_cadastro_agencia_fornecedor</td><td><span class="tag">Lookup</span></td><td>Cadastro consolidado</td></tr>
<tr><td>TabelaVinculados</td><td><span class="tag">Aux</span></td><td>V\u00ednculos ativos</td></tr>
<tr><td>Indicadores_relat\u00f3rio</td><td><span class="tag">Aux</span></td><td>Indicadores para relat\u00f3rio</td></tr>
<tr><td>Holidays / HolidaysDefinition</td><td><span class="tag">Aux</span></td><td>Feriados</td></tr>
<tr><td>DateAutoTemplate</td><td><span class="tag">Aux</span></td><td>Template de datas autom\u00e1tico</td></tr>
</tbody></table></div>
<h3 class="section-title">Relacionamentos Principais</h3>
<div class="tbl-wrap"><table><thead><tr><th>De (Fato)</th><th>Para (Dimens\u00e3o)</th><th>Chave</th><th>Cardinalidade</th></tr></thead><tbody>
<tr><td>fato_status_contratantes</td><td>dim_agencia</td><td>sk_agencia</td><td>N:1</td></tr>
<tr><td>fato_status_contratantes</td><td>dim_fornecedor</td><td>sk_fornecedor</td><td>N:1</td></tr>
<tr><td>fato_status_contratantes</td><td>dim_rede</td><td>sk_rede</td><td>N:1</td></tr>
<tr><td>fato_status_contratantes</td><td>dim_contratante</td><td>sk_contratante</td><td>N:1</td></tr>
<tr><td>fato_status_contratantes</td><td>Data</td><td>dt_referencia</td><td>N:1</td></tr>
<tr><td>fato_acesso</td><td>dim_visitante</td><td>sk_visitante</td><td>N:1</td></tr>
<tr><td>fato_acesso</td><td>dim_loja</td><td>sk_loja</td><td>N:1</td></tr>
<tr><td>fato_acesso</td><td>Data</td><td>dt_entrada</td><td>N:1</td></tr>
<tr><td>dim_loja</td><td>dim_rede</td><td>sk_rede</td><td>N:1</td></tr>
<tr><td>dim_loja</td><td>Estado</td><td>ds_estado</td><td>N:1</td></tr>
</tbody></table></div>
</div>
''')
