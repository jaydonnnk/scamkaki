from scamkaki.domain.reports import draft_report
from scamkaki.domain.types import Extraction, Leak

EXTRACTION = Extraction("spf", "transfer", "OCBC", "000-123456-7", None, None, "Safety account.")


def test_draft_report_is_labeled_draft_and_fixture():
    text = draft_report(EXTRACTION, [], "en-spf-01")

    assert text.startswith("DRAFT - not sent.")
    assert "Demo fixture case en-spf-01" in text
    assert "Police (SPF)" in text and "Money transfer" in text
    assert "000-123456-7" in text
    assert "Leak check: Ah Ma said no" in text


def test_draft_report_without_case_says_unverified_and_shows_leaks():
    leaks = [Leak("otp_or_account_digits", 2, "my code is ######")]

    text = draft_report(EXTRACTION, leaks, None)

    assert text.startswith("DRAFT - not sent.")
    assert "not verified as a real scam call" in text
    assert "LEAK CHECK FAILED" in text and "otp_or_account_digits" in text
