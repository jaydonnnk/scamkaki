"""Create or update a Bolna agent from agents/<name>.json, filling ${VARS} from settings.

Usage: uv run python scripts/bolna_agent.py guardian
Prints only the agent id. Secrets are substituted in memory and never written to disk.
"""

import json
import string
import sys
from pathlib import Path

import httpx

from scamkaki.integrations.bolna import BASE_URL
from scamkaki.lib.env import get_settings

ROOT = Path(__file__).resolve().parents[1]


def render(name: str) -> dict:
    settings = get_settings()
    values = {field.upper(): str(value) for field, value in settings.model_dump().items()}
    template = string.Template((ROOT / "agents" / f"{name}.json").read_text())
    missing = [v for v in template.get_identifiers() if not values.get(v)]
    if missing:
        sys.exit(f"missing settings: {', '.join(missing)}")
    return json.loads(template.substitute(values))


def main(name: str) -> None:
    settings = get_settings()
    body = render(name)
    agent_id = getattr(settings, f"bolna_{name}_agent_id", "")
    headers = {"Authorization": f"Bearer {settings.bolna_api_key}"}
    with httpx.Client(base_url=BASE_URL, headers=headers, timeout=30) as http:
        if agent_id:
            response = http.put(f"/v2/agent/{agent_id}", json=body)
        else:
            response = http.post("/v2/agent", json=body)
        if response.is_error:
            sys.exit(f"Bolna {response.status_code}: {response.text[:500]}")
        print(agent_id or response.json()["agent_id"])


if __name__ == "__main__":
    main(sys.argv[1])
