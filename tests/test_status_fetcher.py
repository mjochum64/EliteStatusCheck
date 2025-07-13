"""
Pytest unit tests for status_fetcher module.
"""

import os
import pytest
from fastapi.testclient import TestClient
from elite_status.main import app
import json

client = TestClient(app)

def test_status_success(monkeypatch, tmp_path):
    # Simuliere ein gültiges Status.json im Testverzeichnis
    status_data = {"event": "Status", "Flags": 1234}
    save_dir = tmp_path
    status_file = save_dir / "Status.json"
    status_file.write_text(json.dumps(status_data))
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    response = client.get("/api/v1/status/")
    assert response.status_code == 200
    assert response.json()["event"] == "Status"

def test_status_file_missing(monkeypatch, tmp_path):
    # Kein Status.json vorhanden
    monkeypatch.setenv("ELITE_STATUS_PATH", str(tmp_path))
    response = client.get("/api/v1/status/")
    # Sollte leere Daten oder Fehler liefern
    assert response.status_code == 200
    # Akzeptiere leeres Dict oder Fehlerausgabe
    assert isinstance(response.json(), dict)
