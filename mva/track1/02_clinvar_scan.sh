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

# --- A Pathogenic/Likely_pathogenic filter silently discards two whole classes,
#     and on this genome it discarded 137 calls. ClinVar files Factor V Leiden as
#     CLNSIG=drug_response, reviewed by expert panel, with "Thrombophilia due to
#     activated protein C resistance" and "Pregnancy loss, recurrent" among its
#     disease terms - and it does not match the filter above. So does every
#     pharmacogenomic variant, including a DPYD allele in this sample.
#     Pulled out explicitly rather than hidden inside a wider regex nobody reads.
echo
echo "=== drug_response / risk_factor / protective, non-reference genotype ==="
awk -F'\t' '$7 != "0/0" && $7 != "./." && $11 ~ /drug_response|risk_factor|protective|Affects/' \
    "$WORK/clinvar_hits.tsv" | tee "$WORK/clinvar_pgx_risk.tsv" | wc -l
echo "--- of those, reviewed by expert panel or practice guideline:"
awk -F'\t' '$12 ~ /expert_panel|practice_guideline/ {split($13,g,":"); printf "  %s:%s %s>%s GT=%s %s [%s]\n", $1,$2,$3,$4,$7,g[1],$11}' \
    "$WORK/clinvar_pgx_risk.tsv"
