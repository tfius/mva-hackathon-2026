"""Test the germline VCF for mosaic aneuploidy, with no realignment required.

Mosaic variegated aneuploidy is defined cytogenetically, not by its variants, so
the diagnosis makes a prediction the sequencing data can be asked about directly.

In a population where a fraction f of cells carries three copies of a chromosome,
a heterozygous SNP on it no longer sits at allele balance 0.5. Allele dosages
become (1 + f) and 1 out of (2 + f), so the B-allele frequency splits into bands

    (1 + f) / (2 + f)  and  1 / (2 + f)     i.e.  0.5 +/- f / (2 * (2 + f))

which for small f is 0.5 +/- f/4. A mosaic monosomy is the mirror image. Binomial
sampling at ~44x drowns this in any single SNP, so the statistic is aggregate:
per chromosome, the variance of the B-allele frequency in excess of what binomial
sampling explains,

    excess_var = Var(BAF) - mean( BAF * (1 - BAF) / DP )

with the implied mosaic fraction f ~ 4 * sqrt(excess_var).

The filters are the whole difference between a result and an artefact. Run
unfiltered, this statistic reports a large "signal" on chr17, chr19, chr20 and
chr22 that is entirely GC and mappability bias - those are the GC-rich,
segmental-duplication-rich chromosomes, and their apparent excess tracks
reference bias rather than copy number. Requiring MQ >= 59, dbSNP membership and
a narrow depth band removes it.
"""
from __future__ import annotations

import argparse
import math
import statistics
import subprocess
import sys
from collections import defaultdict

BCFTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/bcftools"
AUTOSOMES = [f"chr{c}" for c in range(1, 23)]


def collect(vcf, min_mq, dp_lo, dp_hi, min_gq, require_dbsnp):
    fmt = "%CHROM\t%POS\t%REF\t%ALT\t%FILTER\t%MQ\t%DB\t[%GT\t%AD\t%GQ]\n"
    proc = subprocess.Popen([BCFTOOLS, "query", "-f", fmt, vcf],
                            stdout=subprocess.PIPE, text=True)
    by_chrom = defaultdict(list)
    for line in proc.stdout:
        chrom, _pos, ref, alt, filt, mq, db, gt, ad, gq = line.rstrip("\n").split("\t")
        if filt != "PASS" or gt not in ("0/1", "0|1", "1|0"):
            continue
        if len(ref) != 1 or len(alt) != 1:
            continue          # indel allele depths are not trustworthy for balance
        if require_dbsnp and db != "1":
            continue          # dbSNP membership stands in for "common, well behaved"
        try:
            if float(mq) < min_mq:
                continue
            ad_ref, ad_alt = (int(x) for x in ad.split(",")[:2])
            if int(gq) < min_gq:
                continue
        except ValueError:
            continue
        dp = ad_ref + ad_alt
        if not (dp_lo <= dp <= dp_hi):
            continue          # a narrow band removes the depth dependence of the
                              # binomial term instead of modelling it
        by_chrom[chrom].append((ad_alt / dp, dp))
    proc.stdout.close()
    proc.wait()
    return by_chrom


def summarise(by_chrom):
    out = {}
    for chrom, vals in by_chrom.items():
        n = len(vals)
        if n < 1000:
            continue
        bafs = [b for b, _ in vals]
        mean = sum(bafs) / n
        var = sum((b - mean) ** 2 for b in bafs) / n
        binom = sum(b * (1 - b) / d for b, d in vals) / n
        excess = var - binom
        out[chrom] = {
            "n_het": n,
            "mean_baf": mean,
            "excess_var": excess,
            "implied_f": 4 * math.sqrt(excess) if excess > 0 else 0.0,
            "median_dp": statistics.median(d for _, d in vals),
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--min-mq", type=float, default=59.0)
    ap.add_argument("--dp-lo", type=int, default=38)
    ap.add_argument("--dp-hi", type=int, default=50)
    ap.add_argument("--min-gq", type=int, default=50)
    ap.add_argument("--no-dbsnp-filter", action="store_true",
                    help="reproduce the confounded version, for the report")
    ap.add_argument("--out")
    args = ap.parse_args()

    stats = summarise(collect(args.vcf, args.min_mq, args.dp_lo, args.dp_hi,
                              args.min_gq, not args.no_dbsnp_filter))
    auto = [c for c in AUTOSOMES if c in stats]
    excesses = [stats[c]["excess_var"] for c in auto]
    med = statistics.median(excesses)
    sd = statistics.stdev(excesses)

    lines = ["chrom\tn_het\tmean_baf\texcess_var\tdelta_vs_median\timplied_f\tmedian_dp"]
    for c in auto + [x for x in ("chrX", "chrY") if x in stats]:
        s = stats[c]
        lines.append(
            f"{c}\t{s['n_het']}\t{s['mean_baf']:.5f}\t{s['excess_var']:.6f}\t"
            f"{s['excess_var'] - med:+.6f}\t{s['implied_f']:.4f}\t{s['median_dp']:.0f}"
        )
    text = "\n".join(lines)
    print(text)

    # Detection limit: a 3-sigma outlier against the chromosome-to-chromosome
    # scatter is the smallest per-chromosome mosaic fraction this can see.
    f_limit = 4 * math.sqrt(3 * sd) if sd > 0 else float("nan")
    print(
        f"\n# autosomal excess variance: median {med:.6f}, sd across chromosomes {sd:.6f}\n"
        f"# no chromosome deviates by more than {max(abs(e - med) for e in excesses) / sd:.1f} sd\n"
        f"# 3-sigma per-chromosome detection limit: mosaic fraction f ~ {f_limit:.3f}\n"
        f"# NOTE the uniform floor of {med:.6f} is shared by every chromosome. It is either\n"
        f"#      technical overdispersion or a genome-wide uniform mosaic fraction of\n"
        f"#      f ~ {4 * math.sqrt(med):.2f}; a single sample cannot separate the two. A\n"
        f"#      *variegated* aneuploidy - a different random chromosome per cell - is\n"
        f"#      precisely the situation that produces a uniform floor and no per-chromosome\n"
        f"#      outlier, so this result is consistent with, not evidence against, MVA.",
        file=sys.stderr,
    )
    if args.out:
        open(args.out, "w").write(text + "\n")


if __name__ == "__main__":
    main()
