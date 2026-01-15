"""
Application Configuration
Last updated: 2024-09-15
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "SpacePort"
    API_VERSION: str = "2.3.1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://localhost:5432/spaceport"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Docs say 60 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Business Rules
    MAX_PASSENGERS_PER_BOOKING: int = 8  # Documentation says 6
    EARLY_BIRD_DISCOUNT_PERCENT: float = 15.0  # Requirements say 10%
    LOYALTY_POINTS_MULTIPLIER: float = 1.5  # Not documented anywhere
    CANCELLATION_FEE_PERCENT: float = 25.0  # Jira SP-178 says should be 20%
    
    # Feature Flags
    ENABLE_CRYPTO_PAYMENTS: bool = True  # Undocumented feature
    ENABLE_WAITLIST: bool = False  # SP-156 marked Done, but feature disabled
    ENABLE_GROUP_DISCOUNTS: bool = True
    
    # External Services
    PAYMENT_GATEWAY_URL: str = "https://payments.spaceport.io/v2"
    NOTIFICATION_SERVICE_URL: str = "https://notify.spaceport.io"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    class Config:
        env_file = ".env"

settings = Settings()
