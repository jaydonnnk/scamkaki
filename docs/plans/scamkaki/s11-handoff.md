# S11 handoff

Updated 2026-10-30, Asia/Singapore, for authorized S10 publication. S10 implementation
729000b is committed and in main. S11 execution/test authority remains pending. Background only.

```text
You are receiving background for Scamkaki S11 in /Users/jayd0/Desktop/bolna on macOS arm64.
Prepared 2026-10-30, Asia/Singapore, from published main and actual Git/source state.
This handoff is background only. S10 commit/main integration/push is authorized. Its implementation
729000b is in main. Re-verify final refs after publication. S11 execution/test authority remains pending.

Skeleton: docs/plans/scamkaki/s8-handoff.md and AGENTS.md's eight-section Slice handoff prompts.
Historical S8-S10 prompts supply structure/context, not new execution authority. The gate
documents win. Re-verify Git and files before acting; stop and ask rather than guess on conflict.
Be brief and honest. No em dashes, invented results, weakened checks or co-author trailers.
Visualizations are .html. Never print/hash .env.local or expose credentials. Context transfer
uses transfer-context plus the repository rules around 50-70% of the context window.

1. Project in brief

Scamkaki gives Singapore seniors English and Hindi Guardian phone lines to check suspicious
contact before moving money, or get urgent guidance after acting. The app evaluates recorded
warning signs and alerts family on likely-scam results through Telegram and a private-link
page. Ah Ma Bait stalls fictional scam callers, records claimed agency/request/payee details
and supplies seven-day script counts. A separate human reviewer reads draft reports.

The senior is the person contacted. Family receives alerts and calls back. The fictional
scammer may impersonate an agency, bank, courier, employer, investment group or relative.
The reviewer is separate from the family-link viewer.

Targets from published 01-product.md, not achieved real-world results: family alert within
1 minute and callback before money moves; EN Guardian at least 7 of 8 scam fixtures flagged
and at most 1 of 4 legit; HI Guardian 2 of 2 scams and 0 of 1 legit; both already-acted courier
cases urgent with bank guidance; every likely_scam alerts and no other verdict does; EN Bait
at least 4 of 5 planted payees, HI Bait at least 1 of 2; zero leaks. S6 live proof remains open.
Local fixture/browser checks do not establish effectiveness or human comprehension.

Hard rules: Bait never speaks an NRIC, OTP, card number, password or real-looking bank/PayNow
identifier; she stalls. No agent claims to be a government, police or bank employee. Reports
are drafts, human-reviewed before anything is sent and never automatically filed. Fixtures,
test callers and demo data stay labeled on screens, evidence and videos. Seed stories never
copy victim identities. Guardian outputs are "likely scam", "unclear, talk to family" or
"no scam signs found", never certainty of safety.

[verified 2026-10-30] Gates 1, 2, 3 and 4 remain APPROVED 2026-10-30 for the redesign.
Design/plan approval does not itself authorize S11 implementation, databases or publication.

2. Where S11 sits, all slices and build plan

Approved build order, with current status from working 00-status.md:
- S1: Guardian tracer, webhook/tool/dashboard end to end. Checked done.
- S2: Hindi voice and per-language agent mapping. Checked done; fixture/listener limits retained.
- S3: Guardian verdict and Telegram/private-link family alert. Checked done; sent is not receipt.
- S4: Bait extraction, leak guard, stored scripts and draft reports. Checked done; HI flaky result retained.
- S5: Sophisticated verdict, warning signs and already-acted guidance behind the tool. Checked done.
- S6: Guardian conversation and live validation of the five values. Offline repairs built;
  live proof incomplete. Failed probes/audio and Hindi listener gap remain evidence.
- S7: Dashboard, report review and demo. Built and published; backup video/full live demo open.
- S8: Reviewer workspace, Overview, Calls history and separate call/check detail. Published in main.
- S9: Visual seven-day Bait script patterns and shared matching explanation. Published in main.
- S10: Focused Reports entry/review with persistent first-review time and original draft.
  Complete and committed at 729000b, fast-forwarded into main. Main push is authorized.
- S11: Voice room and explicit-start lifecycle using the existing session endpoint/SDK.
  Approved plan, unstarted; its main prerequisite is met. Execution/test authority is pending.
- S12: Family restyle, safe stale/empty polling, and full eight-screen redesign checks.
  Approved plan, unstarted; depends on S8-S11 in main. There is no S13 plan.

Gate 4 allows the offline UI sequence S8 -> S9 -> S10 -> S11 -> S12 on existing S7 code
without closing S6/S7 gaps. S11 moves the existing test-call controls into a clear dedicated
room; it does not establish that real voice works or repair the agents.

S11 requires S8-S10 in main. This is met by S10 implementation 729000b and its verified
fast-forward into main. Re-verify the final main tip, committed contents and remote refs after
the publication task. Push is not an extra S11 prerequisite. Do not create the S11 branch or
run its destructive checks until the named S11 local/test grant exists.

Build plan after those prerequisites and the named S11 local/test grant exist:
A. Verify the committed S10 package/main tip, create scamkaki/slice-11-voice-room from it,
   inventory inherited work and establish the focused/full baseline with fake providers.
B. Add failing real-route/configuration tests and offline controller checks. The intended
   breaks are implicit Start, duplicate attempts, changing selection mid-call and stale events.
C. Build /voice in the existing reviewer shell. Move the pinned SDK, call controls and owning
   controller out of Overview. Keep Overview's appropriate refresh/focus behavior; no duplicate
   SDK/controller or Voice auto-refresh. Navigation exposes the implemented Voice destination.
D. Implement the approved configuration and lifecycle states with native controls: availability,
   explicit disclosure/Start, connecting/connected, hang-up/end/error recovery and Calls link.
   Preserve the existing session URL/query/body/response behavior and EN/HI line mapping.
E. Extend the safe preview for the new Voice owner and controlled fake lifecycle. Prove zero
   effects before Start, exactly one fake attempt on Start, one-at-a-time behavior, recovery
   and late-event isolation at 1280/375 px. No real microphone, provider session or credit use.
F. Independently mutate the affected guards and restore exact bytes. Run the relevant full
   checks, record actual evidence and update status/progress. Use architect-reviewer for scoped
   post-slice cleanup, preserve historical work, and stop before S12.

Never cut S1, S3, S4's leak guard, S5's already-acted/offline fixture checks, fixture labels,
failed attempts, honest missing fields, independent call/check records, warning/urgent meanings,
auth, human report review or family isolation. Original cut order: S7 extra polish, S6 Hindi
live, then English reduced to four named cases with disclosure. Redesign cuts optional motion,
decoration and duplicate copy first. Cutting an approved screen/function needs user re-steering.

3. S11 contract

Copied verbatim from published 04-slices.md, "### S11: Voice room":

- **Branch:** `scamkaki/slice-11-voice-room`; depends on S8-S10 in main.
- **Visible result:** Voice room lets a reviewer select Guardian/Bait and English/Hindi, read the
  microphone/credit disclosure and explicitly start. Connection, hang-up and failure are clear.
- **Builds:** `/voice`, owning template/controller, existing pinned SDK and session endpoint.
  Move call UI/controller out of Overview. No agent, model, price, prompt, tool or transcript change.
  State machine and configured-agent availability follow Gate 3; no duplicated SDK/controller.
- **Assigned tests:** route auth and configuration handling; fake-provider session contract;
  offline controller explicit-start/one-at-a-time/end/error/late-event checks. Selection and page
  load counters must remain zero; Start increments exactly once under the fake SDK.
- **Evidence:** `evidence/s11-voice-room.md`; fake-provider browser connection lifecycle and
  offline checks, screenshots at both widths, SDK/controller guard mutation receipts. Run no
  real microphone/provider session to make this evidence.
- **Falsifiers:** session minted on load/selection/navigation; double click creates two sessions;
  selectors change during connection; stale events reset a newer call; hidden account credit use.
- **Exit decision:** local fake lifecycle passes. Actual provider audio/connection remains
  unverified by this slice; stop for S12 authorization.
- **Authorizations to request:** S11 local implementation/branch and named test-branch checks.
  Any real web call or microphone/provider validation needs a separate named scope and budget.

Gate 2/3 constraints:
- Keep FastAPI/Jinja/Postgres, existing dependencies, system fonts, HTML/CSS/inline SVG and
  the midnight/ice/electric blue palette. Chartreuse is restrained fixture/emphasis color,
  never a safety claim. No new framework, schema, library or external font.
- GET /voice uses AdminDep and configuration availability. Missing agent configuration
  disables Start with an explanation. Family keeps FamilyDep and no reviewer navigation.
- The pinned SDK belongs only on /voice after the move. Load, selection, navigation and
  polling mint no session. Only Start conversation triggers the existing microphone/SDK flow.
- State is idle -> connecting -> connected -> ended; error restores usable controls. One SDK
  instance per attempt. Selection is locked while connecting/connected, repeat Start cannot
  make another attempt, and stale callbacks cannot reset a newer attempt.
- Hang-up, call end and connection failure recover clearly. After call end there is a Calls
  link, not automatic navigation. Voice never reloads during a conversation. No-JS explains
  that voice requires JavaScript. Status/error text stays readable and safely rendered.

4. Out of scope

S12 owns family restyling and stale/empty polling repair, plus complete eight-screen final
verification. S11 preserves all existing Reports URLs, first-review time, reviewed draft,
no-send behavior, source links and access to other reports; it does not redesign S10 again.
S8 independent call/check meaning and S9 seven-day Bait record counts remain unchanged.

Protected: agents/, seed meanings/expectations, verdict/extraction/leak/alert/report-draft
rules, migrations, CI, manifests/lockfile, retained failed S6 records/audio and historical
mockups. No agent/model/price/prompt/tool/transcript/session-provider contract change, languages,
transfer, embeddings, filing, identity matching, network tracking or broad cleanup.

No production write, real microphone/provider session/call, wallet read, agent update,
Telegram message, spending, provisioning, installation, S6 rerun or S7 completion claim.
The S10 commit/main integration/push is authorized. S11 publication/deployment and S12
remain separately scoped.

5. Current state

[verified 2026-10-30] S10 implementation commit 729000bd9b639fb19903b9d186d2c5ba4858b2e7 contains
the reviewed 33-file package and was fast-forwarded into main from S9 6565bc4. HEAD/main/
retained S10 branch matched with clean tree/index at that integration snapshot. The later
documentation follow-up advances the tip. Verify actual branch/HEAD/main/origin/main and
ls-remote after publication, and require 729000b to be an ancestor of main. Do not use the
old S9 SHA as the expected current tip. No S11 branch exists.

S10 source/tests/preview/evidence and 17 JPEG screenshots are committed. Session records and
this handoff are included. Preserve them. Source/test/screenshot bytes match the reviewed
package. Fresh publication suite: 316 passed, one existing warning in 62.22 seconds. Ruff
lint/format, offline Node caller, bounded credential/configuration scan and diff checks pass.
The prior 35 independent fault receipts match current source hashes; faults were not rerun.

[verified from retained S10 records] Final full suite 316 passed, one existing Starlette/httpx
warning. Ruff lint/format, offline caller and diff checks passed. Final 35/35 independent faults
were caught with exact restoration. Actual native validation/POST/303, database persistence,
reload and repeat HTTP review preserved time/draft; fake fetch/session/send counts were zero.
Seventeen screenshots retain two initial captures. A read-only auxiliary source/screenshot
review found no unresolved S10 issue; it did not independently run runtime checks. These are
retained S10 results, not fresh S11 checks, clean first-run proof or human usability evidence.
Invalid test-ID/request-count assumptions, patch/lint and leak-label corrections remain recorded.

[verified] The user questioned screenshot formatting and requested the live design. The actual
preview was opened at a normal 620x737 pane; its responsive panels stack and scrollWidth was
620. No source/design change followed that inspection. The later user request authorizes
S10 publication only. It does not grant S11 execution or change an approved design decision.

[verified] /voice, voice.html, test_voice.py and scripts/check_ui.mjs do not exist yet. Existing
S7 buttons/controller and SDK remain in dashboard.html. Source pins Bolna Web Call v3.0.1 at
https://cdn.jsdelivr.net/gh/bolna-ai/web-call@v3.0.1/dist/bolna-web-call.min.js.
POST /web-call/session already uses AdminDep, resolves line/language, rejects an unconfigured
agent with 503 and forwards string user_data to mint_web_call_session. Existing fake tests
cover Guardian/Bait EN/HI and admin protection. That is source/test evidence, not a live SDK check.

Preview trap: preview_ui.py currently substitutes the SDK inside dashboard.html. Its fake SDK
only emits an error on start and call-end on stop. Moving the production controller without
updating that preview owner risks loading the real SDK. The existing fake cannot prove the
new happy/late-event lifecycle until controlled fake events/counters are added.

[verified] Python 3.12.15, uv 0.13.0 and Node v24.21.0 are installed. .env.local exists and
was neither printed nor hashed. S10 publication checks privately re-verified the distinct test
endpoint and test-only connection. This is not an S11 test grant; re-verify before S11 checks.
Integration fixtures migrate/truncate the test branch. TEST_DATABASE_URL alone does not
redirect a normally launched app's DATABASE_URL.

[verified] The inspection preview on 127.0.0.1:8783 is stopped. Session 81053 was unavailable
in the publication chat, so PID 6813's exact command and listener ownership were re-verified
before SIGINT. No listener remained. The first database preflight detected another client
and stopped before a reset. Subsequent read-only inspection and the unchanged preflight found
no other test clients. The full suite then ran under existing S10 isolated-test authority.
Do not stop historical PIDs or restart/reset a preview implicitly. S11 tests/previews require
their named grant and exclusive test-database ownership. No real provider or microphone ran.

[unknown] Live credential validity, wallet/available credit, deployed Render revision,
real audio/SDK connection, Telegram receipt, human comprehension, physical devices, named
assistive technology and CI. Historical caps and source configuration grant no spend.

6. Authority

User, 2026-10-30: "Yes please commit s9 and fast forward to main and push. I give authority for this as well".
The selected annotation was "Explicit S10 implementation/branch authority and named test-database mutation authority."
This covered S9 publication and S10 local/branch plus isolated TEST_DATABASE_URL migrations,
truncation/review fixture writes with fake Bolna/Telegram, never production. It did not grant
S10 publication, S11 or live/provider actions.

User, 2026-10-30: "Okay make the copy paste handoff prompt for slice 11. Rememeber to include the slices and the build plan thanks".
That requested the S11 handoff only.

User, 2026-10-30: "Please commit slice 10 and push to main so that s11 can start cleanly. I authorize".
This authorizes the S10 package commit, main fast-forward and push. Implementation 729000b
is committed and in main. It grants no S11 implementation/required branch or named S11
destructive test-branch checks; those remain pending.
Proposed S11 test scope is migrations/truncation and fixture writes on the freshly verified
TEST_DATABASE_URL branch, with fake Bolna/Telegram and controlled fake browser SDK only,
never production or a real microphone/session. Once granted, that exact scope persists
without step-by-step reconfirmation. Publication, installations, real provider credential use,
paid/live actions, deployment and S12 remain separate named actions.

7. Read first

AGENTS.md including Slice handoff prompts; ~/.agents/skills/software-factory/SKILL.md;
current main-tip 00-status.md and 01-product.md through 04-slices.md, especially the redesign
sections and exact S11 contract. 00-status.md/PROGRESS.md carry S10 integration and publication
checks. The S8 handoff is the structural skeleton; s10-session-transfer.md is historical background.
The visual reference is mockups/redesign/voice.html, illustrative only. Use functional-ui
and frontend-design within the approved design; no repeat gate approval unless a decision changes.

Relevant source under src/scamkaki/: app/main.py, templates/dashboard.html, _reviewer.html,
_theme.html, _error.html and report.html; lib/env.py and integrations/bolna.py. Relevant tests:
tests/integration/test_web_call.py, test_admin_auth.py, test_dashboard.py, test_checks.py,
test_reports.py, test_patterns.py and conftest.py; tests/conftest.py and tests/support/fakes.py.
Preview: scripts/preview_ui.py. Offline caller: scripts/caller/check-live.mjs. Read migrations
for context only. voice.html, test_voice.py and scripts/check_ui.mjs are planned S11 files,
not existing proof. Evidence: evidence/s10-report-review.md and checks/ui-redesign-preview.md.
All these document/evidence/mockup paths are under docs/plans/scamkaki/ unless otherwise stated.

Re-verification commands: git status --short; git diff --cached --name-only;
git branch --show-current; git log -5 --oneline main; git rev-parse HEAD main;
git ls-remote origin refs/heads/main; git merge-base --is-ancestor 729000b main.
Verify committed S10 contents and the final main tip before separately authorized S11 branch creation.
No command may print credential values.

8. Done means

After the prerequisite and explicit S11/test-branch grant exist, the approved Voice room is
reachable, configuration-aware and explicit-start only. Overview no longer owns call controls
or the pinned SDK/controller. Existing EN/HI Guardian/Bait session behavior is preserved.
Literal tests/fake counters prove zero starts/mints on load/selection/navigation, exactly one
on Start, no overlapping attempt, locked selectors, end/hang-up/error recovery and stale-event
isolation. Missing configuration is honest, no-JS is explained, and Voice has no call-time refresh.

At 1280 and 375 px, actual fake-provider browser checks cover the lifecycle, unavailable/error
states, keyboard focus, Hindi labels, selection and measured overflow. Real requests under
fake providers are distinct from simulated events, and both are labeled. Each claimed guard
gets its own mutation, a failing assigned check and exact restoration. Failure receipts retain
short tracebacks and credential redaction. No assertion is weakened or replaced with a source-only proxy.

Focused checks run while building, then the relevant full suite with no installation:
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q --tb=short
node scripts/caller/check-live.mjs
node scripts/check_ui.mjs
git diff --check
The check_ui command applies after the planned script actually exists. Full suite/preview
resets require the named S11 test scope and exclusive database ownership.

evidence/s11-voice-room.md records actual URL/port/stop command, fixture/configuration inputs,
HTTP/auth/cache observations, SDK/fake-provider counters around each action, lifecycle/events,
screenshots, keyboard/overflow, mutations/restores, retained failures and unavailable checks.
00-status.md and PROGRESS.md agree; only status records authority. Architect-reviewer cleanup
stays within S11 and preserves historical/user files. Local fake proof establishes neither
real voice nor usability, S6/S7 closure or deployment. S12 remains a separate slice.
The exact post-S11 closing question is "Continue to slice S12, or re-steer?".

Wait for instructions before taking any action.
```
