"""What Guardian decides, says, and tells the family. Never says a call is safe."""

from datetime import datetime
from zoneinfo import ZoneInfo

from scamkaki.domain.types import (
    Acted,
    Agency,
    Channel,
    Demand,
    GuardianReport,
    Language,
    MatchResult,
    Tactic,
    Verdict,
)

GOV_AGENCIES: frozenset[Agency] = frozenset(
    {"spf", "ica", "china_official", "moh", "cpf", "mom", "iras", "mas", "minlaw"}
)
HARD_DEMANDS: frozenset[Demand] = frozenset(
    {"transfer", "cash_handover", "otp", "card_details", "app_install", "gift_card"}
)
# Legit callers rarely do these; any one alone means likely scam.
RED_TACTICS: frozenset[Tactic] = frozenset(
    {"handoff", "secrecy", "stay_on_line", "channel_move", "paid_first", "link_fee", "new_payee"}
)
# Real banks also know your details and warn of deadlines, so these only make it unclear.
WEAK_TACTICS: frozenset[Tactic] = frozenset({"urgency_threat", "knew_details"})
HARM_ACTED: frozenset[Acted] = frozenset({"paid", "gave_code_or_card", "installed_app"})

_HI_WARNINGS = " पैसे मत भेजिए। ओटीपी, यानी आपके फ़ोन पर आया हुआ गुप्त नंबर, किसी को मत बताइए।"

SAY: dict[Language, dict[Verdict, str]] = {
    "en": {
        "likely_scam": "This is likely a {scam_type}. I have alerted your family.",
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

# Said first when the senior already paid, gave a code or card, or installed an app.
ACT_NOW: dict[Language, str] = {
    "en": (
        "Call your bank now on the number on the back of your card, and call ScamShield at 1799. "
    ),
    "hi": (
        "अभी अपने बैंक को अपने कार्ड के पीछे लिखे नंबर पर फ़ोन कीजिए,"
        " और स्कैमशील्ड को एक सात नौ नौ पर फ़ोन कीजिए। "
    ),
}

# Added when a friend or family member asked for money with no red warning sign.
CALL_BACK: dict[Language, str] = {
    "en": " Call them back on the number you already have, not the one that contacted you.",
    "hi": (" उन्हें उसी नंबर पर वापस फ़ोन कीजिए जो आपके पास पहले से है, उस नंबर पर नहीं जिससे संपर्क हुआ।"),
}

_SIMILAR: dict[Language, str] = {
    "en": " Same script heard {times} this week.",
    "hi": " ऐसी ही कॉल इस हफ़्ते {n} बार आई है।",
}


def _times(n: int) -> str:
    return "1 time" if n == 1 else f"{n} times"


def _friend_money(report: GuardianReport) -> bool:
    return report.agency == "friend_family" and report.demand in HARD_DEMANDS


def decide(report: GuardianReport, similar_count: int) -> Verdict:
    if report.acted in HARM_ACTED:
        return "likely_scam"
    if report.tactics & RED_TACTICS:
        return "likely_scam"
    if _friend_money(report):
        return "unclear"
    if report.demand in HARD_DEMANDS:
        return "likely_scam"
    if report.agency in GOV_AGENCIES and report.demand == "personal_info":
        return "likely_scam"
    if report.tactics & WEAK_TACTICS or report.acted == "unsure" or similar_count >= 1:
        return "unclear"
    return "no_scam_signs"


def sentence_for(
    verdict: Verdict, report: GuardianReport, similar_count: int, language: Language = "en"
) -> str:
    if verdict == "likely_scam" and language == "en":
        say = SAY["en"]["likely_scam"].format(scam_type=scam_type(report))
    else:
        say = SAY[language][verdict]
    if report.acted in HARM_ACTED:
        say = ACT_NOW[language] + say
    if verdict == "unclear" and _friend_money(report):
        say += CALL_BACK[language]
    if similar_count >= 1:
        say += _SIMILAR[language].format(n=similar_count, times=_times(similar_count))
    return say


def unclear(language: Language = "en") -> MatchResult:
    """The fallback for any internal error, so the call never goes silent."""
    return MatchResult(verdict="unclear", similar_count=0, say=SAY[language]["unclear"])


def match(report: GuardianReport, similar_count: int, language: Language = "en") -> MatchResult:
    """similar_count is how many Bait scripts this week share the agency and demand."""
    verdict = decide(report, similar_count)
    return MatchResult(
        verdict,
        similar_count,
        sentence_for(verdict, report, similar_count, language),
        urgent=report.acted in HARM_ACTED,
    )


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
    "mas": "MAS",
    "minlaw": "Ministry of Law",
    "bank": "A bank",
    "telco": "A telco",
    "courier": "A courier",
    "investment": "An investment group",
    "employer": "A job or employer",
    "friend_family": "A friend or family member",
    "other": "Not clear",
}
DEMAND_LABELS: dict[Demand, str] = {
    "transfer": "Money transfer",
    "cash_handover": "Cash or valuables handed over",
    "otp": "An OTP code",
    "card_details": "Card details on a website",
    "app_install": "Install an app",
    "personal_info": "Personal details",
    "gift_card": "Gift cards",
    "none": "Nothing",
    "other": "Something else",
}
CHANNEL_LABELS: dict[Channel, str] = {
    "call": "Phone call",
    "sms": "SMS",
    "whatsapp": "WhatsApp",
    "video": "Video call",
    "website": "Website",
    "in_person": "In person",
    "other": "Not clear",
}
TACTIC_LABELS: dict[Tactic, str] = {
    "handoff": "Passed to another officer",
    "secrecy": "Told to keep it secret",
    "stay_on_line": "Told to stay on the line",
    "channel_move": "Moved to WhatsApp or video",
    "paid_first": "Paid or shown profit first",
    "link_fee": "Small fee by link",
    "new_payee": "Pay a different account",
    "urgency_threat": "Threat or deadline",
    "knew_details": "Already knew her details",
}
ACTED_LABELS: dict[Acted, str] = {
    "none": "Nothing yet",
    "paid": "Paid money",
    "gave_code_or_card": "Gave card details or a code",
    "installed_app": "Installed an app",
    "unsure": "Not sure",
}


def scam_type(report: GuardianReport) -> str:
    """Short plain label for the kind of scam, used in the spoken verdict."""
    label = AGENCY_LABELS[report.agency]
    if label.startswith("A "):
        label = label[2:]
    elif label.startswith("An "):
        label = label[3:]
    label = label.split(" (")[0]
    if report.agency in GOV_AGENCIES or report.agency in {"bank", "telco", "courier"}:
        return f"{label} impersonation scam"
    if report.agency == "investment":
        return "investment scam"
    if report.agency == "employer":
        return "job scam"
    if report.agency == "friend_family":
        return "friend or family money scam"
    return "scam"


LANGUAGE_LABELS: dict[Language, str] = {"en": "English", "hi": "Hindi"}


def tactic_labels(tactics: frozenset[Tactic]) -> list[str]:
    """Warning-sign labels in a fixed order, so messages read the same every time."""
    return [label for tactic, label in TACTIC_LABELS.items() if tactic in tactics]


def alert_text(report: GuardianReport, language: Language, similar_count: int, at: datetime) -> str:
    urgent = report.acted in HARM_ACTED
    lines = ["[Demo fixture] Ah Ma Guardian: likely scam call"]
    if urgent:
        lines.append(f"URGENT: Ah Ma already: {ACTED_LABELS[report.acted]}")
    lines += [
        f"Contacted by: {CHANNEL_LABELS[report.channel]}",
        f"Caller claimed to be: {AGENCY_LABELS[report.agency]}",
        f"Asked for: {DEMAND_LABELS[report.demand]}",
    ]
    if report.tactics:
        lines.append(f"Warning signs: {', '.join(tactic_labels(report.tactics))}")
    lines.append(f"Line: {LANGUAGE_LABELS[language]}, {at.astimezone(SGT):%d %b %H:%M}")
    if similar_count >= 1:
        lines.append(f"Same script heard {_times(similar_count)} this week.")
    if urgent:
        lines.append(
            "Call Ah Ma now. Help her call the bank on the number on the back of her card."
        )
    else:
        lines.append("Please call Ah Ma now.")
    return "\n".join(lines)
