import re
from html import unescape

import pytest

from scamkaki.domain import store
from scamkaki.domain.types import Extraction
from scamkaki.lib.db import connect
from tests.integration.test_calls import ADMIN
from tests.integration.test_checks import saved_check


def saved_script(conn, name, agency, demand, language="en", line="bait", days_ago=0):
    call_id = store.upsert_call(
        conn,
        execution_id=name,
        line=line,
        language=language,
        fixture_case=name,
        status="completed",
        duration_s=None,
        transcript="",
        extracted={},
    )
    script_id = store.add_script(
        conn, call_id, Extraction(agency, demand, None, None, None, None, None)
    )
    conn.execute(
        "update scripts set created_at = now() - make_interval(days => %s) where id = %s",
        (days_ago, script_id),
    )
    return call_id


@pytest.fixture
def pattern_groups(db):
    with connect(db) as conn:
        for n, language in enumerate(["en", "en", "en", "hi"]):
            call_id = saved_script(conn, f"bank-code-{n}", "bank", "otp", language)
        # Window belongs to the script record, not its parent call.
        conn.execute(
            "update calls set created_at = now() - interval '20 days' where id=%s", (call_id,)
        )
        for n in range(2):
            saved_script(conn, f"bank-transfer-{n}", "bank", "transfer", "hi")
        saved_script(conn, "courier-card", "courier", "card_details")
        saved_script(conn, "old-script", "spf", "personal_info", days_ago=8)
        saved_script(conn, "guardian-overlap", "bank", "otp", line="guardian")
        saved_script(conn, "guardian-only", "ica", "app_install", line="guardian")
    saved_check(db, agency="bank", demand="otp", similar_count=987)


def bars(page):
    rows = re.findall(r'<article class="pattern">(.*?)</article>', page, re.S)
    result = {}
    for row in rows:
        label = re.search(r'<span class="pattern-label">(.*?)</span>', row, re.S)[1]
        count = re.search(r'<strong class="pattern-count">(\d+) record', row)[1]
        width = re.search(r'class="barfill" style="width:([\d.]+)%"', row)[1]
        result[unescape(label)] = (int(count), float(width))
    return result


def test_patterns_show_only_seven_day_bait_groups(client, pattern_groups):
    response = client.get("/patterns", auth=ADMIN)
    assert response.status_code == 200
    assert bars(response.text) == {
        "A bank · An OTP code": (4, 100),
        "A bank · Money transfer": (2, 50),
        "A courier · Card details on a website": (1, 25),
    }
    assert "Police (SPF)" not in response.text and "ICA" not in response.text
    assert response.headers["cache-control"] == "no-store"
    assert "Demo fixtures. Test calls, not real scammers." in response.text
    assert "unique scammers" in response.text and "success rates" in response.text
    assert 'href="/family/' not in response.text


def test_patterns_expand_recorded_labels_languages_and_time(client, pattern_groups):
    page = client.get("/patterns", auth=ADMIN).text
    details = re.findall(r"<details>(.*?)</details>", page, re.S)
    assert len(details) == 3
    assert "Recorded group details" in details[0]
    assert "A bank" in details[0] and "An OTP code" in details[0]
    assert "English" in details[0] and "Hindi" in details[0]
    assert "Hindi" in details[1] and "English" not in details[1]
    assert "English" in details[2] and "Hindi" not in details[2]
    assert "4 Bait records" in details[0] and "2 Bait records" in details[1]
    assert "1 Bait record" in details[2]
    assert "Last recorded" in details[0] and "SGT" in details[0]
    assert "This explains the system. It does not link individual calls and checks." in page
    assert "Guardian check" in page and "Recorded signs and actions also matter." in page


def test_patterns_scale_against_largest_count_and_round(client, db):
    with connect(db) as conn:
        for n in range(3):
            saved_script(conn, f"top-{n}", "bank", "otp")
        for n in range(2):
            saved_script(conn, f"next-{n}", "bank", "transfer")
        saved_script(conn, "last", "courier", "card_details")
    assert bars(client.get("/patterns", auth=ADMIN).text) == {
        "A bank · An OTP code": (3, 100),
        "A bank · Money transfer": (2, 66.67),
        "A courier · Card details on a website": (1, 33.33),
    }


def test_patterns_has_no_group_limit(client, db):
    with connect(db) as conn:
        for agency in ["spf", "ica", "bank", "moh", "mom", "cpf", "iras", "courier"]:
            for demand in [
                "transfer",
                "otp",
                "app_install",
                "personal_info",
                "none",
                "other",
                "gift_card",
            ]:
                saved_script(conn, f"{agency}-{demand}", agency, demand)
    result = bars(client.get("/patterns", auth=ADMIN).text)
    assert len(result) == 56
    assert set(result.values()) == {(1, 100)}


def test_patterns_empty_has_no_bars_or_division_by_zero(client):
    response = client.get("/patterns", auth=ADMIN)
    assert response.status_code == 200
    assert "No Bait scripts in the last 7 days." in response.text
    assert '<article class="pattern">' not in response.text
    assert 'class="barfill"' not in response.text
    assert "nan%" not in response.text and "inf%" not in response.text
    assert response.headers["cache-control"] == "no-store"


def test_patterns_overview_links_and_counts_share_source(client, pattern_groups):
    overview = client.get("/", auth=ADMIN).text
    weekly = overview.split('aria-labelledby="week-h"')[1].split("</section>")[0]
    assert 'href="/patterns"' in weekly
    rows = re.findall(r"<tr>(.*?)</tr>", weekly, re.S)[1:]
    cells = [[unescape(v) for v in re.findall(r"<td[^>]*>(.*?)</td>", row)] for row in rows]
    assert cells == [
        ["A bank", "An OTP code", "4"],
        ["A bank", "Money transfer", "2"],
        ["A courier", "Card details on a website", "1"],
    ]
    for url in ["/", "/calls", "/patterns"]:
        page = client.get(url, auth=ADMIN).text
        nav = page.split('<nav aria-label="Reviewer navigation">')[1].split("</nav>")[0]
        assert 'href="/patterns"' in nav
        assert 'href="/reports"' not in nav and 'href="/voice"' not in nav
    assert 'href="/patterns" aria-current="page"' in client.get("/patterns", auth=ADMIN).text


@pytest.mark.parametrize("url", ["/patterns", "/"])
def test_patterns_escape_hostile_stored_values(client, db, url):
    with connect(db) as conn:
        saved_script(
            conn, "hostile-fixture", '<img src=x onerror="alert(1)">', "<script>alert(2)</script>"
        )
    page = client.get(url, auth=ADMIN).text
    if url == "/":
        page = page.split('aria-labelledby="week-h"')[1].split("</section>")[0]
    assert "&lt;img src=x onerror=" in page and "&lt;script&gt;alert(2)&lt;/script&gt;" in page
    assert '<img src=x onerror="alert(1)">' not in page
    assert "<script>alert(2)</script>" not in page
    assert "hostile-fixture" not in page  # Only grouping fields are projected.


def test_patterns_never_calls_providers(client, bolna, telegram):
    response = client.get("/patterns", auth=ADMIN)
    assert response.status_code == 200
    assert "<script src=" not in response.text and "data-line=" not in response.text
    assert bolna.fetched == [] and telegram.sent == []


def test_patterns_preview_fixture_counts(client, db):
    from scripts.preview_ui import fixture_rows

    fixture_rows(db)
    assert bars(client.get("/patterns", auth=ADMIN).text) == {
        "A courier · Card details on a website": (19, 100),
        "A bank · An OTP code": (4, 21.05),
        "A bank · Money transfer": (2, 10.53),
        "<script>fixture agency</script> · नमस्ते <img src=x onerror=alert(1)>": (1, 5.26),
    }
