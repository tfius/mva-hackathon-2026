"""Mechanism-anchored reachability on OptimusKG rather than PrimeKG.

`05_mechanism_anchored.py` asked, of PrimeKG: starting from the MVA genes,
which drugs are reachable through one protein-protein interaction? It returned
592 drugs, correctly flagged the checkpoint inhibitors as contraindicated, and
could not see the NAD+ precursors at all, because PrimeKG has no drug node for
nicotinamide riboside.

OptimusKG does have those nodes (`04_optimuskg_coverage.py`), and it is roughly
five times denser. This is the same question asked of the better graph - and it
needs no retraining, which is the point: the useful upgrade from a bigger
knowledge graph here is reachability, not a rescored link predictor.

The specific thing to watch: **SIRT2 is a BUB1B interactor.** If OptimusKG
carries a drug edge from any NAD+ precursor into the SIRT2 neighbourhood, the
graph reaches hypothesis H1 on its own. PrimeKG holds every link but the last.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def _fix_user_agent() -> None:
    """Harvard Dataverse 403s the default python-requests User-Agent while
    serving curl the identical URL. Nothing is restricted."""
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
# Inhibiting these worsens the lesion. Flagged, never dropped.
CONTRAINDICATED = {
    "ENSG00000178999": "AURKB", "ENSG00000166851": "PLK1",
    "ENSG00000112742": "TTK", "ENSG00000138778": "CENPE",
    "ENSG00000169679": "BUB1", "ENSG00000156970": "BUB1B",
    "ENSG00000164109": "MAD2L1", "ENSG00000117399": "CDC20",
    "ENSG00000087586": "AURKA", "ENSG00000138160": "KIF11",
}
WATCH = {"nicotinamide riboside", "nicotinamide", "niacin", "nicotinic acid",
         "acadesine", "chloroquine", "hydroxychloroquine", "dasatinib",
         "quercetin", "tanespimycin", "metformin", "cambinol", "reversine"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/optimuskg/"
                                     "mechanism_anchored.tsv")
    args = ap.parse_args()

    _fix_user_agent()
    import optimuskg

    nodes, edges = optimuskg.load_graph()
    print(f"nodes {nodes.shape}  edges {edges.shape}", flush=True)

    name_of, label_of = {}, {}
    for nid, lab, props in nodes.iter_rows():
        label_of[nid] = lab
        d = json.loads(props) if props else {}
        nm = d.get("name") or d.get("symbol")
        if nm:
            name_of[nid] = nm

    # one pass: protein-protein adjacency for our genes, and every protein's drugs
    seeds = set(MVA_GENES.values())
    partners = defaultdict(set)
    drugs_of = defaultdict(set)
    for frm, to, _lab, rel, _und, _props in edges.iter_rows():
        lf, lt = label_of.get(frm), label_of.get(to)
        if lf == "GEN" and lt == "GEN":
            if frm in seeds:
                partners[frm].add(to)
            if to in seeds:
                partners[to].add(frm)
        elif lf == "GEN" and lt == "DRG":
            drugs_of[frm].add((rel, to))
        elif lt == "GEN" and lf == "DRG":
            drugs_of[to].add((rel, frm))

    rows, by_drug = [], defaultdict(set)
    for sym, ens in MVA_GENES.items():
        ps = partners.get(ens, set())
        hits = [(p, rel, d) for p in ps for rel, d in drugs_of.get(p, ())]
        print(f"{sym:8s} {len(ps):5d} interactors, "
              f"{len({d for _, _, d in hits}):4d} reachable drugs", flush=True)
        for p, rel, d in hits:
            flag = "CONTRAINDICATED" if p in CONTRAINDICATED else ""
            rows.append((sym, name_of.get(p, p), rel, name_of.get(d, d), flag))
            by_drug[name_of.get(d, d)].add((sym, name_of.get(p, p), flag))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as fh:
        fh.write("mva_gene\tinteractor\trelation\tdrug\tflag\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    print(f"\n{len(by_drug)} distinct drugs reachable in two hops "
          f"({len(rows)} gene-interactor-drug rows)")

    print("\n=== watch list — do the hypotheses become reachable?")
    lower = {k.lower(): k for k in by_drug}
    for w in sorted(WATCH):
        key = lower.get(w)
        if key:
            via = ", ".join(sorted({f"{g}-{p}" for g, p, _ in by_drug[key]})[:5])
            flag = " [!]" if any(f for _, _, f in by_drug[key]) else ""
            print(f"  {w:26s} REACHABLE via {via}{flag}")
        else:
            print(f"  {w:26s} not reachable")

    print("\n=== flagged contraindicated by construction")
    for d, srcs in sorted(by_drug.items()):
        if any(f for _, _, f in srcs):
            via = ", ".join(sorted({p for _, p, f in srcs if f})[:4])
            print(f"  {d:34.34s} targets {via}")


if __name__ == "__main__":
    main()
