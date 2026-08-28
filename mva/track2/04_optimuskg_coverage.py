"""Does OptimusKG cover what PrimeKG could not?

Two concrete gaps were found in PrimeKG while working this case, and both are
the reason the TxGNN layer could not do what it was asked to do:

1. **BUB1B has 464 edges and not one of them is a drug edge.** Neither do BUB1,
   BUB3, CEP57, TRIP13, CDC20 or MAD2L1 - every gene the MVA disease node
   connects to. So no path `MVA -> BUB1B -> drug` exists at all, and every
   explanation TxGNN can produce has to detour through a hub. The only spindle
   checkpoint proteins that *are* druggable in PrimeKG are AURKB, PLK1, TTK and
   CENPE - which is to say, exactly the ones that must not be inhibited here.
2. **The NAD+ precursors are absent from the clinically annotated drug set.**
   Nicotinamide riboside, nicotinamide mononucleotide and NADH carry no
   indication edges, so the best-supported hypothesis in the report is invisible.

OptimusKG is newer and roughly five times larger: 192,813 nodes, 21,834,669
edges, 145 property keys over 65 resources. This asks whether either gap closes,
which is the only interesting question about swapping the graph.
"""
from __future__ import annotations

import argparse

MVA_GENES = ["BUB1B", "BUB1", "BUB3", "CEP57", "TRIP13"]
CHECKPOINT_DRUGGABLE = ["AURKB", "PLK1", "TTK", "CENPE"]
NAD_PRECURSORS = [
    "nicotinamide riboside", "nicotinamide mononucleotide", "NADH",
    "nicotinamide", "niacin", "nicotinic acid",
]
PROBE_DRUGS = ["dasatinib", "quercetin", "chloroquine", "hydroxychloroquine",
               "metformin", "tanespimycin", "navitoclax", "fisetin", "acadesine"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/optimuskg")
    args = ap.parse_args()

    import optimuskg
    import polars as pl
    from pathlib import Path

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print("loading OptimusKG nodes and edges ...", flush=True)
    nodes, edges = optimuskg.load_graph()
    print(f"  nodes {nodes.shape}  edges {edges.shape}", flush=True)
    print("  node columns:", nodes.columns, flush=True)
    print("  edge columns:", edges.columns, flush=True)

    ncol = "name" if "name" in nodes.columns else nodes.columns[1]
    tcol = "category" if "category" in nodes.columns else nodes.columns[2]
    print("\nnode categories:", flush=True)
    print(nodes.group_by(tcol).len().sort("len", descending=True).head(20))

    def find(term: str):
        return nodes.filter(pl.col(ncol).str.to_lowercase() == term.lower())

    print("\n--- gene coverage")
    for g in MVA_GENES + CHECKPOINT_DRUGGABLE:
        hit = find(g)
        print(f"  {g:8s} {len(hit)} node(s)")

    print("\n--- NAD+ precursor coverage (the PrimeKG gap)")
    for d in NAD_PRECURSORS:
        hit = find(d)
        print(f"  {d:32s} {len(hit)} node(s)")

    print("\n--- probe drug coverage")
    for d in PROBE_DRUGS:
        print(f"  {d:20s} {len(find(d))} node(s)")

    nodes.write_parquet(out / "nodes.parquet")
    print(f"\nwrote {out}/nodes.parquet for follow-up queries")


if __name__ == "__main__":
    main()
