"""Rare, high-scoring variants anywhere in the genome - the incidental-findings pass.

The dossier already shows that filtering to ClinVar Pathogenic asserts negatives
it has not earned. The Atlas allows the opposite pass: score every called SNV on
its predicted effect, with no database in the loop, then ask which of the
high-scoring ones are rare.

Each survivor is then characterised from evidence rather than from memory: how
many Pathogenic/Likely-pathogenic records ClinVar holds for that gene at all
(a gene with none is not an established Mendelian disease gene), and whether
the variant itself has a ClinVar record. No curated actionability list is
hard-coded here, because a list transcribed from memory is exactly the kind of
unaudited annotation this project keeps finding fault with.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys

BCFTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/bcftools"
CLINVAR = "/mnt/data/mva-hackathon-2026/refs/clinvar.vcf.gz"
PATHOGENIC = {"Pathogenic", "Likely_pathogenic", "Pathogenic/Likely_pathogenic"}

# Thresholds: the Atlas's own genome-wide percentiles, not round numbers.
SPLICING_P999 = 2.47
AVI_HIGH = 30.0
RARE_AF = 0.01


def clinvar_gene_burden(genes: set[str]) -> dict[str, dict]:
    """P/LP record count per gene, straight out of the ClinVar VCF."""
    fmt = "%INFO/GENEINFO\t%INFO/CLNSIG\n"
    out = subprocess.run([BCFTOOLS, "query", "-f", fmt, CLINVAR],
                         capture_output=True, text=True, check=True).stdout
    burden = {g: dict(plp=0, total=0) for g in genes}
    for line in out.splitlines():
        gi, sig = line.split("\t")
        for entry in gi.split("|"):
            sym = entry.split(":")[0]
            if sym in burden:
                burden[sym]["total"] += 1
                if sig in PATHOGENIC:
                    burden[sym]["plp"] += 1
    return burden


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True, help="genome_atlas.tsv from 11_")
    ap.add_argument("--vep", required=True, help="VEP JSON for the shortlist")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    vep = {}
    for v in json.load(open(args.vep)):
        c, p, _, ref, alt = v["input"].split()[:5]
        tc = [t for t in v.get("transcript_consequences", []) if t.get("canonical")]
        t = tc[0] if tc else (v.get("transcript_consequences") or [{}])[0]
        af, ids = None, []
        for cv in v.get("colocated_variants", []):
            ids.append(cv.get("id"))
            for fr in cv.get("frequencies", {}).values():
                if fr.get("gnomadg") is not None:
                    af = fr["gnomadg"]
                elif af is None and fr.get("gnomade") is not None:
                    af = fr["gnomade"]
        vep[("chr" + c, p, ref, alt)] = dict(
            gene=t.get("gene_symbol") or "", consequence=v.get("most_severe_consequence"),
            hgvsc=t.get("hgvsc") or "", af=af, ids=[i for i in ids if i],
            spliceai=max([(t.get("spliceai") or {}).get(k) or 0
                          for k in ("DS_AG", "DS_AL", "DS_DG", "DS_DL")] + [0]))

    shortlist = []
    for r in csv.DictReader(open(args.scan), delimiter="\t"):
        key = (r["chrom"], r["pos"], r["ref"], r["alt"])
        if key not in vep:
            continue
        info = vep[key]
        if info["af"] is not None and info["af"] >= RARE_AF:
            continue
        shortlist.append((r, info))
    genes = {i["gene"] for _, i in shortlist if i["gene"]}
    burden = clinvar_gene_burden(genes)

    cols = ["chrom", "pos", "ref", "alt", "gene", "consequence", "hgvsc", "genotype",
            "filter", "gnomad_af", "dbsnp", "avi_phred", "splicing", "spliceai",
            "clinvar_gene_plp", "clinvar_gene_records", "flag"]
    with open(args.out, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        print(f"{len(shortlist)} rare high-scoring SNVs\n")
        for r, i in sorted(shortlist, key=lambda x: -float(x[0]["avi_phred"] or 0)):
            b = burden.get(i["gene"], dict(plp=0, total=0))
            flags = []
            if r["gt"] != "1/1":
                flags.append("heterozygous")
            if b["plp"] == 0:
                flags.append("no P/LP record in this gene")
            if float(r["splicing"] or 0) >= SPLICING_P999 and i["spliceai"] < 0.2:
                flags.append("splice call disputed by SpliceAI")
            fh.write("\t".join(str(x) for x in [
                r["chrom"], r["pos"], r["ref"], r["alt"], i["gene"], i["consequence"],
                i["hgvsc"], r["gt"], r["filter"], i["af"], ",".join(i["ids"]),
                r["avi_phred"], r["splicing"], i["spliceai"], b["plp"], b["total"],
                "; ".join(flags)]) + "\n")
            print(f"  {i['gene']:10s} {r['chrom']}:{r['pos']} {r['ref']}>{r['alt']} "
                  f"{r['gt']} AVI={float(r['avi_phred']):.1f} spl={r['splicing']:>7s} "
                  f"AF={i['af']} ClinVar P/LP in gene={b['plp']:<5d} {'; '.join(flags)}")

    homs = [r for r, _ in shortlist if r["gt"] == "1/1"]
    per_gene: dict[str, int] = {}
    for _, i in shortlist:
        per_gene[i["gene"]] = per_gene.get(i["gene"], 0) + 1
    biallelic = {g: n for g, n in per_gene.items() if n > 1}
    print(f"\nhomozygous: {len(homs)}   genes carrying more than one: {biallelic or 'none'}")
    print(f"genes with any ClinVar P/LP record: "
          f"{sorted(g for g in genes if burden[g]['plp'] > 0)}")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
