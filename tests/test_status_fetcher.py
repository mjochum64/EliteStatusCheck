"""
Pytest unit tests for status_fetcher module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from elite_status.status_fetcher import update_status_data

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

def test_parsed_status_flags(monkeypatch, tmp_path):
    """
    Testet den /api/v1/status/parsed Endpunkt für verschiedene Statusbits.
    """
    # Beispiel: Fahrwerk ausgefahren (Bit 2), Lichter an (Bit 8), Docked (Bit 0)
    flags = (1 << 2) | (1 << 8) | (1 << 0)
    status_data = {"event": "Status", "Flags": flags}
    save_dir = tmp_path
    status_file = save_dir / "Status.json"
    status_file.write_text(json.dumps(status_data))
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    update_status_data()
    response = client.get("/api/v1/status/parsed")
    assert response.status_code == 200
    parsed = response.json()
    assert parsed["docked"] is True
    assert parsed["landing_gear_down"] is True
    assert parsed["lights_on"] is True
    assert parsed["landed"] is False
    assert parsed["shields_up"] is False

# Edge Case: Keine Flags gesetzt

def test_parsed_status_flags_none(monkeypatch, tmp_path):
    status_data = {"event": "Status", "Flags": 0}
    save_dir = tmp_path
    status_file = save_dir / "Status.json"
    status_file.write_text(json.dumps(status_data))
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    update_status_data()
    response = client.get("/api/v1/status/parsed")
    assert response.status_code == 200
    parsed = response.json()
    # Alle Flags sollten False sein
    assert all(v is False for v in parsed.values())

# Fehlerfall: Status.json fehlt

def test_parsed_status_file_missing(monkeypatch, tmp_path):
    monkeypatch.setenv("ELITE_STATUS_PATH", str(tmp_path))
    update_status_data()
    response = client.get("/api/v1/status/parsed")
    assert response.status_code == 200
    parsed = response.json()
    # Alle Flags sollten False sein (Default)
    assert all(v is False for v in parsed.values())
