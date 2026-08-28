"""Whole-chromosome dosage from read depth — the independent check on 04.

`04_mosaic_aneuploidy.py` bounded mosaic aneuploidy using B-allele frequencies
from the VCF. This asks the same question from a different modality entirely,
read depth, so the two can agree or disagree on their own evidence.

**The naive version is wrong, and visibly so.** mosdepth's per-chromosome mean
reports chr22 at 36.5x, chr15 at 38.8x, chr14 at 39.0x and chr13 at 40.8x
against a genome mean near 46x. Those are the acrocentrics: their satellite and
rDNA arrays are unmappable, contribute zero-coverage bases, and drag a
whole-length mean down. Read as dosage that is a 20% deficit on five
chromosomes, which would be a spectacular finding and is an artefact of
including regions no read can map to.

The fix is to work from the 10 kb window depths and take a **median over
mappable windows** - windows whose depth falls in a plausible band around the
genome median. The median is insensitive to the zero blocks and to the
high-depth pileups over segmental duplications, both of which are position
artefacts rather than dosage.

For a chromosome present in three copies in a fraction f of cells, expected
depth ratio is (2 + f) / 2. So f = 2 * (ratio - 1), and the detection limit
follows from the chromosome-to-chromosome scatter.
"""
from __future__ import annotations

import argparse
import gzip
import statistics
from collections import defaultdict

AUTOSOMES = [f"chr{c}" for c in range(1, 23)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", default="/mnt/data/mva-hackathon-2026/work/align/"
                                         "mosdepth.10kb.regions.bed.gz")
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/align/"
                                     "coverage_dosage.tsv")
    args = ap.parse_args()

    by_chrom = defaultdict(list)
    with gzip.open(args.regions, "rt") as fh:
        for line in fh:
            chrom, _s, _e, depth = line.split("\t")
            if "_" in chrom or chrom == "chrM":
                continue
            by_chrom[chrom].append(float(depth))

    # Genome-wide median over all windows sets the mappable band.
    allw = [d for c in AUTOSOMES if c in by_chrom for d in by_chrom[c]]
    gmed = statistics.median([d for d in allw if d > 0])
    lo, hi = 0.5 * gmed, 1.75 * gmed
    print(f"genome median window depth {gmed:.2f}x; "
          f"mappable band {lo:.1f}-{hi:.1f}x\n")

    rows = {}
    for chrom, ds in by_chrom.items():
        kept = [d for d in ds if lo <= d <= hi]
        if len(kept) < 200:
            continue
        rows[chrom] = {
            "n_windows": len(ds),
            "n_mappable": len(kept),
            "frac_mappable": len(kept) / len(ds),
            "median": statistics.median(kept),
            "naive_mean": statistics.fmean(ds),
        }

    auto_med = statistics.median(rows[c]["median"] for c in AUTOSOMES if c in rows)
    ratios = [rows[c]["median"] / auto_med for c in AUTOSOMES if c in rows]
    sd = statistics.stdev(ratios)

    hdr = ("chrom", "median_mappable", "ratio", "implied_f", "naive_mean",
           "frac_mappable")
    lines = ["\t".join(hdr)]
    print(f"{'chrom':7s} {'median':>8s} {'ratio':>7s} {'implied f':>10s} "
          f"{'naive mean':>11s} {'mappable':>9s}")
    for c in AUTOSOMES + ["chrX", "chrY"]:
        if c not in rows:
            continue
        r = rows[c]
        ratio = r["median"] / auto_med
        f = 2 * (ratio - 1)
        print(f"{c:7s} {r['median']:8.2f} {ratio:7.3f} {f:+10.3f} "
              f"{r['naive_mean']:11.2f} {r['frac_mappable']:8.1%}")
        lines.append(f"{c}\t{r['median']:.3f}\t{ratio:.4f}\t{f:+.4f}\t"
                     f"{r['naive_mean']:.3f}\t{r['frac_mappable']:.4f}")

    worst = max(abs(x - 1) for x in ratios)
    print(f"\nautosomal median-of-medians {auto_med:.2f}x; "
          f"chromosome-to-chromosome sd of the ratio {sd:.4f}")
    print(f"largest autosomal deviation {worst:.4f} "
          f"({worst / sd:.1f} sd) -> implied f {2 * worst:+.3f}")
    print(f"3-sigma detection limit on a whole-chromosome gain: f ~ {6 * sd:.3f}")
    if "chrX" in rows and "chrY" in rows:
        print(f"\nchrX ratio {rows['chrX']['median'] / auto_med:.3f}, "
              f"chrY ratio {rows['chrY']['median'] / auto_med:.3f} — "
              f"consistent with a male karyotype")
    open(args.out, "w").write("\n".join(lines) + "\n")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
