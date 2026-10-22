"""What Guardian decides and says. Slice 1 is a stub that always answers "unclear"."""

from scamkaki.domain.types import MatchResult

UNCLEAR_SAY = "Not sure. Please call your family before doing anything."


def stub_match() -> MatchResult:
    return MatchResult(verdict="unclear", similar_count=0, say=UNCLEAR_SAY)
