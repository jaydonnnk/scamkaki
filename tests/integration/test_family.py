import pytest

from scamkaki.app.main import app
from scamkaki.lib.db import connect
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
    assert page.headers["cache-control"] == "no-store"


def test_family_page_is_closed_without_a_link_token(client, test_settings):
    unset = test_settings.model_copy(update={"family_link_token": ""})
    app.dependency_overrides[get_settings] = lambda: unset

    assert client.get("/family/").status_code == 404
    assert client.get("/family/%20").status_code == 404
    assert client.get("/family/anything/alerts").status_code == 404


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


def test_family_alerts_list_recent_urgent_first(client):
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


def test_family_alerts_older_urgent_falls_back_into_time_order(client, db):
    check(client, "courier", "card_details", acted="paid")
    with connect(db) as conn:  # The urgent alert is now 25 hours old.
        conn.execute("update guardian_checks set created_at = now() - interval '25 hours'")
    check(client, "minlaw", "transfer", tactics="handoff")

    alerts = client.get("/family/family-link/alerts").json()

    assert [(a["agency"], a["urgent"]) for a in alerts] == [("minlaw", False), ("courier", True)]


def test_family_standalone_structure_and_refresh_disclosure(client):
    page = client.get("/family/family-link").text
    assert '<a class="skip btn" href="#main">Skip to alerts</a>' in page
    assert '<main id="main"' in page
    assert "Why Guardian raised this alert" in page
    assert "<noscript>" in page and "alerts cannot refresh" in page
    assert 'id="latest"' in page and 'id="earlier"' in page and 'id="sound"' in page
    assert "<nav" not in page and 'class="sidebar"' not in page
    for path in ('href="/calls', 'href="/reports', 'href="/voice', 'href="/patterns'):
        assert path not in page
    assert "innerHTML" not in page
    assert (
        "@media (prefers-reduced-motion:reduce){*{animation:none!important;"
        "transition:none!important}}" in page
    )


def test_family_privacy_headers_and_empty_json(client):
    page = client.get("/family/family-link")
    assert page.headers["x-robots-tag"] == "noindex"
    assert '<meta name="robots" content="noindex">' in page.text
    assert '<meta name="referrer" content="no-referrer">' in page.text
    response = client.get("/family/family-link/alerts")
    assert response.headers["cache-control"] == "no-store"
    assert response.json() == []


def test_family_json_preserves_hostile_recorded_text(client, db):
    check(client, "courier", "card_details", acted="paid")
    needle = '<img src=x onerror="syntheticNeedle()">'
    with connect(db) as conn:
        conn.execute("update guardian_checks set agency=%s, demand=%s", (needle, needle))
    alerts = client.get("/family/family-link/alerts").json()
    assert alerts[0]["agency"] == needle and alerts[0]["demand"] == needle
    page = client.get("/family/family-link").text
    assert needle not in page


def test_family_list_is_bounded_with_stable_timestamp_ties(client, db):
    for _ in range(22):
        check(client, "spf", "transfer")
    with connect(db) as conn:
        conn.execute("update guardian_checks set created_at = timestamp '2026-10-01 00:00:00+00'")
    alerts = client.get("/family/family-link/alerts").json()
    assert [a["id"] for a in alerts] == list(range(22, 2, -1))


def test_family_private_link_does_not_grant_reviewer_access(client):
    for route in ("/", "/calls", "/patterns", "/reports", "/voice", "/calls/1", "/checks/1"):
        assert client.get(route).status_code == 401
    assert client.post("/web-call/session").status_code == 401


def test_family_preview_controls_use_owning_script_and_fakes(client, db, monkeypatch):
    from scamkaki.app import main
    from scripts.preview_ui import preview

    monkeypatch.setattr(main.templates.env, "loader", main.templates.env.loader)
    preview("populated", True)
    page = client.get("/family/preview-family").text
    assert 'id="family-preview-controls"' in page
    assert "padding:0 18px;overflow-wrap:anywhere" in page
    assert "window.scamkakiFamilyPreview" in page
    assert "class PreviewAudio" in page
    assert "window.AudioContext = PreviewAudio" in page
    assert "function check()" in page
    assert 'id="preview-family-empty"' in page
    assert 'id="preview-family-failed"' in page
    assert 'id="preview-family-new"' in page
    assert page.index("window.scamkakiFamilyPreview") < page.index("const AGENCIES")
    assert client.get("/family/preview-family/alerts").json()
    assert main.app.state.preview_bolna.sessions == []
    assert main.app.state.preview_bolna.fetched == []
    assert main.app.state.preview_telegram.sent == []


@pytest.mark.parametrize(
    "acted,urgent",
    [
        ("paid", True),
        ("gave_code_or_card", True),
        ("installed_app", True),
        ("none", False),
        ("unsure", False),
    ],
)
def test_family_harmful_acted_urgency_is_preserved(client, acted, urgent):
    check(client, "courier", "card_details", tactics="link_fee", acted=acted)
    alerts = client.get("/family/family-link/alerts").json()
    assert alerts[0]["acted"] == acted
    assert alerts[0]["urgent"] is urgent


def test_family_preview_includes_stored_nonurgent_fixture(client, db):
    from scripts.preview_ui import fixture_rows

    fixture_rows(db)
    alerts = client.get("/family/family-link/alerts").json()
    assert any(a["urgent"] is False and a["language"] == "hi" for a in alerts)
