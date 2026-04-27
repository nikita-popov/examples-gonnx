"""Kokoro TTS v1.0 handler for gonnx.

Expects:
  model.onnx   — Kokoro-82M ONNX model
               Download: https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX
               File: onnx/model.onnx  (fp32) or onnx/model_quantized.onnx (int8)
  voices.bin   — Kokoro voices binary
               Download: same HF repo, voices/voices-v1.0.bin

Place both files next to manifest.yaml before installing the bundle.

Output: WAV base64, 24000 Hz, mono, 16-bit PCM.
"""
from __future__ import annotations

import asyncio
import base64
import io
import wave

import numpy as np

from gonnx import ModelWorker, Request, WorkerContext

# Maps first character of voice prefix to BCP-47 language tag
_VOICE_LANG_MAP: dict[str, str] = {
    "a": "en-us",
    "b": "en-gb",
    "j": "ja",
    "z": "zh",
    "e": "es",
    "f": "fr",
    "h": "hi",
    "i": "it",
    "p": "pt",
}

_SAMPLE_RATE = 24_000


def _lang_from_voice(voice: str) -> str:
    return _VOICE_LANG_MAP.get(voice[0], "en-us")


def _audio_to_wav_b64(audio: np.ndarray, sample_rate: int = _SAMPLE_RATE) -> str:
    """Convert float32 numpy array [-1, 1] to base64-encoded 16-bit WAV."""
    pcm = np.clip(audio, -1.0, 1.0)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes((pcm * 32767).astype(np.int16).tobytes())
    return base64.b64encode(buf.getvalue()).decode()


class KokoroWorker(ModelWorker):
    def load(self, ctx: WorkerContext) -> None:
        from kokoro_onnx import Kokoro

        voices_path = ctx.asset("voices.bin")
        self.kokoro = Kokoro(ctx.model_path, voices_path)

    def predict(self, req: Request) -> dict:
        text: str = req.json["text"]
        voice: str = req.json.get("voice", "af_heart")
        lang: str = req.json.get("lang") or _lang_from_voice(voice)
        speed: float = float(req.json.get("speed", 1.0))

        # create_stream() is an async generator — must be consumed with asyncio.
        async def _collect() -> list[np.ndarray]:
            chunks: list[np.ndarray] = []
            async for samples, _sr in self.kokoro.create_stream(
                text, voice=voice, lang=lang, speed=speed
            ):
                chunks.append(samples)
            return chunks

        chunks = asyncio.run(_collect())

        audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.float32)

        return {
            "audio_b64": _audio_to_wav_b64(audio),
            "sample_rate": _SAMPLE_RATE,
            "voice": voice,
            "lang": lang,
        }


app = KokoroWorker()
