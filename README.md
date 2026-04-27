# examples-gonnx

Official bundle examples for [gonnx](https://github.com/nikita-popov/gonnx) — Git-first ONNX model runtime.

Each subdirectory is a self-contained **gonnx bundle**: a `manifest.yaml`, a Python handler, any required assets, and an example request. Install any example directly from this repo:

```sh
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir resnet50
```

## Examples

| Bundle | Task | Model | Provider |
|--------|------|-------|----------|
| [resnet50](./resnet50) | Image classification (ImageNet-1k) | ResNet-50 | CPU / CUDA |

## Bundle structure

```
<bundle>/
  manifest.yaml          # required: name, runtime, handler, interface, policy
  handler.py             # Python handler (ModelWorker subclass)
  requirements.txt       # pip dependencies for the handler
  assets/                # static files referenced via ctx.asset()
  examples/
    request.json         # sample inference request
```

## Contributing

1. Create a new subdirectory with the bundle name.
2. Add `manifest.yaml`, `handler.py`, `requirements.txt`, `assets/`, `examples/request.json`.
3. Update the table in this README.
4. Open a PR.

## License

MIT © Nikita Popov
