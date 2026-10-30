# Program Design: Scamkaki

Current amendment: website redesign, Gate 3 APPROVED 2026-10-30.
The original sections below describe the prior contract; the dated redesign section at the end
is the approved amendment. Status and approval authority remain in [00-status.md](00-status.md).

Compact gate draft, 2026-10-22.
Revised 2026-10-22: English and Hindi agents; the Modal TTS service and its files are removed.
Revised 2026-10-24: family alert page and Telegram replace call transfer.
Revised 2026-10-27 (reopened): `GuardianReport`, warning signs (`Tactic`), `Channel` and `Acted`; `decide` takes the report; new act-now and call-back sentences; migration 0005; Guardian fixtures rewritten. Bait code is unchanged.

## Approved S6 fixture-table amendment, 2026-10-28

[verified] The first fixed-clip probe failed. It does not isolate Guardian from caller timing
or ambiguous fixture wording. Keep that attempt and its three accepted alert sends.
The user re-approved the following table corrections on 2026-10-28; verdict rules stay unchanged:

- `en-telco-minlaw-01`: include `knew_details`, since the story says she knew the senior's IC.
- `hi-mom-handoff-01`: include `urgency_threat`, since the fine is due today.
- `en-ica-video-01`: explicitly deny arrest, freezing funds, a deadline, and knowing IC/card
  details in the story; expected tactics stay `handoff+channel_move`.

Caller repair comes first: add a human live-microphone mode that preserves `fixture_case` and
records `caller_mode=live`; it plays no clips and does not infer when the operator should answer
or hang up. A human reads the full verdict before ending the call, within the 180-second cap.
The fixture role-play method changes no success threshold and is never real-senior evidence.

The user approved keeping `gpt-5.4-mini`, temperature 1, `max_tokens=300`, continued help
without refusal, and an explicit yes before a tool call. Both Guardian updates were accepted
and read back on 2026-10-28 [verified]. The user proposed temperature 0.3, but
[Bolna's provider guide](https://www.bolna.ai/docs/openai-llm) documents that GPT-5 models require
1 and reject other values [vendor claim, checked 2026-10-28]. No changed-model cost is authorized.

Behavior improvements remain hypotheses. The user deferred all further live calls for credit
reasons. Offline completion does not satisfy S6's live exit checks. Per-turn tool withholding
on `simple_llm_agent` is unverified and not planned. Call-end alert fallback is not approved:
it changes urgent timing and the truth of "I have alerted your family". Ask again if repeats persist.

## S6 story-wording amendment, user-approved 2026-10-29

`en-ica-video-01` line 3 said the savings go "to an account they give me", which reads as a different payee while the denial line says there was none. The user approved removing that phrase: "moving my savings so they can clear my name". Expected report, tactics (`handoff+channel_move`) and verdict are unchanged. Story wording only.

## S7 handoff direction, user-directed 2026-10-28

Claude uses its relevant design skills and Gate 1's midnight blue, ice blue, electric blue and
chartreuse direction. S7 retains FastAPI, Jinja/server-rendered HTML and the approved screen
functions; no TSX visualization or framework migration. S6 remains open for live evidence.
After S7, prepare the costed S6 validation plan described in Gate 4 and stop before paid work.
No call-end alert fallback, voice-agent or verdict-rule change is included in S7.

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
| `src/scamkaki/app/templates/*.html` | Dashboard, report and family alert pages, from the Gate 1 mockups; `_theme.html` is the shared stylesheet partial, included by all three (S7 amendment, wording only) |
| `migrations/0001_init.sql` | Tables from Gate 2 |
| `migrations/0003_family_alerts.sql` | `guardian_checks.language` and `guardian_checks.alert_status` |
| `migrations/0005_guardian_signs.sql` | `guardian_checks.channel`, `guardian_checks.tactics`, `guardian_checks.acted`, with defaults |
| `agents/{bait,bait_hi,guardian,guardian_hi}.json` | Bolna agent exports, versioned; `_hi` files are the Hindi agents; Bait files also carry their Bolna extraction (disposition) definitions |
| `seed/scripts.json` | Labeled fixture cases, each with `language` and `for` (`bait` or `guardian`). Bait: the existing 5 English scam and 2 Hindi scam cases, unchanged. Guardian: 12 new English cases (8 sophisticated scams, 4 legit look-alikes) and 3 new Hindi cases (2 scam, 1 legit), listed below; the old easy Guardian cases and the `senior_lines` on Bait cases are removed |
| `scripts/check.py` | Reads the stored fixture calls, compares them with each case and prints pass rates |
| `scripts/caller/` | Fixture caller: human microphone mode for Guardian, with legacy scripted clips retained; logs the input mode and fixture id. Guardian audio filenames include a text digest so changed stories cannot reuse stale audio; Bait paths stay unchanged |
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
def recent_alerts(conn, limit: int = 20) -> list[AlertRow]: ...  # urgent from the last 24 h first, then newest
def add_report(conn, call_id: int, draft: str) -> int: ...
def get_report(conn, report_id: int) -> dict | None: ...   # report with its call and script, for GET /reports/{id}
def mark_reviewed(conn, report_id: int) -> None: ...  # draft to reviewed once; a second call keeps the first time
def recent_calls(conn, limit: int = 50) -> list[CallRow]: ...
def scripts_this_week(conn) -> list[ScriptGroup]: ...
def recent_feed(conn, limit: int = 50) -> list[dict]: ...  # Guardian checks and Bait scripts by time, tagged by kind (S7)

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
- `test_family_alerts_list_recent_urgent_first`
- `test_family_alerts_older_urgent_falls_back_into_time_order` (amendment 2026-10-28)
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
| `en-telco-minlaw-01` | Singtel knew my IC and said a number in my name was used for crime, passed me to a MinLaw officer, keep it secret, stay on the line, move savings for checking | minlaw, transfer, call, handoff+secrecy+stay_on_line+knew_details, none | likely_scam |
| `en-bank-otp-01` | Bank fraud team knew my last four card digits, asked me to read the code to cancel a purchase | bank, otp, call, knew_details, none | likely_scam |
| `en-courier-paid-01` | SMS said parcel address invalid; I paid S$1.64 on the website with my card and typed the code | courier, card_details, sms, link_fee, gave_code_or_card | likely_scam, urgent |
| `en-investment-01` | WhatsApp group teacher's stock tips; I took out a small profit; now top up for the VIP group | investment, transfer, whatsapp, paid_first, none | likely_scam |
| `en-whatsapp-friend-01` | Old friend on WhatsApp needs S$800 today, pay to his cousin's account | friend_family, transfer, whatsapp, new_payee+urgency_threat, none | likely_scam |
| `en-cash-handover-01` | Police officer said to withdraw cash and gold so a colleague can collect and check it | spf, cash_handover, call, secrecy, none | likely_scam |
| `en-job-task-01` | Paid S$30 for liking videos; now deposit to unlock better tasks | employer, transfer, whatsapp, paid_first, none | likely_scam |
| `en-ica-video-01` | ICA said a parcel with fake passports is in my name, moved me to a WhatsApp video call with China police, declare my assets; explicitly no threat, deadline or known IC/card details | china_official, transfer, video, handoff+channel_move, none | likely_scam |
| `en-legit-bank-app-01` | Bank called about a card purchase, my bank app showed they were calling, they only asked yes or no | bank, none, call, knew_details, none | unclear (not likely_scam) |
| `en-legit-singpost-01` | SingPost SMS said my parcel is at the POPStation, no link, no fee | courier, none, sms, none, none | no_scam_signs |
| `en-legit-grandson-01` | My grandson called from his usual number, asked me to PayNow him S$50 for groceries he bought me | friend_family, transfer, call, none, none | unclear |
| `en-legit-cpf-01` | gov.sg SMS reminded me to update my CPF nomination by logging in myself with Singpass, no link | cpf, none, sms, none, none | no_scam_signs |
| `hi-mom-handoff-01` | MOM said my son's work pass has a problem, passed me to a police officer, keep it secret, pay the fine today | spf, transfer, call, handoff+secrecy+urgency_threat, none | likely_scam |
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
11. Warning signs travel as one comma-separated string through Bolna's param template; five LLM-filled values per call is [unknown until S6].
12. The act-now advice (call the bank on the number on the card, then 1799) follows SPF's "report to your bank immediately" guidance [verified, SPF advisory 15 Jul 2026]; the Hindi wording needs a listener check.

## Website redesign program design, 2026-10-30

**Gate 3 amendment, APPROVED 2026-10-30.** Read with Gate 2's redesign route/data contract. This section
supersedes earlier screen-file and dashboard-rendering descriptions under this approved amendment.
No application functions or tests below have been implemented by this planning work.

### Files and ownership

All paths below are repository-relative. Keep the existing Python/Jinja stack.

| File | Planned change |
|---|---|
| `src/scamkaki/app/main.py` | New read routes, query validation and page context; retain existing auth, review and session contracts |
| `src/scamkaki/domain/store.py` | Extend call listing; add detail reads and bounded report queue; no write-model change |
| `src/scamkaki/app/presentation.py` | New pure stored-transcript-to-turn projection, no persistence or provider calls |
| `src/scamkaki/app/templates/_theme.html` | Shared palette, typography, status/diagram styles, focus and responsive layout |
| `src/scamkaki/app/templates/_reviewer.html` | New Jinja reviewer shell, active navigation and fixture/provenance treatment |
| `src/scamkaki/app/templates/_error.html` | New reusable 503 content with a local retry link |
| `src/scamkaki/app/templates/dashboard.html` | Overview, priority alert, short review queue, activity and matching diagram |
| `src/scamkaki/app/templates/calls.html` | New query form, call table/phone records, paging, empty and no-match states |
| `src/scamkaki/app/templates/call.html` | New stored call facts, transcript turns, missing-transcript state and Bait report link |
| `src/scamkaki/app/templates/check.html` | New independent check detail, recorded-input diagram and alert state |
| `src/scamkaki/app/templates/patterns.html` | New seven-day bars and expandable agency/request explanations |
| `src/scamkaki/app/templates/report.html` | Focused review with empty entry state, required checkbox and persisted reviewed state |
| `src/scamkaki/app/templates/voice.html` | New room; move existing SDK/controller here, with explicit start and lifecycle states |
| `src/scamkaki/app/templates/family.html` | Standalone family restyle, retain existing IDs/access/polling, clear successful empty results |
| `tests/unit/test_presentation.py` | Transcript projection cases, including continuation/unlabelled/Hindi text |
| `tests/integration/test_dashboard.py` | Move existing claims to owning pages; preserve warnings, urgency, provenance and activity assertions |
| `tests/integration/test_calls.py` | New list/detail/search/page boundaries, failed records, escaping and honest missing fields |
| `tests/integration/test_checks.py` | New independent check detail, verdict/status mappings and absence of inferred links |
| `tests/integration/test_patterns.py` | New actual seven-day grouping, EN/HI aggregation, empty and zero-safe bars |
| `tests/integration/test_reports.py` | Entry choice, new layout, same persisted review guarantees and all existing guard tests |
| `tests/integration/test_voice.py` | New room/auth/configuration handling and fake session contracts |
| `tests/integration/test_family.py` | Preserve secret-link, ordering, labels, headers and safe family output |
| `tests/support/fakes.py` | Only scoped additions needed for UI fixture records; no live fallback |
| `scripts/preview_ui.py` | Local synthetic preview using existing dependencies and explicit test settings/fake providers |
| `scripts/check_ui.mjs` | Offline DOM/controller checks with Node built-ins and small fake elements/events; no session mint or browser dependency |
| `docs/plans/scamkaki/evidence/s8-workspace.md` through `s12-family-ui.md` | One factual evidence record per slice, including failures, screenshots and unavailable checks |
| `docs/plans/scamkaki/00-status.md`, `PROGRESS.md` | Slice state and operational continuation, with approvals held only in status |

Do not change `agents/`, fixture expectations, verdict/extraction/leak/alert/report-draft rules,
migrations, CI, dependency manifests or lockfiles. Keep old mockups and failed evidence.
No installation is implied. Remove moved dashboard call-controller code when Voice owns it;
do not leave duplicate event handlers or unused queries. Preserve every behavior assertion
when its content moves to a different screen rather than weakening it to accept the old page.

### Types and signatures

Proposed signatures, no implementation bodies. Existing rows stay dictionaries, matching the
store convention. No generic repository or UI service layer is introduced.

```python
# app/presentation.py
@dataclass(frozen=True)
class TranscriptTurn:
    speaker: Literal["ah_ma", "caller", "unlabelled"]
    text: str


def transcript_turns(transcript: str) -> list[TranscriptTurn]: ...


# domain/store.py, additions/extension
# List projection excludes transcript, extracted payload and raw payee details.
def recent_calls(
    conn: psycopg.Connection,
    limit: int = 50,
    *,
    query: str = "",
    line: Line | None = None,
    offset: int = 0,
) -> list[dict[str, Any]]: ...
def get_call(conn: psycopg.Connection, call_id: int) -> dict[str, Any] | None: ...
def get_check(conn: psycopg.Connection, check_id: int) -> dict[str, Any] | None: ...
def recent_reports(
    conn: psycopg.Connection,
    limit: int = 5,
    *,
    drafts_only: bool = True,
) -> list[dict[str, Any]]: ...


# get_call: call row plus optional report_id; never joins a Guardian check.
# get_check: check row plus urgent = acted in HARM_ACTED; no synthetic call relation.
# Extend existing get_report projection with call_id for its source-call link.
# recent_reports: id, call_id, status, reviewed_at, created_at, agency, demand,
# language, fixture_case. Drafts first, then created_at DESC, id DESC.
# Existing scripts_this_week, recent_feed, recent_alerts and get_report are reused.


# app/main.py, all reviewer endpoints have dependencies=[AdminDep]
def calls_page(
    request: Request, settings: SettingsDep, q: str = "", line: Line | None = None, page: int = 1
) -> HTMLResponse: ...
def call_page(call_id: int, request: Request, settings: SettingsDep) -> HTMLResponse: ...
def check_page(check_id: int, request: Request, settings: SettingsDep) -> HTMLResponse: ...
def patterns_page(request: Request, settings: SettingsDep) -> HTMLResponse: ...
def reports_entry(request: Request, settings: SettingsDep) -> Response: ...
def voice_page(request: Request, settings: SettingsDep) -> HTMLResponse: ...


# Annotate q with max_length=100 and page with ge=1, le=1000 at the request boundary.
# Positive record IDs; invalid inputs -> 422, missing positive IDs -> 404.
# Page size is fixed at 50; query 51 rows and expose only the first 50.
```

No route-specific data object is needed beyond explicit template context. Use existing
label dictionaries and `duration`/`sgt` filters. Order ties by id for stable navigation.
One helper may render reviewer 503s if duplication merits it; no global error framework.

### Call stacks and state

- Overview GET: admin check, existing feed/week/alerts and five drafts, render Overview.
  Priority uses only a likely-scam harmful-acted alert from the last 24 hours. Activity links
  Guardian rows to checks and Bait rows to reports. It never links checks to calls by time.
- Calls GET: validate query, parameterized filtered SQL with offset and one-row lookahead,
  format list facts and URLs, render Calls. Detail GET reads by primary key and projects the
  stored transcript; Jinja escapes every turn. Missing durations never display as zero.
- Check GET: read by primary key, label stored fields and urgent state, render Check.
  Alert states are sending/sent/failed/not configured/not recorded. Sent never reads Delivered.
- Patterns GET: existing seven-day grouping, compute largest count or zero, render bars with
  adjacent numeric text. No extra aggregation, new matching logic or invented pattern story.
- Reports GET: choose newest draft, else newest reviewed row; 303 to the existing detail URL;
  empty data renders an empty Reports screen. Report GET uses existing `get_report`. Browser
  requires a checked acknowledgment to submit; the existing POST retains its auth/origin,
  first-review timestamp and reviewed-draft semantics. No new server confirmation field.
- Voice GET: read configured agent availability, render selected persona/language and explicit
  credit/microphone disclosure. Missing agent configuration disables Start with explanation.
  `idle -> connecting -> connected -> ended`, with `error` returning controls to usable state.
  One SDK instance per attempt; ignore callbacks from superseded attempts. Selection and GET
  produce zero provider calls. Only Start invokes the existing session flow. After call end,
  show a link to Calls rather than automatically taking the user away.
- Family GET: existing private-link check and headers, render standalone shell. Poll JSON
  through existing path only. Render with `textContent`/DOM nodes, never untrusted innerHTML.
  Successful empty data clears old content; a fetch failure retains it with a stale marker.
  Preserve earlier alerts, sound opt-in and reduced-motion behavior.

State transitions and guards belong to the owning template/controller. Use native form and
button semantics; no controller framework. Calls search and review work with native forms.
Voice requires JS; its no-JS message explains that. Family no-JS explains that alerts cannot
refresh. Reviewer read errors return 503. Detail-not-found is distinct from an empty collection.

### Test plan and guard proof

Planned tests exercise real routes and database rows with fake providers. Names are proposed;
existing behavior tests remain unless their assertions move to the owning page.

| Test or group | Observable assertion |
|---|---|
| `test_reviewer_routes_require_admin` | Every new read route/redirect returns 401 without credentials or with wrong credentials; no record output |
| `test_calls_search_and_line_filter_apply_before_paging` | Matching row beyond the first unfiltered 50 is found; query and line combine, links retain state |
| `test_calls_paging_is_bounded_and_stable` | 51+ fixtures, equal timestamps, no duplicate rows across first/second page; invalid query/line/page is 422 |
| `test_calls_keep_failed_records_and_missing_duration` | Failed, stopped and other stored statuses remain visible; None and zero durations differ |
| `test_call_details_use_saved_time_and_escape_transcript` | Recorded label, original text, speaker/continuation handling, escaped hostile text, no invented times |
| `test_call_and_check_are_not_joined_by_time_or_fixture` | Conflicting nearby rows never place a check verdict on a call |
| `test_check_page_preserves_verdict_urgency_and_alert_states` | Every verdict/status, urgent/none/unsure and missing signs have literal expected labels |
| `test_overview_priority_excludes_old_urgent` | Recent urgent priority, old urgent retained in history and no inflated priority count |
| `test_patterns_show_only_seven_day_bait_groups` | EN+HI same-pair count, different demand separate, eight-day row excluded, empty has no divide-by-zero |
| `test_report_entry_chooses_draft_then_reviewed_then_empty` | Correct destination or empty view; stable ties and auth |
| Existing report review tests | Database status/timestamp survives reload; second review preserves time, redelivery preserves draft; no Telegram or Bolna side effects |
| `test_reviewer_read_failure_is_not_empty_data` | Injected database read error gives 503/Retry; no false No calls yet result |
| `test_voice_room_requires_explicit_start` | Fake SDK/session counters zero before Start; one on Start; selection alone never calls; connecting locks selection |
| Offline voice/family controller cases | Call end/error/repeated click/late event handling, safe text rendering, stale and successful-empty states |
| Existing family guard/order tests | Wrong or unset link stays 404; likely scam only; 24-hour urgent-first and headers persist |

Guard claims require independent mutations: remove each new route's admin dependency; remove
filter before paging; remove harmful-acted/24-hour condition; force missing transcript/duration
into fabricated values; infer call/check linkage; bypass escaping; flatten alert status; bypass
review auth/origin/idempotency; start voice on load/selection; leave stale family alert on empty.
Run each relevant check, retain failures, restore exact bytes. Avoid claiming whole-system coverage.

Inject representative hostile HTML and secret-like synthetic needles on the actual rendered
HTML and family JSON/text surface for the claimed absence/escaping checks. Do not change or
relabel the existing Ah Ma leak scanner's separate scope as full transcript privacy protection.

### Verification and least confident decisions

Use focused tests during each slice, then existing full unit/integration, Ruff lint/format,
`node scripts/caller/check-live.mjs`, new offline UI checks and `git diff --check`. Use only the
verified test branch with fake providers when separately authorized; integrations migrate and
truncate that branch. A local preview must pass explicit test settings and cannot fall back
to production. Do not run it with default `.env.local` application settings.

Browser-check actual pages at 1280 and 375 px, keyboard order/focus, Hindi, expanded text,
empty/error/missing states and all reachable links. Record screenshots, HTTP responses and
measured overflow. Verify Overview-to-urgent/report/call paths in at most two navigation steps.
Human comprehension remains [unknown] until someone performs a walkthrough; automated navigation
is not a usability result. Missing tools/checks are recorded, with no automatic installation.

1. [hypothesis] A Reports navigation entry that opens the newest draft is sufficient. If a
   full report-list screen is needed, return to Gate 1 rather than silently add a ninth screen.
2. [verified] Call/check linkage is incomplete. This plan deliberately displays no Guardian
   verdict on a call, even if an individual nullable execution id happens to be populated.
3. [hypothesis] Fixed 50-row pages and a page cap of 1000 suit the fixture-scale project. No
   performance or production-load result is claimed; do not add indexes without evidence.
4. [unknown] Real transcript variants may differ from the stored fixture strings. Keep
   unlabelled fallback readable and never infer missing turns or identities.
