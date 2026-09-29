from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "config.json"


@dataclass(frozen=True)
class Settings:
    name: str = "Neo"
    user_name: str = "Neal"
    version: str = "0.1.0"
    safe_mode: bool = True
    llm_enabled: bool = False
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2"
    vosk_model_path: str = "models/vosk-model-small-en-us-0.15"
    audio_device_index: int = -1
    audio_blocksize: int = 4000
    command_max_seconds: float = 8.0
    command_silence_seconds: float = 1.1
    tts_voice: str = ""
    tts_rate: int = 175
    tts_volume: float = 1.0


def load_settings() -> Settings:
    data = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}

    raw_safe_mode = data.get("safe_mode", True)
    safe_mode = raw_safe_mode if isinstance(raw_safe_mode, bool) else str(raw_safe_mode).lower() == "true"
    raw_llm = os.getenv("NEO_LLM_ENABLED", data.get("llm_enabled", False))
    llm_enabled = raw_llm if isinstance(raw_llm, bool) else str(raw_llm).lower() == "true"

    return Settings(
        name=os.getenv("NEO_NAME", data.get("name", "Neo")),
        user_name=os.getenv("NEO_USER_NAME", data.get("user_name", "Neal")),
        version=data.get("version", "0.1.0"),
        safe_mode=safe_mode,
        llm_enabled=llm_enabled,
        ollama_url=os.getenv("OLLAMA_URL", data.get("ollama_url", "http://127.0.0.1:11434")),
        ollama_model=os.getenv("OLLAMA_MODEL", data.get("ollama_model", "llama3.2")),
        vosk_model_path=os.getenv(
            "NEO_VOSK_MODEL_PATH",
            data.get("vosk_model_path", "models/vosk-model-small-en-us-0.15"),
        ),
        audio_device_index=int(os.getenv("NEO_AUDIO_DEVICE", data.get("audio_device_index", -1))),
        audio_blocksize=int(os.getenv("NEO_AUDIO_BLOCKSIZE", data.get("audio_blocksize", 4000))),
        command_max_seconds=float(os.getenv("NEO_COMMAND_MAX_SECONDS", data.get("command_max_seconds", 8.0))),
        command_silence_seconds=float(
            os.getenv(
                "NEO_COMMAND_SILENCE_SECONDS",
                data.get("command_silence_seconds", 1.1),
            )
        ),
        tts_voice=os.getenv("NEO_TTS_VOICE", data.get("tts_voice", "")),
        tts_rate=int(os.getenv("NEO_TTS_RATE", data.get("tts_rate", 175))),
        tts_volume=float(os.getenv("NEO_TTS_VOLUME", data.get("tts_volume", 1.0))),
    )
