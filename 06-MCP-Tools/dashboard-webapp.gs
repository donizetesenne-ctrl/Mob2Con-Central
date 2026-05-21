/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║  DASHBOARD ANALÍTICO RG 2.0 — WEB APP COMPLETO                              ║
 * ║  Mob2Con · Maio 2026                                                         ║
 * ║                                                                              ║
 * ║  FUNÇÃO: Servir o dashboard HTML completo via Google Apps Script            ║
 * ║  MÉTODO: Web App que retorna o HTML do dashboard                            ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

function doGet() {
  return HtmlService.createHtmlOutputFromFile('dashboard')
    .setTitle('Analítico RG 2.0 — Dashboard Mob2Con')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║  INSTRUÇÕES DE IMPLANTAÇÃO                                                   ║
 * ╠══════════════════════════════════════════════════════════════════════════════╣
 * ║                                                                              ║
 * ║  1. Abra o Google Apps Script Editor:                                       ║
 * ║     https://script.google.com                                                ║
 * ║                                                                              ║
 * ║  2. Crie um novo projeto: "Dashboard RG 2.0 Web App"                        ║
 * ║                                                                              ║
 * ║  3. Cole este código no arquivo Code.gs                                     ║
 * ║                                                                              ║
 * ║  4. Crie um novo arquivo HTML:                                               ║
 * ║     - Clique em + ao lado de "Files"                                         ║
 * ║     - Escolha "HTML"                                                         ║
 * ║     - Nome: "dashboard"                                                      ║
 * ║     - Cole o conteúdo do arquivo "📊 Dashboard Dados Reais.html"            ║
 * ║                                                                              ║
 * ║  5. Implante como Web App:                                                   ║
 * ║     - Deploy → New deployment                                                ║
 * ║     - Type: Web app                                                          ║
 * ║     - Execute as: Me                                                         ║
 * ║     - Who has access: Anyone                                                 ║
 * ║     - Deploy                                                                 ║
 * ║                                                                              ║
 * ║  6. Copie a URL do Web App                                                   ║
 * ║     Exemplo: https://script.google.com/macros/s/AKfyc.../exec               ║
 * ║                                                                              ║
 * ║  7. Compartilhe o link!                                                      ║
 * ║                                                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */
