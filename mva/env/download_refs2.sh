#!/usr/bin/env bash
# Large references: Exomiser distribution + data bundles, VEP cache.
set -uo pipefail
REFS=${REFS:-/mnt/data/mva-hackathon-2026/refs}
mkdir -p "$REFS"; cd "$REFS"

get () {
  local url=$1 out=${2:-$(basename "$1")}
  if [[ -s $out ]]; then echo "have    $out"; return; fi
  echo "fetch   $out"
  curl -fsSL --retry 5 --retry-delay 5 -C - -o "$out.part" "$url" && mv "$out.part" "$out" \
    && echo "done    $out" || echo "FAILED  $out  <- $url"
}

# Exomiser 15.1.0 CLI + the 2512 data release (newest published on Monarch).
get https://github.com/exomiser/Exomiser/releases/download/15.1.0/exomiser-cli-15.1.0-distribution.zip
get https://data.monarchinitiative.org/exomiser/data/2512_hg38.zip
get https://data.monarchinitiative.org/exomiser/data/2512_phenotype.zip
get https://data.monarchinitiative.org/exomiser/data/2512_hg38.sha256
get https://data.monarchinitiative.org/exomiser/data/2512_phenotype.sha256

# Ensembl VEP 116 indexed offline cache, GRCh38.
get https://ftp.ensembl.org/pub/release-116/variation/indexed_vep_cache/homo_sapiens_vep_116_GRCh38.tar.gz
