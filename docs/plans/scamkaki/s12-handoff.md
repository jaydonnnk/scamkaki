# S12 handoff

Historical S12 boundary snapshot. The later publication/S6 request is recorded in
00-status.md. The body is retained as evidence and does not override current authority.

Prepared 2026-10-30, Asia/Singapore. S11 is published; S12 execution/test authority is pending.
Original eight-section structure, all S1-S12 slices and conditional build plan.

```text
You are receiving background for Scamkaki S12 in /Users/jayd0/Desktop/bolna on macOS arm64.
Prepared 2026-10-30, Asia/Singapore, from published main and actual Git/source state.
This is background only. S11 is published; S12 execution and named test authority are pending.

Skeleton: docs/plans/scamkaki/s8-handoff.md and AGENTS.md's eight-section Slice handoff prompts.
Historical prompts supply structure/context, not authority. Gate documents win.
Re-verify Git and files before acting; stop and ask rather than guess on conflict.
No invented results, weakened checks, em dashes or co-author trailers. Visualizations are .html.
Never print/hash .env.local or expose credentials. Use transfer-context and repository handoff
rules around 50-70% of context. No S12 branch or application edit follows from this prompt alone.

1. Project in brief

Scamkaki gives Singapore seniors English and Hindi Guardian phone lines to check suspicious
contact before moving money, or get urgent guidance after acting. Likely-scam results alert
family through Telegram and a private-link page. Ah Ma Bait stalls fictional scam callers,
records claimed agency/request/payee details and supplies seven-day script counts. A separate
human reviewer reads draft reports.

The senior is the contact recipient. Family receives alerts and calls back. The fictional
scammer may impersonate an agency, bank, courier, employer, investment group or relative.
The report reviewer is separate from the family-link viewer.

Targets from 01-product.md, not achieved real-world outcomes:
- Family alert within 1 minute and callback before money moves.
- EN Guardian: at least 7 of 8 scam fixtures flagged, at most 1 of 4 legit.
- HI Guardian: 2 of 2 scams flagged, 0 of 1 legit.
- Both already-acted courier cases receive urgent alerts and bank guidance.
- Every likely_scam alerts and no other verdict does.
- EN Bait captures at least 4 of 5 planted payees; HI Bait at least 1 of 2. Zero leaks.
S6 live proof remains incomplete. Fixture/browser checks prove neither real-scam efficacy nor
human comprehension. S12 must freshly verify this UI target: from Overview, reach an urgent
Guardian check, report draft or call detail in at most two navigation actions. Earlier local
checks do not replace that full walkthrough or establish human usability.

Hard rules: Bait never speaks an NRIC, OTP, card number, password or real-looking bank/PayNow
identifier; she stalls. No agent claims to be a government, police or bank employee. Reports
remain drafts, human-reviewed before sending and never automatically filed. Fixtures/test
callers/demo data stay labeled. Seed stories never copy victim identities. Guardian outputs
are "likely scam", "unclear, talk to family" or "no scam signs found", never certainty of safety.

[verified 2026-10-30] Redesign Gates 1, 2, 3 and 4 remain APPROVED 2026-10-30 in 00-status.md.
They select the plan, not S12 execution, database actions, publication or provider validation.

2. Where S12 sits, all slices and build plan

Approved sequence and current status:
- S1: Guardian tracer, webhook/tool/dashboard end to end. Checked done.
- S2: Hindi voice and per-language agent mapping. Checked done; recorded limits retained.
- S3: Guardian verdict and Telegram/private-link family alert. Checked done; sent is not receipt.
- S4: Bait extraction, leak guard, stored scripts and draft reports. Checked done; HI flaky result retained.
- S5: Sophisticated verdict, warning signs and already-acted guidance. Checked done.
- S6: Guardian conversation/live validation of five values. Offline repairs built; live proof
  incomplete. Failed probes/audio and Hindi listener gap remain evidence.
- S7: Dashboard, report review and demo. Built/published; backup video/full live demo open.
- S8: Reviewer workspace, Overview, Calls and independent call/check details. Published in main.
- S9: Seven-day Bait script patterns and matching explanation. Published in main.
- S10: Focused Reports review, persistent first time and original draft. Published in main.
- S11: Explicit-start Voice room and lifecycle using existing SDK/session contract. Published
  in main at b6620b1. Local fake lifecycle proved; real audio/SDK connection remains unverified.
- S12: Standalone Family restyle, stale/empty polling repair and all-eight-screen verification.
  Approved plan, unstarted. There is no S13 plan.

Gate 4 allows S8 -> S9 -> S10 -> S11 -> S12 on existing S7 code without closing S6/S7 gaps.
S12 is the final redesign slice. It completes the Family surface and checks the existing
screens together. It does not repair the voice agents or prove real-world effectiveness.
Its S8-S11-in-main prerequisite is MET at b6620b1990e58baebdc9d34991d0adf73a7624bd.
No new S11 publication prerequisite remains. S12 local/test grants remain pending.

Build plan, only after explicit S12 local/test grants:
A. Verify published S8-S11, current main, dirty documentary inventory and authority. Create
   scamkaki/slice-12-family-ui from that main tip. Preserve inherited docs. Establish the
   baseline with fake providers after private test-endpoint/exclusive-ownership checks.
B. Add failing Family route/header/guard checks and actual-script controller cases for initial
   empty/populated, populated -> failed refresh -> recovery, populated -> successful empty,
   new alert, hostile text, missing fields, sound opt-in and reduced-motion/bounded flashing.
C. Restyle family.html as the approved standalone Family experience, with urgent next steps,
   expandable recorded reasons and earlier alerts. Preserve URLs, relevant IDs, labels and
   guidance. No reviewer shell, reviewer navigation or private-link shortcut from Overview.
D. Repair the owning poll/render state narrowly. Failure retains the previous alert with
   an explicit stale/error marker. Successful empty clears stale latest/earlier alert content
   and shows No alerts yet. Retain five-second polling, first-load/new-alert distinction,
   opt-in sound, bounded flashing, reduced motion and honest sent/receipt meaning.
E. Extend scripts/check_ui.mjs to exercise actual Family logic with controlled label maps,
   fake clock/fetch/audio and literal expected results. Preserve all 19 existing Voice/Overview
   checks. Extend the synthetic preview for controlled poll transitions while retaining the
   fail-closed Voice fake SDK replacement. No real microphone/provider/session or Telegram send.
F. At 1280/375 px, walk Overview, Calls, Call detail, Guardian check, Script patterns, Reports,
   Voice and Family. Cover all verdicts on reviewer screens; Family remains likely-scam only.
   Verify urgent/non-urgent, Hindi, empty/missing/error, keyboard/focus, overflow, query/paging,
   source/report links and the three at-most-two-action Overview tasks. Family uses its separate
   fake private URL. Voice Starts use only the fake SDK/provider, with zero implicit effects.
G. Independently mutate each claimed new/affected guard, retain intended failing checks and
   restore exact bytes. Run full relevant checks, record evidence/status/progress and scoped
   architect-reviewer cleanup. Report the redesign result and remaining limits, then stop.

Never cut S1, S3, S4's leak guard, S5's already-acted/offline fixture checks, fixture labels,
failed attempts, honest missing fields, independent call/check records, warning/urgent meanings,
auth, human review or family isolation. Original cut order: S7 extra polish, S6 Hindi live,
then English reduced to four named cases with disclosure. Redesign cuts motion, decoration and
duplicate copy first. Cutting an approved screen/function requires user re-steering.

3. S12 contract

Copied verbatim from published 04-slices.md, "### S12: Family view and completed website flow":

- **Branch:** `scamkaki/slice-12-family-ui`; depends on S8-S11 in main.
- **Visible result:** Family gets concise urgent guidance, expandable reasons and earlier
  alerts through the existing private link. All eight screen types work together with real
  stored fixture data, safe fake providers and the approved responsive design.
- **Builds:** standalone family restyle, safe renderer/state feedback and stale/empty handling.
  Retain five-second poll, 24-hour urgent-first order, opt-in sound, reduced-motion flashing,
  secret-link checks and response headers. No reviewer access or navigation is granted to family.
- **Assigned tests:** family link/list/order/header tests; offline renderer safe text, empty,
  stale/error and new-alert transitions. Browser walkthrough all eight screens, each verdict,
  urgent/non-urgent, Hindi, empty/error, keyboard focus, responsive overflow and query navigation.
  Verify the three Gate 1 tasks take at most two navigation actions from Overview.
- **Evidence:** `evidence/s12-family-ui.md`; genuine browser screenshots and request log against
  local synthetic fixtures, complete task walkthrough, full relevant suite and guard receipts.
  Record missing tooling or named assistive-technology/human checks as unavailable, never passed.
- **Falsifiers:** wrong/private link exposed; family sees non-likely-scam records; changed 24-hour
  ordering; a successful empty response leaves an old alert; failure masks stale data as fresh;
  user text becomes HTML; lost opt-in sound or reduced-motion behavior; broken path to any screen.
- **Exit decision:** redesign go only when its assigned tests and full fake-provider walkthrough
  pass. Human comprehension and S6 live efficacy remain distinct. This does not close S7's
  unrecorded backup video or unrun live demo.
- **Authorizations to request:** S12 local implementation/branch and named test-branch checks.
  Any user walkthrough, real-device/screen-reader check or recording is evidence only if performed.
  No recording install, outreach, commit, deployment or live call is implied.

Gate 2/3 constraints: keep FastAPI/Jinja/Postgres, current dependencies, system fonts and
HTML/CSS/inline SVG. Retain midnight/ice/electric blue and restrained chartreuse for fixtures,
never safe status. No framework, schema, library, external font or new notification mechanism.
Family keeps FamilyDep and existing paths/headers; reviewer routes keep AdminDep. Poll only
the existing Family JSON endpoint. Safe DOM/text nodes remain mandatory. No-JS explains that
alerts cannot refresh. Do not infer call/check linkage or reinterpret counts and timestamps.

4. Out of scope

S8-S11 behavior is preserved during the full walkthrough: independent records, failed/missing
fields, seven-day Bait counts, original draft/first-review time/idempotency/no-send, source
links, session contract, configuration handling and Voice explicit-start/late-event guards.
No duplicate SDK/controller or call controls on Overview. No real SDK/provider/audio validation.

Protected: agents/, seed meanings/expectations, verdict/extraction/leak/alert/report-draft rules,
migrations, CI, manifests/lockfile, failed S6 records/audio and historical mockups/evidence.
No agent/model/price/prompt/tool/transcript change, new language, transfer, embeddings, filing,
identity matching, scam-network tracking or broad cleanup. Preserve existing guidance exactly.
No production write, wallet read, agent update, real call/microphone/provider session, Telegram
message, spend, provisioning, installation, S6 rerun or S7 completion claim. Git publication,
deployment and any human/device/assistive-technology/recording work remain separately scoped.

5. Current state

[verified 2026-10-30] Current branch main. HEAD, main, origin/main, remote refs/heads/main and
retained scamkaki/slice-11-voice-room match b6620b1990e58baebdc9d34991d0adf73a7624bd. Publication
was fast-forward-only; remote equality and 0/0 left/right counts were verified. Tree/index
were clean immediately after the push. No scamkaki/slice-12-family-ui branch exists.

This handoff then adds local documentation only: 00-status.md and PROGRESS.md updates,
s12-handoff.md and s12-handoff-review.md. These four documentary changes are uncommitted;
application/test/screenshot bytes match published main. Preserve them when S12 is authorized.
The published main contains S8-S11; S12 application work has not begun.

[verified] Fresh S11 publication suite: 331 passed, one existing Starlette/httpx warning in
71.45 seconds; Ruff lint/format, 19 actual-script UI checks, offline caller and diff passed.
Retained S11 evidence has 30/30 independent faults caught/restored, seven actual HTTP requests
to fake session minting, zero mic/fetch/send effects and 17 genuine JPEGs. Connected/end/error
callbacks were simulated. These are S11 local facts, not S12 checks or real audio evidence.

The initial fake-credential URL caused a browser fetch rejection before an HTTP request;
normal authenticated URL fixed setup without source changes. Several full-page phone captures
show fixed Skip-link overlays/clipping, with exact cause unestablished. A single offscreen
DOM read does not prove normal-viewport placement for all images. Original failures/captures
remain. The auxiliary review found no blocking source issue; its P3 disclosure correction
was recorded. Its 19 Node/10 database-free checks are auxiliary evidence, not human acceptance.

[verified source, not a new runtime probe] Existing Family already uses createElement,
textContent and replaceChildren for recorded values. Do not replace it with innerHTML.
The current check() renders latest only when alerts.length is nonzero, so an empty success
has no branch clearing the old latest alert. Its error catch reports reachability failure
but does not explicitly label retained content stale. S12 owns these gaps. First check runs
on load and setInterval(check, 5000) polls. flashUntil is set to Date.now() + 30000 for new
alerts; bounded flashing and reduced motion must hold through empty/failure transitions too.
Sound remains opt-in via sound; latest, earlier and status are existing DOM IDs.

Family page retains no-store/no-referrer/noindex; polling JSON retains no-store. Wrong/unset
private link stays 404. The JSON
query returns likely_scam only, at most 20 rows, recent harmful-acted alerts first for 24 hours,
then created_at/id descending. Older urgent records retain urgent meaning but lose priority.
Family's inline JS embeds Jinja label dictionaries. The offline harness currently runs Voice/
Overview only; Family cases must exercise correctly rendered logic, not a copied renderer.
The illustrative mockup is not runtime, polling, sound or persistence proof.

Safe preview already replaces the SDK in voice.html, validates the anchor before resets,
and loads tests/support/voice-preview.html. Preserve that owner/guard and test loader cleanup.
No real external SDK fallback is allowed in the fake walkthrough. TEST_DATABASE_URL alone
does not redirect a normally launched app's DATABASE_URL. Integration fixtures migrate/truncate;
previews/tests/reset modes require exclusive sequential ownership of the same test branch.

[verified] Python 3.12.15, uv 0.13.0 and Node v24.21.0 exist. .env.local exists and was neither
printed nor hashed. S11 publication privately checked a distinct test endpoint and connection;
its first ownership preflight refused another client, later read-only inspection showed none.
No client was terminated. Fresh S12 admission is unchecked and its destructive scope pending.
No listeners remain on 8783/8784; owned S11 previews are stopped, tab closed, viewport reset.
Historical PIDs are not current stop targets. No DB/provider action prepared this S12 handoff.

[unknown] Real provider credential validity, account credit, deployed Render revision after
push, real audio/SDK connection, Telegram receipt, human comprehension, physical devices,
named assistive technology and CI. Historical caps/configuration grant no spend.

6. Authority

User, 2026-10-30: "Please start s11" and selected "Authorize this isolated S11 test scope".
That covered S11 local implementation/branch and verified TEST_DATABASE_URL migrations,
truncation/fixture writes, fake Bolna/Telegram and controlled fake browser SDK only.
It does not extend to S12.

User, 2026-10-30: "Commit and push to main, then the copy paste prompt for s12. PLease follow the structure of the original prompt i gave u to craft the handoff propmt."
This authorized S11 publication and this documentary S12 handoff only. S11 publication is
complete at b6620b1990e58baebdc9d34991d0adf73a7624bd. Pending: S12 local implementation/required
branch and named destructive test-branch checks. No application edit follows from this prompt.

Proposed S12 test scope: migrations/truncation and fixture writes on freshly verified distinct
TEST_DATABASE_URL, fake Bolna/Telegram, controlled Family poll responses and fake browser SDK
only, never production, real microphone/provider sessions or messages. Once granted, that
exact scope persists without step-by-step reconfirmation. Installation, live/paid work,
recording, Git publication and deployment stay separate named actions.

7. Read first

AGENTS.md including Slice handoff prompts; ~/.agents/skills/software-factory/SKILL.md;
current main-tip 00-status.md and 01-product.md through 04-slices.md, especially redesign
sections and exact S12 contract. Use s8-handoff.md as the skeleton. S11 session transfer/review
are labeled historical local-exit context. Visual reference: mockups/redesign/family.html.
Use functional-ui/frontend-design within the approved direction; no repeat gate approval
unless an approved decision changes.

Source: src/scamkaki/app/main.py; app/templates/family.html, _theme.html, _reviewer.html,
dashboard.html, calls.html, call.html, check.html, patterns.html, report.html and voice.html;
domain/store.py recent_alerts; app/presentation.py; lib/env.py. Template/domain paths in this
sentence are under src/scamkaki/. Tests: tests/integration/test_family.py, test_voice.py,
test_admin_auth.py, test_dashboard.py, test_calls.py, test_checks.py, test_patterns.py,
test_reports.py, test_reviewer_errors.py and conftest.py; tests/conftest.py and tests/support/fakes.py.
Preview/checks: scripts/preview_ui.py, scripts/check_ui.mjs, tests/support/voice-preview.html,
scripts/caller/check-live.mjs. Read migrations for context only.
Evidence: evidence/s11-voice-room.md and checks/ui-redesign-preview.md. Planned S12 evidence
is evidence/s12-family-ui.md; it does not exist yet. Gate/evidence/mockup/handoff paths above
are under docs/plans/scamkaki/ unless stated otherwise.

Re-verification:
git status --short
git diff --cached --name-only
git branch --show-current
git log -5 --oneline main
git rev-parse HEAD main
git ls-remote origin refs/heads/main
git merge-base --is-ancestor b6620b1990e58baebdc9d34991d0adf73a7624bd main
No command may print credential values. A different ref/state requires reconciliation, not
assuming this snapshot still holds or discarding inherited work.

8. Done means

After explicit S12/local test authority, Family has the approved private standalone design,
accurate urgent steps/reasons/history, safe stale/empty/new-alert behavior and preserved sound,
reduced motion, five-second polling, 24-hour priority and access/headers. Literal checks prove
populated -> failure retains visibly stale data; later success recovers; successful empty
removes old alert content; hostile text cannot become HTML; new-alert effects follow opt-in.

At 1280/375 px, actual fake-provider browser checks cover all eight screen types, their
appropriate populated/empty/missing/error states, all verdicts, urgent/non-urgent, Hindi,
keyboard/focus, overflow, query/paging and protected review/Voice behavior. The three Gate 1
Overview tasks take at most two navigation actions, with explicit recorded paths. Family
private access stays separate. Actual HTTP requests are distinguished from simulated events.
Genuine normal-viewport captures are preferred where full-page captures introduce artifacts;
retain failed captures and describe limits rather than infer passing layout from them.

Every claimed guard gets an independent mutation, intended failing assigned check and exact
restoration. Retain short redacted failure logs. Focused checks while building, then full
relevant checks with existing dependencies:
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q --tb=short
node scripts/caller/check-live.mjs
node scripts/check_ui.mjs
git diff --check
Full suite and preview resets require the named S12 test grant and exclusive test ownership.

Record evidence/s12-family-ui.md with actual URL/port/stop command, fixture/configuration,
HTTP/access/headers, poll transitions, fake effect counters, screenshots, keyboard/overflow,
three task paths, guard failures/restores, retained failures and unavailable checks. Status
and PROGRESS agree; only status records authority. Use architect-reviewer for scoped cleanup,
preserving historical/user work. Fixture proof does not establish real efficacy, audio,
human comprehension or deployment; it does not close S6/S7.

After S12, report the redesign result and remaining evidence limits, then stop for the user's
next instruction. There is no S13 plan; do not invent a next-slice question or start more work.
Wait for instructions before taking any action.
```
