"""Settings loaded from the environment. The only module that reads env vars."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from scamkaki.domain.types import Language, Line


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.local", extra="ignore")

    bolna_api_key: str
    bolna_bait_agent_id: str = ""
    bolna_bait_hi_agent_id: str = ""
    bolna_guardian_agent_id: str = ""
    bolna_guardian_hi_agent_id: str = ""
    bolna_webhook_token: str
    bolna_tool_token: str
    database_url: str
    app_base_url: str = ""
    family_transfer_number: str = ""
    admin_username: str = "admin"
    admin_password: str = ""
    log_level: str = "info"

    def agent_line(self, agent_id: str | None) -> tuple[Line, Language] | None:
        """Which persona and language a Bolna agent id belongs to; None if it is not ours."""
        agents: dict[str, tuple[Line, Language]] = {
            self.bolna_guardian_agent_id: ("guardian", "en"),
            self.bolna_guardian_hi_agent_id: ("guardian", "hi"),
            self.bolna_bait_agent_id: ("bait", "en"),
            self.bolna_bait_hi_agent_id: ("bait", "hi"),
        }
        return agents.get(agent_id) if agent_id else None

    def guardian_agent_id(self, language: Language) -> str:
        return self.bolna_guardian_hi_agent_id if language == "hi" else self.bolna_guardian_agent_id


@lru_cache
def get_settings() -> Settings:
    return Settings()
