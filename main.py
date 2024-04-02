import time
import json
import os
from threading import Thread
from fastapi import FastAPI
from status_module import router as status_router
from cargo_module import router as cargo_router
from log_module import router as log_router, get_current_star_system

app = FastAPI(title="EliteStatusCheck v0.1.0")

# Dateinamen, die überwacht werden sollen
files_to_watch = ["Status.json", "Cargo.json"]
# Pfad zum Verzeichnis, in dem die Dateien liegen
base_path = os.path.join(os.environ['USERPROFILE'], 'Saved Games', 'Frontier Developments', 'Elite Dangerous')

# Caching der Dateiinhalte
cached_data = {}

def read_and_update_files():
    for filename in files_to_watch:
        file_path = os.path.join(base_path, filename)
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                cached_data[filename] = data
        except Exception as e:
            print(f"Fehler beim Lesen von {filename}: {e}")

def start_file_watcher():
    while True:
        read_and_update_files()
        time.sleep(10)  # Überprüfe die Dateien alle 10 Sekunden

def start_watcher_thread():
    watcher_thread = Thread(target=start_file_watcher, daemon=True)
    watcher_thread.start()

@app.on_event("startup")
async def startup_event():
    start_watcher_thread()

# Module einbinden
app.include_router(status_router, prefix="/status")
app.include_router(cargo_router, prefix="/cargo")
app.include_router(log_router, prefix="/logs")

@app.get("/")
async def read_root():
    # Hole das aktuelle Sternensystem vom log_module
    current_star_system = await get_current_star_system()
    system_name = current_star_system.get("StarSystem", "Unbekanntes System")
    
    # Hole die Flags und Flags2 aus der Status.json, falls verfügbar
    status_data = cached_data.get("Status.json", {})
    flags = status_data.get("Flags", 0)
    flags2 = status_data.get("Flags2", 0)
    
    return {"System": system_name, "Flags": flags, "Flags2": flags2}