#!/usr/bin/env python3
"""Save silero-ru response to a WAV file.

Usage:
    gonnxctl run silero-ru -f request.json | python3 save_wav.py [output.wav]
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
    duration = len(data) / (sr * 2)
    speaker = response.get("speaker", "?")
    print(f"saved {out}  ({duration:.1f}s, {sr} Hz, speaker={speaker})")


if __name__ == "__main__":
    main()
