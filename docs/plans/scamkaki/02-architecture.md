# Architecture: Scamkaki

Compact gate draft, 2026-10-22.
Greenfield repo; no existing code to fit.
Revised 2026-10-22: English and Hindi through Bolna's stock providers; the Modal Hokkien TTS is removed; Mandarin is a stretch.
Revised 2026-10-24: family alerts by Telegram and a family alert page replace Bolna call transfer.
Revised 2026-10-27 (reopened): Guardian also extracts how the senior was contacted, warning signs and whether the senior already acted; `guardian_checks` stores them; agency and demand values grow. Bait is unchanged.

## Shape

- **Bolna** runs four phone agents end to end, one per persona and language: Guardian EN, Guardian HI, Bait EN, Bait HI.
  Each has a fixed speech-to-text language and a stock voice.
  Bolna handles telephony, speech-to-text, LLM (Bolna-hosted `gpt-5.4-mini`), voice, graph routing and per-value extraction.
- **One Python web app** (FastAPI) receives Bolna webhooks, serves the Guardian `match_script` custom function, and renders the dashboard with server-side HTML.
- **Neon Postgres** stores calls, scripts, Guardian checks and report drafts.
- **Family alerts** come from the app, not the agent: when `match_script` decides `likely_scam`, the app records the alert on the Guardian check and sends a Telegram message after it has answered Bolna.
  This does not depend on the LLM choosing to call a tool.
- The app maps each Bolna agent id to its persona (`line`) and `language`.
- Guardian's verdict is a **deterministic rule** over five values the Guardian agent passes in its tool call: claimed agency, demand, contact channel, warning signs and whether the senior already acted.
  The LLM only fills those values from what the senior says; the app decides. A warning-sign rule catches scams whose demand sounds ordinary.
- Script matching is **structured**: same claimed agency and demand within 7 days, using Bolna's allowed-value extraction on all agents.
  Extracted values are the same English enum in both languages, so a script Bait HI collects counts for Guardian EN and the reverse.
  No embeddings, no pgvector.

## Endpoints

| Route | Verb | Caller | Purpose |
|---|---|---|---|
| `/bolna/webhook/{token}` | POST | Bolna | Call status events; on completion, fetch the execution and store it |
| `/tools/match-script` | POST | Bolna Guardian custom function | Take agency, demand, channel, warning signs and acted; return verdict, similar-script count and a sentence for Ah Ma to say |
| `/` | GET | Reviewer | Dashboard: live calls and scripts this week |
| `/web-call/session` | POST | Reviewer | Mint a Bolna web call session for a Guardian agent (`language` `en` or `hi`) |
| `/reports/{id}` | GET | Reviewer | One report draft |
| `/reports/{id}/review` | POST | Reviewer | Mark reviewed; sends nothing |
| `/family/{link_token}` | GET | Family member | Family alert page; checks for new alerts every 5 seconds and flashes and beeps on a new one |
| `/family/{link_token}/alerts` | GET | Family alert page | JSON list of recent `likely_scam` alerts, with channel, warning signs and acted, urgent first |
| `/healthz` | GET | Warm-up ping | Liveness |

Webhook auth: secret token in the path [hypothesis: Bolna documents webhook source IPs, not signatures; verify].
Tool auth: bearer token in the custom function's `api_token` header field.
Family auth: a long random secret in the path (`FAMILY_LINK_TOKEN`), so the family member needs no password; anyone with the link sees the alerts, and rotating the token revokes it.
Dashboard auth: HTTP Basic admin sign-in (`ADMIN_USERNAME`, `ADMIN_PASSWORD`) on `/` and `/web-call/session` (amendment 2026-10-22); fixtures only, no real personal data.

## Data

- `calls`: `id`, `execution_id` (unique), `line` (`bait` | `guardian`), `language` (`en` | `hi`), `fixture_case` (nullable), `transcript`, `extracted` (jsonb), `leaks` (jsonb), `status`, `duration_s`, `created_at`.
  Queries: upsert by `execution_id`; latest 50 for the dashboard.
- `scripts`: `id`, `call_id`, `agency`, `demand`, `payee_bank`, `payee_account`, `paynow_id`, `url`, `summary`, `created_at`.
  Queries: count by `(agency, demand)` where `created_at > now() - 7 days`; group by `(agency, demand)` for "scripts this week".
- `guardian_checks`: `id`, `execution_id` (nullable at tool time), `agency`, `demand`, `channel`, `tactics` (text array of warning signs), `acted`, `verdict`, `similar_count`, `language`, `alert_status` (`null` unless `likely_scam`; then `pending` until the Telegram send finishes, and `sent`, `failed` or `off` when Telegram is not configured), `created_at`.
  Queries: latest 20 `likely_scam` rows for the family page.
  Migration 0005 adds `channel`, `tactics` and `acted` with defaults (`other`, empty, `none`) so older rows stay valid.
- `reports`: `id`, `call_id`, `draft`, `status` (`draft` | `reviewed`), `reviewed_at`.

Migrations are ordered SQL files applied by a small runner; no ORM.

## Flow

**Bait:** scam call, then Bolna Bait graph agent (stall nodes, mission probes, extraction), then call ends, then Bolna posts the webhook, then the app fetches `GET /executions/{id}` (debug bundle when needed), stores the call, runs the leak guard on Ah Ma's turns, writes a `scripts` row and a draft `reports` row.

**Guardian:** senior call, then Bolna Guardian graph agent asks who, how, what, three warning-sign questions and whether the senior already acted, repeats it back, then calls `POST /tools/match-script` with `agency`, `demand`, `channel`, `tactics` (a comma-separated string) and `acted`, then the app drops unknown values, counts matching scripts, decides the verdict, logs a `guardian_checks` row and returns a sentence, then Ah Ma speaks it.
On "likely scam" the app also marks the check as an alert, and after answering it sends the Telegram message and records `alert_status`; the family page shows the alert on its next check.
Then the webhook stores the call as above, without a script row.

**Tests:** a local synthetic-caller page plays one `seed/scripts.json` case's scripted caller lines (macOS `say`) into a Bolna web call to the real agent, passing the case id as web call `user_data`; `scripts/check.py` reads the stored results and prints pass rates.
Bolna has no agent-to-agent test feature and our trial account dials only +1/+91 with no number for Bait, so test agents cannot call our agents (amendment 2026-10-24).

## External

| Service | Use | Env var names |
|---|---|---|
| Bolna API | Agents, executions, test calls | `BOLNA_API_KEY`, `BOLNA_BAIT_AGENT_ID`, `BOLNA_BAIT_HI_AGENT_ID`, `BOLNA_GUARDIAN_AGENT_ID`, `BOLNA_GUARDIAN_HI_AGENT_ID`, `BOLNA_WEBHOOK_TOKEN`, `BOLNA_TOOL_TOKEN` |
| Neon Postgres | App DB and a test branch | `DATABASE_URL`, `TEST_DATABASE_URL` |
| Telegram Bot API | Family alert message, sent to one chat | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| Render (web service) | Public HTTPS for webhook, tool and dashboard | `APP_BASE_URL`, `LOG_LEVEL`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `FAMILY_LINK_TOKEN` |

Hosting choice: Render, as on Envoi.
Free instances sleep when idle, and a cold start during a Guardian tool call may exceed Bolna's tool timeout [unknown]; mitigate with a warm-up ping before demos, or a paid instance if you approve the spend.

## Known limits

- Bolna has no custom speech-to-text, so Hindi understanding depends on Bolna's providers; Bolna accepts `hi` on AssemblyAI at agent creation [verified 2026-10-22], call quality [unknown until S2]; Guardian HI falls back to yes/no and keypad questions.
- One agent per language, not one multilingual agent, because mid-call language switching on Bolna is unverified; the cost is one line per language.
- Mandarin is a stretch: two more agents (`zh`) only after S6, with no schema change beyond the `language` value; blocked today because Bolna refuses `zh` on every transcriber ([evidence](evidence/s2-mandarin-stt-precheck.md)).
- Bolna call transfer was attempted in S3 and blocked on our account ("request blocked by outbound URL policy"); a phone transfer needs a paid telephony setup and stays out of scope.
- The family is only reached if they have Telegram set up or the family page open; nobody is phoned automatically, and a missed alert is not retried.
- Detecting who forwarded a call (SIP `Diversion`) needs our own carrier trunk; out of scope.
- Warning signs travel as one comma-separated string because Bolna's custom-function param template fills `%(name)s` text values; whether the LLM fills five values reliably is [unknown until S5]. Unknown signs are dropped, never guessed.
- Guardian's call grows by about four questions; keeping it under three minutes for a senior is [unknown until S5].
- The verdict is only as good as what the senior tells Guardian and what speech-to-text hears; a senior who hides the secrecy instruction defeats the warning-sign rule.
- Bait's extraction and `scripts` are unchanged, so the 7-day count still matches on agency and demand only; Bait never produces the new agency and demand values (telco, MAS, MinLaw, cash handover and others), so those always count 0 until Bait is extended.
