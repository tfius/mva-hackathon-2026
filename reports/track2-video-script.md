# Track 2 — three-minute pitch script

~450 spoken words, which is 3:00 at 150 wpm and 3:12 at 140. Timings are counted, not estimated. Nothing here is said that the report does not support.

---

**[0:00–0:22] The lesion**

A child with rhabdomyosarcoma, growth restriction and low muscle mass, born at 32 weeks weighing a kilogram. Parents with a history of recurrent miscarriage.

The genome gives biallelic *BUB1B*. A nonsense allele, `p.Leu737Ter`, which loses the entire kinase domain and is predicted to be destroyed by nonsense-mediated decay. And in trans, `p.Asn1002Lys` — a missense inside that same domain, seen once in one and a half million gnomAD alleles.

That call scored a full match at rank one on the challenge leaderboard. It is the confirmed genotype, not our guess.

**[0:22–0:48] What breaks**

One null allele. One partly-working copy. That is not a detail — it is the whole basis of what follows, because complete BubR1 loss is embryonic lethal.

BubR1 is the core of the spindle assembly checkpoint, which stops a cell dividing until every chromosome is properly attached. At reduced dose the checkpoint leaks, chromosomes missegregate, and you get mosaic aneuploidy and cancer.

And BubR1-hypomorphic mice are progeroid — growth retardation, muscle wasting, fat loss. That is this child's phenotype. So the mouse model already exists.

**[0:48–1:18] What the graph confirms, and what it gets wrong**

We ran TxGNN zero-shot on the MVA node in PrimeKG. Genuinely zero-shot — that node has no drug edges at all.

Two of our three mechanism-first hypotheses came back confirmed. Chloroquine and hydroxychloroquine in the top three percent of 1,801 drugs — chloroquine being one of three compounds from Amon's aneuploidy-selective screen. Dasatinib at four percent, the approved half of the senolytic pair whose founding experiment used the BubR1 mouse.

But the model's top recommendations are paclitaxel, vinblastine and eribulin. Microtubule poisons, in the top one percent of indications, for a child whose checkpoint is already broken.

**[1:18–1:52] The result we did not expect**

*BUB1B* has 464 edges in PrimeKG and zero drug edges. So do BUB1, BUB3, CEP57 and TRIP13 — every gene the disease touches. The path from disease to gene to drug does not exist.

We checked OptimusKG. Four times denser, sixty-five independent sources. Same answer. BubR1 is undrugged.

And the checkpoint proteins that *are* druggable — Aurora B, PLK1, TTK — are precisely the ones you must not inhibit. One Aurora B ligand in the graph is reversine, which laboratories use to *induce* aneuploidy.

Find the pathway, find drugs against it, and you get the contraindication list — with a clean subgraph attached.

**[1:52–2:26] What we propose instead**

Reach the protein indirectly.

BubR1's abundance is set by acetylation at lysine 668 — written by CBP, erased by the NAD-dependent deacetylase SIRT2. In BubR1 mice, boosting NAD stabilised BubR1 in vivo, and SIRT2 overexpression raised median lifespan by 58 percent.

Why that matters for *this* child: K668 is deleted on the null allele and intact on the missense one. There is a substrate to stabilise. A patient with two truncating alleles gets nothing from this. This one might.

PrimeKG contains BUB1B–SIRT2 and BUB1B–CBP. It encodes the mechanism. It lacks only the drug edge, because nicotinamide riboside is a supplement. One edge away, and blind.

**[2:26–3:00] How we would be proven wrong**

None of this is a treatment recommendation. They are hypotheses, and each is falsifiable in patient cells within weeks.

Blot for BubR1 — if it is not reduced, we are wrong. Count micronuclei — if the checkpoint holds, stop. Then dose with nicotinamide riboside and watch BubR1 and the K668 acetyl mark together, with a SIRT2 knockdown as the control. If BubR1 rises without SIRT2, we are wrong even though the number moved.

That is the ask. Not a trial. A blot, a chromosome spread, and a knockdown.
