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
- `/status`: Gibt den aktuellen Status zurück
- `/cargo`: Zeigt die Frachtdaten an (noch nicht implementiert!)
- `/log/currentStarSystem`: Gibt das aktuelle Sternensystem zurück

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
Die implementierten Schnittstellen können über die URL `/docs` (Swagger UI) eingesehen werden.

## Aktuelle Informationen
- **Entwickler:** [Martin Jochum]
- **Version:** 0.0.1
- **Letztes Update:** 13.07.2025
- **Lizenz:** [MIT]
- **Kontakt:** [mjochum64@gmail.com]
