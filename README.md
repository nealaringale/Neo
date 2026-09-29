# Neo

Neo is a personal AI assistant for the laptop.

## V1 foundation

- deterministic command routing
- safe laptop actions
- local JSON memory
- optional local LLM brain through Ollama
- logging and configuration
- automated tests and GitHub Actions CI

## Run

python main.py

## Deterministic commands

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

Set these values in config/config.json or environment variables:

llm_enabled = true
ollama_model = your-installed-model

Neo does not execute arbitrary shell commands in V1.
Future versions will add structured tool calling so the local model can select approved tools safely.
