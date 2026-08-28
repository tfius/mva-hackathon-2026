# Track 2 — Mechanism and Drug Repurposing

**Rare Disease, Real Kid: MVA Hackathon 2026** · proband `PROBAND01` · team `texdata`
Draft — mechanism section complete, knowledge-graph section in progress. 28 August 2026

> **Framing.** Everything below is a hypothesis for follow-up, not evidence that a medicine works. No candidate here has been tested in a person with MVA1. Nothing in this document is clinical advice, and every candidate would need mechanism confirmation, then a model system, then a clinician, before it meant anything for a patient.

---

## 1. The lesion, stated precisely

Track 1 calls biallelic *BUB1B*: `c.2210T>G p.Leu737Ter` (null) in trans with `c.3006T>G p.Asn1002Lys` (missense). See [`track1-variant-report.md`](track1-variant-report.md).

*BUB1B* encodes **BubR1**, 1050 aa (UniProt O60566): BUB1 N-terminal domain 62–226, protein kinase domain 766–1050, catalytic proton acceptor D882.

- The **null allele** terminates at residue 737 — 29 residues *before* the kinase domain begins — with the premature termination codon 748 nt upstream of the final exon junction, so nonsense-mediated decay is predicted. This allele contributes nothing.
- The **missense allele** produces full-length protein carrying N1002K inside the kinase domain.

The genotype is therefore **not a null**: it is a hypomorph carrying roughly half-dose, partly-impaired BubR1. That distinction is the whole basis of what follows. Complete BubR1 loss is embryonic lethal; every therapeutic hypothesis worth having here operates on residual protein that exists.

## 2. What breaks downstream

BubR1 is the pseudokinase core of the **mitotic checkpoint complex** (BubR1–Bub3–Cdc20–Mad2), which restrains APC/C-Cdc20 until every kinetochore is correctly attached. It also recruits PP2A-B56 to kinetochores through its KARD motif, stabilising kinetochore–microtubule attachments.

Reduced BubR1 dose therefore produces a **weakened spindle assembly checkpoint** → premature anaphase onset → chromosome missegregation → **constitutional mosaic aneuploidy** and chromosomal instability, which in turn drives the tumour predisposition (rhabdomyosarcoma, Wilms).

The second consequence is less obvious and matters more for repurposing. BubR1-hypomorphic mice (`BubR1^H/H`) are **progeroid**: growth retardation, reduced lifespan, sarcopenia, cataracts, loss of subcutaneous fat. The overlap with this proband's phenotype — short stature, skeletal muscle atrophy, failure to thrive — is direct, and it means an established mouse model exists in which interventions have already been run *on this gene*.

## 3. Three therapeutic hypotheses, each with a published anchor

### H1 — Raise the residual BubR1 protein: NAD⁺ precursors

BubR1 abundance is set by acetylation of **lysine 668**, written by CBP and erased by the NAD⁺-dependent deacetylase **SIRT2**. The age-related decline in BubR1 is a decline in NAD⁺ and hence in SIRT2's ability to keep K668 deacetylated. In `BubR1^H/H` mice, SIRT2 transgenic overexpression raised median lifespan by 58% (122% in males) and maximal lifespan by 21%; **treatment with the NAD⁺ precursor NMN stabilised BubR1 in vivo** ([North et al., *EMBO J* 2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4194088/)).

Why this is allele-aware and not generic longevity hand-waving: **K668 lies in the null allele's deleted region but is intact on the missense allele.** The p.Asn1002Lys protein is full-length and retains the regulatory lysine, so a SIRT2/NAD⁺ intervention has a substrate to act on — it would stabilise exactly the one partially-functional copy this child has. A patient homozygous for truncating alleles would get nothing from this; this genotype is the one where it could work.

Repurposing candidates: nicotinamide riboside, nicotinamide mononucleotide (both available as supplements with human safety data), and nicotinamide itself.

**Where it could fail.** Boosting a checkpoint protein in a child who has already had a malignancy cuts both ways — more BubR1 means better segregation fidelity, but SIRT2 has context-dependent tumour-suppressor and oncogenic roles. Mouse lifespan is not human healthspan. And no NAD⁺ precursor has been tested in MVA.

### H2 — Remove the cells the lesion has already damaged: senolytics

The foundational senolytics experiment was done **in this mouse**. Clearing p16^Ink4a-positive senescent cells from `BubR1` progeroid mice delayed onset of age-related pathology specifically in **adipose tissue, skeletal muscle and eye**, and late-life clearance attenuated disorders that had already established ([Baker et al., *Nature* 479:232–236, 2011](https://www.nature.com/articles/nature10600)).

Adipose and skeletal muscle are precisely the tissues where this proband is symptomatic — low muscle mass, failure to thrive, short stature.

Repurposing candidates: **dasatinib + quercetin** (dasatinib is already approved in paediatric CML, so paediatric pharmacokinetics and safety exist), navitoclax (limited by thrombocytopenia).

**Where it could fail.** `BubR1^H/H` mice are a progeroid model and MVA1 in a child is not progeria; the senescent-cell burden in a young patient may be far lower than in an aged mouse. Senolytics have never been given to a child for this indication. Dasatinib in a cancer-predisposition syndrome needs oncology input, not a hackathon.

### H3 — Exploit the aneuploid cells' own stress: AMPK activation and HSP90 inhibition

Aneuploid cells carry proteotoxic and energy stress that euploid cells do not. Screening trisomic mouse embryonic fibroblasts identified three compounds that selectively impair aneuploid-cell proliferation: **AICAR** (energy-stress inducer / AMPK activator), **17-AAG** (HSP90 inhibitor), and chloroquine (autophagy inhibitor). AICAR and 17-AAG showed real antiproliferative activity in aneuploid cell lines and were stronger in combination ([Tang, Williams, Siegel & Amon, *Cell* 144:499–512, 2011](https://www.cell.com/fulltext/S0092-8674(11)00056-0)).

This hypothesis is aimed at the **tumour**, not the child — and that distinction is the point. In MVA1 the malignant clone is far more aneuploid than the constitutional background, so a genuinely aneuploidy-selective agent has a therapeutic window that a general cytotoxic does not.

Repurposing candidates: metformin and other AMPK activators (extensive paediatric safety data), 17-AAG/tanespimycin and later-generation HSP90 inhibitors.

**Where it could fail.** The constitutional cells are aneuploid too, so "selective" is a matter of degree, not kind. 17-AAG's clinical record is mixed. AICAR itself is not a practical oral drug; metformin is a much weaker AMPK activator and the substitution is an assumption, not a result.

## 4. What is contraindicated — the negative result that matters

A weakened spindle assembly checkpoint is already the lesion. Any agent that weakens it further is not a candidate, it is a hazard:

- **MPS1/TTK inhibitors** — directly target checkpoint signalling
- **Aurora B inhibitors** — impair error correction at kinetochores
- **KIF11/Eg5 and PLK1 inhibitors** — mitotic-arrest-dependent mechanisms that presuppose an intact checkpoint

Two further clinical notes fall out of the mechanism. First, in a chromosomal-instability syndrome the standing question of **radiosensitivity and genotoxic-chemotherapy tolerance** should be treated as open rather than assumed. Second, drugs whose antitumour mechanism *requires* a functional checkpoint will underperform here on principle.

Stating contraindications is not a hedge — a repurposing screen that cannot say what to avoid has not characterised the mechanism it claims to be reasoning from. This list is also a concrete, falsifiable prediction that the knowledge-graph model can be scored against: TxGNN emits contraindication probabilities as well as indications, and the checkpoint inhibitors above should rank high on the contraindication side.

## 5. Knowledge-graph layer — method

*In progress. Recorded here so the reasoning is auditable rather than retrofitted.*

The three hypotheses above are a **literature prior** — reached by mechanism, before any model was run. The graph layer is deliberately run second and independently, so agreement between the two means something.

1. **Proxy-phenotype mapping.** MVA1 is thinly represented in any biomedical knowledge graph — that is the defining problem for a disease with no approved treatment. Map MONDO MVA1 onto proxy disease nodes in PrimeKG and OptimusKG: chromosomal-instability syndromes, other aneuploidy disorders, cohesinopathies, and the CIN-high cancers.
2. **TxGNN zero-shot.** Indication *and* contraindication prediction on the mapped nodes. Zero-shot inference on a treatment-less orphan disease is the case TxGNN was designed for. Pretrained on PrimeKG (129k nodes / 4.05M edges).
3. **TxGNN Explain (GraphMask).** Multi-hop subgraph per surviving candidate, so every recommendation ships with the edges that produced it rather than a bare score.
4. **OptimusKG as the evidence layer.** 192,813 nodes / 21,834,669 edges over 65 resources, grounded in 18 ontologies via BioCypher/Biolink — roughly 5× PrimeKG's edge count with type-specific metadata. TxGNN's pretrained weights resolve PrimeKG node ids, so PrimeKG carries the model and OptimusKG carries corroboration and graph-RAG retrieval. Retraining TxGNN on OptimusKG is the stretch goal and the honest answer to the Scalability criterion.
5. **Corroboration.** ChEMBL/DrugBank/Open Targets for tractability; DepMap for aneuploidy-selective dependencies.

**Scoring.** Repurposing Feasibility = mechanistic support × evidence strength × paediatric safety record × availability. Reported as a table with each factor separately visible, so a reader can disagree with one weight without discarding the analysis.

**The interesting outcome is disagreement.** If TxGNN nominates a class that mechanism reasoning missed, that is the model earning its place. If it misses all three hypotheses above, that is a finding about knowledge-graph coverage of ultra-rare disease — which is itself worth reporting.

## 6. References

- North BJ, Rosenberg MA, Jeganathan KB, et al. SIRT2 induces the checkpoint kinase BubR1 to increase lifespan. *EMBO J* 33(13):1438–1453, 2014. [PMC4194088](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4194088/)
- Baker DJ, Wijshake T, Tchkonia T, et al. Clearance of p16Ink4a-positive senescent cells delays ageing-associated disorders. *Nature* 479:232–236, 2011. [doi:10.1038/nature10600](https://www.nature.com/articles/nature10600)
- Tang Y-C, Williams BR, Siegel JJ, Amon A. Identification of aneuploidy-selective antiproliferation compounds. *Cell* 144(4):499–512, 2011. [doi:10.1016/j.cell.2011.01.017](https://www.cell.com/fulltext/S0092-8674(11)00056-0)
- Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine (PrimeKG). *Sci Data* 10:67, 2023.
- Huang K, Chandak P, Wang Q, et al. A foundation model for clinician-centered drug repurposing (TxGNN). *Nat Med*, 2024.
- OptimusKG: unifying biomedical knowledge in a modern multimodal graph. [arXiv:2604.27269](https://arxiv.org/abs/2604.27269)
- UniProt O60566 (BUB1B_HUMAN).
