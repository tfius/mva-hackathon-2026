# Track 2 — three-minute pitch script

Draft for recording. Timings are speaking-pace estimates at ~150 wpm. Nothing here should be said that the report does not support.

---

**[0:00–0:25] The lesion, precisely**

A child with rhabdomyosarcoma, growth restriction, low muscle mass, born at 32 weeks weighing about a kilogram — and a family history of recurrent miscarriage.

The genome gives biallelic *BUB1B*: a nonsense allele, `p.Leu737Ter`, that stops 30 residues short of the kinase domain, losing it entirely and is predicted to be destroyed by nonsense-mediated decay — and in trans, `p.Asn1002Lys`, a missense inside the kinase domain seen once in one and a half million gnomAD alleles.

One null. One partly-working copy. That is not an incidental detail — it is the whole basis of what follows, because complete BubR1 loss is embryonic lethal. Every child with this syndrome has residual protein.

**[0:25–0:50] What breaks**

BubR1 is the core of the spindle assembly checkpoint — the mechanism that stops a cell dividing until every chromosome is properly attached. At reduced dose the checkpoint leaks, chromosomes missegregate, and you get mosaic aneuploidy and a cancer predisposition.

There is a second consequence that matters more for treatment. BubR1-hypomorphic mice are progeroid: growth retardation, muscle wasting, fat loss. That is this child's phenotype, and it means there is a mouse model in which interventions have already been run on this exact gene.

**[0:50–1:20] What the knowledge graph says — and what it cannot say**

We ran TxGNN zero-shot on the mosaic variegated aneuploidy node in PrimeKG. Genuinely zero-shot: that node has 214 phenotype edges, five genes, and no drug edges at all.

Two of our three mechanism-first hypotheses came back independently confirmed. Chloroquine and hydroxychloroquine at the 2.8th percentile of 1,801 drugs — chloroquine being one of the three compounds identified in Amon's aneuploidy-selective screen. Dasatinib at 3.8% — the approved half of the senolytic pair whose founding experiment used the BubR1 mouse.

But the model's top recommendations are paclitaxel, vinblastine and eribulin. Microtubule poisons. In the top one percent of *indications* for a child whose spindle checkpoint is already broken.

**[1:20–1:50] The result we did not expect**

*BUB1B* has 464 edges in PrimeKG and **zero drug edges**. So do BUB1, BUB3, CEP57, TRIP13 — every gene the disease connects to. The path from disease to gene to drug does not exist.

We checked OptimusKG, four times denser around BUB1B, built from 65 independent sources. Same answer. BubR1 is undrugged.

And the checkpoint proteins that *are* druggable — Aurora B, PLK1, TTK — are precisely the ones you must not inhibit here. One of the Aurora B ligands in the graph is reversine, which laboratories use to *induce* aneuploidy.

A pipeline that reasons "find the pathway, find drugs against it" returns the contraindication list as its answer, with a clean-looking explanation subgraph attached.

**[1:50–2:30] What we propose instead**

Reach the protein indirectly.

BubR1's abundance is set by acetylation at lysine 668 — written by CBP, erased by the NAD⁺-dependent deacetylase SIRT2. In BubR1-hypomorphic mice, boosting NAD⁺ stabilised BubR1 in vivo and SIRT2 overexpression raised median lifespan by 58 percent.

Here is why that matters for *this* child specifically: **K668 is deleted on the null allele but intact on the missense one.** There is a substrate to stabilise. A patient with two truncating alleles would get nothing from this. This one might.

PrimeKG contains BUB1B–SIRT2 and BUB1B–CBP. It encodes the entire mechanism. What it lacks is a drug edge, because nicotinamide riboside is a supplement with no indication records. The graph was one edge away and could not see it.

**[2:30–3:00] How we would be proven wrong**

None of this is a treatment recommendation. They are hypotheses, and every one is falsifiable in patient cells within weeks.

Blot for BubR1 — if it is not reduced, the whole report is wrong. Count micronuclei — if the checkpoint is not failing, stop. Then dose patient cells with nicotinamide riboside and watch BubR1 protein and the K668 acetyl mark together, with a SIRT2 knockdown as the control: if BubR1 rises without SIRT2, we are wrong even though the number moved.

That is what we are asking for. Not a trial. A blot, a chromosome spread, and a knockdown.
