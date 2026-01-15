"""
Application Configuration
Last updated: 2024-08-10
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SpacePort"
    API_VERSION: str = "2.2.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://localhost:5432/spaceport"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Reduced for security
    
    # Business Rules
    MAX_PASSENGERS_PER_BOOKING: int = 8  # Increased per customer feedback
    EARLY_BIRD_DISCOUNT_PERCENT: float = 15.0  # Increased for summer promo
    CANCELLATION_FEE_PERCENT: float = 25.0
    LOYALTY_POINTS_MULTIPLIER: float = 1.5
    
    # Feature flags
    ENABLE_WAITLIST: bool = False
    ENABLE_CRYPTO_PAYMENTS: bool = True
    ENABLE_GROUP_DISCOUNTS: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
