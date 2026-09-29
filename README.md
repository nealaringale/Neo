# Neo

Neo is a personal AI assistant for the laptop.

## V1 foundation

- deterministic command routing
- safe laptop actions
- local JSON memory
- optional local LLM brain through Ollama
- logging and configuration
- automated tests and GitHub Actions CI

## Voice mode

Neo now uses a completely local/free voice stack. There is no Picovoice account, AccessKey, or paid wake-word service.

The flow is:

1. Neo starts in silent standby.
2. Vosk continuously checks microphone audio with a restricted grammar containing only the wake word "neo".
3. When "neo" is detected, Neo says "Yes, Neal?"
4. Neo listens for the command.
5. Vosk transcribes the command locally.
6. Neo sends it through the approved tool router.
7. Neo speaks the result using the Windows-installed female TTS voice when one is available.

Vosk is an offline speech-recognition toolkit. The official model list includes the 36 MB Indian-English model vosk-model-small-en-in-0.4, which is intended for lightweight use.

### Install on Windows

    python -m pip install -r requirements.txt

### Download the voice model

Download:

    vosk-model-small-en-in-0.4

Extract it so this folder exists:

    models/vosk-model-small-en-in-0.4/

The model is not committed to GitHub.

### Female voice

Neo uses Windows SAPI5 through pyttsx3 and automatically prefers common installed female voices.

To choose a specific installed voice:

    $env:NEO_TTS_VOICE="Zira"

You can change speaking speed and volume with:

    $env:NEO_TTS_RATE="175"
    $env:NEO_TTS_VOLUME="1.0"

### Microphone

Neo uses the Windows default microphone by default.

To select another input device:

    $env:NEO_AUDIO_DEVICE="2"

Use -1 for the Windows default input device.

### Start voice mode

    python main.py --voice

Expected behavior:

    [Neo] Voice mode active. Waiting for 'Neo'.
    [Neo] Standby...

Say:

    Neo

Neo says:

    Yes, Neal?

Then say:

    Open VS Code

Neo will transcribe the command, execute the approved action, and speak the result.

### Wake-word note

This free implementation uses offline speech recognition as the wake-word detector rather than a dedicated keyword-spotting engine. It therefore uses more CPU than a specialized wake-word detector and can occasionally misrecognize similar-sounding speech. The advantage is that the entire wake process stays local and requires no paid service or cloud account.

## Text mode

    python main.py

Deterministic commands:

    help
    status
    open vscode
    open calculator
    open browser
    search python decorators
    remember editor = VS Code
    recall editor
    exit

## Local brain

Neo can optionally use an Ollama-compatible local API for natural-language fallback.

Set:

    llm_enabled = true
    ollama_model = your-installed-model

Neo does not execute arbitrary shell commands in V1. Future versions will add structured tool calling so the local model can select approved tools safely.

## Roadmap

Voice -> tool calling -> Windows control -> screen vision -> browser automation -> GitHub coding agent -> long-term memory -> multi-step autonomous workflows.
