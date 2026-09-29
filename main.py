from __future__ import annotations

import argparse
from pathlib import Path

# Windows checkouts can expose Git's "neo" package directory as "Neo".
# Support both layouts and avoid collisions with a third-party package.
try:
    from neo.config import ROOT_DIR, load_settings
    from neo.core.assistant import NeoAssistant
    PACKAGE_NAME = "neo"
except ModuleNotFoundError as exc:
    if not (exc.name == "neo" or (exc.name and exc.name.startswith("neo."))):
        raise
    from Neo.config import ROOT_DIR, load_settings
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


def run_microphone_test() -> None:
    if PACKAGE_NAME == "neo":
        from neo.voice.diagnostics import microphone_test
    else:
        from Neo.voice.diagnostics import microphone_test

    settings = load_settings()
    model_path = Path(settings.vosk_model_path)
    if not model_path.is_absolute():
        model_path = ROOT_DIR / model_path

    microphone_test(
        model_path=model_path,
        device_index=settings.audio_device_index,
        seconds=6.0,
    )


def run_wake_test() -> None:
    if PACKAGE_NAME == "neo":
        from neo.voice.diagnostics import wake_test
    else:
        from Neo.voice.diagnostics import wake_test

    settings = load_settings()
    model_path = Path(settings.vosk_model_path)
    if not model_path.is_absolute():
        model_path = ROOT_DIR / model_path

    wake_test(
        model_path=model_path,
        device_index=settings.audio_device_index,
        seconds=10.0,
    )


def list_microphones() -> None:
    if PACKAGE_NAME == "neo":
        from neo.voice.diagnostics import list_microphones as show_microphones
    else:
        from Neo.voice.diagnostics import list_microphones as show_microphones

    show_microphones()


def main() -> None:
    parser = argparse.ArgumentParser(description="Neo personal laptop assistant")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--voice", action="store_true", help="start wake-word voice mode")
    group.add_argument("--mic-test", action="store_true", help="test microphone and Vosk")
    group.add_argument("--wake-test", action="store_true", help="test detection of the word Neo")
    group.add_argument("--list-mics", action="store_true", help="list available microphones")
    args = parser.parse_args()

    if args.voice:
        run_voice_mode()
    elif args.mic_test:
        run_microphone_test()
    elif args.wake_test:
        run_wake_test()
    elif args.list_mics:
        list_microphones()
    else:
        run_text_mode()


if __name__ == "__main__":
    main()
