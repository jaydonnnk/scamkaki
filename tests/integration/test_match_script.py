import pytest

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
            " I will connect you to your family now."
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
    assert "परिवार से जोड़ रही हूँ" in say


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
