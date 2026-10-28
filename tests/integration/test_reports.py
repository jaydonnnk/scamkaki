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
