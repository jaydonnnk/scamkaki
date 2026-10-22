"""SQL for calls and Guardian checks."""

from typing import Any

import psycopg
from psycopg.types.json import Jsonb

from scamkaki.domain.types import Agency, Demand, Language, Line, MatchResult


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
    conn: psycopg.Connection, agency: Agency, demand: Demand, result: MatchResult
) -> int:
    row = conn.execute(
        """
        insert into guardian_checks (agency, demand, verdict, similar_count)
        values (%s, %s, %s, %s) returning id
        """,
        (agency, demand, result.verdict, result.similar_count),
    ).fetchone()
    return row["id"]


def recent_calls(conn: psycopg.Connection, limit: int = 50) -> list[dict[str, Any]]:
    return conn.execute(
        "select * from calls order by created_at desc limit %s", (limit,)
    ).fetchall()


def recent_checks(conn: psycopg.Connection, limit: int = 50) -> list[dict[str, Any]]:
    return conn.execute(
        "select * from guardian_checks order by created_at desc limit %s", (limit,)
    ).fetchall()
