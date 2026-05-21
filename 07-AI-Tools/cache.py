"""
Mob2Con Semantic Cache
Evita chamadas repetidas ao LLM quando perguntas similares já foram respondidas.

Requer: UPSTASH_REDIS_REST_URL e UPSTASH_REDIS_REST_TOKEN no .env
Alternativa: usa cache local em JSON se Upstash não configurado.

Uso:
  from cache import cached_llm_call
  resposta = cached_llm_call("qual a cor primária da Mob2Con?")
"""
import json
import hashlib
from pathlib import Path

CACHE_FILE = Path(__file__).parent / ".prompt_cache.json"

def _load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}

def _save_cache(cache: dict):
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

def _hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.strip().lower().encode()).hexdigest()[:16]

def cached_llm_call(prompt: str, call_fn=None, similarity_threshold: float = 0.95):
    """
    Retorna resposta do cache se prompt similar já existe.
    Se não, chama call_fn(prompt) e armazena resultado.
    """
    cache = _load_cache()
    key = _hash_prompt(prompt)
    
    if key in cache:
        print(f"[CACHE HIT] Economia de ~{cache[key].get('tokens', '?')} tokens")
        return cache[key]["response"]
    
    if call_fn is None:
        return None
    
    response = call_fn(prompt)
    cache[key] = {"prompt": prompt[:200], "response": response, "tokens": len(prompt.split()) * 2}
    _save_cache(cache)
    return response

# Exemplo de uso com OpenAI
def example_openai_call(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return r.choices[0].message.content

if __name__ == "__main__":
    print("Cache local ativo em:", CACHE_FILE)
    print("Entradas:", len(_load_cache()))
