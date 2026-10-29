import json
from datetime import UTC, datetime

import pytest

from scamkaki.domain.types import GuardianReport
from scamkaki.domain.verdict import (
    HARD_DEMANDS,
    RED_TACTICS,
    SAY,
    alert_text,
    decide,
    match,
    scam_type,
    sentence_for,
)
from tests.conftest import ROOT

# Words that would tell a senior a call is safe, per language.
SAFE_WORDS = {"en": ("safe",), "hi": ("सुरक्षित", "सेफ")}
HI_WARNINGS = (
    "पैसे मत भेजिए",
    "ओटीपी, यानी आपके फ़ोन पर आया हुआ गुप्त नंबर, किसी को मत बताइए",
    "परिवार",
)
AT = datetime(2026, 10, 24, 6, 2, tzinfo=UTC)


def report(agency="bank", demand="none", channel="call", tactics=(), acted="none"):
    return GuardianReport(agency, demand, channel, frozenset(tactics), acted)


@pytest.mark.parametrize("demand", sorted(HARD_DEMANDS))
def test_decide_hard_demand_is_likely_scam(demand):
    # A non-government caller with no warning signs, so only the hard-demand rule can fire.
    assert decide(report("courier", demand), 0) == "likely_scam"


@pytest.mark.parametrize(
    "agency", ["spf", "ica", "china_official", "moh", "cpf", "mom", "iras", "mas", "minlaw"]
)
def test_decide_gov_personal_info_is_likely_scam(agency):
    assert decide(report(agency, "personal_info"), 0) == "likely_scam"
    # The same ask from a bank or courier is not enough on its own.
    assert decide(report("bank", "personal_info"), 0) == "no_scam_signs"


@pytest.mark.parametrize("acted", ["paid", "gave_code_or_card", "installed_app"])
def test_decide_harmful_act_is_likely_scam(acted):
    assert decide(report("other", "none", acted=acted), 0) == "likely_scam"


@pytest.mark.parametrize("tactic", sorted(RED_TACTICS))
def test_decide_red_tactic_alone_is_likely_scam(tactic):
    assert decide(report("bank", "none", tactics=[tactic]), 0) == "likely_scam"


def test_decide_friend_money_without_red_tactic_is_unclear():
    assert decide(report("friend_family", "transfer"), 0) == "unclear"
    # A weak sign alone does not make a friend's request a likely scam.
    assert decide(report("friend_family", "transfer", tactics=["urgency_threat"]), 0) == "unclear"


def test_decide_friend_money_with_new_payee_is_likely_scam():
    assert decide(report("friend_family", "transfer", tactics=["new_payee"]), 0) == "likely_scam"


@pytest.mark.parametrize(
    "senior",
    [
        report("bank", "none", tactics=["knew_details"]),
        report("bank", "none", tactics=["urgency_threat"]),
        report("bank", "none", acted="unsure"),
    ],
)
def test_decide_weak_tactic_or_unsure_act_is_unclear(senior):
    assert decide(senior, 0) == "unclear"


def test_decide_repeat_script_is_unclear():
    assert decide(report("bank", "none"), 1) == "unclear"
    assert decide(report("other", "other"), 3) == "unclear"


def test_decide_no_signals_is_no_scam_signs():
    assert decide(report("bank", "none"), 0) == "no_scam_signs"
    assert decide(report("spf", "none"), 0) == "no_scam_signs"


GUARDIAN_CASES = [
    case
    for case in json.loads((ROOT / "seed" / "scripts.json").read_text())["cases"]
    if case["for"] == "guardian"
]


@pytest.mark.parametrize("case", GUARDIAN_CASES, ids=lambda case: case["id"])
def test_decide_matches_every_guardian_fixture(case):
    """Offline: proves the rule on each case's expected report, not what Bolna extracts."""
    expect = case["expect"]
    senior = report(
        expect["agency"], expect["demand"], expect["channel"], expect["tactics"], expect["acted"]
    )
    assert decide(senior, 0) == expect["verdict"]


@pytest.mark.parametrize("language", ["en", "hi"])
@pytest.mark.parametrize("verdict", ["likely_scam", "unclear", "no_scam_signs"])
@pytest.mark.parametrize("similar_count", [0, 2])
@pytest.mark.parametrize(
    "senior", [report(), report("friend_family", "transfer"), report(acted="paid")]
)
def test_sentence_never_says_safe(language, verdict, similar_count, senior):
    say = sentence_for(verdict, senior, similar_count, language)

    assert not any(word in say.lower() for word in SAFE_WORDS[language])
    if language == "hi":
        # Listener feedback (S2): the warnings must be explicit, not left to the LLM.
        assert all(warning in say for warning in HI_WARNINGS)


@pytest.mark.parametrize("language", ["en", "hi"])
def test_sentence_mentions_repeat_count_only_when_seen(language):
    assert sentence_for("unclear", report(), 0, language) == SAY[language]["unclear"]
    assert "2" in sentence_for("unclear", report(), 2, language)


def test_sentence_says_same_script_heard_this_week():
    assert sentence_for("likely_scam", report(), 3, "en").endswith(
        " Same script heard 3 times this week."
    )
    assert sentence_for("unclear", report(), 1, "en").endswith(
        " Same script heard 1 time this week."
    )
    assert sentence_for("unclear", report(), 2, "hi").endswith(" ऐसी ही कॉल इस हफ़्ते 2 बार आई है।")


@pytest.mark.parametrize(
    ("language", "first"),
    [
        ("en", "Call your bank now on the number on the back of your card, and call ScamShield"),
        ("hi", "अभी अपने बैंक को अपने कार्ड के पीछे लिखे नंबर पर फ़ोन कीजिए"),
    ],
)
def test_sentence_for_harmful_act_says_bank_and_1799_first(language, first):
    senior = report("courier", "card_details", "sms", ["link_fee"], "gave_code_or_card")
    result = match(senior, 0, language)

    assert result.verdict == "likely_scam"
    assert result.urgent is True
    assert result.say.startswith(first)
    assert ("1799" if language == "en" else "एक सात नौ नौ") in result.say
    base = SAY[language]["likely_scam"]
    if language == "en":
        base = base.format(scam_type=scam_type(senior))
    assert result.say.endswith(base)


def test_sentence_for_no_harmful_act_is_not_urgent():
    for acted in ("none", "unsure"):
        result = match(report("spf", "transfer", acted=acted), 0, "en")
        assert result.urgent is False
        assert "ScamShield" not in result.say


@pytest.mark.parametrize(
    ("language", "phrase"),
    [
        ("en", "Call them back on the number you already have"),
        ("hi", "उन्हें उसी नंबर पर वापस फ़ोन कीजिए"),
    ],
)
def test_sentence_for_friend_money_says_call_back_on_known_number(language, phrase):
    result = match(report("friend_family", "transfer"), 0, language)

    assert result.verdict == "unclear"
    assert phrase in result.say
    # Only for a friend's money request, never for other unclear calls.
    assert phrase not in match(report("bank", "none", tactics=["knew_details"]), 0, language).say


def test_alert_text_is_labeled_fixture_and_names_claim():
    text = alert_text(report("spf", "transfer"), "hi", 0, AT)

    assert text.startswith("[Demo fixture] Ah Ma Guardian: likely scam call")
    assert "Contacted by: Phone call" in text
    assert "Caller claimed to be: Police (SPF)" in text
    assert "Asked for: Money transfer" in text
    assert "Line: Hindi, 24 Oct 14:02" in text  # Singapore time
    assert "Same script" not in text
    assert "URGENT" not in text and "Warning signs" not in text
    assert text.endswith("Please call Ah Ma now.")


def test_alert_text_lists_warning_signs_in_a_fixed_order():
    text = alert_text(
        report("minlaw", "transfer", tactics=["stay_on_line", "handoff"]), "en", 0, AT
    )

    assert "Caller claimed to be: Ministry of Law" in text
    assert "Warning signs: Passed to another officer, Told to stay on the line" in text


def test_alert_text_marks_urgent_when_acted():
    senior = report("courier", "card_details", "sms", ["link_fee"], "gave_code_or_card")
    text = alert_text(senior, "en", 0, AT)

    assert text.splitlines()[1] == "URGENT: Ah Ma already: Gave card details or a code"
    assert "Contacted by: SMS" in text
    assert "Asked for: Card details on a website" in text
    assert text.endswith("Help her call the bank on the number on the back of her card.")


def test_alert_text_mentions_repeat_script_when_seen():
    text = alert_text(report("ica", "otp"), "en", 3, AT)

    assert "Same script heard 3 times this week." in text
    one = alert_text(report("ica", "otp"), "en", 1, AT)
    assert "Same script heard 1 time this week." in one
