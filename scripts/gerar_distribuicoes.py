#!/usr/bin/env python3
"""Distribuições de probabilidade de valor + Monte Carlo do total (estudo V3).

Lê dados_distribuicao.json (amostras de preço brutas por modelo, FASE 3b),
constrói a distribuição de mistura de valor por item e a distribuição do valor
TOTAL recuperado por Monte Carlo, gera os gráficos (paper/figuras/*.png) e
escreve dist_stats.md (E, desvio, banda 90% por item e total).

Modelo: V_i^b ~ sum_m w_{i,m} F_hat_{i,m}^b  (escolhe modelo por peso, sorteia preço da amostra).
        V^b = sum_i sum_{k=1..N_i} V_{i,k}^b.

Uso: /home/otavio/Documents/vscode/.venv/bin/python scripts/gerar_distribuicoes.py
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#888888",
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

SEED = 20260616
RNG = np.random.default_rng(SEED)
N_ITER = 50_000

_ap = argparse.ArgumentParser()
_ap.add_argument("--exclude", nargs="*", default=[], help="chaves de item a excluir (ex.: moto)")
_ap.add_argument("--figdir", default="figuras", help="subpasta de figuras em paper/")
_ap.add_argument("--stats", default="dist_stats.md", help="arquivo de stats")
_ARGS = _ap.parse_args()

CASE = Path(__file__).resolve().parent.parent
FIG = CASE / "paper" / _ARGS.figdir
FIG.mkdir(parents=True, exist_ok=True)
DATA = CASE / "dados_distribuicao.json"
STATS = CASE / _ARGS.stats

# N_i (slide SEGUR) por chave normalizada de item
N_BY = {"celular": 118, "moto": 113, "bicicleta": 19, "bike": 19, "cordao": 15, "cordão": 15}
LABEL = {"celular": "Celulares", "moto": "Motocicletas", "bicicleta": "Bicicletas",
         "bike": "Bicicletas", "cordao": "Cordões", "cordão": "Cordões"}
COL_REV, COL_REP = "#2C6E9B", "#C9772E"  # revenda (azul), reposição (laranja)


def norm(s):
    return s.strip().lower().replace("ç", "c").replace("ã", "a")


def model_prices(m, base):
    """Array de preços de um modelo na base ('used'/'new'); fallback se vazio."""
    used = np.array(m.get("prices_used") or [], dtype=float)
    new = np.array(m.get("prices_new") or [], dtype=float)
    arr = used if base == "used" else new
    arr = arr[arr > 0]
    if arr.size == 0:  # fallback para a outra base se faltar
        other = new if base == "used" else used
        other = other[other > 0]
        arr = other if other.size else np.array([np.nan])
    return arr


def unit_sample(models, base, size):
    """Amostra de valor de UMA unidade (mistura: peso -> modelo -> preço da amostra)."""
    w = np.array([m["weight"] for m in models], dtype=float)
    w = w / w.sum()
    pools = [model_prices(m, base) for m in models]
    idx = RNG.choice(len(models), size=size, p=w)
    out = np.empty(size, dtype=float)
    for j in range(len(models)):
        sel = idx == j
        k = int(sel.sum())
        if k:
            out[sel] = RNG.choice(pools[j], size=k, replace=True)
    return out


def total_sample(item_models, base, n_iter=N_ITER):
    """Distribuição do valor TOTAL: soma de N_i unidades por item, por iteração."""
    total = np.zeros(n_iter, dtype=float)
    for key, models in item_models.items():
        n = N_BY[norm(key)]
        draws = unit_sample(models, base, n * n_iter).reshape(n_iter, n)
        total += draws.sum(axis=1)
    return total


def fmt(v):
    if abs(v) >= 1e6:
        return f"R$ {v/1e6:.2f} mi".replace(".", ",")
    return ("R$ " + f"{v:,.0f}").replace(",", ".")


def main():
    if not DATA.exists():
        sys.exit(f"ERRO: {DATA} nao encontrado (rode a FASE 3b primeiro).")
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    items = raw["result"] if isinstance(raw, dict) and "result" in raw else raw
    item_models = {}
    for entry in items:
        res = entry.get("research", entry)
        if not res or "models" not in res:
            continue
        item_models[res["item"] if "item" in res else entry.get("item")] = res["models"]

    # chaves normalizadas -> usar o label do item bruto
    norm_models = {}
    for k, v in item_models.items():
        nk = norm(k.split()[0]) if k else k
        for cand in ("celular", "moto", "bicicleta", "bike", "cordao", "cordão"):
            if cand in norm(k):
                nk = cand
                break
        norm_models[nk] = v

    excl = {norm(x) for x in _ARGS.exclude}
    if excl:
        norm_models = {k: v for k, v in norm_models.items() if norm(k) not in excl}
        print(f"  [excluídos: {', '.join(sorted(excl))}]")

    stats_lines = ["# dist_stats.md — distribuições de valor (Monte Carlo, seed %d)\n" % SEED]

    # ---- Figura 1: distribuição de valor por item (2x2) ----
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), facecolor="white")
    order = [k for k in ("celular", "moto", "bicicleta", "cordao", "cordão", "bike") if k in norm_models]
    seen = set()
    panel = 0
    stats_lines.append("## Por item (valor de UMA unidade)\n")
    stats_lines.append("| Item | base | E[V_i] | desvio | p5 | p95 |")
    stats_lines.append("|---|---|--:|--:|--:|--:|")
    for key in order:
        lab = LABEL[norm(key)]
        if lab in seen:
            continue
        seen.add(lab)
        models = norm_models[key]
        ax = axes.flat[panel]; panel += 1
        # cordão tem cauda muito pesada: escala log no eixo x mostra o corpo
        # (folheado, R$15-250) E a cauda (ouro, ate R$5 mil) na mesma figura.
        is_cord = norm(key) in ("cordao", "cordão")
        for base, col, name in (("used", COL_REV, "revenda"), ("new", COL_REP, "reposição")):
            s = unit_sample(models, base, 200_000)
            s = s[np.isfinite(s)]
            hi = np.percentile(s, 99.5)
            if is_cord:
                lo = max(float(s.min()), 1.0)
                bins = np.logspace(np.log10(lo), np.log10(hi), 40)
                ax.hist(s, bins=bins, density=True, color=col, alpha=0.30)
                try:  # KDE em log10(x) com Jacobiano -> densidade correta em x
                    L = np.log10(s[s > 0])
                    kde = gaussian_kde(RNG.choice(L, size=min(L.size, 20_000), replace=False))
                    xs = np.logspace(np.log10(lo), np.log10(hi), 400)
                    ax.plot(xs, kde(np.log10(xs)) / (xs * np.log(10.0)), color=col, lw=1.9, label=name)
                except Exception:
                    ax.plot([], [], color=col, lw=1.9, label=name)
            else:
                ax.hist(s, bins=45, range=(s.min(), hi), density=True, color=col, alpha=0.30)
                try:  # curva KDE suave (cara de distribuição de probabilidade)
                    kde = gaussian_kde(RNG.choice(s, size=min(s.size, 20_000), replace=False))
                    xs = np.linspace(s.min(), hi, 400)
                    ax.plot(xs, kde(xs), color=col, lw=1.9, label=name)
                except Exception:
                    ax.plot([], [], color=col, lw=1.9, label=name)
            stats_lines.append(f"| {lab} | {name} | {fmt(s.mean())} | {fmt(s.std())} | {fmt(np.percentile(s,5))} | {fmt(np.percentile(s,95))} |")
        ax.set_title(lab, fontsize=12, fontweight="bold", color="#2C3E50")
        ax.set_xlabel("valor de uma unidade (R$)" + (" — escala log" if is_cord else ""), fontsize=9)
        ax.set_ylabel("densidade", fontsize=9)
        ax.legend(fontsize=8, frameon=False)
        if is_cord:
            ax.set_xscale("log")
            ax.set_xticks([20, 50, 100, 250, 500, 1000, 2500, 5000])
            ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
            ax.minorticks_off()
        else:
            ax.ticklabel_format(style="plain", axis="x")
    for k in range(panel, 4):
        axes.flat[k].axis("off")
    fig.suptitle("Distribuição de probabilidade do valor por item recuperado",
                 fontsize=14, fontweight="bold", color="#2C3E50")
    fig.text(0.5, 0.01, "Fonte: amostras de preço de mercado por modelo (usado/novo). Elaboração própria.",
             ha="center", fontsize=8, color="#888", style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.96])
    fig.savefig(FIG / "dist_itens.png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ✓ dist_itens.png")

    # ---- Figura 2: distribuição do valor TOTAL (Monte Carlo) com banda 90% ----
    fig, ax = plt.subplots(figsize=(11, 6), facecolor="white")
    stats_lines.append("\n## Valor TOTAL recuperado (Monte Carlo, %d iter)\n" % N_ITER)
    stats_lines.append("| base | E[V] | p5 | p95 |")
    stats_lines.append("|---|--:|--:|--:|")
    for base, col, name in (("used", COL_REV, "revenda"), ("new", COL_REP, "reposição")):
        tot = total_sample(norm_models, base)
        mean, p5, p95 = tot.mean(), np.percentile(tot, 5), np.percentile(tot, 95)
        ax.hist(tot / 1e6, bins=70, density=True, color=col, alpha=0.5, label=f"{name} (E={fmt(mean)})")
        ax.axvline(mean / 1e6, color=col, lw=1.6)
        ax.axvspan(p5 / 1e6, p95 / 1e6, color=col, alpha=0.10)
        stats_lines.append(f"| {name} | {fmt(mean)} | {fmt(p5)} | {fmt(p95)} |")
    ax.set_title("Distribuição do valor total recuperado — banda de 90% (Monte Carlo)",
                 fontsize=13, fontweight="bold", color="#2C3E50")
    ax.set_xlabel("valor total (R$ milhões)", fontsize=10)
    ax.set_ylabel("densidade", fontsize=10)
    ax.legend(fontsize=9, frameon=False)
    fig.text(0.5, 0.005, "Soma de N_i unidades por item; %d iterações; seed %d. Elaboração própria." % (N_ITER, SEED),
             ha="center", fontsize=8, color="#888", style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(FIG / "dist_total.png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ✓ dist_total.png")

    STATS.write_text("\n".join(stats_lines) + "\n", encoding="utf-8")
    print(f"  ✓ {STATS.name}")


if __name__ == "__main__":
    main()
