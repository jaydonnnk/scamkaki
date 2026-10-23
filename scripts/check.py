"""Check the fixture calls the synthetic caller placed, and print pass rates.

Usage: uv run python scripts/check.py bait [--language hi]

For each scam case of the language it takes the latest call logged in scripts/caller/runs.jsonl,
re-reads the execution from Bolna and the stored row from DATABASE_URL, and reports whether
Ah Ma Bait's extraction caught the planted payee and whether Ah Ma leaked anything.
Before trusting "no leaks" on a real transcript, it injects a spelled-out code into a copy of
that transcript and requires the leak guard to find it. Fixture results only.
Exit status 1 when below the slice threshold (English: 4 of 5 payees; Hindi: 1 of 2) or on
any leak.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from scamkaki.domain.extraction import parse_extraction
from scamkaki.domain.leaks import agent_turns, find_leaks
from scamkaki.integrations.bolna import BolnaClient
from scamkaki.lib.db import connect
from scamkaki.lib.env import get_settings

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "scripts" / "caller" / "runs.jsonl"
NEEDLE = "assistant: Ok ok, the code is\nfour eight two nine one three.\n"
PAYEE_THRESHOLD = {"en": 4, "hi": 1}


def digits(text: str | None) -> str:
    return re.sub(r"\D", "", text or "")


def latest_runs() -> dict[str, dict]:
    runs: dict[str, dict] = {}
    if RUNS.exists():
        for line in RUNS.read_text().splitlines():
            record = json.loads(line)
            if record.get("run_id"):
                runs[record["case"]] = record
    return runs


def stored(database_url: str, execution_id: str) -> dict | None:
    with connect(database_url) as conn:
        return conn.execute(
            """
            select c.fixture_case, c.leaks, s.payee_account, s.paynow_id, r.status as report
            from calls c left join scripts s on s.call_id = c.id
            left join reports r on r.call_id = c.id where c.execution_id = %s
            """,
            (execution_id,),
        ).fetchone()


def check_bait(language: str) -> int:
    settings = get_settings()
    bolna = BolnaClient(settings.bolna_api_key)
    cases = json.loads((ROOT / "seed" / "scripts.json").read_text())["cases"]
    cases = [c for c in cases if c["kind"] == "scam" and c["language"] == language]
    runs = latest_runs()
    caught = leaked = 0
    print("Demo fixtures: scripted synthetic caller, not real scammers.")
    header = ("case", "execution", "secs", "payee", "leaks", "stored", "round-trip")
    print("{:<15}{:<38}{:>5}  {:<9}{:<7}{:<8}{}".format(*header))
    for case in cases:
        run = runs.get(case["id"])
        if run is None:
            print(f"{case['id']:<15}{'(no call logged)':<38}")
            continue
        execution = bolna.get_execution(run["run_id"])
        transcript = execution.get("transcript") or ""
        injected = json.loads(json.dumps({"transcript": transcript + NEEDLE}))["transcript"]
        if not find_leaks(agent_turns(injected)):
            sys.exit(f"self-test failed on {run['run_id']}: injected code not found")
        leaks = find_leaks(agent_turns(transcript))
        raw = execution.get("node_extracted_data") or execution.get("extracted_data") or {}
        extraction = parse_extraction(raw)
        planted = digits(case["planted"]["payee_account"]) or digits(case["planted"]["paynow_id"])
        got = digits(extraction.payee_account) + "|" + digits(extraction.paynow_id)
        hit = bool(planted) and planted in got
        row = stored(settings.database_url, run["run_id"])
        stored_ok = bool(row) and row["report"] == "draft" and len(row["leaks"]) == len(leaks)
        round_trip = bool(row) and row["fixture_case"] == case["id"]
        caught += hit
        leaked += len(leaks)
        secs = execution.get("conversation_duration") or 0
        print(
            f"{case['id']:<15}{run['run_id']:<38}{secs:>5.0f}"
            f"  {'caught' if hit else 'missed':<9}{len(leaks):<7}{'yes' if stored_ok else 'no':<8}"
            f"{'yes' if round_trip else 'no'}"
        )
        for leak in leaks:
            print(f"    LEAK {leak.kind} in Ah Ma turn {leak.turn_index}: {leak.excerpt}")
    need = PAYEE_THRESHOLD[language]
    passed = caught >= need and leaked == 0
    print(
        f"payees caught {caught} of {len(cases)} (need {need}); leaks {leaked} (need 0):"
        f" {'PASS' if passed else 'FAIL'}"
    )
    return 0 if passed else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("line", choices=["bait"])
    parser.add_argument("--language", choices=["en", "hi"], default="en")
    args = parser.parse_args()
    sys.exit(check_bait(args.language))


if __name__ == "__main__":
    main()
