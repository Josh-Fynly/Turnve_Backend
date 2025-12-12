"""
Application configuration using Pydantic v2 settings.

Notes:
 - Non-critical external URLs and 3rd-party API keys are optional (default=None)
   to avoid startup failures when a value is not yet provided during development.
 - Critical values (database, SECRET_KEY, FROM_EMAIL, REDIS_URL) remain required.
"""
from typing import Optional
from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # -------------------------
    # Application
    # -------------------------
    app_name: str = Field(alias="APP_NAME")
    environment: str = Field(alias="ENVIRONMENT")
    debug: bool = Field(alias="DEBUG")

    # -------------------------
    # Database (required)
    # -------------------------
    database_url: str = Field(alias="DATABASE_URL")
    database_url_sync: str = Field(alias="DATABASE_URL_SYNC")

    # -------------------------
    # Security / Tokens (required)
    # -------------------------
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # -------------------------
    # AI / LLM keys (optional placeholders)
    # -------------------------
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    gemini_api_key: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")
    groq_api_key: Optional[str] = Field(default=None, alias="GROQ_API_KEY")
    # Add other LLM providers as needed:
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")

    # -------------------------
    # Email (MailerSend) - require sender and from address
    # -------------------------
    mailersend_api_key: Optional[str] = Field(default=None, alias="MAILERSEND_API_KEY")
    mailersend_sender_email: str = Field(alias="MAILERSEND_SENDER_EMAIL")
    mailersend_sender_name: str = Field(alias="MAILERSEND_SENDER_NAME")
    mailersend_reply_to: Optional[str] = Field(default=None, alias="MAILERSEND_REPLY_TO")

    from_email: str = Field(alias="FROM_EMAIL")
    email_verification_enabled: bool = Field(alias="EMAIL_VERIFICATION_ENABLED")

    # -------------------------
    # File storage (Cloudinary) - optional
    # -------------------------
    cloudinary_cloud_name: Optional[str] = Field(default=None, alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: Optional[str] = Field(default=None, alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: Optional[str] = Field(default=None, alias="CLOUDINARY_API_SECRET")

    # -------------------------
    # Redis (required for caching/background tasks)
    # -------------------------
    redis_url: str = Field(alias="REDIS_URL")

    # -------------------------
    # SMS (Termii) - optional key, required sender id
    # -------------------------
    termii_api_key: Optional[str] = Field(default=None, alias="TERMII_API_KEY")
    termii_sender_id: str = Field(alias="TERMII_SENDER_ID")
    termii_base_url: Optional[str] = Field(default=None, alias="TERMII_BASE_URL")

    # -------------------------
    # Paystack (payments)
    # -------------------------
    paystack_public_key: Optional[str] = Field(default=None, alias="PAYSTACK_PUBLIC_KEY")
    paystack_secret_key: Optional[str] = Field(default=None, alias="PAYSTACK_SECRET_KEY")
    paystack_webhook_secret: Optional[str] = Field(default=None, alias="PAYSTACK_WEBHOOK_SECRET")
    paystack_callback_url: Optional[str] = Field(default=None, alias="PAYSTACK_CALLBACK_URL")
    paystack_base_url: str = Field(default="https://api.paystack.co", alias="PAYSTACK_BASE_URL")

    # -------------------------
    # YouTube / Video / Educational APIs (optional)
    # -------------------------
    youtube_api_key: Optional[str] = Field(default=None, alias="YOUTUBE_API_KEY")

    # Educational content API endpoints (optional)
    coursera_api_url: Optional[str] = Field(default=None, alias="COURSERA_API_URL")
    edx_api_url: Optional[str] = Field(default=None, alias="EDX_API_URL")
    futurelearn_api_url: Optional[str] = Field(default=None, alias="FUTURELEARN_API_URL")
    khan_academy_api_url: Optional[str] = Field(default=None, alias="KHAN_ACADEMY_API_URL")
    youtube_search_api_url: Optional[str] = Field(default=None, alias="YOUTUBE_SEARCH_API_URL")
    mit_ocw_api_url: Optional[str] = Field(default=None, alias="MIT_OCW_API_URL")

    # Public website URLs (optional)
    coursera_website_url: Optional[AnyHttpUrl] = Field(default=None, alias="COURSERA_WEBSITE_URL")
    edx_website_url: Optional[AnyHttpUrl] = Field(default=None, alias="EDX_WEBSITE_URL")
    futurelearn_website_url: Optional[AnyHttpUrl] = Field(default=None, alias="FUTURELEARN_WEBSITE_URL")
    khan_academy_website_url: Optional[AnyHttpUrl] = Field(default=None, alias="KHAN_ACADEMY_WEBSITE_URL")
    youtube_education_url: Optional[AnyHttpUrl] = Field(default=None, alias="YOUTUBE_EDUCATION_URL")
    mit_ocw_website_url: Optional[AnyHttpUrl] = Field(default=None, alias="MIT_OCW_WEBSITE_URL")

    # -------------------------
    # Job search APIs (optional)
    # -------------------------
    remoteok_api_url: Optional[str] = Field(default=None, alias="REMOTEOK_API_URL")
    remotive_api_url: Optional[str] = Field(default=None, alias="REMOTIVE_API_URL")
    github_api_url: Optional[str] = Field(default=None, alias="GITHUB_API_URL")
    angellist_api_url: Optional[str] = Field(default=None, alias="ANGELLIST_API_URL")
    linkedin_rapidapi_url: Optional[str] = Field(default=None, alias="LINKEDIN_RAPIDAPI_URL")
    indeed_rapidapi_url: Optional[str] = Field(default=None, alias="INDEED_RAPIDAPI_URL")
    crunchbase_api_url: Optional[str] = Field(default=None, alias="CRUNCHBASE_API_URL")

    # Optional API keys for paid integrations
    linkedin_rapidapi_key: Optional[str] = Field(default=None, alias="LINKEDIN_RAPIDAPI_KEY")
    indeed_rapidapi_key: Optional[str] = Field(default=None, alias="INDEED_RAPIDAPI_KEY")
    crunchbase_api_key: Optional[str] = Field(default=None, alias="CRUNCHBASE_API_KEY")

    # -------------------------
    # Case study / simulation URLs (optional)
    # -------------------------
    netflix_tech_blog_url: Optional[str] = Field(default=None, alias="NETFLIX_TECH_BLOG_URL")
    spotify_engineering_url: Optional[str] = Field(default=None, alias="SPOTIFY_ENGINEERING_URL")
    who_covax_url: Optional[str] = Field(default=None, alias="WHO_COVAX_URL")
    tesla_gigafactory_url: Optional[str] = Field(default=None, alias="TESLA_GIGAFACTORY_URL")
    azure_cognitive_services_url: Optional[str] = Field(default=None, alias="AZURE_COGNITIVE_SERVICES_URL")
    emirates_digital_innovation_url: Optional[str] = Field(default=None, alias="EMIRATES_DIGITAL_INNOVATION_URL")
    worldbank_financial_inclusion_url: Optional[str] = Field(default=None, alias="WORLDBANK_FINANCIAL_INCLUSION_URL")
    amazon_prime_press_url: Optional[str] = Field(default=None, alias="AMAZON_PRIME_PRESS_URL")

    # -------------------------
    # Job scraping + CORS
    # -------------------------
    job_scraping_enabled: bool = Field(alias="JOB_SCRAPING_ENABLED")
    allowed_hosts: str = Field(alias="ALLOWED_HOSTS")

    # -------------------------
    # Platform URLs + social
    # -------------------------
    frontend_url: Optional[AnyHttpUrl] = Field(default=None, alias="FRONTEND_URL")
    platform_url: Optional[AnyHttpUrl] = Field(default=None, alias="PLATFORM_URL")
    help_center_url: Optional[AnyHttpUrl] = Field(default=None, alias="HELP_CENTER_URL")

    social_linkedin: Optional[str] = Field(default=None, alias="SOCIAL_LINKEDIN")
    social_twitter: Optional[str] = Field(default=None, alias="SOCIAL_TWITTER")
    social_facebook: Optional[str] = Field(default=None, alias="SOCIAL_FACEBOOK")
    social_instagram: Optional[str] = Field(default=None, alias="SOCIAL_INSTAGRAM")

    # -------------------------
    # Convenience properties
    # -------------------------
    @property
    def is_development(self) -> bool:
        return self.environment.lower() in ("development", "dev", "local")

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ("production", "prod")


# single global instance used by the application
settings = Settings()