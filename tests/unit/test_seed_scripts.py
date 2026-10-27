"""The fixture cases: counted, labeled, valid, and each scam plants the payee it expects."""

import json
import re
from collections import Counter

from scamkaki.domain.leaks import normalize_spoken_digits
from scamkaki.domain.types import ACTED, AGENCIES, CHANNELS, DEMANDS, TACTICS
from tests.conftest import ROOT

SEED = json.loads((ROOT / "seed" / "scripts.json").read_text())
CASES = SEED["cases"]


def digits(text: str | None) -> str:
    return re.sub(r"\D", "", text or "")


def test_seed_has_the_planned_cases_all_labeled():
    counts = Counter((case["for"], case["language"], case["kind"]) for case in CASES)
    assert counts == {
        ("bait", "en", "scam"): 5,
        ("bait", "hi", "scam"): 2,
        ("guardian", "en", "scam"): 8,
        ("guardian", "en", "legit"): 4,
        ("guardian", "hi", "scam"): 2,
        ("guardian", "hi", "legit"): 1,
    }
    assert len({case["id"] for case in CASES}) == len(CASES)
    assert "fixture" in SEED["label"].lower()
    for case in CASES:
        assert case["label"].startswith("Demo fixture")
        assert case["expect"]["agency"] in AGENCIES and case["expect"]["demand"] in DEMANDS


def test_each_scam_caller_says_its_planted_payee():
    for case in (c for c in CASES if c["for"] == "bait"):
        planted = case["planted"]
        payee = digits(planted["payee_account"]) or digits(planted["paynow_id"])
        spoken = digits(normalize_spoken_digits(" ".join(case["caller_lines"])))
        assert payee and payee in spoken, case["id"]
        assert planted["payee_account"] is None or planted["payee_account"].startswith("000-")


CONFIRM = {"en": "yes", "hi": "हाँ"}


GUARDIAN = [case for case in CASES if case["for"] == "guardian"]
# Words that make a scam easy to spot; the senior in a sophisticated scam never says them.
GIVEAWAYS = ("scam", "safety account", "safe account", "money laundering", "धोखाधड़ी", "स्कैम")


def test_guardian_cases_expect_a_full_valid_report():
    for case in GUARDIAN:
        expect = case["expect"]
        assert expect["agency"] in AGENCIES and expect["demand"] in DEMANDS, case["id"]
        assert expect["channel"] in CHANNELS and expect["acted"] in ACTED, case["id"]
        assert set(expect["tactics"]) <= set(TACTICS), case["id"]
        assert expect["verdict"] in ("likely_scam", "unclear", "no_scam_signs"), case["id"]
        assert (expect["verdict"] == "likely_scam") == (case["kind"] == "scam"), case["id"]
        assert "caller_lines" not in case, case["id"]
    for case in CASES:
        assert ("senior_lines" in case) == (case["for"] == "guardian"), case["id"]


def test_guardian_fixtures_avoid_giveaway_words():
    for case in GUARDIAN:
        said = " ".join(case["senior_lines"]).lower()
        assert not [word for word in GIVEAWAYS if word in said], case["id"]


def test_each_guardian_case_has_senior_lines_ending_in_a_yes():
    """Guardian repeats the story back and waits for a yes before it checks the script."""
    for case in GUARDIAN:
        lines = case["senior_lines"]
        assert len(lines) >= 3, case["id"]
        assert lines[-1].lower().startswith(CONFIRM[case["language"]]), case["id"]
        # The senior describes the call; no identifiers ride along.
        assert not re.search(r"\d{3,}", normalize_spoken_digits(" ".join(lines))), case["id"]
