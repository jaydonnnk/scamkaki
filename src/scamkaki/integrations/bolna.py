"""Bolna REST client. Base URL and auth from https://www.bolna.ai/docs/AGENTS.md."""

from typing import Any

import httpx

BASE_URL = "https://api.bolna.ai"


class BolnaClient:
    def __init__(self, api_key: str, base_url: str = BASE_URL) -> None:
        self._http = httpx.Client(
            base_url=base_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=20
        )

    def get_execution(self, execution_id: str) -> dict[str, Any]:
        response = self._http.get(f"/executions/{execution_id}")
        response.raise_for_status()
        return response.json()
