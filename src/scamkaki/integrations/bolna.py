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

    def mint_web_call_session(
        self, agent_id: str, user_data: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Short-lived, single-use browser call session (Web Call SDK docs).

        user_data are the call's variables, for example the fixture case id.
        """
        body: dict[str, Any] = {"agent_id": agent_id}
        if user_data:
            body["user_data"] = user_data
        response = self._http.post("/web-call/session", json=body)
        response.raise_for_status()
        return response.json()
