from __future__ import annotations

import os
from pathlib import Path

from ..config import ROOT_DIR, Settings
from ..core.assistant import NeoAssistant
from .stt import SpeechListener
from .tts import Speaker
from .wake_word import WakeWordDetector


class VoiceAssistant:
    """Wake-word voice loop: listen silently -> hear Neo -> listen -> respond."""

    def __init__(self, settings: Settings, assistant: NeoAssistant) -> None:
        self.settings = settings
        self.assistant = assistant
        self.speaker = Speaker(
            voice_name=settings.tts_voice or None,
            rate=settings.tts_rate,
            volume=settings.tts_volume,
        )

        keyword_path = Path(settings.wake_word_path)
        if not keyword_path.is_absolute():
            keyword_path = ROOT_DIR / keyword_path

        model_path = Path(settings.vosk_model_path)
        if not model_path.is_absolute():
            model_path = ROOT_DIR / model_path

        self.wake = WakeWordDetector(
            keyword_path=keyword_path,
            access_key=os.getenv("PICOVOICE_ACCESS_KEY"),
            device_index=settings.audio_device_index,
            sensitivity=settings.wake_sensitivity,
        )
        self.listener = SpeechListener(
            model_path=model_path,
            device_recorder=self.wake.recorder,
            max_seconds=settings.command_max_seconds,
        )

    def run(self) -> None:
        self.speaker.speak(
            f"Neo voice mode is active. Say Neo when you need me, {self.settings.user_name}."
        )

        try:
            while True:
                print("\n[Neo] Listening for wake word...")
                self.wake.wait()

                self.speaker.speak("Yes, Neal?")
                print("[Neo] Wake word detected. Listening for command...")

                command = self.listener.listen()
                if not command:
                    self.speaker.speak("I didn't catch that.")
                    continue

                print(f"You: {command}")
                response, should_exit = self.assistant.handle(command)
                print(f"Neo: {response}")
                self.speaker.speak(response)

                if should_exit:
                    break
        except KeyboardInterrupt:
            print("\n[Neo] Voice mode stopped.")
        finally:
            self.wake.close()
