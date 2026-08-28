"""Pull the exon/intron structure of one gene from Ensembl (GRCh38) so variants
can be classified by their position relative to splice sites without waiting on
a full VEP cache."""
from __future__ import annotations

import json
import sys
import urllib.request

SERVER = "https://rest.ensembl.org"


def canonical_transcript(symbol: str) -> dict:
    url = f"{SERVER}/lookup/symbol/homo_sapiens/{symbol}?expand=1"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        gene = json.load(r)
    tx = [t for t in gene["Transcript"] if t.get("is_canonical")] or gene["Transcript"]
    return gene, tx[0]


def main(symbol: str) -> None:
    gene, tx = canonical_transcript(symbol)
    print(f"# {symbol} {gene['id']} chr{gene['seq_region_name']}:{gene['start']}-{gene['end']} "
          f"strand={gene['strand']}")
    print(f"# canonical transcript {tx['id']} ({tx.get('display_name')}) "
          f"biotype={tx['biotype']} exons={len(tx['Exon'])}")
    exons = sorted(tx["Exon"], key=lambda e: e["start"])
    print("exon_index\tstart\tend\tlength")
    for i, e in enumerate(exons, 1):
        idx = i if gene["strand"] == 1 else len(exons) - i + 1
        print(f"{idx}\t{e['start']}\t{e['end']}\t{e['end'] - e['start'] + 1}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "BUB1B")
