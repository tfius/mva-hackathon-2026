# Track 1 — Variant Prediction Report

**Rare Disease, Real Kid: MVA Hackathon 2026** · proband `PROBAND01` (`WGS_EX2312012`)
Team `texdata` · GRCh38 · 28 August 2026

---

## 1. The call

**Biallelic *BUB1B* (15q15.1) — mosaic variegated aneuploidy syndrome 1 (MVA1, MIM 257300), autosomal recessive, compound heterozygous.**

| | Allele A | Allele B |
|---|---|---|
| GRCh38 | `chr15:40209701 T>G` | `chr15:40220612 T>G` |
| HGVS c. | `ENST00000287598.11:c.2210T>G` | `ENST00000287598.11:c.3006T>G` |
| HGVS p. | `p.Leu737Ter` | `p.Asn1002Lys` |
| Consequence | stop_gained, exon 17/23 | missense, exon 23/23 |
| Genotype | 0/1 · AD 21,25 · DP 46 · GQ 99 | 0/1 · AD 15,13 · DP 28 · GQ 99 |
| Population frequency | gnomAD genomes 3.29 × 10⁻⁵ (rs759242053) | **1 allele in 1,461,878** gnomAD v4 exomes (AF 6.8 × 10⁻⁷); absent from gnomAD genomes and from dbSNP |
| In silico | PTC 746 nt upstream of the final exon–exon junction → NMD predicted | AlphaMissense 0.923, MVP 0.852, REVEL 0.472 |
| Exomiser ACMG | **PATHOGENIC** — PVS1, PM2_Supporting, PP4_Moderate, PP5_Strong | **UNCERTAIN_SIGNIFICANCE** — PM2_Supporting, PP4_Moderate, BP1 |
| ClinVar | **Pathogenic/Likely_pathogenic**, "Mosaic variegated aneuploidy syndrome 1" | novel nucleotide; `c.3006T>A`, the *same* p.Asn1002Lys substitution, is a ClinVar VUS |

This is the configuration MVA1 is known for: one null allele paired with one hypomorphic missense. Complete biallelic loss of BUB1B is not compatible with life, so surviving patients essentially always retain partial function on one allele.

## 2. Why these two, mechanistically

BUB1B encodes BubR1, the pseudokinase core of the mitotic spindle assembly checkpoint. UniProt O60566: 1050 aa, BUB1 N-terminal domain 62–226, protein kinase domain **766–1050**, catalytic proton acceptor D882.

- **`p.Leu737Ter`** stops the product after residue 736 — **30 residues short of the kinase domain**, which is lost entirely. The premature termination codon sits at c.2209–2211, and the final exon–exon junction is at c.2957/c.2958, so the PTC is 746 nt upstream of it and far past the 50–55 nt boundary: nonsense-mediated decay is predicted, and the allele is a true null. Even on transcript that escaped NMD, the product would lack the entire kinase domain.
- **`p.Asn1002Lys`** sits *inside* the kinase domain, 120 residues C-terminal to the active site, and swaps a neutral amide for a positive charge. AlphaMissense 0.923 and MVP 0.852, though REVEL is only 0.472 — the predictors do not agree, and that disagreement is reported rather than averaged away. It appears **once** in 1,461,878 gnomAD v4 exome alleles and not at all in gnomAD genomes: essentially private. The identical amino-acid substitution reached by a different nucleotide (`c.3006T>A`) is already in ClinVar as a VUS — independent evidence that the residue is under clinical scrutiny — while `c.3006T>C`, which is synonymous, is classified Likely benign. The classification tracks the protein change, not the position.

Phenotype fit: rhabdomyosarcoma is the MVA1-defining malignancy (with Wilms tumour), and intrauterine growth restriction, short stature and failure to thrive are core MVA1 features. Parental recurrent pregnancy loss is on-mechanism for carrier parents of a chromosome-segregation disorder, not incidental history.

Nephrocalcinosis is *not* a recognised MVA1 feature. Present since birth in a 32-week, ~1 kg infant, it is far better explained by prematurity — loop diuretics and parenteral nutrition — than by a second genetic diagnosis. It is reported here as explained, not as unexplained.

## 3. How the call was reached

The pipeline is in `mva/track1/`. Data never leaves `/mnt/data`; nothing patient-derived is committed.

**S1 · Normalisation** (`01_normalize.sh`). The challenge VCF is Sentieon Haplotyper → GVCFtyper with GATK `VariantFiltration`, on GRCh38 with **unprefixed contig names** (`1`, not `chr1`) and a reference carrying hs38d1 decoys and masked GRC exclusion contigs. The submission format requires `chr`-prefixed UCSC ids. Records were restricted to the primary assembly, contigs renamed, multiallelics split and everything left-aligned against `GCA_000001405.15_GRCh38_no_alt_analysis_set`. FILTER-failing records were deliberately retained: a hard-filter tag is not evidence of non-causality, and dropping them here would be unrecoverable.

Result: **4,962,060 normalised records** — 3,981,890 SNVs, 980,170 indels, Ti/Tv 1.96. Normal for 44× WGS.

Getting this stage right is worth as much as the biology: Track 1 scores on an exact `(chrom, pos, ref, alt)` match, so a correct indel in an equivalent-but-different representation scores zero.

**S2 · ClinVar cross-reference** (`02_clinvar_scan.sh`). The answer key is a *clinically confirmed* pair, so there was a good chance at least one allele was already a ClinVar record. Genome-wide annotation against ClinVar GRCh38 yielded **7** Pathogenic/Likely_pathogenic non-reference calls, non-conflicting. One of them was allele A, annotated verbatim to "Mosaic variegated aneuploidy syndrome 1".

**S3 · Exhaustive locus analysis** (`03_gene_deepdive.py`). ClinVar alone finds one allele and stops — allele B is in no clinical database. Rather than filter by predicted consequence, every called variant across the BUB1B locus ±50 kb was classified against the canonical transcript's exon structure: **175 non-reference calls**, of which 77 upstream, 84 downstream, 12 deep-intronic, and **exactly two exonic** — alleles A and B. **Not one variant falls within ±20 bp of any exon boundary**, which is what rules out a splice-disrupting second allele rather than merely making it unlikely. The 46 calls spanning the gene and its immediate flanks were then pushed through Ensembl VEP, and allele B is the only one that is essentially **private** — a single gnomAD exome allele, no rsID. Every other locus variant is common (AF 0.02–0.99).

This ordering matters. A conventional rare-variant filter chain applied genome-wide can lose allele B, because a lone missense in a gene that already has a ClinVar-pathogenic hit is only interesting once the recessive hypothesis is on the table. Working the locus exhaustively, after the gene is nominated, is what surfaces it.

**S4 · Structural alternatives excluded.** MVA1's second allele is frequently non-coding or a copy-number event, so those were checked before settling: depth holds at 26–48× across the whole gene with no drop, heterozygous calls are distributed throughout with no run of homozygosity, and no variant at all falls within ±20 bp of any exon boundary across the whole ±50 kb locus. There is no deletion in trans.

**S5 · Differential diagnoses.** The other MVA genes carry nothing: CEP57 has 4 called variants (none coding-damaging), TRIP13 has 3, CENPE has 123 of which the two missense score AlphaMissense 0.099 and 0.105 — benign range. No competing candidate approaches the BUB1B pair.

**S6 · Unbiased confirmation with Exomiser** (`mva/track1/exomiser/`). Everything above began from the MVA prior, which is exactly the kind of reasoning that finds what it went looking for. So the same VCF was put through Exomiser 15.1.0 with the 2512 hg38 build, given **only the eight HPO terms and the sex** — no gene panel, no interval, no mention of BUB1B or of MVA — with every inheritance mode enabled so a dominant or de novo answer could not be filtered away.

Of 363 genes and 588 filtered variants, it returned:

| Rank | Gene | MOI | Contributing variants |
|---|---|---|---|
| **1** | **BUB1B** | AD | `c.2210T>G p.Leu737*` |
| **2** | **BUB1B** | **AR** | **`c.2210T>G p.Leu737*` + `c.3006T>G p.Asn1002Lys`** |
| 3 | FANCD2 | AR | — |
| 4 | LZTR1 | AD | — |
| 5 | GNRHR | AD | — |

Rank 2 is the compound-heterozygous pair, both alleles flagged as contributing, matched to **ORPHA:1052 Mosaic variegated aneuploidy syndrome**. A method with no knowledge of the hypothesis reconstructs it exactly. FANCD2 at rank 3 is the sensible near-miss — the other chromosomal-instability syndrome in the differential — and LZTR1 at rank 4 is the same incidental finding submitted here as a secondary.

**On Exomiser's own ACMG call for allele B.** It classifies `p.Asn1002Lys` as VUS, applying **BP1** — "missense variant in a gene for which primarily truncating variants cause disease". For *BUB1B* and MVA1 that rule is misapplied, and the reason is mechanistic: biallelic truncating *BUB1B* is not viable, so surviving MVA1 patients essentially always carry a missense or otherwise hypomorphic allele in trans with a null. The genotype that BP1 treats as evidence against pathogenicity is the genotype the disease requires. Removing BP1 and the classification moves to Likely pathogenic on PM2_Supporting + PP4_Moderate + PP3 (AlphaMissense 0.923, MVP 0.852) with PM3 available once phase is established.

**S7 · Orthogonal validation from our own alignment.** Everything to this point rests on the VCF the organisers supplied — one aligner, one caller. The re-aligned BAM allows the call to be re-derived independently: bwa-mem2 instead of Sentieon's aligner, `bcftools mpileup`/`call` instead of Sentieon Haplotyper.

Calling the BUB1B gene body from scratch returns five variants, and both alleles are among them at the same allele balance:

| | Sentieon (supplied VCF) | bcftools on our bwa-mem2 BAM |
|---|---|---|
| `chr15:40209701 T>G` | 0/1, AD 21,25, DP 46 | 0/1, AD 21,26, DP 47 |
| `chr15:40220612 T>G` | 0/1, AD 15,13, DP 28 | 0/1, AD 15,12, DP 27 |

Read-level evidence at both sites is as clean as it gets:

| | reads | fwd / rev | MAPQ 60 | min MAPQ | alt strand balance | VAF |
|---|---|---|---|---|---|---|
| `chr15:40209701` | 52 | 29 / 23 | **100%** | 60 | 14 fwd, 12 rev | 0.55 |
| `chr15:40220612` | 32 | 11 / 21 | **100%** | 60 | 4 fwd, 8 rev | 0.44 |

Every read at both positions carries the maximum mapping quality of 60, so neither call sits in a region where paralogy or mismapping could manufacture a heterozygote. Alternate alleles appear on both strands, and the variant allele fractions of 0.55 and 0.44 are what a true germline heterozygote looks like. Duplicates were marked and are few (4 and 3 respectively).

Two aligners, two callers, one answer.

## 4. Mosaic aneuploidy tested directly from the reads

MVA is defined cytogenetically. That makes a prediction the sequencing data can be asked about without any karyotype, and without realignment (`04_mosaic_aneuploidy.py`).

If a fraction *f* of cells carries three copies of a chromosome, heterozygous B-allele frequencies on it split into bands at 0.5 ± *f*/4. Binomial noise at 44× hides this in any single SNP, so the statistic is the per-chromosome variance of BAF **in excess of** what binomial sampling explains.

**The filters are the entire difference between a result and an artefact.** Run naively, the statistic reports a large apparent signal on chr17, chr19, chr20 and chr22 — implied mosaic fractions up to 0.37. Those are the GC-rich, segmental-duplication-rich chromosomes, and the "signal" is reference and mappability bias: mean BAF drops to 0.472 there, which is a bias signature, not a dosage signature. Requiring MQ ≥ 59, dbSNP membership and a narrow depth band (38–50×) removes it completely.

| | naive | filtered |
|---|---|---|
| chr20 excess variance | +0.0061 above median | −0.000038 |
| chr22 | +0.0051 | +0.000016 |
| chr17 | +0.0025 | +0.000097 |
| mean BAF range | 0.357–0.497 | 0.4989–0.5000 |

Filtered, **every autosome sits at 0.00071 ± 0.00006**, no chromosome deviates by more than 2.6 σ, and mean BAF is 0.4995 or better everywhere. Sex is male (chrX 4,562 heterozygous calls, chrY present at 0.77× autosomal depth).

**Result: no per-chromosome mosaic aneuploidy above f ≈ 0.054 (3 σ) in this blood sample.**

This is consistent with the diagnosis rather than against it, for two reasons that are worth being explicit about. First, MVA mosaicism is conventionally scored on *cultured* lymphocytes or fibroblasts; aneuploid cells are counter-selected in circulating blood, and bulk uncultured DNA understates it. Second and more fundamentally — the aneuploidy in MVA is *variegated*. A different random chromosome is affected in each cell, so a 30% aneuploid cell population spread across 22 autosomes leaves each individual chromosome at ~1–2%, far below any per-chromosome test.

That predicts a uniform floor with no outlier, which is exactly what is observed. The measured floor of 0.00071 is shared by every chromosome and corresponds to *f* ≈ 0.11 if read as dosage; it is equally consistent with ordinary technical overdispersion, and **a single sample with no matched control cannot separate the two.** Stated as a bound rather than a finding: this analysis excludes a dominant single-chromosome mosaicism and is silent on uniform low-level variegation.

### 4.1 The same question from read depth

The B-allele analysis above uses the VCF. Re-aligning the FASTQs makes a second, independent modality available — read depth — and `08_coverage_aneuploidy.py` asks the same question of it.

**The naive version is wrong, and it is worth showing why.** mosdepth's per-chromosome mean reports chr22 at 36.5×, chr15 at 38.8×, chr14 at 39.0× and chr13 at 40.8× against a genome mean near 46×. Read as dosage that is a ~20% deficit on five chromosomes — a spectacular finding, and an artefact. Those are the acrocentrics, whose satellite and rDNA arrays are unmappable: only **69.6%** of chr22's 10 kb windows carry plausible depth, 76.8% of chr21's, 80.2% of chr15's. A whole-length mean averages in the zero blocks.

Taking instead the **median depth over mappable windows** — those within 0.5–1.75× the genome median, which is insensitive both to the zero blocks and to segmental-duplication pileups:

| | naive mean | robust median | ratio | mappable |
|---|---|---|---|---|
| chr22 | 36.45× | **48.17×** | 1.031 | 69.6% |
| chr15 | 38.80× | **47.02×** | 1.006 | 80.2% |
| chr13 | 40.81× | **46.27×** | 0.990 | 84.3% |
| chr9 | 41.61× | **46.75×** | 1.000 | 86.5% |

Every autosome then falls between 0.984 and 1.046 of the autosomal median of 46.74×, the largest deviation is **2.9 σ**, and no chromosome is an outlier. The 3 σ detection limit is a mosaic fraction of **f ≈ 0.097** — less sensitive than the B-allele test, as expected, since depth carries no allelic information.

`chrX` at 0.522 and `chrY` at 0.537 of autosomal depth confirm a male karyotype from a third direction, independent of both the VCF's heterozygosity and its chrY calls.

**The residual is GC bias, and the two methods together prove it.** The chromosomes still sitting slightly high — chr19 at 1.046, chr17 and chr22 at 1.031, chr16 at 1.027 — are exactly the GC-rich ones, the same set that dominated the *unfiltered* B-allele statistic. If chr19 were genuinely gained at f ≈ 0.09, the B-allele frequencies on it would have to show a matching excess variance. They do not: chr19's filtered excess sits +0.000158 from the autosomal median, well inside noise. A real dosage change moves both statistics; a GC artefact moves only the depth one. It moves only the depth one.

**Joint conclusion.** Two independent modalities, agreeing: no whole-chromosome mosaic aneuploidy is detectable in this blood sample, bounded at **f < 0.054** by allele balance and **f < 0.097** by depth. As set out above, that is what *variegated* aneuploidy is expected to look like in bulk uncultured blood, and it is a bound rather than a refutation.

## 5. Limitations, stated plainly

- **Phase is not determined, and this is now measured rather than assumed.** The FASTQs were re-aligned to GRCh38 (`05_align.sh`: 1,076,740,679 reads, 99.57% mapped, 98.09% properly paired, 12.9% duplicates) and `07_phase_attempt.py` made the attempt.

  Over the BUB1B locus the library's insert size runs to a median of 443 bp, a 99.9th percentile of 1,221 bp and a **largest observed template of 1,272 bp**. The two alleles are 10,911 bp apart — **nine times** the longest fragment in the data. Read-backed phasing would have to chain through intervening heterozygous sites instead, and there is exactly **one** between them, at `chr15:40216470`, splitting the distance into steps of 6,769 bp and 4,142 bp. Both are more than three times the longest template. Checking directly: **0 of 2 consecutive steps are bridged by even one shared template.** `PGT`/`PID` are absent from both calls for the same reason.

  So phase is not recoverable from this library, by a factor of roughly nine — not marginally missed. *Trans* is inferred from the clinical diagnosis, the autosomal-recessive mechanism of MVA1, and the parental history of recurrent pregnancy loss. It would be settled by trio sequencing or by any long-read platform, where a single 15 kb read spans the pair comfortably.
- The mosaic-aneuploidy analysis bounds rather than confirms, as set out above.
- `p.Asn1002Lys` has no functional assay behind it. AlphaMissense 0.923 and kinase-domain position are strong circumstantial support; the ClinVar VUS at the same residue shows the field has not yet closed the question either.
- The Exomiser run is coding-focused. A genome-wide non-coding pass (REMM, full SpliceAI tabix) and a SHEPHERD knowledge-graph ranking are still to come; neither is expected to change the call, but both would strengthen the claim that nothing else was missed.
- Predictor disagreement on allele B is real: AlphaMissense 0.923 and MVP 0.852 against REVEL 0.472. The case rests on the genotype and phenotype, not on any single score.

## 6. Submission

`mva/results/texdata_bub1b-compound-het.csv`, validated by parsing it with the organisers' own `evaluation.py`.

| Rank | EPCR | Type | Call |
|---|---|---|---|
| 1 | 0.95 | primary | `chr15:40209701 T>G` **+** `chr15:40220612 T>G` — the compound-heterozygous pair |
| 2 | 0.80 | primary | `chr15:40209701 T>G` alone |
| 3 | 0.75 | primary | `chr15:40220612 T>G` alone |
| 4 | 0.25 | secondary | `chr22:20996720 C>G` — *LZTR1* `p.Tyr748Ter`, ClinVar P/LP, SpliceAI 0.92. Heterozygous LZTR1 loss of function predisposes to schwannomatosis: actionable, and unrelated to the primary phenotype |
| 5 | 0.10 | primary | `chr3:10046723 AG>A` **+** `chr3:10046725 TAAG>T` — *FANCD2*, the chromosomal-instability differential and Exomiser's rank-3 gene |
| 6 | 0.08 | secondary | `chr1:145927447 C>T` — *RBM8A* 5′UTR, ClinVar P/LP low-penetrance. TAR syndrome carrier |
| 7 | 0.06 | secondary | `chr4:67753920 C>T` — *GNRHR* `p.Arg139His`, ClinVar Pathogenic. Recessive carrier state, no second allele found |

Row 5 is submitted as a considered alternative rather than a belief, and the reason it is *not* believed is worth recording: **ClinVar classifies both FANCD2 alleles Benign, while Exomiser's own ACMG engine applies PVS1 — "null variant in a gene where loss of function is a known mechanism" — to a variant ClinVar has already called benign.** Automated ACMG classification is a useful prior and not a verdict, in both directions; §5 makes the same point about BP1 in the other direction on the real answer.

### Why rows 2 and 3 are there

They look like hedging, so they were tested rather than assumed. Scoring the 7-row submission against five possible answer keys, and against the same submission with rows 2 and 3 removed:

| If the answer key is … | 7 rows | without rows 2–3 |
|---|---|---|
| our pair | **100.0** / F-max 1.000 | 100.0 / 1.000 |
| allele A + a variant we did not call | 50.0 / 0.500 | 50.0 / 0.500 |
| allele B + a variant we did not call | 50.0 / 0.500 | 50.0 / 0.500 |
| **a single variant, allele A** | **50.0** / 0.667 | **0.0** / 0.667 |
| neither allele | 0.0 / 0.000 | 0.0 / 0.000 |

They earn in exactly one scenario — a **single-variant** key — and cost nothing in every other, because F-max is attained at the rank-1 threshold. That scenario is not hypothetical: `evaluation.py`'s docstring describes a compound-heterozygous key, but `score_proband` handles a one-element key and `groundtruth.py` places no constraint on its size. Partial credit for the pair is already secured by row 1, which contains one true variant either way; rows 2 and 3 exist solely to cover the single-variant case.

Also detected and deliberately **not** submitted: *FLG* `p.Arg501Ter` (common, semi-dominant ichthyosis vulgaris), *HK1* recessive carrier state, and a *PRSS1* call at VAF 0.15 in the PRSS1/TRB paralogous region that is more likely a mapping artefact than a real heterozygote.

## 7. Reproducibility and compliance

Pipeline `mva/track1/00`–`04`, panels and Ensembl helpers in `mva/src/mva/`. Environment: bcftools 1.24 / htslib 1.23.1, Python 3.11, Ensembl VEP 116 (REST for locus work, offline cache for the genome-wide pass), ClinVar GRCh38 (August 2026), AlphaMissense hg38, Exomiser 15.1.0 + 2512 data.

Patient data is confined to `/mnt/data/mva-hackathon-2026/`, excluded by `.gitignore`, and will be deleted at the close of the hackathon with notification to `MVAHackathon2026@synapse.org` as the data-use terms require. No attempt was made to re-identify or contact the family.

AlphaMissense is CC BY-NC-SA 4.0 and is used here under its non-commercial terms. ClinVar, gnomAD, Ensembl and UniProt are used under their respective open licences. This report and the accompanying code are released CC BY 4.0.
