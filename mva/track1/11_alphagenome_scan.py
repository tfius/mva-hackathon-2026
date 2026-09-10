"""Annotate every called SNV in a VCF (optionally restricted to a BED) with the
AlphaGenome Atlas AVI score and merged splicing score, via tabix -R batching.

AVI already contains AlphaMissense and protein-termination flags as features, so
it is not an independent line of evidence for coding variants; the splicing
score is what this scan is for - a deep-intronic or synonymous cryptic-splice
allele that a consequence filter would discard.
"""
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys

ENV = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin"
ATLAS_DIR = os.environ.get("ATLAS_DIR", "/mnt/data/AlphaGenome")
AVI = os.path.join(ATLAS_DIR, "alphagenome_variant_impact_score_snvs.tsv.gz")
SPL = os.path.join(ATLAS_DIR, "combined_alphagenome_splicing_snvs.tsv.gz")


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--bed", help="restrict to these regions")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--threads", type=int, default=24)
    args = ap.parse_args()
    os.makedirs(args.workdir, exist_ok=True)

    fmt = "%CHROM\t%POS\t%REF\t%ALT\t%FILTER\t%QUAL\t[%GT\t%AD\t%DP\t%GQ]\n"
    cmd = [f"{ENV}/bcftools", "query", "-i", 'TYPE="snp" && GT="alt"', "-f", fmt]
    if args.bed:
        cmd += ["-R", args.bed]
    cmd.append(args.vcf)
    calls = {}
    beds = {}
    for line in run(cmd).splitlines():
        f = line.split("\t")
        calls[(f[0], f[1], f[2], f[3])] = f[4:]
        beds.setdefault(f[0], []).append(f"{f[0]}\t{int(f[1]) - 1}\t{f[1]}\n")
    for chrom, lines in beds.items():
        path = os.path.join(args.workdir, f"sites.{chrom}.bed")
        content = "".join(lines)
        if not (os.path.exists(path) and open(path).read() == content):  # keep mtime if unchanged
            with open(path, "w") as bed:
                bed.write(content)
    print(f"{len(calls)} SNV calls on {len(beds)} contigs", file=sys.stderr)

    # One tabix -R per contig and file, in parallel; a finished output newer
    # than its BED is reused, so an interrupted run resumes.
    jobs = []
    for chrom in beds:
        bed = os.path.join(args.workdir, f"sites.{chrom}.bed")
        for label, fn in (("avi", AVI), ("spl", SPL)):
            out = f"{bed}.{label}"
            if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(bed) and os.path.getsize(out) > 0:
                continue
            jobs.append((bed, fn, out))

    def lookup(job):
        bed, fn, out = job
        with open(out + ".tmp", "w") as fh:
            subprocess.run([f"{ENV}/tabix", "-R", bed, fn], check=True, stdout=fh)
        os.replace(out + ".tmp", out)

    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        list(pool.map(lookup, jobs))

    ann = {}
    for label, ncol in (("avi", 2), ("spl", 1)):
        n = 0
        for chrom in beds:
            for line in open(os.path.join(args.workdir, f"sites.{chrom}.bed.{label}")):
                f = line.rstrip("\n").split("\t")
                key = tuple(f[:4])
                if key in calls:
                    ann.setdefault(key, {})[label] = f[4:4 + ncol]
                    n += 1
        print(f"{label}: {n} matched", file=sys.stderr)

    with open(args.out, "w") as fh:
        fh.write("chrom\tpos\tref\talt\tfilter\tqual\tgt\tad\tdp\tgq\tavi_raw\tavi_phred\tsplicing\n")
        for key in sorted(calls, key=lambda k: (k[0], int(k[1]))):
            a = ann.get(key, {})
            fh.write("\t".join(list(key) + calls[key] + a.get("avi", ["", ""]) + a.get("spl", [""])) + "\n")
    print("wrote", args.out, file=sys.stderr)


if __name__ == "__main__":
    main()
