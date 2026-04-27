# resnet50

ImageNet-1k image classification using ResNet-50 ONNX.

## Assets

This bundle uses one asset declared in `manifest.yaml`:

| Asset ID | File | Size | Source |
|----------|------|------|--------|
| `model` | `model.onnx` | ~102 MB | [microsoft/resnet-50](https://huggingface.co/microsoft/resnet-50) on HuggingFace |

The file is **not committed to Git**. Fetch it with:

```sh
gonnxctl pull resnet50
```

## Install and run

```sh
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir resnet50
gonnxctl pull resnet50
gonnxctl load resnet50
gonnxctl run resnet50 -f examples/request.json
```

## Request format

```json
{
  "image": "<base64-encoded JPEG or PNG>",
  "top_k": 5
}
```

## Response format

```json
{
  "classes": [
    { "label": "tiger cat", "score": 0.412 },
    { "label": "tabby",     "score": 0.231 }
  ]
}
```

## Preprocessing

The handler resizes the image to 224×224, normalises with ImageNet mean/std
`([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])`, and runs the ONNX session.
Labels are loaded from `assets/labels.txt` (committed in Git — it is a small
text file, not an asset).

## Provider fallback

The manifest lists `CUDAExecutionProvider` first. ONNX Runtime falls back to
`CPUExecutionProvider` automatically if no CUDA device is available.
