from datetime import UTC, datetime

import pytest

from scamkaki.domain.verdict import SAY, alert_text, decide, sentence_for

# Words that would tell a senior a call is safe, per language.
SAFE_WORDS = {"en": ("safe",), "hi": ("सुरक्षित", "सेफ")}
HI_WARNINGS = (
    "पैसे मत भेजिए",
    "ओटीपी, यानी आपके फ़ोन पर आया हुआ गुप्त नंबर, किसी को मत बताइए",
    "परिवार",
)


@pytest.mark.parametrize("demand", ["transfer", "otp", "app_install", "gift_card"])
def test_decide_hard_demand_is_likely_scam(demand):
    # A non-government caller, so only the hard-demand rule can fire.
    assert decide("courier", demand, 0) == "likely_scam"


@pytest.mark.parametrize("agency", ["spf", "ica", "china_official", "moh", "cpf", "mom", "iras"])
def test_decide_gov_personal_info_is_likely_scam(agency):
    assert decide(agency, "personal_info", 0) == "likely_scam"
    # The same ask from a bank or courier is not enough on its own.
    assert decide("bank", "personal_info", 0) == "no_scam_signs"


def test_decide_repeat_script_is_unclear():
    assert decide("bank", "none", 1) == "unclear"
    assert decide("other", "other", 3) == "unclear"


def test_decide_no_signals_is_no_scam_signs():
    assert decide("bank", "none", 0) == "no_scam_signs"
    assert decide("spf", "none", 0) == "no_scam_signs"


@pytest.mark.parametrize("language", ["en", "hi"])
@pytest.mark.parametrize("verdict", ["likely_scam", "unclear", "no_scam_signs"])
@pytest.mark.parametrize("similar_count", [0, 2])
def test_sentence_never_says_safe(language, verdict, similar_count):
    say = sentence_for(verdict, similar_count, language)

    assert not any(word in say.lower() for word in SAFE_WORDS[language])
    if language == "hi":
        # Listener feedback (S2): the warnings must be explicit, not left to the LLM.
        assert all(warning in say for warning in HI_WARNINGS)


@pytest.mark.parametrize("language", ["en", "hi"])
def test_sentence_mentions_repeat_count_only_when_seen(language):
    assert sentence_for("unclear", 0, language) == SAY[language]["unclear"]
    assert "2" in sentence_for("unclear", 2, language)


def test_sentence_says_same_script_heard_this_week():
    assert sentence_for("likely_scam", 3, "en").endswith(" Same script heard 3 times this week.")
    assert sentence_for("unclear", 1, "en").endswith(" Same script heard 1 time this week.")
    assert sentence_for("unclear", 2, "hi").endswith(" ऐसी ही कॉल इस हफ़्ते 2 बार आई है।")


def test_alert_text_is_labeled_fixture_and_names_claim():
    text = alert_text("spf", "transfer", "hi", 0, datetime(2026, 10, 24, 6, 2, tzinfo=UTC))

    assert text.startswith("[Demo fixture] Ah Ma Guardian: likely scam call")
    assert "Caller claimed to be: Police (SPF)" in text
    assert "Asked for: Money transfer" in text
    assert "Line: Hindi, 24 Oct 14:02" in text  # Singapore time
    assert "Same script" not in text
    assert text.endswith("Please call Ah Ma now.")


def test_alert_text_mentions_repeat_script_when_seen():
    text = alert_text("ica", "otp", "en", 3, datetime(2026, 10, 24, tzinfo=UTC))

    assert "Same script heard 3 times this week." in text
    one = alert_text("ica", "otp", "en", 1, datetime(2026, 10, 24, tzinfo=UTC))
    assert "Same script heard 1 time this week." in one
