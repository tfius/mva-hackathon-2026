# Rare Disease, Real Kid — MVA Hackathon 2026

Submission code and reports for the [Rare Disease, Real Kid: MVA Hackathon 2026](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/), organised by Sage Bionetworks, the MVA Society, Hugging Face and BEACON.

Team `texdata`. Both tracks.

---

## The finding

**Track 1 — biallelic *BUB1B*, mosaic variegated aneuploidy syndrome 1 (MIM 257300, ORPHA:1052).**

| | Allele A | Allele B |
|---|---|---|
| GRCh38 | `chr15:40209701 T>G` | `chr15:40220612 T>G` |
| HGVS | `ENST00000287598.11:c.2210T>G` | `ENST00000287598.11:c.3006T>G` |
| Protein | `p.Leu737Ter` | `p.Asn1002Lys` |
| Frequency | gnomAD gAF 3.3 × 10⁻⁵ | 1 allele in 1,461,878 gnomAD v4 exomes |
| Support | ClinVar Pathogenic/Likely_pathogenic for MVA1 | AlphaMissense 0.923, kinase domain |

One null allele, one hypomorphic missense — the configuration MVA1 requires, because biallelic truncating *BUB1B* is not viable.

An **Exomiser 15.1.0 run given only the eight HPO terms and the sex**, with no gene panel and no mention of BUB1B or MVA, ranks this gene first of 363 and the compound-heterozygous pair second, matched to *Mosaic variegated aneuploidy syndrome*. The manual analysis and the blind one land in the same place.

**Track 2 — three mechanism-first repurposing hypotheses**, each anchored to a published experiment in *this* gene or *this* biology, and a contraindication list of equal weight. Details in [`reports/track2-mechanism-and-repurposing.md`](reports/track2-mechanism-and-repurposing.md).

## Reports

| | |
|---|---|
| [`reports/track1-variant-report.md`](reports/track1-variant-report.md) | The variant call, how it was reached, what was excluded, and the limitations — including that phase is **not** determined and why |
| [`reports/track2-mechanism-and-repurposing.md`](reports/track2-mechanism-and-repurposing.md) | BubR1 mechanism, three hypotheses, the TxGNN/PrimeKG/OptimusKG layer, candidate table and contraindications |
| [`journals/`](journals/) | Working log, written as the work happened, including the things that went wrong |
| [`docs/mva-plan.md`](docs/mva-plan.md) | The plan, written before the analysis started |

## Three results that were not expected

**A knowledge graph cannot explain this disease, and the reason is countable.** *BUB1B* has 464 edges in PrimeKG and **zero drug edges** — as do BUB1, BUB3, CEP57 and TRIP13, every gene the MVA disease node touches. The path `MVA → BUB1B → drug` does not exist. OptimusKG, four times denser around BUB1B and drawn from 65 sources, reproduces the gap exactly. BubR1 is undrugged.

**The druggable checkpoint proteins are the contraindicated ones.** AURKB, PLK1, TTK and CENPE carry drug edges; one of the AURKB ligands in PrimeKG is **reversine**, a laboratory tool used to *induce* aneuploidy. A pipeline reasoning "find the pathway, find drugs against it" returns the contraindication list as its answer, with a clean subgraph behind it.

**No mosaic aneuploidy is detectable in blood, and that is consistent with the diagnosis.** B-allele frequencies across every autosome sit at 0.00071 ± 0.00006 excess variance, bounding per-chromosome mosaicism below f ≈ 0.054. *Variegated* aneuploidy puts a different random chromosome in each cell, so a 30% aneuploid population spread over 22 autosomes leaves each chromosome at 1–2% — below any per-chromosome test by construction. The naive version of this analysis "found" mosaicism on chr17, chr19, chr20 and chr22; that was GC and mappability bias, and it vanishes under a mapping-quality and depth-band filter.

## Layout

```
mva/
  env/          environment setup; clear_execstack.py
  src/mva/      gene panels, Ensembl helpers, VEP REST client
  track1/       00 reference · 01 normalise · 02 ClinVar · 03 locus deep-dive
                04 mosaic aneuploidy · 05 realign · 06 coverage and SV
                exomiser/  unbiased HPO-only run
  track2/       01 TxGNN zero-shot · 02 degree-controlled ranking
                03 GraphMask path explanation · 04 OptimusKG coverage
                05 mechanism-anchored reachability
  results/      submission CSV and report
reports/        the two submission reports
journals/       daily working log
external/       third-party checkouts (not committed)
```

## Reproducing

Everything runs from the challenge VCF and FASTQs plus public reference data. `mva/env/download_refs.sh` and `download_refs2.sh` fetch GRCh38, ClinVar, AlphaMissense, Exomiser 15.1.0 with the 2512 hg38 bundle, and the Ensembl VEP 116 cache. Environments are micromamba; `mva/env/clear_execstack.py` is needed for PyTorch 1.10, whose executable-stack flag Linux 6+ refuses to load.

Two workarounds worth knowing about if you hit them: pandas 2 removed `DataFrame.append`, which TxGNN needs (pin 1.5.3), and Harvard Dataverse returns 403 to the default `python-requests` User-Agent while serving curl the identical URL.

## Data handling

The challenge data belongs to a real child and their family. It stays outside this repository — under `/mnt/data/mva-hackathon-2026/`, excluded by `.gitignore` — and will be deleted at the close of the hackathon with notification to `MVAHackathon2026@synapse.org`, as the data-use terms require. No attempt was made to re-identify or contact the family.

The variant coordinates appear in the reports because they *are* the submitted research output, which the hackathon publishes under CC BY 4.0. That is the deliverable; the underlying sequence data is not, and is not here.

## Licences

Code and reports CC BY 4.0, matching the hackathon terms. AlphaMissense is CC BY-NC-SA 4.0 and is used under its non-commercial terms. ClinVar, gnomAD, Ensembl, UniProt, PrimeKG, OptimusKG, TxGNN and Exomiser under their respective licences.

## Acknowledgement

To the child and family who chose to share a genome with strangers, and to the MVA Society, Sage Bionetworks, Hugging Face and BEACON for making it possible to do anything useful with it.
