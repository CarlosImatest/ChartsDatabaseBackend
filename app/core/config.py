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
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False
    )


settings = Settings()