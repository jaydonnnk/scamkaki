import pytest

from scamkaki.app.main import app, get_telegram
from scamkaki.domain import verdict
from scamkaki.lib.db import connect


def test_match_script_rejects_bad_token(client, db):
    response = client.post(
        "/tools/match-script",
        json={"agency": "spf", "demand": "transfer"},
        headers={"Authorization": "Bearer wrong"},
    )

    assert response.status_code == 401
    with connect(db) as conn:
        assert conn.execute("select count(*) as n from guardian_checks").fetchone()["n"] == 0


def test_match_script_decides_and_logs_check(client, db):
    response = client.post(
        "/tools/match-script",
        json={"agency": "SPF", "demand": "transfer"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "verdict": "likely_scam",
        "similar_count": 0,
        "say": (
            "This is likely a scam. Do not transfer money or share any code."
            " I have alerted your family. Please wait for their call."
        ),
    }
    with connect(db) as conn:
        row = conn.execute("select agency, demand, verdict from guardian_checks").fetchone()
    assert row == {"agency": "spf", "demand": "transfer", "verdict": "likely_scam"}


def test_match_script_unknown_values_find_no_scam_signs(client, db):
    response = client.post(
        "/tools/match-script",
        json={"agency": "made-up", "demand": "made-up"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.json()["verdict"] == "no_scam_signs"
    with connect(db) as conn:
        row = conn.execute("select agency, demand from guardian_checks").fetchone()
    assert row == {"agency": "other", "demand": "other"}


def test_match_script_answers_in_hindi_for_hindi_line(client, db):
    response = client.post(
        "/tools/match-script",
        json={"agency": "spf", "demand": "transfer", "language": "hi"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.status_code == 200
    assert response.json()["verdict"] == "likely_scam"
    say = response.json()["say"]
    # Listener feedback (S2): the warnings must be explicit, not left to the LLM.
    assert "पैसे मत भेजिए" in say
    assert "ओटीपी, यानी आपके फ़ोन पर आया हुआ गुप्त नंबर, किसी को मत बताइए" in say
    assert "परिवार को खबर कर दी है" in say


@pytest.mark.parametrize(
    ("language", "say"),
    [("en", "Not sure. Please call your family before doing anything."), ("hi", "पक्का नहीं")],
)
def test_match_script_error_returns_unclear(client, db, monkeypatch, language, say):
    def broken(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(verdict, "decide", broken)
    response = client.post(
        "/tools/match-script",
        json={"agency": "spf", "demand": "transfer", "language": language},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.status_code == 200
    assert response.json()["verdict"] == "unclear"
    assert response.json()["say"].startswith(say)


def check_row(db):
    with connect(db) as conn:
        return conn.execute(
            "select verdict, language, alert_status from guardian_checks"
        ).fetchone()


def test_match_script_likely_scam_alerts_family(client, db, telegram):
    response = client.post(
        "/tools/match-script",
        json={"agency": "spf", "demand": "transfer", "language": "hi"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.json()["verdict"] == "likely_scam"
    assert len(telegram.sent) == 1
    assert telegram.sent[0].startswith("[Demo fixture] Ah Ma Guardian: likely scam call")
    assert "Caller claimed to be: Police (SPF)" in telegram.sent[0]
    assert check_row(db) == {"verdict": "likely_scam", "language": "hi", "alert_status": "sent"}


@pytest.mark.parametrize(
    ("agency", "demand", "verdict"),
    [("bank", "none", "no_scam_signs"), ("other", "other", "no_scam_signs")],
)
def test_match_script_other_verdicts_send_no_alert(client, db, telegram, agency, demand, verdict):
    response = client.post(
        "/tools/match-script",
        json={"agency": agency, "demand": demand},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.json()["verdict"] == verdict
    assert telegram.sent == []
    assert check_row(db)["alert_status"] is None


def test_match_script_error_sends_no_alert(client, db, telegram, monkeypatch):
    monkeypatch.setattr(verdict, "decide", lambda *args: 1 / 0)
    response = client.post(
        "/tools/match-script",
        json={"agency": "spf", "demand": "transfer"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.json()["verdict"] == "unclear"
    assert telegram.sent == []


def test_match_script_telegram_failure_still_answers(client, db, telegram):
    telegram.ok = False
    response = client.post(
        "/tools/match-script",
        json={"agency": "ica", "demand": "otp"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.status_code == 200
    assert response.json()["verdict"] == "likely_scam"
    assert check_row(db)["alert_status"] == "failed"


def test_match_script_without_telegram_records_alert_off(client, db):
    app.dependency_overrides[get_telegram] = lambda: None
    response = client.post(
        "/tools/match-script",
        json={"agency": "courier", "demand": "gift_card"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.json()["verdict"] == "likely_scam"
    assert check_row(db)["alert_status"] == "off"
