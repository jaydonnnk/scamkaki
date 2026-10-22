# Scamkaki

Two Bolna voice agents for seniors in Singapore, each in English and in Hindi (one Bolna agent per language).
Ah Ma Bait answers scam calls as a Singapore auntie, stalls, and extracts the claimed agency, demand and payee details.
Ah Ma Guardian takes calls from seniors, compares what they heard with the scam scripts Bait collected, and hands risky cases to a family member.

## Demo only

- All scam scripts, test callers and dashboard data are labeled fixtures.
- Scam reports are drafts for human review; nothing is filed automatically.
- Ah Ma never gives out an NRIC, OTP, card number or real-looking account number.

## Status

Slice state lives in [docs/plans/scamkaki/00-status.md](docs/plans/scamkaki/00-status.md).
Agent rules live in [AGENTS.md](AGENTS.md).

## Checks

Python 3.12 via `uv`; secrets live in the ignored `.env.local` (names in `.env.example`).

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

Integration tests need `TEST_DATABASE_URL` (a Neon test branch).
Create or update a Bolna agent from `agents/<name>.json` with `uv run python scripts/bolna_agent.py <name>`; apply migrations with `uv run python scripts/migrate.py`.
