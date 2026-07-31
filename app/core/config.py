from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    mongodb_username: str
    mongodb_password: str
    mongodb_uri: str

    database_name: str = "Users"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # --- Email / invite settings ---
    resend_api_key: str
    email_from: str = "onboarding@yourdomain.com"

    # Used to build links that get emailed out (invites, etc.)
    frontend_url: str = "http://localhost:4200"

    verification_code_expire_minutes: int = 15
    invite_expire_hours: int = 24

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False
    )


settings = Settings()