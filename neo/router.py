from __future__ import annotations

from dataclasses import dataclass

from .core.brain import LocalBrain
from .memory import Memory
from .tools.system import (
    create_folder,
    laptop_status,
    lock_laptop,
    network_status,
    open_application,
    open_folder,
    open_url,
    web_search,
)

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

        if lowered in {"help", "commands", "what can you do", "what can you do?"}:
            return CommandResult(
                "I can open apps and websites, open Desktop/Downloads/Documents/"
                "Pictures/Music/Videos, search Google, create a folder on an "
                "approved standard folder, report laptop/network status, remember "
                "information, and lock the Windows laptop."
            )

        if lowered in {"status", "laptop status", "system status"}:
            return CommandResult(laptop_status())

        if lowered in {"network", "network status", "my ip", "ip address"}:
            return CommandResult(network_status())

        if lowered in {
            "lock laptop",
            "lock my laptop",
            "lock computer",
            "lock my computer",
        }:
            return CommandResult(lock_laptop())

        if lowered.startswith("open folder "):
            return CommandResult(open_folder(command[12:]))

        if lowered.startswith("open my "):
            target = command[8:].strip().lower()
            if target in {"desktop", "downloads", "documents", "pictures", "music", "videos"}:
                return CommandResult(open_folder(target))

        if lowered.startswith("open "):
            target = command[5:].strip()
            folder_key = target.lower()
            if folder_key in {"desktop", "downloads", "documents", "pictures", "music", "videos"}:
                return CommandResult(open_folder(folder_key))
            return CommandResult(open_application(target))

        if lowered.startswith("create folder "):
            payload = command[14:].strip()
            location = "desktop"

            marker = " in "
            if marker in payload.lower():
                split_index = payload.lower().rfind(marker)
                name = payload[:split_index].strip()
                location = payload[split_index + len(marker):].strip()
            else:
                name = payload

            return CommandResult(create_folder(name, location))

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
