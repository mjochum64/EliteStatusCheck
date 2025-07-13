"""
Pytest unit tests for log_module (API /api/v1/currentStarSystem)
"""

import pytest
from fastapi.testclient import TestClient
from elite_status.main import app
import json

client = TestClient(app)

def test_current_star_system_success(monkeypatch, tmp_path):
    # Simuliere ein gültiges Logfile mit FSDJump-Event
    log_entry = {"event": "FSDJump", "StarSystem": "Sol"}
    save_dir = tmp_path
    log_file = save_dir / "Journal.01.log"
    log_file.write_text(json.dumps(log_entry) + "\n")
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    response = client.get("/api/v1/currentStarSystem")
    assert response.status_code == 200
    assert response.json()["StarSystem"] == "Sol"

def test_current_star_system_no_log(monkeypatch, tmp_path):
    # Kein Logfile vorhanden
    monkeypatch.setenv("ELITE_STATUS_PATH", str(tmp_path))
    response = client.get("/api/v1/currentStarSystem")
    assert response.status_code == 200
    assert response.json()["StarSystem"] == "Unbekannt"
