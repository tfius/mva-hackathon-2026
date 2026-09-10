"""Query the AlphaGenome Atlas tabix releases for the two BUB1B alleles.

Requires the Atlas downloads (deepmind.google.com/science/alphagenome/downloads)
unzipped under ATLAS_DIR, and ``pysam`` for htslib/tabix access.

Writes mva/results/texdata_alphagenome_bub1b.tsv with every ALT at each
position, so the target allele can be read against its siblings. SHAP columns
are the per-feature contributions to the AVI raw score (they sum to it), which
shows how much of the AVI score is AlphaMissense re-counted.
"""
import os
import sys

import pysam

ATLAS_DIR = os.environ.get("ATLAS_DIR", "/mnt/data/AlphaGenome")
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "texdata_alphagenome_bub1b.tsv")

ALLELES = [
    ("chr15", 40209701, "T", "G", "c.2210T>G", "p.Leu737Ter"),
    ("chr15", 40220612, "T", "G", "c.3006T>G", "p.Asn1002Lys"),
]

FILES = {
    "avi": "alphagenome_variant_impact_score_snvs.tsv.gz",
    "splicing": "combined_alphagenome_splicing_snvs.tsv.gz",
    "shap": "combined_ag_cond_linear_ensemble_20260417_feature_importance_indels_with_am_snvs.tsv.gz",
}
SHAP_KEEP = ["PROTEIN_TERMINATION", "ALPHAMISSENSE", "PHASTCONS_470_WAY", "CACTUS_241_WAY", "MERGED_SPLICING"]


def main() -> None:
    tabs = {k: pysam.TabixFile(os.path.join(ATLAS_DIR, v)) for k, v in FILES.items()}
    rows = {}
    for chrom, pos, ref, alt, hgvs_c, hgvs_p in ALLELES:
        for r in tabs["avi"].fetch(chrom, pos - 1, pos):
            c, p, rf, al, raw, phred = r.split("\t")
            rows[(c, p, rf, al)] = dict(hgvs_c=hgvs_c if al == alt else "", hgvs_p=hgvs_p if al == alt else "",
                                        target="yes" if al == alt else "", avi_raw=raw, avi_phred=phred, splicing="")
        for r in tabs["splicing"].fetch(chrom, pos - 1, pos):
            c, p, rf, al, spl = r.split("\t")
            rows.setdefault((c, p, rf, al), dict(hgvs_c="", hgvs_p="", target="", avi_raw="", avi_phred=""))["splicing"] = spl
        hdr = tabs["shap"].header[0].lstrip("#").split("\t")
        for r in tabs["shap"].fetch(chrom, pos - 1, pos):
            d = dict(zip(hdr, r.split("\t")))
            row = rows.setdefault((d["CHROM"], d["POS"], d["REF"], d["ALT"]), dict(hgvs_c="", hgvs_p="", target="", avi_raw="", avi_phred="", splicing=""))
            feats = {k: float(v) for k, v in d.items() if k not in ("CHROM", "POS", "REF", "ALT")}
            for k in SHAP_KEEP:
                row["shap_" + k.lower()] = d[k]
            row["shap_other"] = f"{sum(v for k, v in feats.items() if k not in SHAP_KEEP):.4f}"
    cols = ["chrom", "pos", "ref", "alt", "target", "hgvs_c", "hgvs_p", "avi_raw", "avi_phred", "splicing"] + \
        ["shap_" + k.lower() for k in SHAP_KEEP] + ["shap_other"]
    with open(OUT, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for (c, p, rf, al), d in sorted(rows.items(), key=lambda kv: (kv[0][0], int(kv[0][1]), kv[0][3])):
            fh.write("\t".join([c, p, rf, al] + [d.get(k, "") for k in cols[4:]]) + "\n")
            print(c, p, rf, al, d["target"], d["avi_phred"], d["splicing"], file=sys.stderr)
    print("wrote", os.path.normpath(OUT), file=sys.stderr)


if __name__ == "__main__":
    main()
