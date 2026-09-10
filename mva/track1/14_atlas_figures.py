"""Two figures from the AlphaGenome Atlas passes over BUB1B.

fig1  Where the two proband alleles fall against every ClinVar SNV in BUB1B.
      The point is the gap: benign and pathogenic separate completely on the
      Atlas variant-impact score, and allele B lands inside the gap, which is
      what a hypomorph - and a VUS - should do.

fig2  The gene's whole mutational surface: the highest score reachable at each
      of its 60,154 positions. It answers "where would a missing second allele
      have to be", which is the live question when only one BUB1B hit is found.

Only the two alleles already disclosed in the report are marked; no other
proband genotype appears in either figure.
"""
from __future__ import annotations

import argparse
import csv
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#a8a7a1"
GRID = "#e4e3df"
BLUE = "#2a78d6"     # categorical slot 1 / diverging cool pole
ORANGE = "#eb6834"   # categorical slot 2
RED = "#e34948"      # diverging warm pole
GRAYMID = "#8a8984"  # diverging neutral midpoint

ALLELE_A = ("Allele A  p.Leu737Ter", 40209701, 33.76585, 0.08699)
ALLELE_B = ("Allele B  p.Asn1002Lys", 40220612, 25.60629, 0.04813)
ATLAS_P999 = 2.47  # Atlas genome-wide 99.9th percentile of the splicing score


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
        ax.spines[s].set_linewidth(1.0)
    ax.tick_params(colors=INK2, labelsize=9, length=3, width=1.0)
    ax.grid(True, color=GRID, linewidth=0.8, alpha=0.9)
    ax.set_axisbelow(True)


def fig_calibration(clinvar_tsv: str, out: str) -> None:
    rows = [r for r in csv.DictReader(open(clinvar_tsv), delimiter="\t")
            if r["gene"] == "BUB1B" and r["avi_phred"] not in ("", "nan")]
    groups = {
        "Benign / Likely benign": ([float(r["avi_phred"]) for r in rows if r["label"] == "B/LB"], BLUE),
        "Uncertain significance": ([float(r["avi_phred"]) for r in rows if r["label"] == "VUS"], GRAYMID),
        "Pathogenic / Likely path.": ([float(r["avi_phred"]) for r in rows if r["label"] == "P/LP"], RED),
    }
    gap_lo = max(groups["Benign / Likely benign"][0])
    gap_hi = min(groups["Pathogenic / Likely path."][0])

    fig, ax = plt.subplots(figsize=(9.2, 4.5), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    style(ax)
    rnd = random.Random(0)

    top, bot = 2.34, -0.78
    ax.add_patch(Rectangle((gap_lo, bot), gap_hi - gap_lo, top - bot,
                           facecolor="#eceae5", edgecolor="none", zorder=0))
    mid = (gap_lo + gap_hi) / 2
    ax.plot([mid, mid], [top, top + 0.30], color=MUTED, linewidth=1.0, zorder=1)
    ax.text(mid, top + 0.40, f"no classified variant in this {gap_hi - gap_lo:.1f}-point band",
            ha="center", va="bottom", fontsize=9, color=INK2)

    for i, (name, (vals, color)) in enumerate(groups.items()):
        y = 2 - i
        ax.scatter(vals, [y + rnd.uniform(-0.17, 0.17) for _ in vals], s=9,
                   color=color, alpha=0.5, linewidths=0, zorder=2, rasterized=True)
        ax.text(-1.4, y + 0.10, name, ha="right", va="center", fontsize=9.5, color=INK)
        ax.text(-1.4, y - 0.20, f"n = {len(vals):,}", ha="right", va="center",
                fontsize=8.5, color=MUTED)

    for (label, _pos, phred, _spl), side in ((ALLELE_B, -1), (ALLELE_A, 1)):
        name, prot = label.split("  ")
        ax.plot([phred, phred], [bot, top], color=INK, linewidth=1.6,
                linestyle=(0, (4, 2)), zorder=3)
        ax.scatter([phred], [bot], s=64, facecolor=SURFACE, edgecolor=INK,
                   linewidths=1.8, zorder=4)
        ax.text(phred + side * 0.7, bot - 0.30, f"{name}\n{prot}\nAVI {phred:.1f}",
                ha="left" if side > 0 else "right", va="top", fontsize=9,
                color=INK, linespacing=1.45)

    ax.set_xlim(-1.7, 57)
    ax.set_ylim(-2.15, 3.30)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("AlphaGenome Atlas variant-impact score (PHRED)", fontsize=9.5, color=INK2)
    ax.set_title("Every ClinVar SNV in $\\it{BUB1B}$, scored by the AlphaGenome Atlas",
                 fontsize=12.5, color=INK, loc="left", pad=26)
    ax.text(0, 1.048, "Benign and pathogenic separate completely. Allele B falls in the gap between them.",
            transform=ax.transAxes, fontsize=9.5, color=INK2)
    fig.subplots_adjust(left=0.215, right=0.98, top=0.815, bottom=0.155)
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)
    print("wrote", out, f"(gap {gap_lo:.2f}-{gap_hi:.2f})")


def fig_saturation(map_tsv: str, exons_tsv: str, out: str) -> None:
    rows = list(csv.DictReader(open(map_tsv), delimiter="\t"))
    pos = [int(r["pos"]) for r in rows]
    spl = [float(r["max_splicing"]) for r in rows]
    avi = [float(r["max_avi_phred"]) for r in rows]
    cls = [r["class"] for r in rows]
    exons = []
    for line in open(exons_tsv):
        if line.startswith(("#", "exon_index")):
            continue
        idx, s, e, _ = line.split("\t")
        exons.append((int(idx), int(s), int(e)))

    canon = [i for i, c in enumerate(cls) if c == "splice_canonical"]
    hot = [i for i, c in enumerate(cls) if c == "intron" and spl[i] >= ATLAS_P999]
    rest = [i for i in range(len(rows)) if i not in set(canon) | set(hot)]

    fig, axes = plt.subplots(3, 1, figsize=(9.6, 6.4), dpi=200,
                             gridspec_kw=dict(height_ratios=[0.30, 1.0, 0.72], hspace=0.16),
                             sharex=True)
    fig.patch.set_facecolor(SURFACE)
    axg, axs, axa = axes

    axg.set_facecolor(SURFACE)
    for s in axg.spines.values():
        s.set_visible(False)
    axg.set_yticks([])
    axg.tick_params(labelbottom=False, length=0)
    axg.plot([min(pos), max(pos)], [0, 0], color=MUTED, linewidth=1.2, zorder=1)
    for idx, s, e in exons:
        axg.add_patch(Rectangle((s, -0.42), max(e - s, 60), 0.84, facecolor=INK2,
                                edgecolor="none", zorder=2))
    axg.set_ylim(-1.1, 1.1)
    axg.text(min(pos), 0.88, "$\\it{BUB1B}$  23 exons, 60,154 positions, transcribed left to right",
             fontsize=9, color=INK2, va="bottom")

    for ax, vals, lab in ((axs, spl, "AlphaGenome splicing score"),
                          (axa, avi, "Variant-impact score (PHRED)")):
        style(ax)
        ax.scatter([pos[i] for i in rest], [vals[i] for i in rest], s=1.6,
                   color=MUTED, alpha=0.35, linewidths=0, rasterized=True, zorder=2)
        ax.set_ylabel(lab, fontsize=9.5, color=INK2)

    axs.scatter([pos[i] for i in canon], [spl[i] for i in canon], s=13, color=BLUE,
                alpha=0.85, linewidths=0, zorder=3, label=f"canonical splice site ({len(canon)} bp)")
    axs.scatter([pos[i] for i in hot], [spl[i] for i in hot], s=26, color=ORANGE,
                linewidths=0, zorder=4, label=f"deep-intronic hotspot ({len(hot)} bp)")
    axs.axhline(ATLAS_P999, color=INK2, linewidth=1.2, linestyle=(0, (4, 2)), zorder=3)
    axs.text(min(pos) + 300, ATLAS_P999 - 0.14, "Atlas genome-wide 99.9th percentile",
             fontsize=8.5, color=INK2, ha="left", va="top")
    leg = axs.legend(loc="upper left", frameon=False, fontsize=9, handletextpad=0.5,
                     borderpad=0.2, labelspacing=0.35)
    for t in leg.get_texts():
        t.set_color(INK2)
    axs.set_ylim(-0.25, 4.3)

    axa.scatter([pos[i] for i in canon], [avi[i] for i in canon], s=13, color=BLUE,
                alpha=0.85, linewidths=0, zorder=3)
    axa.scatter([pos[i] for i in hot], [avi[i] for i in hot], s=26, color=ORANGE,
                linewidths=0, zorder=4)
    axa.set_xlabel("chr15 position (GRCh38)", fontsize=9.5, color=INK2)
    axa.ticklabel_format(axis="x", style="plain", useOffset=False)
    axa.set_xlim(min(pos) - 700, max(pos) + 700)

    # Allele B sits 500 bp from the right edge, so its label hangs to the left.
    for (label, p, phred, splv), dx, ha in ((ALLELE_A, 0, "center"), (ALLELE_B, -600, "right")):
        short = label.split("  ")[0]
        for ax, v, dy in ((axs, splv, 1.50), (axa, phred, 8.5)):
            ax.annotate(short, xy=(p, v), xytext=(p + dx, v + dy), fontsize=8.5, color=INK,
                        ha=ha, va="bottom", zorder=6,
                        arrowprops=dict(arrowstyle="-", color=INK, linewidth=1.2,
                                        shrinkA=1, shrinkB=3))
            ax.scatter([p], [v], s=56, facecolor=SURFACE, edgecolor=INK,
                       linewidths=1.8, zorder=5)

    axg.set_title("The whole mutational surface of $\\it{BUB1B}$: every possible single-letter change",
                  fontsize=12, color=INK, loc="left", pad=16)
    fig.subplots_adjust(left=0.095, right=0.985, top=0.895, bottom=0.095)
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)
    print("wrote", out, f"({len(hot)} deep-intronic hotspots)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", default="/mnt/data/mva-hackathon-2026/work/alphagenome")
    ap.add_argument("--outdir", default="reports/figures")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    fig_calibration(os.path.join(args.workdir, "clinvar_mva_atlas.tsv"),
                    os.path.join(args.outdir, "bub1b-atlas-calibration.png"))
    fig_saturation(os.path.join(args.workdir, "bub1b_saturation_map.tsv"),
                   "/mnt/data/mva-hackathon-2026/work/BUB1B_exons.tsv",
                   os.path.join(args.outdir, "bub1b-saturation-map.png"))


if __name__ == "__main__":
    main()
