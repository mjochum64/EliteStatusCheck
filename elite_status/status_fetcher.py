"""
Module for fetching Elite Dangerous status from APIs.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from elite_status.utils import get_elite_dangerous_save_path
import subprocess
import pathlib
import uinput

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
    status_dir = get_elite_dangerous_save_path()
    if not status_dir:
        print("Elite Dangerous Savegame-Verzeichnis nicht gefunden!")
        return
    status_file_path = os.path.join(status_dir, "Status.json")
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


def parse_status_flags(flags: int = 0) -> dict:
    """
    Interpretiert die Status-Flags und gibt ein Mapping der wichtigsten Stati zurück.
    Gibt für alle bekannten Flags immer einen Wert zurück (Default: False).

    Args:
        flags (int): Status-Flags als Integer.

    Returns:
        dict: Mapping von Statusnamen auf bool.
    """
    flag_map = {
        "docked": 0,
        "landed": 1,
        "landing_gear_down": 2,
        "shields_up": 3,
        "supercruise": 4,
        "flight_assist_off": 5,
        "hardpoints_deployed": 6,
        "in_wing": 7,
        "lights_on": 8,
        "cargo_scoop_deployed": 9,
        "silent_running": 10,
        "scooping_fuel": 11,
        "srv_handbrake": 12,
        "srv_turret_view": 13,
        "srv_turret_retracted": 14,
        "srv_drive_assist": 15,
        "fsd_mass_locked": 16,
        "fsd_charging": 17,
        "fsd_cooldown": 18,
        "low_fuel": 19,
        "over_heating": 20,
        "has_lat_long": 21,
        "is_in_danger": 22,
        "being_interdicted": 23,
        "in_main_ship": 24,
        "in_fighter": 25,
        "in_srv": 26,
        "hud_analysis_mode": 27,
        "night_vision": 28,
        "altitude_from_average_radius": 29,
        "fsd_jump": 30,
        "srv_high_beam": 31,
    }
    return {name: check_flag(flags, bit) for name, bit in flag_map.items()}


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
    Startet die Überwachung der Statusdatei, falls das Verzeichnis existiert.
    """
    path_to_watch = os.path.dirname(os.path.join(get_elite_dangerous_save_path() or '', 'Status.json'))
    if not os.path.isdir(path_to_watch):
        print(f"[WARN] Überwachungs-Verzeichnis nicht gefunden: {path_to_watch}. Watchdog wird nicht gestartet.")
        return
    event_handler = StatusFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()


# Starte den Watchdog Observer in einem separaten Thread
thread = threading.Thread(target=start_watching, daemon=True)
thread.start()

# Initialisiere den Cache beim Start des Moduls
update_status_data()


@router.get("/", summary="Gibt den aktuellen Elite Dangerous Status zurück.")
def get_status():
    """
    Gibt die aktuellen Statusdaten aus dem Cache zurück.

    Returns:
        dict: Die aktuellen Statusdaten.
    """
    return get_status_data()


@router.get("/parsed", summary="Gibt den interpretierten Elite Dangerous Status zurück.")
def get_parsed_status():
    """
    Gibt die wichtigsten Statusflags als boolesche Felder zurück.

    Returns:
        dict: Mapping der wichtigsten Statusflags.
    """
    status = get_status_data()
    flags = status.get("Flags", 0)
    return parse_status_flags(flags)


class ActionRequest(BaseModel):
    action: str
    value: Optional[bool] = None


def load_keymap() -> dict:
    """
    Lädt die Tastenbelegung aus keymap.json.
    Returns:
        dict: Mapping von Action-Name auf Liste von Tasten/Modifikatoren.
    """
    keymap_path = pathlib.Path(__file__).parent / "keymap.json"
    if keymap_path.exists():
        with open(keymap_path, "r", encoding="utf-8") as f:
            import json
            return json.load(f)
    return {}


keymap = load_keymap()


# Mapping von Strings/Keymap zu uinput-Keycodes
UINPUT_KEY_MAP = {
    "l": uinput.KEY_L,
    "a": uinput.KEY_A,
    "space": uinput.KEY_SPACE,
    "left_shift": uinput.KEY_LEFTSHIFT,
    "right_shift": uinput.KEY_RIGHTSHIFT,
    "ctrl": uinput.KEY_LEFTCTRL,
    "left_ctrl": uinput.KEY_LEFTCTRL,
    "right_ctrl": uinput.KEY_RIGHTCTRL,
    "alt": uinput.KEY_LEFTALT,
    "left_alt": uinput.KEY_LEFTALT,
    "right_alt": uinput.KEY_RIGHTALT,
    "mouse1": uinput.BTN_LEFT,
    # ...weitere Keys nach Bedarf...
}

# Initialisiere das virtuelle Eingabegerät mit allen genutzten Keys
UINPUT_DEVICE = uinput.Device(list(set(UINPUT_KEY_MAP.values())))


@router.post("/action", summary="Führt eine Aktion im Spiel aus (z.B. Fahrwerk steuern)")
def perform_action(request: ActionRequest):
    """
    Führt eine Aktion wie das Aus- oder Einfahren des Fahrwerks aus.
    Prüft vorher den Status und gibt nach Ausführung den neuen Status zurück.
    """
    # Aktuellen Status holen
    status = get_status_data()
    flags = status.get("Flags", 0)
    parsed = parse_status_flags(flags)

    # Beispiel: Landing Gear steuern
    if request.action in ["toggle_landing_gear", "set_landing_gear"]:
        # Status-Prüfung: Fahrwerk kann nicht bedient werden, wenn angedockt oder gelandet
        if parsed["docked"] or parsed["landed"]:
            return {"success": False, "reason": "Fahrwerk kann am Boden nicht bedient werden.", "new_status": parsed}
        # Zielzustand bestimmen
        if request.action == "set_landing_gear" and request.value is not None:
            if request.value == parsed["landing_gear_down"]:
                return {"success": True, "info": "Fahrwerk bereits im gewünschten Zustand.", "new_status": parsed}
        # Systembefehl ausführen (jetzt konfigurierbar mit Modifiers)
        try:
            keys = keymap.get(request.action, ["l"])
            print(f"[DEBUG] Aktion: {request.action}, Keys aus keymap: {keys}")
            keycodes = [UINPUT_KEY_MAP[k] for k in keys if k in UINPUT_KEY_MAP]
            print(f"[DEBUG] Zu sendende uinput-Keycodes: {keycodes}")
            if not keycodes:
                print(f"[ERROR] Keine gültigen Keycodes für Aktion {request.action} gefunden.")
                raise Exception(f"Keine gültigen Keycodes für Aktion {request.action} gefunden.")
            if len(keycodes) > 1:
                print(f"[DEBUG] Sende Kombi: {keycodes}")
                UINPUT_DEVICE.emit_combo(keycodes)
            else:
                print(f"[DEBUG] Sende Einzel-Key: {keycodes[0]}")
                UINPUT_DEVICE.emit_click(keycodes[0])
            print("[DEBUG] Virtuelle Eingabe ausgeführt")
        except Exception as e:
            print(f"[ERROR] Virtuelle Eingabe fehlgeschlagen: {e}")
            raise HTTPException(status_code=500, detail=f"Virtuelle Eingabe fehlgeschlagen: {e}")
        # Nach Ausführung Status aktualisieren
        update_status_data()
        new_flags = get_status_data().get("Flags", 0)
        new_parsed = parse_status_flags(new_flags)
        return {"success": True, "new_status": new_parsed}
    else:
        raise HTTPException(status_code=400, detail="Unbekannte oder nicht unterstützte Aktion.")
