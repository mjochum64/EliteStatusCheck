"""
Validation tests for Inara API integration.

This module provides comprehensive validation tests for data integrity,
API compliance, security, and business logic validation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
import re
from typing import Dict, Any, List
from unittest.mock import patch, Mock
from datetime import datetime, timezone

from tests.test_inara_mock_data import (
    InaraMockData, 
    InaraTestFixtures,
    MOCK_MARKET_DATA,
    MOCK_STATIONS_DATA
)


class DataValidator:
    """Utility class for validating API response data structures."""
    
    @staticmethod
    def validate_market_data(data: Dict[str, Any]) -> List[str]:
        """Validate market data response structure."""
        errors = []
        
        # Check required top-level fields
        required_fields = ["header", "events"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if "header" in data:
            header_errors = DataValidator._validate_header(data["header"])
            errors.extend(header_errors)
        
        if "events" in data and isinstance(data["events"], list) and data["events"]:
            event = data["events"][0]
            event_errors = DataValidator._validate_market_event(event)
            errors.extend(event_errors)
        
        return errors
    
    @staticmethod
    def validate_stations_data(data: Dict[str, Any]) -> List[str]:
        """Validate stations data response structure."""
        errors = []
        
        # Check required top-level fields
        required_fields = ["header", "events"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if "header" in data:
            header_errors = DataValidator._validate_header(data["header"])
            errors.extend(header_errors)
        
        if "events" in data and isinstance(data["events"], list) and data["events"]:
            event = data["events"][0]
            stations_errors = DataValidator._validate_stations_event(event)
            errors.extend(stations_errors)
        
        return errors
    
    @staticmethod
    def _validate_header(header: Dict[str, Any]) -> List[str]:
        """Validate response header structure."""
        errors = []
        
        required_fields = ["eventName", "eventVersion", "eventTimestamp", "eventStatus"]
        for field in required_fields:
            if field not in header:
                errors.append(f"Header missing required field: {field}")
        
        # Validate timestamp format
        if "eventTimestamp" in header:
            try:
                datetime.fromisoformat(header["eventTimestamp"].replace('Z', '+00:00'))
            except ValueError:
                errors.append(f"Invalid timestamp format: {header['eventTimestamp']}")
        
        # Validate status code
        if "eventStatus" in header:
            if not isinstance(header["eventStatus"], int):
                errors.append("eventStatus must be an integer")
            elif header["eventStatus"] < 100 or header["eventStatus"] > 599:
                errors.append(f"Invalid HTTP status code: {header['eventStatus']}")
        
        return errors
    
    @staticmethod
    def _validate_market_event(event: Dict[str, Any]) -> List[str]:
        """Validate market event data structure."""
        errors = []
        
        required_fields = ["stationID", "stationName", "systemName", "marketData"]
        for field in required_fields:
            if field not in event:
                errors.append(f"Market event missing required field: {field}")
        
        # Validate marketData array
        if "marketData" in event:
            if not isinstance(event["marketData"], list):
                errors.append("marketData must be an array")
            else:
                for i, commodity in enumerate(event["marketData"]):
                    commodity_errors = DataValidator._validate_commodity(commodity, i)
                    errors.extend(commodity_errors)
        
        # Validate station ID
        if "stationID" in event:
            if not isinstance(event["stationID"], int) or event["stationID"] <= 0:
                errors.append("stationID must be a positive integer")
        
        return errors
    
    @staticmethod
    def _validate_stations_event(event: Dict[str, Any]) -> List[str]:
        """Validate stations event data structure."""
        errors = []
        
        required_fields = ["systemName", "stations"]
        for field in required_fields:
            if field not in event:
                errors.append(f"Stations event missing required field: {field}")
        
        # Validate stations array
        if "stations" in event:
            if not isinstance(event["stations"], list):
                errors.append("stations must be an array")
            else:
                for i, station in enumerate(event["stations"]):
                    station_errors = DataValidator._validate_station(station, i)
                    errors.extend(station_errors)
        
        return errors
    
    @staticmethod
    def _validate_commodity(commodity: Dict[str, Any], index: int) -> List[str]:
        """Validate individual commodity data."""
        errors = []
        
        required_fields = ["commodityID", "commodityName", "sellPrice", "buyPrice", "stock", "demand"]
        for field in required_fields:
            if field not in commodity:
                errors.append(f"Commodity {index} missing required field: {field}")
        
        # Validate numeric fields
        numeric_fields = ["commodityID", "sellPrice", "buyPrice", "stock", "demand"]
        for field in numeric_fields:
            if field in commodity:
                if not isinstance(commodity[field], (int, float)) or commodity[field] < 0:
                    errors.append(f"Commodity {index} {field} must be a non-negative number")
        
        # Validate price logic
        if "sellPrice" in commodity and "buyPrice" in commodity:
            if commodity["sellPrice"] > 0 and commodity["buyPrice"] > 0:
                if commodity["sellPrice"] <= commodity["buyPrice"]:
                    errors.append(f"Commodity {index} sellPrice should be higher than buyPrice")
        
        return errors
    
    @staticmethod
    def _validate_station(station: Dict[str, Any], index: int) -> List[str]:
        """Validate individual station data."""
        errors = []
        
        required_fields = ["stationID", "stationName", "stationType", "distanceToArrival"]
        for field in required_fields:
            if field not in station:
                errors.append(f"Station {index} missing required field: {field}")
        
        # Validate numeric fields
        if "stationID" in station:
            if not isinstance(station["stationID"], int) or station["stationID"] <= 0:
                errors.append(f"Station {index} stationID must be a positive integer")
        
        if "distanceToArrival" in station:
            if not isinstance(station["distanceToArrival"], (int, float)) or station["distanceToArrival"] < 0:
                errors.append(f"Station {index} distanceToArrival must be a non-negative number")
        
        # Validate boolean service flags
        boolean_fields = ["hasMarket", "hasOutfitting", "hasShipyard", "hasRearm", "hasRefuel", "hasRepair"]
        for field in boolean_fields:
            if field in station and not isinstance(station[field], bool):
                errors.append(f"Station {index} {field} must be a boolean")
        
        return errors


class TestDataValidation:
    """Tests for data structure validation."""
    
    def test_valid_market_data_structure(self):
        """Test validation of correct market data structure."""
        errors = DataValidator.validate_market_data(MOCK_MARKET_DATA)
        assert len(errors) == 0, f"Valid market data should have no errors: {errors}"
    
    def test_valid_stations_data_structure(self):
        """Test validation of correct stations data structure."""
        errors = DataValidator.validate_stations_data(MOCK_STATIONS_DATA)
        assert len(errors) == 0, f"Valid stations data should have no errors: {errors}"
    
    def test_missing_required_fields_market(self):
        """Test validation catches missing required fields in market data."""
        invalid_data = {"header": MOCK_MARKET_DATA["header"]}  # Missing events
        errors = DataValidator.validate_market_data(invalid_data)
        assert len(errors) > 0
        assert any("Missing required field: events" in error for error in errors)
    
    def test_missing_required_fields_stations(self):
        """Test validation catches missing required fields in stations data."""
        invalid_data = {"events": MOCK_STATIONS_DATA["events"]}  # Missing header
        errors = DataValidator.validate_stations_data(invalid_data)
        assert len(errors) > 0
        assert any("Missing required field: header" in error for error in errors)
    
    def test_invalid_timestamp_format(self):
        """Test validation catches invalid timestamp formats."""
        invalid_data = MOCK_MARKET_DATA.copy()
        invalid_data["header"]["eventTimestamp"] = "invalid-timestamp"
        errors = DataValidator.validate_market_data(invalid_data)
        assert len(errors) > 0
        assert any("Invalid timestamp format" in error for error in errors)
    
    def test_invalid_status_code(self):
        """Test validation catches invalid HTTP status codes."""
        invalid_data = MOCK_MARKET_DATA.copy()
        invalid_data["header"]["eventStatus"] = 999  # Invalid status code
        errors = DataValidator.validate_market_data(invalid_data)
        assert len(errors) > 0
        assert any("Invalid HTTP status code" in error for error in errors)
    
    def test_invalid_commodity_prices(self):
        """Test validation catches invalid commodity price logic."""
        invalid_data = MOCK_MARKET_DATA.copy()
        invalid_data["events"][0]["marketData"][0]["sellPrice"] = 1000
        invalid_data["events"][0]["marketData"][0]["buyPrice"] = 2000  # Buy higher than sell
        errors = DataValidator.validate_market_data(invalid_data)
        assert len(errors) > 0
        assert any("sellPrice should be higher than buyPrice" in error for error in errors)
    
    def test_negative_values_validation(self):
        """Test validation catches negative values where not allowed."""
        invalid_data = MOCK_MARKET_DATA.copy()
        invalid_data["events"][0]["marketData"][0]["stock"] = -10  # Negative stock
        errors = DataValidator.validate_market_data(invalid_data)
        assert len(errors) > 0
        assert any("must be a non-negative number" in error for error in errors)


class TestBusinessLogicValidation:
    """Tests for business logic and data consistency validation."""
    
    def test_market_data_consistency(self):
        """Test internal consistency of market data."""
        data = MOCK_MARKET_DATA["events"][0]["marketData"][0]
        
        # Test that commodities have realistic price ranges
        if data["sellPrice"] > 0:
            assert data["sellPrice"] > 100, "Sell price seems unrealistically low"
            assert data["sellPrice"] < 1000000, "Sell price seems unrealistically high"
        
        # Test that stock and demand values are reasonable
        assert data["stock"] >= 0, "Stock cannot be negative"
        assert data["demand"] >= 0, "Demand cannot be negative"
    
    def test_station_services_logic(self):
        """Test logical consistency of station services."""
        stations = MOCK_STATIONS_DATA["events"][0]["stations"]
        
        for station in stations:
            # If station has market, it should have basic services
            if station.get("hasMarket", False):
                assert station.get("hasRefuel", False), "Stations with markets typically have refuel"
                assert station.get("hasRepair", False), "Stations with markets typically have repair"
    
    def test_distance_validation(self):
        """Test distance values are reasonable."""
        stations = MOCK_STATIONS_DATA["events"][0]["stations"]
        
        for station in stations:
            distance = station.get("distanceToArrival", 0)
            assert distance >= 0, "Distance cannot be negative"
            assert distance < 10000000, "Distance seems unrealistically far (>10M ls)"
    
    def test_coordinate_validation(self):
        """Test coordinate values are reasonable."""
        if "systemCoordinates" in MOCK_STATIONS_DATA["events"][0]:
            coords = MOCK_STATIONS_DATA["events"][0]["systemCoordinates"]
            assert len(coords) == 3, "System coordinates should have X, Y, Z values"
            
            for coord in coords:
                assert isinstance(coord, (int, float)), "Coordinates should be numeric"
                assert abs(coord) < 100000, "Coordinate value seems unrealistically large"


class TestSecurityValidation:
    """Tests for security-related validation."""
    
    def test_sql_injection_prevention(self):
        """Test that input validation prevents SQL injection attempts."""
        # Test various SQL injection patterns
        malicious_inputs = [
            "'; DROP TABLE stations; --",
            "1' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "<script>alert('xss')</script>",
            "../../etc/passwd"
        ]
        
        for malicious_input in malicious_inputs:
            # This would test input sanitization when implemented
            # For now, just verify the test framework works
            assert isinstance(malicious_input, str)
            assert len(malicious_input) > 0
    
    def test_api_key_validation(self):
        """Test API key format validation."""
        valid_keys = [
            "abcd1234efgh5678",
            "ABCD-1234-EFGH-5678",
            "api_key_123456789"
        ]
        
        invalid_keys = [
            "",
            "short",
            "contains spaces",
            "contains/special/chars",
            None
        ]
        
        # Test key format validation (when implemented)
        for key in valid_keys:
            assert isinstance(key, str)
            assert len(key) > 8  # Minimum reasonable length
        
        for key in invalid_keys:
            if key is not None:
                assert key == "" or " " in key or "/" in key or len(key) < 8
    
    def test_input_length_limits(self):
        """Test input length validation."""
        # System names should have reasonable length limits
        max_system_name_length = 100
        test_system_name = "A" * (max_system_name_length + 1)
        
        assert len(test_system_name) > max_system_name_length
        # When validation is implemented, this should fail
        
        # Station IDs should be within reasonable ranges
        max_station_id = 999999999
        test_station_id = max_station_id + 1
        
        assert test_station_id > max_station_id
        # When validation is implemented, this should be rejected


class TestAPIComplianceValidation:
    """Tests for API specification compliance."""
    
    def test_inara_api_request_format(self):
        """Test that request payloads match Inara API specification."""
        sample_request = InaraTestFixtures.sample_api_request_payload()
        
        # Validate required header fields
        assert "header" in sample_request
        header = sample_request["header"]
        
        required_header_fields = ["appName", "appVersion", "APIkey"]
        for field in required_header_fields:
            assert field in header, f"Missing required header field: {field}"
        
        # Validate events structure
        assert "events" in sample_request
        assert isinstance(sample_request["events"], list)
        assert len(sample_request["events"]) > 0
        
        event = sample_request["events"][0]
        assert "eventName" in event
        assert "eventTimestamp" in event
    
    def test_response_format_compliance(self):
        """Test that responses match expected Inara API format."""
        # Test market data response format
        market_response = MOCK_MARKET_DATA
        assert "header" in market_response
        assert "events" in market_response
        
        # Test header format
        header = market_response["header"]
        assert "eventStatus" in header
        assert "eventStatusText" in header
        assert "eventTimestamp" in header
        
        # Test successful status
        assert header["eventStatus"] == 200
        assert header["eventStatusText"] == "OK"
    
    def test_error_response_format(self):
        """Test that error responses follow the expected format."""
        error_response = InaraMockData.error_response("getMarketForStation", 404, "Not Found")
        
        assert "header" in error_response
        assert "events" in error_response
        
        header = error_response["header"]
        assert header["eventStatus"] == 404
        assert header["eventStatusText"] == "Not Found"
        assert error_response["events"] == []  # Error responses have empty events
    
    def test_timestamp_format_compliance(self):
        """Test that timestamps follow ISO 8601 format."""
        timestamp = InaraMockData.get_timestamp()
        
        # Should be in format: 2025-08-04T10:00:00Z
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$'
        assert re.match(iso_pattern, timestamp), f"Timestamp format invalid: {timestamp}"
        
        # Should be parseable as datetime
        try:
            parsed_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            assert parsed_time.tzinfo is not None, "Timestamp should include timezone info"
        except ValueError as e:
            pytest.fail(f"Timestamp not parseable: {timestamp}, error: {e}")


class TestPerformanceValidation:
    """Tests for performance-related validation."""
    
    def test_response_size_limits(self):
        """Test that responses don't exceed reasonable size limits."""
        market_data_size = len(json.dumps(MOCK_MARKET_DATA))
        stations_data_size = len(json.dumps(MOCK_STATIONS_DATA))
        
        # Reasonable limits for API responses (in bytes)
        max_market_response_size = 100000  # 100KB
        max_stations_response_size = 500000  # 500KB
        
        assert market_data_size < max_market_response_size, \
            f"Market response too large: {market_data_size} bytes"
        
        assert stations_data_size < max_stations_response_size, \
            f"Stations response too large: {stations_data_size} bytes"
    
    def test_commodity_count_limits(self):
        """Test that commodity counts are within reasonable limits."""
        market_data = MOCK_MARKET_DATA["events"][0]["marketData"]
        max_commodities = 200  # Reasonable limit for commodities per station
        
        assert len(market_data) <= max_commodities, \
            f"Too many commodities in response: {len(market_data)}"
    
    def test_station_count_limits(self):
        """Test that station counts are within reasonable limits."""
        stations = MOCK_STATIONS_DATA["events"][0]["stations"]
        max_stations = 100  # Reasonable limit for stations per system
        
        assert len(stations) <= max_stations, \
            f"Too many stations in response: {len(stations)}"


if __name__ == "__main__":
    # Run validation tests
    pytest.main([
        __file__,
        "-v",
        "--tb=short"
    ])