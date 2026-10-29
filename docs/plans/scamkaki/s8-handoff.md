# S8 handoff

Prepared 2026-10-30. Background for an unstarted slice; all redesign gates approved.

```text
You are receiving background for Scamkaki S8 in /Users/jayd0/Desktop/bolna on macOS arm64. Prepared 2026-10-30 (Asia/Singapore) from the current main-tip gate documents, the approved local redesign amendments and actual Git/source state. The user subsequently authorized committing and pushing this package to main. This handoff is included in that publication; verify current refs and tracked documents rather than reuse the earlier uncommitted snapshot. The user's Envoi S25/S26 attachment supplies structure only; none of its commits, infrastructure state, secrets rules or authorizations applies to Scamkaki.

The gate documents win over this prompt. Re-verify Git and files before acting; stop and ask rather than guess if they conflict. AGENTS.md supplies the execution rules. Be brief and honest; no em dashes, invented results, weakened checks or co-author trailers. Any visualization is .html. Secrets never appear in notes, logs, screenshots, prompts or commits, and .env.local is never hashed or printed. Plan a context transfer around 50-70% of the window using transfer-context and the repository's slice-handoff rules.

1. Project in brief

Scamkaki gives Singapore seniors English and Hindi phone lines to check a call or message before moving money, or get urgent guidance after acting. Ah Ma Guardian collects their story, the app evaluates recorded warning signs, and likely-scam results alert family by Telegram and a private-link page. Ah Ma Bait stalls fictional scam callers, extracts claimed agency/request/payee details and feeds seven-day script counts to Guardian; human reviewers inspect its draft reports.

The senior is a Singapore resident contacted by an apparently credible caller or sender. The family member receives alerts and calls the senior back. The scammer may impersonate an agency, bank, courier, employer, investment group or relative. The reviewer is an operator, separate from the family-link viewer.

Targets from 01-product.md, not achieved results: family alert within 1 minute and callback before money moves; English Guardian at least 7 of 8 scam fixtures flagged and at most 1 of 4 legit fixtures; Hindi Guardian 2 of 2 scams and 0 of 1 legit; both already-acted courier cases get urgent family alerts and bank guidance; every likely_scam alerts and no other verdict does; English Bait captures at least 4 of 5 planted payees, Hindi Bait at least 1 of 2, with zero leaks. These are fixture targets, never performance against real scammers. S6 live proof remains incomplete; no real-world outcome or human usability result is established.

Product hard rules: Bait never speaks an NRIC, OTP, card number, password or real-looking bank/PayNow identifier; asked for one, she stalls. No agent claims to be a government, police or bank employee. Reports stay drafts until human review and are never filed automatically. Fixtures/test callers/demo data remain labeled on screens, evidence and videos; seed stories never copy victim identities. Guardian outputs are "likely scam", "unclear, talk to family" or "no scam signs found", never certainty of safety.

[verified 2026-10-30] 00-status.md records Gate 1 APPROVED 2026-10-30 and Gates 2, 3 and 4 APPROVED 2026-10-30 for the website redesign. These approvals select plans, not S8 execution, test-database writes or publication.

2. Where S8 sits

Whole build order: S1 tracer, S2 Hindi voice, S3 verdict/family alert, S4 Bait extraction/leak guard, S5 sophisticated verdict behind the tool, S6 Guardian conversation/live proof, S7 dashboard/report review/demo, S8 reviewer workspace/records, S9 visual script patterns, S10 focused report review, S11 voice room, S12 family view/final website checks.

S1-S5 are checked done in 00-status.md. S6 is open for live proof. S7 is built and checked locally, with backup video and full live demo still open, so its status box remains unchecked. S8-S12 are approved plans and unstarted. Gate 4 explicitly lets the offline UI redesign build on the existing S7 code without waiting for S6 live proof. This does not close S6 or S7 evidence gaps.

Original never-cut items: S1, S3, S4's leak guard, S5's already-acted path/offline fixture check, fixture labels on every screen. Original cut order: S7 extra polish; S6 Hindi live run; S6 English live run down to four cases, two scam including paid courier and two legit, reported as reduced. Redesign never-cut items also include failed attempts, honest missing fields, independent call/check records, warning/urgent meanings, auth, human review and family isolation. Its cut order removes optional motion, decoration and duplicate copy before any approved screen/function. The eight approved screen functions need user re-steering to cut.

S8 matters because it replaces one overloaded dashboard with task-focused Overview, Calls, Call details and Guardian check views. The design target is an urgent check, draft report or call detail reachable from Overview in at most two navigation actions, with no phone-width table overflow. Prototype checks do not establish human comprehension.

3. S8 contract

Copied verbatim from 04-slices.md, "### S8: Reviewer workspace and records":

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

Gate 2/3 decisions that constrain this contract:

- Existing FastAPI/Jinja/Postgres stack, system fonts, HTML/CSS/inline SVG. Midnight blue, ice blue, electric blue and restrained chartreuse; danger remains distinct in text/shape as well as color. No new dependencies or schema.
- New S8 routes are GET /calls?q=&line=&page=1, GET /calls/{call_id}, GET /checks/{check_id}. Every reviewer read uses AdminDep. Positive IDs, q length at most 100, line optional bait/guardian, page 1-1000. Missing positive IDs are 404; invalid input 422; read failure HTML 503/Retry, distinct from empty data.
- Call search is parameterized and applies before paging over fixture case, stored status and English/Hindi label, combined with line. Typed percent/underscore are literal. Fixed 50-row pages, fetch 51 for Next, order created_at DESC then id DESC, filters preserved in links. Lists exclude transcripts, raw extracted payload and payee details.
- Calls.created_at is an insertion time: label Recorded, never invent Started/end timestamps. Stored zero duration differs from None. Failed/stopped/other statuses remain visible. Completed does not mean a passed check.
- Guardian checks stay independent. No join by time, fixture or a coincidentally populated nullable execution id. Call detail never gains an inferred Guardian verdict. Bait call detail can link its actual report.
- Stored transcript markers assistant:/user: become Ah Ma/Caller; continuation lines survive, unlabelled text stays unlabelled, empty transcript is unavailable. Escape all content; no generated turns, speaker guesses, audio player or timestamps.
- Check detail displays its saved verdict, inputs and alert state. Urgent display uses existing HARM_ACTED. Priority on Overview is a likely-scam harmful-acted alert from the last 24 hours; older records remain in history. Telegram sent is not confirmed family receipt. Missing signs read None recorded.
- Overview uses existing feed/week/alerts and up to five draft reports. Existing report/family URLs work throughout. The matching diagram is explanatory, never proof of extraction accuracy. Navigation exposes only implemented destinations. No hardcoded illustrative rows or mockup state-switch controls ship in product templates.

4. Out of scope

S9 owns /patterns and its full visual pattern page. S10 owns /reports entry, focused report restyle and review acknowledgment. S11 owns /voice and the SDK/controller move. S12 owns family restyle and its stale/empty polling repair. S8 may make the shared-theme adjustments needed to keep existing report/family screens usable, but does not build those later capabilities. Existing report GET/POST, auth, same-origin protection, first-review timestamp, reviewed draft preservation and no-send behavior remain required.

Protected scope: agents/, seed fixture meanings/expectations, verdict/extraction/leak/alert/report-draft rules, migrations, CI, manifests/lockfile, retained failed S6 records/audio and historical mockups. No production write, real Bolna session/call, wallet check using credentials, agent change, Telegram message, paid inference, provisioning, install, cleanup sweep, commit, main integration, push or deployment is authorized here. No S6 rerun or S7 demo/video completion claim.

No new languages, call transfer, embeddings, framework migration, automatic filing, multi-family accounts, identity matching or scam-network tracking. Counts remain Bait record counts, not unique scammers or success rates.

5. Current state, verified 2026-10-30 unless marked unknown

[verified] Before publication, the branch was scamkaki/gates-ui-redesign and HEAD/local main/remote main were 154d1d72fc1518b1f5f29ec53024207cdf141a28 with an empty index. This is the source-code baseline, not the hash of the later documentation publication. The current publication head is the commit containing this handoff on main; resolve it with Git and compare with git ls-remote. scamkaki/slice-8-reviewer-workspace does not exist. No application/agent/migration/test/seed/manifest changes were made in this redesign session.

[verified] Modified tracked files: PROGRESS.md; docs/plans/scamkaki/00-status.md, 01-product.md, 02-architecture.md, 03-program-design.md and 04-slices.md. New untracked handoff/preview records are docs/plans/scamkaki/s8-handoff.md, s8-handoff-review.md, checks/ui-redesign-preview.md and mockups/redesign/*.html. These were this session's in-scope uncommitted files before the separately authorized publication. They are included in the main-publication package. After verifying the publication, the receiving session reads the tracked approved documents from main; it does not need to recreate or re-approve them. Any remaining or new dirty files need a fresh inventory.

[verified] The eight self-contained preview files are overview.html, calls.html, call-detail.html, check.html, patterns.html, reports.html, voice.html and family.html under docs/plans/scamkaki/mockups/redesign/. The preview is static illustrative fixture data. It uses no provider SDK, microphone, database or real session.

[verified] Prototype checks: all eight loaded at 1280 and 375 px with document width equal to viewport width; call search/filter, empty/error/retry, local mock review and mock voice selection were exercised. The first retry selected-state bug was fixed and rechecked. This is design-preview evidence only. No application suite was rerun and no S8 feature test exists yet.

[verified] Static preview is listening on 127.0.0.1:8782, PID 77120, started by python3 -m http.server 8782 --bind 127.0.0.1 --directory docs/plans/scamkaki/mockups/redesign, tool session 75911. It is not an S8 application preview. Re-verify before relying on or stopping that PID. Scratch generator/screenshots: work/ui-redesign/. Documentation checker: work/ui-redesign-gates/check_docs.py. Scratch is ignored/local, not a published dependency of the product.

[verified] Python .venv is 3.12.15; FastAPI, Jinja2, psycopg, pytest and Ruff modules are installed. uv is 0.13.0 at /Users/jayd0/.local/bin/uv; Node is v24.21.0 at /Users/jayd0/.local/bin/node. .env.local exists; no credential values were read or hashed for this handoff. Four agent JSON exports and migrations 0001-0005 exist locally. get_call, get_check, recent_reports, app/presentation.py and the new S8 templates are planned, not built.

[verified] Existing source has AdminDep on dashboard/report/session routes, FamilyDep on both family routes, existing report review SQL/guards, recent_feed, recent_alerts, scripts_this_week and a recent_calls query that currently loads full rows. Integration fixtures migrate and truncate the configured test branch. Merely setting TEST_DATABASE_URL does not redirect a normally launched app's DATABASE_URL.

[unknown] Current validity/values of Bolna, Neon, Render or Telegram credentials; exact available test-branch access; deployed revision and provider state. Prior slice records show these services were used, but this session made no live account or database checks. No new credential or infrastructure requirement has been established. Current wallet and permission to use it are not inferred from historical unused caps. S6 live proof and Pravesh's listener result remain open in status.

[verified] Once S8 is explicitly authorized, its branch is created from the then-current verified main tip containing these approved documents. Preserve any dirty work found then. The current publication does not authorize later S8 commits, integration or pushes.

6. Authority

User, 2026-10-30: "Looks good. I approve gate 1. Give the other gates all at once, ill approve them as well". This approved Gate 1 and requested the remaining drafts together.
User, 2026-10-30: "Yes i approve them all, then give a copy paste prompt for s8. Thanks. use this as reference on how to structure the prompt:". This approved the presented Gates 2-4 and requested this handoff. It did not say start S8 or authorize database resets.

S8 local implementation, creation of scamkaki/slice-8-reviewer-workspace and destructive integration-test use of the verified TEST_DATABASE_URL branch remain pending explicit named authorization. The proposed test scope is migrations/truncation of the test branch with fake Bolna/Telegram, never production. Once the user grants that exact scope, it persists and must not be requested again step by step. User, 2026-10-30, subsequently: "PLs push also commit the working tree and push to main once ure done". This authorizes this documentation/preview/handoff package's commit, main fast-forward and push only. It does not authorize S8 implementation or test-database resets. Later S8 Git publication, paid/live/provider actions, installs and manual deployment remain separately scoped.

7. Read first

AGENTS.md and its Slice handoff prompts; /Users/jayd0/.agents/skills/software-factory/SKILL.md; local 00-status.md top and 2026-10-30 sections; 01-product.md website redesign; 02-architecture.md website redesign architecture; 03-program-design.md website redesign program design; 04-slices.md approved S8-S12 build order and exact S8 contract; checks/ui-redesign-preview.md; PROGRESS.md.

Relevant visual skills: frontend-design and functional-ui. The design direction is already approved; no repeat approval is needed unless a decision changes. Plain HTML previews are the visual reference, with the gate decisions taking precedence where mockup placeholders differ, such as Recorded vs Started.

Relevant source: src/scamkaki/app/main.py, app/templates/dashboard.html, _theme.html, report.html and family.html; domain/store.py, types.py and verdict.py; migrations/0001_init.sql through 0005_guardian_signs.sql; tests/integration/test_dashboard.py, test_reports.py, test_admin_auth.py, test_family.py and conftest.py; tests/conftest.py and tests/support/fakes.py. Historical s7-handoff.md is context, not current authority: its unstarted-S7 claims have been superseded.

Re-verification commands include git status --short, git diff --cached --name-only, git branch --show-current, git log -5 --oneline main, git rev-parse HEAD main and git ls-remote origin refs/heads/main. No command should print credential values.

8. Done means

After explicit S8/test-branch authority, the slice has the approved Overview/Calls/Call details/Guardian check behavior, real stored synthetic fixture data, intact existing report/family behavior and no paid/live effects. Gate 3's S8-assigned tests include:
- test_reviewer_routes_require_admin
- test_calls_search_and_line_filter_apply_before_paging
- test_calls_paging_is_bounded_and_stable
- test_calls_keep_failed_records_and_missing_duration
- test_call_details_use_saved_time_and_escape_transcript
- test_call_and_check_are_not_joined_by_time_or_fixture
- test_check_page_preserves_verdict_urgency_and_alert_states
- test_overview_priority_excludes_old_urgent
- test_reviewer_read_failure_is_not_empty_data

Names and behavior remain governed by the approved documents. Each claimed guard has independent fail-capable mutation evidence and exact restoration. Existing assertions moving screens retain their behavior coverage. Injected hostile text is checked on actual rendered output, not merely on helper output. Absence/leak claims remain bounded to the guard actually tested.

Expected commands, only within the authorized scope and without installing anything:
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest tests/unit -q
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest tests/integration -q
node scripts/caller/check-live.mjs
git diff --check

The integration suite needs explicit test-branch authority and verified test settings before it runs. A safe preview uses explicit test Settings and fake providers, never the default production database configuration. scripts/preview_ui.py and any S8-relevant offline UI check are implementation artifacts only if actually needed; later voice/family controller checks are not built early.

Evidence in docs/plans/scamkaki/evidence/s8-workspace.md covers actual preview URL/port/stop command, HTTP 401/404/422/503, desktop/375 px screenshots, filter/paging/transcript navigation, real keyboard focus observations, mutation failures/restores and unavailable checks. 00-status.md records branch, the user's execution/test authorizations, outcomes and evidence limits. PROGRESS.md holds operational facts only. The architect-reviewer post-slice cleanup reviews this slice's changes without deleting retained historical/user work.

No usability, real-phone, named screen-reader, live voice, Telegram-receipt, CI, Render or deployed-result claim follows from local tests. Commit/integration/push/deployment occur only on separate named authorization. S9 remains unstarted. The exact S8 closing question is: Continue to slice S9, or re-steer?

Wait for explicit S8 and test-branch authorization before taking implementation or database actions.
```
