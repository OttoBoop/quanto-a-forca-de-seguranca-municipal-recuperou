#!/usr/bin/env python3
"""TEMPLATE GENÉRICO (agentic-study-latex) — distribuições + Monte Carlo de um total.

Domínio-agnóstico: dado um JSON de "componentes" (cada um com uma contagem e amostras
de valor por base), constrói a distribuição de valor por componente e a distribuição do
TOTAL por simulação de Monte Carlo, e gera os gráficos + estatísticas.

Modelo: para cada base b, V^b = sum_c sum_{k=1..count_c} draw(samples_c^b).
(Caso "valor de bens": componente = categoria de item, count = N_i, bases = revenda/reposição.
 Mas serve para qualquer estudo: count=1 e uma única base, se for o caso.)

INPUT JSON (--input, default agg_input.json):
{
  "title": "Distribuição de valor ...",
  "bases":  [{"key":"rev","label":"revenda"}, {"key":"rep","label":"reposição"}],
  "components": [
     {"label":"Celulares", "count":118, "samples":{"rev":[...], "rep":[...]}},
     {"label":"Bicicletas","count":19,  "samples":{"rev":[...], "rep":[...]}}
  ]
}
(count default = 1; use 1 base se o estudo não tiver duas. Monte o JSON a partir da
saída da FASE 3 — a combinação componente↔contagem é específica do seu modelo.)

Uso: python monte_carlo_dist.py --input agg_input.json [--figdir figuras] [--stats dist_stats.md]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "DejaVu Sans", "axes.edgecolor": "#888888", "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
})

SEED = 20260616
RNG = np.random.default_rng(SEED)
N_ITER = 50_000
PALETTE = ["#2C6E9B", "#C9772E", "#3F8F5B", "#9B4DA0", "#777777"]

ap = argparse.ArgumentParser()
ap.add_argument("--input", default="agg_input.json")
ap.add_argument("--figdir", default="figuras")
ap.add_argument("--stats", default="dist_stats.md")
ap.add_argument("--exclude", nargs="*", default=[], help="labels de componente a excluir")
ARGS = ap.parse_args()

BASE = Path(__file__).resolve().parent
FIG = BASE / ARGS.figdir
FIG.mkdir(parents=True, exist_ok=True)


def fmt(v):
    if abs(v) >= 1e6:
        return f"{v/1e6:.2f} mi".replace(".", ",")
    if abs(v) >= 1e3:
        return f"{v:,.0f}".replace(",", ".")
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pool(comp, bkey):
    arr = np.array((comp.get("samples") or {}).get(bkey) or [], dtype=float)
    return arr[arr > 0]


def unit_sample(comp, bkey, size):
    p = pool(comp, bkey)
    return RNG.choice(p, size=size, replace=True) if p.size else np.array([])


def total_sample(comps, bkey, n_iter=N_ITER):
    total = np.zeros(n_iter)
    for c in comps:
        p = pool(c, bkey)
        if not p.size:
            continue
        n = int(c.get("count", 1))
        total += RNG.choice(p, size=n * n_iter, replace=True).reshape(n_iter, n).sum(axis=1)
    return total


def main():
    f = Path(ARGS.input)
    if not f.exists():
        sys.exit(f"ERRO: {f} não encontrado. Monte o JSON de agregação (ver docstring).")
    cfg = json.loads(f.read_text(encoding="utf-8"))
    bases = cfg.get("bases") or [{"key": "v", "label": "valor"}]
    comps = [c for c in cfg["components"] if c["label"] not in ARGS.exclude]
    title = cfg.get("title", "Distribuição de valor")
    out = [f"# {ARGS.stats} — Monte Carlo (seed {SEED}, {N_ITER} iter)\n"]

    # ---- por componente ----
    n = len(comps)
    cols = 2 if n > 1 else 1
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5.5 * cols, 3.6 * rows), facecolor="white", squeeze=False)
    out.append("## Por componente (valor de UMA unidade)\n\n| Componente | base | E | desvio | p5 | p95 |\n|---|---|--:|--:|--:|--:|")
    for i, c in enumerate(comps):
        ax = axes.flat[i]
        for j, b in enumerate(bases):
            s = unit_sample(c, b["key"], 200_000)
            if not s.size:
                continue
            col = PALETTE[j % len(PALETTE)]
            hi = np.percentile(s, 99.5)
            ax.hist(s, bins=40, range=(s.min(), hi), density=True, color=col, alpha=0.30)
            try:
                kde = gaussian_kde(RNG.choice(s, size=min(s.size, 20_000), replace=False))
                xs = np.linspace(s.min(), hi, 400)
                ax.plot(xs, kde(xs), color=col, lw=1.9, label=b["label"])
            except Exception:
                ax.plot([], [], color=col, label=b["label"])
            out.append(f"| {c['label']} | {b['label']} | {fmt(s.mean())} | {fmt(s.std())} | {fmt(np.percentile(s,5))} | {fmt(np.percentile(s,95))} |")
        ax.set_title(c["label"], fontsize=12, fontweight="bold", color="#2C3E50")
        ax.set_xlabel("valor de uma unidade"); ax.set_ylabel("densidade"); ax.legend(fontsize=8, frameon=False)
    for k in range(n, rows * cols):
        axes.flat[k].axis("off")
    fig.suptitle(title + " — por componente", fontsize=14, fontweight="bold", color="#2C3E50")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG / "dist_itens.png", dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("  ✓ dist_itens.png")

    # ---- total (Monte Carlo) ----
    fig, ax = plt.subplots(figsize=(11, 6), facecolor="white")
    out.append(f"\n## Total (Monte Carlo, {N_ITER} iter)\n\n| base | E | p5 | p95 |\n|---|--:|--:|--:|")
    scale = 1e6 if any(total_sample(comps, b["key"]).mean() >= 1e6 for b in bases) else 1
    unit_lbl = "milhões" if scale == 1e6 else "unidades"
    for j, b in enumerate(bases):
        tot = total_sample(comps, b["key"])
        if not tot.size:
            continue
        col = PALETTE[j % len(PALETTE)]
        mean, p5, p95 = tot.mean(), np.percentile(tot, 5), np.percentile(tot, 95)
        ax.hist(tot / scale, bins=70, density=True, color=col, alpha=0.5, label=f"{b['label']} (E={fmt(mean)})")
        ax.axvline(mean / scale, color=col, lw=1.6); ax.axvspan(p5 / scale, p95 / scale, color=col, alpha=0.10)
        out.append(f"| {b['label']} | {fmt(mean)} | {fmt(p5)} | {fmt(p95)} |")
    ax.set_title(title + " — total, banda de 90%", fontsize=13, fontweight="bold", color="#2C3E50")
    ax.set_xlabel(f"valor total ({unit_lbl})"); ax.set_ylabel("densidade"); ax.legend(fontsize=9, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "dist_total.png", dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("  ✓ dist_total.png")

    (BASE / ARGS.stats).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  ✓ {ARGS.stats}")


if __name__ == "__main__":
    main()
