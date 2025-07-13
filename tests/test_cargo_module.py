"""
Pytest unit tests for cargo_module (API /api/v1/cargo/)
"""

import pytest
from fastapi.testclient import TestClient
from elite_status.main import app
import json

client = TestClient(app)

def test_cargo_success(monkeypatch, tmp_path):
    # Simuliere ein gültiges Cargo.json im Testverzeichnis
    cargo_data = {
        "timestamp": "2025-07-13T12:34:56Z",
        "event": "Cargo",
        "Vessel": "Ship",
        "Count": 1,
        "Inventory": [
            {"Name": "bertrandite", "Name_Localised": "Bertrandit", "Count": 5, "Stolen": 0}
        ]
    }
    save_dir = tmp_path
    cargo_file = save_dir / "Cargo.json"
    cargo_file.write_text(json.dumps(cargo_data))
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    response = client.get("/api/v1/cargo/")
    assert response.status_code == 200
    assert response.json()["event"] == "Cargo"
    assert response.json()["Inventory"][0]["Name"] == "bertrandite"

def test_cargo_file_missing(monkeypatch, tmp_path):
    # Kein Cargo.json vorhanden
    monkeypatch.setenv("ELITE_STATUS_PATH", str(tmp_path))
    response = client.get("/api/v1/cargo/")
    assert response.status_code == 200
    assert "error" in response.json()

def test_cargo_file_empty(monkeypatch, tmp_path):
    # Leere Cargo.json
    save_dir = tmp_path
    cargo_file = save_dir / "Cargo.json"
    cargo_file.write_text("")
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    response = client.get("/api/v1/cargo/")
    assert response.status_code == 200
    assert "error" in response.json()
