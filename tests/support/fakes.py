"""Fake Bolna client and payload builders for tests."""

from typing import Any


class FakeBolna:
    def __init__(self, executions: dict[str, dict[str, Any]] | None = None) -> None:
        self.executions = executions or {}
        self.fetched: list[str] = []

    def get_execution(self, execution_id: str) -> dict[str, Any]:
        self.fetched.append(execution_id)
        return self.executions[execution_id]


def execution(execution_id: str, agent_id: str, **fields: Any) -> dict[str, Any]:
    """A completed execution shaped like GET /executions/{id} in the Bolna docs."""
    return {
        "id": execution_id,
        "agent_id": agent_id,
        "status": "completed",
        "conversation_duration": 16,
        "transcript": "assistant: Hello, this is Ah Ma Guardian.\nuser: Got one man call me.",
        "extracted_data": None,
        "node_extracted_data": None,
        "context_details": {},
        **fields,
    }


class FakeBolnaWithSessions(FakeBolna):
    def __init__(self) -> None:
        super().__init__()
        self.sessions: list[str] = []

    def mint_web_call_session(self, agent_id: str) -> dict[str, Any]:
        self.sessions.append(agent_id)
        return {"session": "fake"}


class FakeTelegram:
    """Records family alert messages; set ok=False to simulate a failed send."""

    def __init__(self, ok: bool = True) -> None:
        self.ok = ok
        self.sent: list[str] = []

    def __call__(self, text: str) -> bool:
        self.sent.append(text)
        return self.ok
