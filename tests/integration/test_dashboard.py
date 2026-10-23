from tests.integration.test_webhook import BAIT_TRANSCRIPT, bait_execution


def test_dashboard_shows_bait_script_and_draft_labeled_fixture(client, bolna):
    leaky = BAIT_TRANSCRIPT + "assistant: Ok, the code is four eight two nine one three.\n"
    bolna.executions["ex-d1"] = bait_execution("ex-d1", transcript=leaky)
    client.post("/bolna/webhook/hook-token", json={"id": "ex-d1", "status": "completed"})

    page = client.get("/", auth=("admin", "admin-pass")).text

    assert "Demo fixtures. Test calls, not real scammers." in page
    assert "Scripts Ah Ma Bait heard" in page
    assert "en-spf-01" in page and "OCBC 000-123456-7" in page
    assert "LEAK (1)" in page
    assert "DRAFT - not sent." in page and "Demo fixture case en-spf-01" in page
