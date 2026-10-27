# Program Design: Scamkaki

Compact gate draft, 2026-10-22.
Revised 2026-10-22: English and Hindi agents; the Modal TTS service and its files are removed.
Revised 2026-10-24: family alert page and Telegram replace call transfer.
Revised 2026-10-27 (reopened): `GuardianReport`, warning signs (`Tactic`), `Channel` and `Acted`; `decide` takes the report; new act-now and call-back sentences; migration 0005; Guardian fixtures rewritten. Bait code is unchanged.

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
| `src/scamkaki/domain/types.py` | `Agency`, `Demand`, `Channel`, `Tactic`, `Acted`, `Verdict`, `Extraction`, `GuardianReport`, `Leak`, `MatchResult` |
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
| `migrations/0005_guardian_signs.sql` | `guardian_checks.channel`, `guardian_checks.tactics`, `guardian_checks.acted`, with defaults |
| `agents/{bait,bait_hi,guardian,guardian_hi}.json` | Bolna agent exports, versioned; `_hi` files are the Hindi agents; Bait files also carry their Bolna extraction (disposition) definitions |
| `seed/scripts.json` | Labeled fixture cases, each with `language` and `for` (`bait` or `guardian`). Bait: the existing 5 English scam and 2 Hindi scam cases, unchanged. Guardian: 12 new English cases (8 sophisticated scams, 4 legit look-alikes) and 3 new Hindi cases (2 scam, 1 legit), listed below; the old easy Guardian cases and the `senior_lines` on Bait cases are removed |
| `scripts/check.py` | Reads the stored fixture calls, compares them with each case and prints pass rates |
| `scripts/caller/` | Synthetic caller: renders each case's caller lines with macOS `say` and serves a local page that plays them into a Bolna web call |
| `scripts/migrate.py` | Applies migrations |
| `scripts/bolna_agent.py` | Creates or updates a Bolna agent from `agents/<name>.json` |
| `tests/support/fakes.py` | Fake Bolna client and payload builders |

## Types and signatures

```python
Agency = Literal["spf", "ica", "china_official", "moh", "cpf", "mom", "iras", "mas", "minlaw",
                 "bank", "telco", "courier", "investment", "employer", "friend_family", "other"]
Demand = Literal["transfer", "cash_handover", "otp", "card_details", "app_install", "personal_info",
                 "gift_card", "none", "other"]
# cash_handover: cash, gold or valuables handed over or deposited at an ATM; card_details: card or bank login typed on a website
Channel = Literal["call", "sms", "whatsapp", "video", "website", "in_person", "other"]
Tactic = Literal["handoff", "secrecy", "stay_on_line", "channel_move", "paid_first", "link_fee", "new_payee",
                 "urgency_threat", "knew_details"]
# handoff: passed to another officer or company; secrecy: told not to tell family or the bank; stay_on_line: keep the call or video on;
# channel_move: moved to WhatsApp, Telegram or video; paid_first: paid or shown profit first; link_fee: small fee by link;
# new_payee: pay a different person or a changed account; urgency_threat: arrest, freeze or deadline today; knew_details: already knew IC or card digits
Acted = Literal["none", "paid", "gave_code_or_card", "installed_app", "unsure"]
Verdict = Literal["likely_scam", "unclear", "no_scam_signs"]
Line = Literal["bait", "guardian"]
Language = Literal["en", "hi"]

GOV_AGENCIES: frozenset[Agency]  # spf, ica, china_official, moh, cpf, mom, iras, mas, minlaw
HARD_DEMANDS: frozenset[Demand]  # transfer, cash_handover, otp, card_details, app_install, gift_card
RED_TACTICS: frozenset[Tactic]   # handoff, secrecy, stay_on_line, channel_move, paid_first, link_fee, new_payee
WEAK_TACTICS: frozenset[Tactic]  # urgency_threat, knew_details (real banks also know your details)
HARM_ACTED: frozenset[Acted]     # paid, gave_code_or_card, installed_app

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
class GuardianReport:
    """What the senior told Guardian, as the Guardian agent passes it to match_script."""
    agency: Agency
    demand: Demand
    channel: Channel
    tactics: frozenset[Tactic]
    acted: Acted

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
    urgent: bool  # the senior already paid, gave a code or card, or installed an app

# domain/extraction.py
def parse_extraction(raw: Mapping[str, object]) -> Extraction: ...
def parse_guardian_report(raw: Mapping[str, object]) -> GuardianReport: ...
# unknown agency/demand/channel -> other; tactics: split on commas, trim, lower-case, drop unknown; unknown or missing acted -> none

# domain/leaks.py
def normalize_spoken_digits(text: str) -> str: ...   # "one two three" -> "123", Singlish and Hindi digit words (Devanagari and romanized)
def find_leaks(agent_turns: Sequence[str]) -> list[Leak]: ...
# Leak rules on Ah Ma's turns only: NRIC/FIN pattern [STFGM]\d{7}[A-Z]; any run of 6 or more digits; 13-19 digit card-like runs.

# domain/verdict.py
def decide(report: GuardianReport, similar_count: int) -> Verdict: ...
#  acted in HARM_ACTED -> likely_scam
#  tactics & RED_TACTICS -> likely_scam
#  demand in HARD_DEMANDS and agency == friend_family -> unclear   (call them back on the number you already have)
#  demand in HARD_DEMANDS -> likely_scam
#  agency in GOV_AGENCIES and demand == personal_info -> likely_scam
#  tactics & WEAK_TACTICS, acted == unsure, or similar_count >= 1 -> unclear
#  else -> no_scam_signs
def sentence_for(verdict: Verdict, report: GuardianReport, similar_count: int, language: Language) -> str: ...
# In the line's language; Hindi sentences carry explicit money and OTP warnings.
# acted in HARM_ACTED: starts with "Call your bank now on the number on the back of your card, and call ScamShield at 1799."
# friend_family money request ruled unclear: adds "Call them back on the number you already have, not the one that contacted you."

def alert_text(report: GuardianReport, language: Language, similar_count: int, at: datetime) -> str: ...
# The Telegram message: "[Demo fixture] Ah Ma Guardian: likely scam", "URGENT: Ah Ma already ..." first when acted is harmful,
# how she was contacted, who the caller claimed to be, what they wanted, the warning signs, the line, the time in Singapore,
# and "Please call Ah Ma now." ("... Help her call the bank." when urgent). No phone numbers or transcript.

# domain/reports.py
def draft_report(extraction: Extraction, leaks: Sequence[Leak], fixture_case: str | None) -> str: ...

# domain/store.py
def upsert_call(conn, execution_id: str, line: Line, language: Language, transcript: str, extracted: dict, leaks: list[Leak],
                status: str, duration_s: int | None, fixture_case: str | None) -> int: ...
def add_script(conn, call_id: int, extraction: Extraction) -> int: ...
def count_similar(conn, agency: Agency, demand: Demand, days: int = 7) -> int: ...
def log_guardian_check(conn, report: GuardianReport, language: Language, result: MatchResult) -> int: ...
# alert_status starts as "pending" for likely_scam, else null
def set_alert_status(conn, check_id: int, status: Literal["sent", "failed", "off"]) -> None: ...
def recent_alerts(conn, limit: int = 20) -> list[AlertRow]: ...  # urgent first, then newest
def add_report(conn, call_id: int, draft: str) -> int: ...
def mark_reviewed(conn, report_id: int) -> None: ...
def recent_calls(conn, limit: int = 50) -> list[CallRow]: ...
def scripts_this_week(conn) -> list[ScriptGroup]: ...

# lib/env.py
def agent_line(agent_id: str) -> tuple[Line, Language] | None: ...  # maps the four agent ids; unknown id -> None

# integrations/bolna.py
class BolnaClient:
    def get_execution(self, execution_id: str) -> dict: ...
    def mint_web_call_session(self, agent_id: str, user_data: dict[str, str] | None = None) -> dict: ...

# integrations/telegram.py
def send_message(bot_token: str, chat_id: str, text: str) -> bool: ...  # 5 s timeout; False on any error

# app/main.py
POST /bolna/webhook/{token}   body: Bolna event -> 204
POST /tools/match-script      body: {"agency": str, "demand": str, "channel": str, "tactics": str, "acted": str, "language": "en"|"hi"}
                              -> {"verdict", "similar_count", "say", "urgent"}; missing new fields default to other, empty, none
GET  /family/{link_token}         -> HTML; wrong token -> 404
GET  /family/{link_token}/alerts  -> [{"id", "agency", "demand", "channel", "tactics", "acted", "urgent", "language", "similar_count", "alert_status", "created_at"}]
GET  /, GET /reports/{id}, POST /reports/{id}/review, GET /healthz
```

The fixture case id travels from the synthetic caller to the agents as web call `user_data` and back on the execution, so results are tied to a case without parsing transcripts [hypothesis: Bolna returns call variables on the execution; verify in Slice 1].

## Call stack

**Bait webhook:** `webhook` (token check) to `BolnaClient.get_execution` to `agent_line` to `parse_extraction` to `find_leaks(agent turns)` to `upsert_call` to `add_script` to `draft_report` to `add_report`.
Repeated events for the same execution are idempotent through `upsert_call`; script and report rows are created once.

**Guardian tool:** `match_script` (bearer check) to `parse_guardian_report` to `count_similar(report.agency, report.demand)` to `decide` to `sentence_for` to `log_guardian_check`, returning JSON.
On `likely_scam`, a FastAPI background task runs after the response: `alert_text` to `telegram.send_message` to `set_alert_status` (`off` when the Telegram settings are empty).
A Telegram failure is logged and never changes what Ah Ma says.
Any internal error returns `unclear` with "Not sure. Please call your family before doing anything." so the call never goes silent.

**Fixture check:** the synthetic caller places one web call per case; `scripts/check.py` loads `seed/scripts.json`, reads the stored calls, compares results with each case's expectations, prints a table and exits non-zero below threshold.

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
- `test_decide_hard_demand_is_likely_scam` (every value in `HARD_DEMANDS`, including `cash_handover` and `card_details`)
- `test_decide_gov_personal_info_is_likely_scam`
- `test_decide_harmful_act_is_likely_scam` (with demand `none` and no signs)
- `test_decide_red_tactic_alone_is_likely_scam` (each value in `RED_TACTICS`, with demand `none`)
- `test_decide_friend_money_without_red_tactic_is_unclear`
- `test_decide_friend_money_with_new_payee_is_likely_scam`
- `test_decide_weak_tactic_or_unsure_act_is_unclear`
- `test_decide_repeat_script_is_unclear`
- `test_decide_no_signals_is_no_scam_signs`
- `test_decide_matches_every_guardian_fixture` (offline: each Guardian case's `expect` report gives its `expect.verdict`; proves the rule, not the extraction)
- `test_guardian_fixtures_avoid_giveaway_words` (no senior line contains "scam", "safety account", "safe account" or "money laundering")
- `test_parse_guardian_report_drops_unknown_tactics_and_defaults_acted`
- `test_sentence_never_says_safe`
- `test_sentence_for_harmful_act_says_bank_and_1799_first` (English and Hindi)
- `test_sentence_for_friend_money_says_call_back_on_known_number`
- `test_alert_text_is_labeled_fixture_and_names_claim`
- `test_alert_text_marks_urgent_when_acted`
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
- `test_match_script_stores_channel_tactics_and_acted`
- `test_match_script_without_new_fields_uses_defaults`
- `test_family_alerts_list_urgent_first`
- `test_family_page_rejects_wrong_link`
- `test_family_alerts_lists_likely_scam_only`
- `test_report_review_marks_reviewed_and_sends_nothing`

Live fixture checks (`scripts/check.py`, each run needs call authorization):

- `bait`: 5 scam cases; pass if at least 4 planted payees are captured and zero leaks.
- `guardian`: 12 English cases; pass if at least 7 of 8 scams are `likely_scam`, at most 1 of 4 legit cases is, and `en-courier-paid-01` returns `urgent` with the bank instruction.
- `bait --language hi`: 2 Hindi scam cases; pass if at least 1 payee is captured and zero leaks.
- `guardian --language hi`: 3 Hindi cases; pass if both scams are `likely_scam`, `hi-courier-paid-01` returns `urgent`, and the legit case is not `likely_scam`.

Guardian fixtures (`for: guardian`), paraphrasing public SPF advisories; the senior trusts the caller in every scam case:

| Case | Story the senior tells | Expected report | Verdict |
|---|---|---|---|
| `en-telco-minlaw-01` | Singtel said a number in my name was used for crime, passed me to a MinLaw officer, keep it secret, stay on the line, move savings for checking | minlaw, transfer, call, handoff+secrecy+stay_on_line, none | likely_scam |
| `en-bank-otp-01` | Bank fraud team knew my last four card digits, asked me to read the code to cancel a purchase | bank, otp, call, knew_details, none | likely_scam |
| `en-courier-paid-01` | SMS said parcel address invalid; I paid S$1.64 on the website with my card and typed the code | courier, card_details, sms, link_fee, gave_code_or_card | likely_scam, urgent |
| `en-investment-01` | WhatsApp group teacher's stock tips; I took out a small profit; now top up for the VIP group | investment, transfer, whatsapp, paid_first, none | likely_scam |
| `en-whatsapp-friend-01` | Old friend on WhatsApp needs S$800 today, pay to his cousin's account | friend_family, transfer, whatsapp, new_payee+urgency_threat, none | likely_scam |
| `en-cash-handover-01` | Police officer said to withdraw cash and gold so a colleague can collect and check it | spf, cash_handover, call, secrecy, none | likely_scam |
| `en-job-task-01` | Paid S$30 for liking videos; now deposit to unlock better tasks | employer, transfer, whatsapp, paid_first, none | likely_scam |
| `en-ica-video-01` | ICA said a parcel with fake passports is in my name, moved me to a WhatsApp video call with China police, declare my assets | china_official, transfer, video, handoff+channel_move, none | likely_scam |
| `en-legit-bank-app-01` | Bank called about a card purchase, my bank app showed they were calling, they only asked yes or no | bank, none, call, knew_details, none | unclear (not likely_scam) |
| `en-legit-singpost-01` | SingPost SMS said my parcel is at the POPStation, no link, no fee | courier, none, sms, none, none | no_scam_signs |
| `en-legit-grandson-01` | My grandson called from his usual number, asked me to PayNow him S$50 for groceries he bought me | friend_family, transfer, call, none, none | unclear |
| `en-legit-cpf-01` | gov.sg SMS reminded me to update my CPF nomination by logging in myself with Singpass, no link | cpf, none, sms, none, none | no_scam_signs |
| `hi-mom-handoff-01` | MOM said my son's work pass has a problem, passed me to a police officer, keep it secret, pay the fine | spf, transfer, call, handoff+secrecy, none | likely_scam |
| `hi-courier-paid-01` | Hindi version of the courier fee case, already paid with card and code | courier, card_details, sms, link_fee, gave_code_or_card | likely_scam, urgent |
| `hi-legit-bank-app-01` | Hindi version of the bank-app-confirmed call | bank, none, call, knew_details, none | unclear (not likely_scam) |

Guard coverage: for each rule in `decide` (including each new branch: harmful act, red tactic, friend money) and `find_leaks`, and for the alert-only-on-likely-scam and family-link checks, mutate that branch alone and show the matching unit test fails; record in `evidence/`.

## Least confident decisions

1. Structured matching on agency plus demand instead of embeddings: simple and testable, but blind to new scripts that reuse the same pair.
2. Render free tier: cold starts versus Bolna's tool timeout [unknown].
3. Webhook auth by path token, because Bolna webhook signatures are [unknown].
4. The family alert is sent by the app, so it no longer relies on the LLM (S3 showed it could skip or fail the transfer), but it reaches family only through Telegram or an open family page, and Telegram delivery is [unknown until S3].
5. Hindi speech-to-text and voice quality on Bolna's stock providers [unknown until S2]; fallback is English only.
6. Fixture case id round-trip through call variables [unknown].
7. One agent per language doubles the agent JSON files to keep in sync; a unit test checks each `_hi` file has the same tools, extraction keys and webhook as its English twin.
8. Bait is left unchanged. The alternative is to have Bait extract warning signs too, so the 7-day count can match on tactics; or to move Bait's runs down the cut order since phone scams are shrinking [verified, SPF mid-year brief 2026].
9. Any one red warning sign alone gives `likely_scam`. Legit callers rarely hand you to another officer, ask for secrecy, keep you on the line or ask for a fee by link [hypothesis]; the cost is false alarms if speech-to-text or the LLM mislabels a sign.
10. A money request from friend or family with no red sign is `unclear`, not `likely_scam`, so a real grandson is not reported as a scammer; a hijacked WhatsApp that asks for the same amount to the same person would also pass as `unclear`.
11. Warning signs travel as one comma-separated string through Bolna's param template; five LLM-filled values per call is [unknown until S5].
12. The act-now advice (call the bank on the number on the card, then 1799) follows SPF's "report to your bank immediately" guidance [verified, SPF advisory 15 Jul 2026]; the Hindi wording needs a listener check.
