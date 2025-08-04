# EliteStatusCheck MCP Server Instructions

## Project Overview
EliteStatusCheck is a FastAPI-based backend service that monitors Elite Dangerous game status data and provides a REST API for external applications to interact with the game state.

## Key Components
- **FastAPI Server**: Main application serving REST endpoints
- **Status Monitoring**: Real-time monitoring of Elite Dangerous JSON status files
- **Cargo Management**: Handling of in-game cargo data
- **Action System**: Execution of game actions (e.g., landing gear toggle)
- **Cross-platform Support**: Works on Windows, Linux (with Proton/Steam)

## API Endpoints
- `/api/v1/status` - Current game status
- `/api/v1/cargo` - Cargo data management
- `/api/v1/currentStarSystem` - Current star system info
- `/api/v1/status/parsed` - Parsed status flags as booleans
- `/api/v1/action` - Execute game actions (POST)

## Development Guidelines
1. **Security First**: Never expose sensitive data or create security vulnerabilities
2. **Cross-platform**: Support Windows and Linux (Steam/Proton) environments
3. **Real-time**: Maintain file watching capabilities for live game data
4. **Network Architecture**: Backend runs on game PC, frontend on remote devices
5. **Authentication**: Implement token-based auth for API access
6. **Testing**: Maintain comprehensive unit tests with pytest

## File Structure
- `elite_status/main.py` - FastAPI application entry point
- `elite_status/status_fetcher.py` - Game status monitoring
- `elite_status/cargo_module.py` - Cargo data handling
- `elite_status/log_module.py` - Logging functionality
- `tests/` - Unit tests for all modules

## Environment Setup
- Requires Python with FastAPI, uvicorn, watchdog
- Optional: `ELITE_STATUS_PATH` environment variable for custom game directory
- CORS enabled for local network access
- Supports conda environment activation

## Current Version: 1.0.1
Last updated: July 13, 2025
Developer: Martin Jochum
License: MIT