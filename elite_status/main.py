"""
FastAPI Applikation zur Überwachung von Elite Dangerous Statusdaten
"""

import json
import os
from fastapi import FastAPI
from elite_status.status_fetcher import router as status_router
from elite_status.cargo_module import router as cargo_router
from elite_status.log_module import router as log_router

app = FastAPI(
    title="Elite Dangerous Status Check",
    version="0.0.1",
    description="Eine API zum Überwachen von Elite Dangerous Statusdaten",
)

# Beispiel für das Einbinden der Router
app.include_router(status_router, prefix="/status")
app.include_router(cargo_router, prefix="/cargo")
app.include_router(log_router, prefix="/log")

# Optional: Starte die App mit Uvicorn, falls als Skript ausgeführt
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("elite_status.main:app", host="0.0.0.0", port=8000, reload=True)
