from __future__ import annotations

from ..config import Settings
from ..logger import get_logger
from ..memory import Memory
from ..router import CommandRouter
from .brain import LocalBrain

class NeoAssistant:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.logger = get_logger()
        self.memory = Memory()
        self.brain = LocalBrain(settings)
        self.router = CommandRouter(self.memory, self.brain)

    def greeting(self) -> str:
        llm_state = "enabled" if self.settings.llm_enabled else "disabled"
        return (
            f"Hello {self.settings.user_name}. "
            f"I am {self.settings.name} v{self.settings.version}. "
            f"Local brain: {llm_state}. Type help to get started."
        )

    def handle(self, command: str) -> tuple[str, bool]:
        result = self.router.route(command)
        self.logger.info("command=%r exit=%s", command, result.should_exit)
        return result.text, result.should_exit
