"""
Pydantic models for Inara API responses.

This module defines data models for various Inara API endpoints including
commander profiles, ship information, faction data, and system information.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum


class InaraEventType(str, Enum):
    """Inara API event types."""
    GET_COMMANDER_PROFILE = "getCommanderProfile"
    GET_COMMANDER_SHIP = "getCommanderShip"
    GET_COMMANDER_SHIPS = "getCommanderShips"
    GET_COMMANDER_CREDITS = "getCommanderCredits"
    GET_COMMANDER_RANKS = "getCommanderRanks"
    GET_COMMANDER_REPUTATION = "getCommanderReputation"
    GET_SYSTEM_STATIONS = "getSystemStations"
    GET_SYSTEM_FACTIONS = "getSystemFactions"
    GET_STATION_MARKET = "getStationMarket"
    SET_COMMANDER_TRAVEL_DOCK = "setCommanderTravelDock"
    SET_COMMANDER_TRAVEL_JUMP = "setCommanderTravelJump"


class InaraApiHeader(BaseModel):
    """Inara API request/response header."""
    appName: str = Field(..., description="Application name")
    appVersion: str = Field(..., description="Application version")
    isDeveloped: bool = Field(default=True, description="Development flag")
    APIkey: str = Field(..., description="API key")
    commanderName: Optional[str] = Field(None, description="Commander name")
    commanderFrontierID: Optional[str] = Field(None, description="Commander Frontier ID")


class InaraEvent(BaseModel):
    """Inara API event structure."""
    eventName: InaraEventType = Field(..., description="Event type")
    eventTimestamp: str = Field(..., description="Event timestamp in ISO format")
    eventData: Optional[Dict[str, Any]] = Field(None, description="Event data")
    eventCustomID: Optional[int] = Field(None, description="Custom event ID")


class InaraRequest(BaseModel):
    """Inara API request structure."""
    header: InaraApiHeader = Field(..., description="Request header")
    events: List[InaraEvent] = Field(..., description="List of events")


class InaraEventResponse(BaseModel):
    """Individual event response from Inara API."""
    eventStatus: int = Field(..., description="Event status code")
    eventStatusText: str = Field(..., description="Event status message")
    eventData: Optional[Dict[str, Any]] = Field(None, description="Response data")
    eventCustomID: Optional[int] = Field(None, description="Custom event ID")


class InaraResponse(BaseModel):
    """Inara API response structure."""
    header: InaraApiHeader = Field(..., description="Response header")
    events: List[InaraEventResponse] = Field(..., description="Event responses")


# Commander Profile Models
class CommanderRank(BaseModel):
    """Commander rank information."""
    rankName: str = Field(..., description="Rank name")
    rankValue: int = Field(..., description="Rank value")
    rankProgress: float = Field(..., description="Progress to next rank (0-100)")


class CommanderRanks(BaseModel):
    """All commander ranks."""
    combat: CommanderRank = Field(..., description="Combat rank")
    trade: CommanderRank = Field(..., description="Trade rank")
    explore: CommanderRank = Field(..., description="Exploration rank")
    soldier: CommanderRank = Field(..., description="Soldier rank")
    exobiologist: CommanderRank = Field(..., description="Exobiologist rank")
    cqc: CommanderRank = Field(..., description="CQC rank")
    federation: CommanderRank = Field(..., description="Federation rank")
    empire: CommanderRank = Field(..., description="Empire rank")
    powerplay: Optional[CommanderRank] = Field(None, description="Powerplay rank")


class CommanderCredits(BaseModel):
    """Commander credits information."""
    balance: int = Field(..., description="Current credit balance")
    loan: int = Field(default=0, description="Current loan amount")


class CommanderProfile(BaseModel):
    """Commander profile information."""
    userID: int = Field(..., description="Inara user ID")
    userName: str = Field(..., description="Inara username")
    commanderName: str = Field(..., description="Commander name")
    commanderRanksPilot: CommanderRanks = Field(..., description="Pilot ranks")
    commanderCredits: CommanderCredits = Field(..., description="Credits information")
    preferredAllegianceName: Optional[str] = Field(None, description="Preferred allegiance")
    preferredPowerName: Optional[str] = Field(None, description="Preferred power")
    inGameLocation: Optional[Dict[str, str]] = Field(None, description="Current in-game location")
    avatarImageURL: Optional[str] = Field(None, description="Avatar image URL")
    profileCreated: str = Field(..., description="Profile creation date")
    profileLastUpdate: str = Field(..., description="Profile last update")


# Ship Models
class ShipModule(BaseModel):
    """Ship module information."""
    itemName: str = Field(..., description="Module name")
    itemValue: int = Field(..., description="Module value")
    isOn: bool = Field(default=True, description="Module power status")
    itemPriority: int = Field(default=1, description="Module priority")
    itemAmmoClip: Optional[int] = Field(None, description="Ammo clip size")
    itemAmmoHopper: Optional[int] = Field(None, description="Ammo hopper size")
    itemHealth: float = Field(default=1.0, description="Module health (0-1)")
    slotName: str = Field(..., description="Slot name")
    itemModifications: Optional[List[Dict[str, Any]]] = Field(None, description="Module modifications")


class ShipLoadout(BaseModel):
    """Ship loadout information."""
    shipType: str = Field(..., description="Ship type")
    shipGameID: int = Field(..., description="Ship game ID")
    shipName: Optional[str] = Field(None, description="Ship name")
    shipIdent: Optional[str] = Field(None, description="Ship identifier")
    isCurrentShip: bool = Field(default=False, description="Is current active ship")
    shipValue: int = Field(..., description="Ship total value")
    shipHullValue: int = Field(..., description="Ship hull value")
    shipModulesValue: int = Field(..., description="Ship modules value")
    shipRebuyCost: int = Field(..., description="Ship rebuy cost")
    modules: List[ShipModule] = Field(default_factory=list, description="Ship modules")
    shipLastUpdate: str = Field(..., description="Last update timestamp")


# System and Station Models
class SystemFaction(BaseModel):
    """System faction information."""
    factionName: str = Field(..., description="Faction name")
    factionGovernment: str = Field(..., description="Faction government type")
    factionAllegiance: str = Field(..., description="Faction allegiance")
    factionState: str = Field(..., description="Faction state")
    factionInfluence: float = Field(..., description="Faction influence (0-1)")
    factionHappiness: Optional[str] = Field(None, description="Faction happiness level")
    isControllingFaction: bool = Field(default=False, description="Is controlling faction")


class Station(BaseModel):
    """Station information."""
    stationID: int = Field(..., description="Station ID")
    stationName: str = Field(..., description="Station name")
    stationType: str = Field(..., description="Station type")
    controllingFaction: str = Field(..., description="Controlling faction")
    stationServices: List[str] = Field(default_factory=list, description="Available services")
    stationEconomy: str = Field(..., description="Station economy type")
    stationEconomySecond: Optional[str] = Field(None, description="Secondary economy type")
    stationGovernment: str = Field(..., description="Station government")
    distanceToArrival: float = Field(..., description="Distance to arrival in LS")
    stationAllegiance: str = Field(..., description="Station allegiance")
    stationState: str = Field(..., description="Station state")
    marketUpdated: Optional[str] = Field(None, description="Market data last update")
    shipyardUpdated: Optional[str] = Field(None, description="Shipyard data last update")
    outfittingUpdated: Optional[str] = Field(None, description="Outfitting data last update")


# Market Models
class MarketCommodity(BaseModel):
    """Market commodity information."""
    commodityName: str = Field(..., description="Commodity name")
    meanPrice: int = Field(..., description="Mean galactic price")
    buyPrice: int = Field(..., description="Buy price at station")
    sellPrice: int = Field(..., description="Sell price at station")
    stock: int = Field(..., description="Available stock")
    stockBracket: int = Field(..., description="Stock bracket (0-3)")
    demand: int = Field(..., description="Demand")
    demandBracket: int = Field(..., description="Demand bracket (0-3)")


class StationMarket(BaseModel):
    """Station market information."""
    stationID: int = Field(..., description="Station ID")
    marketCommodities: List[MarketCommodity] = Field(default_factory=list, description="Market commodities")
    marketLastUpdate: str = Field(..., description="Market last update timestamp")


# Error Models
class InaraError(BaseModel):
    """Inara API error information."""
    errorCode: int = Field(..., description="Error code")
    errorText: str = Field(..., description="Error message")
    errorData: Optional[Dict[str, Any]] = Field(None, description="Additional error data")


class InaraErrorHeader(BaseModel):
    """Inara API error header (simplified header for error responses)."""
    eventStatus: int = Field(..., description="Event status code")
    eventStatusText: str = Field(..., description="Event status message")


class InaraErrorResponse(BaseModel):
    """Inara API error response structure (simplified response for errors)."""
    header: InaraErrorHeader = Field(..., description="Error header")


# Utility functions for model validation
def validate_timestamp(timestamp: str) -> bool:
    """
    Validate ISO timestamp format.
    
    Args:
        timestamp: Timestamp string to validate
        
    Returns:
        bool: True if valid
    """
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def create_inara_timestamp() -> str:
    """
    Create Inara API compatible timestamp.
    
    Returns:
        str: ISO format timestamp
    """
    return datetime.utcnow().isoformat() + 'Z'