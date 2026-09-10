"""Audit any variant score for double counting, using the Atlas SHAP release.

The AlphaGenome Atlas variant-impact score is a linear ensemble, and two of its
features - AlphaMissense and multi-species conservation - are themselves
predictors this dossier cites separately. Quoting both as if they were
independent lines of evidence inflates a case without adding information to it.

The SHAP release makes the overlap measurable. For each variant this prints how
much of the score comes from AlphaGenome's own sequence-to-function tracks and
how much is a borrowed annotation re-entering under a new name.

Reads "chrom pos ref alt [label]" per line from a file or stdin.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mva import atlas  # noqa: E402

VERDICT = [
    (0.50, "DOUBLE COUNTING - do not cite alongside AlphaMissense"),
    (0.25, "partly derivative - cite with the overlap stated"),
    (0.00, "independent of AlphaMissense"),
]


def verdict(am: float) -> str:
    for threshold, text in VERDICT:
        if am >= threshold:
            return text
    return VERDICT[-1][1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variants", default="-")
    ap.add_argument("--out")
    args = ap.parse_args()
    src = sys.stdin if args.variants == "-" else open(args.variants)

    rows = []
    for line in src:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        chrom, pos, ref, alt = parts[:4]
        label = " ".join(parts[4:])
        pos = int(pos)
        phred = next((f[5] for f in atlas.region("avi", chrom, pos, pos)
                      if f[2] == ref and f[3] == alt), None)
        shap = next((f for f in atlas.region("shap", chrom, pos, pos)
                     if f[2] == ref and f[3] == alt), None)
        if phred is None or shap is None:
            print(f"{chrom}:{pos} {ref}>{alt}  not in the Atlas (indel, or off-target contig)")
            continue
        d = atlas.shap_decompose(shap)
        am, ag = atlas.am_share(d), atlas.ag_share(d)
        cons = sum(abs(d[f]) for f in ("CACTUS_241_WAY", "PHASTCONS_470_WAY"))
        total = sum(abs(v) for v in d.values())
        term = abs(d["PROTEIN_TERMINATION"]) / total if total else 0
        top = sorted(d.items(), key=lambda kv: -abs(kv[1]))[:3]
        rows.append(dict(chrom=chrom, pos=pos, ref=ref, alt=alt, label=label,
                         avi_phred=float(phred), am_share=am, ag_share=ag,
                         conservation_share=cons / total if total else 0,
                         termination_share=term, verdict=verdict(am),
                         top_features=", ".join(f"{k}={v:.3f}" for k, v in top)))
        print(f"\n{chrom}:{pos} {ref}>{alt}  {label}")
        print(f"  AVI PHRED {float(phred):6.2f}")
        print(f"  AlphaMissense {am:5.0%}   conservation {cons / total:5.0%}   "
              f"termination {term:5.0%}   AlphaGenome's own tracks {ag:5.0%}")
        print(f"  top features: {rows[-1]['top_features']}")
        print(f"  -> {rows[-1]['verdict']}")

    if args.out and rows:
        cols = list(rows[0])
        with open(args.out, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in rows:
                fh.write("\t".join(
                    f"{r[c]:.4f}" if isinstance(r[c], float) else str(r[c])
                    for c in cols) + "\n")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
