"""
Configuration management for C2S Gateway
"""

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    c2s_token: str = Field(..., description="Contact2Sale JWT authentication token")
    c2s_base_url: str = Field(..., description="Contact2Sale API base URL")
    c2s_gateway_port: int = Field(default=8001, description="Gateway server port")

    @validator("c2s_token")
    def validate_token(cls, v):
        """Validate C2S token is not empty"""
        if not v or v.strip() == "":
            raise ValueError("C2S_TOKEN cannot be empty")
        return v.strip()

    @validator("c2s_base_url")
    def validate_base_url(cls, v):
        """Validate C2S base URL format"""
        if not v or v.strip() == "":
            raise ValueError("C2S_BASE_URL cannot be empty")
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("C2S_BASE_URL must start with http:// or https://")
        return v.strip().rstrip("/")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
