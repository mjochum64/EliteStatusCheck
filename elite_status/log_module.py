from fastapi import APIRouter
import os
import json
from typing import Dict, Optional
from glob import glob
from elite_status.utils import get_elite_dangerous_save_path

router = APIRouter()

def get_latest_log_file(directory_path: str) -> Optional[str]:
    """
    Gibt den Pfad zur neuesten Logdatei im angegebenen Verzeichnis zurück.

    Args:
        directory_path (str): Pfad zum Log-Verzeichnis.

    Returns:
        Optional[str]: Pfad zur neuesten Logdatei oder None, falls keine gefunden wurde.
    """
    try:
        list_of_files = glob(os.path.join(directory_path, '*.log'))
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    except ValueError:
        return None

def read_latest_log_entry() -> Dict:
    """
    Liest den letzten relevanten Log-Eintrag (FSDJump oder Location) aus der neuesten Logdatei.

    Returns:
        Dict: Der letzte relevante Log-Eintrag oder ein leeres Dict.
    """
    directory_path = get_elite_dangerous_save_path()
    if not directory_path:
        print("Elite Dangerous Savegame-Verzeichnis nicht gefunden!")
        return {}
    latest_log_file = get_latest_log_file(directory_path)
    if latest_log_file:
        with open(latest_log_file, "r", encoding="utf-8") as file:
            for line in reversed(list(file)):
                try:
                    entry = json.loads(line)
                    if entry.get("event") == "FSDJump":
                        return entry
                    elif entry.get("event") == "Location":
                        return entry
                except json.JSONDecodeError:
                    continue
    return {}

@router.get("/currentStarSystem")
async def get_current_star_system():
    """
    API-Endpunkt: Gibt das aktuelle Sternensystem zurück.

    Returns:
        dict: Name des aktuellen Sternensystems.
    """
    latest_entry = read_latest_log_entry()
    return {"StarSystem": latest_entry.get("StarSystem", "Unbekannt")}
