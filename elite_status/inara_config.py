"""
Inara API Configuration Management

This module handles configuration settings for the Inara API integration,
including API keys, endpoints, and request parameters.
"""

import os
from typing import Optional
try:
    # Pydantic v2
    from pydantic import Field, field_validator
    from pydantic_settings import BaseSettings
    PYDANTIC_V2 = True
except ImportError:
    try:
        # Pydantic v1
        from pydantic import Field, validator as field_validator, BaseSettings
        PYDANTIC_V2 = False
    except ImportError:
        # Fallback
        from pydantic import Field
        from pydantic_settings import BaseSettings
        try:
            from pydantic import field_validator
            PYDANTIC_V2 = True
        except ImportError:
            from pydantic import validator as field_validator
            PYDANTIC_V2 = False


class InaraConfig(BaseSettings):
    """Configuration settings for Inara API integration."""
    
    # API Credentials
    api_key: str = Field(..., description="Inara API key")
    app_name: str = Field(default="EliteStatusCheck", description="Application name for API identification")
    app_version: str = Field(default="1.1.0", description="Application version")
    
    # API Endpoints
    base_url: str = Field(default="https://inara.cz/inapi/v1/", description="Inara API base URL")
    
    # Request Configuration
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    retry_delay: float = Field(default=1.0, description="Delay between retries in seconds")
    backoff_factor: float = Field(default=2.0, description="Exponential backoff factor")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Maximum requests per hour")
    rate_limit_window: int = Field(default=3600, description="Rate limit window in seconds")
    
    # Caching
    cache_enabled: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds (5 minutes default)")
    
    class Config:
        env_prefix = "INARA_"
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"
    
    if PYDANTIC_V2:
        @field_validator('api_key')
        @classmethod
        def validate_api_key(cls, v):
            if not v or v.strip() == "":
                raise ValueError("Inara API key is required")
            return v.strip()
        
        @field_validator('timeout')
        @classmethod
        def validate_timeout(cls, v):
            if v <= 0:
                raise ValueError("Timeout must be positive")
            return v
        
        @field_validator('max_retries')
        @classmethod
        def validate_max_retries(cls, v):
            if v < 0:
                raise ValueError("Max retries cannot be negative")
            return v
    else:
        @field_validator('api_key')
        @classmethod
        def validate_api_key(cls, v):
            if not v or v.strip() == "":
                raise ValueError("Inara API key is required")
            return v.strip()
        
        @field_validator('timeout')
        @classmethod
        def validate_timeout(cls, v):
            if v <= 0:
                raise ValueError("Timeout must be positive")
            return v
        
        @field_validator('max_retries')
        @classmethod
        def validate_max_retries(cls, v):
            if v < 0:
                raise ValueError("Max retries cannot be negative")
            return v


def get_inara_config() -> InaraConfig:
    """
    Get Inara API configuration.
    
    Returns:
        InaraConfig: Configuration instance
        
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    try:
        return InaraConfig()
    except Exception as e:
        raise ValueError(f"Failed to load Inara configuration: {e}")


def validate_config() -> bool:
    """
    Validate Inara API configuration.
    
    Returns:
        bool: True if configuration is valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    try:
        config = get_inara_config()
        return True
    except Exception as e:
        raise ValueError(f"Invalid Inara configuration: {e}")


# Global configuration instance (lazy loaded)
_config: Optional[InaraConfig] = None


def get_config() -> InaraConfig:
    """
    Get cached configuration instance.
    
    Returns:
        InaraConfig: Cached configuration instance
    """
    global _config
    if _config is None:
        _config = get_inara_config()
    return _config