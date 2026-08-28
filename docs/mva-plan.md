# MVA Hackathon 2026 — build plan

**Deadline** 24 Oct 2026 23:59 UTC. Judging to 24 Nov. Winners 25 Nov.
Prizes $50k ($25k cash AWS + $25k Claude credits).

## 0. What the organisers actually score (read from the Space source, not the marketing page)

Source of truth: `SageBio/rare-disease-real-kid-mva-hackathon-2026` → `evaluation.py`, `tabs/submit_track1.py`, `tabs/submit_track2.py`.

### Track 1
- CSV, **max 10 rows**, one row = one candidate (single variant *or* compound-het pair).
- Columns: `proband_id,chrom_1,pos_1,ref_1,alt_1,chrom_2,pos_2,ref_2,alt_2,epcr,finding_type,notes`
- `proband_id` must be `PROBAND01`. Coordinates **GRCh38, `chr`-prefixed**.
- `epcr` ∈ (0,1]. Scorer re-sorts by epcr desc.
- **Rank points**: rank 1 → 100, ≤3 → 50, ≤5 → 25, ≤10 → 10, else 0.
- **Ground truth is a compound-het pair** (`frozenset` of 2 variants). Exact `(chrom,pos,ref,alt)` match.
  One of two correct → **half** the rank points. Both in one row → full.
- **F-max** computed per individual variant across epcr thresholds. `finding_type=secondary` does not hurt.
- **6 submissions**, best one counts. Report (PDF/MD) + public GitHub required.

### Track 2
- **1 submission**. Report + GitHub + 3-min video. Human panel.
- Weights: Scientific Rigor 35 / Potential Impact 25 / Innovation 25 / Scalability 15.
- Must characterise variant mechanism (LoF vs GoF, pathway, downstream consequence) as the basis for repurposing.

### Consequences for design
1. Exact-match scoring means **normalisation is worth as much as biology**. A right indel in the wrong
   representation scores 0. Left-align + split multiallelics against the exact reference, and hedge
   ambiguous indel representations across spare rows.
2. Contig rename required: VCF is `1`, submission wants `chr1`.
3. 10 rows and half-credit rules → put the best pair in row 1, then singletons of each allele,
   then differentials. Never waste rows 1-3.
4. 6 submissions are 6 measurements. Ration them; keep ≥2 in reserve for after the FASTQ re-analysis.

## 1. Data on disk

`/mnt/data/mva-hackathon-2026/data` (symlinked as `./data`). 85 GB. **Must be deleted after the hackathon
and `MVAHackathon2026@synapse.org` notified.** Never commit any of it.

| File | Note |
|---|---|
| `WGS_EX2312012_HGWCNDSX7.vcf.gz` (315 MB) + `.tbi` | Sentieon Haplotyper → GVCFtyper, then GATK `VariantFiltration`. **GRCh38 no-alt, no `chr` prefix.** Single sample `WGS_EX2312012`. SNV+indel only — **no SV, no CNV, no annotation.** |
| 8 × `*_S16_L00{1..4}_R{1,2}_001.fastq.gz` (~84 GB) | 4 lanes paired-end. The only route to SV / CNV / mosaic aneuploidy. |
| `Challenge_Clinical_Phenotype_1.docx` | 8 HPO terms |

### Phenotype
`HP:0002859` rhabdomyosarcoma · `HP:0000121` nephrocalcinosis (since birth) · `HP:0004322` short stature ·
`HP:0001508` failure to thrive · `HP:0003202` skeletal muscle atrophy · `HP:0001622` premature birth (32 wk) ·
`HP:0001518` small for gestational age (~1 kg) · `HP:0200067` parental recurrent spontaneous abortion.

### Prior, stated before looking at the data
Mosaic variegated aneuploidy. Biallelic **BUB1B** (15q15.1, MVA1) is the textbook fit — rhabdomyosarcoma
and Wilms are the MVA1-specific cancers, and MVA1 is characteristically **compound heterozygous**
(one truncating allele + one hypomorphic/expression-reducing allele), which matches the answer key shape.
Differentials that must still be run genome-wide and unbiased: **CEP57** (MVA2), **TRIP13** (MVA3),
**CENPE**, and non-MVA rhabdomyosarcoma predisposition — **TP53**, **DICER1**, **HRAS** (Costello),
**PTPN11**/RASopathies, **FBXW7**.
Nephrocalcinosis is *not* classic MVA; at 32 weeks / 1 kg it is most likely prematurity-related
(loop diuretics, TPN). That reasoning goes in the report rather than driving the gene search.
Parental recurrent miscarriage *is* on-mechanism for a recessive aneuploidy syndrome and supports AR.

## 2. Repos and tools pulled into this project

`external/` — `TxGNN`, `SHEPHERD`, `PrimeKG`, `OptimusKG`, `TDC`, `Exomiser`.
`/mnt/data/mva-hackathon-2026/mamba/envs/mva` — bcftools 1.24, samtools, htslib, bedtools, OpenJDK 21,
python 3.11, pysam, cyvcf2, pandas.

**OptimusKG vs PrimeKG.** OptimusKG (Zitnik lab, Apr 2026) is the newer graph: 190,939 nodes / 21.8 M edges /
145 property keys over 65 sources, vs PrimeKG's 129 k / 4.05 M. But **pretrained TxGNN is trained on PrimeKG**
and TxGNN Explain resolves PrimeKG node IDs. So: PrimeKG carries the pretrained TxGNN + Explain path;
OptimusKG is the richer evidence and graph-RAG layer, with retraining TxGNN on OptimusKG as the
innovation stretch goal (and a real Scalability argument for Track 2).

## 3. Track 1 pipeline

```
FASTQ ──┐
        ├─► [S5] bwa-mem2 → BAM → Manta/DELLY (SV) · mosdepth (CNV) · BAF (mosaic aneuploidy)
VCF ────┴─► [S1] normalise ──► [S2] annotate ──► [S3] rank ×4 ──► [S4] second-allele hunt ──► CSV
```

**S1 — normalise.** `bcftools annotate --rename-chrs` → `chr*`; `bcftools norm -f GRCh38.fa -m -any --check-ref w`;
left-align; drop `*`. QC: ti/tv, het/hom, callable fraction, sex check, relatedness sanity.
Keep an unfiltered copy — `VariantFiltration` FILTER tags must not silently remove a causal allele.

**S2 — annotate.** VEP 113 offline GRCh38 cache + ClinVar VCF (highest yield: a clinically confirmed
answer is very likely already a ClinVar record) + gnomAD v4 AF + **AlphaMissense** (hg38, CC BY-NC-SA —
cite it) + **SpliceAI** + CADD + dbNSFP.

**S3 — four independent rankers, then ensemble.**
1. **Exomiser 14.x** (hg38 + phenotype data), HPO list above, `AUTOSOMAL_RECESSIVE` first then AD / de novo / XR.
   This is the CAGI-validated method the organisers' scorer is adapted from — it is the baseline to beat and
   the baseline to trust.
2. **Rules panel** — MVA genes ∪ GO:0007094 mitotic spindle assembly checkpoint ∪ chromosomal-instability
   ∪ cancer-predisposition ∪ HPO-A gene sets for the 8 terms. Fully interpretable; this is what the report explains.
3. **SHEPHERD** — KG-based causal-gene ranking from HPO + candidate list. Designed for exactly this
   "atypical / novel rare disease" setting.
4. **OptimusKG graph-RAG** — phenotype → gene retrieval over the 21.8 M-edge graph, LLM adjudication,
   every claim carried by a named edge.
Ensemble = rank fusion, disagreements adjudicated by hand and written up.

**S4 — second-allele hunt.** MVA1's second allele is frequently *not* a coding SNV: deep-intronic splice,
5'UTR/promoter expression-reducing, or an exon-level deletion. So for the top gene(s): pull **every**
variant ±50 kb regardless of FILTER or consequence, run SpliceAI over all of them, and look for
loss-of-heterozygosity / depth drop signalling a deletion in trans.

**S5 — FASTQ re-analysis.** This is the differentiator and the reason 85 GB of FASTQ was shipped.
bwa-mem2 (48 threads, ~6 h) → sorted BAM → Manta + DELLY (SV), mosdepth (CNV), B-allele frequency.
Also the direct shot at **demonstrating mosaic aneuploidy from the data itself** — which would confirm the
diagnosis independently of any variant call, and is a strong Innovation card.

**S6 — assemble.** Row 1 = best pair. Rows 2-3 = each allele alone (half-credit insurance).
Rows 4-7 = differentials. Rows 8-10 = indel-representation hedges and secondary findings
(`finding_type=secondary`, which cannot hurt the score).

## 4. Track 2 pipeline

1. **Mechanism.** From the Track 1 call: LoF vs hypomorph, allele-specific effect, SAC failure →
   chromosome missegregation → constitutional mosaic aneuploidy → CIN → rhabdomyosarcoma.
2. **Proxy phenotype.** MVA is thinly represented in any KG. Map to MONDO MVA1 plus proxy nodes
   (CIN cancers, cohesinopathies, other aneuploidy syndromes) in PrimeKG/OptimusKG — the explicit
   proxy-disease step the user asked for, and the mechanism TxGNN was built to exploit.
3. **TxGNN zero-shot** indication *and* contraindication prediction on the disease node(s).
   Zero-shot on a treatment-less orphan disease is TxGNN's designed use case.
4. **TxGNN Explain** → multi-hop subgraph per candidate → graph-backed rationale in the dossier.
   Every recommendation ships with its supporting edges.
5. **Corroborate** — ChEMBL / DrugBank / Open Targets; DepMap for aneuploidy-selective dependencies;
   optional LINCS/CMap signature reversal.
6. **Rank** by Repurposing Feasibility = mechanistic support × evidence strength × paediatric safety ×
   availability. Table + dossier + 3-min video.

Mechanistic guardrail to state explicitly: agents that further weaken the spindle assembly checkpoint
(MPS1/TTK, KIF11, AURKB inhibitors) are *contraindicated* here, not candidates — a hypomorphic SAC is
already the lesion. The productive directions are selective killing of aneuploid cells via their
proteotoxic/metabolic stress, and CIN reduction. Submissions are hypotheses for follow-up, and the
report will say so in those words.

## 5. Compute and storage budget

| Item | Size |
|---|---|
| Challenge data | 85 GB (delete after) |
| VEP GRCh38 cache | ~25 GB |
| Exomiser hg38 + phenotype | ~40 GB |
| SpliceAI precomputed (optional) | ~30 GB |
| GRCh38 + bwa-mem2 index | ~30 GB |
| BAM | ~100 GB |
| PrimeKG + OptimusKG + TxGNN weights | ~10 GB |
| **Total** | **< 350 GB** of 6.1 TB free on `/mnt/data` |

Wall clock: annotation refs a few hours; Exomiser minutes; realignment ~6 h on 48 threads.
2 × RTX PRO 6000 are free for SpliceAI on-the-fly and any TxGNN retraining.

## 6. Milestones

| By | |
|---|---|
| Aug 29 | Env, references, normalised + annotated VCF, first ranked candidate list |
| Aug 31 | Exomiser + panel + SHEPHERD ensemble → **submission 1 of 6** |
| Sep 5 | FASTQ realigned; SV / CNV / mosaic aneuploidy results |
| Sep 12 | TxGNN + OptimusKG Track 2 draft dossier |
| Oct 10 | Final Track 1 submission, Track 2 report + video |
| Oct 24 | Close |
| after | **Delete all data, email MVAHackathon2026@synapse.org** |

## 7. Rules compliance

- Patient data never enters git. `data/` symlink and `/mnt/data` stay out of the repo; `.gitignore` enforces it.
- Public GitHub repo carries code and methods only.
- No attempt to re-identify or contact the family.
- Outputs are CC BY 4.0; AlphaMissense is CC BY-NC-SA and must be cited as such.
