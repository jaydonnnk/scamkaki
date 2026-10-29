# S7 evidence: dashboard, report review and demo

Branch `scamkaki/slice-7-dashboard-demo`, from `main` at `d74f56a` (equal to `origin/main`, clean tree, checked 2026-10-28).
Everything shown is a labeled fixture on a Neon **test** branch with fake Bolna and fake Telegram. No Bolna call, session, agent edit, push, deployment or production write happened in this slice.
The deployed Render app still runs the pre-S7 code.

## Authority

The user authorized S7 by name on 2026-10-28 ("I answer this question now i authroize"). That covers the branch and the code. Commits, main integration, pushes, deployment, installs, calls and spending were not requested and were not done. The inherited S6 work was already published to `main` under the user's earlier publication instruction, so no inherited edits were carried onto this branch.

## What was built

| Area | Change |
|---|---|
| `GET /reports/{id}` | Report page: status, fixture label, claimed agency, demand, payee fields, call length, language, leak result, summary and the stored draft text. Admin sign-in; unknown id is 404 |
| `POST /reports/{id}/review` | Marks the report reviewed and redirects (303) to the report. Admin sign-in; unknown id is 404; a second review keeps the first review time. It sends nothing |
| `store.get_report`, `store.mark_reviewed`, `store.recent_feed` | One report with its call and script; the review update (`where status = 'draft'`); Guardian checks and Bait scripts merged newest first |
| Dashboard | One live feed (Time, Line, Lang, Claimed, Wants, Warning signs, Result) as in the Gate 1 mockup, "Scripts heard this week", the existing call log, test-line buttons with a note that they start real calls |
| Family page | Restyle only; JS, labels, endpoints and the 24-hour urgent-first order are unchanged |
| `_theme.html` | Shared tokens and components, included by all three pages (no static route, no framework) |

Palette (design choices, not approved measurements): midnight blue `#0a1a3f` for the header and structure, ice blue `#f4f8fe` / `#e4effb` surfaces, electric blue `#1546d8` for primary controls, links and focus, chartreuse `#c9f227` only on the fixture label and the reviewed check mark.
Chartreuse is never used for a result. "No scam signs found" is a neutral ice badge with a circle, not green.
Urgent and error meaning is carried by text and shape as well as color: `URGENT` tag, thick left bar, triangle for likely scam, dashed border and diamond for unclear, circle for no scam signs, `LEAK (n)` text.
The urgent and status reds and amber are functional status colors outside the four-color brief; the brief has no danger color.
System font stack with Devanagari fallbacks; no external fonts.

Deviations from the Gate 1 mockups (content and behavior kept, layout changed where the real data differs):

- Guardian checks and Bait scripts are shown in one feed by time. A Guardian check is not linked to its call (Bolna leaves the execution id unfilled), so the feed never claims that a check belongs to a particular call.
- "Scripts heard this week" sits below the feed, not beside it: beside it the Result column was pushed out of view at 1280 px.
- Bait rows show "Not collected" for warning signs (Bait does not extract them) and a report link; payee details and the draft moved from the dashboard to the report page.
- The call log (status, length, case) is kept so failed or odd calls stay visible.
- The mockup files in `mockups/` keep their old colors as history.

## Checks, 2026-10-28

| Check | Result |
|---|---|
| `ruff check .`, `ruff format --check .` | pass |
| `pytest tests/unit` | 183 passed |
| `pytest tests/integration` (Neon test branch, fake Bolna and Telegram) | 76 passed, 1 pre-existing FastAPI/Starlette deprecation warning |
| `node scripts/caller/check-live.mjs` | pass (offline, no calls) |
| `git diff --check` | clean; new untracked files checked for trailing whitespace separately, none |

Baseline before S7 was 244 passed (183 unit, 61 integration). S7 adds a net 15 integration tests: 8 in `tests/integration/test_reports.py`, plus 8 in `test_dashboard.py` replacing 1 old dashboard test.
The old `test_dashboard_shows_bait_script_and_draft_labeled_fixture` was replaced, not weakened: its draft-text and payee assertions moved to the report-page tests because those fields moved to the report page.
Test database check before running: `TEST_DATABASE_URL` and `DATABASE_URL` are both set and differ (boolean comparison only; nothing printed).

Named contract test: `test_report_review_marks_reviewed_and_sends_nothing`. It asserts status and `reviewed_at` in the database, the reviewed page, zero Telegram sends and zero further Bolna fetches.
Two further tests were weak on first writing and were rewritten (below): the redelivery test checked `status` but not that the reviewed draft is kept, and the leak and label assertions matched text that the draft repeats.

## Guard coverage: 28 mutations

`work/scamkaki-s7/mutate.py` applies one edit at a time, runs the four relevant test files, restores the original bytes and compares SHA-256 with the original. Untracked files (`report.html`, `_theme.html`, `test_reports.py`) were protected the same way; all 28 restores matched.
Receipts (ignored, local): `work/scamkaki-s7/mutations-run1.json`, `mutations-rerun-m12-m13.json`, `mutate-run1.log`.

| Id | Mutation | Caught by |
|---|---|---|
| M01 | report page open without sign-in | `test_report_pages_require_admin` |
| M02 | review action open without sign-in | `test_report_pages_require_admin` |
| M03 | `mark_reviewed` records nothing | `test_report_review_marks_reviewed_and_sends_nothing` (+2) |
| M04 | second review overwrites the review time | `test_report_review_twice_keeps_the_first_review_time` |
| M05 | webhook redelivery rewrites a reviewed draft | `test_reviewed_report_is_not_rewritten_when_bolna_redelivers_the_webhook` |
| M06 | missing report page is not a 404 | `test_report_unknown_id_is_not_found` |
| M07 | review of a missing report is not a 404 | `test_report_unknown_id_is_not_found` |
| M08 | review sends a Telegram message | `test_report_review_marks_reviewed_and_sends_nothing` |
| M09 | review calls Bolna | `test_report_review_marks_reviewed_and_sends_nothing` (+1) |
| M10 | summary rendered unescaped | `test_report_page_escapes_what_the_caller_said` |
| M11 | draft text rendered unescaped | `test_report_page_escapes_what_the_caller_said` |
| M12 | report page hides a failed leak check | `test_report_page_flags_a_leak_and_an_unlabeled_test_call` (after fix) |
| M13 | report page drops its fixture label | `test_report_page_shows_the_draft_and_the_script_fields` (after fix) |
| M14 | report banner removed | `test_report_page_shows_the_draft_and_the_script_fields` |
| M15 | dashboard drops warning signs | `test_dashboard_lists_warning_signs_and_the_urgent_result` (+1) |
| M16 | no check is ever urgent | `test_dashboard_lists_warning_signs_and_the_urgent_result` |
| M17 | every check is urgent | `test_dashboard_lists_warning_signs_and_the_urgent_result` (+1) |
| M18 | urgent detail line removed | `test_dashboard_lists_warning_signs_and_the_urgent_result` |
| M19 | no-recorded-signs label removed | `test_dashboard_labels_a_check_with_no_recorded_signs` |
| M20 | dashboard says Bait collected warning signs | `test_dashboard_lists_bait_script_with_leak_check_and_report_link` |
| M21 | feed oldest first | `test_dashboard_orders_the_feed_newest_first_across_both_lines` |
| M22 | dashboard ignores reviewed state | `test_dashboard_shows_reviewed_state_of_a_report` |
| M23 | dashboard fixture label removed | `test_dashboard_lists_bait_script_with_leak_check_and_report_link` |
| M24 | family page fixture label removed | `test_family_page_rejects_wrong_link` |
| M25 | Bait leak hidden on dashboard | `test_dashboard_lists_bait_script_with_leak_check_and_report_link` |
| M26 | weekly script counts wrong | `test_dashboard_summarizes_scripts_heard_this_week` |
| M27 | "Telegram sent" relabeled as delivery | `test_dashboard_lists_warning_signs_and_the_urgent_result` |
| M28 | dashboard open without sign-in | `test_dashboard_requires_admin` (+1) |

Result: **28 of 28 caught, 28 of 28 restored byte-identical** (30 of 30 after the follow-up below).
Invalid first attempt, kept: in the first full run **M12 and M13 were MISSED**. Both tests passed with the page's own leak result and fixture label removed, because the draft text repeats "LEAK CHECK FAILED" and "Demo fixture case" by itself. The assertions were narrowed to the part of the page above the draft, then M12 and M13 alone were rerun and caught. The other 26 results are from the first run; the two edited tests are the only test changes since.
The `bolna.fetched` and Telegram absence assertions were proven against an injected sender in M08 and M09, which is the injected-needle self-test the project asks for.
Scope: these prove the listed branches, not total coverage. M05 guards existing behavior (`add_report`) that S7 relies on, not new code.

Flaky incident, kept: the very first mutation-runner invocation reported a failing baseline (`test_report_pages_require_admin`) and exited before any mutation. No output was saved, so the cause is unknown. Re-running that test 7 times and the four test files once all passed, and the second runner invocation (with the preview server and browser tab closed) had a clean baseline. [hypothesis] concurrent use of the shared test database by the preview server; [unknown] not reproduced.

## Browser checks (headless Chrome and the in-app browser tool)

Preview: `http://127.0.0.1:8770` (local only), run from `work/scamkaki-s7/preview.py` with a test-branch `Settings`, fake Bolna and fake Telegram, synthetic labeled rows. The preview injects the test admin header because the browser tool cannot send Basic credentials; sign-in itself is covered by the integration tests, not by this preview. The server is stopped.
The real Talk to Guardian and Bait buttons were never clicked; the preview log has zero `/web-call` requests.

Screenshots (`docs/plans/scamkaki/evidence/s7/`):
`dashboard-desktop.png` (1280 px), `dashboard-phone-375.png`, `report-draft-desktop.png`, `report-draft-phone-375.png`, `report-reviewed-desktop.png`, `family-desktop.png`, `family-phone-375.png`.
Desktop shots are real 1280 px headless Chrome windows. Headless Chrome will not open a window narrower than about 500 px, so the 375 px shots render the page in a 375 px iframe on a same-origin harness page; the layout width and media queries are those of a 375 px viewport. This is not a real phone.

Observed:

- Desktop: the urgent row has a red left bar, `URGENT` tag, the triangle likely-scam badge, "Ah Ma already: Gave card details or a code" and "Telegram sent". Warning signs show as text chips. Hindi labels (हिंदी, Hindi button text) render.
- 375 px: feed rows become two-column cards with labels, no horizontal scroll (`scrollWidth` not above `innerWidth` was measured at the tool's 800 px viewport; the 375 px screenshots show no clipping).
- Real click on Mark reviewed in the browser tool: the page reloaded as "Reviewed 28 Oct 13:31 SGT" with no button, and the dashboard showed "Report reviewed". Repeated in all three rehearsals.
- Focus: `:focus-visible` on all six dashboard controls computes to a solid 3 px electric-blue outline (programmatic focus). **Real Tab traversal was not verified**: the browser tool's Tab presses left `document.activeElement` on `<body>` nine times. DOM order is the four test-line buttons, then report links. Native `<button>` and `<a>` semantics are expected to handle Enter and Space [hypothesis].
- Contrast, measured from computed styles in the browser (WCAG ratio): fixture label 13.2, likely-scam badge 6.5, unclear badge 7.3, no-scam-signs badge 14.6, URGENT tag 7.6, table headers 6.4, muted text 7.5, primary button 7.2, link 7.2, section headings 7.0. All at or above 4.5. Borders between rows are decorative and lower.
- Not checked: a real phone, a screen reader, other browsers, dark mode (there is none; the old mockups had one), the 15-second auto-refresh under keyboard use beyond reading the code. The refresh now pauses while a control has focus, and says so on the page.

## Demo rehearsals: 3 UI-only walkthroughs, not live demos

Each run, through the in-app browser tool against the labeled preview data, reset first: dashboard (fixture label, warning signs, exactly one urgent result, all three verdict kinds) then report 1 as draft, a real Mark reviewed click, reviewed state, dashboard showing report 1 reviewed and report 2 draft, family page with the urgent alert first.

| Run | Steps passed | Wall time |
|---|---|---|
| 1 | 5 of 5 | 1.1 s |
| 2 | 5 of 5 | 1.0 s |
| 3 | 5 of 5 | 1.0 s |

What this is: an automated UI walkthrough of fixtures with fake providers; it proves the screens and the review action work in sequence, three times, from reset data. A first attempt of the script aborted on an unavailable timer after its first review click (hence one extra POST in the log); it was fixed and the three runs above are complete.
What this is not: a spoken demo, a live Guardian or Bait call, a Telegram delivery, a Render cold-start test or a rehearsal by a person. No full live demo check was run; **a full live demo is unavailable** (calls are deferred by the user) and is recorded as not done, not passed.

## Backup video

**Unavailable, not recorded.** No `ffmpeg` or video library is installed (no installs were authorized), and the macOS screen recorder would capture the user's whole desktop. The seven screenshots and this log are the substitute record; they are not a video. To close this item, the user can record the walkthrough, or authorize an install of a recorder.

## Limits and known risks

- Fixtures and fakes only. Nothing here tests the deployed app, Render cold starts or real Telegram arrival.
- A Guardian check cannot be tied to its call, so warning signs on the feed come from the check row only. Rows logged before migration 0005 carry defaults, so an empty signs list reads "None recorded" (not "none"), and an `other` channel reads "Channel not clear".
- "Telegram sent" means Telegram accepted the message, not that the family saw it; arrival stays unverified.
- Mark reviewed uses the existing HTTP Basic admin sign-in, which browsers resend automatically. After the first draft of this record the user asked for a same-origin check (see the follow-up below); `/web-call/session` has no such check and was not changed.
- A report page shows the stored draft text, which still opens with "DRAFT - not sent" after review; the review record is the status line, not a rewrite of the draft.
- S6's live exit checks are unchanged and still unmet.

## Post-slice cleanup (architect-reviewer, cleanup mode)

Scoped to this slice's diff. No orphan or dead code found: `recent_checks`, `recent_scripts` and `scripts_this_week` are all used by the dashboard path; `r.draft` was dropped from `recent_scripts` because no page needs it there; every CSS class in `_theme.html` is used by a template or by the family page script.
Kept, not deleted: the mockups with their old colors (Gate 1 history), `docs/plans/scamkaki/s7-handoff.md` (historical handoff), 33 inherited obsolete clips in ignored `scripts/caller/clips/` (still awaiting the user's decision), and ignored scratch in `work/scamkaki-s7/` (`preview.py`, `mutate.py`, receipts and logs).
Nothing was deleted.


## Follow-up, 2026-10-28, after the user's answers

User decisions: commit S7, merge and push `main`, add the same-origin check, close S7 with the open items recorded ("Yes to A"); Option A first for S6 with a 150-cent total cap; delete the obsolete clips.

- **Same-origin check.** `POST /reports/{id}/review` returns 403 when an `Origin` header is present and its host differs from the request `Host`; requests with no `Origin` (curl, tests) and matching origins pass. Two tests added, `test_report_review_refuses_a_cross_site_form_post` (failed before the change) and `test_report_review_accepts_a_same_origin_form_post`. Mutations M29 (check removed) and M30 (every Origin rejected) were each caught by their own test and restored byte-identical (`work/scamkaki-s7/mutations-rerun-m29-m30.json`). Limit: it relies on the browser sending `Origin` on form posts; behind Render the `Host` header is assumed to be the public host [unverified until deployed].
- **Obsolete clips deleted.** 33 WAVs in ignored `scripts/caller/clips/`, the batch generated 2026-10-27 22:45 for cases removed or reshaped before S5 closed. Manifest with names, sizes and SHA-256 kept locally at `work/scamkaki-s7/deleted-clips-manifest.json`. Kept on purpose: the other 63 unneeded clips from 2026-10-28 09:08 to 09:09 (S6-era audio, including the failed probe's original clips). All 91 clips the current fixtures need are present. `runs.jsonl` was not touched.
- **Closure.** S7 is closed with two items recorded as open, not passed: no backup video (unavailable) and no full live demo.

## Caller page restyle, 2026-10-29

User decision: restyle the fixture caller to match. Only the CSS and header markup of `scripts/caller/index.html` changed; element ids and the script are unchanged. `node scripts/caller/check-live.mjs` and `tests/unit/test_caller.py` pass. Checked by loading the running page at `http://127.0.0.1:8765/` in headless Chrome at 1280 px (`caller-desktop.png`); no session was minted, no call was placed and no button was clicked. Not checked: the Live microphone role-play view with its facts list, a narrow width, keyboard use. The fixture banner is now chartreuse with midnight text (13:1).
