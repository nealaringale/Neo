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

Neo has a wake-word voice loop.

1. Neo starts in silent standby.
2. A local Porcupine model waits for the custom wake word Neo.
3. When Neo is detected, Neo says: "Yes, Neal?"
4. Neo listens for your command.
5. Vosk transcribes the command locally.
6. Neo runs the approved tool router.
7. Neo speaks the response using the selected/female TTS voice.

Run:

    python main.py --voice

## Voice setup on Windows

Install Python 3.9+ and then:

    python -m pip install -r requirements.txt

### 1. Wake word: Neo

Create a custom Porcupine wake-word model for the phrase Neo using the Picovoice Console.

Select Windows as the target platform and download the generated .ppn file.

Place it here:

    models/neo_windows.ppn

Set your Picovoice AccessKey in the current PowerShell session:

    $env:PICOVOICE_ACCESS_KEY="YOUR_ACCESS_KEY"

Do not commit the AccessKey to GitHub.

### 2. Offline speech recognition

Download the Vosk model named:

    vosk-model-small-en-in-0.4

Extract it here:

    models/vosk-model-small-en-in-0.4

This repository deliberately does not contain the model because it is a separate local model asset.

### 3. Female voice

Neo uses Windows SAPI5 through pyttsx3.

It automatically prefers common installed female voice names such as Zira, Jenny, Aria, Hazel, or Samantha.

To explicitly select an installed voice:

    $env:NEO_TTS_VOICE="Zira"

You can adjust:

    $env:NEO_TTS_RATE="175"
    $env:NEO_TTS_VOLUME="1.0"

### 4. Microphone

Neo uses the default microphone by default.

To select another recording device, set:

    $env:NEO_AUDIO_DEVICE="2"

Use -1 for the Windows default device.

### Start Neo

    python main.py --voice

Expected flow:

    Neo voice mode is active.
    [Neo] Listening for wake word...

Say:

    Neo

Neo replies:

    Yes, Neal?

Then say:

    open vscode

Neo executes the existing approved command and speaks the response.

## Text mode

Run without the voice flag:

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
