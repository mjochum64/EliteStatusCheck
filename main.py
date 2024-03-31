import os
import json
from fastapi import FastAPI
from typing import Dict
import time
from threading import Thread

app = FastAPI()

# Pfad zur Status.json basierend auf dem Windows-Benutzerprofil
def get_status_file_path():
    base_path = os.path.join(os.environ['USERPROFILE'], 'Saved Games', 'Frontier Developments', 'Elite Dangerous')
    return os.path.join(base_path, 'Status.json')

# Überprüfe, ob ein spezifisches Bit gesetzt ist
def check_flag(flags, bit):
    return (flags & (1 << bit)) != 0

# Globale Variable, um den Status zu speichern
status_cache: Dict[str, any] = {}

# Lese die Status-Datei und speichere die Werte im Cache
def read_and_update_status():
    status_file_path = get_status_file_path()
    try:
        with open(status_file_path, "r") as file:
            data = json.load(file)
            status_cache.update(data)
    except FileNotFoundError:
        print(f"Die Datei {status_file_path} wurde nicht gefunden.")
    except json.JSONDecodeError:
        print("Fehler beim Parsen der JSON-Datei.")

# Polling-Funktion, die die Datei regelmäßig überprüft
def start_file_watcher():
    while True:
        read_and_update_status()
        time.sleep(5)  # Polling-Intervall: 5 Sekunden

# Starte den File-Watcher in einem separaten Thread
def start_watcher_thread():
    watcher_thread = Thread(target=start_file_watcher, daemon=True)
    watcher_thread.start()

# FastAPI Endpunkte
@app.get("/")
async def read_root():
    return {"message": "Status-API"}

@app.get("/status")
async def get_status():
    return status_cache

@app.get("/isDocked")
async def is_docked():
    flags = status_cache.get("Flags", 0)
    return {"isDocked": check_flag(flags, 0)}

# Starte den File-Watcher, wenn die Anwendung startet
@app.on_event("startup")
async def on_startup():
    start_watcher_thread()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
