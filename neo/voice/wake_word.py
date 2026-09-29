from __future__ import annotations

import os
from pathlib import Path


class WakeWordDetector:
    """Always-on local wake-word detector using a custom Porcupine model."""

    def __init__(
        self,
        keyword_path: Path,
        access_key: str | None = None,
        device_index: int = -1,
        sensitivity: float = 0.55,
    ) -> None:
        try:
            import pvporcupine
            from pvrecorder import PvRecorder
        except ImportError as exc:
            raise RuntimeError(
                "Voice dependencies are missing. Run: "
                "python -m pip install -r requirements.txt"
            ) from exc

        access_key = access_key or os.getenv("PICOVOICE_ACCESS_KEY")
        if not access_key:
            raise RuntimeError(
                "PICOVOICE_ACCESS_KEY is missing. Create a Picovoice account, "
                "copy your AccessKey, and store it in the environment."
            )

        if not keyword_path.exists():
            raise FileNotFoundError(
                f"Wake-word model not found: {keyword_path}\n"
                "Create a custom 'Neo' keyword model for Windows and place the "
                "downloaded .ppn file at this path."
            )

        self._porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[str(keyword_path)],
            sensitivities=[sensitivity],
        )
        self._recorder = PvRecorder(
            frame_length=self._porcupine.frame_length,
            device_index=device_index,
        )
        self._triggered = False

    def wait(self) -> None:
        """Block until the custom 'Neo' keyword is detected."""
        self._recorder.start()
        try:
            while True:
                frame = self._recorder.read()
                if self._porcupine.process(frame) >= 0:
                    self._triggered = True
                    return
        finally:
            self._recorder.stop()

    @property
    def recorder(self):
        """Expose the recorder so STT can continue using the same device."""
        return self._recorder

    def close(self) -> None:
        try:
            self._recorder.delete()
        finally:
            self._porcupine.delete()
