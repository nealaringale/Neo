from __future__ import annotations

import json
import queue
import time
from pathlib import Path

import sounddevice as sd


class SpeechListener:
    """Offline speech-to-text listener using Vosk."""

    def __init__(
        self,
        model_path: Path,
        device_index: int = -1,
        max_seconds: float = 8.0,
        silence_seconds: float = 1.1,
        blocksize: int = 4000,
    ) -> None:
        try:
            from vosk import KaldiRecognizer, Model, SetLogLevel
        except ImportError as exc:
            raise RuntimeError(
                "Vosk is not installed. Run: "
                "python -m pip install -r requirements.txt"
            ) from exc

        if not model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found: {model_path}"
            )

        self._Model = Model
        self._KaldiRecognizer = KaldiRecognizer
        SetLogLevel(-1)

        self.model = self._Model(str(model_path))
        self.device_index = None if device_index < 0 else device_index
        self.sample_rate = int(
            sd.query_devices(self.device_index, "input")["default_samplerate"]
        )
        self.max_seconds = max_seconds
        self.silence_seconds = silence_seconds
        self.blocksize = blocksize
        self._queue: queue.Queue[bytes] = queue.Queue(maxsize=20)

    def _callback(self, indata, frames, callback_time, status) -> None:
        del frames, callback_time
        if status:
            pass

        try:
            self._queue.put_nowait(bytes(indata))
        except queue.Full:
            pass

    def listen(self) -> str:
        recognizer = self._KaldiRecognizer(self.model, self.sample_rate)
        started = time.monotonic()
        last_speech = started
        heard_speech = False

        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.blocksize,
            device=self.device_index,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            while time.monotonic() - started < self.max_seconds:
                try:
                    data = self._queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                # Vosk's endpointing is the primary signal. The timeout gives
                # the user a natural pause after a short command.
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        return text
                    if heard_speech and time.monotonic() - last_speech >= self.silence_seconds:
                        break

                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get("partial", "").strip()
                if partial_text:
                    heard_speech = True
                    last_speech = time.monotonic()

                if heard_speech and time.monotonic() - last_speech >= self.silence_seconds:
                    break

        final_result = json.loads(recognizer.FinalResult())
        return final_result.get("text", "").strip()
