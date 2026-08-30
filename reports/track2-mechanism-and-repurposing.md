# Track 2 — Mechanism and Drug Repurposing

**Rare Disease, Real Kid: MVA Hackathon 2026** · proband `PROBAND01` · team `texdata` · 29 August 2026
Pitch script: [`track2-video-script.md`](track2-video-script.md) · code: [github.com/tfius/mva-hackathon-2026](https://github.com/tfius/mva-hackathon-2026)

> **Hypotheses for follow-up, not evidence that a medicine works.** None has been tested in anyone with MVA1. Each needs mechanism confirmation in a model system, then a clinician, before it means anything for a patient. This child has an oncology team; nothing here substitutes for it.

> **The genotype is confirmed, not proposed.** The Track 1 submission scored **100.0/100, F-max 1.000, full match at rank 1** against the clinically confirmed answer key.

---

## 1. Summary

**The lesion.** Biallelic *BUB1B*: `p.Leu737Ter`, a nonsense allele losing the entire kinase domain to nonsense-mediated decay, in trans with `p.Asn1002Lys`, a kinase-domain missense seen once in 1,461,878 gnomAD alleles. Not a null genotype — a **hypomorph with residual, partly-working BubR1**. Complete BubR1 loss is embryonic lethal, so every idea here operates on protein that exists.

**The organising claim.** Six candidates, and the first three reach one target — *more BubR1* — from independent directions: **supply the cofactor**, **inhibit the writer of the destabilising mark**, or **rescue the null allele**. None requires a drug that binds BubR1, because none exists.

**Validated premise, shared by candidates 1, 2 and 6.** Sustained high BubR1 expression in mice preserves genomic integrity, reduces tumorigenesis even against oncogenic Ras, extends lifespan, and does so by *correcting mitotic checkpoint impairment and microtubule–kinetochore attachment defects* — the exact two defects this genotype produces ([Baker, *Nat Cell Biol* 2013](https://www.nature.com/articles/ncb2643)).

**Four findings that are the substance of this submission:**

1. **BubR1 is undrugged, and the checkpoint's pharmacology points the wrong way.** *BUB1B* has 464 edges in PrimeKG and **zero drug edges**; so do BUB1, BUB3, CEP57, TRIP13. OptimusKG — four times denser, 65 sources — reproduces the gap exactly. Meanwhile AURKB, PLK1, TTK and CENPE *are* druggable: the contraindicated set. One ligand the graph attaches to AURKB is **reversine** — whose aneuploidy-inducing activity is actually **MPS1/TTK inhibition**. Repeating that annotation uncritically is the failure §4.4 warns about; the point survives corrected, since the druggable checkpoint proteins remain the ones to avoid.
2. **The model's top recommendations are contraindicated.** TxGNN ranks paclitaxel 7th of 1,801 on *indications*, vinblastine 17th, eribulin 19th — microtubule poisons for a child whose checkpoint is already at half dose. The graph knows MVA is a cancer-predisposition syndrome and retrieves sarcoma chemotherapy; it cannot know the checkpoint is broken, because that lives in the variant.
3. **Two distinct blind spots, and only one is about size.** A **schema gap**: nicotinamide riboside does not bind SIRT2, it raises the NAD⁺ SIRT2 consumes, and no graph has an edge type for "increases availability of a cofactor" — so substrate-pool interventions are invisible at any scale. And a **semantics gap**: CREBBP and EP300 are *already* in PrimeKG as BUB1B interactors, and the graph still cannot say that *inhibiting* them should raise BubR1. Link prediction answers "is there a relationship", never "which direction helps my patient".

*With the caveat adversarial review demanded*: this report reads graph-absence more than one way — as a fact about pharmacology for BubR1, as a schema limit for nicotinamide riboside. That holds only because the two were checked differently, and the "no SIRT2 activator exists" claim rests on a graph lookup rather than a ChEMBL search, making it the weakest of the three.
4. **A standard secondary-findings filter asserts negatives it has not earned.** Filtering ClinVar to `Pathogenic|Likely_pathogenic` dropped **137 non-reference calls** on this genome, twelve reviewed by expert panel. It hid Factor V Leiden, and it let us write "no fluoropyrimidine toxicity risk allele" when the child carries an expert-panel `drug_response` *DPYD* variant.

**What we recommend is not a treatment.** It is six experiments (§7), any of which can refute this report. Not a trial — a blot, a chromosome spread, and a knockdown.

**Honest about what that costs.** An earlier draft said "within weeks". Independent feasibility review put it at **9–18 months and $150–300k**, dominated not by bench work but by ethics approval and deriving a patient cell line that does not yet exist — and the data-use terms forbid *this* team from obtaining material at all. Two experiments escape that: **E6b** needs no patient material and **E6a** needs only blood, not a biopsy. The realistic route runs through the child's clinical genetics team, or through labs that already hold MVA patient lines and the assays.

**And the immediately useful part of this dossier is not the candidates.** It is §9 — a published surveillance guideline for MVA that this report initially lacked, a pharmacogenomic profile obtained free from the diagnostic genome, and parental testing, which would establish phase, supply ACMG PM3 and enable recurrence counselling. None of that needs new science.

## 2. The lesion, and what breaks

*BUB1B* encodes **BubR1**, 1050 aa (UniProt O60566): BUB1 N-terminal domain 62–226, protein kinase domain **766–1050**, catalytic proton acceptor D882.

- **`p.Leu737Ter`** stops the product after residue 736 — **30 residues short of the kinase domain**, which is lost entirely. The PTC sits at c.2209–2211 with the final exon–exon junction at c.2957/c.2958, so it is **746 nt upstream** and far past the 50–55 nt rule: NMD predicted, allele contributes nothing.
- **`p.Asn1002Lys`** is full length, inside the kinase domain, 120 residues C-terminal to the active site. AlphaMissense 0.923, MVP 0.852 — though REVEL is 0.472, and that disagreement is reported rather than averaged away.

BubR1 is the pseudokinase core of the mitotic checkpoint complex, restraining APC/C-Cdc20 until every kinetochore is attached. Reduced dose → checkpoint leaks → missegregation → **constitutional mosaic aneuploidy** and the tumour predisposition.

The second consequence matters more for treatment: `BubR1^H/H` mice are **progeroid** — growth retardation, sarcopenia, loss of subcutaneous fat. That is this proband's phenotype, and it means interventions have already been run in this gene's model.

**The load-bearing fact, stated explicitly because candidates 1 and 2 both rest on it.** BubR1 abundance is set by acetylation at **lysine 668**: CBP acetylates it, which **primes BubR1 for ubiquitination and proteasomal degradation**; the NAD⁺-dependent deacetylase **SIRT2 deacetylates K668 and thereby stabilises** the protein ([North et al., *EMBO J* 2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4194088/)). Acetylation at a second site, **K250, is protective** — but it is written by **PCAF, not CBP**, and occurs during **prometaphase**, whereas the K668 route operates in **interphase**. The two are separable, which matters in §5.

## 3. A prediction, recorded before the model was run

A hypomorphic checkpoint **is** the lesion, so agents that weaken it further — MPS1/TTK, Aurora B, PLK1, KIF11 inhibitors — are hazards, not candidates. Full list and clinical consequences in §6.

Recorded here because it is falsifiable: TxGNN emits contraindication probabilities as well as indications, so those agents should surface on the contraindication side. §4.3 reports what actually happened.

## 4. Knowledge-graph layer

The hypotheses in §5 are a **literature prior**, reached by mechanism and written down before any model ran. The graph layer was run independently, so agreement means something.

### 4.1 A genuine zero-shot case, and a correction that changes the answer

PrimeKG's `mosaic variegated aneuploidy syndrome` node (28004) carries 214 phenotype edges, 10 disease-protein edges — **BUB1, BUB1B, BUB3, CEP57, TRIP13** — 6 disease-disease edges, and **zero drug edges**. All 7,957 drug labels are 0. Pretrained TxGNN, `full_graph` split 1, CPU, ~3 s per relation.

**The correction.** TxGNN scores all 7,957 DrugBank nodes, most of them PDB fragments of degree 2 — and on a disease with no drug edges it scores exactly those highest, so the raw ranking nominates *Casimiroin* and unnamed crystallographic fragments for a child (Spearman ρ = **−0.51** against degree). TxGNN's own `Ranked List` is the **1,801 drugs carrying indication or contraindication edges**; within it the artefact vanishes (ρ = **+0.054**). Reported because it is the kind of error that produces a confident, publishable, meaningless answer.

### 4.2 Two hypotheses independently confirmed

Percentile within the 1,801, indication direction: **hydroxychloroquine 50th and chloroquine 51st (2.8%)**, **dasatinib 69th (3.8%)**. Adjacent ranks for two near-identical 4-aminoquinolines are **one observation, not two** — the drug-independence tell §4.4 uses against the CYP3A4 paths. Two independent confirmations, not three. Chloroquine is one of three compounds from Amon's aneuploidy-selective screen; dasatinib is the approved half of the senolytic pair whose founding experiment used the BubR1 mouse. Neither was fitted after the fact.

**H1 cannot be evaluated here at all** — nicotinamide riboside, NMN and NADH carry no indication edges in PrimeKG, because they are supplements. The best-supported hypothesis in this report is invisible to the model.

### 4.3 Where the model and the mechanism disagree

The §3 prediction **failed**. Paclitaxel ranks **7 of 1,801 on indications** (0.4%), vinblastine 17, eribulin 19, vincristine 87, docetaxel 98. The contraindication ranking is led by methoxsalen, mycophenolate and tacrolimus — immunosuppressant and photosensitiser signal, nothing to do with mitosis.

The graph knows MVA is a cancer-predisposition syndrome and retrieves sarcoma chemotherapy. It cannot know the checkpoint is already hypomorphic, because that fact lives in the variant, not the disease node. **The mechanism is right and the model is wrong**, and this is the most clinically consequential line in the report.

### 4.4 Explanations are hub artefacts until audited

Reconstructing paths from the released GraphMask gates (7,695,474 edges; TxGNN's shipped `paths.csv` has no MVA node), raw gate importance gives, for **every** drug:

```
MVA <- Colon cancer -> Pimecrolimus <- CYP3A4 -> <drug>
```

scoring 0.5159 for dasatinib, 0.5152 for hydroxychloroquine, 0.5074 for paclitaxel. Four unrelated drugs, near-identical scores, one hepatic enzyme — the drug-independence is the tell. Presented unaudited, a CYP3A4 lookup becomes a "graph-backed medical rationale".

Excluding `drug_effect` edges, down-weighting by degree and removing 658 ADME hubs leaves thin but honest paths — dasatinib via EPHA2/KIT into Bloom syndrome, another chromosomal-instability cancer-predisposition syndrome. **Beam width was itself a trap**: at 3,000 the filters left only paclitaxel with any path, which looked like a finding and was an artefact of the search; at 12,000 every candidate has paths.

### 4.5 Why nothing reaches BubR1 — and the two blind spots

| Gene | PrimeKG edges | Drug edges | OptimusKG edges | Drug edges |
|---|---|---|---|---|
| BUB1B | 464 | **0** | **1,975** | **0** |
| BUB1 / BUB3 / CEP57 / TRIP13 | 426–516 | **0** | 790–1,585 | **0** |
| AURKB | 762 | 10 — incl. **reversine** | 1,663 | 4 |
| PLK1 / TTK / CENPE | 288–962 | 12 / 6 / 2 | 1,212–1,911 | 4 / 3 / 0 |

`MVA → BUB1B → drug` cannot exist, because its last edge does not. A graph four times denser from 65 independent sources reproduces the gap exactly: **BubR1 is undrugged**, and that is a fact about pharmacology, not about PrimeKG.

**Schema gap.** OptimusKG *does* carry nicotinamide riboside and acadesine as nodes — and neither is reachable from the MVA genes, because nicotinamide riboside does not bind SIRT2; it raises the NAD⁺ SIRT2 consumes. No graph has an edge type for "increases availability of a cofactor this enzyme requires". **Substrate-pool interventions are invisible at any scale**, and that applies to every nutrient and metabolic repurposing candidate.

**Semantics gap.** CREBBP and EP300 are *already* BUB1B interactors in PrimeKG. The edge exists; what cannot be encoded is that **inhibiting** them should raise BubR1. Not missing data — missing meaning.

**And a directional mismatch in the drugs themselves.** Every intervention this genotype needs is an *increase*. Of the proteins adjacent to the lesion, SIRT2's only ligand is **cambinol, an inhibitor**; NAMPT's only ligand is **daporinad, an inhibitor**; and all **44** HSP90 ligands destabilise clients. This is a well-known problem for loss-of-function disease generally — the standard motivation for gene therapy, ASOs and readthrough — and it is quantified here against a specific graph for a specific patient. The one exception is the best new candidate in this report: **inhibiting the writer raises the substrate.**

## 5. Candidates

Feasibility is four factors on a 1–5 scale rather than one number, so a reader can disagree with a weight without discarding the analysis. **Specificity** — how tightly it follows from *this* genotype. **Evidence** — strength and proximity of published support. **Safety** — the paediatric record. **Access** — how readily it could be tried.

| # | Candidate | Mechanism | Spec. | Evid. | Safety | Access | Where it breaks |
|---|---|---|---|---|---|---|---|
| 1 | **Nicotinamide riboside / NMN** | Raise NAD⁺ → SIRT2 keeps K668 deacetylated → BubR1 stabilised. **K668 survives on the missense allele's full-length protein, while the nonsense allele is NMD-degraded and makes essentially none** — so there is a substrate to act on | **5** | **4** | 4 | **5** | **Two risks stronger than previously stated.** NAD⁺ is tumour-supporting — NAMPT *inhibitors* are anticancer agents precisely because tumours are NAD-avid, and NMN increased lesion burden in cancer-prone mice; raising NAD⁺ in a child with a cancer-predisposition syndrome and a prior malignancy cuts against that. And North's chain is **age-related** NAD⁺ decline — a young child may not be depleted, so SIRT2 may not be substrate-limited and E3 could read flat for reasons unrelated to the hypothesis |
| 2 | **CBP/p300 inhibitor** (A-485, CCS1477/inobrodib) | Inhibit the *writer* of the K668 mark and BubR1 should rise. The one case where an available inhibitor points the right way | **5** | 2 | **1** | 3 | **The mechanism may run backwards.** CBP/p300 is the H3K27ac writer at active enhancers, and catalytic inhibitors (A-485, CCS1477) broadly suppress enhancer-driven transcription — so they plausibly lower *BUB1B* mRNA while blocking K668 acetylation. Net effect unknown, possibly negative; one western answers it. The K250 counter-argument does *not* apply (§2: PCAF, prometaphase). Also: never tested for this, pleiotropic, no paediatric data |
| 3 | **PTC readthrough** ± NMD inhibition | Attacks the *other* allele. `c.2210T>G` creates **TGA** — the most readthrough-permissive stop codon, though the +4 base is **A**, second from the bottom of the C > U > A ≥ G context hierarchy. **And the product is not wild type**: UGA readthrough inserts Trp, Cys or Arg, never Leu, so success yields `p.Leu737Trp/Cys/Arg` of unknown function | 4 | **1** | see below | see below | NMD destroys the transcript before a ribosome reaches the PTC (gated by **E6a**); the +4 base is A, an intermediate context; and the agents differ so widely on access and safety that a single score for the row would be meaningless |
| 4 | **Hydroxychloroquine** | Autophagy inhibition; chloroquine is one of three compounds identified as aneuploidy-selective. Aneuploid cells lean on autophagy to clear proteotoxic load | 3 | 3 | **5** | 4 | Constitutional cells are aneuploid too, so "selective" is degree not kind; retinal toxicity is dose-limiting |
| 5 | **Dasatinib (+ quercetin)** | Senolytic clearance of p16^Ink4a-positive cells, which rescued skeletal muscle and adipose **in the BubR1 progeroid mouse** — the tissues this child is symptomatic in | 4 | **3** | 3 | 3 | BubR1^H/H mice are progeroid and a child is not; senescent burden may be low at this age; needs oncology sign-off given cancer predisposition |
| 6 | **Genomic correction** — prime editing of `c.2210T>G`, with epigenetic activation as the less durable alternative | Permanently revert the **nonsense** allele. Not repurposing; included because it shares candidates 1, 2 and 3's validated premise, and because a genomic edit is the one route immune to the durability problem that defeats every other | 4 | 3 | **2** | **1** | Systemic requirement vs tissue-restricted delivery; possible dominant-negative from upregulating the truncated allele; persistent transcriptional activator in a cancer-predisposition background |
| — | *HDAC inhibitors* | Reachable from BUB1B via HDAC1–4, and BubR1 abundance is acetylation-controlled | 2 | 1 | 3 | 3 | **Direction unresolved** — SIRT2 is class III and is not inhibited by these agents. A question, not a candidate |

**A stated criterion for the evidence column, and two scores it changes.** "Strength of published support" is too loose to be checkable, so it is resolved here into one question: **was the proposed modality itself tested, or only a genetic proxy for it?** An experiment that administers the actual class of intervention and measures the actual molecular outcome is worth more than one that establishes the principle by genetic means and leaves the drug as an inference.

Applying it moves two scores in opposite directions.

- **Candidate 1 rises from 3 to 4.** In `BubR1^H/H` mice, **NMN was administered and BubR1 was stabilised in vivo** — the proposed modality, in the correct gene's model, with the molecular outcome this report is trying to produce, and the SIRT2 arm supplies the genetic confirmation alongside it. Very few repurposing hypotheses have that.
- **Candidate 5 falls from 4 to 3.** The founding senolytics experiment cleared p16^Ink4a-positive cells with the **INK-ATTAC transgene** and a dimerizer — genetic ablation. Dasatinib and quercetin were never given to a `BubR1^H/H` mouse. The tissue rescue is real and it is in the right gene, but the step from "removing senescent cells helps" to "these two drugs will remove them here" is an inference, not a result.

Neither is a criticism of the underlying work. It is a statement about how far each result travels toward *this* patient, which is what the column is supposed to measure.

**Candidate 3's agents do not share an access profile, so they are scored separately.** Collapsing them into one number was hiding a factor-of-five spread.

| Agent | Regulatory status | Access | Safety | Note |
|---|---|---|---|---|
| **Ataluren** (Translarna) | EU authorisation **not renewed, 28 Mar 2025**; never approved in the US, where it remains investigational; retained in the UK | **1** | 3 | Expanded-access or compassionate-use route only. Not an off-the-shelf option in any sense |
| **ELX-02** | Investigational, clinical development | **1** | ? | Trial enrolment only |
| **Gentamicin / aminoglycosides** | Approved worldwide, stocked in every hospital pharmacy | **5** | **2** | Access is not the constraint. Toxicity is — and it is patient-specific here, see below |

**Two patient-specific findings change the aminoglycoside assessment, and both come out of the challenge data.**

*Against.* This child has **nephrocalcinosis** (`HP:0000121`), present since birth. Aminoglycosides are characteristically nephrotoxic, and the likeliest cause of the nephrocalcinosis — loop diuretics in a 32-week neonate, as §2 of the Track 1 report argues — is itself a class that potentiates both aminoglycoside nephrotoxicity and ototoxicity. Proposing a nephrotoxic drug to a child with pre-existing renal calcification is not a generic "requires therapeutic drug monitoring" caveat. It is a specific reason this agent may be the wrong one for this patient regardless of how well readthrough works.

*In favour, and it is a real result.* Aminoglycoside-induced hearing loss is strongly modified by mitochondrial *MT-RNR1* variants, principally **m.1555A>G** and **m.1494C>T**, which convert an ordinary dose into a deafening one. The WGS answers this directly. Both positions are **reference** in this child, at **4,497×** and **4,152×** coverage respectively — deep enough to bound heteroplasmy below roughly 0.1%. The only *MT-RNR1* variant called is m.1438A>G, a common haplogroup marker with no ototoxicity association.

So the single largest *genetic* risk multiplier for aminoglycoside ototoxicity is excluded in this patient, with the sequencing depth to say so confidently. Baseline oto- and nephrotoxicity remain, and the nephrocalcinosis concern stands on its own. But this is the kind of question the challenge data can actually answer, and it is worth noting that it required nothing beyond the VCF and one query — a pharmacogenomic read-out obtained for free alongside the diagnostic one.

**On candidate 3 and the ataluren withdrawal.** This was scored 2/3 on evidence and access in an earlier draft, before checking the drug's regulatory status. The European Commission declined to renew Translarna's conditional authorisation on **28 March 2025**, following CHMP opinions in January 2024, June 2024, October 2024 and March 2025 that effectiveness had not been confirmed. That is considerably worse than "contested", and both scores are lowered accordingly.

It does not, however, kill the mechanism. The failure was in Duchenne muscular dystrophy, where readthrough must restore **dystrophin** — a 427 kDa protein — in skeletal muscle, which is close to the hardest possible test. Readthrough of a UGA codon is well documented in vitro, ELX-02 and later agents continue in development, and BubR1 is a far smaller protein where a modest percentage restored could matter, because the deficit here is one of *dose* rather than complete absence.

What the withdrawal really changes is the order of operations: it makes the cheap in vitro readthrough assay (**E6**, §8) the gate, rather than something to run after deciding the candidate is promising. Nobody should pursue this clinically without first knowing the readthrough efficiency at *this* stop codon in *this* context.

**Candidates 1 and 3 are the two that could be investigated without exposing anyone to anything** — both testable in patient-derived cells for BubR1 level and micronucleus rate before any clinical question arises. That is what §7 recommends.

### 5.1 Candidate 6 — genomic correction, and which allele to edit

*Evaluated at a reader's suggestion. One premise has to be corrected first, and it is the second time it has arisen, so it is stated here permanently: **neither allele can be called maternal or paternal.** There are no parental samples, phase was not established (Track 1 report §5: largest observed template 1,272 bp against a 10,911 bp gap, 0 of 2 heterozygous steps bridged), and nothing in a singleton genome assigns an allele to a parent. Even *trans* is inferred from the clinical diagnosis, not measured.*

**Two things about the proposal are right, and one answers an objection this report raised against itself.**

*Prime editing is the correct tool, and base editing is not.* Both variants are `T>G`, so reverting either requires **G→T**. Classical cytosine and adenine base editors perform only transitions — C→T and A→G — and cannot. Worth stating precisely, because "base editors do transitions only" is no longer true as a blanket claim: C-to-G base editors and adenine transversion editors now exist. They still do not help here. On the antisense strand the required change is **C→A**, and CGBEs write C→G while AYBEs act on adenine. **Prime editing remains the only mechanism that resolves this specific sequence**, and it is a precise technical call rather than a fashionable one.

*A genomic edit defeats the durability problem.* §4 and the epigenetic route founder on the same thing: BubR1 matters **in dividing cells**, and an activating epigenetic mark has no self-propagating equivalent of 5-methylcytosine, so it dilutes with every division. A corrected DNA sequence is copied by replication itself. **The objection that sinks epigenetic activation does not apply to genomic correction**, and that is the strongest argument in this candidate's favour.

**But the proposed edit targets the wrong allele, and this genotype settles which is right.**

Write the two alleles as contributions to total BubR1, with *x* the residual activity of the hypomorph (0 < *x* < 1):

| | Genotype | Total BubR1 |
|---|---|---|
| Now | null (0) + hypomorph (*x*) | ***x*** |
| Correct **`c.3006T>G`** (the missense, as proposed) | null (0) + WT (1) | **1** |
| Correct **`c.2210T>G`** (the nonsense) | WT (1) + hypomorph (*x*) | **1 + *x*** |

Correcting the nonsense allele yields more BubR1 than correcting the missense, **by exactly the residual activity of the allele you would otherwise have overwritten**. Both clear the clinical threshold — heterozygous carriers are healthy — but the surplus is not wasted: Baker 2013 showed that *more* BubR1 is protective, reducing tumorigenesis and extending lifespan. Correcting the nonsense allele **also retires a dominant-negative hazard — but a conditional one, and the condition matters.** `p.Leu737Ter` retains the KEN box and Bub3-binding region while losing the kinase domain, so a truncated species that binds Bub3 and Cdc20 without functioning is plausible. It is not, however, an active insult at baseline: **NMD destroys most of that transcript**, which is why the allele contributes ~0 rather than something harmful. The hazard becomes real only if NMD is bypassed — by readthrough with NMD inhibition (candidate 3), or by promoter-level upregulation. So this is a reason to prefer the nonsense edit *and* a reason candidate 3 needs **E6a** first; it is not evidence that a truncated protein is poisoning the checkpoint today. That would need a western for the truncated species, which nobody has run.

**E1 does *not* measure *x*, and an earlier draft said it did.** A western measures **abundance**; *x* was defined as residual **activity**. Worse, ~50% of control is the *healthy-carrier* result — one NMD'd null plus one normally expressed allele — so the stated prediction cannot even discriminate this child from a carrier. Measuring *x* needs a function readout: checkpoint duration under nocodazole challenge, kinetochore BubR1 by quantitative immunofluorescence, with allele-specific rescue.

**And the model itself is weaker than it looks.** The closest published genotype to this child — `BubR1^X753/L1002P`, a truncation paired with a missense **ten residues** from p.Asn1002Lys — is embryonic lethal in mouse, while this child lives. The same study found phenotype severity differing between allele pairs **at matched total BubR1 protein**. If abundance does not track severity, a model denominated in abundance cannot rank two edits. The `1 + x` arithmetic also silently adds an activity term to an abundance column, and the checkpoint is a threshold system — under saturation, `1` and `1 + x` may be the same clinical outcome.

The nonsense-edit preference survives as a *reasonable* prior, not a derived result.

**Where the delivery proposal breaks, and it is developmental rather than technical.**

- **There are no renal stem cells to target.** Human nephrogenesis ceases around 34–36 weeks of gestation; no new nephrons form postnatally. Wilms tumour arises from **nephrogenic rests** — persistent embryonic remnants — not from a maintained progenitor compartment. A renal-cortex-targeted payload aimed at "dividing stem cell niches" is aimed at a population that has largely ceased to exist in a child of this age.
- **The tumour is skeletal muscle, not marrow.** MVA1's characteristic cancers are rhabdomyosarcoma and Wilms. Muscle satellite cells are largely quiescent and mature fibres are post-mitotic syncytia — the delivery problem that muscle gene therapy has spent two decades on.
- **Most of the phenotype is not cancer, and much of it is already fixed.** Growth restriction, short stature and low muscle mass are developmental, and this child was born at 32 weeks weighing a kilogram. No edit is retroactive.
- **Partial correction in an already-mosaic disease.** In vivo editing corrects a fraction of cells, so the result is a mosaic of corrected and uncorrected ones — in a disease already defined by mosaicism. For cancer risk that is still real benefit, since risk falls roughly with the uncorrected fraction. For the systemic dose deficit it is a partial fix at best.

**Verdict.** This candidate is **stronger than the epigenetic version it replaces**, on the durability argument alone, and it absorbs it rather than sitting alongside it. It remains ranked last on **access**, which drops to 1: no in vivo prime editing programme has reached patients, and ligand-targeted extrahepatic LNP delivery to quiescent muscle satellite cells is unsolved.

The reason for keeping it in the table is unchanged and worth stating plainly: **the concept is better supported than several candidates above it and the execution is far worse.** Those are different axes, and collapsing them is how a report recommends something undeliverable. If in vivo prime editing reaches patients, this moves up — and the edit it should make is `c.2210T>G`, not `c.3006T>G`.

## 6. Contraindications

> ### ⚠ This list is about *elective additions*. It is not an argument against protocol chemotherapy.
>
> **Vincristine is a backbone agent of every standard rhabdomyosarcoma regimen — VAC, VIT and IVA.** It appears below as a microtubule-targeting agent on mechanistic grounds, and that must not be read as a reason to withhold or de-escalate curative-intent therapy in a child who has had a rhabdomyosarcoma.
>
> There is **no evidence supporting deviation from COG or EpSSG protocol chemotherapy in MVA1.** The entire therapeutic literature is two case reports pointing in opposite directions: one describing reduced-intensity chemotherapy for rhabdomyosarcoma in PCS-MVA, and one HSCT case in which reduced-intensity conditioning produced "no significant toxicity ... which would be expected in patients with chromosomal instability syndromes".
>
> This section is a mechanistic hypothesis about drugs someone might *add*. Decisions about protocol therapy belong to the treating oncology team, and nothing here informs them.

Stated as strongly as the candidates, because an analysis that cannot say what to avoid has not characterised its mechanism.

- **MPS1/TTK inhibitors** — target checkpoint signalling directly
- **Aurora B inhibitors** — impair kinetochore error correction
- **PLK1 and KIF11/Eg5 inhibitors** — mitotic-arrest-dependent mechanisms presupposing an intact checkpoint
- **HSP90 inhibitors** — see below

Not hypothetical: in PrimeKG the *only* checkpoint proteins carrying drug edges are AURKB, PLK1, TTK and CENPE — this list — while BUB1B and every other MVA gene carry none. One ligand the graph attaches to AURKB is **reversine** — whose aneuploidy-inducing activity is in fact **MPS1/TTK inhibition**, an annotation this report first repeated without auditing. The point survives corrected: the druggable checkpoint proteins remain the ones to avoid. "Find the pathway, find drugs against it" returns the contraindication list with a clean subgraph attached.

**HSP90 inhibitors moved here from the candidate list — a correction worth showing.** An earlier draft listed 17-AAG as a candidate on the strength of Amon's screen. HSP90 inhibition by 17-AAG causes **delocalisation of BUB1 and BUBR1 from kinetochores**, with CENP-H, CENP-I, CENP-E and HEC1. HSP90 with its co-chaperone SGT1 is required for kinetochore **assembly** — upstream of checkpoint signalling, not part of it — so this is a failure to build the structure, not a dampening of a signal. In a child at half BubR1 dose it attacks the protein every other hypothesis tries to preserve.

The tension was visible in our own data and we missed it: §4.5 found 44 HSP90 ligands, all inhibitors, while §5 was still proposing one. Two sections disagreeing is what a review pass is for. **Chloroquine survives** as the aneuploidy-stress candidate — same screen, but autophagy inhibition, no known kinetochore effect.

*Stated at the strength the evidence supports*: this is cell-biology evidence of kinetochore delocalisation, not clinical outcome data in MVA patients, of which there is none. It is enough to remove HSP90 inhibitors from a candidate list for this genotype. It is not a claim that any patient has been harmed.

**On radiation, two claims that must not be conflated.** The AACR Childhood Cancer Predisposition Workshop's 2024 genomic-instability update advises that **radiation exposure should be avoided** in MVA — that is about *diagnostic imaging* and cumulative carcinogenic risk in a cancer-predisposed child, not a statement about radiotherapy tolerance.

**Radiosensitivity in MVA1 is undocumented, and should not be assumed by analogy.** No published clinical or cellular radiosensitivity data exist for BUB1B-mutant patients. The syndromes with documented radiosensitivity — A-T, NBS, Fanconi, LIG4 — are **DNA double-strand-break repair** disorders. MVA1 is a **spindle assembly checkpoint** disorder; the shared label "chromosomal instability syndrome" does not transfer the phenotype. Notably, the same 2024 CCPW paper recommends therapy modification explicitly for A-T, NBS, Bloom, DC/TBD and RTS — **and says nothing at all for MVA.** Silence in a paper that addresses this for six sibling disorders is itself informative.

One further note. And any antitumour agent whose mechanism *requires* a functional checkpoint will underperform here on principle — worth knowing, because TxGNN ranks several in the top 1% of indications.

## 7. What would settle this

**E1 — Is the missense allele actually hypomorphic?** *(tests the premise everything else rests on)*
Western blot for BubR1 in patient versus control. The prediction is roughly half the protein of control, and specifically **not** absent — a null result here refutes the entire report, and an allele-specific expression assay on the transcript would say whether the shortfall is the NMD allele alone or the missense allele contributing less than a full copy.

**E2 — Does the checkpoint actually fail?** *(tests the mechanism)*
Micronucleus frequency and chromosome spreads on patient versus control, with and without a nocodazole challenge. The prediction is elevated missegregation, and it also supplies the read-out for every intervention below. This closes the loop the §4 analysis could not: the WGS bounds mosaicism in *blood* below f ≈ 0.054, but cultured fibroblasts are where MVA has always been scored.

**E3 — Do NAD⁺ precursors raise BubR1?** *(tests H1, the most specific hypothesis)*
Dose-response of nicotinamide riboside on patient cells, reading BubR1 protein level (E1) and micronucleus rate (E2). Two things make this a sharp test rather than a hopeful one. The K668 acetylation state can be measured directly by immunoprecipitation with an acetyl-lysine antibody, so the *mechanism* is observable and not merely the outcome. And SIRT2 knockdown should abolish any effect — if BubR1 rises without SIRT2, the hypothesis is wrong even though the number moved.

This is also the only route available: §4.5 found that SIRT2's sole drug edge in OptimusKG is **cambinol, an inhibitor**, and no SIRT2 activator exists in either graph. H1 has to work at the substrate level or not at all.

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

## 8. Pharmacogenomics, because the genome was already sequenced

This child is receiving oncology care now — cytotoxics, anaesthesia, antifungal and antibacterial cover through neutropenia. Every one has a CPIC-level guideline and the genotype is already in the diagnostic VCF. `08_pharmacogenomics.py` screens 17 loci with **read depth checked at every position**, because a locus with no coverage produces no call exactly like a reference locus, and reporting the two identically is how a screen lies.

| Gene | Result | Depth | Bearing on this child |
|---|---|---|---|
| **F5 Leiden** (rs6025) | **heterozygous** C>T, AD 27,27 | 59× | **Risk-stratifying, not a treatment trigger.** ASH/ISTH 2026 puts the base recommendation for paediatric solid tumours at *no prophylaxis* (very low certainty) while naming CVAD use and known thrombophilia as factors that may shift the balance. One input for a haematologist, not an indication |
| CYP2C19 | ***2/*17** diplotype (*2 het, *17 het, *3 ref) | 44–50× | Intermediate metaboliser — standard dosing with TDM, not actionable. Note CPIC flags **both** ends for voriconazole: poor metabolisers overshoot, and \*17 ultrarapid metabolisers **undershoot into treatment failure**. An earlier draft gave only half the picture |
| CYP3A5 | ***3/*3** homozygous | 50× | Non-expressor. Common (~85% in Europeans); matters only if tacrolimus is ever used |
| **DPYD** (*2A, *13, c.2846A>T, HapB3) | all reference | 42–53× | **No CPIC-actionable reduced-function allele.** Directly relevant: TxGNN ranked fluorouracil 6th |
| DPYD ***6** (rs1801160, c.2194G>A) | **heterozygous**, AD 22,10 | 33× | Found only by the widened filter. ClinVar `drug_response`, *reviewed by expert panel*, terms include `fluorouracil_response_-_Toxicity`. **But CPIC assigns it normal function** and it is not among the four actionable alleles — so it is reported, not acted on |
| TPMT (*2, *3B, *3C), NUDT15 *3 | all reference | 34–65× | No thiopurine risk allele |
| G6PD (A− 202A, A 376G) | reference | 24–29× | No haemolysis risk with rasburicase for tumour lysis |
| **MT-RNR1** m.1555A>G, m.1494C>T | reference | **4,497× / 4,152×** | No mitochondrial predisposition to aminoglycoside deafness |
| F2 20210G>A, SLCO1B1 *5 | reference | 37–38× | — |


**Not assessable, named rather than omitted:** CYP2D6 star alleles (structural variation, CYP2D7 gene conversion), UGT1A1*28 (promoter TA repeat — and irinotecan is in the rhabdomyosarcoma VIT regimen, so a real gap), HLA-B typing.

**The methodological finding.** Factor V Leiden was in the Track 1 ClinVar output all along, excluded because ClinVar files it as `CLNSIG=drug_response`, *reviewed by expert panel*, with `Thrombophilia due to activated protein C resistance` and `Pregnancy loss, recurrent` among its terms. A `Pathogenic|Likely_pathogenic` filter — what essentially every secondary-findings pipeline uses, this one included — dropped **137 non-reference calls**, twelve expert-panel reviewed.

It cost two findings. Factor V Leiden, and **DPYD\*6**, which matters more: the narrow panel let us write "no fluoropyrimidine toxicity risk allele", and the child carries an expert-panel `drug_response` *DPYD* variant. CPIC assigns \*6 normal activity and states dose adaptation is not warranted, so the corrected claim survives — *no CPIC-actionable reduced-function allele* — but the original was not earned. **The filter did not merely hide a finding; it let us assert a clean negative we had not measured**, which is more dangerous in a clinical document than a missing positive.

**A second explanation for the family's reproductive history, stated carefully.** Track 1 reads the parents' recurrent miscarriage as on-mechanism for a recessive segregation disorder — carrier parents, aneuploid conceptuses. That stands. But the child is heterozygous for Factor V Leiden, so **a parent carries it**, and recurrent pregnancy loss is among its ClinVar terms. Not mutually exclusive, and if the carrier is the mother the second is separately manageable. The FVL–pregnancy-loss association is real but modest and contested, and guidelines do not universally recommend screening — so this is **worth testing, not explaining**. Determining which parent carries it is one cheap test, and it is the kind of question a family who donated a genome might want asked.

## 9. What is actionable now, with no new science

Everything above is a hypothesis. This section is not — it is what published guidance already supports for a child with this diagnosis, and the dossier previously contained none of it.

**Cancer surveillance has a published guideline and it is specific.** The AACR Childhood Cancer Predisposition Workshop's 2024 genomic-instability update covers MVA explicitly: **renal ultrasound every 3 months from birth until age 7** for all MVA conditions including genetically unsolved ones, **radiation exposure avoided**, and **regular clinical assessment including review of systems** to detect rhabdomyosarcoma and other malignancies. Prevention column: **HPV vaccination**.

What makes MVA different from generic cancer-predisposition surveillance is as important as what it shares:
- **No whole-body MRI.** Recommended in Li-Fraumeni, constitutional MMRD and others; *not* in MVA. There is no validated rhabdomyosarcoma surveillance modality — the guideline falls back on clinical review of systems.
- **No routine bloodwork**, despite MDS/AML/ALL being in the MVA1 spectrum.
- Ultrasound is chosen partly because it needs **no sedation** — a real consideration in a child facing repeated imaging.
- Risk cannot be quantified: the guideline says the rarity of the syndrome prevents accurate risk assessment. The largest series available reports malignancy in **12 of 31** MVA1 cases.

*Cite the 2024 CCPW/SIOPE recommendation (q3m to age 7), not the "3–4 monthly to age 5" figure that circulates in secondary reviews — that is the older generic >5%-risk framework, not MVA-specific.* One documented disagreement: a 2022 single-centre review additionally advises 3-monthly fundoscopy and blood counts; CCPW endorses only the renal ultrasound. Opinion versus consensus silence, not a settled question.

**Gaps in this dossier that require no new science:**
- **UGT1A1\*28 is answerable today.** Both reports flag it as unassessable from short-read WGS with irinotecan in the VIT regimen. A targeted clinical PGx assay — fragment analysis of the promoter TA repeat — resolves it from a blood draw. Same for CYP2D6 (CNV-aware assay) and HLA-B typing.
- **Ophthalmology and neurology follow-up.** MVA1 series report ocular anomalies ~19%, seizures ~45%, Dandy-Walker ~26%. Neither report mentions eyes, seizures or neurodevelopment.
- **Late effects and fertility.** Alkylator exposure carries gonadotoxicity and second-malignancy risk — the latter of particular weight in a cancer-predisposition syndrome.
- **Nephrocalcinosis should not be filed as closed.** §2 of the Track 1 report argues prematurity is the parsimonious explanation, and that stands. But renal dysfunction is reported in ~13% of MVA1, and this dossier simultaneously uses the renal finding to argue against aminoglycosides — it cannot be both live evidence and a closed question. Baseline and serial renal function belongs in the plan regardless of aetiology, with implications for cisplatin, ifosfamide and methotrexate dosing.
- **Natural history.** Neither report says anything about prognosis. A genomic dossier handed to a family without that context reads as more optimistic than the literature supports; that conversation belongs to the clinical team, and this document should say so rather than be silent.

## 10. From one genotype to a therapeutic hierarchy

The diagnosis is not the endpoint. It **partitions the therapeutic space allele by allele**, which is the organising claim of this report and why a confirmed call mattered.

```
  chr15:40209701 T>G                          chr15:40220612 T>G
  c.2210T>G  p.Leu737Ter                      c.3006T>G  p.Asn1002Lys
  TTA → TGA, exon 17/23                       kinase domain, exon 23/23
  NMD-targeted, makes ~no protein            full length, carries K668
  of the last junction                        AlphaMissense 0.923
         │                                             │
         │ a premature termination codon               │ a protein that exists
         │ is a druggable substrate                    │ and can be stabilised
         ▼                                             ▼
  ┌──────────────────────┐              ┌────────────────────────────────┐
  │ CANDIDATE 3          │              │ CANDIDATE 1  NAD⁺ → SIRT2      │
  │ PTC readthrough      │              │ CANDIDATE 2  inhibit CBP/p300  │
  │ TGA = most permissive│              │ both act on the K668 mark      │
  │ gated by E6a (NMD)   │              │ gated by E1/E3                 │
  └──────────────────────┘              └────────────────────────────────┘
         └──────────────────┬──────────────────────────┘
                            ▼
              the compound-heterozygous state itself
              — reduced BubR1 dose, CIN, senescence —
          ┌─────────────────────────────────────────────┐
          │ CANDIDATE 4  hydroxychloroquine             │
          │ CANDIDATE 5  senolytics                     │
          │ treat the consequence, not the lesion       │
          └─────────────────────────────────────────────┘
                            │
                   ✗ CONTRAINDICATED  MPS1/TTK · Aurora B · PLK1 · KIF11 · HSP90i
                     every one of them worsens a checkpoint already at half dose
```

**Why this is not a rhetorical device.** Each branch is allele-specific in a falsifiable way, and would be *wrong* for a different MVA1 patient:

- A patient with **two truncating alleles** gets nothing from candidates 1 or 2. There is no K668 to keep deacetylated, because there is no full-length protein. They would be a candidate 3 patient exclusively.
- A patient with **two missense alleles** gets nothing from candidate 3. There is no premature termination codon to read through.
- **This child is the only configuration where all three routes are simultaneously live**, because they carry exactly one of each.

That is what "precision" should mean in a repurposing report and usually does not. The common failure is to name a disease and then propose drugs for the disease. Here the two alleles license different interventions, and the report can say which patient each one would fail in.


**The order to attempt it in.** (1) Establish the premise — **E1, E2**. (2) Candidate 1, gated by **E3** reading the K668 mark with SIRT2 knockdown as control. (3) Candidate 3, but only after **E6a** shows nonsense transcript survives NMD — one PCR decides it. (4) Candidate 2 — strongest mechanism-to-drug match, worst safety, a cell-culture question long before a clinical one. (5) Candidates 4 and 5, consequence-directed, useful mainly if the lesion-directed routes fail.

Nothing above step 1 is a treatment decision, and steps 2–4 are cell-culture experiments before they are anything else.

**What Track 1 contributed beyond the diagnosis.** The same WGS, already sequenced and paid for, excluded structural variants at the locus, bounded mosaic aneuploidy from two independent modalities, and excluded the mitochondrial variants that would make an aminoglycoside dangerous. A genome sequenced to find a diagnosis keeps paying out — the most scalable finding here.

## AI assistance disclosure

*Required by the submission rules as updated 28 August 2026.*

- **Provider / tool:** Anthropic — Claude, used via Claude Code (agentic CLI), model Claude Opus 5.
- **Plan / tier:** ⚠️ **TO BE COMPLETED BY THE SUBMITTER** — only the account holder knows the subscription tier and API terms in force.
- **Data-handling setting:** ⚠️ **TO BE COMPLETED BY THE SUBMITTER.**

**What the assistant actually did**, since "used an LLM" spans a wide range and the panel should be able to weigh it: Claude wrote and ran the entire analysis pipeline — normalisation, the ClinVar cross-reference, the locus deep-dive that found allele B, the mosaic-aneuploidy and coverage analyses, the realignment, the TxGNN and knowledge-graph work, the pharmacogenomic screen — and drafted both reports. Every quantitative claim in this document was produced by code in the linked repository and is reproducible from it.

**Independent review was also AI-driven**, and is disclosed because it changed the conclusions: three separate agent instances reviewed the dossier cold — clinical management, adversarial refutation, and experimental feasibility. They found a hard factual error, a safety-level misreading risk, a missing published surveillance guideline, a reversed finding and an ACMG miscalculation. Those corrections are documented in the reports and in `journals/` rather than silently applied.

**Human oversight:** direction, scope, judgement calls and the decision to submit were the submitter's.

## 11. References

*The first block was load-bearing and uncited until independent review.*

- **van Ree JH, et al.** BubR1 allelic effects drive phenotypic heterogeneity in mosaic-variegated aneuploidy progeria syndrome. *J Clin Invest* 2020. [126863](https://www.jci.org/articles/view/126863) — closest published model to this genotype: `BubR1^X753/L1002P`, a truncation with a missense ten residues from p.Asn1002Lys, embryonic lethal in mouse; severity differs between allele pairs **at matched total BubR1 protein**.
- **Suijkerbuijk SJE, et al.** Molecular causes for BUBR1 dysfunction in mosaic variegated aneuploidy. *Cancer Res* 2010;70:4891 — patient lines of this allele class show low overall BUBR1 abundance, impaired checkpoint, alignment defects.
- **AACR Childhood Cancer Predisposition Workshop.** Screening and surveillance in genomic instability disorders. *Clin Cancer Res* 2024;30:5009. [PMC11705613](https://pmc.ncbi.nlm.nih.gov/articles/PMC11705613/) — MVA: renal ultrasound q3m to age 7, radiation avoided, HPV vaccination.
- **CCPW schwannomatosis update.** *Clin Cancer Res* 2025;31:1400. [PMC12002630](https://pmc.ncbi.nlm.nih.gov/articles/PMC12002630/) — incidental *LZTR1* variants without personal or family history should not prompt surveillance imaging.
- **ASH/ISTH 2026.** Anticoagulant prophylaxis in paediatric patients at risk of VTE. *Blood Adv* 2026;10:4303. [PMC13276589](https://pmc.ncbi.nlm.nih.gov/articles/PMC13276589/)
- **Pejaver V, et al.** Calibration of computational tools for missense pathogenicity. *Am J Hum Genet* 2022 — REVEL 0.290–0.644 is indeterminate.
- **Tavtigian SV, et al.** A naturally scaled point system for ACMG/AMP classification. *Hum Mutat* 2020.
- **Biesecker LG, Harrison SM.** Discontinue PP5/BP6. *Genet Med* 2018.
- **Loughran G, et al.** Dual-luciferase readthrough artefacts. *EMBO J* 2025.

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
