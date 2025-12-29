
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_name: str = "MiniHelpDesk API"
    dev_email: str
    version: int = 1
    database_url: str
    
    model_config = SettingsConfigDict(env_file='.env')
    
    
settings = Settings(dev_email="srfrikidev@gmail.com")  # type: ignore