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
from scamkaki.domain.types import Extraction, GuardianReport, Leak, MatchResult  # noqa: E402
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
                leaks=[Leak("otp_or_account_digits", 0, "[masked synthetic fixture]")]
                if n == 54
                else None,
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
                draft = "DEMO FIXTURE. Draft only. Human review required."
                if n == 54:
                    draft += "\nनमस्ते। Synthetic text: <script>fixture draft</script>"
                store.add_report(conn, call_id, draft)
        for n, (outcome, acted, alert) in enumerate(
            [
                ("likely_scam", "gave_code_or_card", "sent"),
                ("likely_scam", "paid", "failed"),
                ("unclear", "unsure", None),
                ("no_scam_signs", "none", None),
                ("likely_scam", "none", "off"),
            ]
        ):
            report = GuardianReport(
                "courier", "card_details", "sms", frozenset({"link_fee"}), acted
            )
            check_id = store.log_guardian_check(
                conn,
                report,
                "hi" if n % 2 or n == 4 else "en",
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
        # S9 fixture counts: courier 19, bank/code 4, bank/transfer 2, hostile text 1.
        groups = [
            ("bank", "otp", "en", 0),
            ("bank", "otp", "en", 0),
            ("bank", "otp", "en", 0),
            ("bank", "otp", "hi", 0),
            ("bank", "transfer", "hi", 0),
            ("bank", "transfer", "hi", 0),
            ("spf", "personal_info", "en", 8),
            ("<script>fixture agency</script>", "नमस्ते <img src=x onerror=alert(1)>", "hi", 0),
        ]
        for n, (agency, demand, language, days_ago) in enumerate(groups):
            call_id = store.upsert_call(
                conn,
                execution_id=f"s9-pattern-fixture-{n}",
                line="bait",
                language=language,
                fixture_case=f"s9-pattern-fixture-{n}",
                status="completed",
                duration_s=None,
                transcript="",
                extracted={},
            )
            script_id = store.add_script(
                conn, call_id, Extraction(agency, demand, None, None, None, None, None)
            )
            conn.execute(
                "update scripts set created_at = now() - make_interval(days => %s) where id=%s",
                (days_ago, script_id),
            )


def preview(state: str, reset: bool):
    if not reset:
        raise SystemExit("Pass --reset-test-db to confirm the destructive test-branch reset.")
    template = (ROOT / "src/scamkaki/app/templates/voice.html").read_text()
    sdk = '<script src="https://cdn.jsdelivr.net/gh/bolna-ai/web-call@v3.0.1/dist/bolna-web-call.min.js"></script>'
    if template.count(sdk) != 1:
        raise RuntimeError("Voice SDK replacement must match exactly once before a preview reset.")
    family_template = (ROOT / "src/scamkaki/app/templates/family.html").read_text()
    family_anchor = "<script>\nconst AGENCIES"
    if family_template.count(family_anchor) != 1:
        raise RuntimeError(
            "Family preview replacement must match exactly once before a preview reset."
        )
    family_fake = (ROOT / "tests/support/family-preview.html").read_text()
    family_template = family_template.replace(family_anchor, family_fake + family_anchor)
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
    if state == "unconfigured":
        settings = settings.model_copy(
            update={
                "bolna_guardian_agent_id": "",
                "bolna_guardian_hi_agent_id": "",
                "bolna_bait_agent_id": "",
                "bolna_bait_hi_agent_id": "",
            }
        )
    migrate(url)
    with connect(url) as conn:
        conn.execute("truncate calls, guardian_checks, scripts, reports restart identity")
    if state in {"populated", "reviewed"}:
        fixture_rows(url)
    if state == "reviewed":
        with connect(url) as conn:
            for row in conn.execute("select id from reports").fetchall():
                store.mark_reviewed(conn, row["id"])
    main.app.dependency_overrides[get_settings] = lambda: settings
    main.app.state.preview_bolna = FakeBolnaWithSessions()
    main.app.state.preview_telegram = FakeTelegram()
    main.app.dependency_overrides[main.get_bolna] = lambda: main.app.state.preview_bolna
    main.app.dependency_overrides[main.get_telegram] = lambda: main.app.state.preview_telegram
    template = template.replace(
        "{% block content %}",
        '{% block content %}<p class="notice">Safe synthetic preview. The fake SDK never '
        "uses a real microphone or provider. Start makes a local request to the "
        "fake session endpoint.</p>",
    )
    template = template.replace(sdk, "")
    fake_sdk = (ROOT / "tests/support/voice-preview.html").read_text()
    template = template.replace("{% endblock %}", fake_sdk + "{% endblock %}", 1)
    main.templates.env.loader = ChoiceLoader(
        [
            DictLoader({"voice.html": template, "family.html": family_template}),
            main.templates.env.loader,
        ]
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
    parser.add_argument(
        "--state",
        choices=["populated", "reviewed", "empty", "error", "unconfigured"],
        default="populated",
    )
    parser.add_argument("--reset-test-db", action="store_true")
    parser.add_argument("--port", type=int, default=8783)
    args = parser.parse_args()
    uvicorn.run(
        preview(args.state, args.reset_test_db), host="127.0.0.1", port=args.port, access_log=False
    )
