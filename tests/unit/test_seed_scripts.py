"""The fixture cases: counted, labeled, valid, and each scam plants the payee it expects."""

import json
import re
from collections import Counter

from scamkaki.domain.leaks import normalize_spoken_digits
from scamkaki.domain.types import AGENCIES, DEMANDS
from tests.conftest import ROOT

SEED = json.loads((ROOT / "seed" / "scripts.json").read_text())
CASES = SEED["cases"]


def digits(text: str | None) -> str:
    return re.sub(r"\D", "", text or "")


def test_seed_has_the_planned_cases_all_labeled():
    counts = Counter((case["language"], case["kind"]) for case in CASES)
    assert counts == {("en", "scam"): 5, ("en", "legit"): 3, ("hi", "scam"): 2, ("hi", "legit"): 1}
    assert len({case["id"] for case in CASES}) == len(CASES)
    assert "fixture" in SEED["label"].lower()
    for case in CASES:
        assert case["label"].startswith("Demo fixture")
        assert case["expect"]["agency"] in AGENCIES and case["expect"]["demand"] in DEMANDS


def test_each_scam_caller_says_its_planted_payee():
    for case in (c for c in CASES if c["kind"] == "scam"):
        planted = case["planted"]
        payee = digits(planted["payee_account"]) or digits(planted["paynow_id"])
        spoken = digits(normalize_spoken_digits(" ".join(case["caller_lines"])))
        assert payee and payee in spoken, case["id"]
        assert planted["payee_account"] is None or planted["payee_account"].startswith("000-")


CONFIRM = {"en": "yes", "hi": "हाँ"}


def test_each_case_has_senior_lines_ending_in_a_yes():
    """Guardian repeats the story back and waits for a yes before it checks the script."""
    for case in CASES:
        lines = case["senior_lines"]
        assert len(lines) >= 3, case["id"]
        assert lines[-1].lower().startswith(CONFIRM[case["language"]]), case["id"]
        # The senior describes the call; no identifiers ride along.
        assert not re.search(r"\d{3,}", normalize_spoken_digits(" ".join(lines))), case["id"]
