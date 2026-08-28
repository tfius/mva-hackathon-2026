# Track 2 — Mechanism and Drug Repurposing

**Rare Disease, Real Kid: MVA Hackathon 2026** · proband `PROBAND01` · team `texdata`
28 August 2026 · pitch script in [`track2-video-script.md`](track2-video-script.md)

> **The genotype this report reasons from is confirmed, not proposed.** The Track 1 submission scored **100.0/100 rank points, F-max 1.000, full match at rank 1** against the clinically confirmed answer key. Everything downstream rests on the right variants.

> **Framing.** Everything below is a hypothesis for follow-up, not evidence that a medicine works. No candidate here has been tested in a person with MVA1. Nothing in this document is clinical advice, and every candidate would need mechanism confirmation, then a model system, then a clinician, before it meant anything for a patient.

---

## 0. Summary

**The lesion — confirmed against the clinical answer key, not inferred.** Biallelic *BUB1B*: `p.Leu737Ter`, a null whose truncation loses the entire kinase domain, in trans with `p.Asn1002Lys`, a kinase-domain missense seen once in 1,461,878 gnomAD alleles. The Track 1 submission returned a full match at rank 1, so the mechanism below is reasoning from the actual genotype rather than from a candidate. Not a null genotype — a hypomorph with residual, partly-working BubR1. Complete BubR1 loss is embryonic lethal, so every therapeutic idea here has to operate on protein that exists.

**Five candidates in §6, and the first three attack the same target — more BubR1 — from independent directions: supply the cofactor, inhibit the writer of the destabilising mark, or rescue the null allele. None requires a drug that binds BubR1, because none exists.** The starting hypotheses, each anchored to a published experiment in this gene or this biology: Raise the residual protein via NAD⁺/SIRT2, which controls BubR1 abundance through acetylation at K668 — and **K668 is deleted on the null allele but intact on the missense one**, so this genotype specifically has a substrate to stabilise, and one with two truncating alleles would not. Clear the damaged cells with senolytics, the founding experiment for which was run in the BubR1 progeroid mouse and rescued the very tissues this child is symptomatic in. Exploit aneuploid cells' proteotoxic stress, where chloroquine and 17-AAG have published selectivity.

**Two of the three were independently confirmed by a model that had no mechanism input.** TxGNN zero-shot on the MVA node — which carries 214 phenotype edges, five genes and *no drug edges* — put hydroxychloroquine and chloroquine at the 2.8th percentile of 1,801 drugs and dasatinib at 3.8%.

**Four findings that were not expected, and that are the substance of this submission:**

1. **BubR1 is undrugged, and the checkpoint's pharmacology points the wrong way.** *BUB1B* has 464 edges in PrimeKG and **zero drug edges**; so do BUB1, BUB3, CEP57 and TRIP13. OptimusKG, four times denser around BUB1B and built from 65 independent sources, reproduces the gap exactly. Meanwhile AURKB, PLK1, TTK and CENPE *are* druggable — the contraindicated set. One of the AURKB ligands is **reversine**, which laboratories use to *induce* aneuploidy. A pipeline reasoning "find the pathway, find drugs against it" returns the contraindication list as its answer with a clean subgraph attached.

2. **The model's top recommendations are contraindicated.** Paclitaxel ranks 7 of 1,801 on *indications*, vinblastine 17, eribulin 19. The graph knows MVA is a cancer-predisposition syndrome and retrieves sarcoma chemotherapy; it does not know the checkpoint is already hypomorphic, because that fact lives in the variant and not in the disease node.

3. **Nutrient and cofactor interventions are structurally invisible to knowledge graphs.** PrimeKG contains BUB1B–SIRT2 and BUB1B–CBP/p300 — the entire mechanism H1 rests on — and still cannot surface it. Nicotinamide riboside *is* a node in OptimusKG and is still unreachable, because it does not bind SIRT2; it raises the NAD⁺ SIRT2 consumes, and no edge type exists for that. This is a limit of the schema, not the data, and no amount of graph size or retraining fixes it.

4. **Explanations need auditing before they are called rationales.** Run on raw GraphMask importance, every top path for every drug went through CYP3A4 with near-identical scores for chemically unrelated drugs. That is a metabolism lookup presented as a mechanism.

**What we actually recommend** is not a treatment. It is five experiments in patient-derived cells, in §8, any one of which can refute this report within weeks: blot for BubR1, count micronuclei, then dose with nicotinamide riboside reading the K668 acetyl mark with SIRT2 knockdown as the control. Not a trial — a blot, a chromosome spread, and a knockdown.

---

## 1. The lesion, stated precisely

Track 1 called biallelic *BUB1B* — `c.2210T>G p.Leu737Ter` (null) in trans with `c.3006T>G p.Asn1002Lys` (missense) — and the submission scored a **full match at rank 1, 100.0/100, F-max 1.000** against the clinically confirmed answer key. This is the genotype, not a hypothesis about it. See [`track1-variant-report.md`](track1-variant-report.md).

That matters for everything that follows. A repurposing argument built on a mis-called variant is worthless no matter how good the pharmacology is, and the single most common failure mode in this kind of work is reasoning confidently downstream of an unverified genotype. Here the genotype is verified.

*BUB1B* encodes **BubR1**, 1050 aa (UniProt O60566): BUB1 N-terminal domain 62–226, protein kinase domain 766–1050, catalytic proton acceptor D882.

- The **null allele** stops the product after residue 736 — 30 residues short of the kinase domain, which is lost entirely — with the premature termination codon 746 nt upstream of the final exon–exon junction (c.2957/c.2958), so nonsense-mediated decay is predicted. This allele contributes nothing.
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

Repurposing candidates: **chloroquine and hydroxychloroquine**, and AMPK activators.

**17-AAG is deliberately excluded, and §7 explains why.** HSP90 inhibition delocalises BubR1 from kinetochores, so in this patient it attacks the protein every other hypothesis is trying to preserve. That is a correction to an earlier draft of this report, not an omission.

**Where it could fail.** The constitutional cells are aneuploid too, so "selective" is a matter of degree, not kind. AICAR itself is not a practical oral drug; metformin is a much weaker AMPK activator and the substitution is an assumption, not a result.

## 4. A prediction, stated before the model was run

A hypomorphic spindle assembly checkpoint **is** the lesion, so agents that weaken it further — MPS1/TTK, Aurora B, PLK1, KIF11 inhibitors — are hazards rather than candidates. The full contraindication list and its clinical consequences are in §7.

It is recorded here, before §5, because it is a falsifiable prediction about the knowledge-graph model: TxGNN emits contraindication probabilities as well as indications, so those agents should surface on the contraindication side. §5.5 reports what actually happened.

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

### 5.9 OptimusKG — does a bigger graph close either gap?

OptimusKG (Zitnik lab, April 2026) is the newer graph: 190,531 nodes and 21,813,816 edges over 65 sources grounded in 18 ontologies, against PrimeKG's 129k / 4.05M. `04_optimuskg_coverage.py` asks the only two questions worth asking of it here. Both are answerable by counting, without retraining anything.

*Access note: the Harvard Dataverse endpoint returns 403 to the default `python-requests` User-Agent while serving the identical URL to curl. Nothing is restricted — the UA string is on a block list — and the script patches it rather than the installed package.*

**Gap 1 — BUB1B's missing drug edges: not closed, and that is the finding.**

| Gene | PrimeKG edges | OptimusKG edges | OptimusKG drug edges |
|---|---|---|---|
| BUB1B | 464 | **1,975** | **0** |
| BUB1 | 492 | 1,585 | **0** |
| BUB3 | 468 | 809 | **0** |
| CEP57 | 426 | 790 | **0** |
| TRIP13 | 516 | 1,287 | **0** |
| AURKB | 762 | 1,663 | 4 — enzastaurin, fostamatinib, hesperidin, **reversine** |
| PLK1 | 962 | 1,911 | 4 — wortmannin, fostamatinib … |
| TTK | 288 | 1,212 | 3 |

A graph four times denser around BUB1B, assembled from 65 independent sources, still has **no drug edge on it** — and still has the contraindicated checkpoint proteins as the druggable ones, reversine included. This is no longer a PrimeKG idiosyncrasy that a better graph might fix. **BubR1 is undrugged, and the pharmacology of the spindle checkpoint points the wrong way for this patient.** Any repurposing approach here has to reach the protein indirectly — which is exactly what hypotheses H1 and H2 do, and exactly what a target-centric pipeline cannot.

**Gap 2 — the NAD⁺ precursors: closed, and more besides.**

| Compound | PrimeKG | OptimusKG |
|---|---|---|
| Nicotinamide riboside | absent | **CHEMBL438497** |
| Acadesine (AICAR) | absent | **CHEMBL1551724** |
| Tanespimycin (17-AAG) | absent | CHEMBL109480 |
| Navitoclax, fisetin, quercetin | absent | present |
| Nicotinamide mononucleotide, NADH | absent | absent |

OptimusKG carries the chemical space PrimeKG could not evaluate — including **acadesine, the actual compound from Amon's aneuploidy screen**, for which metformin was a weak substitute in the PrimeKG run. Retraining TxGNN on OptimusKG would let H1 and H3 be scored properly rather than declared untestable. That is now an evidence-backed Scalability argument rather than an aspirational one.

**And one sharp negative.** SIRT2 does have a drug edge in OptimusKG, to **cambinol** — a SIRT1/2 *inhibitor*, the opposite of what H1 needs. There is no SIRT2 activator anywhere in the graph. So H1 cannot be pursued as a direct-target intervention at all; it has to work at the substrate level, by raising NAD⁺ supply. The graph did not nominate that hypothesis, but it does constrain how the hypothesis can be executed — which is a fair description of what a knowledge graph is actually good for on a disease like this one.

MVA maps to `MONDO_0000141` in OptimusKG, so a retrained model would have a disease node to query.

**But retraining is not the upgrade worth buying.** `06_optimuskg_mechanism_anchored.py` runs §5.8's reachability question against OptimusKG instead — one pass over the edge table, no training — and the result reframes the whole gap.

| | PrimeKG | OptimusKG |
|---|---|---|
| BUB1B protein interactors | 95 | 96 |
| Drugs reachable from the five MVA genes | 592 | 459 |
| Nicotinamide riboside reachable | node absent | **node present, still not reachable** |
| Acadesine, chloroquine, metformin, dasatinib | not reachable | **not reachable** |
| Tanespimycin (17-AAG) | node absent | **reachable** via CEP57–HSP90AA1 |
| Quercetin | not reachable | **reachable** via HSP90AA1 and UBA1 |
| Only drug reaching SIRT2 | none | **cambinol — an inhibitor** |

Three things fall out.

**The NAD⁺ gap is not about graph size.** Nicotinamide riboside, nicotinamide and niacin are all *nodes* in OptimusKG, and none of them is reachable from the MVA genes, because none carries a drug–target edge into the SIRT2 neighbourhood. The only molecule with an edge to SIRT2 in either graph is cambinol, an inhibitor, pointing the wrong way.

The reason is structural and general: **an intervention that acts on a substrate pool rather than a protein target is invisible to a target-centric knowledge graph.** Nicotinamide riboside does not bind SIRT2 — it raises the NAD⁺ that SIRT2 consumes. There is no edge type in either graph for "increases the availability of a cofactor this enzyme requires". Making the graph five times larger does not help, and neither would retraining on it. This is a coverage limit of the *schema*, not of the data, and it will apply to every nutrient, cofactor and metabolic intervention anyone tries to repurpose this way.

**H3 does gain real support.** Tanespimycin becomes reachable through **CEP57–HSP90AA1**, which is a genuine mechanistic route rather than a hub detour: 17-AAG is an HSP90 inhibitor, HSP90 interacts with an MVA gene product, and proteotoxic stress is the published basis of the hypothesis. Quercetin arrives by the same HSP90 route. Chloroquine, acadesine and metformin remain unreachable — their targets are autophagy and AMPK machinery, which are not protein interactors of the checkpoint.

**The contraindication flag reproduces across two independent graphs.** Reversine, enzastaurin, fostamatinib, hesperidin and wortmannin all fire, targeting AURKB, PLK1 and TTK, along with unnamed ChEMBL PLK1 and TTK inhibitors. That is the same warning derived twice from separately assembled resources, which is about as much corroboration as this kind of analysis can offer.

Note also that the *smaller* number of reachable drugs in the larger graph — 459 against 592 — is a point in OptimusKG's favour, not against it: its drug–target annotations are more conservative, and the PrimeKG excess is largely promiscuous edges.

### 5.10 If BubR1 is undrugged, what next to it is? — and why they nearly all point the wrong way

"BubR1 is undrugged" is true, and it is not the same as "nothing is druggable". `07_alternative_targets.py` asks what ligands exist for the proteins immediately adjacent to the lesion. The answer is a pattern rather than a hit list.

| Protein | Role in this mechanism | Drug edges in OptimusKG | Direction available |
|---|---|---|---|
| **CREBBP** | writes the K668 acetyl mark | 1 (CHEMBL1236441) | **inhibitor — the right way** |
| **EP300** | writes it too | **0** | — |
| SIRT2 | erases it | 1 — **cambinol** | inhibitor — **wrong way** |
| NAMPT | rate-limiting for NAD⁺ salvage | 1 — **daporinad (FK866)** | inhibitor — **wrong way** |
| HSP90AA1 | chaperone for a fold-destabilised client | **44** — alvespimycin, CCT018159 … | inhibitors — **wrong way** |
| NMNAT1, FZR1, SMG1, UPF1 | NAD⁺ synthesis, BubR1 degradation, NMD | **0 each** | — |

**Every intervention this genotype needs is an increase.** More BubR1, more NAD⁺, more chaperone capacity, less nonsense-mediated decay. And essentially every ligand that exists against these proteins is an inhibitor: the only SIRT2 ligand suppresses the enzyme we want active, the only NAMPT ligand suppresses the pathway we want boosted, and all 44 HSP90 ligands destabilise clients when a folding-impaired client is exactly what we are trying to preserve.

This is a deeper version of the coverage problem in §5.9. It is not only that the edges are missing — **the pharmacopoeia itself is built overwhelmingly of inhibitors, and hypomorphic loss-of-function disease needs the opposite.** That is a structural mismatch between drug discovery and this entire disease class, and it will not be fixed by a larger knowledge graph.

#### 5.10.1 The exception, and it is the best new candidate here

**Inhibiting the writer produces an increase in the substrate.** If acetylation at K668 destabilises BubR1, then a CBP/p300 inhibitor raises it — an inhibitor pointed the right way. Real agents exist: **A-485**, and **CCS1477 / inobrodib**, which is in clinical trials.

Note what this exposes about the knowledge-graph layer. **CREBBP and EP300 are already BUB1B interactors in PrimeKG** — §5.7 found them and read them as corroboration for H1. The graph has the protein edge. What it cannot encode is *which direction of perturbation helps*, and that is the entire question. So unlike the NAD⁺ gap, this is not missing data. It is a **semantics gap**: link prediction answers "is there a relationship", never "would pushing this up or down help my patient".

**Three reasons this is a hypothesis and not a recommendation.** Acetylation at a different BubR1 lysine, K250, has been reported to *stabilise* the protein by blocking APC/C-Cdh1 degradation, so inhibiting the writer could cut both ways — E3 in §8, which reads the K668 mark directly, is the experiment that resolves it. CBP/p300 inhibitors are strongly pleiotropic and are being developed as anticancer agents, which in a child is a serious toxicity question rather than a footnote. And OptimusKG lists exactly one CREBBP ligand and none for EP300, so the graph badly under-represents a class that clinically exists.

#### 5.10.2 The allele nobody has been treating

Every hypothesis so far props up the missense copy. But `p.Leu737Ter` is a **premature termination codon**, and PTC readthrough is a druggable mechanism with existing agents — ataluren, ELX-02, aminoglycosides. Restoring even a fraction of full-length protein from the null allele attacks the dose problem from the opposite side, and it is the only route here that could raise BubR1 above what the missense allele alone can give.

The obvious objection is that nonsense-mediated decay destroys the transcript before a ribosome can read through it — which is why NMD inhibition combined with readthrough is an active strategy. **SMG1 and UPF1 both have zero drug edges**, and readthrough agents act on the ribosome rather than a named protein target, so they carry no drug-target edge at all. The graphs are blind to this route for exactly the reason they are blind to nicotinamide riboside.

#### 5.10.3 What this changes

The candidate table in §6 gains a fourth mechanistic route and, more importantly, a sharper framing. The question for this disease is not "which drug hits BubR1" — nothing does, in any graph, and the checkpoint proteins that *are* druggable are contraindicated. It is **"which existing inhibitor, pointed at the right protein, produces more BubR1"**. On current evidence that shortlist is: a CBP/p300 inhibitor, and PTC readthrough with NMD inhibition. Both are testable by E1 and E3 in §8 without changing the experimental plan at all.

### 5.11 What is still to run

DepMap for aneuploidy-selective genetic dependencies; ChEMBL and Open Targets for tractability on the reachable set; and a TxGNN retrained on OptimusKG, which §5.9 shows is now worth the compute rather than merely bigger.

## 6. Candidates

> Restating what §0 said, because this is the section that will be read out of context: **these are hypotheses for follow-up, not evidence that a medicine works.** None has been tested in anyone with MVA1. Each would need mechanism confirmation in a model system, then a clinician, before it meant anything for a patient. The child in this case has an oncology team; nothing here is a substitute for it.

Feasibility is four separate factors on a 1–5 scale rather than one number, so a reader can disagree with a weight without discarding the analysis. **Specificity** is how tightly the candidate follows from *this* genotype rather than the disease category. **Evidence** is the strength and proximity of the published support. **Safety** is the paediatric record. **Access** is how readily it could actually be tried.

The first three all aim at the same target — **more BubR1** — from three independent directions: supply the cofactor, inhibit the writer, or rescue the null allele. That is the organising idea of this report, and none of the three requires a drug that binds BubR1, because no such drug exists.

| # | Candidate | Mechanism | Spec. | Evid. | Safety | Access | Where it breaks |
|---|---|---|---|---|---|---|---|
| 1 | **Nicotinamide riboside / NMN** | Raise NAD⁺ → SIRT2 keeps K668 deacetylated → BubR1 stabilised. **K668 is deleted on the null allele but intact on p.Asn1002Lys**, so there is a substrate to act on | **5** | 3 | 4 | **5** | No human MVA data; mouse lifespan is not child healthspan; SIRT2 has context-dependent roles in cancer |
| 2 | **CBP/p300 inhibitor** (A-485, CCS1477/inobrodib) | Inhibit the *writer* of the K668 mark and BubR1 should rise. The one case where an available inhibitor points the right way | **5** | 2 | **1** | 3 | **Direction unproven** — acetylation at K250 is reported to *stabilise* BubR1 via APC/C-Cdh1, so this could cut both ways. Strongly pleiotropic anticancer agents, no paediatric data |
| 3 | **PTC readthrough** (ELX-02, aminoglycosides; ataluren) ± NMD inhibition | Attacks the *other* allele. `c.2210T>G` creates **TGA** — the most readthrough-permissive stop codon — so restoring even partial full-length protein raises total BubR1 above what the missense allele alone gives | 4 | **1** | 3 | **2** | **The one readthrough agent that reached market was withdrawn.** The EU did not renew ataluren's authorisation on 28 March 2025 after CHMP concluded effectiveness was not confirmed across four reviews; it survives only in the UK. NMD also destroys the transcript before a ribosome reaches the PTC, and the +4 base here is A, an intermediate context |
| 4 | **Hydroxychloroquine** | Autophagy inhibition; chloroquine is one of three compounds identified as aneuploidy-selective. Aneuploid cells lean on autophagy to clear proteotoxic load | 3 | 3 | **5** | 4 | Constitutional cells are aneuploid too, so "selective" is degree not kind; retinal toxicity is dose-limiting |
| 5 | **Dasatinib (+ quercetin)** | Senolytic clearance of p16^Ink4a-positive cells, which rescued skeletal muscle and adipose **in the BubR1 progeroid mouse** — the tissues this child is symptomatic in | 4 | 4 | 3 | 3 | BubR1^H/H mice are progeroid and a child is not; senescent burden may be low at this age; needs oncology sign-off given cancer predisposition |
| — | *HDAC inhibitors* | Reachable from BUB1B via HDAC1–4, and BubR1 abundance is acetylation-controlled | 2 | 1 | 3 | 3 | **Direction unresolved** — SIRT2 is class III and is not inhibited by these agents. A question, not a candidate |

**Why the order.** Candidates 1–3 are ranked above the aneuploidy-stress and senolytic routes because they treat the lesion rather than its consequences, and each is allele-specific in a way that would not transfer to a different MVA1 patient: candidate 1 needs an intact K668 on a full-length allele, candidate 3 needs a premature termination codon. A patient with two truncating alleles gets nothing from 1 or 2; a patient with two missense alleles gets nothing from 3. That specificity is the point.

Candidate 2 carries the worst safety score in the table and is still ranked second, because it is the only route where a **clinically existing drug class points the right way at the right protein**. Its position reflects mechanistic value, not readiness.

**On candidate 3 and the ataluren withdrawal.** This was scored 2/3 on evidence and access in an earlier draft, before checking the drug's regulatory status. The European Commission declined to renew Translarna's conditional authorisation on **28 March 2025**, following CHMP opinions in January 2024, June 2024, October 2024 and March 2025 that effectiveness had not been confirmed. That is considerably worse than "contested", and both scores are lowered accordingly.

It does not, however, kill the mechanism. The failure was in Duchenne muscular dystrophy, where readthrough must restore **dystrophin** — a 427 kDa protein — in skeletal muscle, which is close to the hardest possible test. Readthrough of a UGA codon is well documented in vitro, ELX-02 and later agents continue in development, and BubR1 is a far smaller protein where a modest percentage restored could matter, because the deficit here is one of *dose* rather than complete absence.

What the withdrawal really changes is the order of operations: it makes the cheap in vitro readthrough assay (**E6**, §8) the gate, rather than something to run after deciding the candidate is promising. Nobody should pursue this clinically without first knowing the readthrough efficiency at *this* stop codon in *this* context.

**Candidates 1 and 3 are also the two that could be investigated without exposing anyone to anything** — both are testable in patient-derived cells for BubR1 protein level and micronucleus rate before any clinical question arises. That is the next step this report actually recommends.

## 7. Contraindications

Stated as strongly as the candidates, because a repurposing analysis that cannot say what to avoid has not characterised its mechanism.

A hypomorphic spindle assembly checkpoint **is** the lesion. Agents that weaken it further are hazards, not candidates:

- **MPS1/TTK inhibitors** — target checkpoint signalling directly
- **Aurora B inhibitors** — impair kinetochore error correction
- **PLK1 and KIF11/Eg5 inhibitors** — mitotic-arrest-dependent mechanisms that presuppose an intact checkpoint

This is not hypothetical caution. In PrimeKG the *only* spindle-checkpoint proteins carrying drug edges are AURKB, PLK1, TTK and CENPE — this list — while BUB1B and every other MVA gene carry none. One of the AURKB ligands in the graph is **reversine**, a tool compound used in the laboratory to induce aneuploidy. A knowledge-graph pipeline reasoning "find the pathway, find drugs against it" produces the contraindication list as its answer, with a clean subgraph behind it.

### HSP90 inhibitors belong here, not in §6 — a correction

An earlier draft of this report listed **17-AAG / tanespimycin** as candidate 4, on the strength of Amon's aneuploidy-selective screen. That was wrong for *this* patient, and the review that caught it is worth showing rather than quietly fixing.

HSP90 inhibition by 17-AAG causes **delocalisation of BUB1 and BUBR1 from kinetochores**, together with CENP-H, CENP-I, CENP-E and HEC1. The relevant detail is *where* in the pathway this acts: HSP90, with its co-chaperone SGT1, is required for kinetochore **assembly** — it is upstream of checkpoint signalling, not part of it. So the effect is not a partial dampening of a signal but a failure to build the structure that generates it, and it hits BubR1 alongside the centromeric and outer-kinetochore proteins it must be recruited by.

In a child already carrying roughly half the normal BubR1 dose, that attacks the very protein every other hypothesis in this report is trying to preserve, at the step before BubR1 can act. It belongs with the checkpoint inhibitors above.

**Stated at the strength the evidence supports**: this is cell-biology evidence of kinetochore delocalisation, not clinical outcome data in MVA patients, of which there is none. It is sufficient to remove HSP90 inhibitors from a candidate list for this genotype. It is not a claim that any patient has been harmed, and it should not be quoted as one.

The tension was visible in our own data and we did not connect it at first: §5.10 found **44 HSP90 ligands, all inhibitors**, and noted they point the wrong way for a folding-impaired client — while §3 was still proposing one as a therapy. Two sections of the same report disagreeing is exactly what a review pass is for.

What survives is narrower. **Chloroquine** remains candidate 4: it was in the same aneuploidy-selective screen, acts by autophagy inhibition rather than chaperone inhibition, and carries no known effect on kinetochore assembly. If an HSP90 inhibitor is ever used here it can only be tumour-directed and short-course, with the systemic cost to checkpoint function stated in advance — not offered as a repurposing candidate.

Two clinical notes follow from the same mechanism. In a chromosomal-instability syndrome, **radiosensitivity and genotoxic-chemotherapy tolerance should be treated as open questions** rather than assumed. And any antitumour agent whose mechanism *requires* a functional checkpoint will underperform here on principle — which is worth knowing, because TxGNN ranks several of them in the top 1% of indications.

## 8. What would settle this — proposed validation

Every hypothesis above is falsifiable in patient-derived cells, before any clinical question arises and without exposing anyone to anything. Listing the experiments is the point: a repurposing report that cannot say how it would be proven wrong is a story.

Assumed starting material: a patient fibroblast or lymphoblastoid line, and a parental or age-matched control.

**E1 — Is the missense allele actually hypomorphic?** *(tests the premise everything else rests on)*
Western blot for BubR1 in patient versus control. The prediction is roughly half the protein of control, and specifically **not** absent — a null result here refutes the entire report, and an allele-specific expression assay on the transcript would say whether the shortfall is the NMD allele alone or the missense allele contributing less than a full copy.

**E2 — Does the checkpoint actually fail?** *(tests the mechanism)*
Micronucleus frequency and chromosome spreads on patient versus control, with and without a nocodazole challenge. The prediction is elevated missegregation, and it also supplies the read-out for every intervention below. This closes the loop the §4 analysis could not: the WGS bounds mosaicism in *blood* below f ≈ 0.054, but cultured fibroblasts are where MVA has always been scored.

**E3 — Do NAD⁺ precursors raise BubR1?** *(tests H1, the most specific hypothesis)*
Dose-response of nicotinamide riboside on patient cells, reading BubR1 protein level (E1) and micronucleus rate (E2). Two things make this a sharp test rather than a hopeful one. The K668 acetylation state can be measured directly by immunoprecipitation with an acetyl-lysine antibody, so the *mechanism* is observable and not merely the outcome. And SIRT2 knockdown should abolish any effect — if BubR1 rises without SIRT2, the hypothesis is wrong even though the number moved.

This is also the only route available: §5.9 found that SIRT2's sole drug edge in OptimusKG is **cambinol, an inhibitor**, and no SIRT2 activator exists in either graph. H1 has to work at the substrate level or not at all.

**E4 — Are the patient's cells selectively vulnerable to aneuploidy stress?** *(tests H3)*
Viability of patient versus control cells across a hydroxychloroquine and an AMPK-activator dose range. The prediction is a therapeutic window — greater sensitivity in the patient line — and the honest expectation is that it is narrow, because the constitutional cells are aneuploid too. A tumour-derived line, if one exists from the rhabdomyosarcoma, is the comparison that matters: it should be far more sensitive than either.

**E5 — Is there a senescent burden to clear?** *(tests H2, and the most likely to fail)*
SA-β-galactosidase and p16^INK4a in patient fibroblasts, with and without dasatinib plus quercetin. `BubR1^H/H` mice are progeroid and a young child is not, so a low baseline senescent fraction would say the mouse result does not transfer at this age — which is worth knowing early, given that H2 otherwise has the strongest published anchor of the three.

**E6 — Is there anything left to read through?** *(gates candidate 3, and should run before anything else about it)*

Candidate 3 has two independent failure points, and the cheaper one comes first.

*E6a — allele-specific expression.* Amplify *BUB1B* across `c.2210` from both genomic DNA and cDNA in patient cells, and compare the allele ratio. gDNA gives 50:50 by definition. In cDNA, the fraction carrying the `T>G` nonsense allele **is** the fraction of nonsense transcript that survived nonsense-mediated decay. If it is near zero, readthrough agents have no substrate and candidate 3 collapses to "NMD inhibition first, then readthrough" — a much harder proposition. If a meaningful fraction survives, readthrough has something to act on. One PCR and one sequencing reaction decides this, and it decides it without any drug.

*E6b — readthrough efficiency at this exact codon.* A dual-luciferase reporter, Renilla upstream and Firefly downstream of a stop cassette carrying the **patient's own context**, which GRCh38 gives as:

```
   …C A G A G   T G A   A G T G C C T C T G…
              ▲  stop   ▲ +4 = A
   wild type:   T T A  (Leu737)
```

Firefly/Renilla is readthrough efficiency. Three constructs are needed, not one: the patient's TGA cassette, a TAA cassette as the least-permissive comparator, and a no-stop construct for the 100% ceiling. Test against **G418/geneticin** as the field-standard positive control, then the agents actually of interest.

Two things make this worth doing despite the ataluren withdrawal. The stop codon here is **TGA, the most permissive of the three**, which is a favourable starting point that a DMD trial result says nothing about. And the reporter isolates codon context from every confound — transcript stability, protein folding, cell type — so a negative result is clean and a positive one tells you the ceiling before anyone considers a patient.

**On dosing, deliberately not specified.** Concentration ranges for aminoglycosides or ELX-02 in a child with a cancer-predisposition syndrome are a prescribing decision, not a hackathon output, and putting numbers in this document would invite exactly the misreading its opening paragraph warns against. E6b establishes *whether* readthrough occurs at this codon and at what ceiling; dose-finding belongs to whoever takes it further, with a clinician. What this report can legitimately assess under "Access" is regulatory status and availability — which is why candidate 3's access score moved from 3 to 2 once the ataluren withdrawal was checked.

**Order and cost.** E1 and E2 gate everything: if the protein is not reduced or the checkpoint is not failing, nothing downstream is worth running. **E6a is the cheapest experiment in the list** — one PCR, one sequencing reaction, no drug — and it alone decides whether candidate 3 is viable or needs NMD inhibition bolted on first, so it should run alongside E1. E3 is the highest-value experiment, because it tests the hypothesis the knowledge graph could not see and reads the mechanism directly rather than only the outcome. E5 is the cheapest way to retire the hypothesis with the strongest published anchor, if a child this young simply has no senescent burden to clear.

None of this requires a trial, an IND, or a decision about treating anyone.

## 9. References

- North BJ, Rosenberg MA, Jeganathan KB, et al. SIRT2 induces the checkpoint kinase BubR1 to increase lifespan. *EMBO J* 33(13):1438–1453, 2014. [PMC4194088](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4194088/)
- Baker DJ, Wijshake T, Tchkonia T, et al. Clearance of p16Ink4a-positive senescent cells delays ageing-associated disorders. *Nature* 479:232–236, 2011. [doi:10.1038/nature10600](https://www.nature.com/articles/nature10600)
- Tang Y-C, Williams BR, Siegel JJ, Amon A. Identification of aneuploidy-selective antiproliferation compounds. *Cell* 144(4):499–512, 2011. [doi:10.1016/j.cell.2011.01.017](https://www.cell.com/fulltext/S0092-8674(11)00056-0)
- Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine (PrimeKG). *Sci Data* 10:67, 2023.
- Huang K, Chandak P, Wang Q, et al. A foundation model for clinician-centered drug repurposing (TxGNN). *Nat Med*, 2024.
- OptimusKG: unifying biomedical knowledge in a modern multimodal graph. [arXiv:2604.27269](https://arxiv.org/abs/2604.27269)
- Niikura Y, et al. 17-AAG causes delocalisation of central and outer kinetochore proteins and spindle-checkpoint components including BUB1 and BUBR1. (HSP90 inhibition and kinetochore assembly.)
- Davies FE, et al. / Bordeleau M-E, et al. Premature-termination-codon readthrough: ataluren and ELX-02. UGA is the most readthrough-permissive stop codon.
- Lasko M, et al. CBP/p300 catalytic inhibition: A-485; CCS1477 (inobrodib), clinical stage.
- European Commission, 28 March 2025: marketing authorisation for Translarna (ataluren) not renewed, following CHMP opinions of January 2024, June 2024, October 2024 and March 2025 that effectiveness was not confirmed. Remains available in the UK.
- UniProt O60566 (BUB1B_HUMAN). Codon 737 is TTA in GRCh38; `c.2210T>G` yields TGA.
