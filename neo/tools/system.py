from __future__ import annotations

import os
import platform
import shutil
import socket
import subprocess
import webbrowser
from pathlib import Path
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
    "task manager": "taskmgr",
}

URL_ALIASES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
}

SPECIAL_FOLDERS = {
    "desktop": Path.home() / "Desktop",
    "downloads": Path.home() / "Downloads",
    "documents": Path.home() / "Documents",
    "pictures": Path.home() / "Pictures",
    "music": Path.home() / "Music",
    "videos": Path.home() / "Videos",
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

    if key in URL_ALIASES:
        return open_url(URL_ALIASES[key])

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


def open_folder(folder_name: str) -> str:
    key = folder_name.strip().lower()
    folder = SPECIAL_FOLDERS.get(key)

    if folder is None:
        return (
            f"I can only open these folders right now: "
            f"{', '.join(SPECIAL_FOLDERS)}."
        )

    if not folder.exists():
        return f"The {key} folder does not exist at {folder}."

    try:
        os.startfile(str(folder))
    except OSError as exc:
        return f"Could not open {key}: {exc}"

    return f"Opened your {key} folder."


def create_folder(folder_name: str, location: str = "desktop") -> str:
    name = folder_name.strip()
    location_key = location.strip().lower()

    if not name:
        return "Please provide a folder name."

    base = SPECIAL_FOLDERS.get(location_key)
    if base is None:
        return (
            f"I can only create folders in: "
            f"{', '.join(SPECIAL_FOLDERS)}."
        )

    # Prevent path traversal and nested paths. Neo V1 creates one folder
    # directly inside an approved standard folder.
    if Path(name).name != name or name in {".", ".."}:
        return "Please provide only a folder name, not a path."

    target = base / name

    try:
        target.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        return f"A folder named {name} already exists in {location_key}."
    except OSError as exc:
        return f"Could not create the folder: {exc}"

    return f"Created {name} in your {location_key}."


def lock_laptop() -> str:
    if platform.system() != "Windows":
        return "Neo's V1 laptop lock action is currently implemented for Windows."

    try:
        result = subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return f"Could not lock the laptop: {exc}"

    if result.returncode != 0:
        return f"Windows did not lock the laptop (code {result.returncode})."

    return "Locking the laptop."


def laptop_status() -> str:
    return f"OS: {platform.system()} {platform.release()} | Architecture: {platform.machine()}"


def network_status() -> str:
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except OSError:
        return "I could not determine the local network address."

    return f"Hostname: {hostname} | Local IP: {local_ip}"
