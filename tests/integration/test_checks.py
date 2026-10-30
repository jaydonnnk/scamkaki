import pytest

from scamkaki.lib.db import connect
from tests.integration.test_calls import ADMIN, saved_call


def saved_check(db, verdict="likely_scam", acted="paid", alert_status="sent", **fields):
    values = dict(
        agency="courier",
        demand="card_details",
        channel="sms",
        tactics=[],
        language="hi",
        similar_count=0,
        execution_id=None,
    )
    values.update(fields)
    with connect(db) as conn:
        return conn.execute(
            "insert into guardian_checks (verdict, acted, alert_status, agency, demand, channel, "
            "tactics, language, similar_count, execution_id) values "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id",
            (verdict, acted, alert_status, *values.values()),
        ).fetchone()["id"]


def test_call_and_check_are_not_joined_by_time_or_fixture(client, db):
    call_id = saved_call(db, "same-fixture")
    check_id = saved_check(db, execution_id="same-fixture")
    with connect(db) as conn:
        conn.execute(
            "update guardian_checks set created_at = (select created_at from calls where id=%s)",
            (call_id,),
        )
    call = client.get(f"/calls/{call_id}", auth=ADMIN).text
    assert "No verified check link" in call
    assert "Likely scam" not in call and 'href="/checks/' not in call
    check = client.get(f"/checks/{check_id}", auth=ADMIN).text
    assert "No verified call link" in check and 'href="/calls/' not in check
    assert "same-fixture" not in check


def test_check_page_preserves_verdict_urgency_and_alert_states(client, db):
    for verdict, label in [
        ("likely_scam", "Likely scam"),
        ("unclear", "Unclear, talk to family"),
        ("no_scam_signs", "No scam signs found"),
    ]:
        for status, alert_label in [
            ("pending", "Telegram sending"),
            ("sent", "Telegram sent"),
            ("failed", "Telegram failed"),
            ("off", "Telegram not set up"),
            (None, "Alert not recorded"),
        ]:
            for acted, urgent in [
                ("paid", True),
                ("gave_code_or_card", True),
                ("installed_app", True),
                ("none", False),
                ("unsure", False),
            ]:
                check_id = saved_check(db, verdict, acted, status)
                response = client.get(f"/checks/{check_id}", auth=ADMIN)
                assert response.status_code == 200
                page = response.text
                assert label in page and alert_label in page
                assert ('class="urgent-tag"' in page) == urgent
                assert "None recorded" in page and "Hindi" in page
                assert "No verified call link" in page
                assert "Delivered" not in page and "Receipt unknown" in page
                assert response.headers["cache-control"] == "no-store"
    check_id = saved_check(db, tactics=["handoff", "secrecy"], similar_count=2)
    page = client.get(f"/checks/{check_id}", auth=ADMIN).text
    assert "Passed to another officer" in page and "Told to keep it secret" in page
    assert "Same script heard 2 times" in page


@pytest.mark.parametrize("url", ["/", "/calls", "/calls/1", "/checks/1"])
def test_reviewer_routes_require_admin(client, url):
    for auth in (None, ("admin", "wrong")):
        response = client.get(url, auth=auth)
        assert response.status_code == 401
        assert "Recorded" not in response.text
