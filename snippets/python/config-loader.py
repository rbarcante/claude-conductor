"""
USE: When loading and validating configuration from environment variables
REQUIRES: pydantic>=2.0, pydantic-settings>=2.0, Python 3.10+
PATTERN: Configuration, Validation
"""

from enum import Enum
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class LogLevel(str, Enum):
    """Logging level."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# CUSTOMIZE: Define your configuration schema


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    model_config = SettingsConfigDict(env_prefix="DB_")

    url: str = Field(
        ...,
        description="Database connection URL",
        examples=["postgresql://user:pass@localhost:5432/dbname"],
    )
    pool_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Connection pool size",
    )
    pool_timeout: int = Field(
        default=30,
        ge=1,
        description="Pool connection timeout in seconds",
    )
    echo: bool = Field(
        default=False,
        description="Echo SQL statements (for debugging)",
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate database URL format."""
        valid_schemes = ("postgresql://", "mysql://", "sqlite://")
        if not any(v.startswith(scheme) for scheme in valid_schemes):
            raise ValueError(f"Database URL must start with one of: {valid_schemes}")
        return v


class RedisSettings(BaseSettings):
    """Redis configuration."""
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )
    max_connections: int = Field(
        default=10,
        ge=1,
        description="Maximum connections in pool",
    )


class ApiSettings(BaseSettings):
    """External API configuration."""
    model_config = SettingsConfigDict(env_prefix="API_")

    base_url: str = Field(
        ...,
        description="External API base URL",
    )
    timeout: int = Field(
        default=30,
        ge=1,
        description="Request timeout in seconds",
    )
    api_key: str = Field(
        default="",
        description="API key for authentication",
    )
    retry_attempts: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Number of retry attempts",
    )


class FeatureFlags(BaseSettings):
    """Feature flag configuration."""
    model_config = SettingsConfigDict(env_prefix="FEATURE_")

    new_dashboard: bool = Field(
        default=False,
        description="Enable new dashboard UI",
    )
    analytics: bool = Field(
        default=True,
        description="Enable analytics tracking",
    )
    beta_features: bool = Field(
        default=False,
        description="Enable beta features",
    )


class AppSettings(BaseSettings):
    """
    Main application configuration.

    Loads from environment variables with optional .env file support.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(
        default="MyApp",
        description="Application name",
    )
    env: Environment = Field(
        default=Environment.DEVELOPMENT,
        alias="NODE_ENV",
        description="Application environment",
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        description="Logging level",
    )

    # Server
    host: str = Field(
        default="0.0.0.0",
        description="Server bind host",
    )
    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Server bind port",
    )

    # Security
    secret_key: str = Field(
        ...,
        min_length=32,
        description="Secret key for encryption/signing",
    )
    allowed_hosts: list[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="Allowed host headers",
    )
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins",
    )

    # Nested configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    features: FeatureFlags = Field(default_factory=FeatureFlags)

    @model_validator(mode="after")
    def validate_production_settings(self) -> "AppSettings":
        """Validate settings for production environment."""
        if self.env == Environment.PRODUCTION:
            if self.debug:
                raise ValueError("Debug mode must be disabled in production")
            if len(self.secret_key) < 64:
                raise ValueError("Secret key must be at least 64 chars in production")
            if "*" in self.allowed_hosts:
                raise ValueError("Wildcard host not allowed in production")
        return self

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.env == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.env == Environment.PRODUCTION

    @property
    def is_testing(self) -> bool:
        """Check if running in test mode."""
        return self.env == Environment.TEST


@lru_cache
def get_settings() -> AppSettings:
    """
    Get cached application settings.

    Uses lru_cache to ensure settings are only loaded once.
    """
    return AppSettings()


def validate_settings() -> None:
    """
    Validate settings at startup.

    Call this early in application initialization to fail fast
    on configuration errors.
    """
    try:
        settings = get_settings()
        print(f"Configuration loaded: env={settings.env.value}, debug={settings.debug}")
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        raise SystemExit(1) from e


# CUSTOMIZE: Example usage
# from config_loader import get_settings, validate_settings
#
# # At application startup
# validate_settings()
#
# # Anywhere in your application
# settings = get_settings()
# print(f"Running on {settings.host}:{settings.port}")
# print(f"Database: {settings.database.url}")
# print(f"Feature new_dashboard: {settings.features.new_dashboard}")
