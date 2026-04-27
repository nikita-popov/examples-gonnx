#!/usr/bin/env python3
"""Save kokoro-tts response to a WAV file.

Usage:
    gonnxctl run kokoro-tts -f request.json | python3 save_wav.py [output.wav]
    python3 save_wav.py [output.wav] < response.json

Default output filename: output.wav
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
    sr = response.get("sample_rate", 24000)
    duration = len(data) / (sr * 2)  # 16-bit = 2 bytes per sample
    print(f"saved {out}  ({duration:.1f}s, {sr} Hz, {len(data)} bytes)")

if __name__ == "__main__":
    main()
