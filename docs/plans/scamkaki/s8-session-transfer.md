# S8 session transfer

2026-10-30, Asia/Singapore. Historical local-exit snapshot before publication authority.
The user subsequently authorized publishing this S8 package and preparing an S9 prompt.
Resolve current refs from Git and authority from 00-status.md; the blocks below retain the
pre-publication state. The earlier s8-handoff.md is also historical.

## Prompt for a new chat

```text
Background for Scamkaki S8 in /Users/jayd0/Desktop/bolna on macOS arm64.
This background is subordinate to the current gate documents. Git/files require re-verification
before action; any conflict requires an operator decision rather than a guess.

1. Project in brief

Scamkaki gives Singapore seniors English/Hindi Guardian phone lines to describe suspicious
contact before moving money or after acting. Family receives likely-scam alerts by Telegram
and private link. Bait stalls fictional scam callers, extracts their claimed agency/request/payee
and supplies seven-day counts; a separate human reviewer reads draft reports.
The senior is the person contacted, the family member calls back, and the fictional scammer
may impersonate an agency, bank, courier, employer, investment group or relative.
Gates 1, 2, 3 and 4 are APPROVED 2026-10-30 for the redesign, as recorded in 00-status.md.

Targets from 01-product.md are fixture targets, not achieved real-world results: family alert
within one minute and callback before money moves; English Guardian at least 7/8 scams and
at most 1/4 legit, Hindi 2/2 scams and 0/1 legit; both already-acted courier cases urgent with
bank guidance; every likely_scam alerts and no other verdict does; Bait English at least 4/5
payees, Hindi at least 1/2; zero leaks. S6 live proof remains incomplete.

Hard rules: Bait stalls rather than speaking NRIC/OTP/card/password/bank/PayNow identifiers;
no agent claims to be an official/bank employee; reports are human-reviewed drafts and never
filed automatically; fixture labels remain visible; no victim identities; Guardian never says
safe with certainty, only likely scam, unclear/talk to family, or no scam signs found.

2. Where S8 sits

Build order: S1 tracer, S2 Hindi, S3 verdict/alert, S4 Bait/leaks, S5 sophisticated offline
verdict, S6 live conversation proof, S7 dashboard/demo, S8 reviewer records, S9 patterns,
S10 report review, S11 voice room, S12 family/final checks. S1-S5 and now S8 are locally done;
S6 is open, S7 is built but its video/live demo remain open; S9-S12 are unstarted.
Gate 4 permits offline redesign without closing S6/S7 live gaps.
Never cut: S1/S3, S4 leak guard, S5 already-acted/offline fixture check, labels, failed attempts,
honest missing fields, independent call/check records, warning meanings, auth, human review
and family isolation. Cut optional motion/decoration/duplicate copy first. Original cut order:
S7 extra polish, S6 Hindi live, then reduce English to the named four-case sample with disclosure.
S8 makes urgent checks, draft reports and call facts reachable from Overview in at most two
navigation actions. Automated path checks passed; human comprehension is unmeasured.

3. This slice's contract

- **Branch:** `scamkaki/slice-8-reviewer-workspace`.
- **Visible result:** Overview leads to a readable Calls history and actual call/check detail
  pages at desktop and phone widths. The reviewer can find failed calls and read stored
  transcripts. Guardian checks remain separate records with the recorded reasons and alert state.
- **Builds:** shared reviewer shell/theme/error content; Overview activity, priority alert and
  short draft queue; `/calls`, `/calls/{call_id}`, `/checks/{check_id}`; filtered SQL with bounded
  pagination; detail/queue reads; transcript projection. The Overview matching diagram is static
  explanatory content. Existing report and family routes keep working with shared-theme changes.
- **Assigned tests:** `test_reviewer_routes_require_admin` for routes built here; Calls search,
  pre-page filtering, stable paging, failed/missing-duration cases; call transcript and no-inferred-
  linkage tests; Check verdict/status/urgent matrix; recent-vs-old urgent priority; 503 vs empty.
  Existing dashboard assertions move to their owning routes without losing behavioral coverage.
- **Evidence:** `evidence/s8-workspace.md`; local fake-provider preview URL/port and stop command,
  HTTP 401/404/422/503 checks, populated/empty/error screenshots at 1280 and 375 px; real filter,
  Next/Previous and transcript disclosure walkthrough; independent guard mutations and restores.
- **Falsifiers:** a result attached by time/fixture instead of a verified relationship; false
  Started timestamp; an old urgent row promoted as new; lost failure records; missing values
  fabricated as zero; unescaped transcript; search applied only to the first unfiltered page.
- **Exit decision:** go only when the assigned checks and reachable page walkthrough pass.
  Human usability remains unmeasured. Stop for S9 authorization, not automatic continuation.
- **Authorizations to request:** S8 local implementation/branch and named test-branch checks.
  No call, production mutation or Git publication follows from this slice.

4. Out of scope

S9 owns /patterns, S10 /reports entry and focused review, S11 /voice/controller move, S12 family
restyle and stale/empty polling repair. Existing S7 call controls remain on Overview until S11.
No agents, fixture meanings/expectations, migrations, CI, manifests/lockfile, domain verdict/
extraction/leak/alert/report-draft rules or retained S6 records/audio were changed.
No live/provider/production action, installation, publication or deployment occurred.

5. Current state

[verified 2026-10-30] Branch scamkaki/slice-8-reviewer-workspace; HEAD/main 845f28892875c07708407947bdb7e7de39c2d6ef;
branch was created from clean published main, empty index. Implementation and evidence are
uncommitted. Main alone lacks S8 source. Current diff/status is the exact file inventory.
New source: app/presentation.py, templates _reviewer/_error/calls/call/check.html; main.py,
_theme.html, dashboard.html and store.py changed. scripts/preview_ui.py and new route/parser/
preview safety tests exist. Existing dashboard assertions moved without lost behavior checks.
Gate 3 code-fence formatting is whitespace-only. Historical handoff/status mirrors were clarified.

[verified] Final suite 290 passed, one existing Starlette/httpx warning; Ruff lint/format,
Node offline caller check and diff whitespace pass. Initial RED had 24 failures. First faults
34/35; sparse draft-queue test was strengthened and caught the missed fault. Two further
boundary faults caught. Final union 37 distinct faults caught with exact source restores.
Auxiliary UI review found a false page-2 empty-history label; the real route regression failed
before correction and all 11 Calls tests then passed. First failures remain retained in work/.

[verified] Actual fake-provider application walkthrough covered four S8 screens at 1280 and
375 px, populated/empty/503/missing states, HTTP 401/404/422/503, filters, Next/Previous,
escaped transcript, existing report and family, bounded keyboard focus. Evidence and screenshots:
docs/plans/scamkaki/evidence/s8-workspace.md and evidence/s8-screenshots/.
[verified] TEST_DATABASE_URL was reachable on a distinct endpoint from production. Only that
configured test database was migrated/truncated/seeded. Tests and previews ran sequentially.
Final preview http://127.0.0.1:8783, PID 91067, tool session 74921; stop command in evidence.
It uses explicit test Settings, fake SDK/Bolna/Telegram, no microphone or real session.
[verified] Installed Python/uv/Node and existing dependencies were used; nothing installed.
[unknown] Live credential/provider validity, deployed revision, Telegram receipt, real voice,
human usability, physical phone, named screen reader and CI. .env.local was never printed/hashed.

6. Authority

User 2026-10-30: "S8 and test-branch authorization are authroized. Go ahead and start implementation and database actions."
This covers local S8/branch and named test-branch migrations/truncation with fake providers,
never production. No commit, integration, push, deployment, install, provider update, call or
spend is authorized. S9 remains unauthorized and needs S8 in main under separate integration
authority before its branch can start. Earlier gate approvals do not grant those actions.

7. Read first

Relevant records are AGENTS.md, software-factory/functional-ui/frontend-design skills,
00-status.md, 01-product.md through 04-slices.md, evidence/s8-workspace.md and PROGRESS.md.
Current source/tests and the actual diff outrank this summary. The historical start handoff
and prototype evidence are snapshots, not current execution authority or application proof.

8. Done means

S8's local exit checks and reachable-page walkthrough passed. Architect-reviewer found no
in-scope orphan or redundant file to delete. Source/evidence remain uncommitted; S6/S7 gaps
remain open. The required closing question is "Continue to slice S9, or re-steer?"
No S9 work has started. This is a clean local slice boundary, with no publication authority.
Wait for instructions before taking any action.
```

## Prompt for handoff review

```text
Review Scamkaki S8 in /Users/jayd0/Desktop/bolna from scratch, read-only. Be unbiased, thorough
and honest. Assume it may be flawed and look for real problems, not confirmation.
The product gives Singapore seniors English/Hindi scam-check lines and family alerts; Bait
collects fictional script records and every report requires human review. S8 replaces an
overloaded dashboard with Overview, SQL-filtered/paged Calls, stored transcript Call detail
and separate Guardian Check detail. Existing report/family behavior remains required.

Standard: AGENTS.md and the approved S8 contract in current 04-slices.md, with Gates 1-3's
redesign constraints. Branch scamkaki/slice-8-reviewer-workspace at HEAD/main 845f288, source
and evidence uncommitted. Verify current Git and every claim directly. Main alone lacks S8.
Claims: final 290 tests passed, lint/format/Node/diff checks passed; 37 distinct faults caught
across a retained correction, exact restores; populated/empty/error/missing, HTTP and browser
walkthrough at 1280/375 px; no production/provider action or publication; S6/S7 gaps persist.

Inspect main.py, store.py, presentation.py, _theme/_reviewer/_error/dashboard/calls/call/check
HTML, preview_ui.py, changed dashboard/family tests and new calls/checks/reviewer_errors/parser/
preview safety tests. Cross-check evidence/s8-workspace.md, screenshots and retained work logs.
Stress-test SQL filtering before paging, literal wildcards, stable ties, limits, failed calls,
None versus zero duration, insertion-time labels, hostile text escaping, continuation handling,
no inferred call/check join, saved verdict/alert/urgency, old priority expiry, draft-only queue,
auth/cache/errors/retry and protected report/family semantics. Assess design quality, clear
mobile behavior, real empty states and any unused or oversized code.

Do not pass tests for the sake of passing. Flag weakened, proxy or trivially satisfied checks.
Retain the initial 34/35 miss and later-page regression evidence; do not relabel them as clean
first-run proof. Runtime tests use fake providers and only the already authorized configured
test database after independently verifying its isolation. No concurrent preview/test resets,
production write, secret output/hash, provider call, install, source edit or publication is
part of this review. A second LLM review is not independent runtime or human usability proof.
Return PASS, ISSUES FOUND or FAIL with exact file/line evidence, commands/results and the
smallest correction for each real issue. Distinguish blockers from suggestions.
Deliver your verdict and wait for instructions.
```
