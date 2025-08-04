"""
Comprehensive test suite for Inara API integration.

Tests cover configuration, models, client functionality, and API endpoints.
"""

import asyncio
import json
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
from typing import Dict, Any

import httpx
from fastapi.testclient import TestClient
from pydantic import ValidationError

from elite_status.inara_config import InaraConfig, get_inara_config, validate_config
from elite_status.inara_models import (
    InaraRequest, InaraResponse, InaraEvent, InaraEventType,
    CommanderProfile, ShipLoadout, SystemFaction, Station,
    create_inara_timestamp, validate_timestamp
)
from elite_status.inara_client import (
    InaraClient, InaraApiException, InaraAuthenticationException,
    InaraRateLimitException
)
from elite_status.main import app


class TestInaraConfig:
    """Test Inara configuration management."""
    
    @patch.dict('os.environ', {
        'INARA_API_KEY': 'test_key',
        'INARA_APP_NAME': 'TestApp',
        'INARA_TIMEOUT': '60'
    })
    def test_config_from_env(self):
        """Test configuration loading from environment variables."""
        config = InaraConfig()
        assert config.api_key == 'test_key'
        assert config.app_name == 'TestApp'
        assert config.timeout == 60
        assert config.base_url == 'https://inara.cz/inapi/v1/'  # default
    
    def test_config_validation_missing_api_key(self):
        """Test configuration validation with missing API key."""
        with pytest.raises(ValidationError) as exc_info:
            InaraConfig(api_key='')
        assert 'Inara API key is required' in str(exc_info.value)
    
    def test_config_validation_invalid_timeout(self):
        """Test configuration validation with invalid timeout."""
        with pytest.raises(ValidationError) as exc_info:
            InaraConfig(api_key='test_key', timeout=-1)
        assert 'Timeout must be positive' in str(exc_info.value)
    
    def test_config_validation_invalid_retries(self):
        """Test configuration validation with invalid retry count."""
        with pytest.raises(ValidationError) as exc_info:
            InaraConfig(api_key='test_key', max_retries=-1)
        assert 'Max retries cannot be negative' in str(exc_info.value)
    
    @patch.dict('os.environ', {'INARA_API_KEY': 'test_key'})
    def test_get_inara_config(self):
        """Test configuration getter function."""
        config = get_inara_config()
        assert isinstance(config, InaraConfig)
        assert config.api_key == 'test_key'
    
    @patch.dict('os.environ', {'INARA_API_KEY': 'test_key'})
    def test_validate_config_success(self):
        """Test configuration validation success."""
        assert validate_config() is True
    
    def test_validate_config_failure(self):
        """Test configuration validation failure."""
        with patch('elite_status.inara_config.get_inara_config', side_effect=Exception('Config error')):
            with pytest.raises(ValueError) as exc_info:
                validate_config()
            assert 'Invalid Inara configuration' in str(exc_info.value)


class TestInaraModels:
    """Test Inara data models."""
    
    def test_inara_event_creation(self):
        """Test Inara event model creation."""
        event = InaraEvent(
            eventName=InaraEventType.GET_COMMANDER_PROFILE,
            eventTimestamp='2023-01-01T00:00:00.000Z',
            eventData={'test': 'data'}
        )
        assert event.eventName == InaraEventType.GET_COMMANDER_PROFILE
        assert event.eventTimestamp == '2023-01-01T00:00:00.000Z'
        assert event.eventData == {'test': 'data'}
    
    def test_commander_profile_model(self):
        """Test CommanderProfile model validation."""
        profile_data = {
            'userID': 12345,
            'userName': 'TestUser',
            'commanderName': 'CMDR Test',
            'commanderRanksPilot': {
                'combat': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'trade': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'explore': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'soldier': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'exobiologist': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'cqc': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'federation': {'rankName': 'Admiral', 'rankValue': 12, 'rankProgress': 100.0},
                'empire': {'rankName': 'King', 'rankValue': 12, 'rankProgress': 100.0}
            },
            'commanderCredits': {'balance': 1000000, 'loan': 0},
            'profileCreated': '2023-01-01T00:00:00.000Z',
            'profileLastUpdate': '2023-01-01T00:00:00.000Z'
        }
        
        profile = CommanderProfile(**profile_data)
        assert profile.userID == 12345
        assert profile.commanderName == 'CMDR Test'
        assert profile.commanderCredits.balance == 1000000
    
    def test_ship_loadout_model(self):
        """Test ShipLoadout model validation."""
        ship_data = {
            'shipType': 'Anaconda',
            'shipGameID': 12345,
            'shipName': 'Test Ship',
            'isCurrentShip': True,
            'shipValue': 500000000,
            'shipHullValue': 150000000,
            'shipModulesValue': 350000000,
            'shipRebuyCost': 25000000,
            'modules': [],
            'shipLastUpdate': '2023-01-01T00:00:00.000Z'
        }
        
        ship = ShipLoadout(**ship_data)
        assert ship.shipType == 'Anaconda'
        assert ship.isCurrentShip is True
        assert ship.shipValue == 500000000
    
    def test_create_inara_timestamp(self):
        """Test timestamp creation utility."""
        timestamp = create_inara_timestamp()
        assert timestamp.endswith('Z')
        assert validate_timestamp(timestamp) is True
    
    def test_validate_timestamp_valid(self):
        """Test timestamp validation with valid timestamp."""
        assert validate_timestamp('2023-01-01T00:00:00.000Z') is True
        assert validate_timestamp('2023-01-01T00:00:00+00:00') is True
    
    def test_validate_timestamp_invalid(self):
        """Test timestamp validation with invalid timestamp."""
        assert validate_timestamp('invalid-timestamp') is False
        assert validate_timestamp('2023-13-01T00:00:00.000Z') is False


class TestInaraClient:
    """Test Inara API client functionality."""
    
    @pytest.fixture
    def mock_config(self):
        """Create mock configuration for testing."""
        return InaraConfig(
            api_key='test_api_key',
            app_name='TestApp',
            app_version='1.0.0',
            timeout=30,
            max_retries=3,
            rate_limit_requests=10,
            rate_limit_window=60
        )
    
    @pytest.fixture
    def client(self, mock_config):
        """Create client instance for testing."""
        return InaraClient(config=mock_config, commander_name='CMDR Test')
    
    def test_client_initialization(self, client, mock_config):
        """Test client initialization."""
        assert client.config == mock_config
        assert client.commander_name == 'CMDR Test'
        assert isinstance(client.client, httpx.AsyncClient)
    
    def test_create_header(self, client):
        """Test API header creation."""
        header = client._create_header()
        assert header.appName == 'TestApp'
        assert header.APIkey == 'test_api_key'
        assert header.commanderName == 'CMDR Test'
    
    def test_create_event(self, client):
        """Test API event creation."""
        event = client._create_event(
            InaraEventType.GET_COMMANDER_PROFILE,
            {'test': 'data'},
            123
        )
        assert event.eventName == InaraEventType.GET_COMMANDER_PROFILE
        assert event.eventData == {'test': 'data'}
        assert event.eventCustomID == 123
        assert event.eventTimestamp.endswith('Z')
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, client):
        """Test rate limiting functionality."""
        # Fill rate limit
        for _ in range(client.config.rate_limit_requests):
            await client._check_rate_limit()
        
        # Next request should be delayed
        start_time = asyncio.get_event_loop().time()
        await client._check_rate_limit()
        end_time = asyncio.get_event_loop().time()
        
        # Should have been delayed (allow some tolerance for test execution)
        assert end_time - start_time >= 0.9  # Almost 1 second delay
    
    def test_cache_key_generation(self, client):
        """Test cache key generation."""
        request = InaraRequest(
            header=client._create_header(),
            events=[client._create_event(InaraEventType.GET_COMMANDER_PROFILE)]
        )
        
        key1 = client._get_cache_key(request)
        key2 = client._get_cache_key(request)
        
        assert key1 == key2  # Same request should generate same key
        assert 'CMDR Test' in key1  # Should include commander name
    
    def test_caching_functionality(self, client):
        """Test response caching."""
        cache_key = 'test_key'
        
        # Initially not cached
        assert not client._is_cached(cache_key)
        assert client._get_cached(cache_key) is None
        
        # Create and cache response
        response = InaraResponse(
            header=client._create_header(),
            events=[]
        )
        client._set_cache(cache_key, response)
        
        # Should now be cached
        assert client._is_cached(cache_key)
        cached = client._get_cached(cache_key)
        assert cached is not None
        assert cached.header.appName == response.header.appName
    
    @pytest.mark.asyncio
    async def test_make_request_success(self, client):
        """Test successful API request."""
        mock_response_data = {
            'header': {
                'appName': 'TestApp',
                'appVersion': '1.0.0',
                'isDeveloped': True,
                'APIkey': 'test_api_key'
            },
            'events': [{
                'eventStatus': 200,
                'eventStatusText': 'OK',
                'eventData': {'test': 'data'}
            }]
        }
        
        with patch.object(client.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = Mock()
            mock_post.return_value = mock_response
            
            request = InaraRequest(
                header=client._create_header(),
                events=[client._create_event(InaraEventType.GET_COMMANDER_PROFILE)]
            )
            
            response = await client._make_request(request)
            
            assert response.events[0].eventStatus == 200
            assert response.events[0].eventData == {'test': 'data'}
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_make_request_authentication_error(self, client):
        """Test API request with authentication error."""
        mock_response_data = {
            'header': {
                'appName': 'TestApp',
                'appVersion': '1.0.0',
                'isDeveloped': True,
                'APIkey': 'test_api_key'
            },
            'events': [{
                'eventStatus': 202,
                'eventStatusText': 'Authentication failed',
                'eventData': None
            }]
        }
        
        with patch.object(client.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = Mock()
            mock_post.return_value = mock_response
            
            request = InaraRequest(
                header=client._create_header(),
                events=[client._create_event(InaraEventType.GET_COMMANDER_PROFILE)]
            )
            
            with pytest.raises(InaraAuthenticationException):
                await client._make_request(request)
    
    @pytest.mark.asyncio
    async def test_make_request_rate_limit_error(self, client):
        """Test API request with rate limit error."""
        with patch.object(client.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.text = 'Rate limit exceeded'
            mock_post.return_value = mock_response
            
            request = InaraRequest(
                header=client._create_header(),
                events=[client._create_event(InaraEventType.GET_COMMANDER_PROFILE)]
            )
            
            with pytest.raises(InaraRateLimitException):
                await client._make_request(request)
    
    @pytest.mark.asyncio
    async def test_make_request_retry_logic(self, client):
        """Test request retry logic on network errors."""
        with patch.object(client.client, 'post') as mock_post:
            # First two calls fail, third succeeds
            mock_post.side_effect = [
                httpx.RequestError('Network error'),
                httpx.RequestError('Network error'),
                Mock(
                    status_code=200,
                    json=lambda: {
                        'header': {
                            'appName': 'TestApp',
                            'appVersion': '1.0.0',
                            'isDeveloped': True,
                            'APIkey': 'test_api_key'
                        },
                        'events': [{
                            'eventStatus': 200,
                            'eventStatusText': 'OK',
                            'eventData': {'test': 'data'}
                        }]
                    },
                    raise_for_status=Mock()
                )
            ]
            
            request = InaraRequest(
                header=client._create_header(),
                events=[client._create_event(InaraEventType.GET_COMMANDER_PROFILE)]
            )
            
            # Should succeed after retries
            response = await client._make_request(request)
            assert response.events[0].eventStatus == 200
            assert mock_post.call_count == 3
    
    @pytest.mark.asyncio
    async def test_get_commander_profile(self, client):
        """Test getting commander profile."""
        mock_profile_data = {
            'userID': 12345,
            'userName': 'TestUser',
            'commanderName': 'CMDR Test',
            'commanderRanksPilot': {
                'combat': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'trade': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'explore': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'soldier': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'exobiologist': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'cqc': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'federation': {'rankName': 'Admiral', 'rankValue': 12, 'rankProgress': 100.0},
                'empire': {'rankName': 'King', 'rankValue': 12, 'rankProgress': 100.0}
            },
            'commanderCredits': {'balance': 1000000, 'loan': 0},
            'profileCreated': '2023-01-01T00:00:00.000Z',
            'profileLastUpdate': '2023-01-01T00:00:00.000Z'
        }
        
        with patch.object(client, 'send_events') as mock_send:
            mock_response = InaraResponse(
                header=client._create_header(),
                events=[Mock(eventData=mock_profile_data)]
            )
            mock_send.return_value = mock_response
            
            profile = await client.get_commander_profile()
            
            assert profile is not None
            assert profile.userID == 12345
            assert profile.commanderName == 'CMDR Test'
            mock_send.assert_called_once()
    
    def test_clear_cache(self, client):
        """Test cache clearing."""
        # Add something to cache
        client._cache['test'] = {'data': 'test'}
        assert len(client._cache) > 0
        
        # Clear cache
        client.clear_cache()
        assert len(client._cache) == 0


class TestInaraRouter:
    """Test Inara API FastAPI router."""
    
    @pytest.fixture
    def test_client(self):
        """Create test client for FastAPI app."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_inara_client(self):
        """Create mock Inara client."""
        return Mock(spec=InaraClient)
    
    def test_health_check_endpoint(self, test_client):
        """Test health check endpoint."""
        with patch('elite_status.inara_router.validate_config'):
            with patch('elite_status.inara_router.InaraClient') as mock_client_class:
                mock_client = AsyncMock()
                mock_client.__aenter__ = AsyncMock(return_value=mock_client)
                mock_client.__aexit__ = AsyncMock(return_value=None)
                mock_client.get_commander_profile = AsyncMock(return_value=None)
                mock_client_class.return_value = mock_client
                
                response = test_client.get('/api/v1/inara/health')
                
                assert response.status_code == 200
                data = response.json()
                assert 'status' in data
                assert 'inara_api' in data
                assert 'configuration' in data
                assert 'timestamp' in data
    
    def test_get_commander_profile_endpoint(self, test_client):
        """Test commander profile endpoint."""
        mock_profile = {
            'userID': 12345,
            'userName': 'TestUser',
            'commanderName': 'CMDR Test',
            'commanderRanksPilot': {
                'combat': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'trade': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'explore': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'soldier': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'exobiologist': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'cqc': {'rankName': 'Elite', 'rankValue': 8, 'rankProgress': 100.0},
                'federation': {'rankName': 'Admiral', 'rankValue': 12, 'rankProgress': 100.0},
                'empire': {'rankName': 'King', 'rankValue': 12, 'rankProgress': 100.0}
            },
            'commanderCredits': {'balance': 1000000, 'loan': 0},
            'profileCreated': '2023-01-01T00:00:00.000Z',
            'profileLastUpdate': '2023-01-01T00:00:00.000Z'
        }
        
        with patch('elite_status.inara_router.get_inara_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_commander_profile = AsyncMock(
                return_value=CommanderProfile(**mock_profile)
            )
            mock_get_client.return_value = mock_client
            
            response = test_client.get('/api/v1/inara/commander/CMDR%20Test/profile')
            
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['data']['userID'] == 12345
            assert data['data']['commanderName'] == 'CMDR Test'
    
    def test_get_commander_profile_not_found(self, test_client):
        """Test commander profile endpoint when profile not found."""
        with patch('elite_status.inara_router.get_inara_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_commander_profile = AsyncMock(return_value=None)
            mock_get_client.return_value = mock_client
            
            response = test_client.get('/api/v1/inara/commander/NonExistent/profile')
            
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is False
            assert data['message'] == 'Commander profile not found'
            assert data['data'] is None
    
    def test_authentication_error_handling(self, test_client):
        """Test authentication error handling in endpoints."""
        with patch('elite_status.inara_router.get_inara_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_commander_profile = AsyncMock(
                side_effect=InaraAuthenticationException('Auth failed')
            )
            mock_get_client.return_value = mock_client
            
            response = test_client.get('/api/v1/inara/commander/CMDR%20Test/profile')
            
            assert response.status_code == 401
            assert 'Authentication failed' in response.json()['detail']
    
    def test_rate_limit_error_handling(self, test_client):
        """Test rate limit error handling in endpoints."""
        with patch('elite_status.inara_router.get_inara_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_commander_profile = AsyncMock(
                side_effect=InaraRateLimitException('Rate limit exceeded')
            )
            mock_get_client.return_value = mock_client
            
            response = test_client.get('/api/v1/inara/commander/CMDR%20Test/profile')
            
            assert response.status_code == 429
            assert 'Rate limit exceeded' in response.json()['detail']
    
    def test_clear_cache_endpoint(self, test_client):
        """Test cache clearing endpoint."""
        with patch('elite_status.inara_router.get_inara_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.clear_cache = Mock()
            mock_get_client.return_value = mock_client
            
            response = test_client.delete('/api/v1/inara/cache')
            
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['message'] == 'Cache cleared successfully'
            mock_client.clear_cache.assert_called_once()


# Integration tests
class TestInaraIntegration:
    """Integration tests for the complete Inara system."""
    
    @pytest.mark.asyncio
    async def test_full_integration_flow(self):
        """Test complete integration flow from config to API response."""
        # This would be a real integration test with actual API calls
        # For now, we'll test the flow with mocks
        
        config = InaraConfig(
            api_key='test_key',
            app_name='TestApp',
            timeout=30,
            cache_enabled=True
        )
        
        async with InaraClient(config=config, commander_name='CMDR Test') as client:
            # Test that client is properly initialized
            assert client.config.api_key == 'test_key'
            assert client.commander_name == 'CMDR Test'
            
            # Test header creation
            header = client._create_header()
            assert header.APIkey == 'test_key'
            assert header.commanderName == 'CMDR Test'
            
            # Test event creation
            event = client._create_event(InaraEventType.GET_COMMANDER_PROFILE)
            assert event.eventName == InaraEventType.GET_COMMANDER_PROFILE
            
            # Test request creation
            request = InaraRequest(header=header, events=[event])
            assert len(request.events) == 1
            assert request.header.APIkey == 'test_key'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])