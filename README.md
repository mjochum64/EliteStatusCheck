# Elite Status Check

## Beschreibung
Eine API zum Überwachen von Elite Dangerous Statusdaten.

## Verzeichnisstruktur
- elite_status/main.py: Hauptdatei der Anwendung (FastAPI-Server)
- elite_status/status_fetcher.py: Modul zur Überwachung und Verarbeitung der Statusdateien
- elite_status/cargo_module.py: Modul zur Verwaltung von Frachtdaten
- elite_status/log_module.py: Modul zur Protokollierung
- tests/: Unit-Tests für die Module
- archived_*.py: Archivierte Altdateien (nur zu Referenzzwecken)

## Verwendung
1. Installiere die erforderlichen Bibliotheken:

    `pip install -r requirements.txt`

2. Setze optional die Umgebungsvariable `ELITE_STATUS_PATH`, um das Savegame-Verzeichnis explizit anzugeben (empfohlen für Linux/Steam/Proton):

    `export ELITE_STATUS_PATH="/pfad/zum/Elite Dangerous"`

   Wird keine Variable gesetzt, wird der Pfad automatisch je nach Betriebssystem gesucht.

3. Starte die Anwendung mit:

    `python -m elite_status.main`

    oder

    `uvicorn elite_status.main:app --reload --host 0.0.0.0 --port 8000`

## Aktuell gültige Endpunkte
- `/api/v1/status`: Gibt den aktuellen Status zurück
- `/api/v1/cargo`: Zeigt die Frachtdaten an (noch nicht implementiert!)
- `/api/v1/currentStarSystem`: Gibt das aktuelle Sternensystem zurück
- `/api/v1/status/parsed`: Gibt die wichtigsten Statusflags als boolesche Felder zurück
- `/api/v1/action`: Führt Aktionen wie das Steuern des Fahrwerks aus (POST, z.B. `{ "action": "toggle_landing_gear" }`)

## Dateiüberwachung
Die Anwendung überwacht die JSON-Dateien "Status.json" und "Cargo.json" im Savegame-Verzeichnis.

**Hinweis:**
- Die Überwachung wird nur gestartet, wenn das Verzeichnis existiert. Andernfalls erscheint eine Warnung im Log.
- Das Verzeichnis wird automatisch erkannt oder kann über die Umgebungsvariable `ELITE_STATUS_PATH` gesetzt werden.
- Wird das Verzeichnis erst nachträglich angelegt (z.B. nach Spielstart), muss die Anwendung neu gestartet werden, um die Überwachung zu aktivieren.

Weitere Dateien können in zukünftigen Erweiterungen folgen.

## Module
### status_fetcher.py
- Enthält Funktionen zur Verarbeitung und Überwachung von Statusdateien

### cargo_module.py
- Bietet Endpunkte zur Verwaltung von Frachtdaten **(noch nicht implementiert!)**

### log_module.py
- Implementiert Protokollierungsfunktionen und Endpunkte

## API-Dokumentation
Die implementierten Schnittstellen können über die URL `/api/v1/docs` (Swagger UI) eingesehen werden.

## Aktuelle Informationen
- **Entwickler:** [Martin Jochum]
- **Version:** 1.0.1
- **Letztes Update:** 13.07.2025
- **Lizenz:** [MIT]
- **Kontakt:** [mjochum64@gmail.com]

## 4. Testing

- Unit-Tests für die wichtigsten API-Endpunkte (`status_fetcher`, `cargo_module`, `log_module`) mit Pytest und FastAPI TestClient implementiert.
- Tests decken Erfolgs- und Fehlerfälle ab (Datei vorhanden, fehlt, leer etc.).
- Tests können mit folgendem Befehl ausgeführt werden:

      pytest tests/

- Weitere Tests für Datenmodelle und Transformationen empfohlen.

**Achtung (Wayland):**
Virtuelle Eingabegeräte (z.B. python-uinput) werden unter Wayland aus Sicherheitsgründen nicht an laufende Anwendungen oder Spiele durchgereicht. Für systemweite Eingaben und Gaming/Automation ist X11 weiterhin die zuverlässigere Wahl. Unter Wayland funktionieren virtuelle Tastaturen meist nur in evtest, aber nicht in normalen Programmen oder Spielen.

---

## Architektur-Empfehlung: Trennung von Backend (Game-PC) und Frontend (Remote-Gerät)

**Konzept:**
- Das Backend läuft lokal auf dem Spiele-PC und ist für die systemnahe Eingabe (z.B. uinput, xdotool) zuständig.
- Die Frontend-App (z.B. Flutter-App) läuft auf einem separaten Gerät (Smartphone, Tablet, etc.) und kommuniziert über das Netzwerk (WLAN/LAN) mit dem Backend.
- Das Spiel bleibt immer im Fokus und verliert keine Eingabeberechtigung.
- Die Steuerung erfolgt komfortabel und flexibel über das externe Gerät.

**Vorteile:**
- Keine Fokus-Probleme oder Konflikte mit Fenstermanagement (X11/Wayland).
- Systemnahe Eingaben funktionieren zuverlässig, da das Backend direkt auf dem Spiele-PC läuft.
- Mehr Flexibilität für den Nutzer (z.B. Touch, Sprache, mehrere Geräte).
- Bessere Sicherheit: Das Backend kann API-Authentifizierung und Zugriffskontrolle implementieren.

**Hinweise:**
- Stelle sicher, dass das Backend im lokalen Netzwerk erreichbar ist (Firewall, Portfreigabe).
- Aktiviere Authentifizierung für die API, um Missbrauch zu verhindern.
- Dokumentiere die Netzwerk-Architektur und die Vorteile für Nutzer und Entwickler.

---
