from fastapi import APIRouter
import os
import json
from elite_status.utils import get_elite_dangerous_save_path

router = APIRouter()

@router.get("/", summary="Gibt die aktuellen Frachtdaten (Cargo) zurück.")
def get_cargo():
    """
    Gibt die aktuellen Frachtdaten aus Cargo.json zurück.

    Returns:
        dict: Die aktuellen Frachtdaten oder eine leere Struktur.
    """
    cargo_dir = get_elite_dangerous_save_path()
    if not cargo_dir:
        return {"error": "Elite Dangerous Savegame-Verzeichnis nicht gefunden!"}
    cargo_file_path = os.path.join(cargo_dir, "Cargo.json")
    if not os.path.isfile(cargo_file_path):
        return {"error": "Cargo.json nicht gefunden!"}
    try:
        with open(cargo_file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content:
                return {"error": "Cargo.json ist leer."}
            data = json.loads(content)
            return data
    except Exception as e:
        return {"error": f"Fehler beim Lesen von Cargo.json: {e}"}
