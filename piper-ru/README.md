# piper-ru

Russian text-to-speech using [Piper](https://github.com/rhasspy/piper) ONNX
(`ru_RU-irina-medium`, 22050 Hz). Based on the Piper engine from
[nikita-popov/tts-api](https://github.com/nikita-popov/tts-api).

## Assets

Both files are downloaded at `pull` time — not committed to Git.

| Asset ID | File | Size | Source |
|----------|------|------|--------|
| `model` | `model.onnx` | ~63 MB | [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices) |
| `config` | `model.onnx.json` | ~150 KB | same repo |

```sh
gonnxctl pull piper-ru
```

## Install and run

```sh
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir piper-ru
gonnxctl pull piper-ru
gonnxctl load piper-ru
gonnxctl run piper-ru -f examples/request.json
```

## Request format

```json
{
  "text": "Привет, мир!"
}
```

All parameters are optional:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `text` | string | — | Russian text (**required**) |
| `speaker_id` | integer | `0` | Speaker index (multi-speaker models) |
| `length_scale` | number | `1.0` | Speed: `>1` slower, `<1` faster |
| `noise_scale` | number | `0.667` | Pitch/energy variation |
| `noise_w` | number | `0.8` | Phoneme duration variation |

## Response format

```json
{
  "audio_b64": "<base64 WAV>",
  "sample_rate": 22050
}
```

WAV is 22050 Hz, mono, 16-bit PCM.

## Saving audio

**Shell (requires `jq` and `base64`):**

```sh
./examples/save_wav.sh examples/request.json output.wav
```

**Python (no extra deps):**

```sh
gonnxctl run piper-ru -f examples/request.json \
  | python3 examples/save_wav.py output.wav
```

**One-liner:**

```sh
gonnxctl run piper-ru -f examples/request.json \
  | jq -r '.audio_b64' | base64 -d > output.wav
```

**Playback:**

```sh
aplay output.wav           # ALSA (Linux)
ffplay -nodisp output.wav  # ffmpeg
```

## Other voices

Any Piper voice from [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices)
can be used. Update the `assets` URLs in `manifest.yaml` to point to the
corresponding `.onnx` and `.onnx.json` files.

## Notes

- Requires `espeak-ng` installed on the host (`apt install espeak-ng`).
- `network: disabled` — no egress after `pull`.
- `maxConcurrency: 4` — Piper ONNX is CPU-only and thread-safe.
