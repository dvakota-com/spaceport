"""
Application Configuration
Last updated: 2024-07-15
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SpacePort"
    API_VERSION: str = "2.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://localhost:5432/spaceport"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Business Rules
    MAX_PASSENGERS_PER_BOOKING: int = 6
    EARLY_BIRD_DISCOUNT_PERCENT: float = 10.0
    CANCELLATION_FEE_PERCENT: float = 25.0
    
    # Feature flags
    ENABLE_WAITLIST: bool = False
    ENABLE_CRYPTO_PAYMENTS: bool = True  # Beta feature
    
    class Config:
        env_file = ".env"

settings = Settings()
