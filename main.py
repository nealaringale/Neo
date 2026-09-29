from __future__ import annotations

import argparse

from neo.config import load_settings
from neo.core.assistant import NeoAssistant


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
    from neo.voice.assistant import VoiceAssistant

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
