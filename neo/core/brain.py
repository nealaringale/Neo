from __future__ import annotations

import json
import urllib.error
import urllib.request

from ..config import Settings


class LocalBrain:
    """Optional Ollama-backed language model interface.

    Neo remains usable without Ollama. When the local model is unavailable,
    callers receive None and can fall back to deterministic tools.
    """

    def __init__(self, settings: Settings) -> None:
        self.enabled = settings.llm_enabled
        self.model = settings.ollama_model
        self.url = settings.ollama_url.rstrip("/") + "/api/chat"

    def ask(self, prompt: str) -> str | None:
        if not self.enabled:
            return None

        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Neo, Neal's personal laptop AI assistant. "
                        "Be concise, practical, and honest. "
                        "Do not claim to have performed an action unless a tool reports success."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }

        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            return None

        message = data.get("message", {})
        content = message.get("content")
        return content.strip() if isinstance(content, str) and content.strip() else None
