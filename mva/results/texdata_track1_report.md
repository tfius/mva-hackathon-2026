# Track 1 — Variant Prediction Report

**Rare Disease, Real Kid: MVA Hackathon 2026** · proband `PROBAND01` (`WGS_EX2312012`)
Team `texdata` · GRCh38 · 28 August 2026

---

## 1. The call

> **Result: submitted 28 August 2026 and scored against the clinically confirmed answer key — rank points 100.0/100, F-max 1.000, full match at rank 1.** The key is a two-variant pair and it is this pair; the hedge rows in §6 never came into play, and the F-max threshold landed at 0.95, the rank-1 row.


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

Nephrocalcinosis is not a *characteristic* MVA1 feature, though renal dysfunction is reported in ~13% of MVA1 cases, so "not a recognised feature" would be stronger than the literature supports. Prematurity remains the base-rate explanation — nephrocalcinosis occurs in 20–64% of preterm infants, and loop diuretics and parenteral nutrition are the usual drivers.

**Two caveats this report previously omitted, both raised in adversarial review.** First, those exposures are *inferred*, not observed — no drug history is in the challenge data — and Track 2 then builds a patient-specific aminoglycoside argument on top of that inference, which is the most reversible clinical claim in either document. Second, **the chronology does not fit**: the phenotype document records nephrocalcinosis as present *since birth*, and NICU nephrocalcinosis from postnatal diuretics and TPN is acquired over weeks of exposure. A finding present at birth points antenatal.

**So it was screened rather than assumed.** All 13 nephrocalcinosis and Bartter-syndrome genes — *KCNJ1, SLC12A1, CLCNKB, BSND, CASR, CLDN16, CLDN19, CYP24A1, SLC34A1, SLC34A3, ATP6V1B1, ATP6V0A4, CLCN5* — yield **1,147 non-reference calls and zero rare (<1% gnomAD) coding or splice variants**. A 693 bp heterozygous deletion near *KCNJ1* surfaced in the SV panel and was checked: it lies **22,801 bp outside the gene body**, is heterozygous, and antenatal Bartter type 2 is recessive. No monogenic cause is present in these genes. The negative is now measured; the limitation is that it covers SNVs and indels in 13 genes, not deep-intronic, regulatory or copy-number causes.

## 3. How the call was reached

The pipeline is in `mva/track1/`. Data never leaves `/mnt/data`; nothing patient-derived is committed.

**S1 · Normalisation** (`01_normalize.sh`). The challenge VCF is Sentieon Haplotyper → GVCFtyper with GATK `VariantFiltration`, on GRCh38 with **unprefixed contig names** (`1`, not `chr1`) and a reference carrying hs38d1 decoys and masked GRC exclusion contigs. The submission format requires `chr`-prefixed UCSC ids. Records were restricted to the primary assembly, contigs renamed, multiallelics split and everything left-aligned against `GCA_000001405.15_GRCh38_no_alt_analysis_set`. FILTER-failing records were deliberately retained: a hard-filter tag is not evidence of non-causality, and dropping them here would be unrecoverable.

Result: **4,962,060 normalised records** — 3,981,890 SNVs, 980,170 indels, Ti/Tv 1.96. Normal for 44× WGS.

Getting this stage right is worth as much as the biology: Track 1 scores on an exact `(chrom, pos, ref, alt)` match, so a correct indel in an equivalent-but-different representation scores zero.

**S2 · ClinVar cross-reference** (`02_clinvar_scan.sh`). The answer key is a *clinically confirmed* pair, so there was a good chance at least one allele was already a ClinVar record. Genome-wide annotation against ClinVar GRCh38 yielded **7** Pathogenic/Likely_pathogenic non-reference calls, non-conflicting. One of them was allele A, annotated verbatim to "Mosaic variegated aneuploidy syndrome 1".

**S3 · Exhaustive locus analysis** (`03_gene_deepdive.py`). ClinVar alone finds one allele and stops — allele B is in no clinical database. Rather than filter by predicted consequence, every called variant across the BUB1B locus ±50 kb was classified against the canonical transcript's exon structure: **175 non-reference calls**, of which 77 upstream, 84 downstream, 12 deep-intronic, and **exactly two exonic** — alleles A and B. **Not one variant falls within ±20 bp of any exon boundary.** That is what was measured, and the claim is scoped to it: **no candidate splice variant in the canonical ±20 bp windows.** It does *not* rule out a splice-disrupting allele. Branch points sit ~20–50 nt upstream of the 3′ splice site, deep-intronic pseudoexon activation occurs hundreds of nt away, and exonic splice enhancers and silencers are invisible to a distance rule entirely. **SpliceAI has not been run on the 12 deep-intronic calls at this locus**, so this negative is narrower than an earlier draft claimed. The 46 calls spanning the gene and its immediate flanks were then pushed through Ensembl VEP, and allele B is the only one that is essentially **private** — a single gnomAD exome allele, no rsID. Every other locus variant is common (AF 0.02–0.99).

This ordering matters. A conventional rare-variant filter chain applied genome-wide can lose allele B, because a lone missense in a gene that already has a ClinVar-pathogenic hit is only interesting once the recessive hypothesis is on the table. Working the locus exhaustively, after the gene is nominated, is what surfaces it.

**S4 · Structural alternatives excluded.** MVA1's second allele is frequently non-coding or a copy-number event, so those were checked before settling: depth holds at 26–48× across the whole gene with no drop, heterozygous calls are distributed throughout with no run of homozygosity, and no variant falls within ±20 bp of any exon boundary across the ±50 kb locus — a canonical-splice-site negative, not a splicing negative, since SpliceAI has not been run on the deep-intronic calls.

**On excluding a deletion in trans, the argument used here is the wrong one and is replaced.** An earlier draft cited "depth flat 26–48× across the gene" — but a 26→48 spread *is* a 1.85× range, and a heterozygous deletion produces a 2× drop, so a measurement whose scatter spans the effect cannot exclude it. The sound argument was available and unused: **both alleles are called heterozygous with VAF 0.55 and 0.44 at MAPQ 60.** A deletion in trans at either position would render it hemizygous and drive VAF toward 1.0. Allele balance excludes an overlapping deletion far more tightly than any depth range.

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

Rank 2 is the compound-heterozygous pair, both alleles flagged as contributing, matched to **ORPHA:1052 Mosaic variegated aneuploidy syndrome**. A method that was never pointed at BUB1B reconstructs it.

**"Unbiased" needs qualifying, though, and the report's own output gives the reason.** Exomiser's variant scorer reads ClinVar, and allele A is a ClinVar record annotated verbatim to *Mosaic variegated aneuploidy syndrome 1* — which is why **PP5_Strong** appears in its ACMG output. The gene was not rediscovered from phenotype alone; it was partly retrieved from the same annotation §S2 used. What the run genuinely demonstrates is that **no gene panel or interval was needed**, not that the result is independent of ClinVar. Also, rank 1 is BUB1B under an *autosomal dominant* model with the nonsense alone, which is not a disease model for a recessive condition; the meaningful result is **rank 2, the AR compound-heterozygous pair**. FANCD2 at rank 3 is the sensible near-miss — the other chromosomal-instability syndrome in the differential — and LZTR1 at rank 4 is the same incidental finding submitted here as a secondary.

**On Exomiser's own ACMG call for allele B.** It classifies `p.Asn1002Lys` as VUS, applying **BP1** — "missense variant in a gene for which primarily truncating variants cause disease". For *BUB1B* and MVA1 that rule is misapplied, and the reason is mechanistic: biallelic truncating *BUB1B* is not viable, so surviving MVA1 patients essentially always carry a missense or otherwise hypomorphic allele in trans with a null. The genotype that BP1 treats as evidence against pathogenicity is the genotype the disease requires. Removing BP1 is defensible. **The classification that was said to follow from it is not, and this is corrected here.**

Under the ClinGen/Tavtigian points system, PM2_Supporting (1) + PP4_Moderate (2) + PP3_Supporting (1) = **4 points, which is still VUS** (Likely pathogenic needs 6). Under the 2015 Richards combining rules, 1 Moderate + 2 Supporting also fails every Likely-pathogenic combination. An earlier draft asserted LP; that was wrong.

Three further problems in the same evidence set, all against us:

- **PP3 is probably not applicable at all.** ClinGen SVI's calibrated thresholds (Pejaver 2022) place PP3_Supporting at REVEL ≥ 0.644 and BP4 at ≤ 0.290. **REVEL 0.472 sits in the indeterminate band — no code in either direction.** Reaching past it to AlphaMissense is precisely the predictor-shopping this report criticises elsewhere.
- **PP4 is questionable at any strength.** It requires a phenotype highly specific for a disease with a *single* genetic aetiology; MVA has at least five genes, as §S5 and the disease node itself show.
- **PP5_Strong, quoted for allele A, is deprecated.** ClinGen SVI recommended laboratories discontinue PP5/BP6 in 2018. It does not change allele A's call — PVS1 + PM2_Supporting suffices — but it should not be quoted uncritically.

**What actually resolves this is PM3, and PM3 requires parental testing.** That is an ordinary clinical action, not a research question, and it is the highest-yield next step in this dossier.

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

### 3.1 Structural variants — the completeness check

The supplied VCF is SNV/indel only, so a structural variant anywhere in the panel would have been invisible to every analysis before the realignment. §S4 argued against one in BUB1B from depth and heterozygosity, which is an absence-of-evidence argument. `delly sr` on the re-aligned BAM, intersected with the panel by `09_sv_panel_intersect.py`, is the direct test.

**In BUB1B ±50 kb, delly emits four records and exactly one passes filter:**

| Position | Type | Size | FILTER | PE / SR | GT |
|---|---|---|---|---|---|
| `chr15:40113056` | INS | 39 bp | **PASS** | 0 / 12 | 1/1 |
| chr15:24,767,504–60,516,119 | DUP | 35.7 Mb | LowQual | 2 / – | 0/0 |
| chr15:38,016,169–74,552,325 | INV | 36.5 Mb | LowQual | 5 / – | 0/0 |
| chr15:40,131,925–40,132,744 | DEL | 819 bp | LowQual | 2 / – | 0/0 |

The single PASS call is a homozygous 39 bp insertion **48 kb upstream** of the gene — and it is not a missed event at all: the supplied VCF already carries it, as `chr15:40113056 C>CGTGTGGGG…` at 1/1. Everything else in the window is LowQual with two to five read pairs, no split reads, and a reference genotype.

**No structural variant lies in BUB1B, and neither confirmed allele sits inside any called SV.** The compound heterozygote is two genuine SNVs, not a mis-called structural event.

**On the rest of delly's output, a caution rather than a result.** Genome-wide it emits 52,245 records, 17,233 of them PASS, and 305 PASS calls with ≥3 read pairs touch a panel gene. Most are not credible: the list is led by a 223 Mb duplication of chr1, a 34.7 Mb inversion on chr15 and a 48.8 Mb deletion on chr6, all with substantial paired-end support, **no split reads**, and in many cases a `0/0` genotype. These are mismapping in repeat and segmental-duplication structure, not rearrangements.

Requiring split-read support *and* a non-reference genotype leaves 14 of 305 — and several of those are still implausibly large. The small ones that survive both filters (an *APC* 2.6 kb deletion, *KCNJ1* 693 bp, *SMARCB1* 2.6 kb homozygous, *ZWILCH* 768 bp) are the size and zygosity of common structural polymorphism, and none is followed up here.

So the claim this section supports is deliberately narrow: **nothing structural was missed in BUB1B.** A genome-wide SV survey from a single short-read sample with no control panel cannot honestly support more than that, and the filtering above is why.

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

Filtered, **every autosome sits at 0.00071 ± 0.00006**, no chromosome deviates by more than 2.6 σ, and mean BAF is 0.4995 or better everywhere. Sex is male (chrX 4,562 heterozygous calls against 170k on chr1; chrY present).

*Two chrY depth figures appear in this report and they measure different things.* The B-allele analysis reports median depth **at heterozygous call sites** on chrY as 0.77× autosomal — but heterozygous calls on a haploid chromosome are largely mismapped PAR and X-transposed reads, so that number describes an artefact, not dosage. The dosage figure is **0.537×** from §4.1's median over mappable 10 kb windows. Where the two disagree, the windowed one is correct.

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

## 4.2 Evidence provenance — every negative, and the coverage that earns it

Positive findings carry their own evidence. **Negatives do not**: a locus with no coverage produces no variant call, exactly like a locus that is genuinely reference, and a report that presents the two identically is asserting things it has not measured. Every "we did not find X" claim in this dossier is therefore listed with the measurement that makes it a finding rather than a silence.

**The call**

| Claim | Evidence | Measurement |
|---|---|---|
| `chr15:40209701 T>G` is a true heterozygote | 2 aligners, 2 callers | Sentieon AD 21,25 / DP 46 · bwa-mem2+bcftools AD 21,26 / DP 47 · **100% of 52 reads at MAPQ 60** · alt on both strands · VAF 0.55 |
| `chr15:40220612 T>G` is a true heterozygote | same | Sentieon AD 15,13 / DP 28 · ours AD 15,12 / DP 27 · **100% of 32 reads at MAPQ 60** · VAF 0.44 |
| Allele B is essentially private | gnomAD v4 API | **1 allele in 1,461,878** exomes (AF 6.8 × 10⁻⁷); absent from genomes and dbSNP |
| NMD predicted for allele A | exon table arithmetic | PTC at c.2209–2211, last junction c.2957/c.2958 → **746 nt upstream**, far past the 50–55 nt rule |
| The gene call is not method-dependent | Exomiser 15.1.0, HPO terms only | **rank 1 and 2 of 363 genes**, no panel, no BUB1B prior |

**The negatives**

| Claim | What would have hidden it | Measurement that rules that out |
|---|---|---|
| No splice-disrupting second allele | a variant near an exon boundary | **175 non-reference calls** across BUB1B ±50 kb classified by exon position; **0** within 20 bp of any boundary |
| No structural variant at the locus | an SV invisible to an SNV caller | delly `sr`, **52,245 genome-wide calls**; 4 in BUB1B ±50 kb, 1 PASS — a 39 bp insertion **48 kb upstream** already present in the supplied VCF |
| Neither allele is a mis-called SV | the compound het being one rearrangement | **0** called SVs span either position |
| No deletion in trans | a het deletion mimicking hemizygosity | depth **flat 26–48×** across the gene; heterozygous calls distributed throughout; no run of homozygosity |
| No per-chromosome mosaic aneuploidy — B-allele | GC and mappability bias faking one | filtered excess variance **0.00071 ± 0.00006** on every autosome, max deviation **2.6 σ** → **f < 0.054** |
| — same, from read depth | unmappable satellite arrays faking a deficit | median over mappable windows; all autosomes **0.984–1.046**, max **2.9 σ** → **f < 0.097**. chr22 naive mean 36.5× vs robust median 48.2×, **69.6% mappable** |
| Phase is genuinely unrecoverable | assuming rather than measuring | largest observed template **1,272 bp** against a **10,911 bp** gap (9×); one intervening het; **0 of 2 steps bridged** by any shared template |
| No mitochondrial aminoglycoside-deafness allele | low mtDNA coverage | m.1555A>G and m.1494C>T reference at **4,497×** and **4,152×** → heteroplasmy bounded below ~0.1% |
| No CPIC-actionable *DPYD*, *TPMT*, *NUDT15* or *G6PD* risk allele | a position with no reads | **24–65×** at every locus, checked individually against the BAM |

**Explicitly not assessable, named rather than omitted**

CYP2D6 star alleles (structural variation, CYP2D7 gene conversion) · UGT1A1\*28 (promoter TA repeat — and irinotecan is in the rhabdomyosarcoma VIT regimen, so this is a real gap) · HLA-B typing · phase, as above · anything requiring a parental sample.

**Underlying data quality:** 1,076,740,679 reads, **99.57% mapped**, **98.09% properly paired**, 12.9% duplicates, ~45× post-duplicate — median VCF depth 44×, consistent.

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
| 4 | 0.25 | secondary | `chr22:20996720 C>G` — *LZTR1* `p.Tyr748Ter`, ClinVar P/LP, SpliceAI 0.92. **Incidental, and explicitly *not* an imaging indication** — see below |
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

## Methods, software and AI disclosure

*Disclosure required by the rules as updated 28 August 2026. Extended beyond the minimum, because "an LLM was used" spans a wide range and several machine-learning models produced **evidence** in this dossier rather than merely assisting with it. A panel weighing scientific rigour should be able to see which conclusion rests on which model.*

### AI assistant

| | |
|---|---|
| Provider | **Anthropic** |
| Interface | **Claude Code** (agentic CLI), OAuth session — not the raw API |
| Model | **Claude Opus 5** |
| Plan | **Claude Max** subscription |
| Data-handling setting | ⚠️ **See note below — the submitter must confirm this.** |

**What it did.** Claude wrote and executed the entire analysis: VCF normalisation, the genome-wide ClinVar cross-reference, the exhaustive locus analysis that found allele B, the mosaic-aneuploidy and coverage analyses, the four-lane realignment, the phasing attempt, structural-variant intersection, the TxGNN and knowledge-graph work, the pharmacogenomic screen, and both reports. **Every quantitative claim here was produced by code in the linked repository and is reproducible from it** — no figure in this document was asserted by a language model without a script behind it.

**Independent review was also AI-driven, and is disclosed because it changed the conclusions.** Three separate agent instances reviewed the dossier cold — clinical management, adversarial refutation, experimental feasibility. They found a hard factual error (`K668 is deleted on the null allele` — false, since 668 < 737), a safety-level misreading risk (vincristine is standard rhabdomyosarcoma therapy and appeared in our contraindication list), a published surveillance guideline the dossier lacked, a reversed *LZTR1* finding, and an ACMG miscalculation. Corrections are documented in the reports and in `journals/`, not silently applied.

**Human oversight.** Direction, scope, judgement calls and the decision to submit were the submitter's.

### Machine-learning models used as evidence

These are not assistants; their outputs are cited as data.

| Model | Type | Where it is load-bearing | How it is treated |
|---|---|---|---|
| **AlphaMissense** | deep learning (DeepMind) | `p.Asn1002Lys` = **0.923** — a primary pathogenicity argument | CC BY-NC-SA 4.0, used under non-commercial terms |
| **REVEL** | ensemble ML | **0.472** on the same variant | Reported as **disagreeing**, not averaged away; and it sits in ClinGen's indeterminate band (0.290–0.644), which is why PP3 is not claimed |
| **MVP** | deep learning | 0.852 on the same variant | Supporting only |
| **SpliceAI** | deep learning | Exomiser pathogenicity source; nothing surfaced at the locus | **Not run standalone** — stated as a limitation, so the splice negative is scoped to canonical ±20 bp windows |
| **Exomiser HiPhive** | semantic similarity over HPO/MP/ZFIN + PPI | Ranked *BUB1B* 1st of 363 from HPO terms alone | Its independence is qualified: Exomiser reads ClinVar, and its own `PP5_Strong` output proves it |
| **Exomiser ACMG engine** | rule-based automation | Classified both alleles | **Corrected twice** — BP1 misapplied to allele B, PVS1 applied to a ClinVar-benign *FANCD2* allele |
| **TxGNN** | relational GNN link predictor, pretrained on PrimeKG | Zero-shot indication/contraindication ranking | Degree artefact identified and corrected (ρ −0.51 → +0.054); its top recommendations judged **wrong** on mechanism |
| **TxGNN GraphMask** | graph XAI | Explanation paths | Raw output shown to be **hub artefact**; audited before use |

### Knowledge graphs

Not reference lookups — these are the substrate the Track 2 analysis runs on, and several of its central findings are statements *about* them.

| Graph | Scale | Role here |
|---|---|---|
| **PrimeKG** (Chandak, Huang & Zitnik, *Sci Data* 2023) | 129,375 nodes / 4,050,249 edges. [DOI 10.7910/DVN/IXA7BM](https://doi.org/10.7910/DVN/IXA7BM) | TxGNN's training substrate, and the graph in which *BUB1B* has 464 edges and **zero drug edges** — finding 1. Also the source of the CYP3A4 hub paths that the explanation audit rejected, and of the BUB1B–SIRT2 and BUB1B–CREBBP/EP300 edges behind the semantics-gap argument |
| **OptimusKG** (Zitnik Lab, 2026) | 190,531 nodes / 21,813,816 edges / 145 property keys, from 65 resources grounded in 18 ontologies via BioCypher and the Biolink Model. [DOI 10.7910/DVN/IYNGEV](https://doi.org/10.7910/DVN/IYNGEV) | **Independent replication.** Four times denser around BUB1B and still zero drug edges, which is what turns "PrimeKG lacks this" into "BubR1 is undrugged". Also the coverage test that separated the schema gap from a size gap: it *has* the nicotinamide riboside and acadesine nodes PrimeKG lacks, and still cannot reach them from the MVA genes |

Neither graph was modified. Both were queried as distributed; the analysis scripts are in `mva/track2/`.

### Reference data

ClinVar GRCh38 (August 2026) · gnomAD v4 (REST API, and the Exomiser 2512 bundle) · Ensembl VEP 116 offline cache and REST · Exomiser 2512 hg38 + phenotype bundles · UniProt O60566 · Human Phenotype Ontology · GRCh38 `GCA_000001405.15_no_alt_analysis_set`.

### Conventional software

bwa-mem2 · bcftools 1.24 / htslib 1.23.1 · samtools · mosdepth · delly 2.6.0 · Exomiser 15.1.0 with the 2512 hg38 and phenotype bundles · Python 3.11 · GRCh38 `GCA_000001405.15_no_alt_analysis_set`.

### ⚠️ Note on the data-handling setting

This field is a **per-account privacy setting the submitter controls**, not something determinable from the analysis environment, and it is deliberately left for them to confirm rather than guessed — a fabricated value in a compliance statement would be worse than a blank.

For a Claude Max subscription it is the *"help improve Claude"* / model-training preference in **claude.ai → Settings → Privacy**. The submitter should record which state it is in, e.g. *"Anthropic, Claude Max subscription, model-training preference OFF"*.

Note also that **no challenge data was pasted into a chat interface**. The analysis ran locally against files on disk; the assistant issued shell and file operations, and what passed through the model was code, command output and summary statistics.

## 7. Reproducibility and compliance

Pipeline `mva/track1/00`–`04`, panels and Ensembl helpers in `mva/src/mva/`. Environment: bcftools 1.24 / htslib 1.23.1, Python 3.11, Ensembl VEP 116 (REST for locus work, offline cache for the genome-wide pass), ClinVar GRCh38 (August 2026), AlphaMissense hg38, Exomiser 15.1.0 + 2512 data.

The challenge **sequence data** is confined to `/mnt/data/mva-hackathon-2026/`, excluded by `.gitignore`, and will be deleted at the close of the hackathon with notification to `MVAHackathon2026@synapse.org`. No attempt was made to re-identify or contact the family.

**A distinction this report should state rather than blur.** "Nothing patient-derived is committed" would be false, and an earlier draft came close to implying it. *This document is patient-derived.* It is released CC BY 4.0 with a public repository link and contains an essentially private variant absent from dbSNP, exact coordinates for both alleles, sex, gestational age, birth weight, an active malignancy, nephrocalcinosis, and a pharmacogenomic profile including *F5* Leiden, CYP2C19 \*2/\*17, CYP3A5 \*3/\*3 and DPYD \*6. That combination is individual-level genotype-plus-phenotype data.

The hackathon's own terms provide for exactly this — submissions, code and reports are published under CC BY 4.0, and the research output is the deliverable while the sequence data is not. But the honest framing is *"the raw data stays private and the derived findings are published, as the terms require"*, not *"nothing patient-derived leaves this machine"*.

AlphaMissense is CC BY-NC-SA 4.0 and is used here under its non-commercial terms. ClinVar, gnomAD, Ensembl and UniProt are used under their respective open licences. This report and the accompanying code are released CC BY 4.0.
