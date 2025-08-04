# Elite Status Check

## Beschreibung
Eine API zum Überwachen von Elite Dangerous Statusdaten.

## Verzeichnisstruktur
- **elite_status/**: Hauptanwendung (FastAPI-Backend)
  - main.py: FastAPI-Server und Anwendungseinsprungspunkt
  - status_fetcher.py: Statusüberwachung und Action-System
  - cargo_module.py: Frachtdaten-Management
  - log_module.py: Protokollierung und Sternsystem-Tracking
  - command_parser.py: Sprachbefehl-Verarbeitung
  - utils.py: Hilfsfunktionen (Pfaderkennung)
  - data_models.py: Pydantic-Datenmodelle
- **tests/**: Umfassende Unit-Tests für alle Module
- **docs/**: Dokumentation und API-Spezifikationen
  - INARA.txt: Inara API-Dokumentation für Marktdaten-Integration
  - Weitere technische Dokumentation
- **CLAUDE.md**: Entwicklerdokumentation für AI-Assistenten

## Verwendung
1. Installiere die erforderlichen Bibliotheken:

    `pip install -r requirements.txt`

2. Setze optional die Umgebungsvariable `ELITE_STATUS_PATH`, um das Savegame-Verzeichnis explizit anzugeben (empfohlen für Linux/Steam/Proton):

    `export ELITE_STATUS_PATH="/pfad/zum/Elite Dangerous"`

   Wird keine Variable gesetzt, wird der Pfad automatisch je nach Betriebssystem gesucht.

3. Starte die Anwendung mit:

    ```bash
    # Entwicklung mit Auto-Reload
    uvicorn elite_status.main:app --reload --host 0.0.0.0 --port 8000
    
    # Produktion mit Startskript (conda + .env)
    ./start_backend.sh
    
    # Direkter Modulaufruf
    python -m elite_status.main
    ```

## API-Endpunkte

### Statusabfrage
- `/api/v1/status` - Rohe Statusdaten aus Status.json
- `/api/v1/status/parsed` - Wichtige Statusflags als boolesche Werte
- `/api/v1/currentStarSystem` - Aktuelles Sternensystem

### Datenmanagement
- `/api/v1/cargo` - Frachtdaten aus Cargo.json

### Aktionssteuerung
- `/api/v1/action` - Spielaktionen ausführen (POST)
  - Beispiel: `{"action": "toggle_landing_gear"}`
- `/api/v1/command` - Sprachbefehle verarbeiten (POST)
  - Beispiel: `{"command": "Fahrwerk ausfahren"}`

### Zukünftige Erweiterungen
- `/api/v1/market` - Marktdaten über Inara API (geplant)
- `/api/v1/stations` - Stationssuche (geplant)

## Dateiüberwachung
Die Anwendung überwacht die JSON-Dateien "Status.json" und "Cargo.json" im Savegame-Verzeichnis.

**Hinweis:**
- Die Überwachung wird nur gestartet, wenn das Verzeichnis existiert. Andernfalls erscheint eine Warnung im Log.
- Das Verzeichnis wird automatisch erkannt oder kann über die Umgebungsvariable `ELITE_STATUS_PATH` gesetzt werden.
- Wird das Verzeichnis erst nachträglich angelegt (z.B. nach Spielstart), muss die Anwendung neu gestartet werden, um die Überwachung zu aktivieren.

Weitere Dateien können in zukünftigen Erweiterungen folgen.

## Kernmodule

### status_fetcher.py
- Real-time Dateiüberwachung mit watchdog
- Status-Caching und API-Endpunkte
- Action-System für Spielsteuerung
- Authentifizierung und Autorisierung

### cargo_module.py
- Frachtdaten-Management und API-Endpunkte
- Integration mit Elite Dangerous Cargo.json

### log_module.py
- Logging-System und protokollbezogene Endpunkte
- Sternensystem-Tracking

### command_parser.py
- Verarbeitung von Sprachbefehlen und Textkommandos
- Mapping deutscher Befehle zu Spielaktionen
- Erweiterbare Befehlsbibliothek

### utils.py
- Plattformübergreifende Elite Dangerous Pfaderkennung
- Hilfsfunktionen für Systemintegration

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
