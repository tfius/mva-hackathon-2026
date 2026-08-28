#!/usr/bin/env bash
# Point the Exomiser distribution at the 2512 hg38 data bundle.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
EXO=${EXO:-/mnt/data/mva-hackathon-2026/exomiser/exomiser-cli-15.1.0}
cp "$HERE/application.properties" "$EXO/application.properties"
echo "configured $EXO/application.properties:"
cat "$EXO/application.properties"
