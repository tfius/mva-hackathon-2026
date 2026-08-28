#!/usr/bin/env bash
# Copy number, structural variants, and read-level evidence from the BAM.
set -euo pipefail
ENV=${ENV:-/mnt/data/mva-hackathon-2026/mamba/envs/mva}
REFS=${REFS:-/mnt/data/mva-hackathon-2026/refs}
WORK=${WORK:-/mnt/data/mva-hackathon-2026/work/align}
THREADS=${THREADS:-24}
export PATH="$ENV/bin:$PATH"

BAM="$WORK/WGS_EX2312012.markdup.bam"
REF="$REFS/GRCh38_no_alt.fa.gz"

# --- Windowed depth. 10 kb windows give a whole-chromosome dosage read-out that
#     is independent of, and more sensitive than, the VCF B-allele frequency
#     statistic in 04_mosaic_aneuploidy.py.
mosdepth -t "$THREADS" -n --fast-mode --by 10000 "$WORK/mosdepth.10kb" "$BAM"

# --- Structural variants. The challenge VCF has none, so this is the only pass
#     that can say whether a structural event was missed anywhere in the genome.
#     delly needs a real uncompressed FASTA with an index, not a process
#     substitution, so decompress once and keep it.
PLAINREF="$REFS/GRCh38_no_alt.fa"
if [[ ! -s "$PLAINREF.fai" ]]; then
  echo "decompressing reference for delly"
  bgzip -cd -@ 8 "$REF" > "$PLAINREF"
  samtools faidx "$PLAINREF"
fi
delly call -g "$PLAINREF" -o "$WORK/delly.bcf" "$BAM"
bcftools view "$WORK/delly.bcf" | grep -vc '^#' | xargs echo "delly SV records:"

# --- Insert-size distribution, which is what decides whether read-backed
#     phasing of the two BUB1B alleles is even arguable.
samtools stats -@ "$THREADS" "$BAM" | grep -E '^SN|^IS' > "$WORK/samtools_stats.txt"
grep -E '^SN\s+insert size' "$WORK/samtools_stats.txt" || true

# --- The locus itself, for read-level inspection and a phasing attempt.
samtools view -b "$BAM" chr15:40200000-40230000 > "$WORK/BUB1B.locus.bam"
samtools index "$WORK/BUB1B.locus.bam"
echo "wrote $WORK/BUB1B.locus.bam"
