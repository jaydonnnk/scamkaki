# Architecture: Scamkaki

Compact gate draft, 2026-10-22.
Greenfield repo; no existing code to fit.
Revised 2026-10-22: English and Hindi through Bolna's stock providers; the Modal Hokkien TTS is removed; Mandarin is a stretch.

## Shape

- **Bolna** runs four phone agents end to end, one per persona and language: Guardian EN, Guardian HI, Bait EN, Bait HI.
  Each has a fixed speech-to-text language and a stock voice.
  Bolna handles telephony, speech-to-text, LLM (Bolna-hosted `gpt-5.4-mini`), voice, graph routing, per-value extraction and call transfer.
- **One Python web app** (FastAPI) receives Bolna webhooks, serves the Guardian `match_script` custom function, and renders the dashboard with server-side HTML.
- **Neon Postgres** stores calls, scripts, Guardian checks and report drafts.
- The app maps each Bolna agent id to its persona (`line`) and `language`.
- Script matching is **structured**: same claimed agency and demand within 7 days, using Bolna's allowed-value extraction on all agents.
  Extracted values are the same English enum in both languages, so a script Bait HI collects counts for Guardian EN and the reverse.
  No embeddings, no pgvector.

## Endpoints

| Route | Verb | Caller | Purpose |
|---|---|---|---|
| `/bolna/webhook/{token}` | POST | Bolna | Call status events; on completion, fetch the execution and store it |
| `/tools/match-script` | POST | Bolna Guardian custom function | Return verdict, similar-script count and a sentence for Ah Ma to say |
| `/` | GET | Reviewer | Dashboard: live calls and scripts this week |
| `/web-call/session` | POST | Reviewer | Mint a Bolna web call session for a Guardian agent (`language` `en` or `hi`) |
| `/reports/{id}` | GET | Reviewer | One report draft |
| `/reports/{id}/review` | POST | Reviewer | Mark reviewed; sends nothing |
| `/healthz` | GET | Warm-up ping | Liveness |

Webhook auth: secret token in the path [hypothesis: Bolna documents webhook source IPs, not signatures; verify].
Tool auth: bearer token in the custom function's `api_token` header field.
Dashboard auth: HTTP Basic admin sign-in (`ADMIN_USERNAME`, `ADMIN_PASSWORD`) on `/` and `/web-call/session` (amendment 2026-10-22); fixtures only, no real personal data.

## Data

- `calls`: `id`, `execution_id` (unique), `line` (`bait` | `guardian`), `language` (`en` | `hi`), `fixture_case` (nullable), `transcript`, `extracted` (jsonb), `leaks` (jsonb), `status`, `duration_s`, `created_at`.
  Queries: upsert by `execution_id`; latest 50 for the dashboard.
- `scripts`: `id`, `call_id`, `agency`, `demand`, `payee_bank`, `payee_account`, `paynow_id`, `url`, `summary`, `created_at`.
  Queries: count by `(agency, demand)` where `created_at > now() - 7 days`; group by `(agency, demand)` for "scripts this week".
- `guardian_checks`: `id`, `execution_id` (nullable at tool time), `agency`, `demand`, `verdict`, `similar_count`, `created_at`.
- `reports`: `id`, `call_id`, `draft`, `status` (`draft` | `reviewed`), `reviewed_at`.

Migrations are ordered SQL files applied by a small runner; no ORM.

## Flow

**Bait:** scam call, then Bolna Bait graph agent (stall nodes, mission probes, extraction), then call ends, then Bolna posts the webhook, then the app fetches `GET /executions/{id}` (debug bundle when needed), stores the call, runs the leak guard on Ah Ma's turns, writes a `scripts` row and a draft `reports` row.

**Guardian:** senior call, then Bolna Guardian graph agent extracts `agency` and `demand` from what the senior describes, then calls `POST /tools/match-script`, then the app counts matching scripts, decides the verdict, logs a `guardian_checks` row and returns a sentence, then Ah Ma speaks it.
On "likely scam" the agent's prompt calls the transfer tool to the family number configured on the agent.
Then the webhook stores the call as above, without a script row.

**Tests:** a Bolna "Scammer" test agent and a "Senior" test agent, each prompted from one `seed/scripts.json` case, call the real agents; `scripts/check.py` reads the stored results and prints pass rates.

## External

| Service | Use | Env var names |
|---|---|---|
| Bolna API | Agents, executions, test calls | `BOLNA_API_KEY`, `BOLNA_BAIT_AGENT_ID`, `BOLNA_BAIT_ZH_AGENT_ID`, `BOLNA_GUARDIAN_AGENT_ID`, `BOLNA_GUARDIAN_ZH_AGENT_ID`, `BOLNA_WEBHOOK_TOKEN`, `BOLNA_TOOL_TOKEN` |
| Neon Postgres | App DB and a test branch | `DATABASE_URL`, `TEST_DATABASE_URL` |
| Render (web service) | Public HTTPS for webhook, tool and dashboard | `APP_BASE_URL`, `LOG_LEVEL`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` |

Hosting choice: Render, as on Envoi.
Free instances sleep when idle, and a cold start during a Guardian tool call may exceed Bolna's tool timeout [unknown]; mitigate with a warm-up ping before demos, or a paid instance if you approve the spend.

## Known limits

- Bolna has no custom speech-to-text, so Hindi understanding depends on Bolna's providers; Bolna accepts `hi` on AssemblyAI at agent creation [verified 2026-10-22], call quality [unknown until S2]; Guardian HI falls back to yes/no and keypad questions.
- One agent per language, not one multilingual agent, because mid-call language switching on Bolna is unverified; the cost is one line per language.
- Mandarin is a stretch: two more agents (`zh`) only after S6, with no schema change beyond the `language` value; blocked today because Bolna refuses `zh` on every transcriber ([evidence](evidence/s2-mandarin-stt-precheck.md)).
- Detecting who forwarded a call (SIP `Diversion`) needs our own carrier trunk; out of scope.
