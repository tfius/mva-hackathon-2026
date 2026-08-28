#!/usr/bin/env bash
# Unbiased Exomiser run. See sample.yml for why it carries no MVA prior.
#
# Exomiser 15 splits the old single job file into sample / analysis / output,
# and reads its data paths from the distribution's application.properties, which
# 00_configure.sh points at the 2512 hg38 bundle.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
EXO=${EXO:-/mnt/data/mva-hackathon-2026/exomiser/exomiser-cli-15.1.0}
JAVA=${JAVA:-/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/java}
mkdir -p /mnt/data/mva-hackathon-2026/work/exomiser
cd "$EXO"
exec "$JAVA" -Xmx32g -jar exomiser-cli-15.1.0.jar analyse \
  --sample   "$HERE/sample.yml" \
  --analysis "$HERE/analysis.yml" \
  --output   "$HERE/output.yml"
