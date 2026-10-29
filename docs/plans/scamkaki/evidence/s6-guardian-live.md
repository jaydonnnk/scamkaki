# S6 evidence: Guardian five-field conversation

Current state, 2026-10-28: offline repairs complete; live validation deferred by the user.
Both repaired Guardian configurations were accepted and read back. S6 is not a live pass.
Older pending plans below are historical; the final repair result records their resolution.

Branch `scamkaki/slice-6-guardian-live`, from main `59b918d`.
All calls are synthetic senior fixtures, never real seniors or real scam calls.

## Authority and sample

The user authorized starting S6, both Guardian Bolna updates and fixture web calls with a
US$1 total cap including the probe. They permitted cuts because credits are limited.
Pravesh is the Hindi listener. No commits, pushes, main integration, Bait changes or old-clip
deletion are authorized.

Use the approved cut order. No Hindi live run. One English `en-ica-video-01` probe, then at
most four English cases only if the probe succeeds and the remaining budget covers a call:
`en-telco-minlaw-01`, `en-courier-paid-01`, `en-legit-grandson-01`, `en-legit-bank-app-01`.
The reduced run cannot establish the original 12-English or 3-Hindi targets.
No retries are automatic. Preserve every call and its cost, including failed probes.

## Local implementation [verified]

- Both Guardian prompts collect agency, demand, channel, the three warning-sign questions and
  already-acted status; repeat back and wait for confirmation; call `match_script` once.
- All five values are required in both schemas and param templates; enums match domain types.
  Warning signs remain a comma-separated string, with the empty string for no signs.
- Every Guardian fixture has an explicit answer about negative signs and already-acted state.
  Guardian clips generated locally with Daniel and Lekha. Old clips preserved.
- Caller has a 180-second cap for Guardian. This does not establish conversation length.
- Checker reports five stored values, derives urgent from stored acted, checks required spoken
  advice, duration, alerts and transcript leaks; missing or ambiguous cases fail. `--case` labels
  reduced samples. Attempt counts identify reruns while `runs.jsonl` retains all attempts.
- Bait agents, Bait extraction, verdict rules and the dashboard template are unchanged.

## Offline verification [verified]

Baseline: 199 tests passed, with one existing FastAPI/Starlette deprecation warning.
First implementation pass: 225 tests passed, including 164 unit and 61 integration tests.
Both new schema tests failed on the old agents. The missing-legit regression demonstrated
that the old checker reported PASS with all four legit calls absent; it now fails.
After review fixes: 232 tests passed, including 171 unit and 61 integration tests.
The existing deprecation warning remains. Lint and formatting pass.

18 independent checker mutations caught on the final checker: agency, demand, channel, acted, tactics, language,
ambiguous tool count, alert status, leak scanner self-test, transcript leak, duration,
urgent advice first, first verdict ordering, ordinary spoken verdict, unsafe certainty, grandson
call-back, spoken repeat count, and missing cases. Five further independent mutations each remove
one tool param placeholder and are caught. This is 23 of 23 scoped mutations, not total coverage.
Mutations executed in fresh Python processes against in-memory code; product files untouched.
One initial leak-self-test mutation incorrectly targeted the existing Bait branch, so that
attempt is invalid and was retained separately; the corrected Guardian-only mutation failed
its matching test. Local receipts: `work/scamkaki-s6/mutations*.json`.

## Bolna update [verified]

Both PUTs returned HTTP 200. GET read-back confirmed every configured value, including prompts,
required fields, param templates, speech providers and webhook, on 2026-10-28.
An initial whole-object comparison rejected backend-added default fields; a recursive comparison
of all supplied values confirmed no configured field differed. No extra PUT to Guardian EN.
Render `/healthz` returned HTTP 200 before the probe. Account wallet started at 291.0 vendor units.
Only API fields needed for evidence were retained. No secrets are written to receipts.

## Live result

**FAIL. Stop and re-plan before any further call.**

- Case: `en-ica-video-01`, one English synthetic senior probe.
- Execution: `cd987c05-777a-48df-bfed-59381f9ea8cd`, completed, 135.6 seconds.
- Cost: 13.75 US cents, US$0.1375. Wallet: 291.0 to 277.25 cents. The dashboard displays
  US$2.77 after rounding, confirming the wallet units. Remaining authorized cap: US$0.8625.
- Bolna's execution debug progression confirms three `custom_task_match_script` calls,
  all completed with HTTP 200. They match the three rows linked by the call's time window:
  row 46 at 01:13:41 UTC, row 47 at 01:14:06 UTC, row 48 at 01:15:07 UTC.
- Row 46: `ica`, `personal_info`, `call`, `urgency_threat,knew_details`, `none`.
- Row 47: `china_official`, `other`, `video`, `handoff,channel_move,urgency_threat,knew_details`, `none`.
- Row 48: `china_official`, `transfer`, `video`, `handoff,channel_move,urgency_threat`, `none`.
- Final expected signs are `handoff,channel_move`. The initial check marked the additional `urgency_threat` unsupported. The later user review
  identifies this as ambiguous fixture wording, not an isolated Guardian defect. Earlier calls also guessed a demand before it was supplied.
- All three rows have `likely_scam` and `alert_status=sent`, meaning Telegram accepted them.
  Arrival on the family phone is not checked. No cleanup or deletion of these rows.
- The agent called before the final confirmation and more than once. It asked for confirmation
  again after the caller's final yes, then called the tool without another answer.
- The last transcript ends with "Same script", although `similar_count=1`. The required spoken
  count is not evidenced. The transcript also includes a refusal to help.
- `uv run --offline --no-sync python scripts/check.py guardian --case en-ica-video-01` exits 1.
  It flags `tactics`, `tool_count`, and `repeat`, even though the last verdict is `likely_scam`.
- Transcript leak scanner reports zero leaks and its injected self-test passes. This is one
  text transcript, not an audio or real-world safety claim.

No four-case sample, no Hindi calls and no retry ran. The sample thresholds are untested.
Both Guardian Bolna agents retain the S6 configuration that was read back before this probe.
Local safe receipts and transcript are retained in `work/scamkaki-s6/`; the original call log
is retained in `scripts/caller/runs.jsonl`. These ignored files are local evidence, not published artifacts.

## Evidence limits

Stored tool fields and text transcripts do not prove audible delivery, senior understanding,
real-world accuracy or domain safety. Hindi is offline-checked only until a named listener's
actual review is recorded. No Telegram delivery claim without the corresponding evidence.


## Review and re-plan boundary

A fresh read-only code review reproduced two false passes: a missing or unsafe ordinary spoken
verdict could pass, and a later bank instruction could hide an earlier verdict. Matching tests
failed first, then passed after the checker fixes; corresponding independent mutations fail.
This fixes evidence checking only. It does not repair the live conversation.

Two fixture conflicts remain for the user to resolve before scoring further calls:

- `en-telco-minlaw-01` says the caller knew her IC, while its expected tactics omit `knew_details`.
- `hi-mom-handoff-01` says the fine is due today, while its expected tactics omit `urgency_threat`.

The exact-set checker exposes these conflicts. Expectations and approved gate tables were not
silently changed. The probe's urgency sign is also ambiguous: legal-crime framing can imply a threat even without a deadline.
The proposed repair explicitly denies a threat and known details; do not retroactively pass the old attempt.

Original proposal, superseded by the user's caller-first correction below:

1. Reconcile each story with its expected warning signs and mirror approved fixture changes in
   Gate 3. Do not change the verdict rules to conceal extraction failures.
2. Design a collection and confirmation flow that withholds the tool until confirmation, rather
   than relying on the LLM to obey an exactly-once sentence. Confirm Bolna can support this flow
   on the existing agents before proposing a shared-account change. If this changes approved
   architecture or program design, reopen only the affected gates for approval.
3. Check the caller timing and finish conditions offline. The current fixed clips can overlap
   the agent; do not blame the provider for that without evidence.
4. Request one revised English probe explicitly, inside the remaining US$0.8625 cap. No automatic
   retry and no full sample until the five fields and exactly one confirmed tool call are proven.

Post-slice cleanup was not treated as acceptance because S6 failed its probe. A scoped scan found
no application-layer changes, dependency changes or protected-file edits. The 33 inherited
obsolete clips and untracked `.claude/` remain untouched. S7 is not authorized.


## Caller-first correction, 2026-10-28

[verified] The caller sent fixed lines in sequence, used audio/silence heuristics to advance,
and hung up automatically after the final clip. This confounds conversational extraction and
complete-sentence scoring. [hypothesis] It contributed to the early/out-of-phase replies and
cut ending; this run does not separate caller timing from LLM token limits or Guardian behavior.
The three successful tool calls and accepted Telegram sends remain verified. Arrival is unverified.

The user's revised order is fixture meaning, caller repair, supported LLM settings, one human
role-play probe, then a bounded sample only on probe success. Remaining US$0.8625 stays unspent.

- Gate 3's three-row fixture amendment is drafted and awaits re-approval. Seed expectations
  and ICA story have not changed pending that approval.
- Caller live mode is implemented locally. It uses the native microphone path, plays no clips,
  and does not advance turns or end a verdict by silence detection. Operator hang-up and the
  180-second cap remain. Logs retain `fixture_case`, `caller_mode=live` and `human_roleplay`.
- No per-turn tool-gating feature on `simple_llm_agent` is verified or planned. Prompt lines
  are instructions, not enforced guards.
- Local agent drafts use max_tokens 300 and stronger help/explicit-confirmation instructions.
  Temperature 0.3 was requested, but [Bolna's provider guide](https://www.bolna.ai/docs/openai-llm)
  says GPT-5 models require temperature 1 and reject other values [vendor claim]. The local draft
  retains 1; the user's setting decision is pending. No PUT of these repair drafts has run.
- Call-end alert fallback is not pre-approved. It changes urgent timing and conflicts with the
  current spoken claim "I have alerted your family". Ask again if the new probe repeats.
- Pravesh's wording packet remains pending. No Hindi live call or outreach is authorized here.

Offline caller proof: `node scripts/caller/check-live.mjs` executes the page script with a fake
SDK and no network or microphone. It detects synthetic audio in live mode, automatic clip-timed
progression, wrong case/mode labels and a cap beyond 180 seconds. Python HTTP tests use a fake
Bolna client and prove fixture-id forwarding and rejected input modes before any session mint.
An offline browser preview at http://127.0.0.1:8766 replaces the SDK and refuses real sessions.
It was checked at desktop and 375-pixel phone width, with no horizontal overflow. The preview
shows the facts, defaults Guardian to live input and restores controls after operator hang-up.
This is local UI/control proof, not a microphone transport test or a successful Guardian call.


Caller-first verification: 240 Python tests passed, comprising 179 unit and 61 integration tests,
with the existing deprecation warning; lint and formatting passed. The Node page check passed.
Eight independent caller faults were caught, plus eight configuration/prompt-value faults.
These prove the local branches and stored settings only, not live instruction following.
Receipts: `work/scamkaki-s6/caller-mutations.json`, `repair-config-mutations.json`, and
`repair-local-hashes.json`. These hashes describe local drafts, not an updated Bolna read-back.
Offline preview retained for review at http://127.0.0.1:8766, PID 9291; stop with `kill 9291`.
It loads a fixture snapshot at start and must be restarted after approved fixture edits.


## Final offline repair result, 2026-10-28 [verified]

The user approved the S6 Gate 3 fixture-table amendment and the supported settings, then chose
"just do offline fixes" because credits are too limited for role-play. No follow-up live test
is authorized. This does not waive any S6 live exit check or begin S7.

- Added `knew_details` to the telco fixture's expected tactics and `urgency_threat` to Hindi MOM.
  The ICA story now explicitly denies arrest/fund-freezing threats, a deadline and known IC/card
  details. The revised Gate 3 table and seed agree; verdict rules and all verdict expectations
  are unchanged. The original failed attempt and its old fixture hash remain intact.
- Fixed the Guardian clip cache: filenames include the text digest. Existing audio is retained,
  so a story correction cannot silently reuse old speech. Bait paths are unchanged. All 91
  current fixture clips are non-empty 16 kHz WAVs; no historical clip was deleted.
- Both Guardian PUTs returned HTTP 200. GET read-back matched every supplied configuration
  value, allowing backend-added defaults: gpt-5.4-mini, temperature 1, max_tokens 300,
  explicit yes before a tool call and continued help without refusal. Local template hashes
  are in `work/scamkaki-s6/repair-bolna-readback.json`; no credentials appear there.
- Wallet before and after these updates: 277.25 cents, delta 0. Total S6 spend remains
  US$0.1375; US$0.8625 of the cap remains unspent. No session was minted or call placed.
- Fresh full suite: **244 passed**, 183 unit and 61 integration tests, one pre-existing
  FastAPI/Starlette warning. Ruff lint, formatting and Node offline caller checks pass.
  Four further independent faults were caught: removing each approved expected sign, removing
  the ICA denials, and reusing stale Guardian audio names. Receipts are local in
  `work/scamkaki-s6/fixture-repair-mutations.json`; final source hashes in `final-offline-hashes.json`.
- Application/domain code, Bait agents and Bait fixture content remain unchanged. No install,
  migration, commit, push, main integration, call-end alert fallback or clip deletion.
- The offline browser preview and its server on port 8766 were stopped after the user declined
  role-play. The real caller server on port 8765 is also stopped.

Live instruction following after these changes is unknown. Exactly one confirmed tool call,
correct five-field extraction, full audible advice/count, absence of refusal, alert delivery
and the reduced-sample outcomes remain unproven. Pravesh's Hindi text review is still pending.
S6 remains incomplete under its live exit contract, with further calls deferred by the user.


## Publication authority, 2026-10-28

The user requested "Can.u push the current working tree to main first thanks". This authorizes
committing and publishing the current offline repair and evidence package, not a live pass.
The failed probe, remaining live checks, deferred spending and pending Hindi review remain as
recorded. Actual commit and remote state are taken from Git and the latest 00-status.md record.


## 2026-10-29 live probe attempts and prompt fix

The user authorized the live probe ("Can u run the probe thankjs") under the existing 150-cent
cap, with Mr Tan named as the English role-play operator. Six `en-ica-video-01` live calls ran
and all are invalid; they are preserved in `scripts/caller/runs.jsonl` and on Bolna:

| Execution | Duration | Cost | End | Transcript |
|---|---|---|---|---|
| `9dcc06bd` | 28.7s | 2.75 | `user_hung_up` | Echo; the agent's own TTS transcribed as the user |
| `07171a5f` | 16.1s | 2.75 | `inactivity_timeout` | Greeting only; no user audio captured |
| `7f63fd1c` | 16.0s | 2.75 | `inactivity_timeout` | Greeting only; no user audio captured |
| `4f6c1016` | 16.0s | 2.75 | `inactivity_timeout` | Greeting only; no user audio captured |
| `2def2d7e` | 64.9s | 8.25 | `user_hung_up` | Echo loop; "I heard this" repeated between agent and mic |
| `e3d65395` | 62.0s | 8.25 | `user_hung_up` | Clean user audio; the model duplicated its own sentences |

Total spend 27.5 cents; wallet 277.25 to 249.75. Remaining cap 122.5 of 150. No call reached a
tool call or verdict; `check.py` has not been run on a valid attempt.

The echo calls show the operator must use headphones or a headset so Ah Ma's voice does not
re-enter the microphone. The sixth call had clean user audio, so the transport is usable.

The sixth call's duplication is in the model output, not TTS or echo: the transcript contains
each assistant sentence twice, and Bolna's usage data shows 176 output tokens and 660
synthesized characters, matching the duplicated text. The agent is `gpt-5.4-mini` at
temperature 1, max_tokens 300, the settings approved for S6.

The user authorized a one-line prompt fix ("go ahead and apply the fix"). Added to Guardian EN
only: "Say each sentence once. Never repeat the same sentence in one turn." No model,
temperature, max_tokens, tool or `hangup_after_silence` change. `agents/guardian.json` updated;
`tests/unit/test_agent_twins.py` passes. A full `PUT /v2/agent/{id}` was rejected with
"Agent Config > Webhook URL: Must be a valid URL", so `PATCH /v2/agent/{id}` was used with only
`agent_prompts.task_1.system_prompt`. PATCH returned HTTP 200; the GET read-back matches the
local prompt exactly. Wallet before and after: 249.75 cents, delta zero. No call was placed
during the fix.

The 10-second `hangup_after_silence` is unchanged. If a clean retry still ends on silence, a
timeout change needs separate permission. A retry is pending; no Option B calls are authorized
until Option A passes `check.py`.

Two further calls ran after the first fix, before the shortening change:

- `1e59a081` 72.0s, 8.25c, `inactivity_timeout`. The repeat-back was still duplicated, and the
  agent did not call `match_script` after the operator's "yes yes yes yes"; tool logs are empty.
  LLM output 210 tokens and synthesizer 793 characters match the duplicated text, so the
  repetition is model output, not TTS or echo.
- `5d1aeb95` 2.4s, 2.75c, `user_hung_up`, greeting only.

Total spend is now 38.5 cents; wallet 238.75; remaining cap 111.5 of 150.

The user then asked to shorten the replies ("Can u shorten the replies... The agent just needs
to reiterate the key points"). Authorized and applied to Guardian EN only: "Speak short phrases,
not full sentences", the repeat-back becomes one short phrase with a terse example, and the
final style line changes to short phrases. `agents/guardian.json` updated; the keywords required
by `tests/unit/test_agent_twins.py` are preserved. PATCH returned HTTP 200; the GET read-back
matches the local prompt exactly. Wallet before and after: 238.75 cents, delta zero. No model,
temperature, max_tokens, tool or silence-timeout change.

The duplication and the missing tool call are not yet proven fixed. A retry is pending. If the
model still duplicates or fails to call the tool after confirmation, a model change or further
prompt work needs separate permission.


## 2026-10-29 verdict text change

The user asked for a one-line scam summary at the end: "This is likely a <type of scam>. I have
alerted your family." Authorized and implemented in `src/scamkaki/domain/verdict.py`: the
English `likely_scam` say is now a template formatted with `scam_type(report)`, which derives a
short label from the agency, for example "China official impersonation scam" or "courier
impersonation scam". The urgent ACT_NOW prefix and the similar-count suffix are unchanged.
Hindi is unchanged. `scripts/check.py` now builds the expected say from the stored report and
uses "This is likely a" as the verdict marker. Tests updated; full suite 261 passed. No Bolna
agent change was needed because the agent speaks the tool's say word for word. A live retry is
needed to validate the new sentence.


## 2026-10-29 probe attempt after the shortening fix

Call `eb4b7e5f` (152s, 16.5 cents, `local-hangup`) ran with the shortened prompt but before the
verdict text change. `check.py guardian --case en-ica-video-01` exits 1 with errors `tactics`,
`tool_count`, `spoken_verdict`.

- Stored tactics: `handoff, channel_move, new_payee`; expected `handoff, channel_move`. The
  agent added `new_payee` despite the fixture's explicit denial.
- Link `time x2`: two `guardian_checks` rows in the call's time window, so `match_script` was
  called twice. The prompt requires exactly once after confirmation.
- Spoken verdict: the transcript has the old say, "This is likely a scam. Do not transfer money
  or share any code. I have alerted your family. Please wait for their call. Same script heard
  1 time this week." The expected say is now the new one-line template, so this error is
  expected for a call placed before the text change.
- Alert `sent`, verdict `likely_scam`, agency `china_official`, demand `transfer`,
  channel `video`, acted `none`, similar_count 1.

Total spend is now 55 cents; wallet 222.25; remaining cap 95. The probe has not passed. The
tactics and tool_count failures are real and would persist with the new verdict text. A new
call is needed to validate the new sentence, but the extraction and exactly-once tool call must
also be fixed. No Option B authorization.
