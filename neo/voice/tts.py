from __future__ import annotations

import platform
from typing import Any


class Speaker:
    """Text-to-speech speaker with automatic female-voice selection on Windows."""

    def __init__(
        self,
        voice_name: str | None = None,
        rate: int = 175,
        volume: float = 1.0,
    ) -> None:
        try:
            import pyttsx3
        except ImportError as exc:
            raise RuntimeError(
                "pyttsx3 is not installed. Run: python -m pip install -r requirements.txt"
            ) from exc

        self._engine = pyttsx3.init("sapi5" if platform.system() == "Windows" else None)
        self._engine.setProperty("rate", rate)
        self._engine.setProperty("volume", max(0.0, min(1.0, volume)))

        if voice_name:
            self._select_voice_by_name(voice_name)
        else:
            self._select_female_voice()

    def _voices(self) -> list[Any]:
        return list(self._engine.getProperty("voices") or [])

    def _select_voice_by_name(self, voice_name: str) -> None:
        target = voice_name.lower()
        for voice in self._voices():
            label = f"{getattr(voice, 'name', '')} {getattr(voice, 'id', '')}".lower()
            if target in label:
                self._engine.setProperty("voice", voice.id)
                return
        raise RuntimeError(f"Could not find TTS voice matching: {voice_name}")

    def _select_female_voice(self) -> None:
        voices = self._voices()
        preferred = (
            "zira",
            "jenny",
            "aria",
            "susan",
            "hazel",
            "samantha",
            "female",
            "woman",
        )

        for voice in voices:
            label = f"{getattr(voice, 'name', '')} {getattr(voice, 'id', '')}".lower()
            if any(word in label for word in preferred):
                self._engine.setProperty("voice", voice.id)
                return

        # Windows often exposes at least one Microsoft voice even when its
        # metadata does not identify gender. Keep the first available voice
        # as a portable fallback rather than failing startup.
        if voices:
            self._engine.setProperty("voice", voices[0].id)

    def speak(self, text: str) -> None:
        if not text.strip():
            return
        self._engine.say(text)
        self._engine.runAndWait()
