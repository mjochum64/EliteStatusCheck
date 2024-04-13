import json
import os
import asyncio
import uvicorn
from fastapi import FastAPI
from status_module import router as status_router
from cargo_module import router as cargo_router
from log_module import router as log_router, get_current_star_system

app = FastAPI(
    title="Elite Status Check",
    version="0.0.1",
    description="Eine API zum Überwachen von Elite Dangerous Statusdaten",
)

# Dateinamen, die überwacht werden sollen
files_to_watch = ["Status.json", "Cargo.json"]

# Pfad zum Verzeichnis, in dem die Dateien liegen
base_path = os.path.join(
    os.environ["USERPROFILE"], "Saved Games", "Frontier Developments", "Elite Dangerous"
)

# Caching der Dateiinhalte
cached_data = {}

def read_and_update_files():
    """
    Reads and updates files based on the content of files_to_watch.
    """
    for filename in files_to_watch:
        file_path = os.path.join(base_path, filename)
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                cached_data[filename] = data
        except Exception as e:
            print(f"Fehler beim Lesen von {filename}: {e}")

async def start_file_watcher():
    """
    Start the file watcher that reads and updates specified files every 10 seconds using asyncio.
    """
    while True:
        read_and_update_files()
        await asyncio.sleep(10)

async def app_lifespan(app):
    """
    Asynchronous generator to handle startup and shutdown events.
    """
    try:
        await asyncio.create_task(start_file_watcher())
        yield
    finally:
        print("Cleanup actions here")

app.router.lifespan = app_lifespan

# Module einbinden
app.include_router(status_router, prefix="/status")
app.include_router(cargo_router, prefix="/cargo")
app.include_router(log_router, prefix="/logs")

@app.get("/")
async def read_root():
    """
    A function to retrieve the current star system, flags, and flags2 from status data.
    """
    # Hole das aktuelle Sternensystem vom log_module
    current_star_system = await get_current_star_system()
    system_name = current_star_system.get("StarSystem", "Unbekanntes System")

    # Hole die Flags und Flags2 aus der Status.json, falls verfügbar
    status_data = cached_data.get("Status.json", {})
    flags = status_data.get("Flags", 0)
    flags2 = status_data.get("Flags2", 0)

    return {"System": system_name, "Flags": flags, "Flags2": flags2}

# Start the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
