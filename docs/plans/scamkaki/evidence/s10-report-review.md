# S10 focused report review evidence

2026-10-30, Asia/Singapore. Status: **go for S10 local completion**.
Local application, authored synthetic fixtures, fake providers and the isolated test branch only.
Authority is recorded in [00-status.md](../00-status.md). S6/S7 evidence gaps remain open.

## Publication checks, 2026-10-30

[verified] The user separately authorized the S10 commit, main fast-forward and push.
The publication grant is in 00-status.md. S11 implementation and test scope remain pending.
Stopped the inspection preview only after verifying PID 6813's exact command and port 8783
ownership. Its earlier session 81053 was unavailable in this chat. No listener remained.
The first private preflight detected another test client and stopped before any reset.
Subsequent read-only inspection and the unchanged preflight found no other test clients.
Only the distinct test endpoint connected. The existing S10 test scope covers these checks.

[verified] Fresh full suite: 316 passed, one existing Starlette/httpx warning in 62.22 seconds.
Ruff lint passed, 92 files already formatted, offline Node caller and git diff --check passed.
Application, test and screenshot bytes are unchanged. All 17 JPEGs match the retained hashes.
The 35 earlier fault receipts remain prior guard evidence, not a fresh mutation run. No new
browser, microphone, provider, production, installation or deployment check ran.
Receipts: work/scamkaki-s10/publication-*.log and work/scamkaki-s10-publication/.
Earlier uncommitted/non-publication statements below describe the local-completion snapshot.
Final commit/push success is verified from Git after those operations, never predicted here.

## Prerequisite and scope

[verified] Under the user's explicit publication instruction, S9 commit
6565bc40ae10c6d8d41a64739251c10e8b63ff8b was fast-forwarded and pushed to main. Actual
ls-remote/local main/origin/main/retained S9 branch matched, with 0/0 left/right counts and
clean tree/index. Verified S8/S9 content, then created scamkaki/slice-10-report-review from
that main tip before edits. Fresh S9 publication suite: 303 passed, one existing warning;
Ruff lint/format, offline Node caller, bounded package scan and diff checks passed.

[verified] The user also granted the selected S10 local/branch and named test-database scope.
Private comparison normalizes pooler suffixes and confirms distinct TEST_DATABASE_URL and
production endpoints. Only the test endpoint connected. Integrations migrate/truncate it;
previews/reset operations are sequential with tests. No environment file was printed or hashed.

## Implemented behavior

[verified] Admin-only GET /reports reuses recent_reports(limit=1, drafts_only=False), with
existing draft-first/created_at DESC/id DESC ordering. It returns a non-cacheable 303 to the
chosen existing report, or the shared Reports screen with an honest empty state. Read failure
uses HTML 503/no-store/local Retry. Missing detail uses HTML 404/no-store.

[verified] report.html now uses the reviewer shell, existing palette/system fonts and a focused
reading panel with a separate Human review panel. Original draft text, facts, unknown labels,
leak warning and masked findings are escaped. Missing payee values remain not heard and missing
duration remains not recorded. Source links use actual stored call_id. Review status/time are
outside the original draft. Existing POST/auth/origin/SQL and URLs are unchanged. A native
required checkbox has no name/server field. Its browser acknowledgment is no new server guard.

[verified] Reviewer navigation adds Reports while Voice remains absent. Overview activity and
Bait call detail retain individual report links. S7 voice controls remain on Overview. No rule,
schema, migration, provider contract, dependency, agent, seed expectation or family behavior change.

## Checks and retained corrections

[verified] Initial focused red: 10 failed, 24 passed. Nine failures concerned missing S10
behavior. One invalid assertion guessed activity-h instead of the existing feed-h. Corrected
that test, then its preservation check passed before implementation. First green: 44 passed.
Preview fixture red: 2 failed, then 33 checks passed. Final focused selection: 50 passed.
All use short pytest tracebacks and private-value/URL redaction in retained receipts.

[verified] A first patch was rejected for duplicate delete/add targets, with no partial source
edits. It was reapplied as ordinary updates and a template replacement. Ruff later found one
long SQL string and one local import ordering issue; both were corrected. No check was weakened.
The earlier Patterns navigation assertion now requires Reports and continues rejecting Voice.
Ruff lint/format, offline Node caller and diff checks pass. The first full suite passed 316 tests
with one existing warning in 64.56 seconds. After the later leak-label copy correction, the
final full suite passed 316 tests, one existing warning in 63.09 seconds. Final Ruff lint/format
and diff checks passed. The existing offline Node caller also passed without real calls.

## Independent guard faults

[verified] Initial 35/35 and final 35/35 independent faults caught. The final run followed the
leak-label correction. Every assigned check failed alone and exact starting
source bytes were restored. Final SHA-256 values match all restoration receipts. No environment
file was hashed. These are named faults, not whole-system coverage. Redacted logs and the
runnable fault tool are retained in ignored work/scamkaki-s10/faults/, faults-final/ and mutate.py.

| Fault | Assigned failing check |
|---|---|
| entry-admin-removed | `tests/integration/test_checks.py::test_reviewer_routes_require_admin[/reports]` |
| detail-admin-removed | `tests/integration/test_checks.py::test_reviewer_routes_require_admin[/reports/1]` |
| review-admin-removed | `tests/integration/test_reports.py::test_report_pages_require_admin` |
| review-origin-bypassed | `tests/integration/test_reports.py::test_report_review_refuses_a_cross_site_form_post` |
| entry-reviewed-fallback-lost | `tests/integration/test_reports.py::test_report_entry_chooses_draft_then_reviewed_then_empty` |
| entry-newer-reviewed-first | `tests/integration/test_reports.py::test_report_entry_chooses_draft_then_reviewed_then_empty` |
| entry-oldest-created-first | `tests/integration/test_reports.py::test_report_entry_chooses_draft_then_reviewed_then_empty` |
| entry-id-tie-reversed | `tests/integration/test_reports.py::test_report_entry_breaks_equal_created_time_by_descending_id` |
| entry-wrong-redirect-code | `tests/integration/test_reports.py::test_report_entry_chooses_draft_then_reviewed_then_empty` |
| entry-redirect-cacheable | `tests/integration/test_reports.py::test_report_entry_chooses_draft_then_reviewed_then_empty` |
| detail-cacheable | `tests/integration/test_reports.py::test_report_focused_layout_acknowledgment_and_source_call` |
| entry-read-failure-false-empty | `tests/integration/test_reviewer_errors.py::test_reviewer_read_failure_is_not_empty_data[/reports-recent_reports]` |
| detail-missing-is-empty | `tests/integration/test_reports.py::test_report_unknown_id_is_not_found` |
| source-call-uses-report-id | `tests/integration/test_reports.py::test_report_focused_layout_acknowledgment_and_source_call` |
| checkbox-not-required | `tests/integration/test_reports.py::test_report_focused_layout_acknowledgment_and_source_call` |
| navigation-reports-broken | `tests/integration/test_reports.py::test_report_focused_layout_acknowledgment_and_source_call` |
| draft-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| summary-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| agency-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| demand-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| payee_bank-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| payee_account-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| paynow_id-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| url-unescaped | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| leak-warning-hidden | `tests/integration/test_reports.py::test_report_page_flags_a_leak_and_an_unlabeled_test_call` |
| leak-findings-hidden | `tests/integration/test_reports.py::test_reports_preview_has_hostile_draft_and_visible_leak_fixture` |
| fixture-provenance-hidden | `tests/integration/test_reports.py::test_report_page_shows_the_draft_and_the_script_fields` |
| missing-payee-invented | `tests/integration/test_reports.py::test_report_missing_fields_and_hostile_saved_text_remain_visible_and_escaped` |
| first-review-time-rewritten | `tests/integration/test_reports.py::test_report_review_twice_keeps_the_first_review_time` |
| reviewed-draft-redelivery-rewritten | `tests/integration/test_reports.py::test_reviewed_report_is_not_rewritten_when_bolna_redelivers_the_webhook` |
| provider-fetch-on-review | `tests/integration/test_reports.py::test_report_entry_and_review_have_no_provider_effects` |
| provider-session-on-review | `tests/integration/test_reports.py::test_report_entry_and_review_have_no_provider_effects` |
| telegram-send-on-review | `tests/integration/test_reports.py::test_report_entry_and_review_have_no_provider_effects` |
| overview-report-links-hidden | `tests/integration/test_reports.py::test_reports_entry_does_not_hide_other_report_links` |
| bait-detail-report-link-hidden | `tests/integration/test_reports.py::test_reports_entry_does_not_hide_other_report_links` |

## Browser, persistence and HTTP proof

[verified] Actual app at http://127.0.0.1:8783/reports. Owned diagnostic preview command:

```sh
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync python work/scamkaki-s10/serve.py --state populated --reset-test-db
```

The existing preview_ui.py remains directly runnable with --reset-test-db --port 8783.
The diagnostic wrapper adds local receipt logging only, never a production debug endpoint.
Its four sequential modes populated/reviewed/empty/error each reset the isolated test branch.
Stopped by Ctrl-C through owned sessions 65570/PID 230, 86716/PID 944, 96818/PID 1102 and
19643/PID 1153. Each stopped before the next reset. No listener remained before final tests.
These PIDs are historical receipts, not future stop targets. Browser tab closed; viewport reset.

[verified] The populated fixture has 19 reports on the existing Bait calls. Report 19 belongs
to call 55, report 18 to call 52. Report 19 has one authored masked finding and an operator-
authored synthetic draft containing Hindi and `<script>fixture draft</script>`. It is not a
model-generated report or real conversation. Other scripts preserve S9 counts 19/4/2/1.
The separately reset reviewed mode marks all 19 fixtures reviewed to test entry fallback;
its timestamps are separate from the two browser reviews below.

[verified] Browser walkthrough at 1280x900 and 375x812:

- Reports entry opened draft 19. After its review, navigation opened draft 18 rather than
  newer reviewed 19. The all-reviewed fixture mode returned 303 to report 19, with no form.
- At both widths, clicking Mark reviewed with an unchecked native checkbox kept the same
  draft, focused the checkbox and displayed the browser's validation message. No HTTP POST
  was added and the database still had draft/null review time.
- Real Tab/Space/Tab/Enter actions checked acknowledgment and submitted the native form at
  both widths. Checkbox and button had a visible 3px focus outline. Server receipts show
  the actual authenticated POST/303 and subsequent GET. The browser first issued an HTTP
  Basic 401 challenge, then resent credentials. The 401 attempt did not change review state.
- Reloaded DOM timestamps exactly matched the persisted database timestamps. Reviewed pages
  have no review form. Repeat reviews therefore used actual same-origin HTTP POSTs, not a
  second browser button. Both returned 303 and preserved first-review time and draft bytes.
- The source link opened actual call 55, whose Open report link returned to report 19.
  Overview's draft queue reached report 17 in one action. Integration checks also verify
  other activity and Bait detail links. Family kept its own layout without reviewer navigation.
- Native Review notes and limits expanded. Unknown/missing fields and the leak warning remain
  visible. Authored hostile draft text stayed literal; main contained zero injected script nodes.
- Draft, reviewed, empty, missing and 503 pages were captured at both widths. Measured
  document.scrollWidth equaled viewport width. Error Retry was clicked and stayed /reports
  with 503 while the fault persisted, never an empty Reports view.

| Actual browser review | Database before | Database after and reload, UTC | Draft bytes |
|---|---|---|---|
| 19 / call 55 / 375 px | draft, no review time | reviewed, 2026-10-30T04:45:42.875829+00:00 | unchanged |
| 18 / call 52 / 1280 px | draft, no review time | reviewed, 2026-10-30T04:47:10.141623+00:00 | unchanged |

[verified] HTTP auth checks return 401 for missing/wrong credentials. Missing report returns
HTML 404/no-store. Populated redirects and successful/empty reads are no-store; injected read
failure returns HTML 503/no-store and local Retry for entry and detail. Foreign Origin POSTs
return 403; same-origin repeat POSTs return 303. The reviewed fallback returns 303 to report 19;
empty returns HTML 200 with no form or draft. All fake fetch/session/send counts stayed 0/0/0
through viewing, both browser reviews, reloads, repeat HTTP reviews and each preview mode.

Receipts: work/scamkaki-s10/browser-{populated,reviewed,empty,error}/. Actual request/response,
row snapshots and draft hashes are in requests.jsonl, before.json and http-checks.json.
DOM/keyboard/reload/overflow receipts and local HTTP checkers are retained there or in the
S10 scratch root. No microphone, provider credentials, external SDK, session or message used.

[verified] 17 genuine JPEG screenshots are in [s10-screenshots](s10-screenshots/), including two
initial raw-scanner-label captures. The first browser inspection exposed otp_or_account_digits
in the UI. A browser assertion for the human label failed, then passed after mapping it to
Code or account digits. The masked finding and warning remain. The first HTTP counter checker
also failed because it assumed one request per submit, overlooking HTTP Basic's 401 challenge.
Its failure/diagnostic receipt is retained; corrected checks independently require both 401
and 303 with the unauthorized request leaving the row unchanged. Neither issue is hidden as
clean first-run proof. scripts/check_ui.mjs remains future-slice work.

## Final checks

[verified] Final commands, using existing installed dependencies only:

```sh
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q --tb=short
node scripts/caller/check-live.mjs
git diff --check
```

Ruff lint passed, 90 files were already formatted, full suite 316 passed with one existing
Starlette/httpx warning, offline caller and whitespace checks passed. All guards were restored
before the suite. Every baseline file outside the explicit 11-file S10 tracked-change allowlist
is unchanged, including store/rules/schema/agents/seed/historical evidence and screenshots.
No listener remained on 8783. New evidence/screenshots/session records are separate new files.

## Architecture review and limits

[verified] Architect-reviewer post-slice cleanup found no unused S10 styles/helpers, redundant
scaffolding or in-scope orphan requiring deletion. A fresh read-only reviewer inspected the
source, seven desktop/375 screenshots, HTTP/row receipts and final fault restoration hashes.
Verdict: PASS, no unresolved S10 defect. The stale S9 publication summary in status was corrected
and rechecked. This is auxiliary review: it ran no tests, database operation, browser session
or provider action itself. The actual runtime proof above came from this execution session.

The reviewer set aside server checkbox enforcement because the approved contract explicitly
makes this browser acknowledgment only; inherited report-ID validation and POST error/cache
behavior because they are preserved contracts; and S6/S7, S11/S12, production/providers and
broad historical cleanup because they are separate scopes. No deferred S10 defect follows
from those boundaries. Existing write-error behavior was deliberately preserved.

[verified] Final bounded audit passed: the 11 tracked changes match the explicit allowlist,
every other baseline file and historical screenshot is unchanged, final guard hashes match,
all four preview modes have zero fake effects, the 17 screenshot files are genuine JPEGs,
and changed text/retained failure logs pass the bounded private-value/credential-pattern scan.
This scan is not a guarantee about every possible secret format. Index empty, no listener on
8783. Receipts: work/scamkaki-s10/final-artifact-audit.json and the final documentary audit.

[unknown] Human comprehension, physical phones, named assistive technology, live provider
audio, Telegram receipt, CI and deployed Render revision. S10 has not been committed or
published. No production write, real provider/session/call, message, spending, installation,
manual deployment or S11 work occurred. Local fixture proof establishes neither effectiveness
against real scams nor S6/S7 closure. Stop before S11.
