# Rare Disease, Real Kid — MVA Hackathon 2026

Submission for the [Rare Disease, Real Kid: MVA Hackathon 2026](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/) — Sage Bionetworks, the MVA Society, Hugging Face and BEACON. Team `texdata`. Both tracks.

---

## Track 1 — solved

**Biallelic *BUB1B*, mosaic variegated aneuploidy syndrome 1** (MIM 257300, ORPHA:1052).

| | Allele A | Allele B |
|---|---|---|
| GRCh38 | `chr15:40209701 T>G` | `chr15:40220612 T>G` |
| HGVS | `ENST00000287598.11:c.2210T>G` | `ENST00000287598.11:c.3006T>G` |
| Protein | `p.Leu737Ter` | `p.Asn1002Lys` |
| Frequency | gnomAD genomes 3.3 × 10⁻⁵ | **1 allele in 1,461,878** gnomAD v4 exomes |
| Support | ClinVar Pathogenic/Likely_pathogenic for MVA1 | AlphaMissense 0.923, kinase domain |

> **Scored 100.0/100 rank points, F-max 1.000, full match at rank 1** against the clinically confirmed answer key. One null allele and one hypomorphic missense — the configuration MVA1 requires, since biallelic truncating *BUB1B* is not viable.

Allele B is in no clinical database. It surfaced only because the locus was worked exhaustively — 175 non-reference calls across *BUB1B* ±50 kb, classified by exon position — rather than filtered by predicted consequence. A conventional rare-variant chain finds the nonsense and stops.

An **Exomiser run given only the eight HPO terms and the sex**, with no gene panel, ranked *BUB1B* first of 363 genes and the compound-heterozygous pair second, matched to *Mosaic variegated aneuploidy syndrome*.

## Track 2 — mechanism and repurposing

Six candidates reaching one target — **more BubR1** — from independent directions: supply the cofactor (NAD⁺/SIRT2), inhibit the writer of the destabilising acetyl mark (CBP/p300), rescue the null allele (PTC readthrough), or correct it genomically. **None requires a drug that binds BubR1, because none exists.**

Full analysis, candidate table, contraindications and validation plan in [`reports/track2-mechanism-and-repurposing.md`](reports/track2-mechanism-and-repurposing.md).

## Findings

**A knowledge graph cannot explain this disease, and the reason is countable.** *BUB1B* has 464 edges in PrimeKG and **zero drug edges** — as do BUB1, BUB3, CEP57 and TRIP13, every gene the MVA node touches. `MVA → BUB1B → drug` cannot exist. OptimusKG, four times denser and drawn from 65 independent sources, reproduces the gap exactly. **BubR1 is undrugged**, and that is a fact about pharmacology rather than about any one graph.

**The druggable checkpoint proteins are the contraindicated ones.** AURKB, PLK1, TTK and CENPE carry drug edges; BUB1B carries none. A pipeline reasoning "find the pathway, find drugs against it" returns the contraindication list with a clean subgraph attached. (One ligand the graph attaches to AURKB is reversine — whose aneuploidy-inducing activity is in fact MPS1/TTK inhibition. We repeated that annotation uncritically at first, in a report arguing that annotations need auditing.)

**The model's top recommendations are contraindicated by mechanism.** TxGNN ranks paclitaxel 7th of 1,801 on *indications*, vinblastine 17th. The graph knows MVA is a cancer-predisposition syndrome and retrieves sarcoma chemotherapy; it cannot know the checkpoint is already at half dose, because that lives in the variant.

**Two distinct blind spots, and only one is about size.** A *schema* gap — nicotinamide riboside does not bind SIRT2, it raises the NAD⁺ SIRT2 consumes, and no graph encodes "increases availability of a cofactor", so substrate-pool interventions are invisible at any scale. And a *semantics* gap — CREBBP and EP300 are already in PrimeKG as BUB1B interactors, and the graph still cannot say that *inhibiting* them should raise BubR1.

**A standard secondary-findings filter asserts negatives it has not earned.** Filtering ClinVar to `Pathogenic|Likely_pathogenic` dropped **137 non-reference calls** on this genome, twelve reviewed by expert panel. It hid Factor V Leiden, and it let us write "no fluoropyrimidine toxicity risk allele" when the child carries an expert-panel `drug_response` *DPYD* variant.

**No mosaic aneuploidy is detectable in blood, and that is consistent with the diagnosis.** Bounded below f ≈ 0.054 by B-allele frequency and f ≈ 0.097 by read depth. *Variegated* aneuploidy puts a different random chromosome in each cell, so a 30% aneuploid population across 22 autosomes leaves each chromosome below any per-chromosome test. Both naive versions of that analysis produced false positives on the GC-rich chromosomes; the filters are the result.

## Independent review

Three independent agents reviewed the dossier cold — clinical management, adversarial refutation, and experimental feasibility. They found more than a dozen self-review passes had, and the corrections are documented in the reports and [`journals/`](journals/) rather than quietly applied:

- **A hard factual error, stated three times** — "K668 is deleted on the null allele" is false; `p.Leu737Ter` stops after residue 736 and 668 < 737.
- **A safety-level misreading risk** — vincristine is a backbone agent of every standard rhabdomyosarcoma regimen and appeared in our contraindication list. §6 now opens with an explicit guard.
- **A published surveillance guideline the dossier lacked** — renal ultrasound q3m from birth to age 7, radiation avoided, HPV vaccination.
- **A finding stated backwards** — an incidental *LZTR1* variant should not prompt surveillance imaging.
- **ACMG arithmetic that did not reach its stated conclusion** — 4 points is VUS, not Likely pathogenic.

## Layout

```
mva/
  env/          setup; clear_execstack.py (PF_X on PT_GNU_STACK, for PyTorch 1.10 on kernel 7)
  src/mva/      gene panels, Ensembl helpers, VEP REST client
  track1/       00 reference · 01 normalise · 02 ClinVar · 03 locus deep-dive
                04 mosaic aneuploidy (BAF) · 05 realign · 06 coverage+SV
                07 phasing attempt · 08 aneuploidy from depth · 09 SV panel intersect
                exomiser/  unbiased HPO-only run
  track2/       01 TxGNN zero-shot · 02 degree-controlled ranking · 03 GraphMask paths
                04 OptimusKG coverage · 05 mechanism-anchored reachability
                06 same on OptimusKG · 07 alternative targets · 08 pharmacogenomics
  results/      submission CSV, both reports, calendar
reports/        Track 1 and Track 2 submissions, pitch script
journals/       daily working log, including what went wrong
external/       third-party checkouts (not committed)
```

## Reproducing

Everything runs from the challenge VCF and FASTQs plus public reference data. `mva/env/download_refs.sh` and `download_refs2.sh` fetch GRCh38, ClinVar, AlphaMissense, Exomiser 15.1.0 with the 2512 hg38 bundle, and the Ensembl VEP 116 cache.

Three workarounds worth knowing: pandas 2 removed `DataFrame.append`, which TxGNN needs (pin 1.5.3); Harvard Dataverse returns 403 to the default `python-requests` User-Agent while serving curl the identical URL; and PyTorch 1.10's executable-stack flag blocks loading on Linux 6+.

## Identifiers

`WGS_EX2312012` and `HGWCNDSX7` are the organisers' own library and flow-cell names, already present in the challenge dataset's filenames and required for reproducibility. They are not patient identifiers.

## Data handling

The challenge **sequence data** stays outside this repository, under `/mnt/data/`, excluded by `.gitignore`, and will be deleted at the close of the hackathon with notification to `MVAHackathon2026@synapse.org`. No attempt was made to re-identify or contact the family.

**This repository is nonetheless patient-derived, and says so rather than blurring it.** The reports contain variant coordinates, sex, gestational age, birth weight, a malignancy and a pharmacogenomic profile. The hackathon's terms provide for exactly this — submissions, code and reports are published CC BY 4.0 and the research output *is* the deliverable — but the honest framing is "the raw data stays private and the derived findings are published, as the terms require", not "nothing patient-derived leaves this machine".

## Licences

Code and reports CC BY 4.0, matching the hackathon terms. AlphaMissense is CC BY-NC-SA 4.0 and used under its non-commercial terms. ClinVar, gnomAD, Ensembl, UniProt, PrimeKG, OptimusKG, TxGNN and Exomiser under their respective licences.

## Acknowledgement

To the child and family who chose to share a genome with strangers, and to the MVA Society, Sage Bionetworks, Hugging Face and BEACON for making it possible to do anything useful with it.
