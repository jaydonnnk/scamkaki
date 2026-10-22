from scamkaki.app.main import app, get_bolna
from scamkaki.lib.env import get_settings
from tests.support.fakes import FakeBolnaWithSessions

ADMIN = ("admin", "admin-pass")


def test_dashboard_requires_admin(client):
    assert client.get("/").status_code == 401
    assert client.get("/", auth=("admin", "wrong")).status_code == 401
    assert client.get("/", auth=ADMIN).status_code == 200


def test_web_call_session_requires_admin(client):
    bolna = FakeBolnaWithSessions()
    app.dependency_overrides[get_bolna] = lambda: bolna

    assert client.post("/web-call/session", json={}).status_code == 401
    assert bolna.sessions == []


def test_admin_locked_when_no_password_set(client, test_settings):
    app.dependency_overrides[get_settings] = lambda: test_settings.model_copy(
        update={"admin_password": ""}
    )

    assert client.get("/", auth=("admin", "")).status_code == 401


def test_bolna_endpoints_stay_open_to_bolna(client):
    assert client.get("/healthz").status_code == 200
    # Webhook and tool keep their own token checks, not the admin sign-in.
    assert (
        client.post("/bolna/webhook/hook-token", json={"id": "x", "status": "queued"}).status_code
        == 204
    )
