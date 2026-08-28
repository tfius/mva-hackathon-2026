"""Graph-backed rationales for TxGNN's MVA predictions, from the GraphMask gates.

TxGNN Explain trains a GraphMask model that assigns every edge in PrimeKG an
importance for the `indication` task. The released Explorer bundle ships those
gates as a 7,695,474-row edge table with a per-layer attention value, but its
precomputed `paths.csv` covers only a curated demo set - mosaic variegated
aneuploidy is not in it. So the paths are reconstructed here.

Method. Edge importance is the mean of the two layer gates. Paths are found by
bidirectional beam search: two hops out from the disease, two hops out from the
drug, joined at the meeting node, giving meta-paths of up to four hops - the
same shape TxGNN's own explanations take. A path scores as the product of its
edge importances, normalised for length so a short strong path is not beaten by
a long weak one.

A beam is necessary rather than merely convenient: the MVA node has 214
phenotype edges and those phenotypes touch thousands of diseases each, so an
exhaustive search is exponential and mostly noise. The beam keeps the highest
importance frontier at each step, which is the point of having gates at all.

**Gate importance alone produces hub artefacts, and they have to be excluded
explicitly.** Run on raw gates, every top path for every drug went

    MVA <- Colon cancer -> Pimecrolimus <- CYP3A4 -> <drug>

with near-identical scores for chemically unrelated drugs - 0.5159 for
dasatinib, 0.5152 for hydroxychloroquine, 0.5074 for paclitaxel. That is a
statement about shared hepatic metabolism, not about why any of them might help,
and its drug-independence is the giveaway. Two corrections:

  * `drug_effect` edges are side effects. Reaching a candidate through one is
    not a therapeutic rationale, so they are excluded.
  * Intermediate nodes are down-weighted by 1/log10(degree). CYP3A4, ABCG2 and
    ALB connect to a large fraction of the drug set and explain nothing about
    any particular one; a specific protein carries far more information.

`--raw-gates` reproduces the unweighted version for comparison.
"""
from __future__ import annotations

import argparse
import math
import pickle
from collections import defaultdict
from pathlib import Path

DISEASE_NAME = "mosaic variegated aneuploidy syndrome"

# Drug-metabolism and transport proteins. Almost every drug touches these, so a
# path through one carries essentially no information about which drug it
# arrived at - the standard ADME-hub exclusion in network pharmacology. Down-
# weighting by degree alone is not enough: CYP3A4 still wins on gate value.
ADME_PREFIXES = ("CYP", "ABC", "SLC", "UGT", "SULT", "NAT", "GST", "FMO", "AOX")
ADME_EXACT = {"ALB", "AHR", "NR1I2", "NR1I3", "ORM1", "ORM2", "SERPINA6"}


def is_adme(node_type: str, name: str) -> bool:
    return node_type == "gene/protein" and (
        name in ADME_EXACT or any(name.startswith(p) for p in ADME_PREFIXES)
    )


def load_edges(path: str):
    import pandas as pd
    df = pickle.load(open(path, "rb"))
    df["imp"] = (df["indication_layer1_att"] + df["indication_layer2_att"]) / 2.0
    return df


def node_degrees(df):
    from collections import Counter
    deg = Counter()
    for xt, xi, yt, yi in df[["x_type", "x_idx", "y_type", "y_idx"]].itertuples(index=False):
        deg[(xt, xi)] += 1
        deg[(yt, yi)] += 1
    return deg


def build_adjacency(df, drop_adme=True):
    """Undirected adjacency keyed by (type, idx); the relation label and its
    direction are kept on the edge so the rendered path stays readable."""
    adj = defaultdict(list)
    adme = set()
    if drop_adme:
        for t, i, n in df[["x_type", "x_idx", "x_name"]].itertuples(index=False):
            if is_adme(t, n):
                adme.add((t, i))
        for t, i, n in df[["y_type", "y_idx", "y_name"]].itertuples(index=False):
            if is_adme(t, n):
                adme.add((t, i))
        print(f"  excluding {len(adme):,} ADME hub proteins", flush=True)
    cols = ["x_type", "x_idx", "x_name", "y_type", "y_idx", "y_name", "relation", "imp"]
    for xt, xi, xn, yt, yi, yn, rel, imp in df[cols].itertuples(index=False):
        a, b = (xt, xi), (yt, yi)
        if a in adme or b in adme:
            continue
        adj[a].append((b, rel, float(imp), yn, True))
        adj[b].append((a, rel, float(imp), xn, False))
    return adj


def beam_expand(adj, start, start_name, hops, beam, banned_types=(),
                banned_rels=(), deg=None):
    """Return {node: (score, path)} where path is a list of (relation, forward,
    node, node_name, edge_importance)."""
    frontier = {start: (1.0, [])}
    seen = {start: (1.0, [])}
    for _ in range(hops):
        nxt = {}
        for node, (score, path) in frontier.items():
            for nb, rel, imp, nb_name, forward in adj.get(node, ()):
                if nb[0] in banned_types:
                    continue
                if any(b in rel for b in banned_rels):
                    continue
                w = imp
                if deg is not None:
                    # Penalise hubs: a path through CYP3A4 says almost nothing
                    # about which drug it arrived at.
                    w = imp / max(1.0, math.log10(deg.get(nb, 1) + 10))
                s = score * w
                if nb in nxt and nxt[nb][0] >= s:
                    continue
                nxt[nb] = (s, path + [(rel, forward, nb, nb_name, imp)])
        frontier = dict(sorted(nxt.items(), key=lambda kv: -kv[1][0])[:beam])
        for k, v in frontier.items():
            if k not in seen or seen[k][0] < v[0]:
                seen[k] = v
    return seen


def render(disease_name, drug_name, fwd_path, bwd_path):
    """Walk disease -> ... -> meeting node -> ... -> drug.

    The backward half is stored as it was explored, drug outwards, so each step
    there carries the node it *arrived at*. Rendering it in reverse means
    pairing step k's relation with step k-1's node, and the drug itself for the
    last one - otherwise the meeting node prints twice and the drug never does.
    """
    parts = [disease_name]
    for rel, forward, _node, name, _imp in fwd_path:
        parts += [f"-[{rel}]->" if forward else f"<-[{rel}]-", name]
    for k in range(len(bwd_path) - 1, -1, -1):
        rel, forward, _node, _name, _imp = bwd_path[k]
        parts += [f"<-[{rel}]-" if forward else f"-[{rel}]->",
                  bwd_path[k - 1][3] if k - 1 >= 0 else drug_name]
    return " ".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gates",
                    default="/mnt/data/mva-hackathon-2026/txgnn-ckpt/TxGNNExplorer/"
                            "graphmask_output_indication.pkl")
    ap.add_argument("--drugs", nargs="+", required=True,
                    help="drug names as they appear in PrimeKG")
    ap.add_argument("--disease", default=DISEASE_NAME)
    ap.add_argument("--beam", type=int, default=3000)
    ap.add_argument("--require-gene", action="store_true", default=True,
                    help="keep only paths that pass through a gene/protein node")
    ap.add_argument("--allow-any-path", dest="require_gene", action="store_false")
    ap.add_argument("--raw-gates", action="store_true",
                    help="no hub down-weighting and no side-effect exclusion, "
                         "to reproduce what unmodified GraphMask importance gives")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/txgnn/explanations.tsv")
    args = ap.parse_args()

    print("loading GraphMask gates ...", flush=True)
    df = load_edges(args.gates)
    print(f"  {len(df):,} gated edges", flush=True)

    def node_of(name, types):
        for side in ("x", "y"):
            hit = df[(df[f"{side}_name"] == name) & (df[f"{side}_type"].isin(types))]
            if len(hit):
                r = hit.iloc[0]
                return (r[f"{side}_type"], r[f"{side}_idx"])
        return None

    disease = node_of(args.disease, ["disease"])
    if disease is None:
        raise SystemExit(f"disease {args.disease!r} not in the gate table")
    print(f"  disease node {disease}", flush=True)

    print("building adjacency ...", flush=True)
    adj = build_adjacency(df, drop_adme=not args.raw_gates)
    print(f"  {len(adj):,} nodes", flush=True)

    # Two hops from the disease. Anatomy and exposure nodes are hubs that connect
    # everything to everything and explain nothing, so they are kept out.
    # Anatomy and exposure nodes are hubs that connect everything to everything
    # and explain nothing.
    banned = ("anatomy", "exposure")
    banned_rels = () if args.raw_gates else ("drug_effect",)
    deg = None if args.raw_gates else node_degrees(df)
    fwd = beam_expand(adj, disease, args.disease, 2, args.beam, banned, banned_rels, deg)
    print(f"  {len(fwd):,} nodes within two hops of the disease", flush=True)

    rows = []
    for drug_name in args.drugs:
        drug = node_of(drug_name, ["drug"])
        if drug is None:
            print(f"  ! {drug_name}: not in the gate table")
            continue
        bwd = beam_expand(adj, drug, drug_name, 2, args.beam, banned, banned_rels, deg)
        meet = set(fwd) & set(bwd)
        cand = []
        for m in meet:
            fs, fp = fwd[m]
            bs, bp = bwd[m]
            hops = len(fp) + len(bp)
            if hops == 0:
                continue
            rels = [step[0] for step in fp + bp]
            # drug_drug edges are similarity and interaction links. A path that
            # reaches the candidate through one explains nothing about why the
            # candidate should work.
            if any("drug_drug" in r for r in rels):
                continue
            if args.require_gene and not any(
                step[2][0] == "gene/protein" for step in fp + bp
            ):
                continue
            score = (fs * bs) ** (1.0 / hops)   # length-normalised
            cand.append((score, fp, bp))
        cand.sort(key=lambda t: -t[0])
        print(f"\n### {drug_name}  ({len(meet):,} meeting nodes)")
        for score, fp, bp in cand[: args.top]:
            path = render(args.disease, drug_name, fp, bp)
            print(f"  {score:.4f}  {path}")
            rows.append((drug_name, f"{score:.6f}", str(len(fp) + len(bp)), path))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as fh:
        fh.write("drug\tpath_score\thops\tpath\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    print(f"\nwrote {out} ({len(rows)} paths)")


if __name__ == "__main__":
    main()
