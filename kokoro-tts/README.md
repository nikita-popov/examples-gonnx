# kokoro-tts

Text-to-speech in 9 languages using [Kokoro-82M](https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX) ONNX.

## Assets

This bundle uses two assets declared in `manifest.yaml`:

| Asset ID | File | Size | Source |
|----------|------|------|--------|
| `model` | `model.onnx` | ~330 MB | [onnx-community/Kokoro-82M-v1.0-ONNX](https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX) |
| `voices` | `voices.bin` | ~27 MB | same HF repo, `voices/voices-v1.0.bin` |

Neither file is committed to Git. Fetch both with:

```sh
gonnxctl pull kokoro-tts
```

`gonnxctl pull` verifies the sha256 of each file after download. If a file is
already present with the correct hash it is skipped.

## Install and run

```sh
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir kokoro-tts
gonnxctl pull kokoro-tts
gonnxctl load kokoro-tts
gonnxctl run kokoro-tts -f examples/request.json
```

## Request format

```json
{
  "text": "Hello, world!",
  "voice": "af_heart",
  "speed": 1.0
}
```

`lang` is optional — auto-detected from the voice prefix if omitted.

## Response format

```json
{
  "audio_b64": "<base64 WAV>",
  "sample_rate": 24000,
  "voice": "af_heart",
  "lang": "en-us"
}
```

The WAV is 24000 Hz, mono, 16-bit PCM.

## Saving audio

The response contains a base64-encoded WAV in `audio_b64`. Use one of the
helpers in `examples/` to save it to a file.

**Shell (requires `jq` and `base64`):**

```sh
# default output: output.wav
./examples/save_wav.sh examples/request.json

# custom output filename
./examples/save_wav.sh examples/request.json speech.wav
```

**Python (no extra deps):**

```sh
gonnxctl run kokoro-tts -f examples/request.json \
  | python3 examples/save_wav.py output.wav
```

**One-liner with `jq`:**

```sh
gonnxctl run kokoro-tts -f examples/request.json \
  | jq -r '.audio_b64' | base64 -d > output.wav
```

**Playback:**

```sh
aplay output.wav           # ALSA (Linux)
ffplay -nodisp output.wav  # ffmpeg
```

## Voices

| Prefix | Language | Gender |
|--------|----------|--------|
| `af_*` | English US | Female |
| `am_*` | English US | Male |
| `bf_*` | English GB | Female |
| `bm_*` | English GB | Male |
| `jf_*`, `jm_*` | Japanese | F / M |
| `zf_*`, `zm_*` | Chinese | F / M |
| `ef_*`, `em_*` | Spanish | F / M |
| `ff_*` | French | Female |
| `hf_*`, `hm_*` | Hindi | F / M |
| `if_*` | Italian | Female |
| `pf_*`, `pm_*` | Portuguese | F / M |

Default voice: `af_heart`.

## Notes

- `maxConcurrency: 1` — Kokoro is not thread-safe; requests are serialised.
- `network: disabled` — the worker has no egress; all data is local after `pull`.
- The handler produces 16-bit PCM WAV regardless of ONNX Runtime's internal
  float32 output, for maximum client compatibility.
