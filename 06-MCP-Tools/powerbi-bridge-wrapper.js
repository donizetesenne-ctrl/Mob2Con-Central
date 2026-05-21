#!/usr/bin/env node
/**
 * Wrapper MCP para powerbi-bridge
 * 
 * Problema: o server.js original imprime banner colorido no stdout,
 * quebrando o protocolo JSON-RPC do MCP.
 * 
 * Solução: spawna o server.js, filtra o stdout deixando passar só linhas
 * que começam com { (JSON) e redireciona o banner para stderr.
 */
const { spawn } = require('child_process');
const path = require('path');

const serverPath = path.join(
  'C:\\Users\\DONIZE~1\\Downloads\\Mob2Con-Bridge-v2.0.0\\mcp',
  'server.js'
);

const child = spawn('node', [serverPath], {
  env: process.env,
  stdio: ['pipe', 'pipe', 'pipe']
});

// stdin do pai -> stdin do filho
process.stdin.pipe(child.stdin);

// stdout do filho: filtra só JSON-RPC
let stdoutBuffer = '';
child.stdout.on('data', (chunk) => {
  stdoutBuffer += chunk.toString('utf8');
  const lines = stdoutBuffer.split('\n');
  stdoutBuffer = lines.pop(); // guarda a ultima linha (pode estar incompleta)

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    // Só passa linhas que começam com { (JSON-RPC) - resto vira log em stderr
    if (trimmed.startsWith('{')) {
      process.stdout.write(line + '\n');
    } else {
      process.stderr.write('[bridge-log] ' + line + '\n');
    }
  }
});

// stderr do filho -> stderr do pai
child.stderr.pipe(process.stderr);

// propagar exit code
child.on('exit', (code) => {
  if (stdoutBuffer.trim().startsWith('{')) {
    process.stdout.write(stdoutBuffer + '\n');
  }
  process.exit(code ?? 0);
});

child.on('error', (err) => {
  process.stderr.write('[bridge-wrapper] erro: ' + err.message + '\n');
  process.exit(1);
});
