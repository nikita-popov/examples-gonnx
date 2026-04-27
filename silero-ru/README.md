# silero-ru

Russian TTS using [Silero v4](https://github.com/snakers4/silero-models) — 5 speakers,
three sample rates (8 / 24 / 48 kHz).

> **Note:** This bundle uses `engine: torch` and loads the model with
> `torch.jit.load()`. onnxruntime is not involved — Silero TTS does not
> publish an ONNX export. This demonstrates that gonnx handlers are not
> limited to ONNX backends.

## Quick start

```sh
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir silero-ru
gonnxctl pull silero-ru       # downloads model.pt (38 MB)
gonnxctl load silero-ru
gonnxctl run silero-ru -f silero-ru/examples/request.json \
  | python3 silero-ru/examples/save_wav.py output.wav
```

## Speakers

| ID | Description |
|----|-------------|
| `aidar` | Male |
| `baya` | Female |
| `kseniya` | Female |
| `xenia` | Female (default) |
| `eugene` | Male |
| `random` | Random per call |

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `text` | string | required | Russian text (max 2048 chars) |
| `speaker` | string | `xenia` | Speaker ID (see table above) |
| `sample_rate` | integer | `24000` | Output Hz: `8000`, `24000`, `48000` |
| `put_accent` | boolean | `true` | Auto stress placement |
| `put_yo` | boolean | `true` | Auto `е` → `ё` substitution |

## Output

```json
{
  "audio_b64": "<base64 WAV>",
  "sample_rate": 24000,
  "speaker": "xenia"
}
```

## Requirements

- Python ≥ 3.9
- `torch >= 2.0.0`, `omegaconf`, `numpy` (installed automatically into the bundle venv)
- No system-level dependencies
