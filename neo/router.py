from __future__ import annotations

from dataclasses import dataclass

from .core.brain import LocalBrain
from .memory import Memory
from .tools.system import laptop_status, open_application, open_url, web_search

@dataclass(frozen=True)
class CommandResult:
    text: str
    should_exit: bool = False

class CommandRouter:
    """Deterministic tool router with optional natural-language fallback."""

    def __init__(self, memory: Memory, brain: LocalBrain | None = None) -> None:
        self.memory = memory
        self.brain = brain

    def route(self, raw_command: str) -> CommandResult:
        command = raw_command.strip()
        lowered = command.lower()

        if not command:
            return CommandResult("I did not catch a command.")

        if lowered in {"exit", "quit", "shutdown neo", "goodbye"}:
            return CommandResult("Shutting down. See you soon, Neal.", True)

        if lowered in {"help", "commands"}:
            return CommandResult(
                "Commands: help | status | open <app> | url <address> | "
                "search <query> | remember <key> = <value> | recall <key> | exit"
            )

        if lowered == "status":
            return CommandResult(laptop_status())

        if lowered.startswith("open "):
            return CommandResult(open_application(command[5:]))

        if lowered.startswith("url "):
            return CommandResult(open_url(command[4:]))

        if lowered.startswith("search "):
            return CommandResult(web_search(command[7:]))

        if lowered.startswith("remember "):
            payload = command[9:].strip()
            if "=" not in payload:
                return CommandResult("Use: remember <key> = <value>")
            key, value = payload.split("=", 1)
            if not key.strip() or not value.strip():
                return CommandResult("Both a memory key and value are required.")
            self.memory.remember(key, value)
            return CommandResult(f"Remembered {key.strip()}.")

        if lowered.startswith("recall "):
            key = command[7:].strip()
            value = self.memory.recall(key)
            if value is None:
                return CommandResult(f"I do not remember anything for {key}.")
            return CommandResult(f"{key}: {value}")

        if self.brain is not None:
            response = self.brain.ask(command)
            if response:
                return CommandResult(response)

        return CommandResult(
            "I do not know that command yet. Type help to see Neo V1 commands."
        )
