"""
Pytest configuration and shared fixtures for EliteStatusCheck tests.

This module provides common fixtures and configuration for all test modules,
including Inara API testing setup, authentication, and mock data.
"""

import pytest
import os
import tempfile
import json
from unittest.mock import Mock, patch
from typing import Dict, Any, Generator
from pathlib import Path

# Import test utilities
try:
    from tests.test_inara_mock_data import InaraTestFixtures, InaraMockData, TEST_ENV_VARS
except ImportError:
    # Fallback for when mock data module is not available
    InaraTestFixtures = None
    InaraMockData = None
    TEST_ENV_VARS = {
        "INARA_API_KEY": "test_api_key_12345",
        "INARA_API_BASE_URL": "https://inara.cz/inapi/v1/",
        "INARA_RATE_LIMIT": "60",
        "INARA_CACHE_TTL": "300",
        "ELITESTATUS_API_TOKEN": "test_token_67890"
    }


@pytest.fixture(scope="session")
def test_env_vars() -> Dict[str, str]:
    """Provide test environment variables for the session."""
    return TEST_ENV_VARS


@pytest.fixture(scope="function")
def mock_env_vars(monkeypatch, test_env_vars):
    """Set up mock environment variables for each test."""
    for key, value in test_env_vars.items():
        monkeypatch.setenv(key, value)
    return test_env_vars


@pytest.fixture(scope="function")
def temp_elite_directory(tmp_path) -> Path:
    """Create a temporary Elite Dangerous directory structure."""
    elite_dir = tmp_path / "elite_dangerous"
    elite_dir.mkdir()
    
    # Create sample Status.json
    status_data = {
        "event": "Status",
        "Flags": 0,
        "Pips": [4, 2, 6],
        "FireGroup": 0,
        "GuiFocus": 0,
        "Fuel": {"FuelMain": 16.0, "FuelReservoir": 0.63},
        "Cargo": 0.0
    }
    
    status_file = elite_dir / "Status.json"
    status_file.write_text(json.dumps(status_data))
    
    # Create sample Cargo.json
    cargo_data = {
        "event": "Cargo",
        "Count": 0,
        "Inventory": []
    }
    
    cargo_file = elite_dir / "Cargo.json"
    cargo_file.write_text(json.dumps(cargo_data))
    
    return elite_dir


@pytest.fixture(scope="function")
def mock_elite_path(monkeypatch, temp_elite_directory):
    """Mock the Elite Dangerous save path to use temporary directory."""
    monkeypatch.setenv("ELITE_STATUS_PATH", str(temp_elite_directory))
    return temp_elite_directory


@pytest.fixture(scope="function")
def api_headers(test_env_vars) -> Dict[str, str]:
    """Provide API headers with authentication token."""
    return {
        "Authorization": f"Bearer {test_env_vars['ELITESTATUS_API_TOKEN']}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="function")
def invalid_api_headers() -> Dict[str, str]:
    """Provide invalid API headers for testing authentication."""
    return {
        "Authorization": "Bearer invalid_token_123",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="function")
def mock_inara_client():
    """Mock Inara client for testing without real API calls."""
    with patch('elite_status.inara_client.InaraClient') as mock_client:
        # Set up mock client instance
        client_instance = Mock()
        mock_client.return_value = client_instance
        
        # Mock successful responses
        if InaraMockData:
            client_instance.get_market_data.return_value = InaraMockData.market_data_response()
            client_instance.get_stations_in_system.return_value = InaraMockData.stations_in_system_response()
            client_instance.search_commodity.return_value = InaraMockData.commodity_search_response()
            client_instance.get_outfitting_data.return_value = InaraMockData.outfitting_data_response()
        else:
            # Fallback mock responses
            client_instance.get_market_data.return_value = {"header": {"eventStatus": 200}, "events": []}
            client_instance.get_stations_in_system.return_value = {"header": {"eventStatus": 200}, "events": []}
            client_instance.search_commodity.return_value = {"header": {"eventStatus": 200}, "events": []}
            client_instance.get_outfitting_data.return_value = {"header": {"eventStatus": 200}, "events": []}
        
        # Mock error responses for specific cases
        client_instance.get_market_data_error = Mock(
            side_effect=Exception("Station not found")
        )
        client_instance.rate_limit_error = Mock(
            side_effect=Exception("Rate limit exceeded")
        )
        
        yield client_instance


@pytest.fixture(scope="function")
def mock_httpx_client():
    """Mock httpx.AsyncClient for testing HTTP requests."""
    with patch('httpx.AsyncClient') as mock_client:
        client_instance = Mock()
        mock_client.return_value.__aenter__.return_value = client_instance
        mock_client.return_value.__aexit__.return_value = None
        
        # Default successful response
        if InaraTestFixtures and InaraMockData:
            mock_response = InaraTestFixtures.mock_httpx_response(
                InaraMockData.market_data_response()
            )
        else:
            # Fallback mock response
            mock_response = Mock()
            mock_response.json.return_value = {"header": {"eventStatus": 200}, "events": []}
            mock_response.status_code = 200
        client_instance.post.return_value = mock_response
        
        yield client_instance


@pytest.fixture(scope="function")
def sample_market_data() -> Dict[str, Any]:
    """Provide sample market data for testing."""
    if InaraMockData:
        return InaraMockData.market_data_response()
    else:
        return {"header": {"eventStatus": 200}, "events": [{"marketData": []}]}


@pytest.fixture(scope="function")
def sample_stations_data() -> Dict[str, Any]:
    """Provide sample stations data for testing."""
    if InaraMockData:
        return InaraMockData.stations_in_system_response()
    else:
        return {"header": {"eventStatus": 200}, "events": [{"stations": []}]}


@pytest.fixture(scope="function")
def sample_error_response() -> Dict[str, Any]:
    """Provide sample error response for testing."""
    if InaraMockData:
        return InaraMockData.error_response("getMarketForStation", 400, "Bad Request")
    else:
        return {"header": {"eventStatus": 400, "eventStatusText": "Bad Request"}, "events": []}


@pytest.fixture(scope="session")
def performance_test_data():
    """Provide data for performance testing."""
    if InaraTestFixtures:
        return InaraTestFixtures.performance_test_data()
    else:
        return [{"request": {"stationID": 12345}, "expected_response_time": 1.0}]


@pytest.fixture(scope="function")
def cache_directory(tmp_path) -> Path:
    """Create a temporary cache directory."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture(scope="function")
def mock_cache_with_data(cache_directory, sample_market_data):
    """Mock cache with pre-populated data."""
    cache_file = cache_directory / "market_12345.json"
    cache_file.write_text(json.dumps(sample_market_data))
    
    with patch('elite_status.inara_client.CACHE_DIR', str(cache_directory)):
        yield cache_directory


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Automatically clean up test files after each test."""
    yield
    # Cleanup logic here if needed
    pass


# Pytest markers for different test categories
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests requiring external services"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance/benchmark tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "api: marks tests that test API endpoints"
    )


# Custom test collection rules
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark slow tests
        if "performance" in item.nodeid or "load" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)
        
        # Mark integration tests
        if "integration" in item.nodeid or "live_api" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Mark unit tests
        if "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # Mark API tests
        if "endpoint" in item.nodeid or "api" in item.nodeid:
            item.add_marker(pytest.mark.api)


# Test database fixtures (if needed for future database testing)
@pytest.fixture(scope="function")
def test_database():
    """Provide a test database connection (placeholder for future use)."""
    # This would set up a test database if needed
    # For now, return None as we're not using a database
    return None


# Logging configuration for tests
@pytest.fixture(autouse=True)
def configure_test_logging(caplog):
    """Configure logging for tests."""
    import logging
    caplog.set_level(logging.DEBUG, logger="elite_status")
    return caplog


# WebSocket testing fixtures (for future use)
@pytest.fixture(scope="function")
def mock_websocket():
    """Mock WebSocket connection for testing real-time features."""
    with patch('websockets.connect') as mock_connect:
        mock_ws = Mock()
        mock_connect.return_value = mock_ws
        yield mock_ws