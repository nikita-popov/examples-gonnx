# kokoro-tts

Gonnx bundle for **Kokoro TTS v1.0** — a lightweight 82 M-parameter
text-to-speech model that runs fully on CPU via ONNX Runtime.

## Supported languages

| Voice prefix | Language | Voices |
|---|---|---|
| `af_*` / `am_*` | English US (female/male) | `af_heart`, `af_bella`, `am_adam`, … |
| `bf_*` / `bm_*` | English GB (female/male) | `bf_emma`, `bm_george`, … |
| `jf_*` / `jm_*` | Japanese | `jf_alpha`, `jm_omega`, … |
| `zf_*` / `zm_*` | Chinese | `zf_xiaobei`, … |
| `ef_*` / `em_*` | Spanish | — |
| `ff_*` | French | — |
| `hf_*` / `hm_*` | Hindi | — |
| `if_*` | Italian | — |
| `pf_*` / `pm_*` | Portuguese | — |

## Model files (not in repo — too large for Git)

Download from [onnx-community/Kokoro-82M-v1.0-ONNX](https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX)
and place next to `manifest.yaml`:

```
kokoro-tts/
├── model.onnx          # onnx/model.onnx  (~325 MB fp32)  or
│                       # onnx/model_quantized.onnx  (~82 MB int8)
└── voices.bin          # voices/voices-v1.0.bin
```

```bash
# Quick download with huggingface-cli
pip install huggingface_hub
huggingface-cli download onnx-community/Kokoro-82M-v1.0-ONNX \
    onnx/model_quantized.onnx \
    voices/voices-v1.0.bin \
    --local-dir /path/to/kokoro-tts

mv /path/to/kokoro-tts/onnx/model_quantized.onnx /path/to/kokoro-tts/model.onnx
mv /path/to/kokoro-tts/voices/voices-v1.0.bin    /path/to/kokoro-tts/voices.bin
```

## Install & run

```bash
# Install bundle from Git
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir kokoro-tts

# Load model into daemon
gonnxctl load kokoro-tts

# Synthesize
curl -s -X POST http://localhost:8080/v1/models/kokoro-tts/predict \
  -H 'Content-Type: application/json' \
  -d @examples/request.json \
  | jq -r .audio_b64 | base64 -d > output.wav

aplay output.wav
```

## Input / Output

**Request:**
```json
{
  "text": "Hello world",
  "voice": "af_heart",
  "lang": "en-us",
  "speed": 1.0
}
```
- `lang` is optional — auto-detected from voice prefix.

**Response:**
```json
{
  "audio_b64": "<base64-encoded WAV>",
  "sample_rate": 24000,
  "voice": "af_heart",
  "lang": "en-us"
}
```
Output is a 16-bit PCM WAV, 24000 Hz, mono.

## G2P extras

For non-English languages install the corresponding misaki extra:

```bash
pip install 'misaki[ja]'   # Japanese
pip install 'misaki[zh]'   # Chinese
# For ES/FR/HI/IT/PT also install system package:
apt install espeak-ng
pip install 'misaki[es,fr,hi,it,pt]'
```

## Notes

- `maxConcurrency: 1` — ONNX Runtime sessions are not thread-safe without
  re-entrant sessions; increase only if you wrap with a session pool.
- `idleUnloadSeconds: 1800` — model is unloaded after 30 min of inactivity
  to free ~325 MB (fp32) or ~82 MB (int8 quantized) of RAM.
