# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EliteStatusCheck is a FastAPI-based backend service that monitors Elite Dangerous game status data and provides a REST API for external applications. It enables remote control and status monitoring of the Elite Dangerous game through network communication.

**Key Architecture**: The backend runs on the game PC for system-level input control, while frontend apps run on remote devices (smartphones, tablets) and communicate over the local network.

## Essential Commands

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set Elite Dangerous path (optional, Linux/Steam/Proton)
export ELITE_STATUS_PATH="/path/to/Elite Dangerous"

# Activate conda environment (if used)
conda activate elite
```

### Running the Application
```bash
# Development server with auto-reload
uvicorn elite_status.main:app --reload --host 0.0.0.0 --port 8000

# Production startup (uses conda and .env)
./start_backend.sh

# Direct module execution
python -m elite_status.main
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_status_fetcher.py

# Run with verbose output
pytest tests/ -v
```

### API Access
- **Documentation**: http://localhost:8000/api/v1/docs
- **OpenAPI Spec**: http://localhost:8000/api/v1/openapi.json

## Architecture Overview

### Core Modules
- **`elite_status/main.py`**: FastAPI application entry point with CORS configuration
- **`elite_status/status_fetcher.py`**: Real-time file monitoring using watchdog, status caching, and action execution system
- **`elite_status/cargo_module.py`**: Cargo data management endpoints
- **`elite_status/log_module.py`**: Logging functionality and star system tracking
- **`elite_status/utils.py`**: Cross-platform Elite Dangerous directory detection
- **`elite_status/command_parser.py`**: Command parsing for game actions

### API Structure
All endpoints use `/api/v1/` prefix:
- `/api/v1/status/` - Game status monitoring
- `/api/v1/cargo/` - Cargo data management  
- `/api/v1/action` - Execute game actions (POST)
- `/api/v1/currentStarSystem` - Current star system info
- `/api/v1/status/parsed` - Parsed status flags as booleans

### Real-time Monitoring
The application uses Python's `watchdog` library to monitor Elite Dangerous JSON files (`Status.json`, `Cargo.json`) in the game's save directory. Status data is cached globally and updated in real-time.

### Action System
Supports executing game actions through system-level input simulation using `python-uinput` (Linux) for actions like landing gear toggle, requiring appropriate permissions.

## Development Guidelines

### Code Style
- **Language**: Python 3.x with FastAPI
- **Naming**: Snake_case for files, functions, and variables
- **Documentation**: German for user-facing content, English for code
- **Imports**: Standard library → third-party → local imports
- **Error Handling**: Use FastAPI's `HTTPException` for API errors

### Testing Strategy
- **Framework**: pytest with FastAPI TestClient
- **Patterns**: `test_*.py` files with `test_*` functions
- **Fixtures**: Use `monkeypatch` and `tmp_path` for test isolation
- **Coverage**: Test both success and error cases for all endpoints

### Cross-platform Considerations
- Automatic Elite Dangerous directory detection for Windows/Linux
- Steam/Proton compatibility on Linux
- Wayland limitations for virtual input (prefers X11)

## Task Completion Checklist

After making changes:
1. **Run tests**: `pytest tests/` - ensure all tests pass
2. **Verify server startup**: `uvicorn elite_status.main:app --reload`
3. **Check API docs**: Verify `/api/v1/docs` loads correctly
4. **Test modified endpoints**: Use Swagger UI or curl for manual testing

## Environment Variables
- **`ELITE_STATUS_PATH`**: Override Elite Dangerous save directory path
- **`.env`**: Supported for environment configuration (loaded via python-dotenv)

## Dependencies
- **Core**: fastapi, uvicorn, pydantic, python-dotenv
- **Monitoring**: watchdog
- **System Integration**: python-uinput (Linux input simulation)
- **Testing**: pytest, requests
- **HTTP**: httpx