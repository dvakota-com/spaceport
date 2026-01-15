"""
Application Configuration
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SpacePort"
    API_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://localhost:5432/spaceport"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()
