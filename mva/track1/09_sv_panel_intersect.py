"""Intersect delly's structural variant calls with the MVA gene panel.

The supplied VCF is SNV/indel only, so a structural variant anywhere in the
panel would have been invisible to every analysis before the realignment. The
depth and heterozygosity evidence in the Track 1 report already argues against
one in BUB1B - flat 26-48x across the gene, no run of homozygosity - but that is
an absence-of-evidence argument from coverage. This is the direct test, using
read-pair and split-read support.

The answer key is confirmed as the BUB1B compound heterozygote, so this can no
longer change the call. It closes the completeness question: was a structural
event missed anywhere in the genes that matter?

Reports every call touching a panel gene, flags those hitting the two confirmed
alleles or any coding exon of the MVA core genes, and prints the genome-wide
totals for context, since "no SV in BUB1B" only means something alongside how
many the caller found overall.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter, defaultdict

BCFTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/bcftools"
MVA_CORE = {"BUB1B", "BUB1", "BUB3", "CEP57", "TRIP13", "CENPE"}
CONFIRMED = [("chr15", 40209701), ("chr15", 40220612)]


def load_panel(bed: str):
    """chrom -> [(start, end, gene)], from the +/-50 kb panel regions."""
    regions = defaultdict(list)
    for line in open(bed):
        f = line.split("\t")
        regions[f[0]].append((int(f[1]), int(f[2]), f[3]))
    return regions


def overlaps(chrom, start, end, regions):
    return [g for s, e, g in regions.get(chrom, ()) if start <= e and end >= s]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bcf", default="/mnt/data/mva-hackathon-2026/work/align/delly.bcf")
    ap.add_argument("--bed", default="/home/tex/repos/ligands/mva/src/mva/panel_regions.bed")
    ap.add_argument("--min-pe", type=int, default=3,
                    help="minimum paired-end support to report")
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/align/"
                                     "sv_panel_hits.tsv")
    args = ap.parse_args()

    regions = load_panel(args.bed)
    fmt = ("%CHROM\t%POS\t%INFO/END\t%INFO/SVTYPE\t%INFO/SVLEN\t%FILTER\t"
           "%INFO/PE\t%INFO/SR\t%INFO/PRECISE\t[%GT]\n")
    try:
        out = subprocess.run([BCFTOOLS, "query", "-f", fmt, args.bcf],
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        sys.exit(f"could not read {args.bcf}: {e.stderr[:300]}")

    total, passing = Counter(), Counter()
    hits = []
    for line in out.splitlines():
        f = line.split("\t")
        chrom, pos = f[0], int(f[1])
        end = int(f[2]) if f[2] not in (".", "") else pos
        svtype, svlen, filt = f[3], f[4], f[5]
        pe = int(f[6]) if f[6] not in (".", "") else 0
        sr = int(f[7]) if f[7] not in (".", "") else 0
        gt = f[9]
        total[svtype] += 1
        if filt == "PASS":
            passing[svtype] += 1
        if filt != "PASS" or pe < args.min_pe:
            continue
        genes = overlaps(chrom, pos, end, regions)
        if genes:
            hits.append((chrom, pos, end, svtype, svlen, pe, sr, gt, ",".join(sorted(set(genes)))))

    print("genome-wide delly calls by type (all / PASS):")
    for t in sorted(total):
        print(f"  {t:8s} {total[t]:7,} / {passing[t]:,}")
    print(f"  {'TOTAL':8s} {sum(total.values()):7,} / {sum(passing.values()):,}\n")

    print(f"PASS calls with PE>={args.min_pe} touching a panel gene "
          f"(+/-50 kb): {len(hits)}")
    for h in sorted(hits, key=lambda x: (x[8], x[1])):
        chrom, pos, end, svtype, svlen, pe, sr, gt, genes = h
        core = " [MVA CORE]" if set(genes.split(",")) & MVA_CORE else ""
        print(f"  {genes:22.22s} {chrom}:{pos:,}-{end:,} {svtype:5s} "
              f"len={svlen:>9s} PE={pe:<4d} SR={sr:<4d} GT={gt}{core}")

    print("\nstructural variants spanning either confirmed allele:")
    spanning = [h for h in hits
                if any(h[0] == c and h[1] <= p <= h[2] for c, p in CONFIRMED)]
    if spanning:
        for h in spanning:
            print(f"  {h}")
    else:
        print("  none — neither confirmed allele sits inside a called SV, so the "
              "compound heterozygote is not a mis-called structural event")

    with open(args.out, "w") as fh:
        fh.write("chrom\tstart\tend\tsvtype\tsvlen\tpe\tsr\tgt\tgenes\n")
        for h in sorted(hits, key=lambda x: (x[8], x[1])):
            fh.write("\t".join(str(x) for x in h) + "\n")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
