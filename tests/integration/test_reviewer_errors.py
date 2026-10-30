import psycopg
import pytest

from scamkaki.domain import store
from tests.integration.test_calls import ADMIN


@pytest.mark.parametrize(
    "url,read",
    [
        ("/", "recent_feed"),
        ("/calls?q=Hindi&line=bait&page=2", "recent_calls"),
        ("/calls/1", "get_call"),
        ("/checks/1", "get_check"),
        ("/reports/1", "get_report"),
        ("/patterns", "scripts_this_week"),
        ("/", "scripts_this_week"),
    ],
)
def test_reviewer_read_failure_is_not_empty_data(client, monkeypatch, url, read):
    def failed(*args, **kwargs):
        raise psycopg.OperationalError("synthetic-private-database-error")

    monkeypatch.setattr(store, read, failed)
    response = client.get(url, auth=ADMIN)
    assert response.status_code == 503
    assert "Retry" in response.text and "unavailable" in response.text
    assert "No calls yet" not in response.text
    assert "No Bait scripts in the last 7 days." not in response.text
    assert "synthetic-private-database-error" not in response.text
    assert response.headers["cache-control"] == "no-store"
    assert url.replace("&", "&amp;") in response.text
