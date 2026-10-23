"""What Guardian decides, says, and tells the family. Never says a call is safe."""

from datetime import datetime
from zoneinfo import ZoneInfo

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
            " I have alerted your family. Please wait for their call."
        ),
        "unclear": "Not sure. Please call your family before doing anything.",
        "no_scam_signs": (
            "No scam signs found in what you told me. Still, never move money or share"
            " a code because a caller asked. If anything feels wrong, call your family."
        ),
    },
    "hi": {
        "likely_scam": (
            "यह शायद धोखाधड़ी है।"
            + _HI_WARNINGS
            + " मैंने आपके परिवार को खबर कर दी है। उनके फ़ोन का इंतज़ार कीजिए।"
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


SGT = ZoneInfo("Asia/Singapore")

# Plain labels for the family, shared by the Telegram message and the family page.
AGENCY_LABELS: dict[Agency, str] = {
    "spf": "Police (SPF)",
    "ica": "ICA",
    "china_official": "China official",
    "moh": "MOH",
    "cpf": "CPF",
    "mom": "MOM",
    "iras": "IRAS",
    "bank": "A bank",
    "courier": "A courier",
    "other": "Not clear",
}
DEMAND_LABELS: dict[Demand, str] = {
    "transfer": "Money transfer",
    "otp": "An OTP code",
    "app_install": "Install an app",
    "personal_info": "Personal details",
    "gift_card": "Gift cards",
    "none": "Nothing",
    "other": "Something else",
}
LANGUAGE_LABELS: dict[Language, str] = {"en": "English", "hi": "Hindi"}


def alert_text(
    agency: Agency, demand: Demand, language: Language, similar_count: int, at: datetime
) -> str:
    lines = [
        "[Demo fixture] Ah Ma Guardian: likely scam call",
        f"Caller claimed to be: {AGENCY_LABELS[agency]}",
        f"Asked for: {DEMAND_LABELS[demand]}",
        f"Line: {LANGUAGE_LABELS[language]}, {at.astimezone(SGT):%d %b %H:%M}",
    ]
    if similar_count >= 1:
        lines.append(f"Same script heard {similar_count} times this week.")
    lines.append("Please call Ah Ma now.")
    return "\n".join(lines)
