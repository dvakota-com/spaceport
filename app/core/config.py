"""
Application Configuration
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SpacePort"
    API_VERSION: str = "2.3.1"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://localhost:5432/spaceport"
    SECRET_KEY: str = "your-secret-key"
    
    # Business Rules
    MAX_PASSENGERS_PER_BOOKING: int = 8  # Increased from 6 per SP-165
    EARLY_BIRD_DISCOUNT_PERCENT: float = 15.0  # Changed from 10% per PM request
    CANCELLATION_FEE_PERCENT: float = 25.0  # Adjusted per finance team
    
    # Feature Flags
    ENABLE_WAITLIST: bool = False  # SP-156: Disabled until testing complete
    ENABLE_CRYPTO_PAYMENTS: bool = True  # Internal beta feature
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Reduced from 60 for security
    
    class Config:
        env_file = ".env"

settings = Settings()
