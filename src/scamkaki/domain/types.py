"""Domain vocabulary shared by the agents, the tool endpoint and the store."""

from dataclasses import dataclass
from typing import Literal, get_args

Agency = Literal[
    "spf", "ica", "china_official", "moh", "cpf", "mom", "iras", "bank", "courier", "other"
]
Demand = Literal["transfer", "otp", "app_install", "personal_info", "gift_card", "none", "other"]
Verdict = Literal["likely_scam", "unclear", "no_scam_signs"]
Line = Literal["bait", "guardian"]
Language = Literal["en", "hi"]

AGENCIES: tuple[str, ...] = get_args(Agency)
DEMANDS: tuple[str, ...] = get_args(Demand)
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


def as_agency(value: object) -> Agency:
    text = str(value or "").strip().lower()
    return text if text in AGENCIES else "other"  # type: ignore[return-value]


def as_demand(value: object) -> Demand:
    text = str(value or "").strip().lower()
    return text if text in DEMANDS else "other"  # type: ignore[return-value]


def as_language(value: object) -> Language:
    text = str(value or "").strip().lower()
    return text if text in LANGUAGES else "en"  # type: ignore[return-value]
