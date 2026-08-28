"""Mechanism-anchored candidates: drugs reachable from the MVA genes themselves.

TxGNN ranks the whole drug set and its explanations detour through phenotype and
metabolism hubs, because MVA's own genes carry no drug edges. This asks the
narrower question the graph *can* answer honestly:

    starting from BUB1B, BUB1, BUB3, CEP57 and TRIP13, which drugs are reachable
    through one protein-protein interaction?

That is a mechanism-anchored candidate list rather than a phenotype-similarity
one. Every hit comes with the interactor it came through, so the claim it makes
is inspectable: "this drug targets a protein that physically interacts with a
protein the disease disrupts."

It is deliberately not a ranking. It is a reachability set, and its size is
itself the finding.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict

MVA_GENES = {"BUB1B", "BUB1", "BUB3", "CEP57", "TRIP13"}
# Inhibiting these makes the lesion worse; flagged rather than dropped.
CONTRAINDICATED_TARGETS = {"AURKA", "AURKB", "PLK1", "TTK", "CENPE", "KIF11",
                           "BUB1", "BUB1B", "MAD2L1", "CDC20"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kg", default="/mnt/data/mva-hackathon-2026/txgnn-data/kg.csv")
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/txgnn/"
                                     "mechanism_anchored.tsv")
    args = ap.parse_args()

    ppi = defaultdict(set)      # protein -> interacting proteins
    drugs_of = defaultdict(set)  # protein -> {(relation, drug)}

    with open(args.kg, newline="") as fh:
        for row in csv.DictReader(fh):
            xt, yt = row["x_type"], row["y_type"]
            xn, yn, rel = row["x_name"], row["y_name"], row["relation"]
            if xt == "gene/protein" and yt == "gene/protein":
                ppi[xn].add(yn)
                ppi[yn].add(xn)
            elif xt == "gene/protein" and yt == "drug":
                drugs_of[xn].add((rel, yn))
            elif yt == "gene/protein" and xt == "drug":
                drugs_of[yn].add((rel, xn))

    print(f"{len(ppi):,} proteins with interactions; "
          f"{len(drugs_of):,} proteins with drug edges\n")

    rows = []
    for gene in sorted(MVA_GENES):
        partners = ppi.get(gene, set())
        hits = [(p, rel, d) for p in sorted(partners) for rel, d in sorted(drugs_of.get(p, ()))]
        print(f"{gene}: {len(partners)} interactors, "
              f"{len({d for _, _, d in hits})} reachable drugs")
        for p, rel, d in hits:
            rows.append((gene, p, rel, d, "CONTRAINDICATED" if p in CONTRAINDICATED_TARGETS else ""))

    with open(args.out, "w") as fh:
        fh.write("mva_gene\tinteractor\trelation\tdrug\tflag\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    by_drug = defaultdict(set)
    for gene, p, _rel, d, flag in rows:
        by_drug[d].add((gene, p, flag))
    print(f"\n{len(by_drug)} distinct drugs reachable in two hops from the MVA genes")
    print("\nmost-connected reachable drugs:")
    for d, srcs in sorted(by_drug.items(), key=lambda kv: -len(kv[1]))[:25]:
        flags = "  [!] targets a checkpoint protein" if any(f for _, _, f in srcs) else ""
        via = ", ".join(sorted({f"{g}-{p}" for g, p, _ in srcs})[:4])
        print(f"  {d:34.34s} via {via}{flags}")
    print(f"\nwrote {args.out} ({len(rows)} gene-interactor-drug rows)")


if __name__ == "__main__":
    main()
