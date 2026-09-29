from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import ROOT_DIR

class Memory:
    """Small local JSON memory store for Neo V1."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (ROOT_DIR / "data" / "memory.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            self._data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self._data = {}

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def remember(self, key: str, value: str) -> None:
        self._data[key.strip().lower()] = value.strip()
        self._save()

    def recall(self, key: str) -> str | None:
        value = self._data.get(key.strip().lower())
        return str(value) if value is not None else None
