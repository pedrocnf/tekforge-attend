from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App identity
    app_env: str = "prod"
    app_name: str = "Attend API"
    app_version: str = "0.4.0"

    # GCP / current infra
    gcp_project_id: str = "tekforge-attend"
    assets_bucket: str = "tekforge-attend-assets"
    exports_bucket: str = "tekforge-attend-exports"

    # Public URLs aligned with current infra and final domains
    public_web_base_url: str = "https://www.attend.tekforge.com.br"
    public_api_base_url: str = "https://api.attend.tekforge.com.br"

    # Auth
    jwt_secret: str = "change-me-local"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # Admin bootstrap
    enable_admin_bootstrap: bool = False
    admin_bootstrap_password: str = "change-me"
    admin_bootstrap_username: str = "admin"
    admin_bootstrap_email: str = "admin@attend.local"

    # Email
    email_enabled: bool = False
    email_from: str = "hello@attend.local"
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = False

    # Frontend-origin support
    cors_allow_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
