"""Zero-shot drug repurposing for mosaic variegated aneuploidy with TxGNN.

MVA is the case TxGNN was built for. In PrimeKG its disease node carries 214
phenotype edges, 10 disease-protein edges (BUB1, BUB1B, BUB3, CEP57, TRIP13)
and 6 disease-disease edges - and **zero drug edges of any kind**. There is
nothing to memorise, so any ranking the model produces is genuine zero-shot
inference over the graph neighbourhood rather than recall.

Runs on CPU. The graph is 129k nodes / 8M edges, which is small enough that the
absence of a DGL build for this GPU costs only wall-clock, not feasibility.

Outputs a ranked table for both `indication` and `contraindication`. The
contraindication direction is not an afterthought here: a weakened spindle
assembly checkpoint is the lesion, so checkpoint-weakening agents (MPS1/TTK,
Aurora B, KIF11, PLK1) should surface on that side. That is a falsifiable
prediction about the model, stated before the run.
"""
from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path

import pandas as pd

# PrimeKG node id for "mosaic variegated aneuploidy syndrome" (node_index 28004),
# a MONDO_grouped node over MONDO ids 13582, 9759, 54736 and 141.
MVA_NODE_ID = "13582_9759_54736_141"


def find_disease_idx(df: pd.DataFrame, node_id: str) -> float:
    hits = df[(df.x_type == "disease") & (df.x_id.astype(str) == node_id)]
    if hits.empty:
        hits = df[(df.y_type == "disease") & (df.y_id.astype(str) == node_id)]
        if hits.empty:
            raise SystemExit(f"disease node {node_id!r} not found in the split")
        return float(hits.iloc[0].y_idx)
    return float(hits.iloc[0].x_idx)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="/mnt/data/mva-hackathon-2026/txgnn-data")
    ap.add_argument("--ckpt", default="/mnt/data/mva-hackathon-2026/txgnn-ckpt/TxGNNExplorer")
    ap.add_argument("--out", default="/mnt/data/mva-hackathon-2026/work/txgnn")
    ap.add_argument("--node-id", default=MVA_NODE_ID)
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    from txgnn import TxData, TxEval, TxGNN

    print("loading PrimeKG ...", flush=True)
    data = TxData(data_folder_path=args.data)
    # The released checkpoint is full_graph split 1; matching it keeps node
    # indices aligned with the pretrained weights and the GraphMask gates.
    data.prepare_split(split="full_graph", seed=1)

    print("loading pretrained TxGNN ...", flush=True)
    model = TxGNN(data=data, weight_bias_track=False, proj_name="mva", exp_name="mva", device="cpu")
    model.load_pretrained(args.ckpt)
    model.best_model = model.model

    disease_idx = find_disease_idx(data.df, args.node_id)
    print(f"disease idx for {args.node_id}: {disease_idx}", flush=True)

    name_map = pickle.load(open(Path(args.ckpt) / "name_mapping.pkl", "rb"))
    id2name_drug = name_map.get("id2name_drug", {})

    evaluator = TxEval(model=model)
    for relation in ("indication", "contraindication"):
        print(f"\n=== {relation} ===", flush=True)
        res = evaluator.eval_disease_centric(
            disease_idxs=[disease_idx],
            relation=relation,
            save_result=False,
            verbose=False,
            return_raw=True,
        )
        with open(outdir / f"raw_{relation}.pkl", "wb") as fh:
            pickle.dump(res, fh)
        print(f"  raw result type {type(res)}; keys "
              f"{list(res)[:5] if hasattr(res, '__iter__') else res}", flush=True)

    print("\nid2name_drug entries:", len(id2name_drug), file=sys.stderr)


if __name__ == "__main__":
    main()
