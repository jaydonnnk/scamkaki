from scamkaki.lib.db import connect
from tests.conftest import GUARDIAN_AGENT, GUARDIAN_HI_AGENT
from tests.support.fakes import execution


def test_webhook_rejects_bad_token(client, bolna, db):
    bolna.executions["ex-1"] = execution("ex-1", GUARDIAN_AGENT)

    response = client.post("/bolna/webhook/wrong-token", json={"id": "ex-1", "status": "completed"})

    assert response.status_code == 404
    assert bolna.fetched == []
    with connect(db) as conn:
        assert conn.execute("select count(*) as n from calls").fetchone()["n"] == 0


def test_webhook_stores_guardian_call(client, bolna, db):
    bolna.executions["ex-2"] = execution(
        "ex-2", GUARDIAN_AGENT, context_details={"recipient_data": {"fixture_case": "spf-01"}}
    )

    # The posted body is only a pointer: the stored row must come from Bolna's execution.
    response = client.post(
        "/bolna/webhook/hook-token", json={"id": "ex-2", "status": "completed", "transcript": "x"}
    )

    assert response.status_code == 204
    assert bolna.fetched == ["ex-2"]
    with connect(db) as conn:
        row = conn.execute("select * from calls where execution_id = 'ex-2'").fetchone()
    assert row["line"] == "guardian"
    assert row["language"] == "en"
    assert row["status"] == "completed"
    assert row["duration_s"] == 16
    assert row["fixture_case"] == "spf-01"
    assert row["transcript"].startswith("assistant: Hello, this is Ah Ma Guardian.")


def test_webhook_stores_language_of_hindi_guardian(client, bolna, db):
    bolna.executions["ex-3"] = execution("ex-3", GUARDIAN_HI_AGENT)

    response = client.post("/bolna/webhook/hook-token", json={"id": "ex-3", "status": "completed"})

    assert response.status_code == 204
    with connect(db) as conn:
        row = conn.execute("select line, language from calls where execution_id = 'ex-3'")
        row = row.fetchone()
    assert row == {"line": "guardian", "language": "hi"}


def test_webhook_ignores_unknown_agent(client, bolna, db):
    bolna.executions["ex-4"] = execution("ex-4", "someone-elses-agent")

    response = client.post("/bolna/webhook/hook-token", json={"id": "ex-4", "status": "completed"})

    assert response.status_code == 204
    with connect(db) as conn:
        assert conn.execute("select count(*) as n from calls").fetchone()["n"] == 0
