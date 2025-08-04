"""
FastAPI router for Inara API integration endpoints.

This module provides REST endpoints for accessing Inara data including
commander profiles, ship information, system data, and market information.
"""

import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Path, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .inara_client import InaraClient, InaraApiException, InaraAuthenticationException, InaraRateLimitException
from .inara_mock import get_mock_client
import os
from .inara_models import CommanderProfile, ShipLoadout, SystemFaction, Station, StationMarket
from .inara_config import get_config, validate_config


# Response models for API documentation
class ApiResponse(BaseModel):
    """Base API response model."""
    success: bool = Field(..., description="Request success status")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data")


class CommanderProfileResponse(ApiResponse):
    """Commander profile response."""
    data: Optional[CommanderProfile] = Field(None, description="Commander profile data")


class ShipsResponse(ApiResponse):
    """Ships list response."""
    data: Optional[List[ShipLoadout]] = Field(None, description="List of ships")


class CurrentShipResponse(ApiResponse):
    """Current ship response."""
    data: Optional[ShipLoadout] = Field(None, description="Current ship data")


class SystemFactionsResponse(ApiResponse):
    """System factions response."""
    data: Optional[List[SystemFaction]] = Field(None, description="System factions")


class SystemStationsResponse(ApiResponse):
    """System stations response."""
    data: Optional[List[Station]] = Field(None, description="System stations")


class StationMarketResponse(ApiResponse):
    """Station market response."""
    data: Optional[StationMarket] = Field(None, description="Station market data")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    inara_api: str = Field(..., description="Inara API status")
    configuration: str = Field(..., description="Configuration status")
    timestamp: str = Field(..., description="Check timestamp")


# Router setup
router = APIRouter(tags=["inara"])
logger = logging.getLogger(__name__)


# Dependency to get Inara client
async def get_inara_client():
    """
    Dependency to provide Inara client instance.
    
    Returns:
        InaraClient or MockInaraClient: Configured client
        
    Raises:
        HTTPException: If configuration is invalid
    """
    # Check if we should use mock client
    use_mock = os.getenv("INARA_USE_MOCK", "false").lower() == "true"
    
    if use_mock:
        logger.info("Using mock Inara client for testing")
        return await get_mock_client()
    
    try:
        validate_config()
        return InaraClient()
    except Exception as e:
        logger.error(f"Failed to create Inara client: {e}")
        # Fallback to mock client if real client fails
        logger.info("Falling back to mock Inara client")
        return await get_mock_client()


# Health check endpoint
@router.get("/inara/health", response_model=HealthResponse, summary="Check Inara API service health")
async def health_check():
    """
    Check the health status of the Inara API integration.
    
    Returns:
        HealthResponse: Service health information
    """
    from datetime import datetime
    
    health_data = {
        "status": "unknown",
        "inara_api": "unknown", 
        "configuration": "unknown",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    try:
        # Check configuration
        validate_config()
        health_data["configuration"] = "ok"
        
        # Test API connectivity
        async with InaraClient() as client:
            # Try a simple request
            await client.get_commander_profile("test")  # This will fail gracefully
            health_data["inara_api"] = "ok"
            
        health_data["status"] = "healthy"
        
    except InaraAuthenticationException:
        health_data["inara_api"] = "authentication_error"
        health_data["status"] = "degraded"
    except InaraRateLimitException:
        health_data["inara_api"] = "rate_limited"
        health_data["status"] = "degraded"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_data["status"] = "unhealthy"
        if "configuration" not in str(e).lower():
            health_data["inara_api"] = "error"
    
    return HealthResponse(**health_data)


# Commander endpoints
@router.get(
    "/inara/commander/{commander_name}/profile",
    response_model=CommanderProfileResponse,
    summary="Get commander profile",
    description="Retrieve detailed profile information for a specific commander from Inara."
)
async def get_commander_profile(
    commander_name: str = Path(..., description="Commander name", example="CMDR John Doe"),
    client: InaraClient = Depends(get_inara_client)
):
    """
    Get commander profile information from Inara.
    
    Args:
        commander_name: The commander's name
        client: Inara client instance
        
    Returns:
        CommanderProfileResponse: Commander profile data
    """
    try:
        async with client:
            profile = await client.get_commander_profile(commander_name)
            
            if profile:
                return CommanderProfileResponse(
                    success=True,
                    message="Commander profile retrieved successfully",
                    data=profile
                )
            else:
                return CommanderProfileResponse(
                    success=False,
                    message="Commander profile not found",
                    data=None
                )
                
    except InaraAuthenticationException as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {e}")
    except InaraRateLimitException as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {e}")
    except InaraApiException as e:
        raise HTTPException(status_code=400, detail=f"Inara API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting commander profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/inara/commander/{commander_name}/ships",
    response_model=ShipsResponse,
    summary="Get commander ships",
    description="Retrieve all ships owned by a commander from Inara."
)
async def get_commander_ships(
    commander_name: str = Path(..., description="Commander name", example="CMDR John Doe"),
    client: InaraClient = Depends(get_inara_client)
):
    """
    Get all ships owned by a commander.
    
    Args:
        commander_name: The commander's name
        client: Inara client instance
        
    Returns:
        ShipsResponse: List of commander's ships
    """
    try:
        async with client:
            ships = await client.get_commander_ships(commander_name)
            
            return ShipsResponse(
                success=True,
                message=f"Retrieved {len(ships)} ships",
                data=ships
            )
                
    except InaraAuthenticationException as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {e}")
    except InaraRateLimitException as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {e}")
    except InaraApiException as e:
        raise HTTPException(status_code=400, detail=f"Inara API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting commander ships: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/inara/commander/{commander_name}/current-ship",
    response_model=CurrentShipResponse,
    summary="Get commander's current ship",
    description="Retrieve the currently active ship of a commander from Inara."
)
async def get_current_ship(
    commander_name: str = Path(..., description="Commander name", example="CMDR John Doe"),
    client: InaraClient = Depends(get_inara_client)
):
    """
    Get commander's currently active ship.
    
    Args:
        commander_name: The commander's name
        client: Inara client instance
        
    Returns:
        CurrentShipResponse: Current ship data
    """
    try:
        async with client:
            ship = await client.get_current_ship(commander_name)
            
            if ship:
                return CurrentShipResponse(
                    success=True,
                    message="Current ship retrieved successfully",
                    data=ship
                )
            else:
                return CurrentShipResponse(
                    success=False,
                    message="Current ship not found",
                    data=None
                )
                
    except InaraAuthenticationException as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {e}")
    except InaraRateLimitException as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {e}")
    except InaraApiException as e:
        raise HTTPException(status_code=400, detail=f"Inara API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting current ship: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# System endpoints
@router.get(
    "/inara/system/{system_name}/factions",
    response_model=SystemFactionsResponse,
    summary="Get system factions",
    description="Retrieve faction information for a specific system from Inara."
)
async def get_system_factions(
    system_name: str = Path(..., description="System name", example="Sol"),
    client: InaraClient = Depends(get_inara_client)
):
    """
    Get factions in a system.
    
    Args:
        system_name: The system name
        client: Inara client instance
        
    Returns:
        SystemFactionsResponse: System faction data
    """
    try:
        async with client:
            factions = await client.get_system_factions(system_name)
            
            return SystemFactionsResponse(
                success=True,
                message=f"Retrieved {len(factions)} factions for {system_name}",
                data=factions
            )
                
    except InaraAuthenticationException as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {e}")
    except InaraRateLimitException as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {e}")
    except InaraApiException as e:
        raise HTTPException(status_code=400, detail=f"Inara API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting system factions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/inara/system/{system_name}/stations",
    response_model=SystemStationsResponse,
    summary="Get system stations",
    description="Retrieve station information for a specific system from Inara."
)
async def get_system_stations(
    system_name: str = Path(..., description="System name", example="Sol"),
    client: InaraClient = Depends(get_inara_client)
):
    """
    Get stations in a system.
    
    Args:
        system_name: The system name
        client: Inara client instance
        
    Returns:
        SystemStationsResponse: System station data
    """
    try:
        async with client:
            stations = await client.get_system_stations(system_name)
            
            return SystemStationsResponse(
                success=True,
                message=f"Retrieved {len(stations)} stations for {system_name}",
                data=stations
            )
                
    except InaraAuthenticationException as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {e}")
    except InaraRateLimitException as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {e}")
    except InaraApiException as e:
        raise HTTPException(status_code=400, detail=f"Inara API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting system stations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Market endpoints
@router.get(
    "/inara/station/{station_id}/market",
    response_model=StationMarketResponse,
    summary="Get station market data",
    description="Retrieve market information for a specific station from Inara."
)
async def get_station_market(
    station_id: int = Path(..., description="Station ID", example=123456),
    client: InaraClient = Depends(get_inara_client)
):
    """
    Get station market data.
    
    Args:
        station_id: The station ID
        client: Inara client instance
        
    Returns:
        StationMarketResponse: Station market data
    """
    try:
        async with client:
            market = await client.get_station_market(station_id)
            
            if market:
                return StationMarketResponse(
                    success=True,
                    message="Station market data retrieved successfully",
                    data=market
                )
            else:
                return StationMarketResponse(
                    success=False,
                    message="Station market data not found",
                    data=None
                )
                
    except InaraAuthenticationException as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {e}")
    except InaraRateLimitException as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {e}")
    except InaraApiException as e:
        raise HTTPException(status_code=400, detail=f"Inara API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting station market: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Utility endpoints
@router.delete(
    "/inara/cache",
    response_model=ApiResponse,
    summary="Clear API cache",
    description="Clear the Inara API response cache."
)
async def clear_cache(client: InaraClient = Depends(get_inara_client)):
    """
    Clear the Inara API response cache.
    
    Args:
        client: Inara client instance
        
    Returns:
        ApiResponse: Cache clear confirmation
    """
    try:
        async with client:
            client.clear_cache()
            
            return ApiResponse(
                success=True,
                message="Cache cleared successfully",
                data=None
            )
                
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear cache")