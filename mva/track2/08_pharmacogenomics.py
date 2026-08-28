"""Pharmacogenomic screen of the challenge WGS, scoped to this child's actual care.

The m.1555A>G check in section 6 was one locus pair chosen because it bore on a
candidate. This is the screen proper.

The framing matters. This child has had a rhabdomyosarcoma. Whatever happens to
the repurposing hypotheses in this report, they are receiving oncology care now -
cytotoxics, anaesthesia for surgery, antifungal and antibacterial prophylaxis
through neutropenia. Every one of those has a CPIC-level pharmacogenomic
guideline, and the genotype needed to apply it is already sitting in the
diagnostic VCF. It costs one query.

That is the argument for doing this at all: the marginal cost of a
pharmacogenomic read-out on a genome already sequenced for diagnosis is
approximately zero, and the clinical relevance is immediate rather than
hypothetical.

**Absence of a variant call is not the same as a reference genotype.** A position
with no coverage produces no call, exactly like a homozygous-reference position.
Every locus here is therefore checked against the BAM for read depth, and any
locus without adequate coverage is reported as "not assessable" rather than
silently counted as normal - the same discipline the mosaic-aneuploidy analysis
needed.

Deliberately out of scope, because short-read WGS cannot do them honestly
without dedicated tools: CYP2D6 star-allele calling (structural variation and
gene conversion with CYP2D7), UGT1A1*28 (a promoter TA repeat), and HLA typing.
Those are named in the output rather than omitted.
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.request

BCFTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/bcftools"
SAMTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/samtools"
VCF = "/mnt/data/mva-hackathon-2026/work/norm.vcf.gz"
BAM = "/mnt/data/mva-hackathon-2026/work/align/WGS_EX2312012.markdup.bam"

# (rsid, gene, allele, drug(s), why it matters for this child)
PANEL = [
    ("rs3918290",   "DPYD",    "*2A",      "fluorouracil, capecitabine",
     "TxGNN ranked fluorouracil 6th; DPYD deficiency causes severe, sometimes fatal toxicity"),
    ("rs55886062",  "DPYD",    "*13",      "fluorouracil, capecitabine", "same"),
    ("rs67376798",  "DPYD",    "c.2846A>T","fluorouracil, capecitabine", "same"),
    ("rs75017182",  "DPYD",    "HapB3",    "fluorouracil, capecitabine", "same"),
    ("rs116855232", "NUDT15",  "*3",       "mercaptopurine, azathioprine",
     "thiopurine myelosuppression; relevant if leukaemia or immunosuppression follows"),
    ("rs1800462",   "TPMT",    "*2",       "mercaptopurine, azathioprine", "same"),
    ("rs1800460",   "TPMT",    "*3B",      "mercaptopurine, azathioprine", "same"),
    ("rs1142345",   "TPMT",    "*3C",      "mercaptopurine, azathioprine", "same"),
    ("rs1050828",   "G6PD",    "A- 202A",  "rasburicase, primaquine",
     "rasburicase is used for tumour-lysis syndrome and causes haemolysis in G6PD deficiency"),
    ("rs1050829",   "G6PD",    "A 376G",   "rasburicase, primaquine", "same"),
    ("rs4244285",   "CYP2C19", "*2",       "voriconazole",
     "antifungal prophylaxis through neutropenia; poor metabolisers overshoot"),
    ("rs4986893",   "CYP2C19", "*3",       "voriconazole", "same"),
    ("rs12248560",  "CYP2C19", "*17",      "voriconazole",
     "ultrarapid metabolisers underdose"),
    ("rs776746",    "CYP3A5",  "*3",       "tacrolimus", "if immunosuppression is ever needed"),
    ("rs4149056",   "SLCO1B1", "*5",       "statins", "low relevance here; included as a control locus"),
    ("rs6025",      "F5",      "Leiden",   "thrombosis risk",
     "central venous access plus chemotherapy is a prothrombotic setting"),
    ("rs1799963",   "F2",      "20210G>A", "thrombosis risk", "same"),
]

NOT_ASSESSABLE = [
    ("CYP2D6", "star alleles", "codeine, tramadol, ondansetron",
     "requires structural-variant and CYP2D7 gene-conversion aware calling"),
    ("UGT1A1", "*28",          "irinotecan (VIT regimen in rhabdomyosarcoma)",
     "promoter TA-repeat length; short reads cannot size it reliably"),
    ("HLA-B",  "*15:02, *58:01","carbamazepine, allopurinol",
     "requires dedicated HLA typing"),
]


def _get(url, data=None, tries=5):
    """Ensembl returns 503 under load; retry with backoff rather than giving up."""
    import time
    hdrs = {"Accept": "application/json", "User-Agent": "curl/8.5.0"}
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    for n in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=hdrs)
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except Exception as e:
            if n == tries - 1:
                raise
            time.sleep(2 ** n)
    return None


def _mapping(rec):
    for m in rec.get("mappings", []):
        if m.get("assembly_name") == "GRCh38" and "_" not in str(m["seq_region_name"]):
            return (f"chr{m['seq_region_name']}", int(m["start"]), m.get("allele_string"))
    return None


def resolve(rsids):
    """rsID -> (chrom, pos, alleles) on GRCh38, via Ensembl. Batch, then
    per-ID for anything the batch missed."""
    out = {}
    for i in range(0, len(rsids), 20):
        chunk = rsids[i:i + 20]
        try:
            data = _get("https://rest.ensembl.org/variation/homo_sapiens",
                        json.dumps({"ids": chunk}).encode())
        except Exception as e:
            print(f"  batch failed ({e}); falling back to per-ID", file=sys.stderr)
            data = {}
        for rs, rec in (data or {}).items():
            m = _mapping(rec)
            if m:
                out[rs] = m
    for rs in rsids:
        if rs in out:
            continue
        try:
            rec = _get(f"https://rest.ensembl.org/variation/homo_sapiens/{rs}")
            m = _mapping(rec)
            if m:
                out[rs] = m
        except Exception as e:
            print(f"  {rs}: {e}", file=sys.stderr)
    return out


def genotype(chrom, pos):
    r = subprocess.run(
        [BCFTOOLS, "query", "-r", f"{chrom}:{pos}", "-f", "%REF\t%ALT\t[%GT\t%AD\t%DP]\n", VCF],
        capture_output=True, text=True)
    return [l.split("\t") for l in r.stdout.splitlines()]


def depth(chrom, pos):
    r = subprocess.run([SAMTOOLS, "depth", "-r", f"{chrom}:{pos}-{pos}", "-a", BAM],
                       capture_output=True, text=True)
    try:
        return int(r.stdout.split("\t")[2])
    except (IndexError, ValueError):
        return 0


def main() -> None:
    coords = resolve([p[0] for p in PANEL])
    print(f"resolved {len(coords)}/{len(PANEL)} rsIDs to GRCh38\n")
    print(f"{'gene':9s} {'allele':11s} {'rsid':13s} {'locus':22s} {'depth':>7s}  genotype")
    print("-" * 100)

    flagged, unassessable = [], []
    for rs, gene, allele, drug, why in PANEL:
        if rs not in coords:
            unassessable.append((gene, allele, rs, "rsID did not resolve"))
            continue
        chrom, pos, astr = coords[rs]
        d = depth(chrom, pos)
        calls = genotype(chrom, pos)
        if d < 10:
            unassessable.append((gene, allele, rs, f"only {d}x coverage"))
            state = f"NOT ASSESSABLE ({d}x)"
        elif not calls:
            state = "homozygous reference"
        else:
            ref, alt, gt, ad, dp = calls[0]
            state = f"**{gt}**  {ref}>{alt}  AD={ad} DP={dp}"
            if gt not in ("0/0", "./."):
                flagged.append((gene, allele, rs, f"{chrom}:{pos}", gt, drug, why))
        print(f"{gene:9s} {allele:11s} {rs:13s} {chrom+':'+str(pos):22s} {d:6d}x  {state}")

    print("\n" + "=" * 100)
    if flagged:
        print(f"\n{len(flagged)} ACTIONABLE VARIANT(S) CARRIED:")
        for gene, allele, rs, loc, gt, drug, why in flagged:
            print(f"\n  {gene} {allele} ({rs}) at {loc} — genotype {gt}")
            print(f"    affects: {drug}")
            print(f"    why it matters here: {why}")
    else:
        print("\nNo actionable pharmacogenomic variant carried at any assessed locus.")

    if unassessable:
        print(f"\n{len(unassessable)} locus/loci not assessable:")
        for gene, allele, rs, reason in unassessable:
            print(f"  {gene} {allele} ({rs}) — {reason}")

    print("\nOut of scope for short-read WGS without dedicated tools "
          "(named rather than silently omitted):")
    for gene, what, drug, why in NOT_ASSESSABLE:
        print(f"  {gene} {what} — {drug}\n    {why}")


if __name__ == "__main__":
    main()
