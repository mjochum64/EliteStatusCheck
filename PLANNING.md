# Project Plan: Elite Dangerous Status Check

## 1. Project Vision & Goals

This project aims to create a Python application that monitors and displays the current status of the game Elite Dangerous. It will fetch data from official or community-driven APIs to provide real-time information about the game's universe.

**Core Features:**
- Display the current server status (Online, Offline, Maintenance).
- Show GalNet news feeds.
- Report on community goals and their progress.
- Provide information on system statuses (e.g., incursions, conflicts).

## 2. Architecture

The application will be designed with a modular architecture to separate concerns and allow for future expansion.

- **`main.py`**: The main entry point of the application. It will initialize the GUI and start the data fetching loop.
- **`status_module.py`**: A module responsible for fetching and parsing the game's status from relevant APIs.
- **`cargo_module.py`**: This module will handle information related to commodities and trading.
- **`log_module.py`**: For logging application events, errors, and API responses.
- **`gui_module.py` (to be created)**: A module for the graphical user interface, likely using a library like Tkinter, PyQt, or a web-based framework like Streamlit.
- **`config.py` (to be created)**: For managing settings and API keys.

## 3. Tech Stack
- **Language**: Python 3
- **GUI**: To be decided (Streamlit is a strong candidate for rapid development).
- **Data Fetching**: `httpx` or `requests` for making API calls.
- **Data Parsing/Validation**: `Pydantic` for handling API response data.
- **Dependency Management**: `pip` with a `requirements.txt` file.

## 4. Data Sources

The primary data source will be the Elite Dangerous APIs, if available and public. If not, we will investigate community-supported APIs like EDSM (Elite Dangerous Star Map) or Inara.

## 5. Milestones

1.  **Phase 1: Core Functionality**
    -   Set up project structure.
    -   Implement basic API client to fetch server status.
    -   Create a simple command-line interface to display the status.
2.  **Phase 2: GUI Implementation**
    -   Choose and integrate a GUI framework.
    -   Display the server status in the GUI.
    -   Add display for GalNet news.
3.  **Phase 3: Advanced Features**
    -   Implement community goal tracking.
    -   Add system status information.
    -   Implement data caching to avoid excessive API calls.
4.  **Phase 4: Refinement & Packaging**
    -   Write comprehensive tests.
    -   Refactor and clean up the codebase.
    -   Create a distributable package of the application.

## OTHER CONSIDERATIONS:

- API rate limits must be respected.
- Graceful handling of API errors or downtime is crucial.
- The application should be user-friendly and provide clear information.

## [13.07.2025]
- Migration der Status-Logik aus `status_module.py` nach `elite_status/status_fetcher.py`.
- Migration der Logik aus `log_module.py` nach `elite_status/log_module.py`.
- Migration der Cargo-Logik aus `cargo_module.py` nach `elite_status/cargo_module.py`.
- Migration des Hauptmoduls aus `main.py` nach `elite_status/main.py`.
- Neuer Root-Endpunkt `/` gibt API-Info, Version, Doku-Link und Hauptendpunkte als JSON zurück.
- Anpassung an neue Struktur und PEP8.
- Fehlerbehandlung und Docstrings verbessert.
