#!/usr/bin/env node
"use strict";

const fs = require("fs");
const http = require("http");
const path = require("path");
const { execFile } = require("child_process");

const folder = __dirname;
const secretsPath = path.join(folder, "ucm-secrets.json");
const configuredSecrets = readSecrets();
const credentialsDir = path.join(folder, "credentials");
const clientPath = configuredSecrets.GOOGLE_OAUTH_CLIENT_JSON || path.join(credentialsDir, "google-oauth-client.json");
const tokenPath = configuredSecrets.GOOGLE_OAUTH_TOKEN_JSON || path.join(credentialsDir, "google-oauth-token.json");

const scopes = [
  "https://www.googleapis.com/auth/drive",
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/documents",
  "https://www.googleapis.com/auth/presentations",
  "https://www.googleapis.com/auth/gmail.readonly",
  "https://www.googleapis.com/auth/calendar.readonly",
  "https://www.googleapis.com/auth/script.projects",
  "https://www.googleapis.com/auth/script.deployments",
  "https://www.googleapis.com/auth/script.processes",
  "https://www.googleapis.com/auth/script.scriptapp",
  "https://www.googleapis.com/auth/script.external_request",
];

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});

async function main() {
  if (!fs.existsSync(path.dirname(clientPath))) fs.mkdirSync(path.dirname(clientPath), { recursive: true });
  if (!fs.existsSync(path.dirname(tokenPath))) fs.mkdirSync(path.dirname(tokenPath), { recursive: true });

  if (!fs.existsSync(clientPath)) {
    console.log("");
    console.log("Falta o OAuth client JSON.");
    console.log(`Coloque o arquivo aqui: ${clientPath}`);
    console.log("");
    console.log("No Google Cloud, crie em:");
    console.log("APIs e servicos > Credenciais > Criar credenciais > ID do cliente OAuth > Aplicativo para computador");
    console.log("Depois baixe o JSON e renomeie para google-oauth-client.json.");
    console.log("");
    process.exit(1);
  }

  // Remove token antigo para forcar reautorizacao completa
  if (fs.existsSync(tokenPath)) {
    fs.unlinkSync(tokenPath);
    console.log("Token antigo removido. Reautorizacao necessaria.");
  }

  const client = readClient();
  ensureSecrets();

  const port = 53682;
  const redirectUri = `http://localhost:${port}/oauth2callback`;
  const authUrl = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  authUrl.search = new URLSearchParams({
    client_id: client.client_id,
    redirect_uri: redirectUri,
    response_type: "code",
    scope: scopes.join(" "),
    access_type: "offline",
    prompt: "consent",
  }).toString();

  console.log("");
  console.log("Abra esta URL no navegador e autorize sua conta Google:");
  console.log("");
  console.log(authUrl.toString());
  console.log("");
  openBrowser(authUrl.toString());

  const code = await waitForCode(port);
  const response = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      code,
      client_id: client.client_id,
      client_secret: client.client_secret,
      redirect_uri: redirectUri,
      grant_type: "authorization_code",
    }),
  });

  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(text);
  }
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${JSON.stringify(data, null, 2)}`);

  const token = {
    access_token: data.access_token,
    refresh_token: data.refresh_token,
    scope: data.scope,
    token_type: data.token_type,
    expires_at: Date.now() + (Number(data.expires_in || 3600) * 1000),
  };
  fs.writeFileSync(tokenPath, JSON.stringify(token, null, 2));

  console.log("");
  console.log("OAuth configurado com sucesso!");
  console.log(`Token salvo em: ${tokenPath}`);
  console.log(`Escopos: ${data.scope}`);
  console.log("");
  console.log("Reinicie o VS Code/Kiro e teste novamente.");
  console.log("");
}

function openBrowser(url) {
  try {
    execFile("cmd", ["/c", "start", "", url], { windowsHide: true });
  } catch {}
}

function readClient() {
  const raw = JSON.parse(fs.readFileSync(clientPath, "utf8"));
  const client = raw.installed || raw.web || raw;
  if (!client.client_id || !client.client_secret) {
    throw new Error("Arquivo google-oauth-client.json invalido.");
  }
  return client;
}

function ensureSecrets() {
  let secrets = readSecrets();
  secrets.GOOGLE_OAUTH_CLIENT_JSON = clientPath;
  secrets.GOOGLE_OAUTH_TOKEN_JSON = tokenPath;
  secrets.APPSHEET_REGION = secrets.APPSHEET_REGION || "www.appsheet.com";
  secrets.UCM_MAX_CELLS = secrets.UCM_MAX_CELLS || "5000";
  fs.writeFileSync(secretsPath, JSON.stringify(secrets, null, 2));
}

function readSecrets() {
  if (!fs.existsSync(secretsPath)) return {};
  return JSON.parse(fs.readFileSync(secretsPath, "utf8").replace(/^\uFEFF/, ""));
}

function waitForCode(port) {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      try {
        const url = new URL(req.url, `http://localhost:${port}`);
        if (url.pathname !== "/oauth2callback") {
          res.writeHead(404);
          res.end("Not found");
          return;
        }

        const error = url.searchParams.get("error");
        if (error) throw new Error(error);

        const code = url.searchParams.get("code");
        if (!code) throw new Error("Codigo OAuth nao recebido.");

        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end("<h1>Autorizado com sucesso</h1><p>Voce pode fechar esta aba e voltar ao terminal.</p>");
        server.close();
        resolve(code);
      } catch (error) {
        res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
        res.end(error.message);
        server.close();
        reject(error);
      }
    });

    server.listen(port, "localhost", () => {
      console.log(`Aguardando autorizacao em http://localhost:${port}/oauth2callback ...`);
      console.log("");
    });
  });
}
