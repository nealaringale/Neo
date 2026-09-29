from __future__ import annotations

import argparse

# Windows checkouts can expose Git's "neo" package directory as "Neo".
# Linux/macOS keep the lower-case package name. Support both layouts.
try:
    from neo.config import load_settings
    from neo.core.assistant import NeoAssistant
    PACKAGE_NAME = "neo"
except ModuleNotFoundError as exc:
    if exc.name != "neo.config":
        raise
    from Neo.config import load_settings
    from Neo.core.assistant import NeoAssistant
    PACKAGE_NAME = "Neo"


def run_text_mode() -> None:
    settings = load_settings()
    neo = NeoAssistant(settings)

    print("=" * 56)
    print(f"{settings.name} - Personal Laptop Assistant")
    print("=" * 56)
    print(neo.greeting())

    while True:
        try:
            command = input("\nYou > ")
        except (EOFError, KeyboardInterrupt):
            print("\nNeo > Shutting down. See you soon, Neal.")
            break

        response, should_exit = neo.handle(command)
        print(f"Neo > {response}")

        if should_exit:
            break


def run_voice_mode() -> None:
    if PACKAGE_NAME == "neo":
        from neo.voice.assistant import VoiceAssistant
    else:
        from Neo.voice.assistant import VoiceAssistant

    settings = load_settings()
    neo = NeoAssistant(settings)
    VoiceAssistant(settings, neo).run()


def main() -> None:
    parser = argparse.ArgumentParser(description="Neo personal laptop assistant")
    parser.add_argument(
        "--voice",
        action="store_true",
        help="start wake-word voice mode",
    )
    args = parser.parse_args()

    if args.voice:
        run_voice_mode()
    else:
        run_text_mode()


if __name__ == "__main__":
    main()
