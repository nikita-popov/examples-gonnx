#!/usr/bin/env bash
# Save kokoro-tts response to a WAV file.
#
# Usage:
#   ./save_wav.sh [request.json] [output.wav]
#
# Defaults: request.json -> request.json, output -> output.wav
#
# Requires: jq, base64 (coreutils)

set -euo pipefail

REQ=${1:-request.json}
OUT=${2:-output.wav}

gonnxctl run kokoro-tts -f "$REQ" \
  | jq -r '.audio_b64' \
  | base64 -d > "$OUT"

echo "saved $OUT"
