from fastapi import FastAPI
from status_module import router as status_router
from cargo_module import router as cargo_router
from threading import Thread
import time
import json
import os

app = FastAPI(title="Mein FastAPI-Projekt")

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

@app.get("/")
async def read_root():
    return {"message": "Willkommen zu meiner FastAPI-Anwendung!"}
