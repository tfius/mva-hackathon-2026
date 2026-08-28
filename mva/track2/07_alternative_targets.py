"""If BubR1 itself is undrugged, what protein *adjacent* to it is druggable?

The report established that BUB1B carries no drug edge in either PrimeKG or
OptimusKG, and that the druggable checkpoint proteins are the contraindicated
ones. That was treated as the end of the line. It is not.

The mechanism says BubR1 abundance is set by acetylation at K668 - written by
CBP/p300, erased by SIRT2. Two consequences neither knowledge graph can reach,
because both require knowing the *direction* of an effect rather than the
existence of an edge:

  * If acetylation at K668 destabilises BubR1, then inhibiting the writer
    (CREBBP / EP300) should RAISE BubR1. Those are druggable proteins with
    clinical-stage inhibitors. This is the target-level version of the NAD+
    hypothesis, and it is reachable in the graph as a protein - only the
    direction of benefit is missing.
  * Raising NAD+ can be done at a protein target rather than by supplementation:
    NAMPT is the rate-limiting enzyme of the salvage pathway and has activators.

And a third route nothing in this project has yet addressed: the *other* allele.
p.Leu737Ter is a premature termination codon, and PTC readthrough is a druggable
mechanism with existing agents.

This asks the graphs what ligands exist for each of those proteins.
"""
from __future__ import annotations

import json


def _fix_user_agent() -> None:
    import requests
    original = requests.sessions.Session.request
    def request(self, method, url, **kwargs):
        h = kwargs.setdefault("headers", {}) or {}
        h.setdefault("User-Agent", "curl/8.5.0")
        kwargs["headers"] = h
        return original(self, method, url, **kwargs)
    requests.sessions.Session.request = request


TARGETS = {
    "CREBBP":  ("ENSG00000005339", "writes the K668 acetyl mark - inhibit to RAISE BubR1"),
    "EP300":   ("ENSG00000100393", "writes the K668 acetyl mark - inhibit to RAISE BubR1"),
    "SIRT2":   ("ENSG00000068903", "erases it - would need an ACTIVATOR, wrong direction available"),
    "NAMPT":   ("ENSG00000105835", "rate-limiting for NAD+ salvage - activators exist"),
    "NMNAT1":  ("ENSG00000173614", "NAD+ synthesis"),
    "FZR1":    ("ENSG00000105325", "APC/C-Cdh1 adaptor, degrades BubR1"),
    "HSP90AA1":("ENSG00000080824", "chaperone; note 17-AAG INHIBITS it - wrong way for a fold-defective client"),
    "SMG1":    ("ENSG00000157106", "NMD kinase - inhibit to spare the nonsense transcript for readthrough"),
    "UPF1":    ("ENSG00000005007", "NMD core"),
}


def main() -> None:
    _fix_user_agent()
    import optimuskg

    nodes, edges = optimuskg.load_graph()
    label, name = {}, {}
    for nid, lab, props in nodes.iter_rows():
        label[nid] = lab
        d = json.loads(props) if props else {}
        nm = d.get("name") or d.get("symbol")
        if nm:
            name[nid] = nm

    want = {ens: sym for sym, (ens, _) in TARGETS.items()}
    found = {sym: [] for sym in TARGETS}
    for frm, to, _l, rel, _u, _p in edges.iter_rows():
        if frm in want and label.get(to) == "DRG":
            found[want[frm]].append((rel, name.get(to, to)))
        elif to in want and label.get(frm) == "DRG":
            found[want[to]].append((rel, name.get(frm, frm)))

    for sym, (ens, why) in TARGETS.items():
        hits = sorted({d for _, d in found[sym]})
        present = "" if ens in label else "  (NOT IN GRAPH)"
        print(f"\n{sym}{present} — {why}")
        print(f"  {len(hits)} drug edge(s)" + (": " + ", ".join(hits[:12]) if hits else " — none"))


if __name__ == "__main__":
    main()
