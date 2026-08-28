#!/usr/bin/env bash
# Normalise the challenge VCF into the coordinate space the submission requires.
#
# Track 1 is scored on an exact (chrom, pos, ref, alt) match, so a correct indel
# in an equivalent-but-different representation scores zero. Rename contigs to
# the UCSC ids the submission template uses, split multiallelics, left-align.
#
# Restricted to the primary assembly: the caller's reference carried hs38d1
# decoys and masked GRC exclusion contigs that the analysis set does not, and
# nothing submittable lives on them.
set -euo pipefail
ENV=${ENV:-/mnt/data/mva-hackathon-2026/mamba/envs/mva}
REFS=${REFS:-/mnt/data/mva-hackathon-2026/refs}
DATA=${DATA:-/mnt/data/mva-hackathon-2026/data}
WORK=${WORK:-/mnt/data/mva-hackathon-2026/work}
export PATH="$ENV/bin:$PATH"

IN="$DATA/WGS_EX2312012_HGWCNDSX7.vcf.gz"
REF="$REFS/GRCh38_no_alt.fa.gz"
mkdir -p "$WORK"

MAP="$WORK/chr_map.txt"
REGIONS="$WORK/primary_contigs.txt"
if [[ ! -s $MAP ]]; then
  for c in $(seq 1 22) X Y; do echo -e "$c\tchr$c"; done  > "$MAP"
  echo -e "M\tchrM"  >> "$MAP"
  echo -e "MT\tchrM" >> "$MAP"
  cut -f1 "$MAP" > "$REGIONS"
fi

if [[ ! -s "$WORK/norm.vcf.gz.tbi" ]]; then
  bcftools view -r "$(paste -sd, "$REGIONS")" -Ou "$IN" \
    | bcftools annotate --rename-chrs "$MAP" -Ou \
    | bcftools norm -f "$REF" -m -any --check-ref w -Oz -o "$WORK/norm.vcf.gz" --threads 8
  bcftools index -t --threads 8 "$WORK/norm.vcf.gz"
fi

{
  echo "## input:  $IN"
  echo "## output: $WORK/norm.vcf.gz"
  echo
  printf "raw records        %s\n" "$(bcftools index -n "$IN")"
  printf "normalised records %s\n" "$(bcftools index -n "$WORK/norm.vcf.gz")"
  echo
  bcftools stats "$WORK/norm.vcf.gz" | grep -E '^SN|^TSTV' | cut -f2-
} > "$WORK/01_normalize.qc.txt"
cat "$WORK/01_normalize.qc.txt"
