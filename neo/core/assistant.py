from __future__ import annotations

from ..config import Settings
from ..logger import get_logger
from ..memory import Memory
from ..router import CommandRouter

class NeoAssistant:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.logger = get_logger()
        self.memory = Memory()
        self.router = CommandRouter(self.memory)

    def greeting(self) -> str:
        return (
            f"Hello {self.settings.user_name}. "
            f"I am {self.settings.name} v{self.settings.version}. "
            "Type help to get started."
        )

    def handle(self, command: str) -> tuple[str, bool]:
        result = self.router.route(command)
        self.logger.info("command=%r exit=%s", command, result.should_exit)
        return result.text, result.should_exit
