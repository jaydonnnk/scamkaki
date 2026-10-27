"""Parse what Bolna extracted from a Bait call, and what Guardian heard from a senior."""

from collections.abc import Mapping
from typing import Any

from scamkaki.domain.types import (
    Extraction,
    GuardianReport,
    as_acted,
    as_agency,
    as_channel,
    as_demand,
    as_tactics,
)

TEXT_FIELDS = ("payee_bank", "payee_account", "paynow_id", "url", "summary")
# What an extraction LLM writes when the scammer never said it.
_EMPTY = {"", "none", "null", "n/a", "na", "unknown", "not mentioned", "not provided", "-"}


def _key(name: object) -> str:
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def _flatten(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Flat {field: value} from either a flat dict or Bolna's disposition results.

    Dispositions nest category -> name -> {"objective", "subjective", ...}; the objective
    (a fixed option) wins over the free-text subjective answer.
    """
    flat: dict[str, Any] = {}
    for name, value in raw.items():
        if isinstance(value, Mapping) and ("objective" in value or "subjective" in value):
            flat[_key(name)] = value.get("objective") or value.get("subjective")
        elif isinstance(value, Mapping):
            flat.update(_flatten(value))
        else:
            flat[_key(name)] = value
    return flat


def _text(value: object) -> str | None:
    if value is None or isinstance(value, Mapping | list):
        return None
    text = " ".join(str(value).split())
    return None if text.lower().strip(".") in _EMPTY else text


def parse_extraction(raw: Mapping[str, Any] | None) -> Extraction:
    """Unknown agencies and demands become "other"; missing text fields become None."""
    flat = _flatten(raw or {})
    return Extraction(
        agency=as_agency(flat.get("agency")),
        demand=as_demand(flat.get("demand")),
        **{field: _text(flat.get(field)) for field in TEXT_FIELDS},
    )


def parse_guardian_report(raw: Mapping[str, Any] | None) -> GuardianReport:
    """Unknown values become "other"; unknown warning signs are dropped; missing acted is none."""
    flat = _flatten(raw or {})
    return GuardianReport(
        agency=as_agency(flat.get("agency")),
        demand=as_demand(flat.get("demand")),
        channel=as_channel(flat.get("channel")),
        tactics=as_tactics(flat.get("tactics")),
        acted=as_acted(flat.get("acted")),
    )
