# 🧠 07-AI-Tools — Otimização de Tokens e Prompts

Ferramentas para reduzir custo e melhorar performance com LLMs.

## 🚀 Setup Rápido

```cmd
cd 07-AI-Tools
SETUP.bat
```

## 📦 Ferramentas Incluídas

| Ferramenta | Uso | Comando |
|---|---|---|
| **LLMLingua** | Compressão de prompt (até 20x) | `python compress.py --file contexto.md` |
| **Cache Semântico** | Evita chamadas repetidas | `from cache import cached_llm_call` |
| **Langfuse** | Observabilidade de tokens | Dashboard web |
| **Toolkit-for-Prompt-Compression** | Comparar métodos | Notebooks Jupyter |
| **CPC (Workday)** | Compressão de contexto longo | API Python |

## 🎯 Casos de Uso Mob2Con

### 1. Comprimir Brand Guidelines antes de enviar ao agente
```cmd
python compress.py --file ..\01-Brand-Guidelines\Mob2con-brand-context.md --ratio 0.3
```

### 2. Comprimir documentação DAX
```cmd
python compress.py --file ..\03-Documentacao\Mob2con-dax-medidas-padrao.md --ratio 0.5 --output dax_compressed.md
```

### 3. Cache de perguntas frequentes
```python
from cache import cached_llm_call

# Primeira vez: chama LLM
resp = cached_llm_call("qual a paleta de cores Mob2Con?", call_fn=my_llm)

# Segunda vez: retorna do cache (0 tokens gastos)
resp = cached_llm_call("qual a paleta de cores Mob2Con?", call_fn=my_llm)
```

### 4. Monitorar gastos com Langfuse
```python
from langfuse import Langfuse
langfuse = Langfuse()

trace = langfuse.trace(name="mob2con-dashboard-gen")
# ... suas chamadas ao LLM ...
trace.update(metadata={"project": "Nordestão"})
```

## 📊 Economia Esperada

| Cenário | Tokens Antes | Tokens Depois | Economia |
|---|---|---|---|
| Brand Context completo | ~3000 | ~600 | 80% |
| DAX Medidas | ~2500 | ~800 | 68% |
| Layout Base | ~5000 | ~1500 | 70% |
| Cache hit | qualquer | 0 | 100% |

## ⚙️ Configuração Langfuse (opcional)

Criar `.env` nesta pasta:
```
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com
```
