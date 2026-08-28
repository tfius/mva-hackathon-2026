"""Attempt read-backed phasing of the two BUB1B alleles, and measure the failure.

The Track 1 report says phase cannot be determined from this data. That claim
should be a measurement rather than an assertion, so this makes the attempt and
reports the numbers that decide it:

  * the observed insert-size distribution, which sets how far a read pair can
    physically reach
  * the gap between the two alleles, and the gaps between every intervening
    heterozygous site, which is what read-backed chaining would have to cross
  * any read or read pair actually spanning two heterozygous sites, which is
    what phasing would need and what almost certainly does not exist at
    10,911 bp with a 150 bp paired-end library

If a chain does exist, this finds it. If it does not, the report can say by how
much it fails rather than merely that it does.
"""
from __future__ import annotations

import argparse
import statistics
import subprocess
from collections import defaultdict

SAMTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/samtools"
BCFTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/bcftools"

ALLELE_A = ("chr15", 40209701, "T", "G")
ALLELE_B = ("chr15", 40220612, "T", "G")


def insert_sizes(bam: str, region: str, cap: int = 200_000):
    """Template lengths of properly-paired reads in a region."""
    out = subprocess.run(
        [SAMTOOLS, "view", "-f", "2", "-F", "3852", bam, region],
        capture_output=True, text=True, check=True).stdout
    sizes = []
    for line in out.splitlines():
        f = line.split("\t")
        tlen = abs(int(f[8]))
        if 0 < tlen < 100_000:
            sizes.append(tlen)
        if len(sizes) >= cap:
            break
    return sizes


def het_sites(vcf: str, region: str):
    fmt = "%CHROM\t%POS\t%REF\t%ALT\t[%GT]\n"
    out = subprocess.run([BCFTOOLS, "query", "-r", region, "-f", fmt, vcf],
                         capture_output=True, text=True, check=True).stdout
    sites = []
    for line in out.splitlines():
        c, p, ref, alt, gt = line.split("\t")
        if gt in ("0/1", "0|1", "1|0") and len(ref) == 1 and len(alt) == 1:
            sites.append((c, int(p), ref, alt))
    return sites


def reads_over(bam: str, chrom: str, pos: int):
    """Map read name -> base observed at pos, for reads covering it."""
    out = subprocess.run(
        [SAMTOOLS, "view", "-F", "3852", bam, f"{chrom}:{pos}-{pos}"],
        capture_output=True, text=True, check=True).stdout
    calls = {}
    for line in out.splitlines():
        f = line.split("\t")
        name, start, cigar, seq = f[0], int(f[3]), f[5], f[9]
        # walk the CIGAR to find the read offset of the reference position
        ref, read, num = start, 0, ""
        base = None
        for ch in cigar:
            if ch.isdigit():
                num += ch
                continue
            n = int(num); num = ""
            if ch in "M=X":
                if ref <= pos < ref + n:
                    base = seq[read + (pos - ref)]
                    break
                ref += n; read += n
            elif ch in "DN":
                if ref <= pos < ref + n:
                    base = "-"
                    break
                ref += n
            elif ch in "IS":
                read += n
            elif ch == "H":
                pass
        if base:
            calls[name] = base
    return calls


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bam", default="/mnt/data/mva-hackathon-2026/work/align/"
                                     "WGS_EX2312012.markdup.bam")
    ap.add_argument("--vcf", default="/mnt/data/mva-hackathon-2026/work/norm.vcf.gz")
    args = ap.parse_args()

    lo, hi = ALLELE_A[1], ALLELE_B[1]
    gap = hi - lo
    region = f"chr15:{lo - 5000}-{hi + 5000}"
    print(f"allele A {ALLELE_A[0]}:{lo} {ALLELE_A[2]}>{ALLELE_A[3]}")
    print(f"allele B {ALLELE_B[0]}:{hi} {ALLELE_B[2]}>{ALLELE_B[3]}")
    print(f"gap {gap:,} bp\n")

    sizes = insert_sizes(args.bam, region)
    sizes.sort()
    n = len(sizes)
    print(f"insert size over the locus (n={n:,} properly-paired reads)")
    for q in (0.5, 0.9, 0.99, 0.999, 1.0):
        print(f"  p{q*100:<6g} {sizes[min(n - 1, int(q * n))]:>8,} bp")
    print(f"  mean   {statistics.mean(sizes):>8,.0f} bp")
    print(f"\n  the gap is {gap / sizes[-1]:.0f}x the largest observed template "
          f"({sizes[-1]:,} bp)")

    hets = het_sites(args.vcf, f"chr15:{lo}-{hi}")
    print(f"\nheterozygous SNVs from allele A to allele B inclusive: {len(hets)}")
    prev = None
    max_gap = 0
    for c, p, ref, alt in hets:
        d = "" if prev is None else f"  (+{p - prev:,} bp)"
        if prev is not None:
            max_gap = max(max_gap, p - prev)
        print(f"  {c}:{p} {ref}>{alt}{d}")
        prev = p
    print(f"\nlargest step in the chain: {max_gap:,} bp — read-backed phasing "
          f"needs a read or pair spanning each step")

    # Does any single template actually connect two consecutive het sites?
    print("\nchecking for templates spanning consecutive heterozygous sites:")
    linked = 0
    for (c1, p1, _, _), (c2, p2, _, _) in zip(hets, hets[1:]):
        a, b = reads_over(args.bam, c1, p1), reads_over(args.bam, c2, p2)
        shared = set(a) & set(b)
        status = f"{len(shared)} shared template(s)" if shared else "none"
        print(f"  {p1:,} -> {p2:,}  ({p2 - p1:,} bp)  {status}")
        if shared:
            linked += 1
    print(f"\n{linked} of {max(0, len(hets) - 1)} consecutive steps are bridged "
          f"by at least one template.")
    print("A complete chain requires every step to be bridged." if linked else
          "No step is bridged: phase is not recoverable from this library.")


if __name__ == "__main__":
    main()
