"""
Module for fetching Elite Dangerous status from APIs.
"""

from fastapi import APIRouter
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

router = APIRouter()

# Globale Variable für den Cache
default_cache = {}


def get_status_data() -> dict:
    """
    Gibt die gecachten Statusdaten zurück.

    Returns:
        dict: Die aktuellen Statusdaten aus dem Cache.
    """
    return default_cache.get("status_data", {})


def update_status_data() -> None:
    """
    Aktualisiert die Daten im Cache.
    """
    status_file_path = os.path.join(
        os.environ.get("USERPROFILE", ""),
        "Saved Games",
        "Frontier Developments",
        "Elite Dangerous",
        "Status.json",
    )
    global default_cache
    try:
        with open(status_file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content:
                print("Die Datei ist leer. Überspringe das Update.")
                return
            data = json.loads(content)
            default_cache["status_data"] = data
    except json.JSONDecodeError as e:
        print(f"Fehler beim Parsen der JSON-Daten: {e}")
    except OSError as e:
        print(f"Dateifehler beim Aktualisieren des Caches: {e}")


def check_flag(flags: int, bit: int) -> bool:
    """
    Überprüft, ob ein spezifisches Bit gesetzt ist.

    Args:
        flags (int): Die Flags als Integer.
        bit (int): Das zu prüfende Bit.

    Returns:
        bool: True, wenn das Bit gesetzt ist, sonst False.
    """
    return (flags & (1 << bit)) != 0


class StatusFileEventHandler(FileSystemEventHandler):
    """
    Reagiert auf Änderungen der Statusdatei und aktualisiert den Cache.
    """

    def on_modified(self, event):
        if event.src_path.endswith("Status.json"):
            print("Status.json wurde geändert. Aktualisiere den Cache.")
            update_status_data()


def start_watching() -> None:
    """
    Startet die Überwachung der Statusdatei.
    """
    path_to_watch = os.path.dirname(
        os.path.join(
            os.environ.get("USERPROFILE", ""),
            "Saved Games",
            "Frontier Developments",
            "Elite Dangerous",
            "Status.json",
        )
    )
    event_handler = StatusFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()


# Starte den Watchdog Observer in einem separaten Thread
thread = threading.Thread(target=start_watching, daemon=True)
thread.start()

# Initialisiere den Cache beim Start des Moduls
update_status_data()
