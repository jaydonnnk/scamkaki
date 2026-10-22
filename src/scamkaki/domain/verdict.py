"""What Guardian decides and says, in the line's language. Never says a call is safe."""

from scamkaki.domain.types import Agency, Demand, Language, MatchResult, Verdict

GOV_AGENCIES: frozenset[Agency] = frozenset(
    {"spf", "ica", "china_official", "moh", "cpf", "mom", "iras"}
)
HARD_DEMANDS: frozenset[Demand] = frozenset({"transfer", "otp", "app_install", "gift_card"})

_HI_WARNINGS = " पैसे मत भेजिए। ओटीपी, यानी आपके फ़ोन पर आया हुआ गुप्त नंबर, किसी को मत बताइए।"

SAY: dict[Language, dict[Verdict, str]] = {
    "en": {
        "likely_scam": (
            "This is likely a scam. Do not transfer money or share any code."
            " I will connect you to your family now."
        ),
        "unclear": "Not sure. Please call your family before doing anything.",
        "no_scam_signs": (
            "No scam signs found in what you told me. Still, never move money or share"
            " a code because a caller asked. If anything feels wrong, call your family."
        ),
    },
    "hi": {
        "likely_scam": (
            "यह शायद धोखाधड़ी है।" + _HI_WARNINGS + " मैं अभी आपको आपके परिवार से जोड़ रही हूँ।"
        ),
        "unclear": (
            "पक्का नहीं कह सकती।" + _HI_WARNINGS + " कुछ भी करने से पहले अपने परिवार को फ़ोन कीजिए।"
        ),
        "no_scam_signs": (
            "आपकी बातों में धोखाधड़ी के निशान नहीं मिले। फिर भी किसी फ़ोन करने वाले के कहने पर"
            + _HI_WARNINGS
            + " कुछ भी अजीब लगे तो अपने परिवार को फ़ोन कीजिए।"
        ),
    },
}

_SIMILAR: dict[Language, str] = {
    "en": " The same kind of call was reported {n} times recently.",
    "hi": " ऐसी ही कॉल हाल में {n} बार आई है।",
}


def decide(agency: Agency, demand: Demand, similar_count: int) -> Verdict:
    if demand in HARD_DEMANDS:
        return "likely_scam"
    if agency in GOV_AGENCIES and demand == "personal_info":
        return "likely_scam"
    if similar_count >= 1:
        return "unclear"
    return "no_scam_signs"


def sentence_for(verdict: Verdict, similar_count: int, language: Language = "en") -> str:
    say = SAY[language][verdict]
    if similar_count >= 1:
        say += _SIMILAR[language].format(n=similar_count)
    return say


def unclear(language: Language = "en") -> MatchResult:
    """The fallback for any internal error, so the call never goes silent."""
    return MatchResult(verdict="unclear", similar_count=0, say=SAY[language]["unclear"])


def match(agency: Agency, demand: Demand, language: Language = "en") -> MatchResult:
    similar_count = 0  # S5 counts similar scripts from Bait's library.
    verdict = decide(agency, demand, similar_count)
    return MatchResult(verdict, similar_count, sentence_for(verdict, similar_count, language))
