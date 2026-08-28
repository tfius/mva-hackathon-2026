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
"""
from __future__ import annotations

import argparse
import pickle
from collections import defaultdict
from pathlib import Path

DISEASE_NAME = "mosaic variegated aneuploidy syndrome"


def load_edges(path: str):
    import pandas as pd
    df = pickle.load(open(path, "rb"))
    df["imp"] = (df["indication_layer1_att"] + df["indication_layer2_att"]) / 2.0
    return df


def build_adjacency(df):
    """Undirected adjacency keyed by (type, idx); the relation label and its
    direction are kept on the edge so the rendered path stays readable."""
    adj = defaultdict(list)
    cols = ["x_type", "x_idx", "x_name", "y_type", "y_idx", "y_name", "relation", "imp"]
    for xt, xi, xn, yt, yi, yn, rel, imp in df[cols].itertuples(index=False):
        a, b = (xt, xi), (yt, yi)
        adj[a].append((b, rel, float(imp), yn, True))
        adj[b].append((a, rel, float(imp), xn, False))
    return adj


def beam_expand(adj, start, start_name, hops, beam, banned_types=()):
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
                s = score * imp
                if nb in nxt and nxt[nb][0] >= s:
                    continue
                nxt[nb] = (s, path + [(rel, forward, nb, nb_name, imp)])
        frontier = dict(sorted(nxt.items(), key=lambda kv: -kv[1][0])[:beam])
        for k, v in frontier.items():
            if k not in seen or seen[k][0] < v[0]:
                seen[k] = v
    return seen


def render(disease_name, drug_name, fwd_path, bwd_path):
    parts = [disease_name]
    for rel, forward, _node, name, _imp in fwd_path:
        parts += [f"-[{rel}]->" if forward else f"<-[{rel}]-", name]
    for rel, forward, _node, name, _imp in reversed(bwd_path):
        parts += [f"<-[{rel}]-" if forward else f"-[{rel}]->", name]
    parts.append(drug_name) if parts[-1] != drug_name else None
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
    adj = build_adjacency(df)
    print(f"  {len(adj):,} nodes", flush=True)

    # Two hops from the disease. Anatomy and exposure nodes are hubs that connect
    # everything to everything and explain nothing, so they are kept out.
    banned = ("anatomy", "exposure")
    fwd = beam_expand(adj, disease, args.disease, 2, args.beam, banned)
    print(f"  {len(fwd):,} nodes within two hops of the disease", flush=True)

    rows = []
    for drug_name in args.drugs:
        drug = node_of(drug_name, ["drug"])
        if drug is None:
            print(f"  ! {drug_name}: not in the gate table")
            continue
        bwd = beam_expand(adj, drug, drug_name, 2, args.beam, banned)
        meet = set(fwd) & set(bwd)
        cand = []
        for m in meet:
            fs, fp = fwd[m]
            bs, bp = bwd[m]
            hops = len(fp) + len(bp)
            if hops == 0:
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
