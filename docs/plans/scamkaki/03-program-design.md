# Program Design: Scamkaki

Compact gate draft, 2026-10-22.
Revised 2026-10-22: English and Hindi agents; the Modal TTS service and its files are removed.
Revised 2026-10-24: family alert page and Telegram replace call transfer.

## Toolchain

Python 3.12 managed by `uv` (uv 0.13.0 is installed; Python 3.12 is not, `uv` would fetch it).
Runtime dependencies: `fastapi`, `uvicorn`, `psycopg[binary]`, `httpx`, `jinja2`, `pydantic-settings`.
Dev dependencies: `pytest`, `ruff`.
Exact pins are set in `pyproject.toml` and `uv.lock` at Slice 1; installing them needs your authorization.
No local Postgres is installed; integration tests use a Neon test branch through `TEST_DATABASE_URL`.

Checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest tests/unit -q
TEST_DATABASE_URL=... uv run pytest tests/integration -q
uv run python scripts/check.py bait|guardian [--language hi]
```

## Files

| File | Why it lives there |
|---|---|
| `pyproject.toml`, `uv.lock` | Project, pins, ruff and pytest config |
| `src/scamkaki/lib/env.py` | Settings loaded from env; the only reader of env vars |
| `src/scamkaki/lib/db.py` | Connection helper and the small migration runner |
| `src/scamkaki/lib/log.py` | Structured logging without secrets |
| `src/scamkaki/domain/types.py` | `Agency`, `Demand`, `Verdict`, `Extraction`, `Leak`, `MatchResult` |
| `src/scamkaki/domain/extraction.py` | Parse Bolna extracted values into `Extraction`, unknown values to `other` or `None` |
| `src/scamkaki/domain/leaks.py` | Leak guard over Ah Ma's turns |
| `src/scamkaki/domain/verdict.py` | Verdict rule and the sentence Ah Ma says |
| `src/scamkaki/domain/reports.py` | Report draft text |
| `src/scamkaki/domain/store.py` | SQL for calls, scripts, checks, reports |
| `src/scamkaki/integrations/bolna.py` | Bolna REST client: get execution, start test call |
| `src/scamkaki/integrations/telegram.py` | Sends one Telegram message; never raises |
| `src/scamkaki/app/main.py` | FastAPI app and routes |
| `src/scamkaki/app/templates/*.html` | Dashboard, report and family alert pages, from the Gate 1 mockups |
| `migrations/0001_init.sql` | Tables from Gate 2 |
| `migrations/0003_family_alerts.sql` | `guardian_checks.language` and `guardian_checks.alert_status` |
| `agents/{bait,bait_hi,guardian,guardian_hi,test_scammer,test_senior}.json` | Bolna agent exports, versioned; `_hi` files are the Hindi agents |
| `seed/scripts.json` | 8 labeled English fixture cases (5 scam, 3 legit) plus 3 Hindi cases (2 scam, 1 legit), each with a `language` field |
| `scripts/check.py` | Runs agent-vs-agent fixture calls and prints pass rates |
| `scripts/migrate.py` | Applies migrations |
| `scripts/bolna_agent.py` | Creates or updates a Bolna agent from `agents/<name>.json` |
| `tests/support/fakes.py` | Fake Bolna client and payload builders |

## Types and signatures

```python
Agency = Literal["spf", "ica", "china_official", "moh", "cpf", "mom", "iras", "bank", "courier", "other"]
Demand = Literal["transfer", "otp", "app_install", "personal_info", "gift_card", "none", "other"]
Verdict = Literal["likely_scam", "unclear", "no_scam_signs"]
Line = Literal["bait", "guardian"]
Language = Literal["en", "hi"]

GOV_AGENCIES: frozenset[Agency]  # spf, ica, china_official, moh, cpf, mom, iras
HARD_DEMANDS: frozenset[Demand]  # transfer, otp, app_install, gift_card

@dataclass(frozen=True)
class Extraction:
    agency: Agency
    demand: Demand
    payee_bank: str | None
    payee_account: str | None
    paynow_id: str | None
    url: str | None
    summary: str | None

@dataclass(frozen=True)
class Leak:
    kind: Literal["nric", "otp_or_account_digits", "card"]
    turn_index: int
    excerpt: str  # masked

@dataclass(frozen=True)
class MatchResult:
    verdict: Verdict
    similar_count: int
    say: str

# domain/extraction.py
def parse_extraction(raw: Mapping[str, object]) -> Extraction: ...

# domain/leaks.py
def normalize_spoken_digits(text: str) -> str: ...   # "one two three" -> "123", Singlish and Hindi digit words (Devanagari and romanized)
def find_leaks(agent_turns: Sequence[str]) -> list[Leak]: ...
# Leak rules on Ah Ma's turns only: NRIC/FIN pattern [STFGM]\d{7}[A-Z]; any run of 6 or more digits; 13-19 digit card-like runs.

# domain/verdict.py
def decide(agency: Agency, demand: Demand, similar_count: int) -> Verdict: ...
#  demand in HARD_DEMANDS -> likely_scam
#  agency in GOV_AGENCIES and demand == personal_info -> likely_scam
#  similar_count >= 1 -> unclear
#  else -> no_scam_signs
def sentence_for(verdict: Verdict, similar_count: int, language: Language) -> str: ...
# The sentence is in the line's language; Hindi sentences carry explicit money and OTP warnings.

def alert_text(agency: Agency, demand: Demand, language: Language, similar_count: int, at: datetime) -> str: ...
# The Telegram message: "[Demo fixture] Ah Ma Guardian: likely scam", who the caller claimed to be, what they wanted, the line, the time in Singapore, and "Please call Ah Ma now." No phone numbers or transcript.

# domain/reports.py
def draft_report(extraction: Extraction, leaks: Sequence[Leak], fixture_case: str | None) -> str: ...

# domain/store.py
def upsert_call(conn, execution_id: str, line: Line, language: Language, transcript: str, extracted: dict, leaks: list[Leak],
                status: str, duration_s: int | None, fixture_case: str | None) -> int: ...
def add_script(conn, call_id: int, extraction: Extraction) -> int: ...
def count_similar(conn, agency: Agency, demand: Demand, days: int = 7) -> int: ...
def log_guardian_check(conn, agency: Agency, demand: Demand, language: Language, result: MatchResult) -> int: ...
# alert_status starts as "pending" for likely_scam, else null
def set_alert_status(conn, check_id: int, status: Literal["sent", "failed", "off"]) -> None: ...
def recent_alerts(conn, limit: int = 20) -> list[AlertRow]: ...
def add_report(conn, call_id: int, draft: str) -> int: ...
def mark_reviewed(conn, report_id: int) -> None: ...
def recent_calls(conn, limit: int = 50) -> list[CallRow]: ...
def scripts_this_week(conn) -> list[ScriptGroup]: ...

# lib/env.py
def agent_line(agent_id: str) -> tuple[Line, Language] | None: ...  # maps the four agent ids; unknown id -> None

# integrations/bolna.py
class BolnaClient:
    def get_execution(self, execution_id: str) -> dict: ...
    def start_call(self, agent_id: str, to_number: str, variables: dict[str, str]) -> str: ...

# integrations/telegram.py
def send_message(bot_token: str, chat_id: str, text: str) -> bool: ...  # 5 s timeout; False on any error

# app/main.py
POST /bolna/webhook/{token}   body: Bolna event -> 204
POST /tools/match-script      body: {"agency": str, "demand": str, "language": "en"|"hi"} -> {"verdict", "similar_count", "say"}
GET  /family/{link_token}         -> HTML; wrong token -> 404
GET  /family/{link_token}/alerts  -> [{"id", "agency", "demand", "language", "similar_count", "alert_status", "created_at"}]
GET  /, GET /reports/{id}, POST /reports/{id}/review, GET /healthz
```

The fixture case id travels from `scripts/check.py` to the agents as a call variable and back on the execution, so results are tied to a case without parsing transcripts [hypothesis: Bolna returns call variables on the execution; verify in Slice 1].

## Call stack

**Bait webhook:** `webhook` (token check) to `BolnaClient.get_execution` to `agent_line` to `parse_extraction` to `find_leaks(agent turns)` to `upsert_call` to `add_script` to `draft_report` to `add_report`.
Repeated events for the same execution are idempotent through `upsert_call`; script and report rows are created once.

**Guardian tool:** `match_script` (bearer check) to `parse_extraction`-style validation of `agency` and `demand` to `count_similar` to `decide` to `sentence_for` to `log_guardian_check`, returning JSON.
On `likely_scam`, a FastAPI background task runs after the response: `alert_text` to `telegram.send_message` to `set_alert_status` (`off` when the Telegram settings are empty).
A Telegram failure is logged and never changes what Ah Ma says.
Any internal error returns `unclear` with "Not sure. Please call your family before doing anything." so the call never goes silent.

**Fixture check:** `scripts/check.py` loads `seed/scripts.json`, starts one test call per case, waits for the stored calls, compares results with each case's expectations, prints a table and exits non-zero below threshold.

## Test plan

Unit (`tests/unit`):

- `test_parse_extraction_maps_unknown_agency_to_other`
- `test_parse_extraction_keeps_payee_fields`
- `test_find_leaks_detects_nric`
- `test_find_leaks_detects_six_digit_run`
- `test_find_leaks_detects_spelled_out_digits`
- `test_find_leaks_detects_card_number`
- `test_find_leaks_ignores_short_numbers` (for example "wait 5 minutes")
- `test_find_leaks_self_test_on_serialized_transcript` (injected needle in a real-shaped Bolna transcript is found)
- `test_decide_hard_demand_is_likely_scam`
- `test_decide_gov_personal_info_is_likely_scam`
- `test_decide_repeat_script_is_unclear`
- `test_decide_no_signals_is_no_scam_signs`
- `test_sentence_never_says_safe`
- `test_alert_text_is_labeled_fixture_and_names_claim`
- `test_draft_report_is_labeled_draft_and_fixture`
- `test_env_example_lists_exactly_settings_names`
- `test_agent_line_maps_all_four_agents`
- `test_hi_agents_match_english_twins` (same tools, extraction keys and webhook)
- `test_find_leaks_detects_hindi_digit_words` (for example एक दो तीन चार पांच छह, and romanized "ek do teen")

Integration (`tests/integration`, Neon test branch, fake Bolna client):

- `test_webhook_rejects_bad_token`
- `test_webhook_stores_bait_call_script_and_draft`
- `test_webhook_is_idempotent_per_execution`
- `test_webhook_flags_leak_on_call`
- `test_match_script_rejects_bad_token`
- `test_match_script_counts_last_seven_days_only`
- `test_match_script_error_returns_unclear`
- `test_match_script_likely_scam_alerts_family`
- `test_match_script_other_verdicts_send_no_alert`
- `test_match_script_telegram_failure_still_answers`
- `test_family_page_rejects_wrong_link`
- `test_family_alerts_lists_likely_scam_only`
- `test_report_review_marks_reviewed_and_sends_nothing`

Live fixture checks (`scripts/check.py`, each run needs call authorization):

- `bait`: 5 scam cases; pass if at least 4 planted payees are captured and zero leaks.
- `guardian`: 8 cases; pass if at least 4 of 5 scams are `likely_scam` and at most 1 of 3 legit cases is.
- `bait --language hi`: 2 Hindi scam cases; pass if at least 1 payee is captured and zero leaks.
- `guardian --language hi`: 3 Hindi cases; pass if both scams are `likely_scam` and the legit case is not.

Guard coverage: for each rule in `decide` and `find_leaks`, and for the alert-only-on-likely-scam and family-link checks, mutate that branch alone and show the matching unit test fails; record in `evidence/`.

## Least confident decisions

1. Structured matching on agency plus demand instead of embeddings: simple and testable, but blind to new scripts that reuse the same pair.
2. Render free tier: cold starts versus Bolna's tool timeout [unknown].
3. Webhook auth by path token, because Bolna webhook signatures are [unknown].
4. The family alert is sent by the app, so it no longer relies on the LLM (S3 showed it could skip or fail the transfer), but it reaches family only through Telegram or an open family page, and Telegram delivery is [unknown until S3].
5. Hindi speech-to-text and voice quality on Bolna's stock providers [unknown until S2]; fallback is English only.
6. Fixture case id round-trip through call variables [unknown].
7. One agent per language doubles the agent JSON files to keep in sync; a unit test checks each `_hi` file has the same tools, extraction keys and webhook as its English twin.
