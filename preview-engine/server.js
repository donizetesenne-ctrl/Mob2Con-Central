const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static(__dirname));

const mcpConfigPath = 'C:\\Users\\Donizete Senne\\.kiro\\settings\\mcp.json';

function getActiveProjectPath() {
    try {
        const config = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf8'));
        let projectPath = config.mcpServers['powerbi-layout'].env.POWERBI_PROJECT_PATH;
        // Normalização de caminho para evitar erros de case ou typo
        if (projectPath.includes('Nortestão')) projectPath = projectPath.replace('Nortestão', 'Nordestão');
        return projectPath;
    } catch (e) {
        console.error("Erro ao ler mcp.json:", e);
        return null;
    }
}

// GET: Retorna o layout atual
app.get('/api/layout', (req, res) => {
    const projectPath = getActiveProjectPath();
    if (!projectPath) return res.status(500).json({ error: "Projeto não encontrado" });

    const reportPath = projectPath.replace('.pbip', '.Report');
    const pagesDir = path.join(reportPath, 'definition', 'pages');

    try {
        const pages = fs.readdirSync(pagesDir).filter(f => fs.statSync(path.join(pagesDir, f)).isDirectory() && f !== '.pbi');
        const layoutData = { pages: [] };

        for (const pageName of pages) {
            const pagePath = path.join(pagesDir, pageName, 'page.json');
            if (fs.existsSync(pagePath)) {
                const pageInfo = JSON.parse(fs.readFileSync(pagePath, 'utf8'));
                const visualsDir = path.join(pagesDir, pageName, 'visuals');
                const visuals = [];

                if (fs.existsSync(visualsDir)) {
                    const visualFolders = fs.readdirSync(visualsDir).filter(f => fs.statSync(path.join(visualsDir, f)).isDirectory());
                    for (const vFolder of visualFolders) {
                        const vPath = path.join(visualsDir, vFolder, 'visual.json');
                        if (fs.existsSync(vPath)) {
                            const visualJson = JSON.parse(fs.readFileSync(vPath, 'utf8'));
                            visuals.push({
                                folderName: vFolder,
                                ...visualJson
                            });
                        }
                    }
                }

                layoutData.pages.push({
                    name: pageName,
                    displayName: pageInfo.displayName,
                    visuals: visuals
                });
            }
        }
        res.json(layoutData);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// POST: Atualiza múltiplos visuais (Batch Update) com backup
app.post('/api/update-layout', (req, res) => {
    const { pageName, updates } = req.body; // updates: [{ folderName, position }]
    const projectPath = getActiveProjectPath();
    if (!projectPath) return res.status(500).json({ error: "Projeto não encontrado" });

    const reportPath = projectPath.replace('.pbip', '.Report');
    const results = [];

    try {
        for (const update of updates) {
            const visualPath = path.join(reportPath, 'definition', 'pages', pageName, 'visuals', update.folderName, 'visual.json');
            
            if (fs.existsSync(visualPath)) {
                // 1. Criar Backup (.bak)
                fs.copyFileSync(visualPath, visualPath + '.bak');

                // 2. Atualizar JSON
                const visualData = JSON.parse(fs.readFileSync(visualPath, 'utf8'));
                
                // Aplicar Grid de 8px forçado
                visualData.position = {
                    x: Math.round(update.position.x / 8) * 8,
                    y: Math.round(update.position.y / 8) * 8,
                    width: Math.round(update.position.width / 8) * 8,
                    height: Math.round(update.position.height / 8) * 8,
                    z: update.position.z
                };

                fs.writeFileSync(visualPath, JSON.stringify(visualData, null, 2));
                results.push({ folderName: update.folderName, status: 'success' });
            }
        }
        res.json({ success: true, results });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.listen(port, () => {
    console.log(`Kiro High-Agility Editor rodando em http://localhost:${port}`);
});
