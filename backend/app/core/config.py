from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    app_name: str = "Attend API"
    app_version: str = "0.4.0"
    gcp_project_id: str = "tekforge-attend"
    jwt_secret: str = "change-me-local"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    enable_admin_bootstrap: bool = False
    admin_bootstrap_password: str = "change-me"
    admin_bootstrap_username: str = "admin"
    admin_bootstrap_email: str = "admin@attend.local"
    email_enabled: bool = False
    email_from: str = "hello@attend.local"
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = False
    public_web_base_url: str = "https://www.attend.tekforge.com.br"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


settings = Settings()
