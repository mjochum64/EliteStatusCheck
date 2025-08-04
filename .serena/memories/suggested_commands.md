# Suggested Commands for EliteStatusCheck

## Development Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application (Development)
```bash
# Option 1: Direct Python module execution
python -m elite_status.main

# Option 2: Uvicorn with reload for development
uvicorn elite_status.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Production startup script
./start_backend.sh
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

### Environment Setup
```bash
# Set Elite Dangerous path (Linux/Steam/Proton)
export ELITE_STATUS_PATH="/path/to/Elite Dangerous"

# Activate conda environment (if using)
conda activate elite
```

### Development Server Access
- **API Documentation**: http://localhost:8000/api/v1/docs
- **OpenAPI Spec**: http://localhost:8000/api/v1/openapi.json
- **Root Endpoint**: http://localhost:8000/

### Useful Development Commands
```bash
# Check if Elite Dangerous directory is found
python -c "from elite_status.utils import get_elite_dangerous_save_path; print(get_elite_dangerous_save_path())"

# View real-time logs during development
tail -f elite_status.log  # if logging to file

# Test specific API endpoint
curl http://localhost:8000/api/v1/status/
```