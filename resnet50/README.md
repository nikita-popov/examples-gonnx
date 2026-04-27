# resnet50

Image classification bundle for [gonnx](https://github.com/nikita-popov/gonnx).

Classifies an input image into one of the **ImageNet-1k** classes using a ResNet-50 ONNX model.

## Install

```sh
gonnxctl install https://github.com/nikita-popov/examples-gonnx.git --dir resnet50
```

## Model

Export a ResNet-50 from torchvision and place it at `model.onnx` inside the bundle directory:

```python
import torch, torchvision
model = torchvision.models.resnet50(weights="IMAGENET1K_V2")
model.eval()
dummy = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy, "model.onnx",
                  input_names=["input"], output_names=["output"],
                  dynamic_axes={"input": {0: "batch"}})
```

Then replace `assets/labels.txt` with the full ImageNet-1k label list (1000 lines).

## Input

```json
{
  "image": "<base64-encoded JPEG or PNG>",
  "top_k": 5
}
```

## Output

```json
{
  "classes": [
    {"label": "golden retriever", "score": 0.823},
    {"label": "Labrador retriever", "score": 0.091}
  ]
}
```

## Quick run

```sh
# encode a local image and run inference
base64 -w0 cat.jpg | python3 -c "
import sys, json
print(json.dumps({'image': sys.stdin.read(), 'top_k': 3}))
" | gonnxctl run resnet50
```
