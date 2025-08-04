#!/usr/bin/env python3
"""
Debug script to test Inara API integration and identify the validation error.
"""

import asyncio
import json
import os
from pathlib import Path

# Add the project root to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from elite_status.inara_client import InaraClient, InaraApiException
from elite_status.inara_models import InaraRequest, InaraApiHeader, InaraEvent, InaraEventType, create_inara_timestamp
from elite_status.inara_config import get_config
import httpx


async def test_raw_api_request():
    """Test raw API request to see actual response structure."""
    print("=== Testing Raw Inara API Request ===")
    
    config = get_config()
    print(f"API Key configured: {config.api_key[:10]}...")
    print(f"App Name: {config.app_name}")
    print(f"App Version: {config.app_version}")
    print(f"Base URL: {config.base_url}")
    
    # Create a manual request
    header = InaraApiHeader(
        appName=config.app_name,
        appVersion=config.app_version,
        isDeveloped=True,
        APIkey=config.api_key,
        commanderName=None  # Not required for system queries
    )
    
    event = InaraEvent(
        eventName=InaraEventType.GET_SYSTEM_FACTIONS,
        eventTimestamp=create_inara_timestamp(),
        eventData={"systemName": "Ceos"},
        eventCustomID=None
    )
    
    request = InaraRequest(header=header, events=[event])
    
    print("\n=== Request Structure ===")
    request_dict = request.model_dump()
    print(json.dumps(request_dict, indent=2, default=str))
    
    # Make raw HTTP request
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            print("\n=== Making HTTP Request ===")
            response = await client.post(
                config.base_url,
                content=json.dumps(request_dict, default=str),
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"HTTP Error: {response.text}")
                return
            
            response_data = response.json()
            print("\n=== Raw Response ===")
            print(json.dumps(response_data, indent=2))
            
            # Try to validate with our model
            print("\n=== Validating Response ===")
            from elite_status.inara_models import InaraResponse
            try:
                inara_response = InaraResponse(**response_data)
                print("✅ Response validation successful!")
                print(f"Events count: {len(inara_response.events)}")
                for i, event in enumerate(inara_response.events):
                    print(f"Event {i}: Status {event.eventStatus} - {event.eventStatusText}")
            except Exception as e:
                print(f"❌ Response validation failed: {e}")
                print("Response structure doesn't match our model")
                
                # Show what fields are missing/extra
                print("\n=== Response Analysis ===")
                if isinstance(response_data, dict):
                    print("Response keys:", list(response_data.keys()))
                    if 'header' in response_data:
                        print("Header keys:", list(response_data['header'].keys()))
                    if 'events' in response_data:
                        print("Events type:", type(response_data['events']))
                        if response_data['events']:
                            print("First event keys:", list(response_data['events'][0].keys()))
                
        except Exception as e:
            print(f"Request failed: {e}")


async def test_client_request():
    """Test using the Inara client directly."""
    print("\n\n=== Testing Inara Client ===")
    
    try:
        async with InaraClient() as client:
            print("Client created successfully")
            
            # Test system factions
            print("Testing get_system_factions...")
            factions = await client.get_system_factions("Ceos")
            print(f"✅ Retrieved {len(factions)} factions")
            
    except Exception as e:
        print(f"❌ Client test failed: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Main test function."""
    print("Inara API Debug Script")
    print("=" * 50)
    
    await test_raw_api_request()
    await test_client_request()


if __name__ == "__main__":
    asyncio.run(main())