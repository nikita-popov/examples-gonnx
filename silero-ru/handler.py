"""Silero TTS Russian handler for gonnx.

Uses the Silero v4 TorchScript model (.pt) loaded via torch.jit.load().
No ONNX runtime is involved — engine: torch in the manifest is intentional.

Silero does not publish an ONNX export for TTS; this bundle demonstrates
that gonnx handlers are not limited to onnxruntime and can wrap any
Python inference backend.

Model: silero-models v4_ru (5 speakers, 8/24/48 kHz)
Source: https://github.com/snakers4/silero-models
"""
from __future__ import annotations

import base64
import io
import wave

import numpy as np
import torch

from gonnx import ModelWorker, Request, WorkerContext

_SPEAKERS = {"aidar", "baya", "kseniya", "xenia", "eugene", "random"}
_SAMPLE_RATES = {8000, 24000, 48000}


class SileroWorker(ModelWorker):
    def load(self, ctx: WorkerContext) -> None:
        # ctx.model_path = GONNX_MODEL_PATH env var (absolute path to model.pt)
        self._model = torch.jit.load(ctx.model_path, map_location=torch.device("cpu"))
        self._model.eval()

    def predict(self, req: Request) -> dict:
        text: str = req.json["text"]
        speaker: str = req.json.get("speaker", "xenia")
        sample_rate: int = int(req.json.get("sample_rate", 24000))
        put_accent: bool = bool(req.json.get("put_accent", True))
        put_yo: bool = bool(req.json.get("put_yo", True))

        if speaker not in _SPEAKERS:
            raise ValueError(f"unknown speaker {speaker!r}; choose from {sorted(_SPEAKERS)}")
        if sample_rate not in _SAMPLE_RATES:
            raise ValueError(f"unsupported sample_rate {sample_rate}; choose from {sorted(_SAMPLE_RATES)}")

        with torch.no_grad():
            audio = self._model.apply_tts(
                text=text,
                speaker=speaker,
                sample_rate=sample_rate,
                put_accent=put_accent,
                put_yo=put_yo,
            )

        audio_np = audio.numpy() if isinstance(audio, torch.Tensor) else np.asarray(audio)
        return {
            "audio_b64": _to_wav_b64(audio_np, sample_rate),
            "sample_rate": sample_rate,
            "speaker": speaker,
        }


def _to_wav_b64(audio: np.ndarray, sample_rate: int) -> str:
    audio = np.clip(audio, -1.0, 1.0)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    return base64.b64encode(buf.getvalue()).decode()


app = SileroWorker()
