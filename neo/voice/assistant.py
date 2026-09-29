from __future__ import annotations

from pathlib import Path

from ..config import ROOT_DIR, Settings
from ..core.assistant import NeoAssistant
from .stt import SpeechListener
from .tts import Speaker
from .wake_word import WakeWordDetector


class VoiceAssistant:
    """Silent standby -> hear 'Neo' -> listen -> respond."""

    def __init__(self, settings: Settings, assistant: NeoAssistant) -> None:
        self.settings = settings
        self.assistant = assistant

        self.speaker = Speaker(
            voice_name=settings.tts_voice or None,
            rate=settings.tts_rate,
            volume=settings.tts_volume,
        )

        model_path = Path(settings.vosk_model_path)
        if not model_path.is_absolute():
            model_path = ROOT_DIR / model_path

        self.wake = WakeWordDetector(
            model_path=model_path,
            device_index=settings.audio_device_index,
            blocksize=settings.audio_blocksize,
        )

        self.listener = SpeechListener(
            model_path=model_path,
            device_index=settings.audio_device_index,
            max_seconds=settings.command_max_seconds,
            silence_seconds=settings.command_silence_seconds,
            blocksize=settings.audio_blocksize,
        )

    def run(self) -> None:
        print("[Neo] Voice mode active. Waiting for 'Neo'.")

        try:
            while True:
                print("[Neo] Standby...")

                if not self.wake.wait():
                    continue

                self.speaker.speak("Yes, Neal?")
                print("[Neo] Wake word detected. Listening...")

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
