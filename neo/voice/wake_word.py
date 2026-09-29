from __future__ import annotations

import json
import queue
import time
from pathlib import Path

import sounddevice as sd


class WakeWordDetector:
    """Offline wake-word detector using Vosk with an exact 'neo' grammar."""

    def __init__(
        self,
        model_path: Path,
        device_index: int = -1,
        sample_rate: int = 16000,
        blocksize: int = 2000,
    ) -> None:
        try:
            from vosk import KaldiRecognizer, Model, SetLogLevel
        except ImportError as exc:
            raise RuntimeError(
                "Voice dependencies are missing. Run: "
                "python -m pip install -r requirements.txt"
            ) from exc

        if not model_path.exists():
            raise FileNotFoundError(f"Vosk model not found: {model_path}")

        self._KaldiRecognizer = KaldiRecognizer
        SetLogLevel(-1)

        self.model = Model(str(model_path))
        self.device_index = None if device_index < 0 else device_index
        self.sample_rate = sample_rate
        self.blocksize = blocksize
        self._queue: queue.Queue[bytes] = queue.Queue(maxsize=30)

    def _callback(self, indata, frames, callback_time, status) -> None:
        del frames, callback_time
        if status:
            pass
        try:
            self._queue.put_nowait(bytes(indata))
        except queue.Full:
            pass

    @staticmethod
    def _contains_wake_word(result: str) -> bool:
        try:
            text = json.loads(result).get("partial", "").strip().lower()
            if not text:
                text = json.loads(result).get("text", "").strip().lower()
        except json.JSONDecodeError:
            return False

        return "neo" in text.split()

    def wait(self, timeout: float | None = None) -> bool:
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

        recognizer = self._KaldiRecognizer(
            self.model,
            self.sample_rate,
            json.dumps(["neo"]),
        )

        started = time.monotonic()

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.blocksize,
            device=self.device_index,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            while True:
                if timeout is not None and time.monotonic() - started >= timeout:
                    return False

                try:
                    data = self._queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                if recognizer.AcceptWaveform(data):
                    if self._contains_wake_word(recognizer.Result()):
                        return True
                elif self._contains_wake_word(recognizer.PartialResult()):
                    return True
