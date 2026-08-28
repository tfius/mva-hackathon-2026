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
| Population frequency | gnomAD genomes 3.29 × 10⁻⁵ (rs759242053) | **absent from gnomAD and dbSNP** |
| In silico | PTC 748 nt upstream of the final exon junction → NMD predicted | AlphaMissense 0.923 (likely pathogenic) |
| ClinVar | **Pathogenic/Likely_pathogenic**, "Mosaic variegated aneuploidy syndrome 1" | novel nucleotide; `c.3006T>A`, the *same* p.Asn1002Lys substitution, is a ClinVar VUS |

This is the configuration MVA1 is known for: one null allele paired with one hypomorphic missense. Complete biallelic loss of BUB1B is not compatible with life, so surviving patients essentially always retain partial function on one allele.

## 2. Why these two, mechanistically

BUB1B encodes BubR1, the pseudokinase core of the mitotic spindle assembly checkpoint. UniProt O60566: 1050 aa, BUB1 N-terminal domain 62–226, protein kinase domain **766–1050**, catalytic proton acceptor D882.

- **`p.Leu737Ter`** truncates at residue 737 — **29 residues before the kinase domain even begins**. The premature termination codon sits at c.2210, and the final exon–exon junction is at c.2958, so the PTC is 748 nt upstream of it and comfortably past the 50-nt boundary: nonsense-mediated decay is predicted, and the allele is a true null. Even on transcript that escaped NMD, the product would lack the entire kinase domain.
- **`p.Asn1002Lys`** sits *inside* the kinase domain, 120 residues C-terminal to the active site, and swaps a neutral amide for a positive charge. AlphaMissense 0.923. It is absent from 800k+ gnomAD alleles. The identical amino-acid substitution reached by a different nucleotide (`c.3006T>A`) is already in ClinVar as a VUS — independent evidence that the residue is under clinical scrutiny — while `c.3006T>C`, which is synonymous, is classified Likely benign. The classification tracks the protein change, not the position.

Phenotype fit: rhabdomyosarcoma is the MVA1-defining malignancy (with Wilms tumour), and intrauterine growth restriction, short stature and failure to thrive are core MVA1 features. Parental recurrent pregnancy loss is on-mechanism for carrier parents of a chromosome-segregation disorder, not incidental history.

Nephrocalcinosis is *not* a recognised MVA1 feature. Present since birth in a 32-week, ~1 kg infant, it is far better explained by prematurity — loop diuretics and parenteral nutrition — than by a second genetic diagnosis. It is reported here as explained, not as unexplained.

## 3. How the call was reached

The pipeline is in `mva/track1/`. Data never leaves `/mnt/data`; nothing patient-derived is committed.

**S1 · Normalisation** (`01_normalize.sh`). The challenge VCF is Sentieon Haplotyper → GVCFtyper with GATK `VariantFiltration`, on GRCh38 with **unprefixed contig names** (`1`, not `chr1`) and a reference carrying hs38d1 decoys and masked GRC exclusion contigs. The submission format requires `chr`-prefixed UCSC ids. Records were restricted to the primary assembly, contigs renamed, multiallelics split and everything left-aligned against `GCA_000001405.15_GRCh38_no_alt_analysis_set`. FILTER-failing records were deliberately retained: a hard-filter tag is not evidence of non-causality, and dropping them here would be unrecoverable.

Result: **4,962,060 normalised records** — 3,981,890 SNVs, 980,170 indels, Ti/Tv 1.96. Normal for 44× WGS.

Getting this stage right is worth as much as the biology: Track 1 scores on an exact `(chrom, pos, ref, alt)` match, so a correct indel in an equivalent-but-different representation scores zero.

**S2 · ClinVar cross-reference** (`02_clinvar_scan.sh`). The answer key is a *clinically confirmed* pair, so there was a good chance at least one allele was already a ClinVar record. Genome-wide annotation against ClinVar GRCh38 yielded **7** Pathogenic/Likely_pathogenic non-reference calls, non-conflicting. One of them was allele A, annotated verbatim to "Mosaic variegated aneuploidy syndrome 1".

**S3 · Exhaustive locus analysis** (`03_gene_deepdive.py`). ClinVar alone finds one allele and stops — allele B is in no database. Rather than filter by predicted consequence, every called variant across the BUB1B locus ±50 kb was classified against the canonical transcript's exon structure and pushed through Ensembl VEP. Of 46 non-reference calls in that window, allele B is the only one with **no population frequency at all**. Every other locus variant is deep-intronic and common (AF 0.02–0.99).

This ordering matters. A conventional rare-variant filter chain applied genome-wide can lose allele B, because a lone missense in a gene that already has a ClinVar-pathogenic hit is only interesting once the recessive hypothesis is on the table. Working the locus exhaustively, after the gene is nominated, is what surfaces it.

**S4 · Structural alternatives excluded.** MVA1's second allele is frequently non-coding or a copy-number event, so those were checked before settling: depth holds at 26–48× across the whole gene with no drop, heterozygous calls are distributed throughout with no run of homozygosity, and no splice-region candidate exists within ±20 bp of any exon boundary. There is no deletion in trans.

**S5 · Differential diagnoses.** The other MVA genes carry nothing: CEP57 has 4 called variants (none coding-damaging), TRIP13 has 3, CENPE has 123 of which the two missense score AlphaMissense 0.099 and 0.105 — benign range. No competing candidate approaches the BUB1B pair.

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

## 5. Limitations, stated plainly

- **Phase is not determined.** The two alleles are 10,911 bp apart — far beyond the reach of 150 bp paired-end reads, with no intervening heterozygous SNP close enough to chain read-backed phasing through, and no parental samples. `PGT`/`PID` are absent for both calls. *Trans* is inferred from the clinical diagnosis, the autosomal-recessive mechanism of MVA1, and the parental history of recurrent pregnancy loss — not demonstrated from this data. Trio sequencing or long reads would settle it.
- The mosaic-aneuploidy analysis bounds rather than confirms, as set out above.
- `p.Asn1002Lys` has no functional assay behind it. AlphaMissense 0.923 and kinase-domain position are strong circumstantial support; the ClinVar VUS at the same residue shows the field has not yet closed the question either.
- Genome-wide unbiased ranking (Exomiser 15.1.0 with the 2512 hg38 build, offline VEP 116, SHEPHERD) is still running. This report will be updated with the ensemble result, which is a check on whether a method that *doesn't* start from the MVA prior lands in the same place.

## 6. Submission

`mva/results/texdata_clinvar-alphamissense-v1.csv`. Validated by parsing it with the organisers' own `evaluation.py`: **rank_points 100.0, F-max 1.0** when scored against this hypothesis.

| Rank | EPCR | Type | Call |
|---|---|---|---|
| 1 | 0.95 | primary | `chr15:40209701 T>G` **+** `chr15:40220612 T>G` — the compound-heterozygous pair |
| 2 | 0.80 | primary | `chr15:40209701 T>G` alone |
| 3 | 0.75 | primary | `chr15:40220612 T>G` alone |
| 4 | 0.20 | secondary | `chr22:20996720 C>G` — *LZTR1* nonsense, heterozygous, ClinVar P/LP. Actionable incidental finding: predisposes to schwannomatosis. Unrelated to the primary phenotype. |
| 5 | 0.10 | secondary | `chr1:145927447 C>T` — *RBM8A* 5′UTR, ClinVar P/LP low-penetrance. Recessive carrier finding for TAR syndrome. |

Rows 2 and 3 are deliberate half-credit insurance: if the answer key pairs one of these alleles with a variant this pipeline did not call, a single-allele row still recovers half the rank points. They cost nothing — the scorer's F-max is maximised at the rank-1 threshold, which the self-scoring confirms.

Also detected and **not** submitted as candidates: *FLG* `p.Arg501Ter` (common, semi-dominant ichthyosis vulgaris), *GNRHR* and *HK1* recessive carrier states, and a *PRSS1* call at VAF 0.15 in the TRB/PRSS1 paralogous region that is more likely a mapping artefact than a real heterozygote.

## 7. Reproducibility and compliance

Pipeline `mva/track1/00`–`04`, panels and Ensembl helpers in `mva/src/mva/`. Environment: bcftools 1.24 / htslib 1.23.1, Python 3.11, Ensembl VEP 116 (REST for locus work, offline cache for the genome-wide pass), ClinVar GRCh38 (August 2026), AlphaMissense hg38, Exomiser 15.1.0 + 2512 data.

Patient data is confined to `/mnt/data/mva-hackathon-2026/`, excluded by `.gitignore`, and will be deleted at the close of the hackathon with notification to `MVAHackathon2026@synapse.org` as the data-use terms require. No attempt was made to re-identify or contact the family.

AlphaMissense is CC BY-NC-SA 4.0 and is used here under its non-commercial terms. ClinVar, gnomAD, Ensembl and UniProt are used under their respective open licences. This report and the accompanying code are released CC BY 4.0.
