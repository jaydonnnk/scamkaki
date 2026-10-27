"""Check the fixture calls the synthetic caller placed, and print pass rates.

Usage: uv run python scripts/check.py bait|guardian [--language hi]

Both take the latest call per case and line logged in scripts/caller/runs.jsonl and re-read
the execution from Bolna and the stored rows from DATABASE_URL. Fixture results only.

bait: for each bait case, whether Ah Ma Bait's extraction caught the planted payee and whether
Ah Ma leaked anything. Before trusting "no leaks" on a real transcript, it injects a
spelled-out code into a copy of that transcript and requires the leak guard to find it.
Exit status 1 below 4 of 5 payees (Hindi: 1 of 2) or on any leak.

guardian: for every guardian case, Guardian's logged check (found by execution id, else by the
call's time window), its verdict, similar_count, family alert status, and whether Ah Ma said the
repeat-script sentence. Exit status 1 when scams flagged likely_scam fall below 7 of 8
(Hindi: 2 of 2), legit cases flagged exceed 1 of 4 (Hindi: 0 of 1), or any likely_scam check
lacks a sent alert or any other check has one.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

from scamkaki.domain import store
from scamkaki.domain.extraction import parse_extraction
from scamkaki.domain.leaks import agent_turns, find_leaks
from scamkaki.integrations.bolna import BolnaClient
from scamkaki.lib.db import connect
from scamkaki.lib.env import get_settings

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "scripts" / "caller" / "runs.jsonl"
NEEDLE = "assistant: Ok ok, the code is\nfour eight two nine one three.\n"
PAYEE_THRESHOLD = {"en": 4, "hi": 1}
# (at least this many scams flagged, at most this many legit cases flagged)
GUARDIAN_THRESHOLD = {"en": (7, 1), "hi": (2, 0)}
# What Guardian says when Bait heard the same script this week (verdict.sentence_for).
REPEAT_PHRASE = {"en": "Same script heard", "hi": "इस हफ़्ते"}


def digits(text: str | None) -> str:
    return re.sub(r"\D", "", text or "")


def latest_runs(line: str) -> dict[str, dict]:
    runs: dict[str, dict] = {}
    if RUNS.exists():
        for text in RUNS.read_text().splitlines():
            record = json.loads(text)
            # Runs logged before S5 have no line; they were all Bait calls.
            if record.get("run_id") and record.get("line", "bait") == line:
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
    cases = [c for c in cases if c["for"] == "bait" and c["language"] == language]
    runs = latest_runs("bait")
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


def guardian_check(database_url: str, run: dict) -> tuple[dict | None, str]:
    """The check Guardian logged during this call: by execution id, else by time window."""
    with connect(database_url) as conn:
        rows = conn.execute(
            "select * from guardian_checks where execution_id = %s order by id", (run["run_id"],)
        ).fetchall()
        if rows:
            return rows[-1], "id" if len(rows) == 1 else f"id x{len(rows)}"
        started = datetime.fromisoformat(run["started_at"])
        ended = datetime.fromisoformat(run["ended_at"]) + timedelta(seconds=5)
        rows = conn.execute(
            """
            select * from guardian_checks
            where execution_id is null and created_at between %s and %s order by id
            """,
            (started, ended),
        ).fetchall()
    if not rows:
        return None, "none"
    return rows[-1], "time" if len(rows) == 1 else f"time x{len(rows)}"


def repeat_excerpt(transcript: str, language: str) -> str | None:
    for turn in agent_turns(transcript):
        if REPEAT_PHRASE[language] in turn:
            return " ".join(turn.split())
    return None


def check_guardian(language: str) -> int:
    settings = get_settings()
    bolna = BolnaClient(settings.bolna_api_key)
    cases = json.loads((ROOT / "seed" / "scripts.json").read_text())["cases"]
    cases = [c for c in cases if c["for"] == "guardian" and c["language"] == language]
    runs = latest_runs("guardian")
    flagged = {"scam": 0, "legit": 0}
    alert_errors = 0
    print("Demo fixtures: scripted synthetic senior, not real seniors or real scam calls.")
    with connect(settings.database_url) as conn:
        library = store.scripts_this_week(conn)
    print(
        "Bait scripts this week:",
        ", ".join(f"{g['agency']}/{g['demand']} x{g['n']}" for g in library) or "none",
    )
    header = (
        "case",
        "kind",
        "execution",
        "secs",
        "link",
        "agency/demand",
        "verdict",
        "N",
        "alert",
        "said N",
    )
    print("{:<20}{:<7}{:<38}{:>5}  {:<8}{:<24}{:<15}{:<3}{:<8}{}".format(*header))
    for case in cases:
        run = runs.get(case["id"])
        if run is None:
            print(f"{case['id']:<20}{case['kind']:<7}{'(no call logged)'}")
            continue
        execution = bolna.get_execution(run["run_id"])
        transcript = execution.get("transcript") or ""
        check, link = guardian_check(settings.database_url, run)
        secs = execution.get("conversation_duration") or 0
        if check is None:
            print(
                f"{case['id']:<20}{case['kind']:<7}{run['run_id']:<38}{secs:>5.0f}"
                f"  {link:<8}(no check logged)"
            )
            continue
        likely = check["verdict"] == "likely_scam"
        flagged[case["kind"]] += likely
        alert_ok = (check["alert_status"] == "sent") == likely
        alert_errors += not alert_ok
        excerpt = repeat_excerpt(transcript, language)
        said = "yes" if excerpt else ("no" if check["similar_count"] else "-")
        pair = f"{check['agency']}/{check['demand']}"
        print(
            f"{case['id']:<20}{case['kind']:<7}{run['run_id']:<38}{secs:>5.0f}  {link:<8}{pair:<24}"
            f"{check['verdict']:<15}{check['similar_count']:<3}"
            f"{(check['alert_status'] or '-') + ('' if alert_ok else '!'):<8}{said}"
        )
        if excerpt:
            print(f"    Ah Ma: {excerpt}")
    scams = sum(c["kind"] == "scam" for c in cases)
    legit = len(cases) - scams
    need_scam, max_legit = GUARDIAN_THRESHOLD[language]
    passed = flagged["scam"] >= need_scam and flagged["legit"] <= max_legit and not alert_errors
    print(
        f"scams flagged {flagged['scam']} of {scams} (need {need_scam}); legit flagged"
        f" {flagged['legit']} of {legit} (max {max_legit}); alert mismatches {alert_errors}"
        f" (need 0): {'PASS' if passed else 'FAIL'}"
    )
    return 0 if passed else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("line", choices=["bait", "guardian"])
    parser.add_argument("--language", choices=["en", "hi"], default="en")
    args = parser.parse_args()
    check = check_bait if args.line == "bait" else check_guardian
    sys.exit(check(args.language))


if __name__ == "__main__":
    main()
