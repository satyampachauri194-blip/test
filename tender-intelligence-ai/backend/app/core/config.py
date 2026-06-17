"""
Configuration management for the application.
Loads environment variables and provides type-safe configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional, List
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    APP_NAME: str = Field(default="Tender Intelligence AI", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(default="development", description="Environment (development, staging, production)")
    API_PREFIX: str = Field(default="/api/v1", description="API prefix")

    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=4, description="Number of workers")
    RELOAD: bool = Field(default=False, description="Auto reload")

    # Database - PostgreSQL
    DATABASE_URL: str = Field(..., description="PostgreSQL connection URL")
    DB_POOL_SIZE: int = Field(default=10, description="Database pool size")
    DB_MAX_OVERFLOW: int = Field(default=20, description="Database max overflow")
    DB_POOL_TIMEOUT: int = Field(default=30, description="Database pool timeout")
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")
    REDIS_DB: int = Field(default=0, description="Redis database number")

    # Elasticsearch
    ELASTICSEARCH_URL: str = Field(default="http://localhost:9200", description="Elasticsearch URL")
    ELASTICSEARCH_INDEX: str = Field(default="tenders", description="Elasticsearch index name")

    # Security
    SECRET_KEY: str = Field(..., description="Secret key for JWT")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiry")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiry")

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Allow credentials")
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"], description="Allowed methods")
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"], description="Allowed headers")

    # Rate Limiting
    RATE_LIMIT_PER_SECOND: int = Field(default=10, description="Rate limit per second")
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, description="Rate limit per minute")

    # Storage - S3/R2
    STORAGE_PROVIDER: str = Field(default="aws", description="Storage provider (aws, cloudflare)")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS access key")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS secret key")
    AWS_REGION: str = Field(default="ap-south-1", description="AWS region")
    AWS_S3_BUCKET: str = Field(default="tender-intelligence-ai", description="S3 bucket name")
    CLOUDFLARE_ACCOUNT_ID: Optional[str] = Field(default=None, description="Cloudflare account ID")
    CLOUDFLARE_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="Cloudflare access key")
    CLOUDFLARE_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="Cloudflare secret key")
    CLOUDFLARE_R2_BUCKET: Optional[str] = Field(default=None, description="R2 bucket name")

    # Payments - Razorpay
    RAZORPAY_KEY_ID: Optional[str] = Field(default=None, description="Razorpay key ID")
    RAZORPAY_KEY_SECRET: Optional[str] = Field(default=None, description="Razorpay key secret")
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = Field(default=None, description="Razorpay webhook secret")

    # Payments - Stripe
    STRIPE_SECRET_KEY: Optional[str] = Field(default=None, description="Stripe secret key")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = Field(default=None, description="Stripe publishable key")
    STRIPE_WEBHOOK_SECRET: Optional[str] = Field(default=None, description="Stripe webhook secret")

    # Email
    SMTP_HOST: str = Field(default="smtp.sendgrid.net", description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USERNAME: str = Field(default="apikey", description="SMTP username")
    SMTP_PASSWORD: str = Field(..., description="SMTP password/API key")
    EMAIL_FROM: str = Field(default="noreply@tenderintelligence.ai", description="From email")
    EMAIL_SUPPORT: str = Field(default="support@tenderintelligence.ai", description="Support email")

    # SMS - MSG91/Twilio
    SMS_PROVIDER: str = Field(default="msg91", description="SMS provider")
    MSG91_AUTHKEY: Optional[str] = Field(default=None, description="MSG91 auth key")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, description="Twilio account SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, description="Twilio auth token")
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None, description="Twilio phone number")

    # WhatsApp
    WHATSAPP_API_KEY: Optional[str] = Field(default=None, description="WhatsApp API key")
    WHATSAPP_PHONE_ID: Optional[str] = Field(default=None, description="WhatsApp phone ID")

    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, description="Telegram bot token")

    # Celery
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1", description="Celery broker URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/1", description="Celery result backend")

    # Scraper
    SCRAPER_PROXY_LIST: List[str] = Field(default=[], description="List of proxy URLs")
    SCRAPER_TIMEOUT: int = Field(default=30, description="Scraper timeout in seconds")
    SCRAPER_MAX_RETRIES: int = Field(default=3, description="Maximum retry attempts")
    PLAYWRIGHT_HEADLESS: bool = Field(default=True, description="Playwright headless mode")

    # AI/ML
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    AI_MODEL: str = Field(default="gpt-4o-mini", description="AI model to use")
    AI_MAX_TOKENS: int = Field(default=2000, description="Max tokens for AI response")

    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN")
    PROMETHEUS_ENABLED: bool = Field(default=True, description="Enable Prometheus metrics")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format (json, text)")

    @field_validator("DATABASE_URL", "SECRET_KEY", "SMTP_PASSWORD")
    @classmethod
    def validate_required_fields(cls, v: str, info) -> str:
        if not v and os.getenv("ENVIRONMENT") == "production":
            raise ValueError(f"{info.field_name} is required in production")
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def storage_bucket(self) -> str:
        if self.STORAGE_PROVIDER == "cloudflare" and self.CLOUDFLARE_R2_BUCKET:
            return self.CLOUDFLARE_R2_BUCKET
        return self.AWS_S3_BUCKET


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export settings instance
settings = get_settings()
