"""
Mock Inara API client for testing without valid API key.
"""

from typing import List, Optional, Dict, Any
import logging
from .inara_models import (
    InaraResponse, InaraEventResponse, InaraApiHeader, 
    SystemFaction, Station, CommanderProfile, ShipLoadout, StationMarket
)


class MockInaraClient:
    """Mock Inara client for testing purposes."""
    
    def __init__(self, commander_name: Optional[str] = None):
        self.commander_name = commander_name
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def close(self):
        pass
    
    async def get_system_factions(self, system_name: str) -> List[SystemFaction]:
        """Mock system factions data."""
        self.logger.info(f"Mock: Getting factions for system {system_name}")
        
        # Mock faction data
        mock_factions = [
            SystemFaction(
                factionName="Federal Congress",
                factionGovernment="Democracy",
                factionAllegiance="Federation",
                factionState="None",
                factionInfluence=0.45,
                factionHappiness="Happy",
                isControllingFaction=True
            ),
            SystemFaction(
                factionName="Sol Workers' Party",
                factionGovernment="Democracy",
                factionAllegiance="Federation",
                factionState="None",
                factionInfluence=0.35,
                factionHappiness="Happy",
                isControllingFaction=False
            ),
            SystemFaction(
                factionName="Independent Pilots Federation",
                factionGovernment="Cooperative",
                factionAllegiance="Independent",
                factionState="None",
                factionInfluence=0.20,
                factionHappiness="Content",
                isControllingFaction=False
            )
        ]
        
        return mock_factions
    
    async def get_system_stations(self, system_name: str) -> List[Station]:
        """Mock system stations data."""
        self.logger.info(f"Mock: Getting stations for system {system_name}")
        
        mock_stations = [
            Station(
                stationID=1,
                stationName="Abraham Lincoln",
                stationType="Orbis Starport",
                controllingFaction="Federal Congress",
                stationServices=["Commodities", "Shipyard", "Outfitting", "Repair"],
                stationEconomy="Industrial",
                stationEconomySecond="Refinery",
                stationGovernment="Democracy",
                distanceToArrival=496.0,
                stationAllegiance="Federation",
                stationState="None",
                marketUpdated="2024-01-01T12:00:00Z",
                shipyardUpdated="2024-01-01T12:00:00Z",
                outfittingUpdated="2024-01-01T12:00:00Z"
            )
        ]
        
        return mock_stations
    
    async def get_commander_profile(self, commander_name: Optional[str] = None) -> Optional[CommanderProfile]:
        """Mock commander profile."""
        self.logger.info(f"Mock: Getting commander profile for {commander_name or self.commander_name}")
        return None  # Not implemented in mock
    
    async def get_commander_ships(self, commander_name: Optional[str] = None) -> List[ShipLoadout]:
        """Mock commander ships."""
        self.logger.info(f"Mock: Getting commander ships for {commander_name or self.commander_name}")
        return []  # Not implemented in mock
    
    async def get_current_ship(self, commander_name: Optional[str] = None) -> Optional[ShipLoadout]:
        """Mock current ship."""
        self.logger.info(f"Mock: Getting current ship for {commander_name or self.commander_name}")
        return None  # Not implemented in mock
    
    async def get_station_market(self, station_id: int) -> Optional[StationMarket]:
        """Mock station market."""
        self.logger.info(f"Mock: Getting market for station {station_id}")
        return None  # Not implemented in mock


async def get_mock_client(commander_name: Optional[str] = None) -> MockInaraClient:
    """Get mock Inara client for testing."""
    return MockInaraClient(commander_name=commander_name)