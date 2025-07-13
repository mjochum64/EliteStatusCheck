"""
FastAPI Applikation zur Überwachung von Elite Dangerous Statusdaten
"""

import json
import os
from fastapi import FastAPI, APIRouter
from elite_status.status_fetcher import router as status_router
from elite_status.cargo_module import router as cargo_router
from elite_status.log_module import router as log_router

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
            "/api/v1/currentStarSystem"
        ]
    }

# Optional: Starte die App mit Uvicorn, falls als Skript ausgeführt
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("elite_status.main:app", host="0.0.0.0", port=8000, reload=True)
