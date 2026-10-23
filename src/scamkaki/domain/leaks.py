"""Leak guard: did Ah Ma say an NRIC, a code, an account or a card number?

It scans only Ah Ma's own turns, after turning spoken digit words into digits, so
"one two three four five six" and "एक दो तीन चार पांच छह" count the same as "123456".
"""

import re
from collections.abc import Sequence

from scamkaki.domain.types import Leak, LeakKind

# Spoken digit words: English (also what Singlish speakers use), Hindi in Devanagari, and
# romanized Hindi as speech-to-text may write it.
DIGIT_WORDS: dict[str, str] = {
    **dict.fromkeys(["zero", "शून्य", "ज़ीरो", "जीरो", "shunya", "shoonya"], "0"),
    **dict.fromkeys(["one", "एक", "ek"], "1"),
    **dict.fromkeys(["two", "दो", "do"], "2"),
    **dict.fromkeys(["three", "तीन", "teen", "tin"], "3"),
    **dict.fromkeys(["four", "चार", "char", "chaar"], "4"),
    **dict.fromkeys(["five", "पांच", "पाँच", "paanch", "panch"], "5"),
    **dict.fromkeys(["six", "छह", "छः", "छे", "छै", "chhah", "chhe", "chah", "che"], "6"),
    **dict.fromkeys(["seven", "सात", "saat", "sat"], "7"),
    **dict.fromkeys(["eight", "आठ", "aath", "ath"], "8"),
    **dict.fromkeys(["nine", "नौ", "nau", "nao"], "9"),
}
REPEATS = {"double": 2, "डबल": 2, "triple": 3, "ट्रिपल": 3}
DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")

# Python's \b treats Devanagari vowel signs as non-word characters, so mark word edges
# explicitly: no letter, digit or Devanagari letter directly before or after. The danda
# (U+0964, U+0965) ends a sentence, so it counts as an edge.
_LETTER = r"\wऀ-ॣ०-ॿ"
_EDGE_BEFORE = rf"(?<![{_LETTER}])"
_EDGE_AFTER = rf"(?![{_LETTER}])"
_WORDS = "|".join(re.escape(w) for w in sorted(DIGIT_WORDS, key=len, reverse=True))
_DIGIT_WORD = re.compile(_EDGE_BEFORE + f"({_WORDS})" + _EDGE_AFTER, re.IGNORECASE)
_REPEAT = re.compile(
    _EDGE_BEFORE + "(" + "|".join(REPEATS) + r")\s+(\d)" + _EDGE_AFTER, re.IGNORECASE
)
# "one oh two": "oh" is zero only between two digits.
_OH = re.compile(r"(?<=\d)\s+oh\s+(?=\d)", re.IGNORECASE)
_RUN = re.compile(r"\d+(?:(?:[ \t\-]+|[,.] *)\d+)*")
_GROUP_SEP = re.compile(r"(\d+)")

NRIC = re.compile(r"(?<![A-Za-z0-9])[STFGM][ \-]*\d{7}[ \-]*[A-Z](?![A-Za-z0-9])", re.IGNORECASE)
CARD_DIGITS = range(13, 20)
MIN_SECRET_DIGITS = 6
_CONTEXT = 20


def _collapse(run: str) -> str:
    """Join digit groups read out together; keep "78, 1948" apart but join "1, 2, 3"."""
    parts = _GROUP_SEP.split(run)[1:-1]  # digit, sep, digit, sep, ..., digit
    out = previous = parts[0]
    for sep, group in zip(parts[1::2], parts[2::2], strict=True):
        joins = not sep.strip(" \t-") or len(group) == 1 or len(previous) == 1
        out += group if joins else sep + group
        previous = group
    return out


def normalize_spoken_digits(text: str) -> str:
    text = text.translate(DEVANAGARI_DIGITS)
    text = _DIGIT_WORD.sub(lambda m: DIGIT_WORDS[m.group(1).lower()], text)
    # Spaced, so "double five, six" reads as single digits and joins into one run.
    text = _REPEAT.sub(lambda m: " ".join(m.group(2) * REPEATS[m.group(1).lower()]), text)
    text = _OH.sub(" 0 ", text)
    return _RUN.sub(lambda m: _collapse(m.group(0)), text)


def agent_turns(transcript: str) -> list[str]:
    """Ah Ma's turns from a Bolna transcript ("assistant: ..." / "user: ..." lines)."""
    turns: list[str] = []
    speaker = None
    for line in transcript.splitlines():
        head, _, rest = line.partition(":")
        if head.strip().lower() in ("assistant", "user"):
            speaker = head.strip().lower()
            if speaker == "assistant":
                turns.append(rest.strip())
        elif speaker == "assistant" and line.strip():
            turns[-1] = f"{turns[-1]} {line.strip()}"
    return turns


def _excerpt(text: str, start: int, end: int) -> str:
    snippet = text[max(0, start - _CONTEXT) : end + _CONTEXT]
    return re.sub(r"\d", "#", snippet).strip()


def _nric_spans(text: str) -> list[tuple[int, int]]:
    return [m.span() for m in NRIC.finditer(text)]


def _is_card(digits: str) -> bool:
    return len(digits) in CARD_DIGITS


def _is_code_or_account(digits: str) -> bool:
    return len(digits) >= MIN_SECRET_DIGITS and not _is_card(digits)


def _turn_leaks(index: int, turn: str) -> list[Leak]:
    text = normalize_spoken_digits(turn)
    leaks: list[Leak] = []
    for start, end in _nric_spans(text):
        leaks.append(Leak("nric", index, _excerpt(text, start, end)))
        # The NRIC's own digits are not a second leak.
        text = text[:start] + "N" * (end - start) + text[end:]
    for match in re.finditer(r"\d+", text):
        kind: LeakKind | None = None
        if _is_card(match.group()):
            kind = "card"
        elif _is_code_or_account(match.group()):
            kind = "otp_or_account_digits"
        if kind:
            leaks.append(Leak(kind, index, _excerpt(text, *match.span())))
    return leaks


def find_leaks(agent_turns: Sequence[str]) -> list[Leak]:
    return [leak for i, turn in enumerate(agent_turns) for leak in _turn_leaks(i, turn)]
