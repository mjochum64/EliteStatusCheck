# EliteStatusCheck Project Overview

## Purpose
EliteStatusCheck is a FastAPI-based backend service that monitors Elite Dangerous game status data and provides a REST API for external applications to interact with the game state. It enables remote control and status monitoring of the Elite Dangerous game through network communication.

## Tech Stack
- **Backend Framework**: FastAPI with uvicorn
- **Language**: Python 3.x
- **Dependencies**: 
  - httpx, pydantic, python-dotenv, fastapi, uvicorn
  - watchdog (file monitoring)
  - pytest, requests (testing)
  - python-uinput (system input simulation)
- **Environment**: Supports conda environments, .env configuration
- **Platform**: Cross-platform (Windows, Linux with Steam/Proton support)

## Architecture
- **Network-based Design**: Backend runs on game PC, frontend on remote devices
- **Real-time Monitoring**: Uses watchdog to monitor Elite Dangerous JSON status files
- **Modular Structure**: Separated into specialized modules (status, cargo, logging, actions)
- **Authentication**: Token-based authentication system
- **CORS**: Configured for local network access

## Key Features
- Real-time status monitoring of Elite Dangerous game files
- Action execution system (e.g., landing gear toggle) 
- Cross-platform Elite Dangerous directory detection
- Network API for remote device integration
- Comprehensive test coverage with pytest