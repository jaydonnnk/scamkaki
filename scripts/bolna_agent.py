"""Create or update a Bolna agent from agents/<name>.json, filling ${VARS} from settings.

Usage: uv run python scripts/bolna_agent.py guardian
Prints only the agent id. Secrets are substituted in memory and never written to disk.
A "dispositions" list in the file (Bolna's post-call extractions) is synced by name.
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


def checked(response: httpx.Response) -> httpx.Response:
    if response.is_error:
        sys.exit(f"Bolna {response.status_code}: {response.text[:500]}")
    return response


def sync_dispositions(http: httpx.Client, agent_id: str, wanted: list[dict]) -> None:
    """Create missing dispositions and update existing ones, matched by name."""
    existing = checked(http.get("/dispositions/", params={"agent_id": agent_id})).json()
    by_name = {item["name"]: item["id"] for item in existing}
    for spec in wanted:
        if spec["name"] in by_name:
            checked(http.put(f"/dispositions/{by_name[spec['name']]}", json=spec))
        else:
            checked(http.post("/dispositions/", json={**spec, "agent_id": agent_id}))


def main(name: str) -> None:
    settings = get_settings()
    body = render(name)
    dispositions = body.pop("dispositions", [])
    agent_id = getattr(settings, f"bolna_{name}_agent_id", "")
    headers = {"Authorization": f"Bearer {settings.bolna_api_key}"}
    with httpx.Client(base_url=BASE_URL, headers=headers, timeout=30) as http:
        if agent_id:
            checked(http.put(f"/v2/agent/{agent_id}", json=body))
        else:
            agent_id = checked(http.post("/v2/agent", json=body)).json()["agent_id"]
        if dispositions:
            sync_dispositions(http, agent_id, dispositions)
        print(agent_id)


if __name__ == "__main__":
    main(sys.argv[1])
