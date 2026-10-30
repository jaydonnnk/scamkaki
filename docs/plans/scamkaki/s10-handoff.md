# S10 handoff

Historical preparation snapshot. Later S9 publication and S10 local/test authority are recorded
in [00-status.md](00-status.md). Re-verify current Git prerequisites before execution.

Prepared 2026-10-30, Asia/Singapore. S9 is complete locally but remains uncommitted and absent
from main. The S10 prerequisite and execution authority are pending. This is background only.

```text
You are receiving background for Scamkaki S10 in /Users/jayd0/Desktop/bolna on macOS arm64.
Prepared 2026-10-30 (Asia/Singapore) from published main and actual Git/source state.

Skeleton reference: docs/plans/scamkaki/s8-handoff.md supplies the retained eight-section
structure, following AGENTS.md's Slice handoff prompts. The original S9 prompt supplied in
this chat uses the same structure. The Envoi S25/S26 example supplies structure only; its
commits, infrastructure, state and authorizations do not apply. Historical S8/S9 prompts
are not S10 execution authority.

The gate documents win over this prompt. Re-verify Git and files before acting; stop and
ask rather than guess if they conflict. Be brief and honest. No em dashes, invented results,
weakened checks or co-author trailers. Visualizations are .html. Never print or hash
.env.local or expose secrets. Use short pytest tracebacks and redact credential values from
failure receipts. Plan context transfer around 50-70% using transfer-context and the
repository's slice-handoff rules.

1. Project in brief

Scamkaki gives Singapore seniors English and Hindi Guardian phone lines to check suspicious
contact before moving money, or get urgent guidance after acting. The app evaluates recorded
warning signs and alerts family on likely-scam results through Telegram and a private-link
page. Ah Ma Bait stalls fictional scam callers, records claimed agency/request/payee details
and supplies seven-day script counts; a separate human reviewer reads draft reports.

The senior is the person contacted. Family receives alerts and calls back. The fictional
scammer may impersonate an agency, bank, courier, employer, investment group or relative.
The reviewer is separate from the family-link viewer.

Targets from 01-product.md, not achieved real-world results: family alert within 1 minute
and callback before money moves; EN Guardian at least 7 of 8 scam fixtures flagged and at most
1 of 4 legit; HI Guardian 2 of 2 scams and 0 of 1 legit; both already-acted courier cases urgent
with bank guidance; every likely_scam alerts and no other verdict does; EN Bait at least 4 of
5 planted payees, HI Bait at least 1 of 2; zero leaks. S6 live proof remains incomplete.
Fixture targets and local UI checks do not establish effectiveness or human usability.

Hard rules: Bait never speaks an NRIC, OTP, card number, password or real-looking bank/PayNow
identifier; she stalls. No agent claims to be a government, police or bank employee. Reports
are drafts, always human-reviewed before anything is sent and never automatically filed.
Fixtures/test callers/demo data stay labeled on screens, evidence and videos. Seed stories
never copy victim identities. Guardian outputs are "likely scam", "unclear, talk to family"
or "no scam signs found", never certainty of safety.

[verified 2026-10-30] Gates 1, 2, 3 and 4 remain APPROVED 2026-10-30 for the redesign in
00-status.md. They approve the design/plan, not S10 execution, publication or database actions.

2. Where S10 sits

Build order: S1 tracer, S2 Hindi voice, S3 verdict/family alert, S4 Bait extraction/leak guard,
S5 sophisticated verdict behind the tool, S6 Guardian conversation/live proof, S7 dashboard/
report review/demo, S8 reviewer workspace/records, S9 visual script patterns, S10 focused
report review, S11 voice room, S12 family/final website checks.

[verified] S1-S5 are checked done. S6 live proof is open. S7 is built, with backup video/full
live demo open. S8 is published to main. S9 is complete locally, with a go decision, but is
uncommitted and absent from main. S10-S12 are approved plans and unstarted. Gate 4 permits
the local redesign without closing S6/S7 gaps.

S10 requires S8/S9 in main. That prerequisite is currently NOT MET. S9 needs a separately
authorized commit and fast-forward into main before the S10 branch is created. Push is a
separate action and is not itself the S10 prerequisite.
Do not silently stack on S9, branch from main without S9, discard dirty work or publish it.

Never cut: S1, S3, S4's leak guard, S5's already-acted/offline fixture check, fixture labels,
failed attempts, honest missing fields, independent call/check records, warning/urgent
meanings, auth, human review and family isolation. Original cut order: S7 extra polish,
S6 Hindi live, then English reduced to four named cases with disclosure. Redesign cuts
optional motion, decoration and duplicate copy first. Cutting an approved screen/function
requires user re-steering.

S10 makes the existing human review step reachable and focused. Reviewed means a person
read the draft. It does not mean the allegation was confirmed, guidance was validated,
a report was filed or a recipient received anything. Differentiation remains a hypothesis.

3. S10 contract

Copied verbatim from published 04-slices.md, "### S10: Focused report review":

- **Branch:** `scamkaki/slice-10-report-review`; depends on S8/S9 in main.
- **Visible result:** Reports navigation opens the newest draft or the latest reviewed report,
  or explains that there are no reports. Each real report uses the approved focused layout.
  Review is acknowledged in the browser and persists across reload without sending anything.
- **Builds:** `/reports` entry, report template restyle and native required checkbox; existing
  report GET/POST routes and review SQL reused. Preserve all reports' access through Overview
  activity and Bait call detail; show review timestamp/status distinctly from original draft text.
- **Assigned tests:** report-entry draft/reviewed/empty and auth cases; all existing report guard,
  first-review timestamp, redelivery, escaping, leak-label and no-send assertions. Browser test
  required checkbox, real POST/303, reload and repeat review with fake providers only.
- **Evidence:** `evidence/s10-report-review.md`; before/after database review state on test branch,
  real request/redirect evidence, screenshots, zero fake provider effects and guard mutations.
- **Falsifiers:** reviewed state disappears on reload; a second review changes its timestamp;
  redelivery rewrites the reviewed draft; any provider call/send; hiding leak findings; review
  styled as filed or delivered. Checkbox is UI acknowledgment, not a new server guard claim.
- **Exit decision:** go when persistent review and existing protections hold; stop for S11.
- **Authorizations to request:** S10 local implementation/branch and named test-branch checks.

Gate 2/3 constraints:
- Keep FastAPI/Jinja/Postgres, existing dependencies, system fonts, HTML/CSS/inline SVG and
  the approved midnight/ice/electric blue palette with restrained chartreuse for fixtures
  and emphasis, never a claim of safety. No new framework, schema, library or external font.
- GET /reports uses AdminDep and returns 303 to the newest draft, else the newest reviewed
  row, or an empty Reports view. Reuse recent_reports and its approved draft-first,
  created_at DESC/id DESC ordering. This is one focused Reports screen, not a report list.
- Existing /reports/{report_id} and POST /reports/{report_id}/review URLs remain compatible.
  Use the reviewer shell/theme and real source call_id. Keep Overview activity/draft links
  and Bait call-detail report links; opening one newest report must not hide the others.
- The native required checkbox is a browser acknowledgment. It adds no server confirmation
  field or new security claim. The existing POST keeps admin/origin checks and its 303.
  First review time and the reviewed draft survive repeat review and webhook redelivery.
- Show review status/time separately from original draft text. Preserve fixture/no-fixture
  labels, leak findings, extracted facts and honest missing values. Escape stored content.
- Missing reports remain 404. Reviewer read failure is HTML 503 with local Retry, never
  false empty. Keep reviewer reads non-cacheable. Reuse reviewer_page/reviewer_error where
  appropriate; do not change webhook/tool or unrelated write-error behavior.
- Navigation exposes only implemented destinations. S10 adds Reports; Voice waits for S11.
  Family retains FamilyDep and no reviewer navigation.

4. Out of scope

S11 owns /voice and the SDK/controller move. Existing S7 voice controls remain on Overview;
do not duplicate or move them in S10. S12 owns family restyling and stale/empty polling repair.
Preserve S8 independent call/check records and S9's shared seven-day Bait count meaning.

Protected: agents/, seed meanings/expectations, verdict/extraction/leak/alert/report-draft
rules, migrations, CI, manifests/lockfile, failed S6 records/audio and historical mockups.
No new report-list screen, report editor, regeneration, filing integration, languages,
transfer, embeddings, identity matching or scam-network tracking. No production writes,
provider/session/call, wallet check, agent update, Telegram message, paid inference,
provisioning, installation, cleanup sweep, S6 rerun or S7 completion claim.

5. Current state

[verified 2026-10-30] Current branch: scamkaki/slice-9-script-patterns. HEAD, local main and
remote refs/heads/main match 87739f0716da49641887401071cefae750696c98, the published S8 commit.
Index is empty. No S10 branch exists. S9 source/tests/screenshots/evidence and documentary
work are dirty on S9; preserve them. A clone of current main has S8 but not S9.

The S9 package changes main.py, store.py's weekly Bait filter, reviewer shell/theme/dashboard,
preview_ui.py and auth/error tests. New files include patterns.html, _matching.html,
test_patterns.py, evidence/s9-script-patterns.md, 13 screenshots and S9 transfer/review docs.
Earlier PROGRESS/status and s9-handoff/review documents are retained documentary work.
S10 handoff preparation adds documentation only. Nothing here is a publication instruction.

[verified] Retained S9 final suite: 303 passed, one existing Starlette/httpx warning. Ruff
lint/format, Node offline caller and diff checks passed. Final 26/26 faults were caught with
exact source restoration; 13 genuine screenshots include two initial captures with disclosed
limits. The initial fault run was 24/24. An Overview unknown-label regression failed before
its fix; the first diagram was cramped, and one scrolled capture showed an off-viewport
skip-link artifact. Control+Home was unavailable. Verbose failure-log URL representations
were redacted; the final runner uses short tracebacks/redaction. These are retained S9
results, not fresh S10 checks, clean first-run proof or human usability results.

[verified] /reports entry does not exist yet. report.html remains the legacy focused draft
page. Its form currently posts Mark reviewed directly and has no acknowledgment checkbox.
The existing report GET uses AdminDep, get_report and reviewer error/no-store helpers.
The existing review POST checks admin and Origin, marks reviewed and redirects 303. It sends
nothing. add_report preserves reviewed draft text on redelivery; mark_reviewed changes only
draft rows, preserving the first timestamp. recent_reports already supports drafts_only=False
and a bounded limit with draft-first/created_at/id ordering. The shell exposes Overview,
Calls and Script patterns. No S10 behavior or browser review-acknowledgment test has run.

[verified] Python 3.12.15, uv 0.13.0 and Node v24.21.0 are installed. Existing libraries were
used without installation. .env.local exists and must never be printed or hashed. During
S9, TEST_DATABASE_URL was privately verified as a distinct endpoint and used successfully.
Fresh S10 access remains unchecked and requires its own named authorization before mutation.
Integration fixtures migrate/truncate the test database. TEST_DATABASE_URL alone does not
redirect a normal app's DATABASE_URL.

[verified] preview_ui.py requires --reset-test-db, explicit test Settings and fake providers,
rejecting a missing/shared production endpoint. The S9 preview on 127.0.0.1:8783 was stopped;
no listener remained on fresh handoff inspection. Old PID receipts are historical. Tests
and preview resets run sequentially. S10 browser proof must observe actual test-database
review persistence and fake-provider counters around the review actions.

[unknown] Live credential validity, deployed Render revision, real voice, Telegram receipt,
human comprehension, physical devices, named assistive technology and CI. No provider,
database or deployment check was performed to prepare this handoff.

6. Authority

User, 2026-10-30: "please start", after the S9 background and the response awaiting S9
implementation and named test-branch authorization. This covered S9 local implementation,
its required branch and the described isolated TEST_DATABASE_URL migrations/truncation with
fake Bolna/Telegram. It did not authorize S9 publication or S10.

User, 2026-10-30: "REferencing the orginal prompt i gave u, make one for s10 thanks".
This requests an S10 handoff only. S9 commit/main integration/push remain unauthorized.
S10 local implementation/required branch and named destructive test checks remain pending.
Proposed S10 test scope: migrations/truncation/review fixture writes on the freshly verified
TEST_DATABASE_URL branch with fake Bolna/Telegram, never production. Once that scope is
granted and the main prerequisite is satisfied, retain it without step-by-step reconfirmation.
Calls, spending, account changes, installs, commits, integration, push and deployment remain
separate named actions. Preparing or reviewing this prompt grants none of them.

7. Read first

AGENTS.md, including Slice handoff prompts; ~/.agents/skills/software-factory/SKILL.md;
current main-tip 00-status.md and 01-product.md through 04-slices.md, especially the redesign
sections and exact S10 contract; current working status and PROGRESS.md for uncommitted S9.
Use functional-ui/frontend-design for the approved design; no repeat gate approval unless
a decision changes.

Skeleton: docs/plans/scamkaki/s8-handoff.md, structure only. Current background:
docs/plans/scamkaki/s9-session-transfer.md. Visual reference:
docs/plans/scamkaki/mockups/redesign/reports.html, illustrative only. Evidence:
docs/plans/scamkaki/evidence/s9-script-patterns.md and evidence/s8-workspace.md. Retain the
distinction between mockup, application, local browser and live-provider proof.

Source: src/scamkaki/app/main.py; templates/report.html, _reviewer.html, _theme.html,
_error.html, dashboard.html and call.html under src/scamkaki/app/; domain/store.py and
domain/reports.py under src/scamkaki/; scripts/preview_ui.py; tests/integration/test_reports.py,
test_dashboard.py, test_calls.py, test_reviewer_errors.py and conftest.py; tests/conftest.py
and tests/support/fakes.py. Read migrations for context only. scripts/check_ui.mjs remains
a planned later file, not existing S10 proof.

Re-verification: git status --short; git diff --cached --name-only; git branch --show-current;
git log -5 --oneline main; git rev-parse HEAD main; git ls-remote origin refs/heads/main.
After separately authorized S9 commit/main integration, verify its committed contents and the new main
tip before creating scamkaki/slice-10-report-review from that verified tip. No command may
print credential values.

8. Done means

After S9 reaches main and explicit S10/test-branch authority exists, Reports entry/navigation
and focused detail meet the copied contract. Literal fixture assertions cover draft priority
over newer reviewed rows, reviewed fallback, empty state and stable ties. Preserve every
existing auth/origin, first-review time, redelivery, escaping, leak-label and no-send check.
Extend reviewer error/auth coverage for /reports. No existing assertion is weakened.

At 1280 and 375 px, exercise draft, reviewed, empty, missing and unavailable states. The
unchecked native acknowledgment blocks browser submission; checking it permits the actual
POST/303. Database status/time persist on reload, repeat review preserves the first time,
and no fake provider fetch/session/send occurs because of viewing/reviewing. Preserve other
reports' access and the actual stored source-call link. Check hostile stored text on rendered
output, keyboard focus and overflow. Prove each claimed affected guard with an independent
mutation and exact restoration; retain failures with credentials redacted.

Run focused checks while building, then the relevant full suite without installing:
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q --tb=short
node scripts/caller/check-live.mjs
git diff --check
Short tracebacks change presentation only, not assertions or test selection. The full suite
and preview resets require the named S10 test-branch scope. No real microphone/provider session.

Record actual URL/port/stop command, fixture inputs, entry targets, review database state
before/after, real requests/redirects/reloads, provider counters, HTTP/cache behavior,
screenshots, keyboard/overflow, mutations/restores and unavailable checks in
evidence/s10-report-review.md. Update 00-status.md and PROGRESS.md consistently; only status
records authority. Run architect-reviewer post-slice cleanup within S10 scope, preserving
historical/user files. Human usability, devices/assistive technology, calls, Telegram receipt,
CI and deployment remain unverified unless actually checked under appropriate authority.
Stop before S11. The exact closing question is "Continue to slice S11, or re-steer?".

Wait for the unmet S9-in-main prerequisite and explicit S10 implementation and named
test-branch authorization before any S10 branch/code/database action.
Wait for instructions before taking any action.
```
