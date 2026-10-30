import re
from datetime import UTC, datetime

import pytest

from scamkaki.domain import store
from scamkaki.lib.db import connect

ADMIN = ("admin", "admin-pass")


def saved_call(db, name="record", **fields):
    values = dict(
        execution_id=name,
        line="guardian",
        language="en",
        fixture_case=name,
        status="completed",
        duration_s=16,
        transcript="assistant: Hello\nuser: Help",
        extracted={"private": "raw-secret-synthetic"},
    )
    values.update(fields)
    with connect(db) as conn:
        return store.upsert_call(conn, **values)


def call_links(page):
    return [int(n) for n in re.findall(r'href="/calls/(\d+)"', page)]


def test_calls_search_and_line_filter_apply_before_paging(client, db):
    target = saved_call(db, "needle_%", line="bait", language="hi")
    saved_call(db, "needleAB", line="bait")
    saved_call(db, "needle_%guardian")
    with connect(db) as conn:
        conn.execute("update calls set created_at = now() - interval '2 hours'")
        for n in range(55):
            conn.execute(
                "insert into calls (execution_id, line, status, fixture_case) "
                "values (%s, 'guardian', 'failed', %s)",
                (f"new-{n}", f"new-{n}"),
            )
    page = client.get("/calls", params={"q": "needle_%", "line": "bait"}, auth=ADMIN)
    assert page.status_code == 200
    assert call_links(page.text) == [target]
    assert "needleAB" not in page.text and "needle_%guardian" not in page.text
    assert call_links(client.get("/calls?q=Hindi&line=bait", auth=ADMIN).text) == [target]
    assert call_links(client.get("/calls?q=failed&line=bait", auth=ADMIN).text) == []
    assert len(call_links(client.get("/calls?q=failed", auth=ADMIN).text)) == 50
    assert len(call_links(client.get("/calls?q=failed&line=", auth=ADMIN).text)) == 50
    assert "No matching calls" in client.get("/calls?q=absent", auth=ADMIN).text
    assert client.get("/calls", params={"q": "' OR 1=1 --"}, auth=ADMIN).status_code == 200
    with connect(db) as conn:
        rows = store.recent_calls(conn, query="Hindi", line="bait")
    assert len(rows) == 1
    assert not {"transcript", "extracted", "payee_account", "paynow_id"} & rows[0].keys()


def test_calls_paging_is_bounded_and_stable(client, db):
    with connect(db) as conn:
        for n in range(53):
            conn.execute(
                "insert into calls "
                "(execution_id, line, language, status, fixture_case, created_at) "
                "values (%s, 'bait', 'hi', 'stopped', %s, '2026-01-01T00:00:00Z')",
                (f"paging-{n}", f"paging-{n}"),
            )
    first = client.get("/calls?q=Hindi&line=bait", auth=ADMIN)
    second = client.get("/calls?q=Hindi&line=bait&page=2", auth=ADMIN)
    assert call_links(first.text) == list(range(53, 3, -1))
    assert call_links(second.text) == [3, 2, 1]
    assert "q=Hindi&amp;line=bait&amp;page=2" in first.text
    assert "q=Hindi&amp;line=bait&amp;page=1" in second.text
    assert 'rel="next"' not in second.text
    assert first.headers["cache-control"] == "no-store"
    for params in ({"page": 0}, {"page": 1001}, {"page": "bad"}, {"line": "all"}, {"q": "x" * 101}):
        assert client.get("/calls", params=params, auth=ADMIN).status_code == 422


def test_calls_keep_failed_records_and_missing_duration(client, db):
    ids = [
        saved_call(db, status, status=status, duration_s=duration)
        for status, duration in [("failed", None), ("stopped", 0), ("balance-low", 62)]
    ]
    page = client.get("/calls", auth=ADMIN)
    assert page.status_code == 200
    assert set(call_links(page.text)) == set(ids)
    assert "failed" in page.text and "stopped" in page.text and "balance-low" in page.text
    assert "not recorded" in page.text and "0 s" in page.text and "1 min 2 s" in page.text
    assert "Completed does not mean a passed check" in page.text
    assert "raw-secret-synthetic" not in page.text


def test_call_details_use_saved_time_and_escape_transcript(client, db):
    call_id = saved_call(
        db,
        "<img src=x onerror=alert(9)>",
        language="hi",
        duration_s=0,
        transcript="unlabelled\nassistant: <script>alert(1)</script>\ncontinued\nuser: नमस्ते",
    )
    with connect(db) as conn:
        conn.execute("update calls set created_at = %s", (datetime(2026, 1, 2, 3, 4, tzinfo=UTC),))
    response = client.get(f"/calls/{call_id}", auth=ADMIN)
    assert response.status_code == 200
    page = response.text
    assert "Recorded" in page and "02 Jan 11:04" in page and "SGT" in page
    assert "Started" not in page and "Ended" not in page
    assert "0 s" in page and "Ah Ma" in page and "Caller" in page
    assert "unlabelled" in page and "continued" in page and "नमस्ते" in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    assert "<script>alert(1)</script>" not in page and "<img src=x" not in page
    assert "&lt;img src=x" in page
    assert "raw-secret-synthetic" not in page
    assert "No verified check link" in page
    assert response.headers["cache-control"] == "no-store"
    missing = saved_call(db, "no-transcript", transcript=" \n ", duration_s=None, fixture_case=None)
    page = client.get(f"/calls/{missing}", auth=ADMIN).text
    assert "Transcript unavailable" in page and "not recorded" in page
    assert "no fixture case" in page
    assert "<audio" not in page


def test_bait_detail_links_only_its_actual_report(client, db):
    call_id = saved_call(db, "bait-detail", line="bait")
    other = saved_call(db, "other-bait", line="bait")
    with connect(db) as conn:
        store.add_report(conn, other, "unrelated draft")
    assert 'href="/reports/' not in client.get(f"/calls/{call_id}", auth=ADMIN).text
    with connect(db) as conn:
        own = store.add_report(conn, call_id, "own draft")
    assert f'href="/reports/{own}"' in client.get(f"/calls/{call_id}", auth=ADMIN).text


@pytest.mark.parametrize("url", ["/calls/0", "/calls/-1", "/checks/0", "/checks/-1"])
def test_reviewer_detail_ids_must_be_positive(client, url):
    assert client.get(url, auth=ADMIN).status_code == 422


def test_reviewer_missing_records_are_not_empty_collections(client):
    for url in ("/calls/999", "/checks/999"):
        response = client.get(url, auth=ADMIN)
        assert response.status_code == 404
        assert response.headers["cache-control"] == "no-store"
    assert "No calls yet" in client.get("/calls", auth=ADMIN).text


def test_empty_later_page_does_not_claim_empty_history(client, db):
    saved_call(db)
    for url in ("/calls?page=2", "/calls?q=record&page=2"):
        page = client.get(url, auth=ADMIN).text
        assert "No calls on this page" in page
        assert "No calls yet" not in page and "No matching calls" not in page
        assert 'rel="prev"' in page
