import os
from pathlib import Path

import pytest

from scamkaki.lib.env import Settings

ROOT = Path(__file__).resolve().parents[1]
GUARDIAN_AGENT = "agent-guardian-test"
GUARDIAN_HI_AGENT = "agent-guardian-hi-test"
BAIT_AGENT = "agent-bait-test"
BAIT_HI_AGENT = "agent-bait-hi-test"


def _test_database_url() -> str | None:
    if os.environ.get("TEST_DATABASE_URL"):
        return os.environ["TEST_DATABASE_URL"]
    env_file = ROOT / ".env.local"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("TEST_DATABASE_URL="):
                return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return None


@pytest.fixture
def test_settings() -> Settings:
    url = _test_database_url()
    if not url:
        pytest.fail("TEST_DATABASE_URL is not set (env or .env.local)")
    return Settings(
        _env_file=None,
        bolna_api_key="test-key",
        bolna_guardian_agent_id=GUARDIAN_AGENT,
        bolna_guardian_hi_agent_id=GUARDIAN_HI_AGENT,
        bolna_bait_agent_id=BAIT_AGENT,
        bolna_bait_hi_agent_id=BAIT_HI_AGENT,
        bolna_webhook_token="hook-token",
        bolna_tool_token="tool-token",
        database_url=url,
        admin_password="admin-pass",
        family_link_token="family-link",
    )
