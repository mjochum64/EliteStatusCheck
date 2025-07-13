# Project Tasks: Elite Dangerous Status Check

## 1. Project Setup (13. Juli 2025)

- [x] Update `GEMINI.md`, `PLANNING.md`, `TASK.md`, and `CHANGELOG.md` for the new project.
- [x] Initialize Git repository and create initial commit.
- [x] Create `requirements.txt` with initial dependencies (`httpx`, `pydantic`, `python-dotenv`).
- [x] Set up `.env.example` for any necessary API keys or configuration.
- [x] Create project folder structure und alle Kernmodule im Verzeichnis `elite_status/` angelegt und migriert.

## 2. Core Development

- [x] Implement the `status_fetcher` module to get data from an Elite Dangerous API (Statusdaten aus lokaler Datei, API-Ready).
- [x] Implementierte FastAPI-Endpunkte für Status, Cargo (Platzhalter) und Logik.
- [x] Migration und Integration der bestehenden Logik in die neue Struktur.
- [ ] Create Pydantic models in `data_models.py` to validate the API responses.
- [ ] Implement a basic command-line interface in `main.py` to display the fetched status. (Optional, aktuell nur API)
- [x] Set up logging for the application (Basis-Logging vorhanden).

## 3. GUI Development

- [ ] Choose a GUI library (e.g., Streamlit, Tkinter, PyQt).
- [ ] Implement the basic GUI layout in `gui.py`.
- [ ] Connect the GUI to the `status_fetcher` to display live data.
- [ ] Add components to display different aspects of the game status (server, GalNet, etc.).

## 4. Testing

- [x] Write unit tests for die wichtigsten API-Endpunkte (`status_fetcher`, `cargo_module`, `log_module`).
- [ ] Write tests for the Pydantic data models.
- [ ] Write tests for any data transformation logic.

**Tests ausführen:**

    pytest tests/

Die Tests simulieren verschiedene Szenarien (Erfolgsfall, Datei fehlt, Datei leer) und nutzen FastAPI TestClient sowie Pytest.

## 5. Documentation

- [x] Write a `README.md` with a project description, setup instructions, and usage guide.
- [x] Add Google-style docstrings to alle neuen Funktionen und Module.
- [x] Kommentiere komplexe oder nicht offensichtliche Codeabschnitte.
- [x] Dokumentation der API-Endpunkte und des Root-Endpunkts `/`.

## Discovered During Work

- (Empty)

## [13.07.2025]
- Migration der Status-Logik aus `status_module.py` nach `elite_status/status_fetcher.py` begonnen.
- Migration der Logik aus `log_module.py` nach `elite_status/log_module.py`.
- Migration der Cargo-Logik aus `cargo_module.py` nach `elite_status/cargo_module.py`.
- Neuer Root-Endpunkt `/` gibt API-Info, Version, Doku-Link und Hauptendpunkte als JSON zurück.
- Neuer /api/v1/cargo/ Endpunkt liefert aktuelle Frachtdaten aus Cargo.json oder eine Fehlermeldung.
