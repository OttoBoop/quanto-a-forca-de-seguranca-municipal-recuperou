#!/usr/bin/env python3
"""
gerar_pdf_curto.py — Converte .md curto para PDF de 1 página.

Especificação: Times New Roman 12pt, espaçamento 1.5, margens 2.5cm, A4.
Validado: ~325-340 palavras cabem em 1 página com essa configuração.

Uso:
    python gerar_pdf_curto.py --input documento.md
    python gerar_pdf_curto.py --input documento.md --output saida.pdf

Dependência: weasyprint  (pip install weasyprint)
"""
import argparse
import re
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description="Converte .md curto em PDF de 1 página (Times 12pt, 1.5, A4)")
parser.add_argument("--input", required=True, help="Caminho do .md de entrada")
parser.add_argument("--output", help="Caminho do .pdf de saída (padrão: mesmo nome do input)")
args = parser.parse_args()

md_path = Path(args.input)
pdf_path = Path(args.output) if args.output else md_path.with_suffix(".pdf")

if not md_path.exists():
    print(f"Erro: arquivo não encontrado: {md_path}")
    sys.exit(1)

text = md_path.read_text(encoding="utf-8")


def md_to_html_body(md):
    lines = md.split("\n")
    html = []
    for line in lines:
        if line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("**") and line.endswith("**") and len(line) > 4:
            html.append(f"<h3>{line[2:-2]}</h3>")
        elif line.strip() == "---":
            html.append("<hr>")
        elif line.strip() == "":
            html.append("")
        else:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            html.append(f"<p>{line}</p>")
    return "\n".join(html)


body = md_to_html_body(text)

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: A4;
    margin: 2.5cm 2.5cm 2.5cm 2.5cm;
  }}
  body {{
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
    text-align: justify;
  }}
  h1 {{
    font-size: 13pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 4pt;
    margin-top: 0;
  }}
  h2 {{
    font-size: 12pt;
    font-weight: bold;
    margin-top: 8pt;
    margin-bottom: 2pt;
  }}
  h3 {{
    font-size: 12pt;
    font-weight: bold;
    margin-top: 10pt;
    margin-bottom: 2pt;
    display: inline;
  }}
  p {{
    margin: 0 0 6pt 0;
    text-indent: 1.25cm;
  }}
  p:first-of-type {{
    text-indent: 0;
  }}
  hr {{
    border: none;
    border-top: 1px solid #000;
    margin: 6pt 0;
  }}
  strong {{
    font-weight: bold;
  }}
</style>
</head>
<body>
{body}
</body>
</html>"""

html_path = pdf_path.with_suffix(".html")
html_path.write_text(html, encoding="utf-8")

try:
    from weasyprint import HTML
    HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    html_path.unlink()  # limpa o HTML intermediário

    # Verifica número de páginas
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        pages = len(doc)
        doc.close()
        status = "✅ 1 página" if pages == 1 else f"⚠️  {pages} páginas"
    except ImportError:
        status = "(instale pymupdf para verificar nº de páginas)"

    print(f"PDF gerado: {pdf_path}")
    print(f"Páginas: {status}")
    print(f"Tamanho: {pdf_path.stat().st_size // 1024} KB")

except ImportError:
    print("Erro: weasyprint não instalado. Execute: pip install weasyprint")
    sys.exit(1)
