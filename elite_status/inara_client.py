"""
Inara API Client

This module provides a comprehensive client for interacting with the Inara API,
including authentication, error handling, retry logic, and caching.
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta

import httpx
from pydantic import ValidationError

from .inara_config import get_config, InaraConfig
from .inara_models import (
    InaraRequest, InaraResponse, InaraApiHeader, InaraEvent,
    InaraEventType, InaraError, InaraErrorResponse, CommanderProfile, ShipLoadout,
    SystemFaction, Station, StationMarket, create_inara_timestamp
)


class InaraApiException(Exception):
    """Base exception for Inara API errors."""
    
    def __init__(self, message: str, error_code: Optional[int] = None, error_data: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.error_data = error_data


class InaraRateLimitException(InaraApiException):
    """Exception raised when rate limit is exceeded."""
    pass


class InaraAuthenticationException(InaraApiException):
    """Exception raised for authentication errors."""
    pass


class InaraClient:
    """
    Inara API client with authentication, retry logic, and caching.
    """
    
    def __init__(self, config: Optional[InaraConfig] = None, commander_name: Optional[str] = None):
        """
        Initialize Inara API client.
        
        Args:
            config: Configuration instance (uses global config if None)
            commander_name: Commander name for API requests
        """
        self.config = config or get_config()
        self.commander_name = commander_name
        self.logger = logging.getLogger(__name__)
        
        # HTTP client setup
        self.client = httpx.AsyncClient(
            timeout=self.config.timeout,
            headers={
                'User-Agent': f'{self.config.app_name}/{self.config.app_version}',
                'Content-Type': 'application/json'
            }
        )
        
        # Rate limiting
        self._request_times: List[float] = []
        self._rate_limit_lock = asyncio.Lock()
        
        # Caching
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_enabled = self.config.cache_enabled
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    def _create_header(self, commander_name: Optional[str] = None) -> InaraApiHeader:
        """
        Create API request header.
        
        Args:
            commander_name: Override commander name
            
        Returns:
            InaraApiHeader: Request header
        """
        return InaraApiHeader(
            appName=self.config.app_name,
            appVersion=self.config.app_version,
            isDeveloped=True,
            APIkey=self.config.api_key,
            commanderName=commander_name or self.commander_name
        )
    
    def _create_event(self, event_type: InaraEventType, event_data: Optional[Dict] = None, 
                     custom_id: Optional[int] = None) -> InaraEvent:
        """
        Create API event.
        
        Args:
            event_type: Type of event
            event_data: Event data payload
            custom_id: Custom event ID
            
        Returns:
            InaraEvent: API event
        """
        return InaraEvent(
            eventName=event_type,
            eventTimestamp=create_inara_timestamp(),
            eventData=event_data,
            eventCustomID=custom_id
        )
    
    async def _check_rate_limit(self):
        """Check and enforce rate limiting."""
        async with self._rate_limit_lock:
            now = time.time()
            window_start = now - self.config.rate_limit_window
            
            # Remove old requests
            self._request_times = [t for t in self._request_times if t > window_start]
            
            if len(self._request_times) >= self.config.rate_limit_requests:
                sleep_time = self._request_times[0] + self.config.rate_limit_window - now
                if sleep_time > 0:
                    self.logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                    await asyncio.sleep(sleep_time)
            
            self._request_times.append(now)
    
    def _get_cache_key(self, request: InaraRequest) -> str:
        """
        Generate cache key for request.
        
        Args:
            request: API request
            
        Returns:
            str: Cache key
        """
        events_data = [(e.eventName, e.eventData) for e in request.events]
        return f"{request.header.commanderName}:{hash(str(events_data))}"
    
    def _is_cached(self, cache_key: str) -> bool:
        """
        Check if response is cached and valid.
        
        Args:
            cache_key: Cache key
            
        Returns:
            bool: True if cached and valid
        """
        if not self._cache_enabled or cache_key not in self._cache:
            return False
        
        cached_data = self._cache[cache_key]
        cache_time = cached_data.get('timestamp', 0)
        return time.time() - cache_time < self.config.cache_ttl
    
    def _get_cached(self, cache_key: str) -> Optional[InaraResponse]:
        """
        Get cached response.
        
        Args:
            cache_key: Cache key
            
        Returns:
            Optional[InaraResponse]: Cached response if available
        """
        if not self._is_cached(cache_key):
            return None
        
        try:
            return InaraResponse(**self._cache[cache_key]['data'])
        except (KeyError, ValidationError) as e:
            self.logger.warning(f"Invalid cached data: {e}")
            return None
    
    def _set_cache(self, cache_key: str, response: InaraResponse):
        """
        Cache response.
        
        Args:
            cache_key: Cache key
            response: Response to cache
        """
        if not self._cache_enabled:
            return
        
        # Handle both Pydantic v1 and v2 compatibility for caching
        try:
            # Pydantic v2
            response_data = response.model_dump()
        except AttributeError:
            # Pydantic v1
            response_data = response.dict()
            
        self._cache[cache_key] = {
            'timestamp': time.time(),
            'data': response_data
        }
    
    async def _make_request(self, request: InaraRequest, retry_count: int = 0) -> InaraResponse:
        """
        Make HTTP request to Inara API.
        
        Args:
            request: API request
            retry_count: Current retry attempt
            
        Returns:
            InaraResponse: API response
            
        Raises:
            InaraApiException: On API errors
            InaraRateLimitException: On rate limit errors
            InaraAuthenticationException: On authentication errors
        """
        # Check cache first
        cache_key = self._get_cache_key(request)
        cached_response = self._get_cached(cache_key)
        if cached_response:
            self.logger.debug(f"Using cached response for {cache_key}")
            return cached_response
        
        # Rate limiting
        await self._check_rate_limit()
        
        try:
            self.logger.debug(f"Making request to Inara API: {[e.eventName for e in request.events]}")
            
            # Handle both Pydantic v1 and v2 compatibility
            try:
                # Pydantic v2
                request_data = request.model_dump()
            except AttributeError:
                # Pydantic v1
                request_data = request.dict()
            
            response = await self.client.post(
                self.config.base_url,
                content=json.dumps(request_data, default=str),
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 429:  # Rate limit
                raise InaraRateLimitException("Rate limit exceeded")
            
            response.raise_for_status()
            response_data = response.json()
            
            # Check if this is an error response format
            if ('header' in response_data and 
                'eventStatus' in response_data['header'] and 
                'events' not in response_data):
                # This is an error response with simplified format
                error_response = InaraErrorResponse(**response_data)
                error_code = error_response.header.eventStatus
                error_message = error_response.header.eventStatusText
                
                if error_code == 400:
                    raise InaraAuthenticationException(
                        f"Authentication/Authorization failed: {error_message}",
                        error_code=error_code
                    )
                else:
                    raise InaraApiException(
                        f"API error: {error_message}",
                        error_code=error_code
                    )
            
            # Parse normal response
            inara_response = InaraResponse(**response_data)
            
            # Check for API errors
            for event in inara_response.events:
                if event.eventStatus >= 200:  # Inara error codes
                    if event.eventStatus == 202:  # Authentication error
                        raise InaraAuthenticationException(
                            f"Authentication failed: {event.eventStatusText}",
                            error_code=event.eventStatus
                        )
                    elif event.eventStatus >= 400:  # Client error
                        raise InaraApiException(
                            f"API error: {event.eventStatusText}",
                            error_code=event.eventStatus
                        )
                    else:  # Warning
                        self.logger.warning(f"API warning: {event.eventStatusText}")
            
            # Cache successful response
            self._set_cache(cache_key, inara_response)
            
            return inara_response
            
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
            
            if e.response.status_code == 401:
                raise InaraAuthenticationException(error_msg)
            elif e.response.status_code == 429:
                raise InaraRateLimitException(error_msg)
            else:
                raise InaraApiException(error_msg)
                
        except httpx.RequestError as e:
            if retry_count < self.config.max_retries:
                delay = self.config.retry_delay * (self.config.backoff_factor ** retry_count)
                self.logger.warning(f"Request failed, retrying in {delay}s: {e}")
                await asyncio.sleep(delay)
                return await self._make_request(request, retry_count + 1)
            else:
                raise InaraApiException(f"Request failed after {self.config.max_retries} retries: {e}")
        
        except Exception as e:
            raise InaraApiException(f"Unexpected error: {e}")
    
    async def send_events(self, events: List[InaraEvent], commander_name: Optional[str] = None) -> InaraResponse:
        """
        Send events to Inara API.
        
        Args:
            events: List of events to send
            commander_name: Override commander name
            
        Returns:
            InaraResponse: API response
        """
        header = self._create_header(commander_name)
        request = InaraRequest(header=header, events=events)
        return await self._make_request(request)
    
    async def get_commander_profile(self, commander_name: Optional[str] = None) -> Optional[CommanderProfile]:
        """
        Get commander profile information.
        
        Args:
            commander_name: Commander name (uses instance default if None)
            
        Returns:
            Optional[CommanderProfile]: Commander profile data
        """
        event = self._create_event(InaraEventType.GET_COMMANDER_PROFILE)
        response = await self.send_events([event], commander_name)
        
        if response.events and response.events[0].eventData:
            try:
                return CommanderProfile(**response.events[0].eventData)
            except ValidationError as e:
                self.logger.error(f"Failed to parse commander profile: {e}")
                return None
        
        return None
    
    async def get_commander_ships(self, commander_name: Optional[str] = None) -> List[ShipLoadout]:
        """
        Get commander's ships.
        
        Args:
            commander_name: Commander name (uses instance default if None)
            
        Returns:
            List[ShipLoadout]: List of ships
        """
        event = self._create_event(InaraEventType.GET_COMMANDER_SHIPS)
        response = await self.send_events([event], commander_name)
        
        ships = []
        if response.events and response.events[0].eventData:
            try:
                ships_data = response.events[0].eventData.get('ships', [])
                for ship_data in ships_data:
                    ships.append(ShipLoadout(**ship_data))
            except ValidationError as e:
                self.logger.error(f"Failed to parse ships: {e}")
        
        return ships
    
    async def get_current_ship(self, commander_name: Optional[str] = None) -> Optional[ShipLoadout]:
        """
        Get commander's current ship.
        
        Args:
            commander_name: Commander name (uses instance default if None)
            
        Returns:
            Optional[ShipLoadout]: Current ship data
        """
        ships = await self.get_commander_ships(commander_name)
        for ship in ships:
            if ship.isCurrentShip:
                return ship
        return None
    
    async def get_system_factions(self, system_name: str) -> List[SystemFaction]:
        """
        Get factions in a system.
        
        Args:
            system_name: System name
            
        Returns:
            List[SystemFaction]: List of factions
        """
        event_data = {"systemName": system_name}
        event = self._create_event(InaraEventType.GET_SYSTEM_FACTIONS, event_data)
        response = await self.send_events([event])
        
        factions = []
        if response.events and response.events[0].eventData:
            try:
                factions_data = response.events[0].eventData.get('factions', [])
                for faction_data in factions_data:
                    factions.append(SystemFaction(**faction_data))
            except ValidationError as e:
                self.logger.error(f"Failed to parse system factions: {e}")
        
        return factions
    
    async def get_system_stations(self, system_name: str) -> List[Station]:
        """
        Get stations in a system.
        
        Args:
            system_name: System name
            
        Returns:
            List[Station]: List of stations
        """
        event_data = {"systemName": system_name}
        event = self._create_event(InaraEventType.GET_SYSTEM_STATIONS, event_data)
        response = await self.send_events([event])
        
        stations = []
        if response.events and response.events[0].eventData:
            try:
                stations_data = response.events[0].eventData.get('stations', [])
                for station_data in stations_data:
                    stations.append(Station(**station_data))
            except ValidationError as e:
                self.logger.error(f"Failed to parse system stations: {e}")
        
        return stations
    
    async def get_station_market(self, station_id: int) -> Optional[StationMarket]:
        """
        Get station market data.
        
        Args:
            station_id: Station ID
            
        Returns:
            Optional[StationMarket]: Station market data
        """
        event_data = {"stationID": station_id}
        event = self._create_event(InaraEventType.GET_STATION_MARKET, event_data)
        response = await self.send_events([event])
        
        if response.events and response.events[0].eventData:
            try:
                return StationMarket(**response.events[0].eventData)
            except ValidationError as e:
                self.logger.error(f"Failed to parse station market: {e}")
                return None
        
        return None
    
    def clear_cache(self):
        """Clear response cache."""
        self._cache.clear()
        self.logger.info("Cache cleared")


# Convenience functions
async def get_client(commander_name: Optional[str] = None) -> InaraClient:
    """
    Get configured Inara client.
    
    Args:
        commander_name: Commander name for requests
        
    Returns:
        InaraClient: Configured client instance
    """
    return InaraClient(commander_name=commander_name)