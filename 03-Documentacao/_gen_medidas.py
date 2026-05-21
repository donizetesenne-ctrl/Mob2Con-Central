def write_page_medidas(f):
    measures = [
        ("01 - Sinais", [
            ("CS_Dias_Sem_Login", "DATEDIFF(MAX(fato_status_contratantes[dt_acesso_anterior]), TODAY(), DAY)", "Inteiro"),
            ("CS_Fat_Zerado_Dias", "DATEDIFF(CALCULATE(MAX(fato_status_contratantes[dt_referencia]), fato_status_contratantes[vl_unitario_plano_mobcontrol] > 0), TODAY(), DAY)", "Inteiro"),
            ("CS_Inadimplencia_Total", "CALCULATE(COUNTROWS(fato_status_contratantes), fato_status_contratantes[fl_inadimplente] = TRUE())", "Inteiro"),
            ("CS_Contas_Ativas_7d", "CALCULATE(COUNTROWS(fato_status_contratantes), fato_status_contratantes[fl_acesso] = TRUE(), DATESINPERIOD(Data[Date], TODAY(), -7, DAY))", "Inteiro"),
            ("CS_Promotores_Ativos", "CALCULATE(DISTINCTCOUNT(fato_status_promotores_alocacao_vinculo[sk_visitante]), fato_status_promotores_alocacao_vinculo[fl_ativo] = TRUE())", "Inteiro"),
        ]),
        ("01 - Uso Plataforma", [
            ("CS_Contas_Ativas_15d", "CALCULATE(COUNTROWS(fato_status_contratantes), fato_status_contratantes[fl_acesso] = TRUE(), DATESINPERIOD(Data[Date], TODAY(), -15, DAY))", "Inteiro"),
            ("CS_Contas_Ativas_30d", "CALCULATE(COUNTROWS(fato_status_contratantes), fato_status_contratantes[fl_acesso] = TRUE(), DATESINPERIOD(Data[Date], TODAY(), -30, DAY))", "Inteiro"),
            ("CS_Pct_Contas_Ativas_7d", "DIVIDE([CS_Contas_Ativas_7d], COUNTROWS(fato_status_contratantes), 0)", "Percentual"),
            ("CS_Contas_Inativas_7d", "COUNTROWS(fato_status_contratantes) - [CS_Contas_Ativas_7d]", "Inteiro"),
            ("CS_Media_Acessos_Por_Promotor", "DIVIDE(COUNTROWS(fato_acesso), DISTINCTCOUNT(fato_acesso[sk_visitante]), 0)", "Decimal"),
            ("CS_WoW_Delta_Ativas", "[CS_Contas_Ativas_7d] - CALCULATE([CS_Contas_Ativas_7d], DATEADD(Data[Date], -7, DAY))", "Inteiro"),
        ]),
        ("02 - Alertas", [
            ("CS_Lojas_Sem_Acesso_30d", "CALCULATE(DISTINCTCOUNT(fato_acesso[sk_loja]), DATESINPERIOD(Data[Date], TODAY(), -30, DAY), ISBLANK(fato_acesso[dt_entrada]))", "Inteiro"),
            ("CS_Eventos_Distinct", "DISTINCTCOUNT(fato_status_contratantes[tp_evento_plano])", "Inteiro"),
        ]),
        ("02 - Faturamento Zerado", [
            ("CS_Fat_Zerado_Total", "CALCULATE(COUNTROWS(fato_status_contratantes), fato_status_contratantes[vl_unitario_plano_mobcontrol] = 0)", "Inteiro"),
            ("CS_Fat_Zerado_Classificacao", "SWITCH(TRUE(), [CS_Fat_Zerado_Dias] >= 60, \"CHURN_IMINENTE\", [CS_Fat_Zerado_Dias] >= 31, \"CRITICO\", [CS_Fat_Zerado_Dias] >= 16, \"ACAO_NECESSARIA\", [CS_Fat_Zerado_Dias] >= 8, \"ALERTA_LEVE\", \"OK\")", "Texto"),
        ]),
        ("03 - Health Score", [
            ("CS_Health_Score", "VAR pct_acesso = DIVIDE(COUNTROWS(FILTER(fato_status_contratantes, fato_status_contratantes[fl_acesso] = TRUE())), COUNTROWS(fato_status_contratantes), 0) * 100\\nVAR is_ativo = IF(SELECTEDVALUE(dim_contratante[ds_status_atual]) = \"1\", 100, 0)\\nVAR is_pagante = IF(SELECTEDVALUE(fato_status_contratantes[fl_cliente_pagante_mobcontrol]) = TRUE(), 100, 50)\\nRETURN (pct_acesso * 0.40) + (is_ativo * 0.35) + (is_pagante * 0.25)", "Decimal"),
            ("CS_Health_Score_Status", "SWITCH(TRUE(), [CS_Health_Score] >= 75, \"SAUDAVEL\", [CS_Health_Score] >= 50, \"ATENCAO\", [CS_Health_Score] >= 25, \"CRITICO\", \"CHURN RISK\")", "Texto"),
            ("CS_Risk_Band", "SWITCH(TRUE(), [CS_Health_Score] >= 75, 1, [CS_Health_Score] >= 50, 2, [CS_Health_Score] >= 25, 3, 4)", "Inteiro"),
            ("CS_Contas_Risco_Total", "CALCULATE(COUNTROWS(fato_status_contratantes), FILTER(ALL(fato_status_contratantes), [CS_Health_Score] < 50))", "Inteiro"),
            ("CS_Alert_Color_HealthScore", "SWITCH(TRUE(), [CS_Health_Score] >= 75, \"#10B981\", [CS_Health_Score] >= 50, \"#F59E0B\", [CS_Health_Score] >= 25, \"#EF4444\", \"#7F1D1D\")", "Texto"),
        ]),
        ("04 - Turnover", [
            ("CS_Turnover_Admissoes", "CALCULATE(COUNTROWS(fato_status_promotores_alocacao_vinculo), fato_status_promotores_alocacao_vinculo[tp_evento] = \"Admissao\")", "Inteiro"),
            ("CS_Turnover_Desligamentos", "CALCULATE(COUNTROWS(fato_status_promotores_alocacao_vinculo), fato_status_promotores_alocacao_vinculo[tp_evento] = \"Desligamento\")", "Inteiro"),
            ("CS_Turnover_Saldo", "[CS_Turnover_Admissoes] - [CS_Turnover_Desligamentos]", "Inteiro"),
            ("CS_Turnover_Taxa_Pct", "DIVIDE([CS_Turnover_Desligamentos], [CS_Promotores_Ativos], 0)", "Percentual"),
        ]),
        ("05 - Financeiro", [
            ("CS_Inadimplencia_MRR_Risco", "CALCULATE(SUM(fato_status_contratantes[vl_unitario_plano_mobcontrol]), fato_status_contratantes[fl_inadimplente] = TRUE())", "Moeda"),
            ("CS_Inadimplencia_Taxa_Pct", "DIVIDE([CS_Inadimplencia_Total], COUNTROWS(fato_status_contratantes), 0)", "Percentual"),
        ]),
        ("06 - Limpeza Base", [
            ("CS_Limpeza_Inativos_Com_Acesso", "CALCULATE(COUNTROWS(fato_status_contratantes), dim_contratante[ds_status_atual] <> \"1\", fato_status_contratantes[fl_acesso] = TRUE())", "Inteiro"),
            ("CS_Limpeza_Inadimpl_Com_Acesso", "CALCULATE(COUNTROWS(fato_status_contratantes), fato_status_contratantes[fl_inadimplente] = TRUE(), fato_status_contratantes[fl_acesso] = TRUE())", "Inteiro"),
            ("CS_Limpeza_Promotores_Nao_Vinculados", "CALCULATE(DISTINCTCOUNT(fato_status_promotores_alocacao_vinculo[sk_visitante]), ISBLANK(fato_status_promotores_alocacao_vinculo[sk_contratante]))", "Inteiro"),
        ]),
        ("07 - Pendencias", [
            ("CS_Pendencia_Total", "CALCULATE(COUNTROWS(fato_agg_status_documento_redes), fato_agg_status_documento_redes[fl_pendente] = TRUE())", "Inteiro"),
            ("CS_Pendencia_Taxa_Completude", "1 - DIVIDE([CS_Pendencia_Total], COUNTROWS(fato_agg_status_documento_redes), 0)", "Percentual"),
        ]),
        ("08 - MobConnect", [
            ("CS_MobConnect_Atividades_30d", "CALCULATE(COUNTROWS(fato_mobconnect_atividades), DATESINPERIOD(Data[Date], TODAY(), -30, DAY))", "Inteiro"),
            ("CS_MobConnect_Adocao_Pct", "DIVIDE(CALCULATE(DISTINCTCOUNT(fato_mobconnect_atividades[sk_contratante])), COUNTROWS(dim_contratante), 0)", "Percentual"),
        ]),
        ("08 - Painel CS", [
            ("CS_Integration_Marker", "\"CS_PANEL_v2\"", "Texto"),
            ("CS_Threshold_Inatividade", "LOOKUPVALUE(_CS_Cluster[threshold], _CS_Cluster[cluster_name], SELECTEDVALUE(dim_contratante[ds_cluster]))", "Inteiro"),
            ("CS_Owner_Email", "LOOKUPVALUE(_CS_Owner[email], _CS_Owner[cluster_name], SELECTEDVALUE(dim_contratante[ds_cluster]))", "Texto"),
            ("CS_Empresas_Target", "LOOKUPVALUE(_CS_Cluster[target], _CS_Cluster[cluster_name], SELECTEDVALUE(dim_contratante[ds_cluster]))", "Inteiro"),
            ("CS_Health_Score_Delta_7d", "[CS_Health_Score] - CALCULATE([CS_Health_Score], DATEADD(Data[Date], -7, DAY))", "Decimal"),
            ("CS_Alerta_Queda_Brusca", "IF(ABS([CS_Health_Score_Delta_7d]) > 15, \"ALERTA\", \"OK\")", "Texto"),
            ("CS_Flag_Inatividade", "VAR _ultimo_acesso = CALCULATE(MAX(fato_status_contratantes[dt_acesso_anterior]), fato_status_contratantes[fl_acesso] = TRUE())\\nVAR _dias = IF(ISBLANK(_ultimo_acesso), 999, DATEDIFF(_ultimo_acesso, TODAY(), DAY))\\nVAR _thr = [CS_Threshold_Inatividade]\\nRETURN IF(_dias >= _thr, \"INATIVO\", \"ATIVO\")", "Texto"),
            ("CS_Flag_Fat_Zerado", "VAR _ultimo_fat = CALCULATE(MAX(fato_status_contratantes[dt_referencia]), fato_status_contratantes[vl_unitario_plano_mobcontrol] > 0)\\nVAR _dias = IF(ISBLANK(_ultimo_fat), 0, DATEDIFF(_ultimo_fat, TODAY(), DAY))\\nRETURN SWITCH(TRUE(), _dias >= 60, \"CHURN_IMINENTE\", _dias >= 31, \"CRITICO\", _dias >= 16, \"ACAO_NECESSARIA\", _dias >= 8, \"ALERTA_LEVE\", \"OK\")", "Texto"),
            ("CS_Flag_Alto_Risco", "IF([CS_Health_Score] < 25 && [CS_Flag_Inatividade] = \"INATIVO\", \"ALTO_RISCO\", \"NORMAL\")", "Texto"),
            ("CS_Tier_Expansao", "VAR _score = [CS_Health_Score]\\nVAR _uso = [CS_Pct_Base_Com_Acesso]\\nRETURN SWITCH(TRUE(), _score > 80 && _uso > 0.80, \"TIER_1\", _score >= 65 && _uso > 0.60, \"TIER_2\", _score >= 50 && _uso > 0.40, \"TIER_3\", \"NENHUM\")", "Texto"),
            ("CS_Contas_Churn_Risk", "CALCULATE(COUNTROWS(fato_status_contratantes), FILTER(ALL(fato_status_contratantes), [CS_Health_Score] < 25))", "Inteiro"),
            ("CS_Contas_Expansao_Tier1", "CALCULATE(COUNTROWS(fato_status_contratantes), FILTER(ALL(fato_status_contratantes), [CS_Tier_Expansao] = \"TIER_1\"))", "Inteiro"),
            ("CS_Score_Medio_Base", "AVERAGEX(ALL(fato_status_contratantes), [CS_Health_Score])", "Decimal"),
            ("CS_Total_Contas_Ativas", "CALCULATE(COUNTROWS(fato_status_contratantes), dim_contratante[ds_status_atual] = \"1\")", "Inteiro"),
            ("CS_Pct_Base_Com_Acesso", "DIVIDE([CS_Contas_Ativas_7d], [CS_Total_Contas_Ativas], 0)", "Percentual"),
            ("CS_MRR_Total", "SUM(fato_status_contratantes[vl_unitario_plano_mobcontrol])", "Moeda"),
            ("CS_Taxa_Churn", "VAR churned = COUNTROWS(FILTER(ALL(fato_status_contratantes), fato_status_contratantes[tp_evento_plano] = \"Churn\"))\\nVAR total = COUNTROWS(FILTER(ALL(dim_contratante), dim_contratante[ds_status_atual] <> BLANK()))\\nRETURN DIVIDE(churned, total, 0)", "Percentual"),
        ]),
        ("09 - Expansao", [
            ("CS_Expansao_Oportunidades", "CALCULATE(COUNTROWS(fato_status_contratantes), FILTER(ALL(fato_status_contratantes), [CS_Tier_Expansao] <> \"NENHUM\"))", "Inteiro"),
        ]),
        ("10 - Onboarding", [
            ("CS_Onboarding_Novos_30d", "CALCULATE(COUNTROWS(dim_contratante), DATESINPERIOD(Data[Date], TODAY(), -30, DAY), dim_contratante[fl_novo] = TRUE())", "Inteiro"),
        ]),
        ("11 - Fraude", [
            ("CS_Score_Fraude", "VAR _Curtas = CALCULATE(COUNTROWS(fato_acesso), fato_acesso[qt_horas_permanencia] < 0.5)\\nVAR _Longas = CALCULATE(COUNTROWS(fato_acesso), fato_acesso[qt_horas_permanencia] > 4)\\nVAR _Total = COUNTROWS(fato_acesso)\\nRETURN ROUND(DIVIDE(_Curtas + _Longas, _Total, 0) * 100, 0)", "Inteiro"),
            ("Score_Risco_Fraude", "VAR _RatioFinalMes = [Ratio Turnover Final Mes]\\nVAR _PctInadimplencia = [% Turnover Inadimplencia]\\nVAR _PctNaoFaturados = [% Nao Faturados]\\nRETURN ROUND((_RatioFinalMes - 1) * 40 + _PctInadimplencia * 30 + _PctNaoFaturados * 30, 0)", "Inteiro"),
        ]),
    ]
    f.write('''<div id="pg-medidas" class="page">
<h2 class="section-title">Cat\u00e1logo de Medidas CS (53 medidas)</h2>
<input type="text" class="search-measures" id="search-measures" placeholder="Buscar medida por nome ou pasta..." oninput="filterMeasures()">
<div id="measures-container">
''')
    total = 0
    for folder, items in measures:
        f.write(f'<h3 style="font-size:12px;font-weight:700;margin:16px 0 8px;color:var(--pri)" data-folder="{folder}">{folder} ({len(items)} medidas)</h3>\n')
        for name, dax, fmt in items:
            total += 1
            dax_display = dax.replace('\\n', '\n').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            f.write(f'''<div class="measure-card" data-name="{name.lower()}" data-folder="{folder.lower()}">
<div class="mh" onclick="this.nextElementSibling.classList.toggle(\'open\')"><span><i class="fas fa-ruler-combined" style="color:var(--pri);margin-right:6px"></i>{name}</span><span class="tag" style="font-size:9px">{fmt}</span></div>
<div class="mb"><pre>{dax_display}</pre><div style="margin-top:6px;font-size:10px;color:var(--tx2)">Display Folder: {folder} | Format: {fmt}</div></div>
</div>\n''')
    f.write(f'</div>\n<p style="margin-top:16px;font-size:11px;color:var(--tx2)">Total: {total} medidas catalogadas</p>\n</div>\n')
