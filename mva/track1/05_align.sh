#!/usr/bin/env bash
# Re-align the challenge FASTQs to GRCh38.
#
# The organisers shipped 85 GB of FASTQ alongside the VCF, and the VCF is
# SNV/indel only - no structural variants, no copy number, and no read-level
# evidence. This produces the BAM those analyses need:
#
#   * read-level validation of both BUB1B alleles
#   * a documented attempt at read-backed phasing (expected to fail - the two
#     alleles are 10,911 bp apart and the library is 150 bp paired-end - but a
#     measured insert-size distribution is worth more than an assertion)
#   * SV and CNV calling, to close out "was anything missed structurally"
#   * a tighter mosaic-aneuploidy bound than the VCF alone supports
#
# Four lanes, paired-end, aligned separately so the read groups stay honest,
# then merged and duplicate-marked.
set -euo pipefail
ENV=${ENV:-/mnt/data/mva-hackathon-2026/mamba/envs/mva}
REFS=${REFS:-/mnt/data/mva-hackathon-2026/refs}
DATA=${DATA:-/mnt/data/mva-hackathon-2026/data}
WORK=${WORK:-/mnt/data/mva-hackathon-2026/work/align}
THREADS=${THREADS:-44}
SORT_THREADS=${SORT_THREADS:-8}
SORT_MEM=${SORT_MEM:-3G}
export PATH="$ENV/bin:$PATH"

REF="$REFS/GRCh38_no_alt.fa.gz"
SAMPLE=WGS_EX2312012
FLOWCELL=HGWCNDSX7
mkdir -p "$WORK"
cd "$WORK"   # so any tool that ignores -T still writes here, not into the repo

# --- bwa-mem2 index. Peak RSS during construction is roughly 80 GB for GRCh38,
#     so this deliberately runs on its own rather than alongside anything else.
if [[ ! -s "$REF.bwt.2bit.64" ]]; then
  echo "[$(date +%T)] building bwa-mem2 index (this is the memory-hungry step)"
  bwa-mem2 index "$REF"
fi

for LANE in L001 L002 L003 L004; do
  OUT="$WORK/$SAMPLE.$LANE.bam"
  [[ -s "$OUT" ]] && { echo "[$(date +%T)] have $OUT"; continue; }
  R1="$DATA/${SAMPLE}_${FLOWCELL}_S16_${LANE}_R1_001.fastq.gz"
  R2="$DATA/${SAMPLE}_${FLOWCELL}_S16_${LANE}_R2_001.fastq.gz"
  RG="@RG\tID:${FLOWCELL}.${LANE}\tSM:${SAMPLE}\tLB:${SAMPLE}\tPL:ILLUMINA\tPU:${FLOWCELL}.${LANE}"
  echo "[$(date +%T)] aligning $LANE"
  bwa-mem2 mem -t "$THREADS" -R "$RG" "$REF" "$R1" "$R2" \
    | samtools sort -@ "$SORT_THREADS" -m "$SORT_MEM" -o "$OUT.tmp" -
  mv "$OUT.tmp" "$OUT"
done

MERGED="$WORK/$SAMPLE.markdup.bam"
if [[ ! -s "$MERGED" ]]; then
  echo "[$(date +%T)] merging, fixmate and marking duplicates"
  # Every stage gets an explicit temp prefix under $WORK. Without -T, samtools
  # sort spills tens of gigabytes into the current working directory, which for
  # a backgrounded run is wherever it happened to be launched from - in this
  # case the git repository.
  samtools merge -@ "$THREADS" -o - "$WORK/$SAMPLE".L00[1-4].bam \
    | samtools collate -@ "$SORT_THREADS" -O - "$WORK/collate.tmp" \
    | samtools fixmate -@ "$SORT_THREADS" -m - - \
    | samtools sort -@ "$SORT_THREADS" -m "$SORT_MEM" -T "$WORK/sort.tmp" - \
    | samtools markdup -@ "$SORT_THREADS" -T "$WORK/markdup.tmp" - "$MERGED.tmp"
  mv "$MERGED.tmp" "$MERGED"
  samtools index -@ "$THREADS" "$MERGED"
fi

echo "[$(date +%T)] done"
samtools flagstat -@ "$THREADS" "$MERGED" | tee "$WORK/flagstat.txt"
