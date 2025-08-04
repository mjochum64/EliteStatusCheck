"""
Pydantic models for Elite Dangerous API responses.

This module exports data models for various APIs including Inara integration.
For backward compatibility, common models are re-exported here.
"""

# Import Inara models for backward compatibility
from .inara_models import (
    # Core API models
    InaraRequest,
    InaraResponse,
    InaraEvent,
    InaraEventType,
    InaraApiHeader,
    InaraEventResponse,
    InaraError,
    
    # Commander models
    CommanderProfile,
    CommanderRanks,
    CommanderRank,
    CommanderCredits,
    
    # Ship models
    ShipLoadout,
    ShipModule,
    
    # System and station models
    SystemFaction,
    Station,
    StationMarket,
    MarketCommodity,
    
    # Utility functions
    create_inara_timestamp,
    validate_timestamp
)

# Re-export commonly used models
__all__ = [
    # Core API
    'InaraRequest',
    'InaraResponse', 
    'InaraEvent',
    'InaraEventType',
    'InaraApiHeader',
    'InaraEventResponse',
    'InaraError',
    
    # Commander
    'CommanderProfile',
    'CommanderRanks',
    'CommanderRank', 
    'CommanderCredits',
    
    # Ships
    'ShipLoadout',
    'ShipModule',
    
    # Systems and stations
    'SystemFaction',
    'Station',
    'StationMarket',
    'MarketCommodity',
    
    # Utilities
    'create_inara_timestamp',
    'validate_timestamp'
]

# Additional Elite Dangerous specific models can be added here
# These would be models for local game data, not Inara API responses
