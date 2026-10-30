# S9 script patterns evidence

2026-10-30, Asia/Singapore. Local application, synthetic fixtures, fake providers and the
isolated Postgres test branch only. Status: **go for S9 local completion**.
Authority is in [00-status.md](../00-status.md). S6 live proof and S7 video/live demo stay open.

## Scope and baseline

[verified] User: "please start", answering the S9 background and the response awaiting S9
implementation and named test-branch authorization. Created `scamkaki/slice-9-script-patterns`
from main `87739f0716da49641887401071cefae750696c98`. HEAD, local main and remote main matched;
index empty. Preserved inherited PROGRESS.md, 00-status.md and s9-handoff/review documents.
The two inherited handoff files remain byte-identical to their starting receipts.

[verified] The test endpoint differs from production, including after pooler suffix removal.
Only TEST_DATABASE_URL was connected, migrated, truncated and populated. No production
connection, environment-file output or environment-file hash was used. Existing dependencies
only, on macOS arm64 with Python 3.12.15. No installation.

[verified] Baseline: 290 passed, one existing Starlette/httpx deprecation warning.
First S9 route/link/auth/error tests: 10 failed, 10 passed because the page was absent.
After implementation: 30 focused checks passed. A preview-fixture check failed before its
fixture additions, then all nine Patterns checks passed.

## Implemented behavior and query

[verified] Admin-only GET /patterns uses reviewer_page/reviewer_error, shared theme and
no-store. It reads scripts_this_week, the same function as Overview. The shared SQL joins
scripts to calls and now explicitly requires `c.line = 'bait'`. Its existing script timestamp
window remains `s.created_at > now() - interval '7 days'`; groups remain agency/demand,
combining languages. No aggregation store, schema or matching-rule change.

[verified] Every group has visible agency/request labels and a numeric record count. Width
is count divided by largest count, rounded to two decimal places. Empty groups render no bars;
the empty maximum defaults to zero and no division runs. Native details show recorded labels,
languages and last-recorded time. Unknown stored values retain escaped text rather than blank
labels. Descriptions add no conversations, caller identities, network links or success rates.

[verified] Overview's weekly link and reviewer navigation reach /patterns. The matching
explanation is one shared _matching.html include on both pages. Its arrows explain the system,
not relationships between individual calls and checks. Existing voice controls remain on
Overview; Reports/Voice navigation entries were not added. Family behavior remains separate.

## Literal fixture expectations

The real-route grouping test stores these inputs, including deliberately inconsistent Guardian
script rows to test the Bait read boundary. None is a real caller or scam outcome.

| Input | Expected visible count |
|---|---|
| Bank / OTP: three English and one Hindi Bait script | 4, width 100% |
| Bank / transfer: two Hindi Bait scripts | 2, width 50% |
| Courier / card details: one English Bait script | 1, width 25% |
| SPF / personal details: script eight days old, recent parent call | Excluded |
| One current Bank / OTP script with a parent call 20 days old | Included in the 4 above |
| Guardian-parent Bank / OTP and ICA / app scripts | Both excluded |
| Separate Guardian check with similar_count 987 | Does not contribute |

[verified] A separate 3/2/1 case expects widths 100/66.67/33.33. Another case retains all
56 valid agency/request groups, each count 1 and width 100%, proving no 50-group list limit.
The actual rendered hostile-value test covers both Patterns and Overview's weekly summary.

The preview retains S8's 19 courier/card-details fixtures, then adds four Bank/OTP, two
Bank/transfer, one eight-day SPF row and one hostile-text row. Visible counts are 19/4/2/1;
widths are 100/21.05/10.53/5.26%. Languages are EN+HI for the first two, HI for the last two.
The hostile input is `<script>fixture agency</script>` and
`नमस्ते <img src=x onerror=alert(1)>`. These are synthetic escaping needles.

## Corrections and retained attempts

[verified] After the first 302-test full pass, extending the hostile-value test to Overview
reproduced blank unknown weekly labels: one failure, one pass. Fixed the weekly projection
to use escaped stored-value fallbacks, matching Patterns. The focused Patterns/dashboard
run then passed 20 checks. Existing assertions were preserved.

[verified] The first desktop screenshot exposed cramped words in the shared matching diagram.
Stacked its nodes vertically. The original first-narrow-diagram-1280.jpg is retained, alongside
the corrected populated-1280.jpg. This was a visual correction, not a gate decision change.

[verified] A full-page phone capture while scrolled included a skip link whose live DOM box
was above the viewport, top -80/bottom -36, without focus. This appears to be a capture artifact.
Retained first-scrolled-capture-375.jpg. The final populated phone capture starts at scrollY 0.
Control+Home could not be delivered by the browser tool. Real navigation and scroll controls
worked; actual Tab/Enter traversal and visible focus were checked at both widths.

[verified] Initial verbose pytest failures retained database-URL representations in owned
local logs. Those representations were redacted in the retained receipts. The final fault
runner uses short tracebacks and URL redaction. No credential values were printed in this
record or chat, and no environment file was printed or hashed.

## Independent guard faults

[verified] Initial run: 24/24 caught. After the Overview correction, final run: 26/26 caught.
Each fault ran alone, failed its assigned pytest check and restored exact starting source
bytes. Source SHA-256 receipts match before/after; no environment file was hashed. Initial
and final logs/runners remain under ignored work/scamkaki-s9/, with URL redaction as above.
These are named fault checks, not a claim of complete system coverage.

| Fault | Assigned failing check |
|---|---|
| guardian-rows-included | `test_patterns_show_only_seven_day_bait_groups` |
| eight-day-rows-included | `test_patterns_show_only_seven_day_bait_groups` |
| window-uses-call-age | `test_patterns_show_only_seven_day_bait_groups` |
| hindi-rows-excluded | `test_patterns_show_only_seven_day_bait_groups` |
| languages-split-same-pair | `test_patterns_show_only_seven_day_bait_groups` |
| different-requests-collapsed | `test_patterns_show_only_seven_day_bait_groups` |
| group-list-truncated | `test_patterns_has_no_group_limit` |
| bars-scaled-to-total | `test_patterns_scale_against_largest_count_and_round` |
| bars-all-full-width | `test_patterns_scale_against_largest_count_and_round` |
| numeric-count-inflated | `test_patterns_show_only_seven_day_bait_groups` |
| empty-maximum-unguarded | `test_patterns_empty_has_no_bars_or_division_by_zero` |
| patterns-admin-removed | `test_reviewer_routes_require_admin[/patterns]` |
| records-cacheable | `test_patterns_show_only_seven_day_bait_groups` |
| read-error-is-200 | `test_reviewer_read_failure_is_not_empty_data[/patterns-scripts_this_week]` |
| read-error-is-empty | `test_reviewer_read_failure_is_not_empty_data[/patterns-scripts_this_week]` |
| bar-agency-unescaped | `test_patterns_escape_hostile_stored_values` |
| bar-request-unescaped | `test_patterns_escape_hostile_stored_values` |
| detail-agency-unescaped | `test_patterns_escape_hostile_stored_values` |
| detail-request-unescaped | `test_patterns_escape_hostile_stored_values` |
| recorded-languages-truncated | `test_patterns_expand_recorded_labels_languages_and_time` |
| overview-summary-emptied | `test_patterns_overview_links_and_counts_share_source` |
| overview-pattern-link-broken | `test_patterns_overview_links_and_counts_share_source` |
| navigation-pattern-link-broken | `test_patterns_overview_links_and_counts_share_source` |
| patterns-loads-remote-sdk | `test_patterns_never_calls_providers` |
| overview-agency-unescaped | `test_patterns_escape_hostile_stored_values` |
| overview-request-unescaped | `test_patterns_escape_hostile_stored_values` |

## Browser and HTTP walkthrough

[verified] Real app preview at http://127.0.0.1:8783/patterns with explicit test Settings,
fake Bolna/Telegram and an inline fake SDK on Overview. Patterns loads no script or SDK.
No microphone, real session, provider call or message. Integration tests and preview resets
ran sequentially, never concurrently.

```sh
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync python scripts/preview_ui.py --reset-test-db --port 8783
```

The same command with `--state empty` and then `--state error` exercised those actual modes.
Stopped each process with Ctrl-C through its owned terminal session: populated 25489/PID 89570,
empty 47107/PID 90535, error 54558/PID 90629. No listener remained before the final suite.
Any future run must verify the port/PID again. Never launch the normal app with production
DATABASE_URL for this preview.

[verified] At 1280x900 and 375x812:

- Populated, empty and unavailable pages were visibly inspected and captured.
- document.scrollWidth equaled viewport width, including expanded-content captures.
- Overview's weekly link reached Patterns in one action at both widths. Reviewer navigation
  also reached the actual page. Overview retained the same four groups and counts.
- Every desktop disclosure opened with its recorded labels/languages/time; phone keyboard
  expansion and hostile details also opened. Tab reached skip link, brand, three navigation
  links and the first summary. Enter expanded it; focus had a solid 3px outline.
- Computed bar ratios agreed with displayed count ratios within CSS pixel rounding.
- Hostile values remained literal text. No injected main script/img nodes or external scripts
  appeared on Patterns. Hindi text remained present.
- Missing/wrong credentials returned 401 in each mode. Authorized populated and empty reads
  returned HTML 200/no-store; injected read failure returned HTML 503/no-store with local Retry.
  Retry was clicked and remained /patterns with 503 while the fault persisted, never false empty.

[verified] Thirteen genuine screenshots are retained in [s9-screenshots](s9-screenshots/),
including the two initial captures discussed above. Final main states are populated-1280/375,
empty-1280/375 and error-1280/375.jpg. Browser tab closed and viewport override reset.
DOM/request receipts and the read-only HTTP checker are in ignored work/scamkaki-s9/.

## Final checks and review

[verified] Fresh final suite: 303 passed, one existing Starlette/httpx deprecation warning.
The final command uses short tracebacks to avoid fixture-argument credential representations;
it changes failure presentation only. All assertions and the full test selection remain.

```sh
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q --tb=short
node scripts/caller/check-live.mjs
git diff --check
```

[verified] Ruff lint passed and the format check found 82 files already formatted. The offline
Node caller check passed without calls. The final diff check passed. Source guards were restored before the
full suite. Protected-file and documentary audits are recorded with the final session receipt.

[verified] Architect-reviewer post-slice check found no in-scope orphan, redundant implementation
or cleanup deletion. Both pages use _matching.html; new route/template/style/test/preview
pieces have callers. No new imports, dependency layer or aggregation store. Historical files
were preserved. A fresh agent inspected source, screenshots and retained receipts and found
no concrete S9 issue. It did not rerun tests, access a database or operate the browser, so
this is an auxiliary review rather than independent runtime or human-usability proof.

[verified] Final audit: 14 starting protected-file hashes still match, including both inherited
S9 handoffs. Protected directories/manifests and historical mockups have no changes. All final
fault restoration hashes match the current affected source. The six final main-state browser
receipts agree with screenshot counts, widths and zero overflow. A bounded credential-pattern
scan of changed text and retained failure logs found no matches. This is a bounded scan, not
a guarantee about every possible secret format. Index empty; HEAD/local main/remote main
remain 87739f0716da49641887401071cefae750696c98. No listener on port 8783. Receipt:
work/scamkaki-s9/final-audit.json. S9 remains uncommitted and unpublished.

## Publication re-verification, 2026-10-30

[verified] Later user authority covers this completed S9 package's commit, fast-forward into
main and push. Starting refs still match 87739f0 and the index is empty. Fresh full suite:
303 passed, one existing Starlette/httpx warning in 60.79 seconds. Ruff lint, format check
with 87 files, offline Node caller and diff checks pass. The test endpoint is freshly verified
as distinct, and only it is connected. All 23 tracked protected-file hashes match the starting
publication snapshot. The explicit publication manifest contains 34 files, including the
retained 13 screenshots and dated handoffs. Publication receipts live in ignored
work/scamkaki-s9-publication/. Earlier uncommitted/unpublished statements describe local exit.
Commit, fast-forward and push outcomes are resolved from Git after those operations.

## Evidence limits and stop

[unknown] Human comprehension, physical phones, named assistive technology, live audio,
provider credentials, Telegram receipt, CI and deployment. These checks establish local UI
and isolated test-branch behavior only. They do not establish scam detection performance,
S6 live completion or S7's missing recording/live demo. No agent, seed expectation, migration,
CI, manifest/lockfile, report/family rule or historical evidence was changed. No commit,
integration, push, deployment, provider action, spending or S10 work occurred.
