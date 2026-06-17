#!/usr/bin/env python3
"""Transcreve um arquivo de áudio (ogg/opus/mp3/wav) para texto via faster-whisper.

Uso:
    python3 scripts/transcrever_audio.py --input ARQUIVO.ogg [--model medium] [--lang pt] [--out saida.md]

Saída: imprime a transcrição e, se --out for dado, salva em markdown com segmentos timestamped.
Parte da pipeline generic-nb-lm-agentic-search (etapa P-1: transcrição de fonte de áudio).
"""
import argparse
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="arquivo de áudio")
    ap.add_argument("--model", default="medium", help="tamanho do modelo whisper (small/medium/large-v3)")
    ap.add_argument("--lang", default="pt", help="código do idioma (pt, en, ...)")
    ap.add_argument("--out", default=None, help="caminho do .md de saída (opcional)")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    audio = Path(args.input)
    if not audio.exists():
        sys.exit(f"ERRO: arquivo não encontrado: {audio}")

    print(f"[transcrever] carregando modelo '{args.model}' (CPU, int8)...", file=sys.stderr)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    print(f"[transcrever] transcrevendo {audio.name} (lang={args.lang})...", file=sys.stderr)
    segments, info = model.transcribe(
        str(audio),
        language=args.lang,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    seg_lines = []
    full_text = []
    for seg in segments:
        ts = f"[{seg.start:6.1f}s → {seg.end:6.1f}s]"
        line = f"{ts} {seg.text.strip()}"
        print(line)
        seg_lines.append(line)
        full_text.append(seg.text.strip())

    transcript = " ".join(full_text)

    if args.out:
        out = Path(args.out)
        with out.open("w", encoding="utf-8") as f:
            f.write(f"# Transcrição — {audio.name}\n\n")
            f.write(f"- **Duração:** {info.duration:.1f}s\n")
            f.write(f"- **Idioma detectado:** {info.language} (prob. {info.language_probability:.2f})\n")
            f.write(f"- **Modelo:** faster-whisper `{args.model}`\n\n")
            f.write("## Texto corrido\n\n")
            f.write(transcript + "\n\n")
            f.write("## Segmentos (timestamped)\n\n")
            f.write("\n".join(seg_lines) + "\n")
        print(f"\n[transcrever] salvo em {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
