#!/usr/bin/env bash
# Recompress the GRCh38 no-alt analysis set with bgzip and index it.
# NCBI ships plain gzip, which samtools faidx cannot random-access.
set -euo pipefail
ENV=${ENV:-/mnt/data/mva-hackathon-2026/mamba/envs/mva}
REFS=${REFS:-/mnt/data/mva-hackathon-2026/refs}
export PATH="$ENV/bin:$PATH"

cd "$REFS"
if [[ ! -s GRCh38_no_alt.fa.gz.fai ]]; then
  echo "bgzip: GRCh38_no_alt.fna.gz -> GRCh38_no_alt.fa.gz"
  zcat GRCh38_no_alt.fna.gz | bgzip -@ 12 -c > GRCh38_no_alt.fa.gz
  samtools faidx GRCh38_no_alt.fa.gz
fi
echo "reference ready:"
head -3 GRCh38_no_alt.fa.gz.fai
