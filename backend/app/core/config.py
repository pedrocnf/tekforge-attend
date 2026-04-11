from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    app_name: str = "TekAttend API"
    app_version: str = "0.2.0"
    gcp_project_id: str = "tekforge-attend"
    exports_bucket: str = "tekforge-attend-exports"
    assets_bucket: str = "tekforge-attend-assets"
    jwt_secret: str = "change-me-local"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    admin_bootstrap_password: str = "change-me-local"
    admin_bootstrap_username: str = "admin"
    admin_bootstrap_email: str = "admin@tekattend.local"
    enable_admin_bootstrap: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
