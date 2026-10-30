import re
from html import unescape

import pytest

from scamkaki.domain import store
from scamkaki.domain.types import Extraction
from scamkaki.lib.db import connect
from tests.integration.test_dashboard import ADMIN
from tests.integration.test_webhook import BAIT_EXTRACTED, BAIT_TRANSCRIPT, bait_execution


def store_bait_call(client, bolna, execution_id="ex-r1", **fields):
    bolna.executions[execution_id] = bait_execution(execution_id, **fields)
    client.post("/bolna/webhook/hook-token", json={"id": execution_id, "status": "completed"})


def report_row(db):
    with connect(db) as conn:
        return conn.execute("select * from reports order by id").fetchone()


def review(client, report_id=1, **kwargs):
    return client.post(f"/reports/{report_id}/review", auth=ADMIN, follow_redirects=False, **kwargs)


def test_report_page_shows_the_draft_and_the_script_fields(client, bolna):
    store_bait_call(client, bolna)

    page = client.get("/reports/1", auth=ADMIN)

    assert page.status_code == 200
    assert "Draft only; nothing is sent automatically." in page.text
    assert "DRAFT, not reviewed" in page.text and "Mark reviewed" in page.text
    assert "Demo fixture case" in page.text.split("Draft text")[0]  # not only inside the draft
    assert "en-spf-01" in page.text.split("Draft text")[0]
    assert "OCBC" in page.text and "000-123456-7" in page.text
    assert "Police (SPF)" in page.text and "Money transfer" in page.text
    assert "16 s" in page.text
    assert "None found" in page.text


def test_report_page_escapes_what_the_caller_said(client, bolna):
    hostile = {
        "Scam script": {
            **BAIT_EXTRACTED["Scam script"],
            "summary": {"objective": None, "subjective": "<script>alert(1)</script>"},
        }
    }
    store_bait_call(client, bolna, extracted_data=hostile)

    page = client.get("/reports/1", auth=ADMIN).text

    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page


def test_report_page_flags_a_leak_and_an_unlabeled_test_call(client, bolna):
    leaky = BAIT_TRANSCRIPT + "assistant: Ok, the code is four eight two nine one three.\n"
    store_bait_call(client, bolna, transcript=leaky, context_details={})

    page = client.get("/reports/1", auth=ADMIN).text

    facts = page.split("Draft text")[0]  # the draft text repeats these words by itself
    assert "LEAK CHECK FAILED" in facts
    assert "no fixture case" in facts


def test_report_review_marks_reviewed_and_sends_nothing(client, bolna, telegram, db):
    store_bait_call(client, bolna)
    fetched_before = list(bolna.fetched)

    response = review(client)

    assert response.status_code == 303
    assert response.headers["location"] == "/reports/1"
    row = report_row(db)
    assert row["status"] == "reviewed" and row["reviewed_at"] is not None
    page = client.get("/reports/1", auth=ADMIN).text
    assert "Reviewed" in page and "Mark reviewed" not in page
    assert "DRAFT, not reviewed" not in page
    assert telegram.sent == []
    assert bolna.fetched == fetched_before


def test_report_review_twice_keeps_the_first_review_time(client, bolna, db):
    store_bait_call(client, bolna)
    review(client)
    first = report_row(db)["reviewed_at"]

    again = review(client)

    assert again.status_code == 303
    assert report_row(db)["reviewed_at"] == first


def test_reviewed_report_is_not_rewritten_when_bolna_redelivers_the_webhook(client, bolna, db):
    store_bait_call(client, bolna)
    review(client)
    reviewed = report_row(db)

    changed = {
        "Scam script": {
            **BAIT_EXTRACTED["Scam script"],
            "summary": {"objective": None, "subjective": "A different summary."},
        }
    }
    bolna.executions["ex-r1"] = bait_execution("ex-r1", extracted_data=changed)
    client.post("/bolna/webhook/hook-token", json={"id": "ex-r1", "status": "completed"})

    after = report_row(db)
    assert after["status"] == "reviewed"
    assert after["draft"] == reviewed["draft"] and "A different summary" not in after["draft"]
    assert after["reviewed_at"] == reviewed["reviewed_at"]


def test_report_unknown_id_is_not_found(client):
    assert client.get("/reports/999", auth=ADMIN).status_code == 404
    assert review(client, 999).status_code == 404


def test_report_pages_require_admin(client, bolna, telegram, db):
    store_bait_call(client, bolna)

    assert client.get("/reports/1").status_code == 401
    assert client.post("/reports/1/review", follow_redirects=False).status_code == 401
    assert client.post("/reports/1/review", auth=("admin", "wrong")).status_code == 401
    assert report_row(db)["status"] == "draft"
    assert telegram.sent == []


def test_report_review_refuses_a_cross_site_form_post(client, bolna, telegram, db):
    store_bait_call(client, bolna)

    response = review(client, headers={"Origin": "https://evil.example"})

    assert response.status_code == 403
    assert report_row(db)["status"] == "draft"
    assert telegram.sent == []


def test_report_review_accepts_a_same_origin_form_post(client, bolna, db):
    store_bait_call(client, bolna)

    response = review(client, headers={"Origin": "http://testserver"})

    assert response.status_code == 303
    assert report_row(db)["status"] == "reviewed"


def saved_report(conn, name, created_at, *, reviewed=False):
    call_id = store.upsert_call(
        conn,
        execution_id=name,
        line="bait",
        language="hi",
        fixture_case=name,
        status="completed",
        duration_s=None,
        transcript="",
        extracted={},
    )
    store.add_script(conn, call_id, Extraction("bank", "otp", None, None, None, None, None))
    report_id = store.add_report(conn, call_id, f"DEMO FIXTURE: {name}. Original draft.")
    conn.execute("update reports set created_at = %s where id = %s", (created_at, report_id))
    if reviewed:
        store.mark_reviewed(conn, report_id)
    return report_id, call_id


def test_report_entry_chooses_draft_then_reviewed_then_empty(client, db):
    empty = client.get("/reports", auth=ADMIN, follow_redirects=False)
    assert empty.status_code == 200
    assert "No reports yet." in empty.text
    assert 'aria-current="page">Reports</a>' in empty.text
    assert "Mark reviewed" not in empty.text and "Draft text" not in empty.text
    assert empty.headers["cache-control"] == "no-store"
    with connect(db) as conn:
        saved_report(conn, "older-reviewed", "2026-10-01T00:00:00Z", reviewed=True)
        saved_report(conn, "newer-reviewed", "2026-10-04T00:00:00Z", reviewed=True)
        saved_report(conn, "older-draft", "2026-10-02T00:00:00Z")
        saved_report(conn, "newest-draft", "2026-10-03T00:00:00Z")
    entry = client.get("/reports", auth=ADMIN, follow_redirects=False)
    assert entry.status_code == 303 and entry.headers["location"] == "/reports/4"
    assert entry.headers["cache-control"] == "no-store"
    with connect(db) as conn:
        store.mark_reviewed(conn, 3)
        store.mark_reviewed(conn, 4)
    fallback = client.get("/reports", auth=ADMIN, follow_redirects=False)
    assert fallback.status_code == 303 and fallback.headers["location"] == "/reports/2"
    assert fallback.headers["cache-control"] == "no-store"


@pytest.mark.parametrize("reviewed", [False, True])
def test_report_entry_breaks_equal_created_time_by_descending_id(client, db, reviewed):
    with connect(db) as conn:
        saved_report(conn, "tie-one", "2026-10-01T00:00:00Z", reviewed=reviewed)
        saved_report(conn, "tie-two", "2026-10-01T00:00:00Z", reviewed=reviewed)
    response = client.get("/reports", auth=ADMIN, follow_redirects=False)
    assert response.status_code == 303 and response.headers["location"] == "/reports/2"


def test_report_focused_layout_acknowledgment_and_source_call(client, bolna, db):
    with connect(db) as conn:
        store.upsert_call(
            conn,
            execution_id="unrelated-call",
            line="guardian",
            language="en",
            fixture_case="unrelated-fixture",
            status="failed",
            duration_s=None,
            transcript="",
            extracted={},
        )
    store_bait_call(client, bolna)
    response = client.get("/reports/1", auth=ADMIN)
    page = response.text
    assert response.status_code == 200 and response.headers["cache-control"] == "no-store"
    assert "<title>Reports | Scamkaki</title>" in page
    assert 'href="/reports" aria-current="page">Reports</a>' in page
    assert 'href="/calls/2"' in page and 'href="/calls/1"' not in page
    checkbox = re.search(r'<input\b[^>]*type="checkbox"[^>]*>', page)[0]
    assert 'id="review-confirm"' in checkbox and "required" in checkbox
    assert "name=" not in checkbox  # Native acknowledgment adds no server confirmation field.
    assert 'method="post" action="/reports/1/review"' in page
    assert "I have read this draft and checked its source." in page
    assert "Nothing is sent" in page and "Human review" in page


def test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped(client, db):
    with connect(db) as conn:
        report_id, _ = saved_report(conn, "hostile", "2026-10-01T00:00:00Z")
        conn.execute(
            "update scripts set agency=%s, demand=%s, payee_bank=%s, payee_account=%s, "
            "paynow_id=%s, url=%s, summary=%s",
            (
                "<b>agency</b>",
                "<b>demand</b>",
                "<b>bank</b>",
                "<b>account</b>",
                "<b>paynow</b>",
                "<b>url</b>",
                "नमस्ते <img src=x onerror=alert(1)>",
            ),
        )
        conn.execute(
            "update reports set draft=%s where id=%s", ("<script>draft</script>", report_id)
        )
    page = client.get("/reports/1", auth=ADMIN).text
    for value in ["agency", "demand", "bank", "account", "paynow", "url"]:
        assert f"&lt;b&gt;{value}&lt;/b&gt;" in page
        assert f"<b>{value}</b>" not in page
    assert "नमस्ते &lt;img src=x onerror=alert(1)&gt;" in page
    assert "&lt;script&gt;draft&lt;/script&gt;" in page and "<script>draft</script>" not in page
    assert "not recorded" in page  # Missing duration is never presented as zero.
    with connect(db) as conn:
        conn.execute(
            "update scripts set payee_bank=null,payee_account=null,paynow_id=null,"
            "url=null,summary=null"
        )
    missing = client.get("/reports/1", auth=ADMIN).text
    assert missing.count("not heard") == 4
    assert "Summary from the call" not in missing


def test_report_review_separates_status_time_from_original_draft(client, bolna, db):
    store_bait_call(client, bolna)
    original = report_row(db)["draft"]
    review(client)
    row = report_row(db)
    assert row["reviewed_at"] is not None
    with connect(db) as conn:
        conn.execute("update reports set reviewed_at='2026-10-30T01:02:03Z' where id=1")
    page = client.get("/reports/1", auth=ADMIN).text
    draft = re.search(r'<pre class="report-draft">(.*?)</pre>', page, re.S)[1]
    assert unescape(draft) == original
    assert 'id="review-status"' in page and "Reviewed" in page.split("Draft text")[0]
    assert "30 Oct 09:02 SGT" in page.split("Draft text")[0]
    assert "Mark reviewed" not in page and "review-confirm" not in page
    assert "does not confirm the allegation" in page


def test_report_entry_and_review_have_no_provider_effects(client, db, monkeypatch, telegram):
    from scamkaki.app import main
    from tests.support.fakes import FakeBolnaWithSessions

    bolna = FakeBolnaWithSessions()
    monkeypatch.setitem(main.app.dependency_overrides, main.get_bolna, lambda: bolna)
    with connect(db) as conn:
        saved_report(conn, "no-effects", "2026-10-01T00:00:00Z")
    assert client.get("/reports", auth=ADMIN).status_code == 200
    assert review(client).status_code == 303
    assert client.get("/reports/1", auth=ADMIN).status_code == 200
    assert review(client).status_code == 303
    assert bolna.fetched == [] and bolna.sessions == [] and telegram.sent == []


def test_reports_entry_does_not_hide_other_report_links(client, db):
    with connect(db) as conn:
        for n in range(3):
            saved_report(conn, f"report-{n}", f"2026-10-0{n + 1}T00:00:00Z")
    overview = client.get("/", auth=ADMIN).text
    activity = overview.split('aria-labelledby="feed-h"')[1].split("</section>")[0]
    for n in range(1, 4):
        assert f'href="/reports/{n}"' in activity
        detail = client.get(f"/calls/{n}", auth=ADMIN).text
        assert f'href="/reports/{n}"' in detail
    assert 'href="/voice"' not in overview


def test_reports_preview_has_hostile_draft_and_visible_leak_fixture(client, db):
    from scripts.preview_ui import fixture_rows

    fixture_rows(db)
    page = client.get("/reports/19", auth=ADMIN).text
    assert "LEAK CHECK FAILED: 1 found" in page
    assert "[masked synthetic fixture]" in page
    assert "Code or account digits: [masked synthetic fixture]" in page
    assert "नमस्ते" in page and "&lt;script&gt;fixture draft&lt;/script&gt;" in page
    assert "<script>fixture draft</script>" not in page
    assert 'href="/calls/55"' in page


def test_reports_reviewed_preview_uses_only_fakes_and_reviewed_fallback(client, db):
    from scamkaki.app import main
    from scripts.preview_ui import preview

    preview("reviewed", True)
    response = client.get("/reports", auth=("admin", "preview-only"), follow_redirects=False)
    assert response.status_code == 303 and response.headers["location"] == "/reports/19"
    with connect(db) as conn:
        assert (
            conn.execute("select count(*) as n from reports where status='draft'").fetchone()["n"]
            == 0
        )
        assert (
            conn.execute(
                "select count(*) as n from reports where reviewed_at is not null"
            ).fetchone()["n"]
            == 19
        )
    assert main.app.state.preview_bolna.fetched == []
    assert main.app.state.preview_bolna.sessions == []
    assert main.app.state.preview_telegram.sent == []
