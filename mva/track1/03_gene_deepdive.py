"""Deep dive on a single gene: classify every called variant by its position
relative to the canonical transcript's exons.

MVA1 is characteristically compound heterozygous with one truncating allele and
one hypomorphic allele that is often *not* a coding missense - deep-intronic
splice, 5'UTR or promoter. A coding-consequence filter would throw that allele
away, so this looks at everything in the locus.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

BCFTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/bcftools"
SPLICE_WINDOW = 20  # bp either side of an exon boundary worth flagging


def load_exons(path: str):
    exons, meta = [], []
    for line in open(path):
        if line.startswith("#"):
            meta.append(line.strip())
            continue
        if line.startswith("exon_index"):
            continue
        idx, start, end, _ = line.split("\t")
        exons.append((int(idx), int(start), int(end)))
    return meta, sorted(exons, key=lambda e: e[1])


def classify(pos: int, exons, gene_start: int, gene_end: int, strand: int) -> str:
    for idx, s, e in exons:
        if s <= pos <= e:
            return f"exon{idx}"
    for idx, s, e in exons:
        if s - SPLICE_WINDOW <= pos < s:
            return f"splice_5p_of_exon{idx}(-{s - pos})"
        if e < pos <= e + SPLICE_WINDOW:
            return f"splice_3p_of_exon{idx}(+{pos - e})"
    if gene_start <= pos <= gene_end:
        return "intron_deep"
    if pos < gene_start:
        return "upstream" if strand == 1 else "downstream"
    return "downstream" if strand == 1 else "upstream"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--exons", required=True)
    ap.add_argument("--region", required=True, help="e.g. 15:40140984-40241137")
    ap.add_argument("--clinvar")
    args = ap.parse_args()

    meta, exons = load_exons(args.exons)
    hdr = meta[0]  # "# SYMBOL ENSG chrN:start-end strand=S"
    coords = hdr.split()[3]
    gene_start, gene_end = (int(x) for x in coords.split(":")[1].split("-"))
    strand = int(hdr.split("strand=")[1])
    print("\n".join(meta))
    print(f"# splice window +/-{SPLICE_WINDOW} bp\n")

    fmt = "%CHROM\t%POS\t%REF\t%ALT\t%QUAL\t%FILTER\t[%GT\t%AD\t%DP\t%GQ]\n"
    cmd = [BCFTOOLS, "query", "-r", args.region, "-f", fmt, args.vcf]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

    print("chrom\tpos\tref\talt\tqual\tfilter\tgt\tad\tdp\tgq\tlocation")
    counts = {}
    for line in out.splitlines():
        f = line.split("\t")
        if f[6] in ("0/0", "./."):
            continue
        loc = classify(int(f[1]), exons, gene_start, gene_end, strand)
        key = loc.split("(")[0]
        counts[key] = counts.get(key, 0) + 1
        print(line + "\t" + loc)

    print("\n# location counts", file=sys.stderr)
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"#   {k}\t{v}", file=sys.stderr)


if __name__ == "__main__":
    main()
