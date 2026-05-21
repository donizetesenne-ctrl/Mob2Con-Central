# 🎉 Dashboard Online — Link Ativo!

## 🔗 Link do Dashboard

**Acesse aqui:** https://script.google.com/macros/s/AKfycbwkF4in7_FjTDUwruBtl-LRGw5ugQcrMmdb63TbJO091MGJu4y_1keuHRrdFrLyxTrdZw/exec

---

## ✅ Status da Publicação

- **Data de publicação:** 15/05/2026 às 15:35
- **Arquivo HTML no Drive:** `📊 Dashboard Dados Reais.html`
- **ID do arquivo:** `1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc`
- **Apps Script Project ID:** `1lh1BffvyiRMEV4wHpAXQLw05gLx7jIKO7qxGOSNcWfaF9O7otZOUpFtF`
- **Tamanho do arquivo:** 124.844 bytes (122 KB)
- **Backup criado:** ✅ Sim (ID: `1FTAcQoBimEVpaQZp3fRqddp3gA0WVJfo`)

---

## 📊 Conteúdo Integrado

O dashboard online agora inclui:

### ✅ Dados Rede 2.0 (7 redes)
- COOPNOVA
- NOVA ERA
- BIGBOX
- NORDESTÃO
- GRUPO CENCOSUD
- INATIVOS
- MERCADINHO SÃO LUIZ

### ✅ Dados Gestão Performance (6 redes)
- GBARBOSA (93% confiabilidade)
- NORDESTÃO (93% confiabilidade)
- NOVA ERA (93% confiabilidade)
- PREZUNIC (93% confiabilidade)
- BIGBOX (86% confiabilidade)
- PAGUE MENOS (0% confiabilidade - CRÍTICO)

### 📈 Abas Disponíveis
1. **🧠 Análise Crítica (CEO)** — Visão executiva consolidada
2. **Visão Geral** — KPIs principais e alertas
3. **Vendas** — Evolução e análise por unidade
4. **Ruptura** — Comercial e operacional
5. **Operacional** — Horas e visitas
6. **Fornecedores** — Top 10 por rede
7. **Redes** — Performance consolidada
8. **👥 Promotores** — Status e alocação
9. **📋 Contratos** — Pontuais e semanais
10. **📄 Documentação** — Regularização

---

## 🔄 Como Atualizar o Dashboard

### Opção 1: Via MCP Universal Control (Automático)

```javascript
// O dashboard já está configurado para atualizar automaticamente
// Basta editar o arquivo local e sincronizar:

mcp_universal_control_sync_local_drive({
  direction: "local_to_drive",
  driveFileId: "1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc",
  localPath: "C:\\Users\\Donizete Senne\\Desktop\\dashboard-dados-reais.html",
  mimeType: "text/html",
  overwrite: true
})
```

### Opção 2: Via Google Drive (Manual)

1. Acesse: https://drive.google.com/file/d/1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc/view
2. Clique em "Abrir com" → "Editor de texto"
3. Cole o novo código HTML
4. Salve (Ctrl+S)
5. Aguarde 1-2 minutos para o cache atualizar
6. Recarregue o link do dashboard

### Opção 3: Via Apps Script Editor

1. Acesse: https://script.google.com/home/projects/1lh1BffvyiRMEV4wHpAXQLw05gLx7jIKO7qxGOSNcWfaF9O7otZOUpFtF/edit
2. O código já está configurado para buscar o HTML do Drive
3. Não precisa alterar nada no Apps Script
4. Apenas atualize o arquivo HTML no Drive

---

## 🎯 Recursos Especiais

### 🔒 Governança e Confiabilidade
- Indicadores de confiabilidade por rede
- Alertas automáticos para redes com problemas
- Métricas de qualidade de dados

### 📊 Gestão de Performance
- Horas projetadas vs realizadas
- GAP de execução por rede
- Top 10 fornecedores por ruptura operacional

### 🧠 Visão Executiva (CEO)
- KPIs consolidados
- Gráficos de tendência
- Alertas críticos
- Scorecard por rede

---

## 🔧 Configuração Técnica

### Apps Script (doGet)
```javascript
var HTML_FILE_ID = '1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc';

function doGet() {
  var file = DriveApp.getFileById(HTML_FILE_ID);
  var html = file.getBlob().getDataAsString('UTF-8');
  return HtmlService.createHtmlOutput(html)
    .setTitle('Dashboard Mob2Con — Analítico RG 2.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
```

### Permissões
- **Acesso:** ANYONE_ANONYMOUS (público)
- **Execução:** USER_DEPLOYING (donizete.senne@mob2con.com.br)
- **Timezone:** America/Sao_Paulo

---

## 📱 Compartilhamento

### Link Curto (Recomendado)
Crie um link curto usando:
- **Bitly:** https://bitly.com
- **TinyURL:** https://tinyurl.com
- **Google URL Shortener:** https://goo.gl (descontinuado, use Bitly)

### QR Code
Gere um QR Code para acesso mobile:
- **QR Code Generator:** https://www.qr-code-generator.com
- Cole o link do dashboard
- Baixe a imagem PNG
- Compartilhe via WhatsApp/Email

---

## 🚨 Troubleshooting

### Dashboard não carrega
1. Verifique se o arquivo HTML está no Drive (ID: `1dnUoVDNuBkk_0IRF32kod8K5gEO-31cc`)
2. Confirme que o Apps Script está publicado como Web App
3. Limpe o cache do navegador (Ctrl+Shift+Delete)
4. Tente em modo anônimo/privado

### Dados não aparecem
1. Abra o console do navegador (F12)
2. Verifique erros JavaScript
3. Confirme que os objetos `DATA_REDES`, `DATA_GESTAO_PERFORMANCE` estão definidos
4. Teste a função `renderActive()` no console

### Gráficos não renderizam
1. Verifique se o Highcharts está carregando (console)
2. Confirme que os elementos `<div id="...">` existem
3. Teste em outro navegador
4. Verifique conexão com CDN do Highcharts

---

## 📞 Suporte

**Desenvolvido por:** Kiro AI + MCP Universal Control  
**Data:** 15/05/2026  
**Versão:** 2.0 (com integração Gestão Performance)  

**Contato:**  
- Email: donizete.senne@mob2con.com.br  
- Empresa: Mob2Con  

---

## 🎉 Pronto!

Seu dashboard está **ONLINE** e **FUNCIONANDO**! 🚀

Acesse agora: https://script.google.com/macros/s/AKfycbwkF4in7_FjTDUwruBtl-LRGw5ugQcrMmdb63TbJO091MGJu4y_1keuHRrdFrLyxTrdZw/exec
