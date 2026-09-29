from __future__ import annotations

import platform
import shutil
import subprocess
import webbrowser
from urllib.parse import quote_plus

APP_ALIASES = {
    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
    "chrome": "chrome",
    "google chrome": "chrome",
    "edge": "msedge",
    "microsoft edge": "msedge",
    "firefox": "firefox",
    "notepad": "notepad",
    "calculator": "calc",
}

def _run_command(command: list[str]) -> str:
    if shutil.which(command[0]) is None:
        return f"I could not find {command[0]} on this laptop."
    try:
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        return f"Failed to launch {command[0]}: {exc}"
    return f"Opened {command[0]}."

def open_application(app_name: str) -> str:
    key = app_name.strip().lower()

    if key in {"browser", "default browser", "web browser"}:
        try:
            webbrowser.open("about:blank")
        except Exception as exc:
            return f"Could not open the browser: {exc}"
        return "Opened the default browser."

    command = APP_ALIASES.get(key)
    if command is None:
        return (
            f"{app_name} is not in Neo's V1 application allow-list. "
            "Add its executable to APP_ALIASES after verifying it."
        )
    return _run_command([command])

def open_url(url: str) -> str:
    value = url.strip()
    if not value:
        return "Please provide a URL."
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    try:
        webbrowser.open(value)
    except Exception as exc:
        return f"Could not open the browser: {exc}"
    return f"Opened {value}."

def web_search(query: str) -> str:
    query = query.strip()
    if not query:
        return "Please provide something to search for."
    return open_url(f"https://www.google.com/search?q={quote_plus(query)}")

def laptop_status() -> str:
    return f"OS: {platform.system()} {platform.release()} | Architecture: {platform.machine()}"
