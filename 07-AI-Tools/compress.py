"""
Mob2Con Prompt Compressor
Comprime prompts longos antes de enviar ao LLM, economizando tokens.

Uso:
  python compress.py "seu prompt longo aqui"
  python compress.py --file caminho/do/arquivo.md
  python compress.py --ratio 0.5 --file contexto.md
"""
import sys
import argparse
from pathlib import Path

def compress_prompt(text: str, ratio: float = 0.5, target_tokens: int = None):
    """Comprime prompt usando LLMLingua."""
    from llmlingua import PromptCompressor
    
    compressor = PromptCompressor(
        model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
        use_llmlingua2=True
    )
    
    kwargs = {"context": [text], "rate": ratio, "force_tokens": ["\n", ".", "?", "!"]}
    if target_tokens:
        kwargs["target_token"] = target_tokens
    
    result = compressor.compress_prompt(**kwargs)
    return result

def count_tokens(text: str) -> int:
    """Conta tokens usando tiktoken."""
    import tiktoken
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(text))

def main():
    parser = argparse.ArgumentParser(description="Mob2Con Prompt Compressor")
    parser.add_argument("text", nargs="?", help="Texto para comprimir")
    parser.add_argument("--file", "-f", help="Arquivo para comprimir")
    parser.add_argument("--ratio", "-r", type=float, default=0.5, help="Taxa de compressão (0.1=muito, 0.9=pouco). Default: 0.5")
    parser.add_argument("--tokens", "-t", type=int, help="Alvo de tokens máximo")
    parser.add_argument("--output", "-o", help="Salvar resultado em arquivo")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        print("Uso: python compress.py 'texto' ou --file arquivo.md")
        sys.exit(1)

    tokens_antes = count_tokens(text)
    print(f"Original: {tokens_antes} tokens ({len(text)} chars)")
    print(f"Comprimindo com ratio={args.ratio}...")

    result = compress_prompt(text, ratio=args.ratio, target_tokens=args.tokens)
    compressed = result["compressed_prompt"]
    tokens_depois = count_tokens(compressed)
    
    economia = (1 - tokens_depois / tokens_antes) * 100
    print(f"Comprimido: {tokens_depois} tokens ({len(compressed)} chars)")
    print(f"Economia: {economia:.1f}% ({tokens_antes - tokens_depois} tokens)")
    print(f"---")
    
    if args.output:
        Path(args.output).write_text(compressed, encoding="utf-8")
        print(f"Salvo em: {args.output}")
    else:
        print(compressed[:500] + ("..." if len(compressed) > 500 else ""))

if __name__ == "__main__":
    main()
