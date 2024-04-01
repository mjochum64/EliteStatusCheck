from fastapi import APIRouter
import os
import json
from typing import Dict, Optional
from glob import glob

router = APIRouter()

def get_latest_log_file(directory_path: str) -> Optional[str]:
    try:
        # Liste alle .log Dateien im Verzeichnis auf und sortiere sie nach Erstellungszeit
        list_of_files = glob(os.path.join(directory_path, '*.log'))
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    except ValueError:
        # Keine Dateien gefunden
        return None

def read_latest_log_entry() -> Dict:
    directory_path = os.path.join(os.environ['USERPROFILE'], 'Saved Games', 'Frontier Developments', 'Elite Dangerous')
    latest_log_file = get_latest_log_file(directory_path)
    if latest_log_file:
        # Lese die Datei rückwärts, um den letzten relevanten Eintrag zu finden
        with open(latest_log_file, "r") as file:
            for line in reversed(list(file)):
                try:
                    entry = json.loads(line)
                    # Prüfe, ob der Eintrag das gesuchte Event enthält
                    if entry.get("event") == "SupercruiseExit":
                        return entry
                except json.JSONDecodeError:
                    continue
    return {}

@router.get("/currentStarSystem")
async def get_current_star_system():
    latest_entry = read_latest_log_entry()
    return {"StarSystem": latest_entry.get("StarSystem", "Unbekannt")}
