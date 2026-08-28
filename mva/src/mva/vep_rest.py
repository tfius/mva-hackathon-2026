"""Annotate a handful of variants through the Ensembl VEP REST endpoint.

Used for targeted locus work while the full offline VEP cache downloads. Not a
substitute for the offline run - it is rate limited and only sensible for tens
of variants.
"""
from __future__ import annotations

import json
import sys
import urllib.request

SERVER = "https://rest.ensembl.org"


def vep(hgvs_like: list[str], species: str = "human") -> list[dict]:
    req = urllib.request.Request(
        f"{SERVER}/vep/{species}/region",
        data=json.dumps(
            {
                "variants": hgvs_like,
                "canonical": 1,
                "hgvs": 1,
                "numbers": 1,
                "domains": 1,
                "af": 1,
                "af_gnomadg": 1,
                "AlphaMissense": 1,
                "SpliceAI": 1,
                "mane": 1,
            }
        ).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def main() -> None:
    # stdin: "chrom pos ref alt" per line, chrom without the chr prefix
    variants = []
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        c, p, ref, alt = line.split()[:4]
        variants.append(f"{c} {p} . {ref} {alt} . . .")

    for res in vep(variants):
        print(f"\n### {res.get('input')}  {res.get('most_severe_consequence')}")
        for k in ("colocated_variants",):
            for cv in res.get(k, []) or []:
                freqs = cv.get("frequencies", {})
                print(f"  known: {cv.get('id')} freq={json.dumps(freqs)[:200]}")
        for tc in res.get("transcript_consequences", []) or []:
            if not (tc.get("canonical") or tc.get("mane_select")):
                continue
            bits = [
                tc.get("gene_symbol"),
                tc.get("transcript_id"),
                ",".join(tc.get("consequence_terms", [])),
                tc.get("hgvsc"),
                tc.get("hgvsp"),
                f"exon={tc.get('exon')}" if tc.get("exon") else None,
                f"intron={tc.get('intron')}" if tc.get("intron") else None,
                f"am={tc.get('alphamissense', {}).get('am_pathogenicity')}"
                if tc.get("alphamissense") else None,
            ]
            print("  " + " | ".join(str(b) for b in bits if b))
        if res.get("spliceai"):
            print(f"  spliceai: {json.dumps(res['spliceai'])[:300]}")


if __name__ == "__main__":
    main()
