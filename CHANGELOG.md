# Changelog

This document records all notable changes to the Elite Dangerous Status Check project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-07-13

### Added
- Initial project setup.
- Created `PLANNING.md` to outline the project vision, architecture, and milestones.
- Created `TASK.md` to track project tasks.
- Created `GEMINI.md` with AI agent instructions tailored for this project.
- Created this `CHANGELOG.md` to document project changes.
- Transferred existing modules (`status_module.py`, `cargo_module.py`, `log_module.py`) from a previous project as a starting point.

## [13.07.2025]
- Migration der Funktionalität aus `main.py`, `status_module.py`, `log_module.py`, `cargo_module.py` in das neue Verzeichnis `elite_status/` abgeschlossen.
- Alte Module wurden archiviert (umbenannt zu `archived_*.py`).
- Neuer Root-Endpunkt `/` gibt API-Info, Version, Doku-Link und Hauptendpunkte als JSON zurück.
- Neuer /api/v1/cargo/ Endpunkt liefert aktuelle Frachtdaten aus Cargo.json oder eine Fehlermeldung.

## [1.0.0] - 2025-07-13
- Erstes stabiles Release: API-Endpunkte für Status, Cargo, aktuelles Sternensystem, Root-Info, plattformübergreifende Pfaderkennung, Tests und vollständige Dokumentation.

## [1.0.1] - 2025-07-13
### Geändert
- Abhängigkeit 'requests' zu requirements.txt hinzugefügt (Test-Fix)
- Testumgebung und Dokumentation aktualisiert
- Alle Tests laufen erfolgreich

## [1.0.2] - 2025-07-13
### Hinzugefügt
- Hilfsfunktion parse_status_flags(flags) zur Auswertung aller relevanten Statusbits
- Neuen API-Endpunkt /api/v1/status/parsed für die wichtigsten Statusflags als boolesche Felder
- Endpunkt /api/v1/action für Aktionen wie das Steuern des Fahrwerks (Landing Gear)

# CHANGELOG.md

## [1.1.0] - 2025-08-04

### Hinzugefügt
- **CLAUDE.md**: Umfassende Entwicklerdokumentation für AI-Assistenten mit Projektübersicht, Befehlen und Architektur
- **Inara API Integration (Vorbereitung)**: 
  - `docs/INARA.txt`: Dokumentation der Inara API für zukünftige Marktdaten-Integration
  - Grundlage für Markt- und Stationssuche basierend auf Pilotenposition
- **Serena MCP Server**: Konfiguration und Speicher-Dateien für erweiterte Entwicklungsunterstützung
- **Erweiterte Dokumentation**: Überarbeitete README.md mit besserer Struktur und API-Übersicht

### Entfernt
- Veraltete GitHub Workflows und Konfigurationsdateien
- `GEMINI.md` (ersetzt durch CLAUDE.md)

### Geplant
- `/api/v1/market` - Marktdaten über Inara API
- `/api/v1/stations` - Stationssuche für Waren und Schiffskomponenten

## 2025-07-19
- Erweiterung des Sprachbefehl-Mappings in `command_parser.py` um zahlreiche Elite Dangerous Funktionen (Fahrwerk, Lichter, Frachtluke, Hardpoints, Supercruise, FSD, Nachtmodus, Analysemodus, Statusabfragen etc.).
- Neuer Endpoint `/api/v1/command` im Backend zur Verarbeitung von Textbefehlen (Sprachsteuerung).
- Konzept und alle relevanten Markdown-Dokumente in den `docs/`-Ordner verschoben.
- Dokumentation und Konzept für sprachgesteuerte KI-Kommunikation im Frontend und Backend aktualisiert.