"""
Application Configuration Management

This module handles all application settings using Pydantic Settings.
Settings are loaded from environment variables and .env file.
"""

from typing import List,Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Environment variables take precedence over .env file values.
    All settings are validated using Pydantic.
    """

    # ============================================
    # APPLICATION SETTINGS
    # ============================================
    APP_NAME: str = Field(
        default="DataPipeline Pro",
        description="Application name"
    )
    
    DEBUG: bool = Field(
        default=False,
        description="Debug mode - should be False in Production"
    )

    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, staging, or production"
    )
    
    API_VERSION: str = Field(
        default="v1",
        description="API version"
    )
    
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )

    # ============================================
    # DATABASE SETTINGS
    # ============================================
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/datapipeline",
        description="PostgreSQL database connection URL"
    )
    
    DB_POOL_SIZE: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Database connection pool size"
    )
    
    DB_MAX_OVERFLOW: int = Field(
        default=10,
        ge=0,
        le=50,
        description="Maximum overflow connections"
    )
    
    DB_ECHO: bool = Field(
        default=False,
        description="Echo SQL queries - useful for debugging"
    )
    
    DB_POOL_RECYCLE: int = Field(
        default=3600,
        description="Time in seconds to recycle connections"
    )

    # ============================================
    # REDIS SETTINGS
    # ============================================
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    
    REDIS_MAX_CONNECTIONS: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum Redis connections"
    )
    
    REDIS_DECODE_RESPONSES: bool = Field(
        default=True,
        description="Decode Redis responses to strings"
    )
    
    REDIS_SOCKET_TIMEOUT: int = Field(
        default=5,
        description="Redis socket timeout in seconds"
    )

    # ============================================
    # SECURITY SETTINGS
    # ============================================
    SECRET_KEY: str = Field(
        ...,  # ... means required, no default
        min_length=32,
        description="Secret key for JWT token signing - MUST be kept secret"
    )
    
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        ge=1,
        le=1440,
        description="Access token expiration time in minutes"
    )
    
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Refresh token expiration time in days"
    )
    
    BCRYPT_ROUNDS: int = Field(
        default=12,
        ge=4,
        le=31,
        description="Bcrypt hashing rounds for password encryption"
    )
    
    # ============================================
    # API SETTINGS
    # ============================================
    API_PREFIX: str = Field(
        default="/api/v1",
        description="API route prefix"
    )
    
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="Allowed host headers"
    )
    
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        ge=1,
        le=1000,
        description="API rate limit per minute per IP"
    )
    
    # ============================================
    # KAFKA SETTINGS (for later phases)
    # ============================================
    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        default="localhost:9092",
        description="Kafka bootstrap servers"
    )
    
    KAFKA_TOPIC_DATA_INGESTION: str = Field(
        default="data-ingestion",
        description="Kafka topic for data ingestion"
    )
    
    # ============================================
    # AWS SETTINGS (for later phases)
    # ============================================
    AWS_ACCESS_KEY_ID: Optional[str] = Field(
        default=None,
        description="AWS access key ID"
    )
    
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(
        default=None,
        description="AWS secret access key"
    )
    
    AWS_REGION: str = Field(
        default="us-east-1",
        description="AWS region"
    )
    
    S3_BUCKET_NAME: Optional[str] = Field(
        default=None,
        description="S3 bucket name for data storage"
    )
    
    # ============================================
    # MONITORING SETTINGS
    # ============================================
    SENTRY_DSN: Optional[str] = Field(
        default=None,
        description="Sentry DSN for error tracking"
    )
    
    ENABLE_METRICS: bool = Field(
        default=True,
        description="Enable Prometheus metrics collection"
    )
    
    # ============================================
    # VALIDATORS
    # ============================================
    @field_validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Ensure ENVIRONMENT is one of the allowed values."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v
    
    @field_validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Ensure LOG_LEVEL is valid."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v_upper
    
    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        """Ensure DATABASE_URL starts with postgresql://"""
        if not v.startswith("postgresql://") and not v.startswith("postgres://"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v
    
    @field_validator("REDIS_URL")
    def validate_redis_url(cls, v):
        """Ensure REDIS_URL starts with redis://"""
        if not v.startswith("redis://"):
            raise ValueError("REDIS_URL must start with redis://")
        return v
    
    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Ensure SECRET_KEY is sufficiently strong."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        if v == "your-secret-key-here-change-in-production":
            raise ValueError("You must change the default SECRET_KEY!")
        return v
    
    # ============================================
    # COMPUTED PROPERTIES
    # ============================================
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"
    
    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL (for SQLAlchemy)."""
        return self.DATABASE_URL
    
    @property
    def database_url_async(self) -> str:
        """Get async database URL (for async SQLAlchemy)."""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    # ============================================
    # PYDANTIC CONFIGURATION
    # ============================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields in .env
        validate_default=True
    )
    
    def get_database_settings(self) -> dict:
        """Get database configuration as dictionary."""
        return {
            "url": self.DATABASE_URL,
            "pool_size": self.DB_POOL_SIZE,
            "max_overflow": self.DB_MAX_OVERFLOW,
            "echo": self.DB_ECHO,
            "pool_recycle": self.DB_POOL_RECYCLE,
        }
    
    def get_redis_settings(self) -> dict:
        """Get Redis configuration as dictionary."""
        return {
            "url": self.REDIS_URL,
            "max_connections": self.REDIS_MAX_CONNECTIONS,
            "decode_responses": self.REDIS_DECODE_RESPONSES,
            "socket_timeout": self.REDIS_SOCKET_TIMEOUT,
        }
    
    # class Config:
    #     """Pydantic configuration (for backwards compatibility)."""
    #     case_sensitive = True


# ============================================
# SETTINGS INSTANCE (SINGLETON PATTERN)
# ============================================
@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    
    Uses lru_cache to ensure only one instance is created (singleton pattern).
    This is efficient and allows for easy dependency injection in FastAPI.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Create global settings instance for convenience
settings = get_settings()
