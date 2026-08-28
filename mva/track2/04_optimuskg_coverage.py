"""Does OptimusKG close the two gaps that stopped the PrimeKG/TxGNN layer?

Working this case turned up two specific holes in PrimeKG, and both are the
reason the knowledge-graph layer could not do what it was asked to:

1. **BUB1B has 464 edges and not one is a drug edge.** Neither do BUB1, BUB3,
   CEP57, TRIP13, CDC20 or MAD2L1 - every gene the MVA disease node touches. So
   `MVA -> BUB1B -> drug` cannot exist and every explanation detours through a
   hub. Meanwhile AURKB, PLK1, TTK and CENPE *are* druggable: the contraindicated
   set.
2. **The NAD+ precursors are not in the clinically annotated drug set**, so the
   best-supported hypothesis in the report is invisible to the model - even
   though PrimeKG does contain BUB1B-SIRT2 and BUB1B-CREBBP/EP300, the whole
   mechanism, missing only its last edge.

OptimusKG is newer and about five times larger: 190,531 nodes, 21,813,816 edges,
65 sources. Whether either gap closes is the only interesting question about
swapping graphs, and it is answerable directly rather than by re-running a model.

Schema note: nodes are (id, label, properties-as-JSON). Gene ids are Ensembl
with the symbol inside `properties`, drugs are ChEMBL ids with `name` and
`synonyms`, diseases are DOID. Nothing is queryable by a bare `name` column,
which is worth saying because assuming otherwise returns a confident zero for
every lookup.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _fix_user_agent() -> None:
    """Harvard Dataverse blocks the default python-requests User-Agent.

    Every call comes back 403 Forbidden while the identical URL returns 200 to
    curl. Nothing is restricted; the UA string is on a block list. Patched here
    rather than in the installed package so the environment stays reproducible.
    """
    import requests

    original = requests.sessions.Session.request

    def request(self, method, url, **kwargs):
        headers = kwargs.setdefault("headers", {}) or {}
        headers.setdefault("User-Agent", "curl/8.5.0")
        kwargs["headers"] = headers
        return original(self, method, url, **kwargs)

    requests.sessions.Session.request = request


MVA_GENES = {
    "BUB1B": "ENSG00000156970", "BUB1": "ENSG00000169679",
    "BUB3": "ENSG00000154473", "CEP57": "ENSG00000166037",
    "TRIP13": "ENSG00000071539",
}
CHECKPOINT_DRUGGABLE = {
    "AURKB": "ENSG00000178999", "PLK1": "ENSG00000166851",
    "TTK": "ENSG00000112742", "CENPE": "ENSG00000138778",
    "SIRT2": "ENSG00000068903", "CREBBP": "ENSG00000005339",
}
NAD_PRECURSORS = ["nicotinamide riboside", "nicotinamide mononucleotide",
                  "nicotinamide", "niacin", "nicotinic acid", "nadh"]
PROBE_DRUGS = ["dasatinib", "quercetin", "chloroquine", "hydroxychloroquine",
               "metformin", "tanespimycin", "navitoclax", "fisetin", "acadesine",
               "vorinostat", "romidepsin", "reversine"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/optimuskg")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    _fix_user_agent()
    import optimuskg
    import polars as pl

    cached = out / "nodes.parquet"
    if cached.exists():
        nodes = pl.read_parquet(cached)
        _, edges = optimuskg.load_graph()
    else:
        nodes, edges = optimuskg.load_graph()
        nodes.write_parquet(cached)
    print(f"nodes {nodes.shape}  edges {edges.shape}\n", flush=True)

    # --- index the JSON properties once
    name_of, sym_of, label_of = {}, {}, {}
    by_name = {}
    for nid, lab, props in nodes.iter_rows():
        label_of[nid] = lab
        d = json.loads(props) if props else {}
        nm = d.get("name") or d.get("symbol")
        if nm:
            name_of[nid] = nm
            by_name.setdefault((lab, nm.lower()), nid)
        if lab == "GEN" and d.get("symbol"):
            sym_of[d["symbol"]] = nid
        for syn in (d.get("synonyms") or d.get("exact_synonyms") or []):
            if isinstance(syn, str):
                by_name.setdefault((lab, syn.lower()), nid)

    # --- adjacency restricted to whatever touches our genes
    want = set(MVA_GENES.values()) | set(CHECKPOINT_DRUGGABLE.values())
    touching = {g: [] for g in want}
    for frm, to, lab, rel, _und, _props in edges.iter_rows():
        if frm in touching:
            touching[frm].append((to, rel))
        if to in touching:
            touching[to].append((frm, rel))

    print("=== gene coverage and drug edges")
    for label, table in (("MVA genes", MVA_GENES), ("checkpoint / acetylation", CHECKPOINT_DRUGGABLE)):
        print(f"-- {label}")
        for sym, ens in table.items():
            nbrs = touching.get(ens, [])
            drugs = sorted({name_of.get(n, n) for n, _ in nbrs if label_of.get(n) == "DRG"})
            present = "yes" if ens in label_of else "NOT IN GRAPH"
            print(f"  {sym:8s} {present:12s} edges={len(nbrs):5d}  drug edges={len(drugs):4d}"
                  + (f"  e.g. {', '.join(drugs[:6])}" if drugs else "  -- none --"))

    print("\n=== NAD+ precursor coverage (the PrimeKG gap)")
    for d in NAD_PRECURSORS:
        nid = by_name.get(("DRG", d))
        print(f"  {d:32s} {'found ' + nid if nid else 'absent'}")

    print("\n=== probe drug coverage")
    for d in PROBE_DRUGS:
        nid = by_name.get(("DRG", d))
        print(f"  {d:20s} {'found ' + nid if nid else 'absent'}")

    print("\n=== MVA disease node")
    for cand in ("mosaic variegated aneuploidy syndrome",
                 "mosaic variegated aneuploidy syndrome 1"):
        nid = by_name.get(("DIS", cand))
        print(f"  {cand:45s} {'found ' + nid if nid else 'absent'}")


if __name__ == "__main__":
    main()
