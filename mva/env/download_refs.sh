#!/usr/bin/env bash
# Reference data for the MVA hackathon Track 1 pipeline.
# Everything lands in $REFS (outside the git repo).
set -uo pipefail
REFS=${REFS:-/mnt/data/mva-hackathon-2026/refs}
mkdir -p "$REFS"
cd "$REFS"

get () {  # get <url> [outname]
  local url=$1 out=${2:-$(basename "$1")}
  if [[ -s $out ]]; then echo "have    $out"; return; fi
  echo "fetch   $out"
  curl -fsSL --retry 5 --retry-delay 5 -C - -o "$out.part" "$url" && mv "$out.part" "$out" \
    && echo "done    $out" || echo "FAILED  $out  <- $url"
}

# --- GRCh38 no-alt analysis set, UCSC contig ids (chr1..chrY). Matches what the
#     submission format wants and is sequence-identical to the caller's reference
#     for all non-masked primary contigs.
get https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz GRCh38_no_alt.fna.gz

# --- ClinVar (GRCh38). Highest-yield single annotation: a clinically confirmed
#     answer key is very likely already a ClinVar record.
get https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
get https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi

# --- AlphaMissense (hg38). CC BY-NC-SA 4.0 -- cite accordingly.
get https://storage.googleapis.com/dm_alphamissense/AlphaMissense_hg38.tsv.gz
