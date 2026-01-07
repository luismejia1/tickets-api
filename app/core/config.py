
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    api_name: str = "MiniHelpDesk API"
    dev_email: str
    version: int = 1
    database_url: str
    api_version: str = '/api/v1'

    model_config = SettingsConfigDict(env_file='.env')

    # Security settings
    secret_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"


settings = Settings(dev_email="srfrikidev@gmail.com")  # type: ignore
