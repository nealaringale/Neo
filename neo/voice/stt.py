from __future__ import annotations

import json
from array import array
from pathlib import Path
import time


class SpeechListener:
    """Offline command recognizer using Vosk and the existing microphone."""

    def __init__(
        self,
        model_path: Path,
        device_recorder,
        max_seconds: float = 8.0,
    ) -> None:
        try:
            from vosk import KaldiRecognizer, Model
        except ImportError as exc:
            raise RuntimeError(
                "Vosk is not installed. Run: python -m pip install -r requirements.txt"
            ) from exc

        if not model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found: {model_path}\n"
                "Download the small Indian-English Vosk model and extract it there."
            )

        self._model = Model(str(model_path))
        self._recorder = device_recorder
        self._sample_rate = int(self._recorder.sample_rate)
        self._max_seconds = max_seconds
        self._Recognizer = KaldiRecognizer

    def listen(self) -> str:
        recognizer = self._Recognizer(self._model, self._sample_rate)
        started = time.monotonic()

        self._recorder.start()
        try:
            while time.monotonic() - started < self._max_seconds:
                frame = self._recorder.read()
                pcm = array("h", frame).tobytes()

                if recognizer.AcceptWaveform(pcm):
                    data = json.loads(recognizer.Result())
                    text = data.get("text", "").strip()
                    if text:
                        return text

            data = json.loads(recognizer.FinalResult())
            return data.get("text", "").strip()
        finally:
            self._recorder.stop()
