"""
Application Configuration
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SpacePort"
    API_VERSION: str = "2.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://localhost:5432/spaceport"
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Business Rules (per PRD-2024-Q1)
    MAX_PASSENGERS_PER_BOOKING: int = 6
    EARLY_BIRD_DISCOUNT_PERCENT: float = 10.0
    CANCELLATION_FEE_PERCENT: float = 20.0
    
    class Config:
        env_file = ".env"

settings = Settings()
