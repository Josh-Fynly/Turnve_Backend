"""
Application configuration using Pydantic v2 settings.
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(alias="APP_NAME")
    environment: str = Field(alias="ENVIRONMENT")
    debug: bool = Field(alias="DEBUG")

    # Database
    database_url: str = Field(alias="DATABASE_URL")
    database_url_sync: str = Field(alias="DATABASE_URL_SYNC")

    # Security
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # AI Providers
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    gemini_api_key: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")
    groq_api_key: Optional[str] = Field(default=None, alias="GROQ_API_KEY")

    # Email – MailerSend
    mailersend_api_key: Optional[str] = Field(default=None, alias="MAILERSEND_API_KEY")
    mailersend_sender_email: str = Field(alias="MAILERSEND_SENDER_EMAIL")
    mailersend_sender_name: str = Field(alias="MAILERSEND_SENDER_NAME")
    from_email: str = Field(alias="FROM_EMAIL")
    email_verification_enabled: bool = Field(alias="EMAIL_VERIFICATION_ENABLED")

    # Storage
    cloudinary_cloud_name: Optional[str] = Field(default=None, alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: Optional[str] = Field(default=None, alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: Optional[str] = Field(default=None, alias="CLOUDINARY_API_SECRET")

    # Redis
    redis_url: str = Field(alias="REDIS_URL")

    # Paystack
    paystack_public_key: Optional[str] = Field(default=None, alias="PAYSTACK_PUBLIC_KEY")
    paystack_secret_key: Optional[str] = Field(default=None, alias="PAYSTACK_SECRET_KEY")
    paystack_webhook_secret: Optional[str] = Field(default=None, alias="PAYSTACK_WEBHOOK_SECRET")
    paystack_callback_url: Optional[str] = Field(default=None, alias="PAYSTACK_CALLBACK_URL")
    paystack_base_url: str = Field(default="https://api.paystack.co", alias="PAYSTACK_BASE_URL")

    @property
    def is_development(self) -> bool:
        return self.environment.lower() in ("development", "dev", "local")

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ("production", "prod")


settings = Settings()