"""Local fixture preview. Explicit test settings and fake providers, never production.

Run from the repository root with --reset-test-db. This migrates/truncates TEST_DATABASE_URL.
"""

import argparse
import sys
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlsplit

import psycopg
import uvicorn
from jinja2 import ChoiceLoader, DictLoader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scamkaki.app import main  # noqa: E402
from scamkaki.domain import store  # noqa: E402
from scamkaki.domain.types import Extraction, GuardianReport, MatchResult  # noqa: E402
from scamkaki.lib.db import connect, migrate  # noqa: E402
from scamkaki.lib.env import Settings, get_settings  # noqa: E402
from tests.conftest import _test_database_url  # noqa: E402
from tests.support.fakes import FakeBolnaWithSessions, FakeTelegram  # noqa: E402


def fixture_rows(url: str) -> None:
    with connect(url) as conn:
        for n in range(56):
            bait = n % 3 == 0
            call_id = store.upsert_call(
                conn,
                execution_id=f"ui-fixture-{n}",
                line="bait" if bait else "guardian",
                language="hi" if n % 2 else "en",
                fixture_case=f"ui-fixture-{n:02d}",
                status=["failed", "stopped", "completed", "balance-low"][n % 4],
                duration_s=None if n % 4 == 0 else (0 if n % 4 == 1 else 62),
                transcript=(
                    "Unlabelled saved note\nassistant: Please tell me what happened.\n"
                    "user: नमस्ते। A courier asked for a small fee.\n"
                    "I paid on the link.\nassistant: <script>synthetic hostile text</script>"
                )
                if n % 4 != 0
                else "",
                extracted={},
            )
            if bait:
                extraction = Extraction(
                    "courier",
                    "card_details",
                    None,
                    None,
                    None,
                    None,
                    "Synthetic fixture. Courier fee requested.",
                )
                store.add_script(conn, call_id, extraction)
                store.add_report(conn, call_id, "DEMO FIXTURE. Draft only. Human review required.")
        for n, (outcome, acted, alert) in enumerate(
            [
                ("likely_scam", "gave_code_or_card", "sent"),
                ("likely_scam", "paid", "failed"),
                ("unclear", "unsure", None),
                ("no_scam_signs", "none", None),
            ]
        ):
            report = GuardianReport(
                "courier", "card_details", "sms", frozenset({"link_fee"}), acted
            )
            check_id = store.log_guardian_check(
                conn,
                report,
                "hi" if n % 2 else "en",
                MatchResult(outcome, 2, "fixture", acted == "paid"),
            )
            conn.execute(
                "update guardian_checks set alert_status = %s where id = %s", (alert, check_id)
            )
            if n == 1:
                conn.execute(
                    "update guardian_checks set created_at = now() - interval '25 hours' "
                    "where id = %s",
                    (check_id,),
                )


def preview(state: str, reset: bool):
    if not reset:
        raise SystemExit("Pass --reset-test-db to confirm the destructive test-branch reset.")
    url = _test_database_url()
    if not url:
        raise SystemExit("TEST_DATABASE_URL is required.")
    # Inspect endpoint equality privately. Never print either URL or settings object.
    test_host = urlsplit(url).hostname
    production_host = urlsplit(Settings().database_url).hostname
    if (
        not test_host
        or not production_host
        or test_host.replace("-pooler", "") == production_host.replace("-pooler", "")
    ):
        raise SystemExit("A distinct test database endpoint is required.")
    settings = Settings(
        _env_file=None,
        bolna_api_key="preview-fake",
        bolna_webhook_token="preview-hook",
        bolna_tool_token="preview-tool",
        database_url=url,
        admin_password="preview-only",
        family_link_token="preview-family",
        telegram_bot_token="",
        telegram_chat_id="",
        bolna_guardian_agent_id="fake-guardian",
        bolna_guardian_hi_agent_id="fake-guardian-hi",
        bolna_bait_agent_id="fake-bait",
        bolna_bait_hi_agent_id="fake-bait-hi",
    )
    migrate(url)
    with connect(url) as conn:
        conn.execute("truncate calls, guardian_checks, scripts, reports restart identity")
    if state == "populated":
        fixture_rows(url)
    main.app.dependency_overrides[get_settings] = lambda: settings
    main.app.dependency_overrides[main.get_bolna] = lambda: FakeBolnaWithSessions()
    main.app.dependency_overrides[main.get_telegram] = lambda: FakeTelegram()
    # The existing S7 call controller stays in production until S11. Preview has no SDK or mic.
    template = (ROOT / "src/scamkaki/app/templates/dashboard.html").read_text()
    template = template.replace(
        "{% block content %}",
        '{% block content %}<p class="notice">Safe synthetic preview. Voice controls use a '
        "fake SDK, with no microphone or provider connection.</p>",
    )
    template = template.replace(
        '<script src="https://cdn.jsdelivr.net/gh/bolna-ai/web-call@v3.0.1/dist/bolna-web-call.min.js"></script>',
        """<script>
        class BolnaWebCall {
          constructor() { this.listeners = {}; }
          on(name, handler) { this.listeners[name] = handler; }
          start() {
            this.listeners.error({message: "Safe preview. No microphone or provider call."});
          }
          stop() { this.listeners["call-end"](); }
        }
        </script>""",
    )
    main.templates.env.loader = ChoiceLoader(
        [DictLoader({"dashboard.html": template}), main.templates.env.loader]
    )
    if state == "error":

        @contextmanager
        def unavailable(_url):
            raise psycopg.OperationalError("Synthetic preview read failure")
            yield

        main.connect = unavailable
    return main.app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", choices=["populated", "empty", "error"], default="populated")
    parser.add_argument("--reset-test-db", action="store_true")
    parser.add_argument("--port", type=int, default=8783)
    args = parser.parse_args()
    uvicorn.run(
        preview(args.state, args.reset_test_db), host="127.0.0.1", port=args.port, access_log=False
    )
