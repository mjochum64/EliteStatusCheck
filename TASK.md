# Project Tasks: Elite Dangerous Status Check

## 1. Project Setup (13. Juli 2025)

- [x] Projektstruktur, .env, requirements.txt, erste Module und Doku angelegt.

## 2. Backend-API (FastAPI)

- [x] Status-API (Status.json, Flags, interpretierte Statuswerte)
- [x] Cargo-API (Cargo.json, Platzhalter)
- [x] Log-API (Logdateien, Debug-Logging)
- [x] Token-basierte Authentifizierung und CORS
- [x] Virtuelle Eingabe (uinput) für Aktionen (Fahrwerk, Lichter, etc.)
- [x] Endpunkt /api/v1/action für Button-Aktionen
- [x] Endpunkt /api/v1/command für Text-/Sprachbefehle (Mapping, KI-ready)
- [x] Modularisierung: command_parser.py für Mapping und spätere KI-Integration
- [x] .env-Handling mit python-dotenv
- [x] Startskript mit conda-Umgebung

## 3. Frontend (Flutter-App)

- [x] Grundfunktionalität: Statusanzeige, Fahrwerksteuerung per Button
- [x] Spracheingabe (on-device) und Senden an /api/v1/command
- [ ] Erweiterung: Rückmeldung anzeigen, weitere Aktionen/Status
- [ ] (Optional) WebSocket für Live-Status

## 4. Tests & Qualität

- [x] Pytest-Tests für API-Endpunkte und Mapping
- [ ] Tests für neue /command-Logik und Mapping
- [ ] Tests für Fehlerfälle und Security

## 5. Dokumentation

- [x] Alle Markdown-Dateien in docs/-Ordner verschoben
- [x] Konzept und API-Doku aktualisiert (Sprachsteuerung, Mapping, KI)
- [x] CHANGELOG.md gepflegt

## Discovered During Work

- Mapping und KI-Logik müssen regelmäßig erweitert werden (Synonyme, neue Aktionen)
- WebSocket-Integration für Statusupdates im Frontend prüfen

## 2025-07-19

- Sprachsteuerung, Mapping, neue Endpunkte und docs-Ordner umgesetzt.
