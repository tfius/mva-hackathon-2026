"""Can either BUB1B allele be repaired by a base editor, and what would it break?

Track 2 lists "correct the null allele" as one of six routes to more BubR1.
That route is usually costed as a delivery problem, but it has a prior
constraint nobody checks first: base editors only make transition changes
(A->G, C->T), so half of all point mutations are simply out of reach, and the
guides that do reach a target drag bystander edits along with them.

This enumerates every SpCas9-family guide that could place the target base in
an editing window, and then scores every bystander edit each guide would risk
against the AlphaGenome Atlas - so the design is filtered by predicted damage
rather than by PAM availability alone.

Coordinates are GRCh38; BUB1B is on the + strand.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mva import atlas  # noqa: E402

SAMTOOLS = "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/samtools"
REF = "/mnt/data/mva-hackathon-2026/refs/GRCh38_no_alt.fa"
FLANK = 80

# (label, patient change, codon span on the + strand, what the edit must achieve)
TARGETS = [
    dict(name="Allele A  c.2210T>G  p.Leu737Ter", chrom="chr15", pos=40209701,
         ref="T", alt="G", codon=(40209700, 40209702)),
    dict(name="Allele B  c.3006T>G  p.Asn1002Lys", chrom="chr15", pos=40220612,
         ref="T", alt="G", codon=(40220610, 40220612)),
]

# Editor: name, base on the protospacer strand that is changed, and to what.
EDITORS = [("ABE (adenine)", "A", "G"), ("CBE (cytosine)", "C", "T")]
# Protospacer positions edited, 1-based from the PAM-distal end.
WINDOWS = {"canonical 4-8": (4, 8), "ABE8e wide 4-10": (4, 10)}
# PAM, as an IUPAC pattern 3' of the 20-mer, and the enzyme that reads it.
PAMS = [("NGG", "SpCas9"), ("NG", "SpCas9-NG / xCas9"), ("NNN", "SpRY (near-PAMless)")]
IUPAC = {"N": "ACGT", "R": "AG", "Y": "CT", "G": "G", "A": "A", "C": "C", "T": "T"}
CODONS = {
    "TTT": "Phe", "TTC": "Phe", "TTA": "Leu", "TTG": "Leu", "CTT": "Leu", "CTC": "Leu",
    "CTA": "Leu", "CTG": "Leu", "ATT": "Ile", "ATC": "Ile", "ATA": "Ile", "ATG": "Met",
    "GTT": "Val", "GTC": "Val", "GTA": "Val", "GTG": "Val", "TCT": "Ser", "TCC": "Ser",
    "TCA": "Ser", "TCG": "Ser", "CCT": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "ACT": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr", "GCT": "Ala", "GCC": "Ala",
    "GCA": "Ala", "GCG": "Ala", "TAT": "Tyr", "TAC": "Tyr", "TAA": "Ter", "TAG": "Ter",
    "CAT": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln", "AAT": "Asn", "AAC": "Asn",
    "AAA": "Lys", "AAG": "Lys", "GAT": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "TGT": "Cys", "TGC": "Cys", "TGA": "Ter", "TGG": "Trp", "CGT": "Arg", "CGC": "Arg",
    "CGA": "Arg", "CGG": "Arg", "AGT": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
    "GGT": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
}
COMP = str.maketrans("ACGTN", "TGCAN")


def revcomp(s: str) -> str:
    return s.translate(COMP)[::-1]


def fetch(chrom: str, start: int, end: int) -> str:
    out = subprocess.run([SAMTOOLS, "faidx", REF, f"{chrom}:{start}-{end}"],
                         capture_output=True, text=True, check=True).stdout
    return "".join(out.splitlines()[1:]).upper()


def pam_ok(seq: str, pattern: str) -> bool:
    return len(seq) == len(pattern) and all(
        b in IUPAC[p] for b, p in zip(seq, pattern))


def guides(seq: str, origin: int, target_pos: int, edit_from: str,
           window: tuple[int, int], pam: str):
    """Every protospacer putting target_pos in the editing window, either strand."""
    lo, hi = window
    plen = len(pam)
    for strand in (1, -1):
        for offset in range(lo, hi + 1):
            # protospacer position `offset` must land on target_pos
            if strand == 1:
                p_start = target_pos - (offset - 1)          # + strand, 5'->3'
                proto_span = (p_start, p_start + 19)
                pam_span = (p_start + 20, p_start + 19 + plen)
            else:
                p_start = target_pos + (offset - 1)          # - strand reads right to left
                proto_span = (p_start - 19, p_start)
                pam_span = (p_start - 19 - plen, p_start - 20)
            s0, s1 = proto_span[0] - origin, proto_span[1] - origin
            m0, m1 = pam_span[0] - origin, pam_span[1] - origin
            if s0 < 0 or m0 < 0 or s1 >= len(seq) or m1 >= len(seq):
                continue
            proto = seq[s0:s1 + 1]
            pam_seq = seq[m0:m1 + 1]
            if strand == -1:
                proto, pam_seq = revcomp(proto), revcomp(pam_seq)
            if not pam_ok(pam_seq, pam):
                continue
            if proto[offset - 1] != edit_from:
                continue
            yield dict(strand=strand, proto=proto, pam=pam_seq,
                       span=proto_span, target_offset=offset)


def bystanders(g: dict, origin: int, target_pos: int, edit_from: str, edit_to: str,
               window: tuple[int, int]):
    """Editable bases other than the target inside the window, as + strand changes."""
    lo, hi = window
    out = []
    for off in range(lo, hi + 1):
        if g["proto"][off - 1] != edit_from:
            continue
        pos = (g["span"][0] + off - 1) if g["strand"] == 1 else (g["span"][1] - off + 1)
        if pos == target_pos:
            continue
        if g["strand"] == 1:
            ref_p, alt_p = edit_from, edit_to
        else:
            ref_p, alt_p = edit_from.translate(COMP), edit_to.translate(COMP)
        out.append((pos, ref_p, alt_p))
    return out


def score(chrom: str, pos: int, ref: str, alt: str) -> tuple[str, str]:
    """Atlas AVI PHRED and splicing score for one substitution, or blanks."""
    a = next((f[5] for f in atlas.region("avi", chrom, pos, pos)
              if f[2] == ref and f[3] == alt), "")
    s = next((f[4] for f in atlas.region("splicing", chrom, pos, pos)
              if f[2] == ref and f[3] == alt), "")
    return a, s


def repair_options(pat_codon: str, ref_codon: str, c0: int):
    """Transition edits that stop the patient codon being a stop codon."""
    out = []
    for i in range(3):
        for editor, frm, to in EDITORS:
            for strand in (1, -1):
                base = pat_codon[i] if strand == 1 else pat_codon[i].translate(COMP)
                if base != frm:
                    continue
                new_plus = to if strand == 1 else to.translate(COMP)
                new_codon = pat_codon[:i] + new_plus + pat_codon[i + 1:]
                if CODONS[pat_codon] != "Ter" or CODONS[new_codon] == "Ter":
                    continue
                wt_new = ref_codon[:i] + new_plus + ref_codon[i + 1:]
                out.append(dict(pos=c0 + i, editor=editor, frm=frm, to=to, strand=strand,
                                new_codon=new_codon, wt_codon=ref_codon, wt_new=wt_new))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cols = ["target", "repair_site", "editor", "pam", "enzyme", "window", "strand",
            "protospacer", "pam_seq", "target_offset", "n_bystanders", "bystander_pos",
            "bys_ref", "bys_alt", "bys_avi_phred", "bys_splicing"]
    out_rows = []

    for t in TARGETS:
        origin = t["pos"] - FLANK
        ref_seq = fetch(t["chrom"], origin, t["pos"] + FLANK)
        pat_seq = ref_seq[:t["pos"] - origin] + t["alt"] + ref_seq[t["pos"] - origin + 1:]
        c0, c1 = t["codon"]
        ref_codon = ref_seq[c0 - origin:c1 - origin + 1]
        pat_codon = pat_seq[c0 - origin:c1 - origin + 1]
        print(f"\n=== {t['name']}")
        print(f"    codon {c0}-{c1}: reference {ref_codon} ({CODONS[ref_codon]}) "
              f"-> patient {pat_codon} ({CODONS[pat_codon]})")
        print(f"    reverting {t['alt']}>{t['ref']} is a transversion, which no "
              f"base editor performs; correction needs prime editing or HDR")

        options = repair_options(pat_codon, ref_codon, c0)
        if not options:
            print("    and no transition edit elsewhere in the codon improves it "
                  "either - this allele is not a base-editing target")
            continue

        for opt in options:
            silent = CODONS[opt["wt_new"]] == CODONS[opt["wt_codon"]]
            print(f"\n    Read-through option: {t['chrom']}:{opt['pos']} "
                  f"{opt['frm']}>{opt['to']} on the {'+' if opt['strand'] > 0 else '-'} strand "
                  f"via {opt['editor']}")
            print(f"      patient allele    {pat_codon} ({CODONS[pat_codon]}) -> "
                  f"{opt['new_codon']} ({CODONS[opt['new_codon']]})")
            print(f"      wild-type allele  {opt['wt_codon']} ({CODONS[opt['wt_codon']]}) -> "
                  f"{opt['wt_new']} ({CODONS[opt['wt_new']]})"
                  + ("   [silent - the guide need not discriminate between alleles]"
                     if silent else "   [WARNING: alters the functional copy]"))
            for wname, window in WINDOWS.items():
                for pam, enzyme in PAMS:
                    found = list(guides(pat_seq, origin, opt["pos"], opt["frm"], window, pam))
                    summary = []
                    for g in found:
                        bys = bystanders(g, origin, opt["pos"], opt["frm"], opt["to"], window)
                        scored = [(bp, br, ba) + score(t["chrom"], bp, br, ba) for bp, br, ba in bys]
                        base = [t["name"], f"{t['chrom']}:{opt['pos']}", opt["editor"], pam,
                                enzyme, wname, "+" if g["strand"] == 1 else "-", g["proto"],
                                g["pam"], g["target_offset"], len(bys)]
                        if scored:
                            out_rows += [base + list(x) for x in scored]
                        else:
                            out_rows.append(base + ["", "", "", "", ""])
                        worst = max((float(x[3]) for x in scored if x[3]), default=0.0)
                        summary.append((len(bys), worst))
                    if not found:
                        print(f"      {pam:4s} {enzyme:22s} {wname:16s}: no guide")
                        continue
                    nb = [n for n, _ in summary]
                    worst = max(w for _, w in summary)
                    clean = sum(1 for n, w in summary if w < 20)
                    print(f"      {pam:4s} {enzyme:22s} {wname:16s}: {len(found)} guide(s), "
                          f"{min(nb)}-{max(nb)} bystanders, worst bystander AVI {worst:.1f}, "
                          f"{clean} guide(s) with every bystander under AVI 20")

    with open(args.out, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in out_rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    print("\nwrote", args.out, f"({len(out_rows)} rows)")


if __name__ == "__main__":
    main()
