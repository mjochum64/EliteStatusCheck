# Inara API Integration

The Inara API integration provides comprehensive access to Elite Dangerous commander data, ship information, system data, and market information through the [Inara.cz](https://inara.cz) community database.

## Features

- **Commander Profiles**: Get detailed commander information including ranks, credits, and reputation
- **Ship Data**: Access complete ship loadouts, modules, and current ship information  
- **System Information**: Retrieve faction data and station listings for any system
- **Market Data**: Access commodity prices and market information for stations
- **Robust Error Handling**: Comprehensive error handling with retry logic and rate limiting
- **Response Caching**: Configurable TTL-based caching to improve performance
- **Authentication**: Secure API key-based authentication

## Configuration

Add your Inara API credentials to your `.env` file:

```bash
# Get your API key from: https://inara.cz/settings-api/
INARA_API_KEY=API_KEY_FROM_INARA
INARA_APP_NAME=EliteStatusCheck
INARA_APP_VERSION=1.1.0

# Optional configuration (defaults shown)
INARA_BASE_URL=https://inara.cz/inapi/v1/
INARA_TIMEOUT=30
INARA_MAX_RETRIES=3
INARA_RETRY_DELAY=1.0
INARA_BACKOFF_FACTOR=2.0
INARA_RATE_LIMIT_REQUESTS=100
INARA_RATE_LIMIT_WINDOW=3600
INARA_CACHE_ENABLED=true
INARA_CACHE_TTL=300
```

## API Endpoints

All endpoints are available under `/api/v1/inara/`:

### Health Check
- `GET /api/v1/inara/health` - Check service health and API connectivity

### Commander Endpoints
- `GET /api/v1/inara/commander/{commander_name}/profile` - Get commander profile
- `GET /api/v1/inara/commander/{commander_name}/ships` - Get all commander ships
- `GET /api/v1/inara/commander/{commander_name}/current-ship` - Get current active ship

### System Endpoints  
- `GET /api/v1/inara/system/{system_name}/factions` - Get system factions
- `GET /api/v1/inara/system/{system_name}/stations` - Get system stations

### Market Endpoints
- `GET /api/v1/inara/station/{station_id}/market` - Get station market data

### Utility Endpoints
- `DELETE /api/v1/inara/cache` - Clear response cache

## Usage Examples

### Get Commander Profile
```bash
curl "http://localhost:8000/api/v1/inara/commander/CMDR%20Example/profile"
```

### Get System Information
```bash
curl "http://localhost:8000/api/v1/inara/system/Sol/stations"
curl "http://localhost:8000/api/v1/inara/system/Sol/factions"  
```

### Health Check
```bash
curl "http://localhost:8000/api/v1/inara/health"
```

## Response Format

All endpoints return responses in a consistent format:

```json
{
  "success": true,
  "message": "Request completed successfully",
  "data": {
    // Response data here
  }
}
```

Error responses include additional error information:

```json
{
  "success": false,
  "message": "Error description",
  "data": null
}
```

## Error Handling

The integration includes comprehensive error handling:

- **Authentication Errors** (401): Invalid or missing API key
- **Rate Limiting** (429): API rate limit exceeded
- **API Errors** (400): Invalid requests or Inara API errors
- **Network Errors**: Automatic retry with exponential backoff
- **Validation Errors**: Invalid request parameters

## Rate Limiting

The client includes built-in rate limiting to respect Inara's API limits:

- Default: 100 requests per hour
- Configurable via `INARA_RATE_LIMIT_REQUESTS` and `INARA_RATE_LIMIT_WINDOW`
- Automatic queuing and delay when limits are reached

## Caching

Response caching is enabled by default to improve performance:

- Default TTL: 5 minutes (300 seconds)
- Configurable via `INARA_CACHE_TTL`
- Can be disabled by setting `INARA_CACHE_ENABLED=false`
- Manual cache clearing via `/api/v1/inara/cache` endpoint

## Development

### Running Tests

```bash
# Run all Inara integration tests
pytest tests/test_inara_integration.py -v

# Run specific test categories
pytest tests/test_inara_integration.py::TestInaraConfig -v
pytest tests/test_inara_integration.py::TestInaraClient -v
pytest tests/test_inara_integration.py::TestInaraRouter -v
```

### Architecture

The integration consists of several modules:

- `inara_config.py` - Configuration management with Pydantic settings
- `inara_models.py` - Data models for all API responses  
- `inara_client.py` - Core API client with authentication and error handling
- `inara_router.py` - FastAPI router providing REST endpoints
- `data_models.py` - Re-exports models for backward compatibility

### Adding New Endpoints

To add new Inara API endpoints:

1. Add the event type to `InaraEventType` enum in `inara_models.py`
2. Create corresponding data models if needed
3. Add client method in `inara_client.py`
4. Add FastAPI endpoint in `inara_router.py`
5. Add tests in `test_inara_integration.py`

## Troubleshooting

### Common Issues

1. **Authentication Failed (401)**
   - Verify your API key is correct
   - Ensure `INARA_API_KEY` is set in your environment
   - Check that your API key is active on Inara.cz

2. **Rate Limit Exceeded (429)**  
   - Reduce request frequency
   - Increase `INARA_RATE_LIMIT_WINDOW` or decrease `INARA_RATE_LIMIT_REQUESTS`
   - Enable caching to reduce API calls

3. **Configuration Errors (500)**
   - Check all required environment variables are set
   - Validate configuration with `/api/v1/inara/health` endpoint
   - Review logs for specific configuration issues

4. **Network Timeouts**
   - Increase `INARA_TIMEOUT` value
   - Check network connectivity to inara.cz
   - Review retry configuration

### Logging

Enable debug logging to troubleshoot issues:

```bash
LOG_LEVEL=DEBUG
```

The client logs all API requests, responses, errors, and caching operations.

## Resources

- [Inara API Documentation](https://inara.cz/inapi/)
- [Get Inara API Key](https://inara.cz/settings-api/) 
- [Elite Dangerous Database](https://inara.cz)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
