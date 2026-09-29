from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from neo.memory import Memory
from neo.router import CommandRouter


class TestMemory(unittest.TestCase):
    def test_remember_and_recall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            memory = Memory(Path(tmp) / "memory.json")
            memory.remember("Editor", "VS Code")
            self.assertEqual(memory.recall("editor"), "VS Code")


class TestRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory = Memory(Path(self.temp_dir.name) / "memory.json")
        self.router = CommandRouter(self.memory)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_help(self) -> None:
        result = self.router.route("help")
        self.assertIn("status", result.text)

    def test_status(self) -> None:
        result = self.router.route("status")
        self.assertIn("OS:", result.text)

    def test_remember_and_recall(self) -> None:
        self.router.route("remember editor = VS Code")
        result = self.router.route("recall editor")
        self.assertEqual(result.text, "editor: VS Code")

    def test_exit(self) -> None:
        result = self.router.route("exit")
        self.assertTrue(result.should_exit)

    def test_unknown_command(self) -> None:
        result = self.router.route("do something impossible")
        self.assertIn("do not know", result.text.lower())


if __name__ == "__main__":
    unittest.main()
