from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str
    
    # API Keys
    ANTHROPIC_API_KEY: str
    LOB_API_KEY: str
    
    # Application
    APP_NAME: str = "DepositGuard AI"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Model Configuration
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
