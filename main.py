from __future__ import annotations

from neo.config import load_settings
from neo.core.assistant import NeoAssistant

def main() -> None:
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

if __name__ == "__main__":
    main()
