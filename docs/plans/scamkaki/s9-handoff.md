# S9 handoff

Prepared 2026-10-30 after S8 publication. Follows the retained S8 skeleton and AGENTS.md's eight-section handoff order. S9 execution/test-branch authority is pending.

```text
You are receiving background for Scamkaki S9 in /Users/jayd0/Desktop/bolna on macOS arm64. Prepared 2026-10-30 (Asia/Singapore) from published main and actual Git/source state.

Skeleton reference: docs/plans/scamkaki/s8-handoff.md supplies the retained eight-section structure, following AGENTS.md's Slice handoff prompts. The earlier Envoi S25/S26 example supplies structure only. Its commits, infrastructure, state and authorizations do not apply to Scamkaki. The historical S8 prompt is not current execution authority.

The gate documents win over this prompt. Re-verify Git and files before acting; stop and ask rather than guess if they conflict. Be brief and honest. No em dashes, invented results, weakened checks or co-author trailers. Visualizations are .html. Never print or hash .env.local or expose secrets. Plan context transfer around 50-70% using transfer-context and the repository's slice-handoff rules.

1. Project in brief

Scamkaki gives Singapore seniors English and Hindi Guardian phone lines to check suspicious contact before moving money, or get urgent guidance after acting. The app evaluates recorded warning signs and alerts family on likely-scam results through Telegram and a private-link page. Ah Ma Bait stalls fictional scam callers, records claimed agency/request/payee details and supplies seven-day script counts; a separate human reviewer reads draft reports.

The senior is the person contacted. The family member receives alerts and calls back. The fictional scammer may impersonate an agency, bank, courier, employer, investment group or relative. The reviewer is separate from the family-link viewer.

Targets from 01-product.md, not achieved real-world results: family alert within 1 minute and callback before money moves; English Guardian at least 7 of 8 scam fixtures flagged and at most 1 of 4 legit fixtures; Hindi Guardian 2 of 2 scams and 0 of 1 legit; both already-acted courier cases urgent with bank guidance; every likely_scam alerts and no other verdict does; English Bait at least 4 of 5 planted payees, Hindi Bait at least 1 of 2; zero leaks. S6 live proof remains incomplete. Fixture targets and local UI checks do not establish real-world effectiveness or human usability.

Hard rules: Bait never speaks an NRIC, OTP, card number, password or real-looking bank/PayNow identifier; she stalls. No agent claims to be a government, police or bank employee. Reports are drafts, always human-reviewed before anything is sent and never automatically filed. Fixtures/test callers/demo data stay labeled on screens, evidence and videos. Seed stories never copy victim identities. Guardian outputs are "likely scam", "unclear, talk to family" or "no scam signs found", never certainty of safety.

[verified 2026-10-30] Gates 1, 2, 3 and 4 are APPROVED 2026-10-30 for the redesign in 00-status.md. They approve the design/plan, not S9 execution or database actions.

2. Where S9 sits

Build order: S1 tracer, S2 Hindi voice, S3 verdict/family alert, S4 Bait extraction/leak guard, S5 sophisticated verdict behind the tool, S6 Guardian conversation/live proof, S7 dashboard/report review/demo, S8 reviewer workspace/records, S9 visual script patterns, S10 focused report review, S11 voice room, S12 family/final website checks.

[verified] S1-S5 are checked done. S6 live proof is open. S7 is built, with backup video/full live demo open. S8 is complete locally and published to main. S9-S12 are approved plans and unstarted. Gate 4 permits offline redesign without waiting for or closing S6/S7 live gaps. S9's S8-in-main prerequisite is now satisfied.

Never cut: S1, S3, S4's leak guard, S5's already-acted/offline fixture check, fixture labels, failed attempts, honest missing fields, independent call/check records, warning/urgent meanings, auth, human review and family isolation. Original cut order: S7 extra polish, S6 Hindi live, then English reduced to four named cases with disclosure. Redesign cuts optional motion, decoration and duplicate copy first. Cutting an approved screen/function requires user re-steering.

S9 makes stored Bait script counts readable and reachable. Counts describe records, not unique scammers, confirmed scams, accuracy or success rates. Differentiation remains a bounded hypothesis.

3. S9 contract

Copied verbatim from published 04-slices.md, "### S9: Visual script patterns":

- **Branch:** `scamkaki/slice-9-script-patterns`; depends on S8 in main.
- **Visible result:** Script patterns shows seven-day Bait groups as labeled bars and expandable
  explanations. Reviewer navigation and Overview links reach the actual page.
- **Builds:** `/patterns`, pattern template and shared diagram styling, reusing
  `scripts_this_week`; no new aggregation store or expanded Bait extraction.
- **Assigned tests:** `test_patterns_show_only_seven_day_bait_groups`; EN/HI aggregation,
  different requests remaining separate, numeric labels/bar scaling, no-data state and database
  failure state; route auth. Verify Overview's summary and Patterns use the same source meaning.
- **Evidence:** `evidence/s9-script-patterns.md`; fixture group inputs/expected counts, screenshots
  and expanded-content walkthrough, route/SQL evidence and affected guard mutation receipts.
- **Falsifiers:** mixing Guardian rows into Bait counts; counting an eight-day script; invented
  scam-network relationships or success percentages; bars contradicting their text labels.
- **Exit decision:** go when count boundaries, labels, links and responsive layout pass; stop
  for S10 authorization. No claim of real scam detection performance.
- **Authorizations to request:** S9 local implementation/branch and named test-branch checks.

Gate 2/3 constraints:
- Keep FastAPI/Jinja/Postgres, existing dependencies, system fonts, HTML/CSS/inline SVG and the approved midnight/ice/electric blue palette with restrained chartreuse. No new framework, chart library, schema or external font.
- GET /patterns uses AdminDep and the shared reviewer shell/theme. Reviewer navigation and an Overview link reach it. Expose only implemented destinations; family keeps FamilyDep and no reviewer navigation.
- Reuse scripts_this_week. Show all seven-day agency/request groups across EN/HI. Same pair combines languages; different requests stay separate. Bars have visible labels and numeric counts; widths are relative to the largest group. No data yields no bars and no division by zero.
- Expanded explanations use recorded agency/demand and existing labels, not generated stories or inferred relationships. The matching diagram explains the system; it does not reconstruct individual conversations or link calls/checks.
- A database read failure is an HTML 503 with local Retry, never a false empty result. Keep no-store and escaped stored content. Reuse S8's reviewer_page/reviewer_error where appropriate; webhook/tool error behavior stays unchanged.
- Overview's summary and Patterns must share the same source meaning. Keep stored facts, failure records, transcript handling, urgent priority and existing report/family behavior intact.

4. Out of scope

S10 owns /reports entry, focused report restyle and review acknowledgment. S11 owns /voice and the SDK/controller move. S12 owns family restyle and stale/empty polling repair. Existing S7 voice controls remain on Overview until S11; do not duplicate or move them in S9.

Protected: agents/, seed fixture meanings/expectations, verdict/extraction/leak/alert/report-draft rules, migrations, CI, manifests/lockfile, retained S6 failed records/audio and historical mockups. No new languages, transfer, embeddings, account/identity matching, scam-network tracking or automatic filing. No production writes, provider/session/call, wallet check, agent change, Telegram message, paid inference, provisioning, installation, cleanup sweep, S6 rerun or S7 completion claim.

5. Current state

[verified 2026-10-30] Publication commit and main: 87739f0716da49641887401071cefae750696c98 (feat: add reviewer workspace and stored record views). Local main, remote refs/heads/main and retained scamkaki/slice-8-reviewer-workspace matched via git ls-remote. Current branch is main. Index was empty and the worktree clean immediately after publication. No S9 branch exists. After explicit S9 authority, create scamkaki/slice-9-script-patterns from the then-current verified main tip, preserving known documentary work.

[verified] This handoff is prepared after the push. Only post-publication documentation is local/uncommitted: PROGRESS.md, docs/plans/scamkaki/00-status.md, s9-handoff.md and s9-handoff-review.md in the gate folder. Preserve it. No S9 application/test/agent/migration/fixture/manifest change was made. A clone of main already has S8; it may lack these later handoff files.

[verified] Fresh pre-publication suite: 290 passed, one existing Starlette/httpx warning. Ruff lint/format, Node offline caller and diff checks passed. S8 retained 37 distinct caught faults across corrections, 23 genuine screenshots and 1280/375 px populated/empty/error/HTTP walkthroughs. The first fault run was 34/35; a sparse draft-queue test was strengthened. A page-2 empty-history bug was reproduced before its fix. These limits remain in evidence/s8-workspace.md; they are not clean first-run or human usability proof.

[verified] Python 3.12.15, uv 0.13.0 and Node v24.21.0 are installed. Existing FastAPI/Jinja/psycopg/pytest/Ruff were used without installation. .env.local exists, never printed or hashed. Four agent exports and migrations 0001-0005 exist.

[verified] /patterns, patterns.html and test_patterns.py do not exist yet. The visual reference mockups/redesign/patterns.html exists and is illustrative only. The current shell exposes Overview/Calls. Overview already reads scripts_this_week; that SQL joins scripts to calls, filters script created_at to the last seven days, groups agency/demand and returns n/languages/last_seen. No S9 behavior test has run.

[verified] scripts/preview_ui.py uses explicit test Settings and fake SDK/Bolna/Telegram; it requires --reset-test-db and refuses a missing/shared production endpoint. The S8 preview on port 8783 was stopped before publication tests; no listener remained. Re-verify PIDs/ports rather than reuse old receipts. Tests and preview resets must run sequentially.

[verified] S8's configured TEST_DATABASE_URL was rechecked as distinct from production and successfully used for the 290-test run. Integration fixtures migrate and truncate that database. TEST_DATABASE_URL alone does not redirect a normally launched app's DATABASE_URL. Current S9 access must be rechecked after named authorization, without displaying credentials.

[unknown] Live provider credential validity, deployed Render revision, real voice behavior, Telegram receipt, human usability, physical phone and named screen-reader results. No live/provider/deployment check was made for publication. A main push may trigger existing Render auto-deployment; its result is unverified.

6. Authority

User, 2026-10-30: "S8 and test-branch authorization are authroized. Go ahead and start implementation and database actions." This covered S8 and its named test branch only.

User, 2026-10-30: "Commit and push to main then make the copy paste prompt for s9(make sure to reference the skeleton prompt)". This authorized the completed S8 publication and this handoff. S8 was committed, fast-forwarded and pushed; its branch is retained. This is not S9 implementation or test-database authority.

S9 local implementation/required branch and named destructive test checks remain pending explicit authorization. Proposed test scope: migrations/truncation on the verified TEST_DATABASE_URL branch with fake Bolna/Telegram, never production. Once that exact scope is granted, retain it without step-by-step reconfirmation. Calls, spending, account changes, installs, commits, integration, push and deployment remain separate.

7. Read first

AGENTS.md, including Slice handoff prompts; ~/.agents/skills/software-factory/SKILL.md; current main-tip 00-status.md and 01-product.md through 04-slices.md, especially their redesign sections and exact S9 contract; PROGRESS.md. Use functional-ui/frontend-design for the approved design; no repeat gate approval unless a decision changes.

Skeleton reference: docs/plans/scamkaki/s8-handoff.md for structure only; its old state is historical. Visual reference: docs/plans/scamkaki/mockups/redesign/patterns.html. Evidence: docs/plans/scamkaki/evidence/s8-workspace.md and checks/ui-redesign-preview.md, keeping application and prototype proof distinct.

Source: src/scamkaki/app/main.py; templates/_reviewer.html, _theme.html, _error.html and dashboard.html; src/scamkaki/domain/store.py and domain/verdict.py for existing labels; scripts/preview_ui.py; tests/integration/test_dashboard.py, test_checks.py, test_reviewer_errors.py and conftest.py; tests/conftest.py and tests/support/fakes.py. Read migrations for context only. scripts/check_ui.mjs is a later planned file, not existing S9 proof.

Re-verification: git status --short; git diff --cached --name-only; git branch --show-current; git log -5 --oneline main; git rev-parse HEAD main; git ls-remote origin refs/heads/main. No command may print credential values.

8. Done means

After explicit S9/test-branch authority, the real /patterns page and Overview/navigation links meet the copied contract, with populated/empty/503 states at 1280 and 375 px. Tests use literal expected fixture counts: EN/HI same-pair aggregation, different requests separate, eight-day exclusion, Guardian data excluded, numeric/bar agreement, zero-safe empty data, auth and read failure. Extend existing reviewer auth/error coverage for /patterns. Hostile stored text must be checked on actual rendered output. Prove each claimed guard with an independent mutation and exact restoration; retain failed attempts.

Run focused checks while building, then the relevant full suite without installing:
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q
node scripts/caller/check-live.mjs
git diff --check

The full suite includes destructive integration checks and needs the named S9 test-branch authority. Preview uses explicit test Settings/fakes and no real microphone/provider session. Record the actual URL/port/stop command, fixture inputs and literal expected counts, HTTP status/cache behavior, Overview-to-Patterns navigation, expanded explanations, keyboard focus, responsive overflow, screenshots, mutations/restores and unavailable checks in evidence/s9-script-patterns.md. Update 00-status.md and operational PROGRESS.md consistently; only status records authority.

Run architect-reviewer post-slice cleanup within S9 scope, preserving historical/user files. Human comprehension, real devices/assistive technology, live calls, Telegram receipt, CI and deployment stay unverified unless actually checked under appropriate authority. Stop before S10; the exact closing question is "Continue to slice S10, or re-steer?"

Wait for explicit S9 implementation and named test-branch authorization before any S9 branch/code/database action. Wait for instructions before taking any action.
```
