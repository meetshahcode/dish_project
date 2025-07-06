from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# Configuration settings for the application
class Settings(BaseSettings):
    app_name: str = "Dish Project"
    admin_email: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    access_token_expires_minutes: int
    refresh_token_expires_minutes: int
    secret_key: str
    algorithm: str
    access_header: str 
    refresh_header: str
    

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()