#!/usr/bin/env bash
# Genome-wide ClinVar cross-reference.
#
# The Track 1 answer key is a *clinically confirmed* pair, so there is a good
# chance both alleles are already ClinVar records. This is the cheapest shot at
# the answer and it runs before any of the heavy annotation is in place.
#
# Runs against the raw VCF because ClinVar and the challenge VCF share the same
# unprefixed GRCh38 contig naming. Renaming happens later, in 01_normalize.sh.
set -euo pipefail
ENV=${ENV:-/mnt/data/mva-hackathon-2026/mamba/envs/mva}
REFS=${REFS:-/mnt/data/mva-hackathon-2026/refs}
DATA=${DATA:-/mnt/data/mva-hackathon-2026/data}
WORK=${WORK:-/mnt/data/mva-hackathon-2026/work}
export PATH="$ENV/bin:$PATH"

IN="$DATA/WGS_EX2312012_HGWCNDSX7.vcf.gz"
mkdir -p "$WORK"

if [[ ! -s "$WORK/clinvar_hits.tsv" ]]; then
  bcftools annotate -a "$REFS/clinvar.vcf.gz" \
      -c INFO/CLNSIG,INFO/CLNDN,INFO/CLNREVSTAT,INFO/GENEINFO,INFO/CLNVC,INFO/MC,INFO/ALLELEID \
      --threads 8 -Ou "$IN" \
    | bcftools view -i 'INFO/CLNSIG!="."' -Ou \
    | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL\t%FILTER\t[%GT\t%AD\t%DP\t%GQ]\t%CLNSIG\t%CLNREVSTAT\t%GENEINFO\t%MC\t%CLNDN\n' \
    > "$WORK/clinvar_hits.tsv"
fi

echo "ClinVar-annotated genotyped sites: $(wc -l < "$WORK/clinvar_hits.tsv")"
echo
echo "=== Pathogenic / Likely_pathogenic, non-reference genotype ==="
awk -F'\t' '$7 != "0/0" && $7 != "./." && $11 ~ /Pathogenic|Likely_pathogenic/ && $11 !~ /Conflicting/' \
    "$WORK/clinvar_hits.tsv" \
  | tee "$WORK/clinvar_pathogenic.tsv" | wc -l
