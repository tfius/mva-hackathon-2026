# Track 2 — three-minute pitch script

Word counts are measured, not estimated — see the figure under each heading. Total 0 words. Timings below are derived from those counts at 160 wpm, which lands at 0:00; at a slower 150 wpm it runs 3:14, so keep the pace up. Nothing here is said that the report does not support.

---

**[0:00–0:22] The lesion** · 74 words

A child with rhabdomyosarcoma, growth restriction and low muscle mass, born at 32 weeks weighing a kilogram. Parents with recurrent miscarriage.

The genome gives biallelic *BUB1B*: `p.Leu737Ter`, a nonsense allele losing the whole kinase domain to nonsense-mediated decay, and in trans `p.Asn1002Lys`, a missense inside that domain seen once in one and a half million gnomAD alleles.

That call scored a full match at rank one on the leaderboard. Confirmed genotype, not a guess.

**[0:22–0:48] What breaks** · 63 words

One null allele, one partly-working copy — and that is the whole basis of what follows, because complete BubR1 loss is embryonic lethal.

BubR1 is the core of the spindle assembly checkpoint. At reduced dose it leaks, chromosomes missegregate, and you get mosaic aneuploidy and cancer.

BubR1-hypomorphic mice are also progeroid — growth retardation, muscle wasting, fat loss. This child's phenotype. The model already exists.

**[0:48–1:18] What the graph confirms, and what it gets wrong** · 70 words

We ran TxGNN zero-shot on the MVA node in PrimeKG — genuinely zero-shot, that node has no drug edges at all.

It confirmed two of our three mechanism-first hypotheses — chloroquine and dasatinib, both in the top four percent of 1,801 drugs, both reached independently from the literature.

But its top recommendations are paclitaxel, vinblastine and eribulin. Microtubule poisons, top one percent of indications, for a child whose checkpoint is already broken.

**[1:18–1:52] The result we did not expect** · 93 words

*BUB1B* has 464 edges in PrimeKG and zero drug edges. So do BUB1, BUB3, CEP57 and TRIP13 — every gene the disease touches. The path from disease to gene to drug does not exist.

We checked OptimusKG: four times denser, sixty-five sources. Same answer. BubR1 is undrugged.

And the checkpoint proteins that *are* druggable — Aurora B, PLK1, TTK — are exactly the ones you must not inhibit. One Aurora B ligand in the graph is reversine, which laboratories use to *induce* aneuploidy.

Find the pathway, find drugs against it, and you get the contraindication list.

**[1:52–2:26] What we propose instead** · 103 words

Reach the protein indirectly.

BubR1's abundance is set by acetylation at lysine 668 — written by CBP, erased by the NAD-dependent deacetylase SIRT2. In BubR1 mice, boosting NAD stabilised BubR1 in vivo, and SIRT2 overexpression raised median lifespan 58 percent.

Why that matters for *this* child: K668 is deleted on the null allele and intact on the missense one. There is a substrate to stabilise. A patient with two truncating alleles gets nothing from this. This one might.

PrimeKG contains BUB1B–SIRT2 and BUB1B–CBP. It encodes the mechanism, and lacks only the drug edge, because nicotinamide riboside is a supplement. One edge away, and blind.

**[2:26–3:00] How we would be proven wrong** · 83 words

None of this is a treatment recommendation. They are hypotheses, each falsifiable in patient cells within weeks.

Blot for BubR1 — if it is not reduced, we are wrong. Count micronuclei — if the checkpoint holds, stop. Then dose with nicotinamide riboside and watch BubR1 and the K668 acetyl mark together, with a SIRT2 knockdown as control. If BubR1 rises without SIRT2, we are wrong even though the number moved.

That is the ask. Not a trial. A blot, a chromosome spread, and a knockdown.
