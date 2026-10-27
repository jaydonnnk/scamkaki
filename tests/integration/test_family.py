from scamkaki.app.main import app
from scamkaki.lib.env import get_settings


def check(client, agency, demand, **signs):
    return client.post(
        "/tools/match-script",
        json={"agency": agency, "demand": demand, **signs},
        headers={"Authorization": "Bearer tool-token"},
    )


def test_family_page_rejects_wrong_link(client):
    assert client.get("/family/wrong").status_code == 404
    assert client.get("/family/wrong/alerts").status_code == 404

    page = client.get("/family/family-link")
    assert page.status_code == 200
    assert "Demo fixtures. Test calls, not real scammers." in page.text
    assert page.headers["referrer-policy"] == "no-referrer"


def test_family_page_is_closed_without_a_link_token(client, test_settings):
    unset = test_settings.model_copy(update={"family_link_token": ""})
    app.dependency_overrides[get_settings] = lambda: unset

    assert client.get("/family/").status_code == 404
    assert client.get("/family/%20").status_code == 404


def test_family_alerts_lists_likely_scam_only(client):
    check(client, "bank", "none")
    check(client, "spf", "transfer")
    check(client, "other", "other")

    response = client.get("/family/family-link/alerts")

    assert response.status_code == 200
    alerts = response.json()
    assert [(a["agency"], a["demand"]) for a in alerts] == [("spf", "transfer")]
    assert alerts[0]["alert_status"] == "sent"
    assert alerts[0]["language"] == "en"


def test_family_alerts_list_urgent_first(client):
    check(client, "courier", "card_details", channel="sms", tactics="link_fee", acted="paid")
    check(client, "minlaw", "transfer", channel="call", tactics="stay_on_line,handoff")

    alerts = client.get("/family/family-link/alerts").json()

    assert [(a["agency"], a["urgent"]) for a in alerts] == [("courier", True), ("minlaw", False)]
    assert alerts[0]["acted"] == "paid" and alerts[0]["channel"] == "sms"
    assert alerts[1]["tactics"] == ["handoff", "stay_on_line"]  # fixed order, not as sent


def test_family_page_knows_the_new_labels(client):
    page = client.get("/family/family-link").text

    assert "Urgent: Ah Ma already acted" in page
    assert "Told to stay on the line" in page and "Card details on a website" in page
