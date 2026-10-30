"""Voice routes use fake providers and no database connection."""

import re

import pytest
from fastapi.testclient import TestClient

from scamkaki.app import main
from scamkaki.lib.env import Settings, get_settings
from tests.support.fakes import FakeBolnaWithSessions, FakeTelegram

ADMIN = ("admin", "voice-test")
SDK = "https://cdn.jsdelivr.net/gh/bolna-ai/web-call@v3.0.1/dist/bolna-web-call.min.js"


@pytest.fixture
def voice_client(monkeypatch):
    settings = Settings(
        _env_file=None,
        database_url="postgresql://unused.invalid/never-connect",
        bolna_api_key="offline-only",
        bolna_webhook_token="hook-test",
        bolna_tool_token="tool-test",
        admin_password="voice-test",
        family_link_token="voice-family-test",
        bolna_guardian_agent_id="private-guardian-en",
        bolna_guardian_hi_agent_id="private-guardian-hi",
        bolna_bait_agent_id="private-bait-en",
        bolna_bait_hi_agent_id="private-bait-hi",
    )
    bolna, telegram = FakeBolnaWithSessions(), FakeTelegram()
    monkeypatch.setitem(main.app.dependency_overrides, get_settings, lambda: settings)
    monkeypatch.setitem(main.app.dependency_overrides, main.get_bolna, lambda: bolna)
    monkeypatch.setitem(main.app.dependency_overrides, main.get_telegram, lambda: telegram)

    def no_database(*args, **kwargs):
        raise AssertionError("Voice route must not open a database")

    monkeypatch.setattr(main, "connect", no_database)
    with TestClient(main.app) as client:
        yield client, settings, bolna, telegram


def test_voice_requires_admin_and_fails_closed_without_password(voice_client, monkeypatch):
    client, settings, bolna, _ = voice_client
    for auth in [None, ("admin", "wrong"), ("admin", "voice-family-test")]:
        assert client.get("/voice", auth=auth).status_code == 401
    monkeypatch.setitem(
        main.app.dependency_overrides,
        get_settings,
        lambda: settings.model_copy(update={"admin_password": ""}),
    )
    assert client.get("/voice", auth=("admin", "")).status_code == 401
    assert bolna.sessions == []


def test_voice_renders_disclosure_configuration_and_no_provider_effects(voice_client):
    client, settings, bolna, telegram = voice_client
    response = client.get("/voice", auth=ADMIN)
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    page = response.text
    assert "<title>Voice room | Scamkaki</title>" in page
    assert 'href="/voice" aria-current="page">Voice room</a>' in page
    assert page.count(f'<script src="{SDK}"></script>') == 1
    assert "microphone" in page and "account credit" in page
    assert "<noscript>" in page and "requires JavaScript" in page
    for persona in ["guardian", "bait"]:
        radio = re.search(rf'<input\b[^>]*id="{persona}"[^>]*>', page)[0]
        assert 'type="radio"' in radio and 'data-en="true"' in radio and 'data-hi="true"' in radio
        for language in ["en", "hi"]:
            assert settings.agent_id(persona, language) not in page
    assert 'lang="hi">हिंदी / Hindi</option>' in page
    assert re.search(r'<button\b[^>]*id="start"[^>]*disabled', page)
    assert re.search(r'<a\b[^>]*id="voice-results"[^>]*href="/calls"[^>]*hidden', page)
    assert bolna.sessions == [] and bolna.fetched == [] and telegram.sent == []


@pytest.mark.parametrize(
    "line,language,field",
    [
        ("guardian", "en", "bolna_guardian_agent_id"),
        ("guardian", "hi", "bolna_guardian_hi_agent_id"),
        ("bait", "en", "bolna_bait_agent_id"),
        ("bait", "hi", "bolna_bait_hi_agent_id"),
    ],
)
def test_voice_exposes_only_boolean_availability_and_session_stays_503(
    voice_client, monkeypatch, line, language, field
):
    client, settings, bolna, _ = voice_client
    monkeypatch.setitem(
        main.app.dependency_overrides, get_settings, lambda: settings.model_copy(update={field: ""})
    )
    response = client.get("/voice", auth=ADMIN)
    assert response.status_code == 200
    for persona in ["guardian", "bait"]:
        radio = re.search(rf'<input\b[^>]*id="{persona}"[^>]*>', response.text)[0]
        for lang in ["en", "hi"]:
            expected = "false" if (persona, lang) == (line, language) else "true"
            assert f'data-{lang}="{expected}"' in radio
    result = client.post(f"/web-call/session?line={line}&language={language}", auth=ADMIN, json={})
    assert result.status_code == 503 and result.json() == {"detail": "Agent not configured"}
    assert bolna.sessions == []


@pytest.mark.parametrize(
    "line,language,expected",
    [
        ("guardian", "en", "private-guardian-en"),
        ("guardian", "hi", "private-guardian-hi"),
        ("bait", "en", "private-bait-en"),
        ("bait", "hi", "private-bait-hi"),
    ],
)
def test_voice_preserves_session_query_body_and_response(voice_client, line, language, expected):
    client, _, bolna, telegram = voice_client
    response = client.post(
        f"/web-call/session?line={line}&language={language}",
        auth=ADMIN,
        json={"user_data": {"fixture_case": "s11-offline", "n": 2}},
    )
    assert response.status_code == 200 and response.json() == {"session": "fake"}
    assert bolna.sessions == [expected]
    assert bolna.user_data == [{"fixture_case": "s11-offline", "n": "2"}]
    assert bolna.fetched == [] and telegram.sent == []


def test_overview_no_longer_owns_voice_and_navigation_reaches_room(client):
    response = client.get("/", auth=("admin", "admin-pass"))
    assert response.status_code == 200
    assert SDK not in response.text and "new BolnaWebCall" not in response.text
    assert "data-line=" not in response.text and "Existing test lines" not in response.text
    assert 'href="/voice"' in response.text and 'id="refresh"' in response.text
    assert client.get("/voice", auth=("admin", "admin-pass")).status_code == 200
    family = client.get("/family/family-link").text
    assert 'aria-label="Reviewer navigation"' not in family and 'href="/voice"' not in family


@pytest.mark.parametrize("state", ["populated", "unconfigured"])
def test_preview_serves_fake_sdk_and_routes_sessions_to_fake_provider(
    client, db, monkeypatch, state
):
    from scripts.preview_ui import preview

    monkeypatch.setattr(main.templates.env, "loader", main.templates.env.loader)
    preview(state, True)
    page = client.get("/voice", auth=("admin", "preview-only")).text
    assert SDK not in page
    assert "Safe synthetic preview" in page
    assert "scamkakiVoicePreview" in page
    assert main.app.state.preview_bolna.sessions == []
    assert main.app.state.preview_telegram.sent == []
    response = client.post(
        "/web-call/session?line=bait&language=hi", auth=("admin", "preview-only"), json={}
    )
    if state == "unconfigured":
        assert response.status_code == 503
        assert main.app.state.preview_bolna.sessions == []
    else:
        assert response.status_code == 200 and response.json() == {"session": "fake"}
        assert main.app.state.preview_bolna.sessions == ["fake-bait-hi"]


def test_preview_refuses_missing_voice_sdk_anchor_before_migrations(monkeypatch):
    from pathlib import Path

    from scripts import preview_ui

    read_text = Path.read_text

    def altered_template(path, *args, **kwargs):
        text = read_text(path, *args, **kwargs)
        return text.replace(SDK, "changed-sdk") if path.name == "voice.html" else text

    def forbidden_migration(*args):
        raise AssertionError("Preview reached database before validating its SDK replacement")

    monkeypatch.setattr(Path, "read_text", altered_template)
    monkeypatch.setattr(preview_ui, "migrate", forbidden_migration)
    with pytest.raises(RuntimeError, match="Voice SDK"):
        preview_ui.preview("populated", True)
