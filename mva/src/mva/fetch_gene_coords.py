"""Resolve panel gene symbols to GRCh38 coordinates via the Ensembl REST API.

Writes a BED file (chr-prefixed, with a configurable flank) plus a TSV of the
raw lookups. Run once; the output is committed so the pipeline is reproducible
without network access.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

from panels import ALL_GENES, PANELS

SERVER = "https://rest.ensembl.org"
FLANK = 50_000  # MVA1's second allele is often non-coding; look well past the CDS.


def lookup(symbols: list[str]) -> dict:
    out = {}
    for i in range(0, len(symbols), 50):
        chunk = symbols[i : i + 50]
        req = urllib.request.Request(
            f"{SERVER}/lookup/symbol/homo_sapiens",
            data=json.dumps({"symbols": chunk}).encode(),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            out.update(json.load(r))
        print(f"  resolved {len(out)}/{len(symbols)}", file=sys.stderr)
    return out


def main(outdir: str = ".") -> None:
    outdir = Path(outdir)
    data = lookup(ALL_GENES)

    panel_of = {}
    for name, genes in PANELS.items():
        for g in genes:
            panel_of.setdefault(g, []).append(name)

    rows, missing = [], []
    for sym in ALL_GENES:
        e = data.get(sym)
        if not e or "seq_region_name" not in e:
            missing.append(sym)
            continue
        chrom = e["seq_region_name"]
        if chrom not in [str(c) for c in range(1, 23)] + ["X", "Y", "MT"]:
            missing.append(sym)  # patch/scaffold placement, not usable
            continue
        rows.append(
            {
                "symbol": sym,
                "ensembl_id": e["id"],
                "chrom": f"chr{chrom}",
                "start": e["start"],
                "end": e["end"],
                "strand": e["strand"],
                "panels": ",".join(panel_of[sym]),
            }
        )

    (outdir / "gene_coords.tsv").write_text(
        "\t".join(rows[0].keys())
        + "\n"
        + "\n".join("\t".join(str(r[k]) for k in rows[0]) for r in rows)
        + "\n"
    )
    with (outdir / "panel_regions.bed").open("w") as fh:
        for r in sorted(rows, key=lambda r: (r["chrom"], r["start"])):
            fh.write(
                f"{r['chrom']}\t{max(0, r['start'] - FLANK)}\t{r['end'] + FLANK}\t"
                f"{r['symbol']}\t0\t{'+' if r['strand'] == 1 else '-'}\n"
            )

    print(f"resolved {len(rows)} genes; missing: {missing or 'none'}", file=sys.stderr)


if __name__ == "__main__":
    main(*sys.argv[1:])
