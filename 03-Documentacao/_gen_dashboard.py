# -*- coding: utf-8 -*-
"""
Gerador de Dashboard HTML - Analise Estudo Cadastro Promotores
Mob2Con - Brand: #F46901 (orange), Raleway, Grid 8px
"""
import os

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "ANALISE-ESTUDO-CADASTRO-PROMOTORES.html")

def generate_html():
    """Gera o HTML completo do dashboard."""
    html = []
    html.append(get_head())
    html.append(get_css())
    html.append(get_body_start())
    html.append(get_sidebar())
    html.append(get_main_start())
    html.append(get_filter_bar())
    html.append(get_page_resumo())
    html.append(get_page_pg01())
    html.append(get_page_pg02())
    html.append(get_page_pg03())
    html.append(get_page_pg04())
    html.append(get_page_pg05())
    html.append(get_page_pg06())
    html.append(get_page_pg07())
    html.append(get_page_pg08())
    html.append(get_page_pg09())
    html.append(get_page_pg10())
    html.append(get_page_clusters())
    html.append(get_page_modelo())
    html.append(get_main_end())
    html.append(get_scripts())
    html.append("</body></html>")
    return "\n".join(html)

def get_head():
    return '''<!DOCTYPE html>
<html lang="pt-BR" data-t="l">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Analise Estudo Cadastro Promotores - Mob2Con</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;700;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
'''

def get_css():
    return '''<style>
:root{--pri:#F46901;--green:#16A34A;--red:#DC2626;--yellow:#EAB308;--blue:#2563EB;
--bg:#FFFFFF;--bg2:#F8F9FA;--text:#1A1A1A;--text2:#6B7280;--border:#E5E7EB;
--card:#FFFFFF;--sidebar-bg:#1A1A1A;--sidebar-text:#FFFFFF;--g:8px;--radius:8px}
