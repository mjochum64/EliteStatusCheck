"""
Mock data and fixtures for Inara API testing.

This module provides comprehensive mock data structures that mirror
the actual Inara API responses for testing purposes.
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Any


class InaraMockData:
    """Collection of mock data for Inara API responses."""
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp in ISO format."""
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    @classmethod
    def successful_header(cls, event_name: str) -> Dict[str, Any]:
        """Generate a successful response header."""
        return {
            "eventName": event_name,
            "eventVersion": 1,
            "eventTimestamp": cls.get_timestamp(),
            "eventStatus": 200,
            "eventStatusText": "OK"
        }
    
    @classmethod
    def error_header(cls, event_name: str, status: int, message: str) -> Dict[str, Any]:
        """Generate an error response header."""
        return {
            "eventName": event_name,
            "eventVersion": 1,
            "eventTimestamp": cls.get_timestamp(),
            "eventStatus": status,
            "eventStatusText": message
        }
    
    @classmethod
    def market_data_response(cls, station_id: int = 12345) -> Dict[str, Any]:
        """Mock market data response for a station."""
        return {
            "header": cls.successful_header("getMarketForStation"),
            "events": [{
                "stationID": station_id,
                "stationName": "Abraham Lincoln",
                "systemName": "Sol",
                "systemCoordinates": [0, 0, 0],
                "distanceToArrival": 486,
                "marketUpdateTime": cls.get_timestamp(),
                "marketData": [
                    {
                        "commodityID": 128049204,
                        "commodityName": "Gold",
                        "sellPrice": 50125,
                        "buyPrice": 49875,
                        "stock": 156,
                        "demand": 0,
                        "stockBracket": 2,
                        "demandBracket": 0
                    },
                    {
                        "commodityID": 128049205,
                        "commodityName": "Silver",
                        "sellPrice": 4875,
                        "buyPrice": 4725,
                        "stock": 0,
                        "demand": 342,
                        "stockBracket": 0,
                        "demandBracket": 2
                    },
                    {
                        "commodityID": 128049202,
                        "commodityName": "Palladium",
                        "sellPrice": 13156,
                        "buyPrice": 12844,
                        "stock": 89,
                        "demand": 0,
                        "stockBracket": 1,
                        "demandBracket": 0
                    },
                    {
                        "commodityID": 128049203,
                        "commodityName": "Platinum",
                        "sellPrice": 19279,
                        "buyPrice": 18721,
                        "stock": 0,
                        "demand": 156,
                        "stockBracket": 0,
                        "demandBracket": 2
                    }
                ]
            }]
        }
    
    @classmethod
    def stations_in_system_response(cls, system_name: str = "Sol") -> Dict[str, Any]:
        """Mock stations in system response."""
        return {
            "header": cls.successful_header("getStationsInSystem"),
            "events": [{
                "systemName": system_name,
                "systemCoordinates": [0, 0, 0],
                "stations": [
                    {
                        "stationID": 12345,
                        "stationName": "Abraham Lincoln",
                        "stationType": "Coriolis Starport",
                        "distanceToArrival": 486,
                        "allegiance": "Federation",
                        "government": "Corporate",
                        "economy": "High Tech",
                        "secondEconomy": "Industrial",
                        "hasMarket": True,
                        "hasOutfitting": True,
                        "hasShipyard": True,
                        "hasRearm": True,
                        "hasRefuel": True,
                        "hasRepair": True,
                        "dockingPads": {
                            "small": 20,
                            "medium": 8,
                            "large": 4
                        },
                        "controllingFaction": "Sol Workers' Party"
                    },
                    {
                        "stationID": 12346,
                        "stationName": "Daedalus",
                        "stationType": "Ocellus Starport",
                        "distanceToArrival": 384,
                        "allegiance": "Federation",
                        "government": "Corporate",
                        "economy": "Industrial",
                        "secondEconomy": "Extraction",
                        "hasMarket": True,
                        "hasOutfitting": False,
                        "hasShipyard": False,
                        "hasRearm": True,
                        "hasRefuel": True,
                        "hasRepair": True,
                        "dockingPads": {
                            "small": 16,
                            "medium": 6,
                            "large": 2
                        },
                        "controllingFaction": "Sol Workers' Party"
                    },
                    {
                        "stationID": 12347,
                        "stationName": "Galileo",
                        "stationType": "Orbis Starport",
                        "distanceToArrival": 505,
                        "allegiance": "Federation",
                        "government": "Corporate",
                        "economy": "Service",
                        "secondEconomy": "Tourism",
                        "hasMarket": False,
                        "hasOutfitting": True,
                        "hasShipyard": True,
                        "hasRearm": True,
                        "hasRefuel": True,
                        "hasRepair": True,
                        "dockingPads": {
                            "small": 24,
                            "medium": 10,
                            "large": 6
                        },
                        "controllingFaction": "Sol Workers' Party"
                    }
                ]
            }]
        }
    
    @classmethod
    def commodity_search_response(cls, commodity_name: str = "Gold") -> Dict[str, Any]:
        """Mock commodity search response."""
        return {
            "header": cls.successful_header("getCommodityByName"),
            "events": [{
                "commodityID": 128049204,
                "commodityName": commodity_name,
                "category": "Metals",
                "isRare": False,
                "averagePrice": 50000,
                "locations": [
                    {
                        "systemName": "Sol",
                        "stationName": "Abraham Lincoln",
                        "sellPrice": 50125,
                        "stock": 156,
                        "stockBracket": 2,
                        "distanceToStar": 486
                    },
                    {
                        "systemName": "Alpha Centauri",
                        "stationName": "Hutton Orbital",
                        "sellPrice": 49875,
                        "stock": 89,
                        "stockBracket": 1,
                        "distanceToStar": 6784404
                    }
                ]
            }]
        }
    
    @classmethod
    def outfitting_data_response(cls, station_id: int = 12345) -> Dict[str, Any]:
        """Mock outfitting data response."""
        return {
            "header": cls.successful_header("getOutfittingForStation"),
            "events": [{
                "stationID": station_id,
                "stationName": "Abraham Lincoln",
                "systemName": "Sol",
                "outfittingUpdateTime": cls.get_timestamp(),
                "modules": [
                    {
                        "moduleID": 128049495,
                        "moduleName": "Frame Shift Drive",
                        "moduleClass": 5,
                        "moduleRating": "A",
                        "price": 5103953,
                        "category": "Core Internal"
                    },
                    {
                        "moduleID": 128049496,
                        "moduleName": "Power Plant",
                        "moduleClass": 6,
                        "moduleRating": "A",
                        "price": 1610080,
                        "category": "Core Internal"
                    },
                    {
                        "moduleID": 128049497,
                        "moduleName": "Thrusters",
                        "moduleClass": 7,
                        "moduleRating": "A",
                        "price": 5103953,
                        "category": "Core Internal"
                    }
                ]
            }]
        }
    
    @classmethod
    def error_response(cls, event_name: str, error_code: int = 400, 
                      error_message: str = "Bad Request") -> Dict[str, Any]:
        """Mock error response."""
        return {
            "header": cls.error_header(event_name, error_code, error_message),
            "events": []
        }
    
    @classmethod
    def rate_limit_response(cls, event_name: str) -> Dict[str, Any]:
        """Mock rate limit exceeded response."""
        return cls.error_response(
            event_name, 
            429, 
            "Rate limit exceeded. Please wait before making another request."
        )
    
    @classmethod
    def unauthorized_response(cls, event_name: str) -> Dict[str, Any]:
        """Mock unauthorized response."""
        return cls.error_response(
            event_name,
            401,
            "Unauthorized. Invalid or missing API key."
        )
    
    @classmethod
    def not_found_response(cls, event_name: str) -> Dict[str, Any]:
        """Mock not found response."""
        return cls.error_response(
            event_name,
            404,
            "Resource not found."
        )
    
    @classmethod
    def server_error_response(cls, event_name: str) -> Dict[str, Any]:
        """Mock server error response."""
        return cls.error_response(
            event_name,
            500,
            "Internal server error. Please try again later."
        )


class InaraTestFixtures:
    """Test fixtures and helper methods for Inara API testing."""
    
    @staticmethod
    def mock_httpx_response(json_data: Dict[str, Any], status_code: int = 200):
        """Create a mock httpx response object."""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.json.return_value = json_data
        mock_response.status_code = status_code
        mock_response.raise_for_status.return_value = None
        
        if status_code >= 400:
            from httpx import HTTPStatusError
            mock_response.raise_for_status.side_effect = HTTPStatusError(
                f"HTTP {status_code}", 
                request=Mock(), 
                response=mock_response
            )
        
        return mock_response
    
    @staticmethod
    def create_test_environment_vars() -> Dict[str, str]:
        """Create test environment variables."""
        return {
            "INARA_API_KEY": "test_api_key_12345",
            "INARA_API_BASE_URL": "https://inara.cz/inapi/v1/",
            "INARA_RATE_LIMIT": "60",  # requests per minute
            "INARA_CACHE_TTL": "300",  # cache TTL in seconds
            "ELITESTATUS_API_TOKEN": "test_token_67890"
        }
    
    @staticmethod
    def sample_api_request_payload() -> Dict[str, Any]:
        """Sample API request payload structure."""
        return {
            "header": {
                "appName": "EliteStatusCheck",
                "appVersion": "1.1.0",
                "isDeveloped": True,
                "APIkey": "test_api_key_12345",
                "commanderName": "TestCommander"
            },
            "events": [{
                "eventName": "getMarketForStation",
                "eventTimestamp": InaraMockData.get_timestamp(),
                "eventData": {
                    "stationID": 12345
                }
            }]
        }
    
    @classmethod
    def performance_test_data(cls) -> List[Dict[str, Any]]:
        """Generate data for performance testing."""
        test_cases = []
        
        # Test different station IDs
        for station_id in range(12345, 12355):
            test_cases.append({
                "request": {
                    "stationID": station_id
                },
                "expected_response_time": 1.0  # seconds
            })
        
        return test_cases
    
    @classmethod
    def error_scenarios(cls) -> List[Dict[str, Any]]:
        """Generate various error scenarios for testing."""
        return [
            {
                "name": "Invalid API Key",
                "setup": {"api_key": "invalid_key"},
                "expected_status": 401,
                "expected_response": cls.mock_data.unauthorized_response("getMarketForStation")
            },
            {
                "name": "Rate Limit Exceeded",
                "setup": {"rate_limited": True},
                "expected_status": 429,
                "expected_response": cls.mock_data.rate_limit_response("getMarketForStation")
            },
            {
                "name": "Station Not Found",
                "setup": {"station_id": 99999},
                "expected_status": 404,
                "expected_response": cls.mock_data.not_found_response("getMarketForStation")
            },
            {
                "name": "Server Error",
                "setup": {"server_error": True},
                "expected_status": 500,
                "expected_response": cls.mock_data.server_error_response("getMarketForStation")
            }
        ]
    
    # Reference to mock data class
    mock_data = InaraMockData


# Export commonly used fixtures
MOCK_MARKET_DATA = InaraMockData.market_data_response()
MOCK_STATIONS_DATA = InaraMockData.stations_in_system_response()
MOCK_COMMODITY_DATA = InaraMockData.commodity_search_response()
MOCK_OUTFITTING_DATA = InaraMockData.outfitting_data_response()
MOCK_ERROR_RESPONSE = InaraMockData.error_response("getMarketForStation")
TEST_ENV_VARS = InaraTestFixtures.create_test_environment_vars()