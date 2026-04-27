#!/usr/bin/env bash
# Save piper-ru response to a WAV file.
#
# Usage:
#   ./save_wav.sh [request.json] [output.wav]

set -euo pipefail

REQ=${1:-request.json}
OUT=${2:-output.wav}

gonnxctl run piper-ru -f "$REQ" \
  | jq -r '.audio_b64' \
  | base64 -d > "$OUT"

echo "saved $OUT"
