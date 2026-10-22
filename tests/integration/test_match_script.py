from scamkaki.lib.db import connect


def test_match_script_rejects_bad_token(client, db):
    response = client.post(
        "/tools/match-script",
        json={"agency": "spf", "demand": "transfer"},
        headers={"Authorization": "Bearer wrong"},
    )

    assert response.status_code == 401
    with connect(db) as conn:
        assert conn.execute("select count(*) as n from guardian_checks").fetchone()["n"] == 0


def test_match_script_stub_answers_unclear_and_logs_check(client, db):
    response = client.post(
        "/tools/match-script",
        json={"agency": "SPF", "demand": "made-up"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "verdict": "unclear",
        "similar_count": 0,
        "say": "Not sure. Please call your family before doing anything.",
    }
    with connect(db) as conn:
        row = conn.execute("select agency, demand, verdict from guardian_checks").fetchone()
    assert row == {"agency": "spf", "demand": "other", "verdict": "unclear"}


def test_match_script_answers_in_hindi_for_hindi_line(client, db):
    response = client.post(
        "/tools/match-script",
        json={"agency": "spf", "demand": "transfer", "language": "hi"},
        headers={"Authorization": "Bearer tool-token"},
    )

    assert response.status_code == 200
    assert response.json()["verdict"] == "unclear"
    assert response.json()["say"] == "पक्का नहीं कह सकती। कुछ भी करने से पहले अपने परिवार को फ़ोन कीजिए।"
