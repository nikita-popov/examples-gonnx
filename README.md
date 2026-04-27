# examples-gonnx

Official bundle examples for [gonnx](https://github.com/nikita-popov/gonnx) —
Git-first ONNX model runtime.

Each subdirectory is a self-contained **gonnx bundle**: `manifest.yaml`, a Python
handler, and an `assets[]` section that declares the large binary files (model
weights, voice packs, vocabularies) to fetch separately via `gonnxctl pull`.

## Quick start

```sh
# 1. Install the bundle from this repo (no large files downloaded yet)
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir resnet50

# 2. Fetch declared assets (model.onnx etc.), verify sha256
gonnxctl pull resnet50

# 3. Load the worker process
gonnxctl load resnet50

# 4. Run inference
gonnxctl run resnet50 -f resnet50/examples/request.json
```

Replace `resnet50` with any bundle name from the table below.

## Examples

| Bundle | Task | Model | Assets fetched by `pull` |
|--------|------|-------|-------------------------|
| [resnet50](./resnet50) | Image classification (ImageNet-1k) | ResNet-50 ONNX (fp32, ~100 MB) | `model.onnx` |
| [kokoro-tts](./kokoro-tts) | Text-to-speech (9 languages) | Kokoro-82M ONNX (~330 MB) | `model.onnx`, `voices.bin` |

## How assets work

Large binary files are **not committed to Git**. They are declared in
`manifest.yaml` under the `assets:` key:

```yaml
assets:
  - id: model
    url: https://huggingface.co/.../model.onnx
    sha256: <64-char hex>        # mandatory — cache key + integrity check
    size: 102400000              # bytes, for progress bar only
    dest: ./model.onnx           # path relative to bundle directory
```

`gonnxctl pull <name>` downloads each asset, verifies the sha256, and places it
at `dest`. If the file already exists with the correct hash, it is skipped.
A failed download never corrupts an existing valid file.

See the [RFC](https://github.com/nikita-popov/gonnx/blob/master/docs/rfc-v0.md)
for the full asset specification.

## Bundle layout

```
<bundle>/
  manifest.yaml          # required — name, runtime, handler, interface, policy, assets
  handler.py             # Python handler (ModelWorker subclass)
  requirements.txt       # pip dependencies for the handler
  .gitignore             # excludes asset dest files (model.onnx etc.)
  examples/
    request.json         # sample inference request
```

## Contributing

1. Create a new subdirectory with the bundle name.
2. Add `manifest.yaml` with an `assets:` section for all large files.
3. Add `handler.py`, `requirements.txt`, `examples/request.json`.
4. Add `.gitignore` listing all `assets[].dest` paths.
5. Update the table above.
6. Open a PR.

## License

MIT © Nikita Popov
