from scamkaki.domain.extraction import parse_extraction, parse_guardian_report
from scamkaki.domain.types import GuardianReport


def test_parse_extraction_maps_unknown_agency_to_other():
    extraction = parse_extraction({"agency": "Interpol", "demand": "bitcoin"})

    assert extraction.agency == "other"
    assert extraction.demand == "other"


def test_parse_extraction_keeps_payee_fields():
    # Bolna disposition results: category -> name -> {objective, subjective, ...}.
    raw = {
        "Scam script": {
            "agency": {"objective": "spf", "subjective": None, "confidence": 0.9},
            "demand": {"objective": "transfer", "subjective": None},
            "payee_bank": {"objective": None, "subjective": "OCBC"},
            "payee_account": {"objective": None, "subjective": " 000-123456-7 "},
            "paynow_id": {"objective": None, "subjective": "not mentioned"},
            "url": {"objective": None, "subjective": ""},
            "summary": {"objective": None, "subjective": "Fake police, safety account."},
        }
    }

    extraction = parse_extraction(raw)

    assert extraction.agency == "spf"
    assert extraction.demand == "transfer"
    assert extraction.payee_bank == "OCBC"
    assert extraction.payee_account == "000-123456-7"
    assert extraction.paynow_id is None
    assert extraction.url is None
    assert extraction.summary == "Fake police, safety account."


def test_parse_extraction_accepts_flat_values_and_nothing():
    assert parse_extraction({"agency": "ICA", "paynow_id": "8000 0000"}).paynow_id == "8000 0000"
    empty = parse_extraction(None)
    assert (empty.agency, empty.demand, empty.payee_account) == ("other", "other", None)


def test_parse_guardian_report_drops_unknown_tactics_and_defaults_acted():
    senior = parse_guardian_report(
        {
            "agency": "MinLaw",
            "demand": "transfer",
            "channel": "WhatsApp",
            "tactics": " Handoff, secrecy,made-up, stay on line ,",
        }
    )

    assert senior == GuardianReport(
        "minlaw", "transfer", "whatsapp", frozenset({"handoff", "secrecy", "stay_on_line"}), "none"
    )


def test_parse_guardian_report_maps_unknown_values_and_nothing():
    assert parse_guardian_report(
        {"agency": "x", "demand": "y", "channel": "pigeon", "tactics": "", "acted": "maybe"}
    ) == GuardianReport("other", "other", "other", frozenset(), "none")
    assert parse_guardian_report(None) == GuardianReport("other", "other")
    assert parse_guardian_report({"acted": "Gave_Code_Or_Card"}).acted == "gave_code_or_card"
