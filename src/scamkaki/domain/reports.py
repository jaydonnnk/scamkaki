"""Draft scam report text for a Bait call. Drafts only: a human reviews before anything is sent."""

from collections.abc import Sequence

from scamkaki.domain.types import Extraction, Leak
from scamkaki.domain.verdict import AGENCY_LABELS, DEMAND_LABELS

DRAFT_HEADER = (
    "DRAFT - not sent. A person must review this before anything goes to ScamShield,"
    " the police or a bank."
)


def draft_report(extraction: Extraction, leaks: Sequence[Leak], fixture_case: str | None) -> str:
    label = (
        f"Demo fixture case {fixture_case}: a scripted test call, not a real scammer."
        if fixture_case
        else "Test call with no fixture case: not verified as a real scam call."
    )
    lines = [
        DRAFT_HEADER,
        label,
        "",
        f"Caller claimed to be: {AGENCY_LABELS[extraction.agency]}",
        f"Caller wanted: {DEMAND_LABELS[extraction.demand]}",
        f"Payee bank: {extraction.payee_bank or 'not heard'}",
        f"Payee account: {extraction.payee_account or 'not heard'}",
        f"PayNow ID: {extraction.paynow_id or 'not heard'}",
        f"Link: {extraction.url or 'not heard'}",
        f"Summary: {extraction.summary or 'none'}",
        "",
    ]
    if leaks:
        kinds = ", ".join(sorted({leak.kind for leak in leaks}))
        count = len(leaks)
        lines.append(f"LEAK CHECK FAILED: Ah Ma may have said {count} secret value(s) ({kinds}).")
    else:
        lines.append("Leak check: Ah Ma said no NRIC, code, account or card number.")
    return "\n".join(lines)
