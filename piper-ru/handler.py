"""Piper ONNX Russian TTS handler for gonnx.

Expects:
  model.onnx       — Piper ONNX model
  model.onnx.json  — Phoneme ID map and audio config

Both files are downloaded as assets at pull time (see manifest.yaml).
The default voice is ru_RU-irina-medium from rhasspy/piper-voices.

Output: WAV base64, 22050 Hz (voice-dependent), mono, 16-bit PCM.
"""
from __future__ import annotations

import base64
import io
import json
import wave

import numpy as np
import onnxruntime as ort
from phonemizer.backend import EspeakBackend

from gonnx import ModelWorker, Request, WorkerContext


class PiperWorker(ModelWorker):
    def load(self, ctx: WorkerContext) -> None:
        config_path = ctx.asset("model.onnx.json")
        with open(config_path, encoding="utf-8") as f:
            self._config = json.load(f)

        self._sample_rate: int = self._config["audio"]["sample_rate"]
        self._num_speakers: int = self._config.get("num_speakers", 1)
        self._phoneme_to_id: dict = self._config["phoneme_id_map"]
        espeak_voice: str = self._config.get("espeak", {}).get("voice", "ru")

        self._sess = ort.InferenceSession(
            ctx.model_path,
            providers=ctx.providers,
        )
        self._backend = EspeakBackend(
            espeak_voice,
            with_stress=True,
            language_switch="remove-flags",
        )

    def predict(self, req: Request) -> dict:
        text: str = req.json["text"]
        speaker_id: int = int(req.json.get("speaker_id", 0))
        length_scale: float = float(req.json.get("length_scale", 1.0))
        noise_scale: float = float(req.json.get("noise_scale", 0.667))
        noise_w: float = float(req.json.get("noise_w", 0.8))

        phoneme_ids = self._phonemize(text)
        inputs = {
            "input":         np.array([phoneme_ids], dtype=np.int64),
            "input_lengths": np.array([len(phoneme_ids)], dtype=np.int64),
            "scales":        np.array([noise_scale, length_scale, noise_w],
                                      dtype=np.float32),
        }
        if self._num_speakers > 1:
            inputs["sid"] = np.array([speaker_id], dtype=np.int64)

        audio = self._sess.run(None, inputs)[0].squeeze().astype(np.float32)
        audio = np.clip(audio, -1.0, 1.0)

        return {
            "audio_b64": _to_wav_b64(audio, self._sample_rate),
            "sample_rate": self._sample_rate,
        }

    def _phonemize(self, text: str) -> list[int]:
        p2i = self._phoneme_to_id
        bos = p2i.get("^", [1])[0]
        eos = p2i.get("$", [2])[0]
        phonemes = self._backend.phonemize([text], njobs=1)[0]
        ids = [bos]
        for ph in phonemes:
            ids += p2i.get(ph, [])
        ids.append(eos)
        return ids


def _to_wav_b64(audio: np.ndarray, sample_rate: int) -> str:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    return base64.b64encode(buf.getvalue()).decode()


app = PiperWorker()
