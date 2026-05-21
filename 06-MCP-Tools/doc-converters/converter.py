"""
Mob2Con Doc Converter — Docling + Marker + MinerU
Converte PDFs, DOCX, XLSX, PPTX, imagens → Markdown/JSON para LLMs.

Uso:
    python converter.py arquivo.pdf --engine docling --output md
    python converter.py pasta/ --engine marker --output json
    python converter.py relatorio.pdf --engine mineru
"""

import argparse
import json
from pathlib import Path


def convert_docling(input_path: Path, output_format: str = "md") -> str:
    """Docling: melhor para tabelas complexas e documentos Office."""
    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    result = converter.convert(str(input_path))

    if output_format == "json":
        return json.dumps(result.document.export_to_dict(), ensure_ascii=False, indent=2)
    return result.document.export_to_markdown()


def convert_marker(input_path: Path, output_format: str = "md") -> str:
    """Marker: melhor para PDFs com imagens, equações e artefatos."""
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict

    models = create_model_dict()
    converter = PdfConverter(artifact_dict=models)
    rendered = converter(str(input_path))

    if output_format == "json":
        return json.dumps(rendered.metadata, ensure_ascii=False, indent=2)
    return rendered.markdown


def convert_mineru(input_path: Path, output_format: str = "md") -> str:
    """MinerU: melhor para documentos científicos com fórmulas e gráficos."""
    from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
    from magic_pdf.pipe.UNIPipe import UNIPipe

    output_dir = input_path.parent / f"{input_path.stem}_mineru"
    output_dir.mkdir(exist_ok=True)

    reader = FileBasedDataReader("")
    pdf_bytes = reader.read(str(input_path))

    pipe = UNIPipe(pdf_bytes, [], image_writer=FileBasedDataWriter(str(output_dir)))
    pipe.pipe_classify()
    pipe.pipe_analyze()
    pipe.pipe_parse()

    md_content = pipe.pipe_mk_markdown("", str(output_dir))

    if output_format == "json":
        return json.dumps({"content": md_content, "source": str(input_path)}, ensure_ascii=False, indent=2)
    return md_content


ENGINES = {
    "docling": convert_docling,
    "marker": convert_marker,
    "mineru": convert_mineru,
}


def convert(input_path: str, engine: str = "docling", output_format: str = "md") -> str:
    """Interface unificada para conversão."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    fn = ENGINES.get(engine)
    if not fn:
        raise ValueError(f"Engine inválida: {engine}. Use: {list(ENGINES.keys())}")

    return fn(path, output_format)


def batch_convert(folder: str, engine: str = "docling", output_format: str = "md", extensions: tuple = (".pdf", ".docx", ".xlsx", ".pptx")):
    """Converte todos os documentos de uma pasta."""
    folder_path = Path(folder)
    output_dir = folder_path / "converted"
    output_dir.mkdir(exist_ok=True)

    for file in folder_path.iterdir():
        if file.suffix.lower() in extensions:
            try:
                result = convert(str(file), engine, output_format)
                out_file = output_dir / f"{file.stem}.{output_format}"
                out_file.write_text(result, encoding="utf-8")
                print(f"✅ {file.name} → {out_file.name}")
            except Exception as e:
                print(f"❌ {file.name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mob2Con Doc Converter")
    parser.add_argument("input", help="Arquivo ou pasta para converter")
    parser.add_argument("--engine", choices=list(ENGINES.keys()), default="docling")
    parser.add_argument("--output", choices=["md", "json"], default="md")
    parser.add_argument("--batch", action="store_true", help="Converter pasta inteira")
    args = parser.parse_args()

    if args.batch or Path(args.input).is_dir():
        batch_convert(args.input, args.engine, args.output)
    else:
        result = convert(args.input, args.engine, args.output)
        out_path = Path(args.input).with_suffix(f".{args.output}")
        out_path.write_text(result, encoding="utf-8")
        print(f"✅ Salvo em: {out_path}")
