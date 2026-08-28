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

## 5. Knowledge-graph layer — TxGNN zero-shot

The three hypotheses above are a **literature prior**, reached by mechanism and written down before any model was run. The graph layer was then run independently, so agreement between the two means something.

### 5.1 MVA really is a zero-shot case

In PrimeKG the node `mosaic variegated aneuploidy syndrome` (index 28004, a MONDO_grouped node over MONDO 13582 / 9759 / 54736 / 141) carries:

- 214 `disease_phenotype_positive` edges
- 10 `disease_protein` edges — **BUB1, BUB1B, BUB3, CEP57, TRIP13**
- 6 `disease_disease` edges — *chromosomal anomaly*, *neoplastic syndrome*, *polymalformative genetic syndrome with increased risk of developing cancer*
- **zero drug edges of any kind**

Every one of the 7,957 drug labels is 0. There is nothing to memorise, so the ranking is genuine zero-shot inference. Pretrained TxGNN (`full_graph` split 1, n_hid 512, prototype module on) run on CPU; both `indication` and `contraindication` in about 3 seconds each once the graph is loaded.

### 5.2 A correction that changes the answer

TxGNN scores all 7,957 DrugBank nodes in PrimeKG. Most of those are PDB ligands and experimental fragments with a node degree of 2 — and on a disease with no drug edges the model scores **exactly those highest**, because it has learned almost nothing about them. Ranked on the raw 7,957, the top recommendations for this child are *Casimiroin*, *Dithioerythritol* and a run of unnamed crystallographic fragments, and the score correlates *negatively* with degree (Spearman ρ = −0.51).

TxGNN's own `Ranked List` is restricted to the **1,801 drugs that carry indication or contraindication edges** somewhere in PrimeKG. That is the only set a therapeutic recommendation can honestly be drawn from. Within it the degree artefact disappears: ρ = **+0.054** for indication, +0.115 for contraindication. The ranking is not a popularity prior.

Reported because it is the kind of error that produces a confident, publishable, meaningless answer.

### 5.3 What the model returns

Top of the indication ranking for MVA:

| Rank | Drug | Score |
|---|---|---|
| 1 | Nifurtimox | +2.56 |
| 2 | Trifarotene | +2.03 |
| 3 | Methotrexate | +1.72 |
| 4 | Formestane | +1.45 |
| 5 | Imatinib | +1.25 |
| 6 | Fluorouracil | +1.25 |
| 7 | **Paclitaxel** | +1.14 |

Read the graph neighbourhood and this is unsurprising: MVA's disease-disease edges say *neoplastic syndrome* and *cancer-predisposition syndrome*, so the model retrieves antineoplastics. It is answering "what treats a childhood cancer syndrome", not "what corrects a spindle assembly checkpoint hypomorph".

### 5.4 The prior probes — stated before the run, scored after

Percentile within the 1,801 clinically annotated drugs, indication direction:

| Hypothesis | Drug | Rank | Percentile |
|---|---|---|---|
| **H3** aneuploidy-selective | **Hydroxychloroquine** | 50 | **2.8%** |
| **H3** | **Chloroquine** | 51 | **2.8%** |
| **H2** senolytic | **Dasatinib** | 69 | **3.8%** |
| H1 NAD⁺ | Niacin | 218 | 12.1% |
| H1 | Nicotinamide | 569 | 31.6% |
| H3 | Metformin | 1543 | 85.7% |

**Two independent convergences.** Chloroquine is one of the three compounds Amon's screen identified as aneuploidy-selective, and the graph puts chloroquine and its hydroxy analogue in the top 3% — reached from a completely different direction, with no aneuploidy-biology input. Dasatinib is the approved half of the dasatinib+quercetin senolytic pair whose founding experiment was run in the BubR1 mouse, and the graph puts it in the top 4%. Neither was fitted after the fact.

**H1 cannot be evaluated here, and that is a coverage finding rather than a refutation.** Nicotinamide riboside, nicotinamide mononucleotide and NADH are absent from PrimeKG's clinically annotated drug set entirely — they carry no indication edges, because they are supplements. The single best-supported, most allele-specific hypothesis in this report is invisible to the knowledge graph. Any KG-only repurposing pipeline would have missed it.

Metformin at 85.7% is a fair miss: it was always a weak substitution for AICAR, which is not in PrimeKG at all.

### 5.5 Where the model and the mechanism disagree — and who is right

The contraindication prediction stated in §4 **failed**, and failed informatively.

| Drug | Indication rank | Percentile |
|---|---|---|
| Paclitaxel | 7 | 0.4% |
| Vinblastine | 17 | 0.9% |
| Eribulin | 19 | 1.1% |
| Vincristine | 87 | 4.8% |
| Docetaxel | 98 | 5.4% |

Every microtubule-targeting agent sits near the **top of the indications**, not the contraindications. The contraindication ranking meanwhile is led by methoxsalen, mycophenolate and tacrolimus — immunosuppressant and photosensitiser signal, unrelated to mitosis.

The graph knows MVA is a cancer-predisposition syndrome and retrieves sarcoma chemotherapy. It does not know that the spindle assembly checkpoint in this child is *already* hypomorphic, because that fact lives in the variant, not in the disease node. The mechanism is right and the model is wrong, and the disagreement is the most clinically consequential statement in this report: a knowledge-graph repurposing pipeline run on this case without mechanism reasoning would rank checkpoint-dependent chemotherapeutics as the leading recommendations.

### 5.6 Explanations — hub artefacts, and what survives removing them

`03_txgnn_explain.py` reconstructs graph-backed rationales from the released GraphMask gates: a 7,695,474-row edge table with per-layer importance for the indication task. TxGNN's shipped `paths.csv` covers a curated demo set and has no MVA node, so paths are found by bidirectional beam search, two hops from the disease and two from the drug, joined at the meeting node and scored as the length-normalised product of edge importances.

**Run on raw gate importance the result is an artefact, and an instructive one.** Every top path, for every drug, was:

```
MVA <- Colon cancer -> Pimecrolimus <- CYP3A4 -> <drug>
```

scoring 0.5159 for dasatinib, 0.5152 for hydroxychloroquine, 0.5123 for chloroquine, 0.5074 for paclitaxel. Four chemically unrelated drugs, four near-identical scores, one shared hepatic enzyme. The drug-independence is the tell: this is a statement about metabolism, not about why any of them might help. Presented unchecked, a CYP3A4 lookup becomes a "graph-backed medical rationale".

Three corrections: `drug_effect` edges excluded, since a side effect is not a therapeutic rationale; intermediate nodes down-weighted by 1/log₁₀(degree); and 658 ADME hub proteins (CYP, ABC, SLC, UGT, ALB and relatives) removed outright, because degree down-weighting alone did not stop CYP3A4 winning on gate value. Beam width matters and was itself a trap — at 3,000 the filters left only paclitaxel with any path, which looked like a dramatic finding and was an artefact of the search. At 12,000 every candidate has paths. The result below is the beam-12,000 one.

What survives is honest but thin:

```
Dasatinib   MVA <-[disease_disease]- chromosomal anomaly -> Prader-Willi syndrome
                <-[disease_protein]- EPHA2 -[drug_protein]-> Dasatinib
Dasatinib   MVA -[disease_disease]-> cancer-predisposition syndrome <- Bloom syndrome
                <-[disease_protein]- KIT -[drug_protein]-> Dasatinib
Paclitaxel  MVA <-[disease_protein]- TRIP13 -> germ cell tumor
                -[disease_disease]-> testicular teratoma <-[off-label use]- Paclitaxel
```

Dasatinib's routes go through its real kinase targets (EPHA2, KIT, STAT5B) but into unrelated syndromes; the Bloom syndrome path is the only one with biological texture, Bloom being another chromosomal-instability cancer-predisposition syndrome. Paclitaxel's route passes through an actual MVA gene, and says *an MVA gene is implicated in a cancer, and this drug is used off-label in that cancer.* None of it is about checkpoint dose. Nothing routes through BubR1.

Two honest caveats about the reconstruction itself. The search is undirected, so some recovered paths traverse `contraindication` edges while supporting an indication prediction — those edges do carry non-zero GraphMask importance for the indication task, but any rationale shown to a clinician must mark their polarity, and this reconstruction currently does not. And path scores are not calibrated probabilities; they order paths, nothing more.

### 5.7 Why no explanation reaches BubR1 — and the near miss that matters

Counting edges in PrimeKG directly:

| Gene | Total edges | Drug edges |
|---|---|---|
| BUB1B | 464 | **0** |
| BUB1 | 492 | **0** |
| BUB3 | 468 | **0** |
| CEP57 | 426 | **0** |
| TRIP13 | 516 | **0** |
| CDC20 | 500 | **0** |
| MAD2L1 | 580 | **0** |
| AURKB | 762 | 10 — AT9283, Enzastaurin, **Reversine** … |
| PLK1 | 962 | 12 |
| TTK | 288 | 6 — BOS172722 … |
| CENPE | 404 | 2 — GSK-923295 |

**Every gene the MVA node connects to has zero drug edges.** The path `MVA → BUB1B → drug` does not exist because its last edge does not exist. That is a property of the graph, not a failure of the model, and it explains the hub detour completely.

The sharper half: the checkpoint proteins that *are* druggable in PrimeKG — AURKB, PLK1, TTK, CENPE — are precisely the ones that must not be inhibited in a child whose checkpoint is already hypomorphic. One of the AURKB ligands, **reversine**, is a laboratory tool used to *induce* aneuploidy. A pipeline reasoning "find the disease's pathway, find drugs against it" would nominate the contraindicated class with high confidence and a clean subgraph behind it.

**And now the finding that changes how this should be read.** BUB1B's 95 protein interactors in PrimeKG include **SIRT2**, **CREBBP** and **EP300** — alongside HDAC1–5 and KAT2A/KAT2B.

That is the entire acetylation-control axis hypothesis H1 rests on: CBP/p300 writes the acetyl mark, SIRT2 erases it, and BubR1 abundance follows. **PrimeKG encodes the mechanism.** What it does not encode is any drug edge from the NAD⁺ precursors to SIRT2 or its pathway, because nicotinamide riboside and NMN are supplements with no indication records. The graph holds every link but the last one, and TxGNN cannot surface the best-supported hypothesis in this report while sitting one edge away from it.

The lesson is not that knowledge graphs are the wrong tool. It is that ranking 1,801 drugs by a link predictor asks the graph a question it cannot answer here, while walking outward from the disease's own genes asks one it can.

### 5.8 Mechanism-anchored reachability

So `05_mechanism_anchored.py` asks the narrower question directly: starting from BUB1B, BUB1, BUB3, CEP57 and TRIP13, which drugs are reachable through a single protein–protein interaction? Every hit carries the interactor it came through, so the claim is inspectable — *this drug targets a protein that physically interacts with a protein the disease disrupts* — and candidates whose target is itself a checkpoint protein are flagged rather than dropped.

526 interactors, **592 distinct reachable drugs**, 939 gene–interactor–drug rows. Three groups stand out:

- **Flagged contraindicated by construction** — fostamatinib (BUB1B–AURKB, BUB1–PLK1), enzastaurin (BUB1B–AURKB), wortmannin (BUB1–PLK1). The flag fires exactly where the mechanism says it should, which is a check on the method as much as on the drugs.
- **The acetylation axis** — HDAC inhibitors (vorinostat, romidepsin, panobinostat, belinostat, mocetinostat, pracinostat) are all reachable through BUB1B–HDAC1/2/3/4. Mechanistically adjacent and worth follow-up, but **the direction of effect is unresolved**: SIRT2 is a class III sirtuin and is not inhibited by these class I/II agents, and the published acetylation sites on BubR1 do not all act in the same direction. Listed as a question, not a recommendation.
- **NADH**, reachable via BUB1B–NDUFA2, BUB1–ALDH1B1 and BUB3–DLD — redox metabolism rather than the SIRT2 axis, so weak corroboration at best.

This is a reachability set, not a ranking, and its interpretation is bounded by that. But it recovers the mechanism the drug-level model could not, from the same graph.

### 5.7 What is still to run

OptimusKG (192,813 nodes / 21,834,669 edges over 65 resources, ~5x PrimeKG's edges) as an independent evidence layer, with the specific question of whether it covers the NAD⁺ precursors PrimeKG cannot see. Retraining TxGNN on OptimusKG is the stretch goal and the honest answer to the Scalability criterion. DepMap for aneuploidy-selective dependencies; ChEMBL/Open Targets for tractability.

### 5.8 Scoring

Repurposing Feasibility = mechanistic support × evidence strength × paediatric safety record × availability, with each factor reported separately so a reader can disagree with one weight without discarding the analysis.

## 6. References

- North BJ, Rosenberg MA, Jeganathan KB, et al. SIRT2 induces the checkpoint kinase BubR1 to increase lifespan. *EMBO J* 33(13):1438–1453, 2014. [PMC4194088](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4194088/)
- Baker DJ, Wijshake T, Tchkonia T, et al. Clearance of p16Ink4a-positive senescent cells delays ageing-associated disorders. *Nature* 479:232–236, 2011. [doi:10.1038/nature10600](https://www.nature.com/articles/nature10600)
- Tang Y-C, Williams BR, Siegel JJ, Amon A. Identification of aneuploidy-selective antiproliferation compounds. *Cell* 144(4):499–512, 2011. [doi:10.1016/j.cell.2011.01.017](https://www.cell.com/fulltext/S0092-8674(11)00056-0)
- Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine (PrimeKG). *Sci Data* 10:67, 2023.
- Huang K, Chandak P, Wang Q, et al. A foundation model for clinician-centered drug repurposing (TxGNN). *Nat Med*, 2024.
- OptimusKG: unifying biomedical knowledge in a modern multimodal graph. [arXiv:2604.27269](https://arxiv.org/abs/2604.27269)
- UniProt O60566 (BUB1B_HUMAN).
