#!/usr/bin/env python3
"""
Simple test server to test only the Inara API functionality.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elite_status.inara_router import router as inara_router
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Inara API Test Server",
    description="Test server for Inara API integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only the Inara router
app.include_router(inara_router, prefix="/api/v1")

if __name__ == "__main__":
    print("Starting Inara API Test Server...")
    print("Available endpoints:")
    print("- GET /api/v1/inara/health")
    print("- GET /api/v1/inara/system/{system_name}/factions")
    print("- GET /api/v1/inara/system/{system_name}/stations")
    print("- GET /api/v1/inara/commander/{commander_name}/profile")
    print("- GET /api/v1/inara/commander/{commander_name}/ships")
    print("- GET /api/v1/inara/commander/{commander_name}/current-ship")
    print("- GET /api/v1/inara/station/{station_id}/market")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)