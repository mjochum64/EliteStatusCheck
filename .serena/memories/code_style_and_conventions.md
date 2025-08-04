# Code Style and Conventions

## Language and Framework Conventions
- **Language**: Python 3.x
- **Framework**: FastAPI with uvicorn
- **Documentation**: German language for user-facing content, English for code

## Code Structure Patterns
- **Modular Design**: Each major functionality in separate modules
- **Router Pattern**: Each module exports a FastAPI router
- **Global Caching**: Uses global variables for status data caching
- **Exception Handling**: HTTPException for API errors

## File and Function Naming
- **Files**: Snake_case (e.g., `status_fetcher.py`)
- **Functions**: Snake_case (e.g., `get_status_data()`)
- **Variables**: Snake_case (e.g., `default_cache`)
- **Constants**: UPPER_CASE (e.g., `API_PREFIX`)

## Documentation Style
- **Docstrings**: German language with detailed parameter descriptions
- **Comments**: Mix of German and English, descriptive
- **API Documentation**: Swagger/OpenAPI integration

## Import Conventions
```python
# Standard library imports first
import os
import json
from typing import Optional

# Third-party imports
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Local imports last
from elite_status.utils import get_elite_dangerous_save_path
```

## Error Handling
- Use FastAPI's HTTPException for API errors
- Graceful handling of missing files/directories
- Logging for debugging purposes

## Testing Conventions
- **Framework**: pytest with FastAPI TestClient
- **File naming**: `test_*.py` pattern
- **Function naming**: `test_*` pattern
- **Fixtures**: Use monkeypatch and tmp_path for isolation
- **Coverage**: Test both success and error cases