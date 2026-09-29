from __future__ import annotations

import json
import queue
import time
from array import array
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel


def list_microphones() -> None:
    devices = sd.query_devices()
    print("\nNeo microphone devices:\n")
    for index, device in enumerate(devices):
        if device["max_input_channels"] > 0:
            marker = "  <-- DEFAULT INPUT" if index == sd.default.device[0] else ""
            print(
                f"[{index}] {device['name']} | "
                f"channels={device['max_input_channels']} | "
                f"rate={int(device['default_samplerate'])}{marker}"
            )


def microphone_test(model_path: Path, device_index: int = -1, seconds: float = 6.0) -> None:
    if not model_path.exists():
        raise FileNotFoundError(f"Vosk model not found: {model_path}")

    SetLogLevel(-1)
    model = Model(str(model_path))

    device = None if device_index < 0 else device_index
    info = sd.query_devices(device, "input")
    sample_rate = int(info["default_samplerate"])

    print(f"\nMicrophone: {info['name']}")
    print(f"Sample rate: {sample_rate}")
    print(f"Listening for {seconds:.0f} seconds...")
    print("Say:  hello Neo, this is a microphone test")
    print()

    audio_queue: queue.Queue[bytes] = queue.Queue(maxsize=50)

    def callback(indata, frames, callback_time, status) -> None:
        del frames, callback_time, status
        try:
            audio_queue.put_nowait(bytes(indata))
        except queue.Full:
            pass

    recognizer = KaldiRecognizer(model, sample_rate)
    started = time.monotonic()
    peak = 0

    with sd.RawInputStream(
        samplerate=sample_rate,
        blocksize=2000,
        device=device,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while time.monotonic() - started < seconds:
            try:
                data = audio_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            samples = array("h")
            samples.frombytes(data)
            if samples:
                current_peak = max(abs(x) for x in samples)
                peak = max(peak, current_peak)
                bars = min(30, int(current_peak / 1100))
                print("\rMic level: " + "█" * bars + " " * (30 - bars), end="", flush=True)

            recognizer.AcceptWaveform(data)

    print(f"\nPeak level: {peak}")
    result = json.loads(recognizer.FinalResult())
    text = result.get("text", "").strip()

    if text:
        print(f"Vosk heard: {text}")
    else:
        print("Vosk heard: <nothing>")

    if peak < 100:
        print("\nWARNING: Almost no microphone signal reached Python.")
        print("Check Windows microphone permission, selected input device, and microphone mute.")
    elif not text:
        print("\nThe microphone is working, but Vosk did not recognize speech.")
        print("Try speaking closer to the microphone or selecting a different input device.")
    else:
        print("\nMicrophone + Vosk are working.")
