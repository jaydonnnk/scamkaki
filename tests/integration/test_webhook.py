from scamkaki.lib.db import connect
from tests.conftest import BAIT_AGENT, GUARDIAN_AGENT, GUARDIAN_HI_AGENT
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


BAIT_TRANSCRIPT = (
    "assistant: Hello? Who is this ah?\n"
    "user: Inspector Lim, SPF. Transfer your savings to OCBC account 000-123456-7.\n"
    "assistant: Aiyo, which bank you say? Let me find my pen.\n"
)
BAIT_EXTRACTED = {
    "Scam script": {
        "agency": {"objective": "spf", "subjective": None},
        "demand": {"objective": "transfer", "subjective": None},
        "payee_bank": {"objective": None, "subjective": "OCBC"},
        "payee_account": {"objective": None, "subjective": "000-123456-7"},
        "paynow_id": {"objective": None, "subjective": ""},
        "url": {"objective": None, "subjective": ""},
        "summary": {"objective": None, "subjective": "Fake SPF officer, safety account."},
    }
}


def bait_execution(execution_id, **fields):
    defaults = {
        "transcript": BAIT_TRANSCRIPT,
        "extracted_data": BAIT_EXTRACTED,
        "context_details": {"recipient_data": {"fixture_case": "en-spf-01"}},
    }
    return execution(execution_id, BAIT_AGENT, **{**defaults, **fields})


def test_webhook_stores_bait_call_script_and_draft(client, bolna, db):
    bolna.executions["ex-b1"] = bait_execution("ex-b1")

    response = client.post("/bolna/webhook/hook-token", json={"id": "ex-b1", "status": "completed"})

    assert response.status_code == 204
    with connect(db) as conn:
        call = conn.execute("select * from calls where execution_id = 'ex-b1'").fetchone()
        script = conn.execute("select * from scripts").fetchone()
        report = conn.execute("select * from reports").fetchone()
    assert (call["line"], call["leaks"]) == ("bait", [])
    assert script["call_id"] == call["id"]
    assert (script["agency"], script["demand"]) == ("spf", "transfer")
    assert (script["payee_bank"], script["payee_account"]) == ("OCBC", "000-123456-7")
    assert script["paynow_id"] is None
    assert report["call_id"] == call["id"]
    assert report["status"] == "draft"
    assert report["draft"].startswith("DRAFT - not sent.")
    assert "Demo fixture case en-spf-01" in report["draft"]


def test_webhook_is_idempotent_per_execution(client, bolna, db):
    bolna.executions["ex-b2"] = bait_execution("ex-b2")

    for _ in range(3):
        response = client.post(
            "/bolna/webhook/hook-token", json={"id": "ex-b2", "status": "completed"}
        )
        assert response.status_code == 204

    with connect(db) as conn:
        counts = conn.execute(
            "select (select count(*) from calls) as calls, (select count(*) from scripts)"
            " as scripts, (select count(*) from reports) as reports"
        ).fetchone()
    assert counts == {"calls": 1, "scripts": 1, "reports": 1}


def test_webhook_keeps_a_reviewed_report(client, bolna, db):
    bolna.executions["ex-b3"] = bait_execution("ex-b3")
    client.post("/bolna/webhook/hook-token", json={"id": "ex-b3", "status": "completed"})
    with connect(db) as conn:
        conn.execute("update reports set status = 'reviewed', draft = 'checked by a person'")

    client.post("/bolna/webhook/hook-token", json={"id": "ex-b3", "status": "completed"})

    with connect(db) as conn:
        report = conn.execute("select status, draft from reports").fetchone()
    assert report == {"status": "reviewed", "draft": "checked by a person"}


def test_webhook_flags_leak_on_call(client, bolna, db):
    leaky = BAIT_TRANSCRIPT + "assistant: Ok ok, the code is four eight two nine one three.\n"
    bolna.executions["ex-b4"] = bait_execution("ex-b4", transcript=leaky)

    client.post("/bolna/webhook/hook-token", json={"id": "ex-b4", "status": "completed"})

    with connect(db) as conn:
        call = conn.execute("select leaks from calls where execution_id = 'ex-b4'").fetchone()
        report = conn.execute("select draft from reports").fetchone()
    assert [(leak["kind"], leak["turn_index"]) for leak in call["leaks"]] == [
        ("otp_or_account_digits", 2)
    ]
    assert not any(ch.isdigit() for ch in call["leaks"][0]["excerpt"])
    assert "LEAK CHECK FAILED" in report["draft"]


def test_webhook_stores_no_script_for_guardian(client, bolna, db):
    bolna.executions["ex-g1"] = execution("ex-g1", GUARDIAN_AGENT, extracted_data=BAIT_EXTRACTED)

    client.post("/bolna/webhook/hook-token", json={"id": "ex-g1", "status": "completed"})

    with connect(db) as conn:
        assert conn.execute("select count(*) as n from scripts").fetchone()["n"] == 0
        assert conn.execute("select count(*) as n from reports").fetchone()["n"] == 0
