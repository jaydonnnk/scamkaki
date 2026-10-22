"""What Guardian decides and says. The stub always answers "unclear", in the line's language."""

from scamkaki.domain.types import Language, MatchResult

UNCLEAR_SAY: dict[Language, str] = {
    "en": "Not sure. Please call your family before doing anything.",
    "hi": (
        "पक्का नहीं कह सकती। पैसे मत भेजिए। ओटीपी किसी को मत बताइए।"
        " कुछ भी करने से पहले अपने परिवार को फ़ोन कीजिए।"
    ),
}


def stub_match(language: Language = "en") -> MatchResult:
    return MatchResult(verdict="unclear", similar_count=0, say=UNCLEAR_SAY[language])
