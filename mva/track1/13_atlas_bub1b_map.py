"""Saturation map of BUB1B: every possible SNV in the gene, scored.

The Atlas has a score for all three alternates at all 60,153 positions of the
gene, so the whole mutational surface can be read without running a model.
This asks where in BUB1B a new variant would have to fall to matter - which is
the practical question when a patient has one BUB1B hit and the second allele
has not been found, the situation MVA1 presents with.

Emits a per-position table (max over the three alternates) plus a per-region
summary, and marks the two proband alleles and the ClinVar P/LP set.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mva import atlas  # noqa: E402

GENE = ("chr15", 40160984, 40221137)
EXONS = "/mnt/data/mva-hackathon-2026/work/BUB1B_exons.tsv"
SPLICE_WINDOW = 20
ALLELES = {40209701: "A p.Leu737Ter", 40220612: "B p.Asn1002Lys"}


def load_exons(path: str) -> list[tuple[int, int, int]]:
    out = []
    for line in open(path):
        if line.startswith(("#", "exon_index")):
            continue
        idx, s, e, _ = line.split("\t")
        out.append((int(idx), int(s), int(e)))
    return sorted(out, key=lambda x: x[1])


def classify(pos: int, exons) -> tuple[str, str]:
    """(fine label, coarse class)."""
    for idx, s, e in exons:
        if s <= pos <= e:
            return f"exon{idx}", "exon"
    for idx, s, e in exons:
        if s - SPLICE_WINDOW <= pos < s:
            return f"acceptor_exon{idx}(-{s - pos})", (
                "splice_canonical" if s - pos <= 2 else "splice_region")
        if e < pos <= e + SPLICE_WINDOW:
            return f"donor_exon{idx}(+{pos - e})", (
                "splice_canonical" if pos - e <= 2 else "splice_region")
    return "intron", "intron"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--summary", required=True)
    args = ap.parse_args()

    exons = load_exons(EXONS)
    chrom, start, end = GENE

    per_alt: dict[tuple[int, str, str], dict] = {}
    for kind, cols in (("avi", ("avi_raw", "avi_phred")), ("splicing", ("splicing",))):
        for f in atlas.region(kind, chrom, start, end):
            key = (int(f[1]), f[2], f[3])
            rec = per_alt.setdefault(key, {})
            for i, c in enumerate(cols):
                rec[c] = float(f[4 + i])
    for f in atlas.region("shap", chrom, start, end):
        d = atlas.shap_decompose(f)
        rec = per_alt.setdefault((int(f[1]), f[2], f[3]), {})
        rec["shap_termination"] = d["PROTEIN_TERMINATION"]
        rec["shap_alphamissense"] = d["ALPHAMISSENSE"]
        rec["shap_splicing"] = d["MERGED_SPLICING"]
        rec["ag_share"] = atlas.ag_share(d)
    print(f"{len(per_alt)} scored alternates over {end - start + 1} positions", file=sys.stderr)

    by_pos: dict[int, dict] = {}
    for (pos, ref, alt), rec in per_alt.items():
        p = by_pos.setdefault(pos, dict(ref=ref, n_alt=0, max_avi=0.0, max_spl=0.0,
                                        best_alt="", best_spl_alt=""))
        p["n_alt"] += 1
        if rec.get("avi_phred", 0) > p["max_avi"]:
            p["max_avi"], p["best_alt"] = rec["avi_phred"], alt
        if rec.get("splicing", 0) > p["max_spl"]:
            p["max_spl"], p["best_spl_alt"] = rec["splicing"], alt

    cols = ["pos", "ref", "n_alt", "region", "class", "max_avi_phred", "best_alt",
            "max_splicing", "best_splicing_alt", "proband_allele"]
    with open(args.out, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for pos in sorted(by_pos):
            p = by_pos[pos]
            fine, coarse = classify(pos, exons)
            fh.write("\t".join(str(x) for x in [
                pos, p["ref"], p["n_alt"], fine, coarse,
                f"{p['max_avi']:.4f}", p["best_alt"],
                f"{p['max_spl']:.5f}", p["best_spl_alt"],
                ALLELES.get(pos, "")]) + "\n")

    import statistics as st
    groups: dict[str, list[dict]] = {}
    for pos, p in by_pos.items():
        groups.setdefault(classify(pos, exons)[1], []).append(p)
    with open(args.summary, "w") as fh:
        fh.write("class\tpositions\tmed_max_avi\tp95_max_avi\tmed_max_splicing\t"
                 "p95_max_splicing\tfrac_splicing_over_2.47\n")
        for cls, ps in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            avi = sorted(p["max_avi"] for p in ps)
            spl = sorted(p["max_spl"] for p in ps)
            fh.write(f"{cls}\t{len(ps)}\t{st.median(avi):.2f}\t{avi[int(len(avi)*.95)]:.2f}\t"
                     f"{st.median(spl):.4f}\t{spl[int(len(spl)*.95)]:.4f}\t"
                     f"{sum(1 for x in spl if x >= 2.47) / len(spl):.4f}\n")
    print("wrote", args.out, "and", args.summary, file=sys.stderr)
    print(open(args.summary).read(), file=sys.stderr)


if __name__ == "__main__":
    main()
