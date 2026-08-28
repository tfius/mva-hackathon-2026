"""Turn TxGNN's raw logits into a ranked, degree-controlled candidate table.

Two things this does that a bare ranked list does not.

**The right candidate universe.** TxGNN scores all 7,957 DrugBank nodes in
PrimeKG, but most of those are PDB ligands and experimental compounds with a
degree of 2 - and on a disease with no drug edges the model scores exactly those
highest, because it has learned almost nothing about them. Ranking on the raw
7,957 nominates "Casimiroin" and a string of crystallographic fragments for a
child with MVA. TxGNN's own `Ranked List` is restricted to the 1,801 drugs that
carry indication or contraindication edges somewhere in PrimeKG, and that is the
set a therapeutic recommendation can honestly be drawn from. This script ranks
within it.

**Degree control.** Knowledge-graph link predictors are not neutral about how
well connected a node is. Scores are regressed on log drug degree and the
residual carried alongside, so a candidate that ranks well on the residual is
one the graph likes *for this disease specifically* rather than one whose
position is explained by its connectivity.

**Named prior probes.** The three mechanistic hypotheses in the Track 2 report
were written before this model was run. Their drugs are looked up by name here,
so the comparison is a genuine prediction check rather than a story fitted
afterwards.
"""
from __future__ import annotations

import argparse
import csv
import math
import pickle
from collections import Counter
from pathlib import Path

# Hypotheses fixed in reports/track2-mechanism-and-repurposing.md before this ran.
PRIOR_PROBES = {
    "H1 NAD+/SIRT2 -> stabilise BubR1": [
        "Nicotinamide", "Nicotinamide riboside", "Nicotinamide mononucleotide",
        "NADH", "Niacin", "Nicotinic acid",
    ],
    "H2 senolytic": ["Dasatinib", "Quercetin", "Navitoclax", "Fisetin"],
    "H3 aneuploidy-selective stress": [
        "Metformin", "Tanespimycin", "Chloroquine", "Hydroxychloroquine",
        "Acadesine", "Geldanamycin",
    ],
    "contraindicated: weakens the checkpoint further": [
        "Paclitaxel", "Docetaxel", "Vincristine", "Vinblastine", "Eribulin",
        "Volasertib", "Alisertib", "Barasertib",
    ],
}


def drug_degree(kg_csv: str) -> Counter:
    deg: Counter = Counter()
    with open(kg_csv, newline="") as fh:
        for row in csv.DictReader(fh):
            if row["x_type"] == "drug":
                deg[row["x_id"]] += 1
            if row["y_type"] == "drug":
                deg[row["y_id"]] += 1
    return deg


def linfit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx if sxx else 0.0
    return slope, my - slope * mx


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="/mnt/data/mva-hackathon-2026/work/txgnn")
    ap.add_argument("--ckpt", default="/mnt/data/mva-hackathon-2026/txgnn-ckpt/TxGNNExplorer")
    ap.add_argument("--kg", default="/mnt/data/mva-hackathon-2026/txgnn-data/kg.csv")
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/txgnn")
    args = ap.parse_args()

    id2name = pickle.load(open(Path(args.ckpt) / "name_mapping.pkl", "rb"))["id2name_drug"]
    print("computing drug degrees from PrimeKG ...", flush=True)
    deg = drug_degree(args.kg)

    for rel in ("indication", "contraindication"):
        raw = pickle.load(open(Path(args.raw) / f"raw_{rel}.pkl", "rb"))
        pred = next(iter(raw["prediction"].values()))
        labels = next(iter(raw["label"].values()))
        assert not any(labels.values()), "disease has known edges; this is not zero-shot"

        # TxGNN's own Ranked List is the clinically annotated drug subset; the
        # full prediction dict is dominated by PDB ligands that mean nothing as
        # therapeutic candidates. See the module docstring.
        universe = set(next(iter(raw["result"]["Ranked List"].values())))
        ids = [i for i in pred if id2name.get(i, i) in universe]
        scores = [float(pred[i]) for i in ids]
        logdeg = [math.log10(deg.get(i, 0) + 1) for i in ids]

        slope, intercept = linfit(logdeg, scores)
        rho = spearman(logdeg, scores)
        resid = [s - (slope * d + intercept) for s, d in zip(scores, logdeg)]

        rows = sorted(
            (
                {
                    "drug_id": i,
                    "name": id2name.get(i, i),
                    "score": s,
                    "prob": 1 / (1 + math.exp(-s)),
                    "degree": deg.get(i, 0),
                    "residual": r,
                }
                for i, s, r in zip(ids, scores, resid)
            ),
            key=lambda d: -d["score"],
        )
        for n, r in enumerate(rows, 1):
            r["rank"] = n
        by_resid = sorted(rows, key=lambda d: -d["residual"])
        for n, r in enumerate(by_resid, 1):
            r["rank_residual"] = n

        out = Path(args.out) / f"ranked_{rel}.tsv"
        cols = ["rank", "rank_residual", "drug_id", "name", "score", "prob", "degree", "residual"]
        with out.open("w") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in rows:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")

        print(f"\n===== {rel}  ({len(rows)} clinically annotated drugs of "
              f"{len(pred)} scored; all labels 0 -> zero-shot)")
        print(f"score vs log10(degree): Spearman rho = {rho:+.3f}, slope = {slope:+.3f}")
        print("  top 15 by raw score:")
        for r in rows[:15]:
            print(f"    {r['rank']:4d}  {r['name']:32.32s} score {r['score']:+7.3f}  deg {r['degree']:5d}")
        print("  top 15 by degree-corrected residual:")
        for r in by_resid[:15]:
            print(f"    {r['rank_residual']:4d}  {r['name']:32.32s} resid {r['residual']:+7.3f}  "
                  f"raw rank {r['rank']:4d}  deg {r['degree']:5d}")

        idx = {r["name"].lower(): r for r in rows}
        print("  named prior probes:")
        for label, names in PRIOR_PROBES.items():
            hits = [(n, idx[n.lower()]) for n in names if n.lower() in idx]
            missing = [n for n in names if n.lower() not in idx]
            print(f"    {label}")
            for n, r in sorted(hits, key=lambda x: x[1]["rank"]):
                pct = 100 * r["rank"] / len(rows)
                print(f"       {n:28.28s} rank {r['rank']:5d} ({pct:5.1f}%)  "
                      f"resid rank {r['rank_residual']:5d}  deg {r['degree']:5d}")
            if missing:
                print(f"       not in PrimeKG drug set: {', '.join(missing)}")


if __name__ == "__main__":
    main()
