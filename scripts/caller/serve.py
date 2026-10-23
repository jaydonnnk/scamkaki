"""Synthetic caller: plays a fixture case's scripted caller lines into a Bolna web call.

Usage: uv run python scripts/caller/serve.py   then open http://127.0.0.1:8765

Renders each case's caller_lines with macOS `say` (Daniel for English, Lekha for Hindi),
serves a local page that places a web call to the case's agent with the case id as
user_data, and appends each placed call to scripts/caller/runs.jsonl for scripts/check.py.
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
PORT = 8765


def load_cases() -> dict[str, dict]:
    cases = json.loads((ROOT / "seed" / "scripts.json").read_text())["cases"]
    return {case["id"]: case for case in cases if case.get("caller_lines")}


def render_clips(cases: dict[str, dict]) -> None:
    CLIPS.mkdir(exist_ok=True)
    for case in cases.values():
        for i, line in enumerate(case["caller_lines"]):
            wav = CLIPS / f"{case['id']}-{i}.wav"
            if wav.exists():
                continue
            aiff = wav.with_suffix(".aiff")
            subprocess.run(
                ["say", "-v", VOICES[case["language"]], "-r", "190", "-o", aiff, line], check=True
            )
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", aiff, wav], check=True)
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
                        "clips": [f"/clips/{case['id']}-{i}.wav" for i in range(len(lines))],
                    }
                    for case in self.cases.values()
                    for lines in [case["caller_lines"]]
                ],
            )
        return super().do_GET()

    def do_POST(self):
        url = urlparse(self.path)
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        if url.path == "/session":
            case = self.cases.get(parse_qs(url.query).get("case", [""])[0])
            if case is None:
                return self._json(404, {"error": "unknown case"})
            settings = get_settings()
            agent_id = settings.agent_id("bait", case["language"])
            if not agent_id:
                return self._json(503, {"error": "Bait agent id not set"})
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
