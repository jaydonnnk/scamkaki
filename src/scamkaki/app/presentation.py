"""Project stored transcript markers without guessing missing speakers or turns."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class TranscriptTurn:
    speaker: Literal["ah_ma", "caller", "unlabelled"]
    text: str


def transcript_turns(transcript: str) -> list[TranscriptTurn]:
    if not transcript.strip():
        return []
    turns: list[TranscriptTurn] = []
    speaker: Literal["ah_ma", "caller", "unlabelled"] = "unlabelled"
    lines: list[str] = []
    for line in transcript.splitlines():
        marker, separator, text = line.partition(":")
        if separator and marker in ("assistant", "user"):
            if lines:
                turns.append(TranscriptTurn(speaker, "\n".join(lines)))
            speaker = "ah_ma" if marker == "assistant" else "caller"
            lines = [text.removeprefix(" ")]
        else:
            lines.append(line)
    if lines:
        turns.append(TranscriptTurn(speaker, "\n".join(lines)))
    return turns
