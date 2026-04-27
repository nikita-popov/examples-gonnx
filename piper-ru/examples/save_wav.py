#!/usr/bin/env python3
"""Save piper-ru response to a WAV file.

Usage:
    gonnxctl run piper-ru -f request.json | python3 save_wav.py [output.wav]
"""
import base64
import json
import sys

def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "output.wav"
    response = json.load(sys.stdin)
    data = base64.b64decode(response["audio_b64"])
    with open(out, "wb") as f:
        f.write(data)
    sr = response.get("sample_rate", 22050)
    duration = len(data) / (sr * 2)
    print(f"saved {out}  ({duration:.1f}s, {sr} Hz, {len(data)} bytes)")

if __name__ == "__main__":
    main()
