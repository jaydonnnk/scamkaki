"""Domain vocabulary shared by the agents, the tool endpoint and the store."""

from dataclasses import dataclass
from typing import Literal, get_args

Agency = Literal[
    "spf",
    "ica",
    "china_official",
    "moh",
    "cpf",
    "mom",
    "iras",
    "mas",
    "minlaw",
    "bank",
    "telco",
    "courier",
    "investment",
    "employer",
    "friend_family",
    "other",
]
# cash_handover: cash, gold or valuables handed over or deposited at an ATM.
# card_details: card details or a bank login typed on a website.
Demand = Literal[
    "transfer",
    "cash_handover",
    "otp",
    "card_details",
    "app_install",
    "personal_info",
    "gift_card",
    "none",
    "other",
]
# How the caller reached the senior.
Channel = Literal["call", "sms", "whatsapp", "video", "website", "in_person", "other"]
# Warning signs the senior describes. handoff: passed to another officer or company;
# secrecy: told not to tell family or the bank; stay_on_line: keep the call or video on;
# channel_move: moved to WhatsApp, Telegram or video; paid_first: paid or shown profit first;
# link_fee: a small fee by link; new_payee: pay a different person or a changed account;
# urgency_threat: arrest, freeze or a deadline today; knew_details: already knew IC or card digits.
Tactic = Literal[
    "handoff",
    "secrecy",
    "stay_on_line",
    "channel_move",
    "paid_first",
    "link_fee",
    "new_payee",
    "urgency_threat",
    "knew_details",
]
# What the senior already did before calling Guardian.
Acted = Literal["none", "paid", "gave_code_or_card", "installed_app", "unsure"]
Verdict = Literal["likely_scam", "unclear", "no_scam_signs"]
Line = Literal["bait", "guardian"]
Language = Literal["en", "hi"]

AGENCIES: tuple[str, ...] = get_args(Agency)
DEMANDS: tuple[str, ...] = get_args(Demand)
CHANNELS: tuple[str, ...] = get_args(Channel)
TACTICS: tuple[str, ...] = get_args(Tactic)
ACTED: tuple[str, ...] = get_args(Acted)
LANGUAGES: tuple[str, ...] = get_args(Language)


LeakKind = Literal["nric", "otp_or_account_digits", "card"]


@dataclass(frozen=True)
class Extraction:
    """What Ah Ma Bait got the scammer to say."""

    agency: Agency
    demand: Demand
    payee_bank: str | None
    payee_account: str | None
    paynow_id: str | None
    url: str | None
    summary: str | None


@dataclass(frozen=True)
class GuardianReport:
    """What the senior told Guardian, as the Guardian agent passes it to match_script."""

    agency: Agency
    demand: Demand
    channel: Channel = "other"
    tactics: frozenset[Tactic] = frozenset()
    acted: Acted = "none"


@dataclass(frozen=True)
class Leak:
    """A secret-looking value Ah Ma said. The excerpt has every digit masked."""

    kind: LeakKind
    turn_index: int
    excerpt: str


@dataclass(frozen=True)
class MatchResult:
    verdict: Verdict
    similar_count: int
    say: str
    urgent: bool = False  # the senior already paid, gave a code or card, or installed an app


def as_agency(value: object) -> Agency:
    text = str(value or "").strip().lower()
    return text if text in AGENCIES else "other"  # type: ignore[return-value]


def as_demand(value: object) -> Demand:
    text = str(value or "").strip().lower()
    return text if text in DEMANDS else "other"  # type: ignore[return-value]


def as_channel(value: object) -> Channel:
    text = str(value or "").strip().lower()
    return text if text in CHANNELS else "other"  # type: ignore[return-value]


def as_tactics(value: object) -> frozenset[Tactic]:
    """Comma-separated warning signs; unknown ones are dropped, never guessed."""
    items = value if isinstance(value, list | tuple) else str(value or "").split(",")
    words = (str(item).strip().lower().replace(" ", "_") for item in items)
    return frozenset(word for word in words if word in TACTICS)  # type: ignore[misc]


def as_acted(value: object) -> Acted:
    text = str(value or "").strip().lower()
    return text if text in ACTED else "none"  # type: ignore[return-value]


def as_line(value: object) -> Line:
    return "bait" if str(value or "").strip().lower() == "bait" else "guardian"


def as_language(value: object) -> Language:
    text = str(value or "").strip().lower()
    return text if text in LANGUAGES else "en"  # type: ignore[return-value]
