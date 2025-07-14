import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import pytest
from fastapi.testclient import TestClient
from elite_status.main import app
from elite_status.status_fetcher import update_status_data

client = TestClient(app)

def test_action_toggle_landing_gear(monkeypatch, tmp_path):
    # Simuliere Status: Fahrwerk eingefahren, nicht angedockt, nicht gelandet
    flags = 0  # alle False
    status_data = {"event": "Status", "Flags": flags}
    save_dir = tmp_path
    status_file = save_dir / "Status.json"
    status_file.write_text(json.dumps(status_data))
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    update_status_data()
    # Patch subprocess.run, damit kein echter Tastendruck erfolgt
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: None)
    response = client.post("/api/v1/status/action", json={"action": "toggle_landing_gear"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "new_status" in response.json()

def test_action_landing_gear_blocked(monkeypatch, tmp_path):
    # Simuliere Status: angedockt
    flags = 1  # Bit 0 = docked
    status_data = {"event": "Status", "Flags": flags}
    save_dir = tmp_path
    status_file = save_dir / "Status.json"
    status_file.write_text(json.dumps(status_data))
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    update_status_data()
    response = client.post("/api/v1/status/action", json={"action": "toggle_landing_gear"})
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Fahrwerk kann am Boden nicht bedient werden" in response.json()["reason"]

def test_action_landing_gear_idempotent(monkeypatch, tmp_path):
    # Simuliere Status: Fahrwerk bereits ausgefahren
    flags = (1 << 2)  # Bit 2 = landing_gear_down
    status_data = {"event": "Status", "Flags": flags}
    save_dir = tmp_path
    status_file = save_dir / "Status.json"
    status_file.write_text(json.dumps(status_data))
    monkeypatch.setenv("ELITE_STATUS_PATH", str(save_dir))
    update_status_data()
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: None)
    response = client.post("/api/v1/status/action", json={"action": "set_landing_gear", "value": True})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "Fahrwerk bereits im gewünschten Zustand" in response.json()["info"]
