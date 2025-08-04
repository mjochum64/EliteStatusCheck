# Codebase Structure

## Main Application Structure
```
elite_status/
├── main.py              # FastAPI application entry point
├── status_fetcher.py    # Core status monitoring and API endpoints
├── cargo_module.py      # Cargo data management module
├── log_module.py        # Logging functionality and endpoints
├── data_models.py       # Pydantic models (placeholder for future use)
├── utils.py             # Utility functions (path detection, etc.)
├── command_parser.py    # Command parsing for actions
├── gui.py               # GUI components (if applicable)
├── keymap.json          # Key mapping configuration
└── __init__.py          # Package initialization
```

## Core Modules

### main.py
- FastAPI application setup and configuration
- Router inclusion and CORS middleware
- API prefix configuration (/api/v1)
- Root endpoint definition

### status_fetcher.py
- Real-time file monitoring with watchdog
- Status data caching and API endpoints
- Action execution system (landing gear, etc.)
- Authentication/authorization handling

### cargo_module.py
- Cargo data management endpoints
- Integration with Elite Dangerous cargo files

### log_module.py
- Logging system and log-related API endpoints
- Current star system tracking

## Supporting Files
- `tests/` - Comprehensive pytest test suite
- `docs/` - API specifications and frontend documentation
- `start_backend.sh` - Production startup script with conda support
- `requirements.txt` - Python dependencies
- `.env.example` - Environment configuration template

## API Structure
All endpoints follow the `/api/v1/` prefix pattern:
- Status endpoints: `/api/v1/status/`
- Cargo endpoints: `/api/v1/cargo/`
- Action endpoints: `/api/v1/action`
- Logging endpoints: `/api/v1/log/` or similar