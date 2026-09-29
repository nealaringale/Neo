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
    )
