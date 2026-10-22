"""Settings loaded from the environment. The only module that reads env vars."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.local", extra="ignore")

    bolna_api_key: str
    bolna_bait_agent_id: str = ""
    bolna_guardian_agent_id: str = ""
    bolna_webhook_token: str
    bolna_tool_token: str
    database_url: str
    tts_base_url: str = ""
    tts_api_key: str = ""
    app_base_url: str = ""
    log_level: str = "info"


@lru_cache
def get_settings() -> Settings:
    return Settings()
