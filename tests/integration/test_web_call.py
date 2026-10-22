from scamkaki.app.main import app, get_bolna
from tests.conftest import GUARDIAN_AGENT
from tests.support.fakes import FakeBolnaWithSessions


def test_web_call_session_mints_for_guardian_agent(client):
    bolna = FakeBolnaWithSessions()
    app.dependency_overrides[get_bolna] = lambda: bolna

    response = client.post("/web-call/session", json={})

    assert response.status_code == 200
    assert response.json() == {"session": "fake"}
    assert bolna.sessions == [GUARDIAN_AGENT]
