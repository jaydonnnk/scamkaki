"""Demo backup: send a Guardian fixture's expected report straight to the match-script tool.

No voice call and no Bolna credit. Each run writes a labeled fixture check and, for a likely
scam, sends a real [Demo fixture] Telegram alert. Fixture results only, not a real conversation.

    uv run python scripts/demo_backup.py en-courier-paid-01 hi-courier-paid-01

The target is APP_BASE_URL unless --url is given; the token is BOLNA_TOOL_TOKEN.
"""

import argparse
import json
import sys
from pathlib import Path

import httpx

from scamkaki.lib.env import get_settings

SEED = Path(__file__).resolve().parents[1] / "seed" / "scripts.json"


def guardian_cases() -> dict[str, dict]:
    cases = json.loads(SEED.read_text())["cases"]
    return {case["id"]: case for case in cases if case["for"] == "guardian"}


def tool_body(case: dict) -> dict[str, str]:
    """The report a correct Guardian call would send for this fixture."""
    expect = case["expect"]
    return {
        "agency": expect["agency"],
        "demand": expect["demand"],
        "channel": expect["channel"],
        "tactics": ",".join(expect["tactics"]),
        "acted": expect["acted"],
        "language": case["language"],
    }


def main() -> None:
    cases = guardian_cases()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("case_ids", nargs="+", choices=sorted(cases), metavar="case_id")
    parser.add_argument("--url", help="Base URL; defaults to APP_BASE_URL")
    args = parser.parse_args()
    settings = get_settings()
    base = (args.url or settings.app_base_url).rstrip("/")
    if not base:
        sys.exit("Set APP_BASE_URL or pass --url.")
    failed = False
    for case_id in args.case_ids:
        case = cases[case_id]
        response = httpx.post(
            f"{base}/tools/match-script",
            json=tool_body(case),
            headers={"Authorization": f"Bearer {settings.bolna_tool_token}"},
            timeout=30,
        )
        if response.status_code != 200:
            print(f"{case_id}: HTTP {response.status_code}")
            failed = True
            continue
        result = response.json()
        ok = result.get("verdict") == case["expect"]["verdict"]
        failed |= not ok
        print(f"{case_id}: {result.get('verdict')} (urgent {result.get('urgent')})")
        print(f"  {result.get('say')}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
