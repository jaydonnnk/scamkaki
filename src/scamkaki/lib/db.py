"""Postgres connection helper and the migration runner."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

MIGRATIONS_DIR = Path(__file__).resolve().parents[3] / "migrations"


@contextmanager
def connect(database_url: str) -> Iterator[psycopg.Connection]:
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        yield conn


def migrate(database_url: str) -> list[str]:
    """Apply migrations/NNNN_*.sql in order, once each. Returns the names applied now."""
    applied: list[str] = []
    with connect(database_url) as conn:
        conn.execute(
            "create table if not exists schema_migrations"
            " (name text primary key, applied_at timestamptz not null default now())"
        )
        done = {r["name"] for r in conn.execute("select name from schema_migrations")}
        for path in sorted(MIGRATIONS_DIR.glob("[0-9][0-9][0-9][0-9]_*.sql")):
            if path.name in done:
                continue
            with conn.transaction():
                conn.execute(path.read_text())
                conn.execute("insert into schema_migrations (name) values (%s)", (path.name,))
            applied.append(path.name)
    return applied
