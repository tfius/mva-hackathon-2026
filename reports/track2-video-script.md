# Track 2 — three-minute pitch script

Written to be spoken. Short sentences, no nested clauses, no unpronounceable variant nomenclature — put `p.Leu737Ter` and `p.Asn1002Lys` on the slide, say "nonsense" and "missense". Total **478 words** — 2:59 at 160 wpm, 3:11 at a relaxed 150. Counts measured, timings derived.

Delivery notes: the two beats that carry this pitch are **1:14** and **2:24**. Slow down for both. Everything before 1:14 is setup and can be brisk.

---

**[0:00–0:26] The lesion** · 70 words · 26s

A child with rhabdomyosarcoma, growth restriction and low muscle mass. Born at 32 weeks weighing a kilogram. Parents with recurrent miscarriage.

The genome gives biallelic *BUB1B*. One nonsense allele, destroyed before it makes protein. And in trans, a missense inside the kinase domain — seen once in one and a half million gnomAD alleles.

That call scored a full match at rank one on the leaderboard. Confirmed genotype, not a guess.

**[0:26–0:49] What breaks** · 61 words · 23s

One dead allele. One partly-working copy. That is the whole basis of what follows, because complete BubR1 loss is embryonic lethal.

BubR1 is the core of the spindle assembly checkpoint. At reduced dose it leaks. Chromosomes missegregate. You get mosaic aneuploidy, and cancer.

BubR1-hypomorphic mice are also progeroid — growth retardation, muscle wasting, fat loss. This child's phenotype. The model already exists.

**[0:49–1:13] What the graph gets right, and wrong** · 66 words · 25s

We ran TxGNN zero-shot on the MVA node in PrimeKG. That node has no drug edges at all.

It confirmed two of our three mechanism-first hypotheses. Both in the top four percent of eighteen hundred drugs. Both reached independently, from the literature.

But its own top recommendations are paclitaxel, vinblastine, eribulin. Microtubule poisons. Top one percent of indications — for a child whose checkpoint is already broken.

**[1:13–1:47] The result we did not expect** · 90 words · 34s

*BUB1B* has 464 edges in PrimeKG and zero drug edges. So does every other gene this disease touches. The path from disease, to gene, to drug does not exist.

We checked OptimusKG. Four times denser. Sixty-five independent sources. Same answer. **BubR1 is undrugged.**

And the checkpoint proteins that *are* druggable — Aurora B, PLK1, TTK — are exactly the ones you must not inhibit here. One of them is reversine. Laboratories use it to *induce* aneuploidy.

Find the pathway, find drugs against it, and what you get back is the contraindication list.

**[1:47–2:27] What we propose instead** · 106 words · 40s

So reach the protein indirectly.

BubR1's abundance is set by acetylation at one lysine. CBP writes that mark, and the mark triggers degradation. The NAD-dependent deacetylase SIRT2 removes it, and the protein survives.

That gives two ways up. Raise NAD, so SIRT2 keeps the mark off — in BubR1 mice, that stabilised the protein in vivo. Or inhibit the writer. CBP inhibitors exist, and they are in trials. An inhibitor pointed the right way.

And this child's missense allele still makes full-length protein carrying that lysine. There is something to stabilise.

PrimeKG already knows CBP touches BubR1. It cannot say which direction helps. That is the gap.

**[2:27–2:59] How we would be proven wrong** · 85 words · 32s

None of this is a treatment recommendation. They are hypotheses, and each one is falsifiable in patient cells.

Blot for BubR1 — if it is not reduced, we are wrong. Count micronuclei — if the checkpoint holds, stop. Then dose with nicotinamide riboside, and watch the protein and the acetyl mark together, with SIRT2 knocked down as the control. If BubR1 rises without SIRT2, we are wrong even though the number moved.

That is the ask. Not a trial. A blot, a chromosome spread, and a knockdown.
