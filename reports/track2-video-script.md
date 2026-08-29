# Track 2 — three-minute pitch script

Total 505 spoken words. Section timings are derived from those counts at 160 wpm, landing at 3:09; at a relaxed 150 wpm it runs 3:16, so keep the pace up. Nothing here is said that the report does not support.

---

**[0:00–0:27] The lesion** · 74 words · 28s

A child with rhabdomyosarcoma, growth restriction and low muscle mass, born at 32 weeks weighing a kilogram. Parents with recurrent miscarriage.

The genome gives biallelic *BUB1B*: `p.Leu737Ter`, a nonsense allele losing the whole kinase domain to nonsense-mediated decay, and in trans `p.Asn1002Lys`, a missense inside that domain seen once in one and a half million gnomAD alleles.

That call scored a full match at rank one on the leaderboard. Confirmed genotype, not a guess.

**[0:27–0:51] What breaks** · 63 words · 24s

One null allele, one partly-working copy — and that is the whole basis of what follows, because complete BubR1 loss is embryonic lethal.

BubR1 is the core of the spindle assembly checkpoint. At reduced dose it leaks, chromosomes missegregate, and you get mosaic aneuploidy and cancer.

BubR1-hypomorphic mice are also progeroid — growth retardation, muscle wasting, fat loss. This child's phenotype. The model exists.

**[0:51–1:17] What the graph confirms, and what it gets wrong** · 70 words · 26s

We ran TxGNN zero-shot on the MVA node in PrimeKG — that node has no drug edges at all.

It confirmed two of our three mechanism-first hypotheses, both in the top four percent of 1,801 drugs, both reached independently from the literature.

But its top recommendations are paclitaxel, vinblastine and eribulin. Microtubule poisons, top one percent of indications, for a child whose checkpoint is already broken.

**[1:17–1:52] The result we did not expect** · 93 words · 35s

*BUB1B* has 464 edges in PrimeKG and zero drug edges. So do BUB1, BUB3, CEP57 and TRIP13 — every gene the disease touches. The path from disease to gene to drug does not exist.

We checked OptimusKG: four times denser, sixty-five sources. Same answer. BubR1 is undrugged.

And the checkpoint proteins that *are* druggable — Aurora B, PLK1, TTK — are exactly the ones you must not inhibit. One Aurora B ligand in the graph is reversine, which laboratories use to *induce* aneuploidy.

Find the pathway, find drugs against it, and you get the contraindication list.

**[1:52–2:33] What we propose instead** · 109 words · 41s

Reach the protein indirectly.

BubR1's abundance is set by acetylation at lysine 668 — written by CBP, erased by the NAD-dependent deacetylase SIRT2. So there are two ways up.

Raise NAD, and SIRT2 keeps the mark off — in BubR1 mice that stabilised BubR1 in vivo. Or inhibit the writer: CBP/p300 inhibitors exist and are in trials. An inhibitor pointed the right way.

Why this child specifically — the missense allele makes full-length protein carrying K668; the nonsense allele is destroyed before it makes any. There is a substrate to stabilise. Two truncating alleles would get nothing.

PrimeKG already knows CBP touches BubR1. It cannot say which direction helps. That is the gap.

**[2:33–3:04] How we would be proven wrong** · 83 words · 31s

None of this is a treatment recommendation. They are hypotheses, each falsifiable in patient cells within weeks.

Blot for BubR1 — if it is not reduced, we are wrong. Count micronuclei — if the checkpoint holds, stop. Then dose with nicotinamide riboside and watch BubR1 and the K668 acetyl mark together, with a SIRT2 knockdown as control. If BubR1 rises without SIRT2, we are wrong even though the number moved.

That is the ask. Not a trial. A blot, a chromosome spread, and a knockdown.
