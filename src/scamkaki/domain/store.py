"""SQL for calls, Bait scripts and reports, Guardian checks and family alerts."""

from dataclasses import asdict
from typing import Any, Literal

import psycopg
from psycopg.types.json import Jsonb

from scamkaki.domain.types import (
    TACTICS,
    Agency,
    Demand,
    Extraction,
    GuardianReport,
    Language,
    Leak,
    Line,
    MatchResult,
)

AlertStatus = Literal["sent", "failed", "off"]


def upsert_call(
    conn: psycopg.Connection,
    *,
    execution_id: str,
    line: Line,
    language: Language,
    transcript: str,
    extracted: dict[str, Any],
    leaks: list[Leak] | None = None,
    status: str,
    duration_s: int | None,
    fixture_case: str | None,
) -> int:
    row = conn.execute(
        """
        insert into calls (execution_id, line, language, transcript, extracted, leaks, status,
                           duration_s, fixture_case)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        on conflict (execution_id) do update set
            transcript = excluded.transcript,
            extracted = excluded.extracted,
            leaks = excluded.leaks,
            status = excluded.status,
            duration_s = excluded.duration_s,
            fixture_case = coalesce(excluded.fixture_case, calls.fixture_case)
        returning id
        """,
        (
            execution_id,
            line,
            language,
            transcript,
            Jsonb(extracted),
            Jsonb([asdict(leak) for leak in leaks or []]),
            status,
            duration_s,
            fixture_case,
        ),
    ).fetchone()
    return row["id"]


def add_script(conn: psycopg.Connection, call_id: int, extraction: Extraction) -> int:
    """One script per Bait call; a repeated webhook refreshes it instead of adding a row."""
    fields = asdict(extraction)
    columns = ", ".join(fields)
    updates = ", ".join(f"{name} = excluded.{name}" for name in fields)
    row = conn.execute(
        f"""
        insert into scripts (call_id, {columns}) values (%s, {", ".join(["%s"] * len(fields))})
        on conflict (call_id) do update set {updates}
        returning id
        """,
        (call_id, *fields.values()),
    ).fetchone()
    return row["id"]


def add_report(conn: psycopg.Connection, call_id: int, draft: str) -> int:
    """One draft report per Bait call; a reviewed report is never rewritten."""
    row = conn.execute(
        """
        insert into reports (call_id, draft) values (%s, %s)
        on conflict (call_id) do update set draft = excluded.draft
            where reports.status = 'draft'
        returning id
        """,
        (call_id, draft),
    ).fetchone()
    if row is None:  # Already reviewed: keep it as the reviewer saw it.
        row = conn.execute("select id from reports where call_id = %s", (call_id,)).fetchone()
    return row["id"]


def recent_scripts(conn: psycopg.Connection, limit: int = 50) -> list[dict[str, Any]]:
    """Bait scripts with their call and draft report, newest first, for the dashboard."""
    return conn.execute(
        """
        select s.*, c.language, c.fixture_case, c.leaks, r.id as report_id, r.draft,
               r.status as report_status
        from scripts s join calls c on c.id = s.call_id
        left join reports r on r.call_id = s.call_id
        order by s.created_at desc, s.id desc limit %s
        """,
        (limit,),
    ).fetchall()


def count_similar(conn: psycopg.Connection, agency: Agency, demand: Demand, days: int = 7) -> int:
    """Bait scripts with this agency and demand in the last `days` days, in any language."""
    row = conn.execute(
        """
        select count(*) as n from scripts
        where agency = %s and demand = %s and created_at > now() - make_interval(days => %s)
        """,
        (agency, demand, days),
    ).fetchone()
    return row["n"]


def scripts_this_week(conn: psycopg.Connection) -> list[dict[str, Any]]:
    """Bait scripts of the last 7 days grouped by agency and demand, most heard first."""
    return conn.execute(
        """
        select s.agency, s.demand, count(*) as n,
               array_agg(distinct c.language order by c.language) as languages,
               max(s.created_at) as last_seen
        from scripts s join calls c on c.id = s.call_id
        where s.created_at > now() - interval '7 days'
        group by s.agency, s.demand
        order by n desc, last_seen desc
        """
    ).fetchall()


def log_guardian_check(
    conn: psycopg.Connection,
    report: GuardianReport,
    language: Language,
    result: MatchResult,
    execution_id: str | None = None,
) -> int:
    alert_status = "pending" if result.verdict == "likely_scam" else None
    row = conn.execute(
        """
        insert into guardian_checks (agency, demand, channel, tactics, acted, language, verdict,
                                     similar_count, alert_status, execution_id)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id
        """,
        (
            report.agency,
            report.demand,
            report.channel,
            [tactic for tactic in TACTICS if tactic in report.tactics],
            report.acted,
            language,
            result.verdict,
            result.similar_count,
            alert_status,
            execution_id,
        ),
    ).fetchone()
    return row["id"]


def set_alert_status(conn: psycopg.Connection, check_id: int, status: AlertStatus) -> None:
    conn.execute("update guardian_checks set alert_status = %s where id = %s", (status, check_id))


def recent_alerts(conn: psycopg.Connection, limit: int = 20) -> list[dict[str, Any]]:
    """Likely-scam checks for the family page, newest first, except that urgent ones (the senior
    already acted) from the last 24 hours go on top. Older urgent ones fall back into time order,
    so they never sit above, or flash instead of, a newer alert for good."""
    return conn.execute(
        """
        select id, agency, demand, channel, tactics, acted,
               acted in ('paid', 'gave_code_or_card', 'installed_app') as urgent,
               language, similar_count, alert_status, created_at
        from guardian_checks where verdict = 'likely_scam'
        order by (acted in ('paid', 'gave_code_or_card', 'installed_app')
                  and created_at > now() - interval '24 hours') desc,
                 created_at desc, id desc
        limit %s
        """,
        (limit,),
    ).fetchall()


def recent_calls(conn: psycopg.Connection, limit: int = 50) -> list[dict[str, Any]]:
    return conn.execute(
        "select * from calls order by created_at desc limit %s", (limit,)
    ).fetchall()


def recent_checks(conn: psycopg.Connection, limit: int = 50) -> list[dict[str, Any]]:
    return conn.execute(
        "select * from guardian_checks order by created_at desc limit %s", (limit,)
    ).fetchall()
