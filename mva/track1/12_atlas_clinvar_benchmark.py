"""Does the AlphaGenome Atlas separate ClinVar's calls in the MVA genes?

A predictor is only worth citing on a novel variant if it agrees with the
answer where the answer is known. This scores every ClinVar SNV in the MVA and
spindle-checkpoint genes and asks whether Pathogenic/Likely pathogenic records
score above Benign/Likely benign ones - in these genes, not genome-wide, since
that is where the claim about allele B is being made.

Reports AUC with a Mann-Whitney U p-value, and the same for AlphaMissense's own
SHAP contribution, so the Atlas's added value over AlphaMissense is visible.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mva import atlas  # noqa: E402

BCFTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/bcftools"
CLINVAR = "/mnt/data/mva-hackathon-2026/refs/clinvar.vcf.gz"

GENES = {
    "BUB1B": ("chr15", 40160984, 40221137),
    "CEP57": ("chr11", 95789965, 95837070),
    "TRIP13": ("chr5", 892849, 919357),
    "CENPE": ("chr4", 103105349, 103198463),
    "BUB1": ("chr2", 110635468, 110678098),
    "BUB3": ("chr10", 123154365, 123313144),
}

PATHOGENIC = {"Pathogenic", "Likely_pathogenic", "Pathogenic/Likely_pathogenic"}
BENIGN = {"Benign", "Likely_benign", "Benign/Likely_benign"}


def clinvar_snvs():
    """(gene, chrom, pos, ref, alt, clnsig, revstat, molecular consequence)."""
    for gene, (chrom, start, end) in GENES.items():
        reg = f"{chrom[3:]}:{start}-{end}"
        fmt = "%CHROM\t%POS\t%REF\t%ALT\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\t%INFO/MC\n"
        out = subprocess.run([BCFTOOLS, "query", "-r", reg, "-f", fmt, CLINVAR],
                             capture_output=True, text=True, check=True).stdout
        for line in out.splitlines():
            f = line.split("\t")
            if len(f[2]) != 1 or len(f[3]) != 1 or f[3] == ".":
                continue  # SNVs only: the Atlas has nothing else
            yield (gene, "chr" + f[0], int(f[1]), f[2], f[3], f[4], f[5], f[6])


def auc(pos: list[float], neg: list[float]) -> tuple[float, float]:
    """AUC by rank-sum, plus a normal-approximation two-sided p-value."""
    import math
    if not pos or not neg:
        return float("nan"), float("nan")
    merged = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg])
    ranks, i = {}, 0
    while i < len(merged):
        j = i
        while j + 1 < len(merged) and merged[j + 1][0] == merged[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    rank_pos = sum(ranks[k] for k, (_, lab) in enumerate(merged) if lab == 1)
    n1, n2 = len(pos), len(neg)
    u = rank_pos - n1 * (n1 + 1) / 2
    a = u / (n1 * n2)
    mu, sd = n1 * n2 / 2, math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    z = (u - mu) / sd if sd else 0.0
    p = math.erfc(abs(z) / math.sqrt(2))
    return a, p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workdir", required=True)
    args = ap.parse_args()
    os.makedirs(args.workdir, exist_ok=True)

    records = list(clinvar_snvs())
    print(f"{len(records)} ClinVar SNVs across {len(GENES)} genes", file=sys.stderr)

    bed = atlas.write_sites_bed([(r[1], r[2]) for r in records],
                                os.path.join(args.workdir, "clinvar_sites.bed"))
    ann: dict[tuple, dict] = {}
    for kind in ("avi", "splicing", "shap"):
        n = 0
        for f in atlas.regions_from_bed(kind, bed):
            key = (f[0], int(f[1]), f[2], f[3])
            if kind == "avi":
                ann.setdefault(key, {}).update(avi_raw=float(f[4]), avi_phred=float(f[5]))
            elif kind == "splicing":
                ann.setdefault(key, {}).update(splicing=float(f[4]))
            else:
                d = atlas.shap_decompose(f)
                ann.setdefault(key, {}).update(
                    shap=d, am_share=atlas.am_share(d), ag_share=atlas.ag_share(d))
            n += 1
        print(f"  {kind}: {n} rows", file=sys.stderr)

    rows, groups = [], {"P/LP": [], "B/LB": [], "VUS": [], "other": []}
    for gene, chrom, pos, ref, alt, sig, rev, mc in records:
        a = ann.get((chrom, pos, ref, alt))
        if not a or "avi_phred" not in a:
            continue
        label = ("P/LP" if sig in PATHOGENIC else
                 "B/LB" if sig in BENIGN else
                 "VUS" if sig == "Uncertain_significance" else "other")
        shap = a.get("shap", {})
        rows.append(dict(
            gene=gene, chrom=chrom, pos=pos, ref=ref, alt=alt, clnsig=sig,
            revstat=rev, mc=(mc or "").split("|")[-1], label=label,
            avi_raw=a["avi_raw"], avi_phred=a["avi_phred"],
            splicing=a.get("splicing", ""),
            am_contrib=shap.get("ALPHAMISSENSE", ""),
            splice_contrib=shap.get("MERGED_SPLICING", ""),
            am_share=round(a.get("am_share", float("nan")), 4),
            ag_share=round(a.get("ag_share", float("nan")), 4)))
        groups[label].append(rows[-1])

    cols = list(rows[0])
    with open(args.out, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")

    print(f"\nscored {len(rows)} ClinVar SNVs "
          f"({ {k: len(v) for k, v in groups.items()} })", file=sys.stderr)
    plp, blb = groups["P/LP"], groups["B/LB"]
    for name, key in (("AVI PHRED", "avi_phred"),
                      ("AlphaMissense SHAP contribution", "am_contrib"),
                      ("AlphaGenome splicing", "splicing")):
        p = [float(r[key]) for r in plp if r[key] != ""]
        b = [float(r[key]) for r in blb if r[key] != ""]
        a, pv = auc(p, b)
        print(f"{name:34s} AUC={a:.3f}  p={pv:.2e}  (n={len(p)} P/LP vs {len(b)} B/LB)",
              file=sys.stderr)
    print("wrote", args.out, file=sys.stderr)


if __name__ == "__main__":
    main()
