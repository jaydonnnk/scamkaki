from scamkaki.lib.db import connect
from tests.integration.test_match_script import bait_script
from tests.integration.test_webhook import BAIT_TRANSCRIPT, bait_execution

ADMIN = ("admin", "admin-pass")


def guardian_check(client, agency, demand, **signs):
    return client.post(
        "/tools/match-script",
        json={"agency": agency, "demand": demand, **signs},
        headers={"Authorization": "Bearer tool-token"},
    )


def test_dashboard_lists_bait_script_with_leak_check_and_report_link(client, bolna):
    leaky = BAIT_TRANSCRIPT + "assistant: Ok, the code is four eight two nine one three.\n"
    bolna.executions["ex-d1"] = bait_execution("ex-d1", transcript=leaky)
    client.post("/bolna/webhook/hook-token", json={"id": "ex-d1", "status": "completed"})

    page = client.get("/", auth=ADMIN).text

    assert "Demo fixtures. Test calls, not real scammers." in page
    assert "en-spf-01" in page
    assert "LEAK (1)" in page
    assert 'href="/reports/1"' in page and "Report draft" in page
    assert "Not collected" in page  # Bait does not extract warning signs


def test_dashboard_shows_reviewed_state_of_a_report(client, bolna):
    bolna.executions["ex-d2"] = bait_execution("ex-d2")
    client.post("/bolna/webhook/hook-token", json={"id": "ex-d2", "status": "completed"})
    client.post("/reports/1/review", auth=ADMIN)

    page = client.get("/", auth=ADMIN).text

    assert "Report reviewed" in page and "Report draft" not in page


def test_dashboard_lists_warning_signs_and_the_urgent_result(client):
    guardian_check(client, "minlaw", "transfer", channel="call", tactics="secrecy,handoff")
    guardian_check(
        client, "courier", "card_details", channel="sms", tactics="link_fee", acted="paid"
    )

    page = client.get("/", auth=ADMIN).text

    assert "Warning signs" in page
    assert "Passed to another officer" in page and "Told to keep it secret" in page
    assert "Small fee by link" in page
    assert "URGENT" in page and "Ah Ma already: Paid money" in page
    assert page.count("URGENT") == 1  # only the paid check is urgent
    assert "Telegram sent" in page


def test_dashboard_labels_a_check_with_no_recorded_signs(client):
    guardian_check(client, "spf", "transfer")

    page = client.get("/", auth=ADMIN).text

    assert "None recorded" in page
    assert "Likely scam" in page


def test_dashboard_keeps_unclear_and_no_signs_results_in_the_feed(client):
    guardian_check(client, "cpf", "none", channel="sms")
    guardian_check(client, "friend_family", "transfer", channel="call")

    page = client.get("/", auth=ADMIN).text

    assert "No scam signs found" in page
    assert "Unclear, talk to family" in page
    assert "URGENT" not in page


def test_dashboard_summarizes_scripts_heard_this_week(client, db):
    bait_script(db, "spf", "transfer", "en")
    bait_script(db, "spf", "transfer", "hi")
    bait_script(db, "bank", "transfer", "en", days_ago=8)

    page = client.get("/", auth=ADMIN).text

    week = page.split("Scripts heard this week")[1].split("Call log")[0]
    assert "<td>Police (SPF)</td><td>Money transfer</td><td>2</td>" in week
    assert "A bank" not in week  # older than 7 days


def test_dashboard_orders_the_feed_newest_first_across_both_lines(client, bolna, db):
    bolna.executions["ex-d3"] = bait_execution("ex-d3")
    client.post("/bolna/webhook/hook-token", json={"id": "ex-d3", "status": "completed"})
    guardian_check(client, "courier", "card_details", tactics="link_fee")
    with connect(db) as conn:
        conn.execute("update scripts set created_at = now() - interval '1 hour'")

    page = client.get("/", auth=ADMIN).text

    assert page.index("Small fee by link") < page.index("Report draft")


def test_dashboard_keeps_the_calls_log_with_status_and_case(client, bolna):
    bolna.executions["ex-d4"] = bait_execution("ex-d4", status="completed")
    client.post("/bolna/webhook/hook-token", json={"id": "ex-d4", "status": "completed"})

    page = client.get("/", auth=ADMIN).text

    assert "Call log" in page and "completed" in page
