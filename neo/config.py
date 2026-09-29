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

def load_settings() -> Settings:
    data = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}

    raw_safe_mode = data.get("safe_mode", True)
    safe_mode = raw_safe_mode if isinstance(raw_safe_mode, bool) else str(raw_safe_mode).lower() == "true"

    return Settings(
        name=os.getenv("NEO_NAME", data.get("name", "Neo")),
        user_name=os.getenv("NEO_USER_NAME", data.get("user_name", "Neal")),
        version=data.get("version", "0.1.0"),
        safe_mode=safe_mode,
    )
