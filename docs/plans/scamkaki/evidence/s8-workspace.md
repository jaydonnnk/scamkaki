# S8 reviewer workspace evidence

2026-10-30, Asia/Singapore. Local synthetic fixtures and fake providers only.
Status: **go for S8 local completion**. Authority remains in [00-status.md](../00-status.md).
S9 remains unstarted. Source and evidence were uncommitted at the local exit boundary.
The user subsequently authorized their commit, main integration and push; see 00-status.md.

## Authority and baseline

[verified] The user authorized S8 implementation and the named test-branch database actions.
Created `scamkaki/slice-8-reviewer-workspace` from clean main `845f28892875c07708407947bdb7e7de39c2d6ef`.
Local HEAD/main and remote main matched via `git ls-remote`. Index was empty.
The planning package was already committed. Its older uncommitted snapshot was historical.

[verified] Configured TEST_DATABASE_URL was reachable on a distinct endpoint from production,
including comparison after removing the pooler suffix. Only that configured test database
was migrated, truncated and populated. No environment-file contents or hashes were printed.
Application preview receives explicit test Settings and fake Bolna/Telegram dependencies.
It substitutes a local fake SDK for the existing remote call SDK. No microphone, real session,
provider call or message was used. The preview tests reject a missing URL, shared production
endpoint and absent explicit reset flag before any database mutation.

[verified] Baseline `UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q`:
262 passed, one existing Starlette/httpx deprecation warning. Initial S8 checks: 24 failed,
8 passed. The missing routes/projection/error states caused the failures.

## Implemented behavior

[verified] Overview has recent independent activity, last-24-hour urgent priority, up to five
draft reports, seven-day Bait counts and a static matching explanation. Calls searches fixture,
status and language labels in parameterized SQL before paging, with a combined line filter.
Percent and underscore are literal. Pages fetch 51, display 50 and use created_at/id ordering.
Call lists omit transcripts, raw extraction and payee fields. All stored statuses remain visible.

[verified] Details use Recorded insertion time, preserve missing versus zero duration, escape
stored transcript turns and retain continuation/unlabelled text. Guardian checks remain separate
even if an execution id matches a call. Bait links only its actual report. Check details preserve
saved verdict, harmful-acted urgency and every alert status. Telegram sent is not receipt.
New reads use AdminDep, positive IDs, bounded inputs, no-store and distinct 404/422/503 responses.
Report reads also get 503 handling; existing review/write and family behavior remain intact.

[verified] No patterns/report entry/voice-room/family restyle was built. S7 voice controls and
controller remain together on Overview for the S11 move. No new dependency, schema, agent,
fixture meaning or verdict/extraction/leak/alert/report-draft rule was changed.

## Test corrections retained

[verified] First focused run: 31 passed, one old weekly-count assertion failed because it
matched the old table markup. Its Police/Money transfer/count 2 and old-bank exclusion assertions
were retained in the new owning section. Full run then passed 286 tests.

[verified] Initial faults: 34 of 35 caught. The reviewed-row filter fault escaped because six
drafts filled the five-row queue ahead of reviewed rows. The test was strengthened with one
remaining draft and reviewed rows, passed intact, then failed on the same fault. All source
bytes were restored after each attempt. The first missed receipt remains retained.

[verified] Auxiliary read-only functional UI review found an empty later-page bug: page 2 with
one stored row said No calls yet. A real route regression failed before the fix, then all 11
Calls tests passed. It now says No calls on this page with Previous guidance. The auxiliary
review found no additional actionable issues. This review is not independent runtime proof.

Two additional independent faults then proved invalid-line rejection and stored-zero duration.
Both failed their assigned tests. Final union: 37 distinct faults caught across the recorded runs.

## Independent fault receipts

[verified] Each fault below ran alone, produced a pytest assertion failure and was restored to
its exact starting bytes. The queue filter passed only after the correction described above.
Receipts, runner and source-only restoration hashes are retained under ignored
`work/scamkaki-s8/`; no environment file was hashed. These prove the named checks can fail,
not complete system coverage.

| Fault | Failing check |
|---|---|
| `auth-_` | `test_checks.py::test_reviewer_routes_require_admin` |
| `auth-_calls` | `test_checks.py::test_reviewer_routes_require_admin` |
| `auth-_calls_call_id` | `test_checks.py::test_reviewer_routes_require_admin` |
| `auth-_checks_check_id` | `test_checks.py::test_reviewer_routes_require_admin` |
| `search-disabled` | `test_calls.py::test_calls_search_and_line_filter_apply_before_paging` |
| `line-filter-disabled` | `test_calls.py::test_calls_search_and_line_filter_apply_before_paging` |
| `wildcards-not-literal` | `test_calls.py::test_calls_search_and_line_filter_apply_before_paging` |
| `stable-order-removed` | `test_calls.py::test_calls_paging_is_bounded_and_stable` |
| `offset-ignored` | `test_calls.py::test_calls_paging_is_bounded_and_stable` |
| `lookahead-shown` | `test_calls.py::test_calls_paging_is_bounded_and_stable` |
| `list-loads-transcript-payload` | `test_calls.py::test_calls_search_and_line_filter_apply_before_paging` |
| `failed-calls-hidden` | `test_calls.py::test_calls_keep_failed_records_and_missing_duration` |
| `missing-duration-zero` | `test_calls.py::test_calls_keep_failed_records_and_missing_duration` |
| `false-started-label` | `test_calls.py::test_call_details_use_saved_time_and_escape_transcript` |
| `timestamp-fabricated` | `test_calls.py::test_call_details_use_saved_time_and_escape_transcript` |
| `transcript-unescaped` | `test_calls.py::test_call_details_use_saved_time_and_escape_transcript` |
| `empty-transcript-generated` | `test_calls.py::test_call_details_use_saved_time_and_escape_transcript` |
| `speaker-guessed` | `test_presentation.py` |
| `continuation-dropped` | `test_presentation.py` |
| `inferred-call-check-link` | `test_checks.py::test_call_and_check_are_not_joined_by_time_or_fixture` |
| `priority-expiry-removed` | `test_dashboard.py::test_overview_priority_excludes_old_urgent` |
| `priority-harm-removed` | `test_dashboard.py::test_overview_priority_excludes_old_urgent` |
| `urgent-omits-paid` | `test_checks.py::test_check_page_preserves_verdict_urgency_and_alert_states` |
| `urgent-omits-gave_code_or_card` | `test_checks.py::test_check_page_preserves_verdict_urgency_and_alert_states` |
| `urgent-omits-installed_app` | `test_checks.py::test_check_page_preserves_verdict_urgency_and_alert_states` |
| `urgent-always` | `test_checks.py::test_check_page_preserves_verdict_urgency_and_alert_states` |
| `alert-state-flattened` | `test_checks.py::test_check_page_preserves_verdict_urgency_and_alert_states` |
| `queue-unbounded` | `test_dashboard.py::test_overview_draft_queue_is_bounded_and_excludes_reviewed` |
| `queue-includes-reviewed` | `test_dashboard.py::test_overview_draft_queue_is_bounded_and_excludes_reviewed` |
| `503-is-200` | `test_reviewer_errors.py` |
| `positive-call_id-guard-removed` | `test_calls.py::test_reviewer_detail_ids_must_be_positive` |
| `positive-check_id-guard-removed` | `test_calls.py::test_reviewer_detail_ids_must_be_positive` |
| `query-length-unbounded` | `test_calls.py::test_calls_paging_is_bounded_and_stable` |
| `page-minimum-removed` | `test_calls.py::test_calls_paging_is_bounded_and_stable` |
| `page-maximum-removed` | `test_calls.py::test_calls_paging_is_bounded_and_stable` |
| `invalid-line-accepted` | `test_calls.py::test_calls_paging_is_bounded_and_stable` |
| `zero-duration-missing` | `test_calls.py::test_calls_keep_failed_records_and_missing_duration` |

## Browser and HTTP proof

[verified] Actual application preview at http://127.0.0.1:8783, bound to loopback only.
Command from the repository root:

```sh
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync python scripts/preview_ui.py --reset-test-db --port 8783
```

This command resets the configured test database. `--state empty` uses no rows;
`--state error` injects a synthetic database-read failure at the app boundary. State selection
is CLI-only; product templates contain no sample-state switches or illustrative rows.
All three modes were actually run. Browser uses only the fixed dummy preview sign-in from
the script, never production credentials. Screenshot files capture page content, not credentials.

[verified] Populated fixtures: 56 calls, 19 Bait reports/scripts and four independent Guardian
checks. Unfiltered Calls showed 50 then six rows, with IDs 56..7 then 6..1. Next and Previous
were clicked. Hindi plus Bait returned nine rows, all Hindi and Bait. Stored hostile script
text displayed as text in the expanded transcript, including a Hindi caller and continuation.
Both absent durations and stored zero were visibly retained in history. Filter, query and
pagination results were also checked through real PostgreSQL integration tests.

[verified] Overview to urgent check took one navigation action; Overview to draft report one;
Overview to a call took Browse calls then a record, two actions. Scrolling is excluded from
these action counts. These are automated path checks, not human comprehension measurements.

[verified] Four new reviewer GETs returned 401 without credentials and with a wrong password,
then 200 with the synthetic authorized account. Missing positive call/check IDs returned 404.
Zero/negative IDs, invalid line and page 0/1001 returned 422. Injected database failure returned
HTML 503/Retry/no-store for Overview, Calls, Call, Check and existing report reads. Retry was
clicked and preserved `q=Hindi&line=bait&page=2`. Empty database views returned real empty states,
never a substituted error state. HTTP receipts are `http-populated.json` and `http-error.json`
under `work/scamkaki-s8/`; values contain paths/statuses, not secrets.

[verified] Genuine screenshots in [s8-screenshots](s8-screenshots/): Overview, Calls, expanded
Call, separate Check; empty Overview/Calls; shared 503 states; missing record; existing report
and family at desktop/375 px. Existing family polling rendered the urgent synthetic alert and
older alert with no reviewer navigation. Report review was not submitted in this browser run;
its persistent review, auth/origin, idempotency and no-send guarantees passed integration tests.

[verified] Browser document scrollWidth equaled viewport width at 1280 and 375 px for the
captured states. Temporary viewport overrides were used. Initial desktop captures were
1280x720; final four S8 desktop screenshots were replaced with 1280x900 captures. Phone captures
were 375x812. Temporary viewport overrides were reset before completion.
Keyboard actions visibly focused Skip to content with a 3 px outline, Enter focused main,
and Tab from search reached Line then Apply filters with visible focus. This is a bounded
keyboard traversal, not a whole-app accessibility audit or named screen-reader check.

[verified] While the first preview was intentionally stopped for a regression test, Overview's
existing auto-refresh reached a connection-refused browser page. No app fault was inferred.
The restarted server returned HTTP 200; a fresh browser tab restored the actual preview.
A label-based browser selector also failed for Line; the visible native select's observed ID
worked. Neither incident is counted as a successful application interaction.

## Architecture cleanup and remaining limits

[verified] Post-slice architect-reviewer check: every new template has a route/include consumer;
the transcript helper is used by Call detail; all changed store methods have inspected callers.
No in-scope orphan, stale scaffolding or redundant file was found. Historical mockups, failed
S6 records/audio and ignored scratch were retained. No deletion or cleanup sweep was performed.
Ruff required whitespace-only formatting in existing Gate 3 Python code fences; no gate decision
or copied S8 contract changed. New navigation contains implemented Overview/Calls only.

[unknown] Human usability, actual phone/assistive technology, real voice behavior, family
receipt, production runtime, CI and deployment. This is local fake-provider and real test-DB
proof only. S6 live proof and S7 backup video/full live demo remain open. S9-S12 are unstarted.
No installation, real provider/session/call, production mutation, Git publication or deployment.

## Final verification and preview ownership

[verified] Final `UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q --tb=short`:
**290 passed**, one existing Starlette/httpx deprecation warning. Final Ruff lint and format
checks passed, as did `node scripts/caller/check-live.mjs` and `git diff --check`.
No dependencies were installed or changed. New script/source/tests were included by Ruff.
The offline caller check exercised no microphone/provider calls.

[verified] Final populated preview was restored after the suite, PID **91067**, tool session
**74921**, listening at **http://127.0.0.1:8783/**. Stop with `kill -INT 91067` after confirming
that PID still owns port 8783 using `lsof -nP -iTCP:8783 -sTCP:LISTEN`.
The server remains available for local review and uses the fake SDK/providers. Final browser
DOM had zero external script elements. Focus on an Overview control visibly paused its
15-second refresh. The in-app browser tab was retained and its viewport override reset.
Scratch server logs remain in `work/scamkaki-s8/`, outside product evidence/publication.

[verified] Final diff review found only S8 source, tests, preview support and documentary
maintenance, with an empty index. Protected paths were unchanged. New text/source files were
also checked for whitespace, bounded credential patterns and em dashes. At that local exit,
no S8 commit, main integration, push or deployment had occurred; main/HEAD was `845f288`.
The later publication request is recorded in 00-status.md. Resolve final refs from Git.

[verified] Final documentary/source scan covered 50 changed/new files, including 23 genuine
JPEG screenshots, retained the exact S8 contract in both handoff records and found no bounded
credential-pattern or whitespace matches. Final remote main still matched `845f288` via
`git ls-remote`. [Session transfer and independent review prompt](../s8-session-transfer.md)
are prepared at this local slice boundary. The final four desktop S8 captures are 1280x900;
phone captures are 375x812, all with document width equal to viewport width.

## Publication verification, 2026-10-30

[verified] Fresh publication suite: 290 passed, one existing Starlette/httpx warning. Ruff
lint/format, Node offline caller, diff whitespace and the explicit 50-file bounded credential
scan passed. The configured test endpoint still differs from production. No-mistakes CLI
is unavailable; no installation or new pipeline configuration was made.

[verified] Preview PID 91067 was stopped before the destructive test checks. Port 8783 had
no listener afterward. The earlier screenshots remain retained S8 evidence; they were not
repeated for this Git publication. Resolve any future preview process from live state.
The user's publication authority and S9 handoff request are recorded in 00-status.md.
Commit/push success and exact refs are verified from Git after publication.
