"""
FastAPI Applikation zur Überwachung von Elite Dangerous Statusdaten
"""

import json
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from elite_status.status_fetcher import router as status_router
from elite_status.cargo_module import router as cargo_router
from elite_status.log_module import router as log_router
from elite_status.inara_router import router as inara_router

app = FastAPI(
    title="Elite Dangerous Status Check",
    version="1.0.0",
    description="Eine API zum Überwachen von Elite Dangerous Statusdaten",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
)

API_PREFIX = "/api/v1"

app.include_router(status_router, prefix=f"{API_PREFIX}/status")
app.include_router(cargo_router, prefix=f"{API_PREFIX}/cargo")
app.include_router(log_router, prefix=f"{API_PREFIX}")
app.include_router(inara_router, prefix=f"{API_PREFIX}")

# CORS für das lokale Netzwerk erlauben
origins = [
    "http://localhost",
    "http://127.0.0.1",
    # Beispiel: alle Geräte im 192.168.x.x Netz
    "http://192.168.0.0/16",
    "http://10.0.0.0/8",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für Entwicklung, später gezielt einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    """
    Root-Endpunkt: Gibt API-Info und Links zurück.
    """
    return {
        "name": "Elite Dangerous Status Check API",
        "version": "1.0.0",
        "description": "API zur Überwachung von Elite Dangerous Statusdaten.",
        "docs": "/api/v1/docs",
        "endpoints": [
            "/api/v1/status/",
            "/api/v1/cargo/",
            "/api/v1/currentStarSystem",
            "/api/v1/inara/"
        ]
    }

# Optional: Starte die App mit Uvicorn, falls als Skript ausgeführt
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("elite_status.main:app", host="0.0.0.0", port=8000, reload=True)
