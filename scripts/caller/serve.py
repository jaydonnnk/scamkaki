"""Synthetic caller: plays a fixture case's scripted lines into a Bolna web call.

Usage: uv run python scripts/caller/serve.py   then open http://127.0.0.1:8765

Two modes per case: "bait" plays the scammer's caller_lines to Ah Ma Bait, "guardian" plays
the senior's senior_lines to Ah Ma Guardian. Renders the lines with macOS `say` (Daniel for
English, Lekha for Hindi), serves a local page that places a web call to the line's agent in
the case's language with the case id as user_data, and appends each placed call to
scripts/caller/runs.jsonl for scripts/check.py.
Every call it places costs Bolna credit. Binds to localhost only; the API key stays here.
"""

import json
import subprocess
from datetime import UTC, datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from scamkaki.integrations.bolna import BolnaClient
from scamkaki.lib.env import get_settings

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CLIPS = HERE / "clips"
RUNS = HERE / "runs.jsonl"
VOICES = {"en": "Daniel", "hi": "Lekha"}
# Words per minute; None keeps the voice default. Lekha at 190 garbled Sarvam's Hindi digits (S4).
RATES = {"en": "190", "hi": None}
PORT = 8765
# The scripted lines each line's agent hears, and the clip name suffix they render to.
LINES = {"bait": ("caller_lines", ""), "guardian": ("senior_lines", "-senior")}


def load_cases() -> dict[str, dict]:
    cases = json.loads((ROOT / "seed" / "scripts.json").read_text())["cases"]
    return {case["id"]: case for case in cases}


def clip_names(case: dict, line: str) -> list[str]:
    field, suffix = LINES[line]
    return [f"{case['id']}{suffix}-{i}.wav" for i in range(len(case.get(field) or []))]


def rate(language: str) -> list[str]:
    return ["-r", RATES[language]] if RATES[language] else []


def render_clips(cases: dict[str, dict]) -> None:
    CLIPS.mkdir(exist_ok=True)
    for case in cases.values():
        for line, (field, _) in LINES.items():
            for name, text in zip(clip_names(case, line), case.get(field) or [], strict=True):
                wav = CLIPS / name
                if wav.exists():
                    continue
                aiff = wav.with_suffix(".aiff")
                voice = ["-v", VOICES[case["language"]], *rate(case["language"])]
                subprocess.run(["say", *voice, "-o", aiff, text], check=True)
                subprocess.run(
                    ["afconvert", "-f", "WAVE", "-d", "LEI16@16000", aiff, wav], check=True
                )
                aiff.unlink()


class Handler(SimpleHTTPRequestHandler):
    cases: dict[str, dict] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def _json(self, status: int, body: object) -> None:
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/cases":
            return self._json(
                200,
                [
                    {
                        "id": case["id"],
                        "language": case["language"],
                        "line": line,
                        "clips": [f"/clips/{name}" for name in names],
                    }
                    for line in LINES
                    for case in self.cases.values()
                    for names in [clip_names(case, line)]
                    if names
                ],
            )
        return super().do_GET()

    def do_POST(self):
        url = urlparse(self.path)
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        if url.path == "/session":
            query = parse_qs(url.query)
            case = self.cases.get(query.get("case", [""])[0])
            line = query.get("line", ["bait"])[0]
            if case is None or line not in LINES or not clip_names(case, line):
                return self._json(404, {"error": "unknown case or line"})
            settings = get_settings()
            agent_id = settings.agent_id(line, case["language"])
            if not agent_id:
                return self._json(503, {"error": f"{line} agent id not set"})
            session = BolnaClient(settings.bolna_api_key).mint_web_call_session(
                agent_id, {"fixture_case": case["id"]}
            )
            return self._json(200, session)
        if url.path == "/log":
            record = {**json.loads(body or b"{}"), "logged_at": datetime.now(UTC).isoformat()}
            with RUNS.open("a") as runs:
                runs.write(json.dumps(record) + "\n")
            return self._json(200, {"ok": True})
        return self._json(404, {"error": "not found"})


def main() -> None:
    Handler.cases = load_cases()
    render_clips(Handler.cases)
    print(f"Synthetic caller on http://127.0.0.1:{PORT} ({len(Handler.cases)} cases)", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
