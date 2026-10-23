"""SQL for calls, Guardian checks and family alerts."""

from typing import Any, Literal

import psycopg
from psycopg.types.json import Jsonb

from scamkaki.domain.types import Agency, Demand, Language, Line, MatchResult

AlertStatus = Literal["sent", "failed", "off"]


def upsert_call(
    conn: psycopg.Connection,
    *,
    execution_id: str,
    line: Line,
    language: Language,
    transcript: str,
    extracted: dict[str, Any],
    status: str,
    duration_s: int | None,
    fixture_case: str | None,
) -> int:
    row = conn.execute(
        """
        insert into calls (execution_id, line, language, transcript, extracted, status,
                           duration_s, fixture_case)
        values (%s, %s, %s, %s, %s, %s, %s, %s)
        on conflict (execution_id) do update set
            transcript = excluded.transcript,
            extracted = excluded.extracted,
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
            status,
            duration_s,
            fixture_case,
        ),
    ).fetchone()
    return row["id"]


def log_guardian_check(
    conn: psycopg.Connection,
    agency: Agency,
    demand: Demand,
    language: Language,
    result: MatchResult,
) -> int:
    alert_status = "pending" if result.verdict == "likely_scam" else None
    row = conn.execute(
        """
        insert into guardian_checks (agency, demand, language, verdict, similar_count,
                                     alert_status)
        values (%s, %s, %s, %s, %s, %s) returning id
        """,
        (agency, demand, language, result.verdict, result.similar_count, alert_status),
    ).fetchone()
    return row["id"]


def set_alert_status(conn: psycopg.Connection, check_id: int, status: AlertStatus) -> None:
    conn.execute("update guardian_checks set alert_status = %s where id = %s", (status, check_id))


def recent_alerts(conn: psycopg.Connection, limit: int = 20) -> list[dict[str, Any]]:
    return conn.execute(
        """
        select id, agency, demand, language, similar_count, alert_status, created_at
        from guardian_checks where verdict = 'likely_scam'
        order by created_at desc, id desc limit %s
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
