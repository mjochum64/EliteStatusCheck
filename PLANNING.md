# Project Plan: Elite Dangerous Status Check

## 1. Project Vision & Goals

Ziel ist eine modulare, sichere API-Backend-Lösung (FastAPI, Python), die Status und Aktionen für Elite Dangerous bereitstellt und von einer mobilen Flutter-App (iOS/Android) ferngesteuert werden kann. Die Sprachsteuerung erfolgt on-device im Frontend, die Interpretation und Ausführung der Befehle übernimmt das Backend (Mapping, später KI).

**Core Features:**
- Statusanzeige (Flags, Rohdaten, interpretierte Werte)
- Steuerung von Fahrwerk, Lichtern, Frachtluke, etc. (virtuelle Eingabe)
- Token-Auth, CORS, Logging, .env
- Sprachsteuerung: Textbefehl an /api/v1/command, Mapping/KI im Backend
- Flutter-Frontend: Statusanzeige, Buttons, Spracheingabe, Rückmeldung

## 2. Architektur

- **Backend (FastAPI, Python):**
  - status_fetcher.py, cargo_module.py, log_module.py, command_parser.py
  - Endpunkte: /api/v1/status, /api/v1/status/parsed, /api/v1/action, /api/v1/command
  - Virtuelle Eingabe (uinput), Keymapping, Token-Auth, Logging
- **Frontend (Flutter, Dart):**
  - Statusanzeige, Steuerbuttons, Spracheingabe (speech_to_text), Rückmeldung
  - Kommunikation via HTTP (REST), optional WebSocket
- **Doku:**
  - docs/-Ordner: Konzept, API, KI, Aufgaben, Changelog

## 3. Tech Stack
- **Backend:** Python 3, FastAPI, Uvicorn, Pydantic, python-uinput, python-dotenv, Pytest
- **Frontend:** Flutter, Dart, speech_to_text
- **Doku:** Markdown, docs/-Ordner

## 4. Milestones
1. **Backend-API & Grundfunktionen**
2. **Flutter-Frontend (Status, Buttons, Spracheingabe)**
3. **Sprachsteuerung & Mapping**
4. **Tests, Security, Doku**
5. **(Optional) KI-Integration, WebSocket, weitere Features**

## 5. Weitere Überlegungen
- Mapping und KI-Logik modular halten
- API- und Security-Tests regelmäßig ergänzen
- Doku und Mapping im Projektverlauf pflegen

## [2025-07-19]
- Architektur und Planung an aktuelle Lösung (API-Backend + Flutter-Frontend + Sprachsteuerung) angepasst.
