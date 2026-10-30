# S11 Voice room evidence

2026-10-30, Asia/Singapore. Status: **go for S11 local completion**.
Authored fixtures, fake providers and the isolated test branch only. Authority is recorded
in [00-status.md](../00-status.md). S6 live proof and S7 video/live-demo gaps remain open.

## Publication checks, 2026-10-30

[verified] The later user request authorizes S11 commit/main integration/push and then a
S12 handoff, as recorded in 00-status.md. The S12 local/test grant remains pending.
Exact reviewed 37-file package and completion hashes matched before documentary updates.
Fresh full suite: 331 passed, one existing Starlette/httpx warning in 71.45 seconds.
Ruff lint/format, 19 offline UI checks, offline caller and diff passed. Application/test/
screenshot bytes remain unchanged. The 30 retained fault hashes still match; no new browser
or mutation run occurred. Earlier S11 screenshot limits and failures remain unchanged.

[verified] Private endpoint check confirmed a distinct test endpoint and test-only connection.
The first ownership preflight refused another client before mutations; follow-up read-only
inspection found no other clients. No client was terminated. No preview listener on 8783/8784.
No environment file was printed or hashed. Receipts: work/scamkaki-s11-publication/.
Earlier local-exit/non-publication statements below are historical. Final Git commit/push
success is verified after execution and is never predicted within this package.

## Prerequisite and authority

[verified] Starting main/local/remote main was 2a6a21ed588991d622b86d77de26550487756db2,
with S8-S10 committed and an empty index/clean tree. Created and confirmed
scamkaki/slice-11-voice-room from that tip before application edits. User: "Please start s11".
The later selected answer was "Authorize this isolated S11 test scope", covering migrations,
truncation and fixture writes on freshly verified TEST_DATABASE_URL, fake Bolna/Telegram and
a controlled fake browser SDK only. No production, real microphone/provider session or spend.

[verified] Private endpoint comparison normalizes the pooler suffix and confirms a distinct
test endpoint. The first preflight refused another client before any reset. Subsequent
read-only inspection found no other clients. No client was terminated. The test-only connection
passed, and previews/tests ran sequentially. Neither environment file contents nor their hashes
were printed or retained. The source of the transient other client remains unknown.

## Implemented result

[verified] Admin GET /voice renders the shared reviewer shell and only boolean EN/HI availability
for Guardian/Bait. Agent identifiers never enter its HTML. Native radio choices and a language
select precede microphone/account-credit disclosure and explicit Start. Missing configuration
and missing SDK disable Start with readable explanations. No-JS copy and disabled native Start
are present. Actual JavaScript-disabled browser behavior was not separately exercised.

[verified] Voice alone owns the pinned v3.0.1 SDK and controller among reviewer pages. Overview
retains focus-aware 15-second refresh and has no voice buttons, constructor or SDK. Shared
navigation reaches Voice. Family has no reviewer navigation. Existing session URL/query/body/
response and EN/HI agent mapping are preserved, with no session-route implementation change.
No agent, model, prompt, transcript, rule, migration, manifest or lockfile changed.

[verified] The controller reserves one attempt before SDK construction, locks both selections,
and handles connecting/connected/end/error. It waits for stop before recovery when stopping is
asynchronous, rejects another Start, and ignores callbacks/rejections from superseded attempts.
The end state offers an explicit Calls link. It never reloads. If an unexpected stop failure
occurs, it retains the lock and offers another Hang up or closing the page, rather than
starting a potentially overlapping call. This case is offline proof only.

[verified source inspection] The unchanged pinned SDK has asynchronous start/stop and can
emit an error and reject start. Its public source was read without running it in a browser:
[pinned SDK](https://cdn.jsdelivr.net/gh/bolna-ai/web-call@v3.0.1/dist/bolna-web-call.min.js).
This establishes source behavior only, never account access or working provider audio.

## Test evidence and corrections

[verified] Existing offline baseline: 188 unit tests. Existing full baseline: 316 passed with
one existing warning in 65.16 seconds, excluding only the newly authored, intentionally red
Voice test file. Initial new route run: six failed on absent /voice, four existing session
contracts passed. Initial Node run failed because voice.html did not exist; that failure alone
does not establish the 19 behavior checks' capability. The independent faults below do.

[verified] The first implemented route/controller run passed 10 route cases and 19 offline UI
checks. Focused integration selection then passed 60 cases. Preview red checks exposed the
real SDK still served on Voice and a missing replacement guard. Preview now refuses a reset
unless its pinned SDK anchor matches exactly once, removes that script, and injects
only tests/support/voice-preview.html into Voice. Three final preview checks passed.
The fake lifecycle controls are preview-only and absent from production templates.

[verified] Reports' existing preview test now restores the Jinja loader after its scope, so it
cannot contaminate later production-template checks. Earlier assertions excluding Voice from
navigation now require the implemented destination. No behavioral assertion was removed.
Initial Ruff checks found long Python lines and formatting differences; corrected those and
retained the failed tool output. No lint configuration, dependency or check was weakened.

[verified] Final commands with installed dependencies only:

```sh
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync ruff format --check .
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync pytest -q --tb=short
node scripts/caller/check-live.mjs
node scripts/check_ui.mjs
git diff --check
```

Full suite: 331 passed, one existing Starlette/httpx warning in 72.50 seconds. Ruff lint passed;
93 files already formatted. Offline caller and all 19 UI checks passed; diff check passed.
No tests were skipped or excluded in the final full suite. Log:
work/scamkaki-s11/final-full-suite.log. Final code hashes match the restored fault receipts.

## Browser and actual fake-provider requests

[verified] Actual application at http://127.0.0.1:8784/voice. Diagnostic wrapper:

```sh
UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync python work/scamkaki-s11/serve.py --state populated --reset-test-db --port 8784
```

The wrapper adds preview-only counters/request receipts. The production app has no diagnostic
route. The normal preview remains runnable through scripts/preview_ui.py --reset-test-db.
All sessions below are HTTP requests to an in-process fake Bolna client, never real sessions.
Fake connected/end/error buttons emit simulated SDK callbacks, never provider audio/events.
The preview replaces and blocks microphone access; no external SDK script loads.

[verified] Desktop 1280x900 and phone 375x812 walkthrough:

- Load, persona/language selection and navigation created zero SDK instances/starts. Server
  counters stayed unchanged while reading Voice, Overview, Calls and Reports.
- Actual keyboard Tab moved from language to Start, with a measured 3px focus outline at both
  widths. Hindi labels remained readable. Enter started one desktop attempt. Double-clicks
  created only one attempt on desktop and phone; no overlapping instance was created.
- Connecting and connected locked both radio choices and the select. Hang up, natural end
  and error restored usable controls. Calls remained an explicit link, with no navigation
  on end. Following it reached Calls; reviewer navigation returned to a fresh inert Voice.
- Phone connection remained Connected for 37,248 ms with the same single attempt and no
  reload. This is one observed interval, not live-provider stability or latency evidence.
- Delayed fake stop kept Start and selectors locked. A simulated call-start during ending
  did not replace Ending. Completing stop restored controls.
- Previous call start/end/error callbacks left a newer Connecting attempt intact at both
  widths. An error event on desktop and an event plus rejected Start on phone recovered.
  Hindi and authored HTML-like error text stayed literal; a browser read found zero injected
  image nodes. Node independently rejects unsafe innerHTML writes.
- Missing-agent mode kept Start disabled for selections at both widths. Its actual manual
  session POST returned 503/Agent not configured with zero fake mints.
- Every saved 1280/375 measurement has document.scrollWidth equal to viewport width. These
  checks establish local browser behavior only, not human comprehension or physical-device use.

[verified] Seven successful actual HTTP POSTs reached the fake session endpoint in order:
fake-bait-hi, fake-guardian, fake-bait, fake-guardian-hi, fake-guardian-hi, fake-bait-hi,
fake-guardian. Each returned 200 with the existing fake response. user_data was None each time.
Fake execution fetches and Telegram sends remained empty. Browser microphone counters stayed
zero. Read-only HTTP checks additionally verified no-store and three denied auth cases, with
no counter changes. Request logs distinguish successful POSTs from authentication challenges.

[verified] One initial browser setup failed because the preview URL embedded fake Basic
credentials. Browser fetch rejected the relative session URL before an HTTP request. The
controller recovered; the failure screenshot/JSON are retained under
first-embedded-credentials-error-1280. Navigating to the normal credential-free localhost URL
using the existing auth session resolved it without product-code changes. The final seven
successful POSTs exclude that failed browser request attempt. Do not call this clean first-run
proof or count the failed request as a session minted.

[verified] 17 genuine JPEG captures are in [s11-screenshots](s11-screenshots/), including the
setup failure. Several full-page phone captures show a fixed Skip-link overlay, for example
connecting-375, ended-375, error-375 and ending-locked-375. idle-375 has a clipped top artifact.
This is not an exhaustive affected-file list. One live DOM inspection placed that link at
y=-80..-36 while measured overflow remained zero. That single inspection does not establish
the cause or normal-viewport placement for every capture. [unknown] The exact artifact cause
is unestablished. The screenshots do not prove normal-viewport Skip-link placement; width
measurements and lifecycle receipts are separate evidence. No production CSS repair was made.
Preview controls/diagnostics in expanded captures are explicitly fake, not product controls.

[verified] All owned previews stopped through Ctrl-C: initial session 70421/PID 24874,
final populated 68782/PID 25412 and unconfigured 42118/PID 26821. The initial inspection process
was restarted solely to add preview event controls compatible with read-only browser evaluation.
Initial receipts remain in browser-populated-initial. No listener remained before final tests.
Browser tab closed and viewport override reset. These PIDs are historical, never future targets.
Receipts: work/scamkaki-s11/browser-{populated,unconfigured}/, saved DOM/counter JSON files in
work/scamkaki-s11/, mobile-no-refresh.json and browser HTTP logs. No concurrent DB reset/preview.

## Independent guard faults

[verified] All 30 independently applied faults were caught by their assigned check. Every
fault restored exact starting bytes in finally. Current SHA-256 values match every restoration
receipt. Failure logs show intended assertion/unsafe-HTML failures, with no missing-test,
collection or database-connection failure substituted for a caught guard. This is evidence for
these named faults, not whole-system coverage. No environment file was hashed.
Runnable tool, redacted failure logs and receipts: work/scamkaki-s11/mutate.py and faults/.

| Named fault | Assigned failing check |
|---|---|
| voice-admin-removed | `tests/integration/test_voice.py::test_voice_requires_admin_and_fails_closed_without_password` |
| configuration-always-available | `tests/integration/test_voice.py::test_voice_exposes_only_boolean_availability_and_session_stays_503` |
| voice-navigation-hidden | `tests/integration/test_voice.py::test_voice_renders_disclosure_configuration_and_no_provider_effects` |
| sdk-duplicated-on-overview | `tests/integration/test_voice.py::test_overview_no_longer_owns_voice_and_navigation_reaches_room` |
| implicit-load-start | `node scripts/check_ui.mjs explicit-start` |
| implicit-persona-start | `node scripts/check_ui.mjs explicit-start` |
| implicit-language-start | `node scripts/check_ui.mjs explicit-start` |
| repeated-start-allowed | `node scripts/check_ui.mjs one-at-a-time-and-selection-lock` |
| persona-not-locked | `node scripts/check_ui.mjs one-at-a-time-and-selection-lock` |
| language-not-locked | `node scripts/check_ui.mjs one-at-a-time-and-selection-lock` |
| unconfigured-start-enabled | `node scripts/check_ui.mjs unavailable-selection` |
| missing-sdk-start-enabled | `node scripts/check_ui.mjs missing-sdk` |
| hangup-unavailable-during-connection | `node scripts/check_ui.mjs one-at-a-time-and-selection-lock` |
| hangup-inert | `node scripts/check_ui.mjs hang-up-connected` |
| attempt-never-released | `node scripts/check_ui.mjs natural-end-and-restart` |
| error-skips-sdk-stop | `node scripts/check_ui.mjs error-stops-before-recovery` |
| late-start-updates-new-attempt | `node scripts/check_ui.mjs late-call-start` |
| start-during-hangup-updates-status | `node scripts/check_ui.mjs hang-up-during-connection` |
| late-end-resets-new-attempt | `node scripts/check_ui.mjs late-call-end` |
| late-error-stops-old-sdk | `node scripts/check_ui.mjs late-error` |
| start-rejection-ignored | `node scripts/check_ui.mjs failure-reject` |
| sdk-error-event-ignored | `node scripts/check_ui.mjs error-stops-before-recovery` |
| status-rendered-as-html | `node scripts/check_ui.mjs error-is-text` |
| calls-link-never-shown | `node scripts/check_ui.mjs natural-end-and-restart` |
| voice-refresh-added | `node scripts/check_ui.mjs explicit-start` |
| overview-refresh-drops-focus | `node scripts/check_ui.mjs overview-focus-refresh-without-call-owner` |
| preview-anchor-guard-bypassed | `tests/integration/test_voice.py::test_preview_refuses_missing_voice_sdk_anchor_before_migrations` |
| preview-fake-moved-to-wrong-owner | `tests/integration/test_voice.py::test_preview_serves_fake_sdk_and_routes_sessions_to_fake_provider[populated]` |
| persona-query-hardcoded | `node scripts/check_ui.mjs one-at-a-time-and-selection-lock` |
| language-query-hardcoded | `node scripts/check_ui.mjs one-at-a-time-and-selection-lock` |

## Architecture cleanup and limits

[verified] Scoped source inspection found the old .talk styling unused after removing the
Overview call UI; removed those styles in this slice. There is one production Voice controller
and one separate safe preview fake. New template, test, preview fixture and offline checker
have route/loader/test/command references. Historical files and failed evidence are preserved.
A fresh read-only auxiliary review found no blocking source defect or in-scope orphan. It
flagged P3 documentation that understated the mobile screenshot overlays; corrected that
caveat here and in the transfer. The reviewer freshly ran 19 Node UI checks, 10 database-free
route/session cases and diff check, and checked all 30 restoration hashes. It performed no
DB/provider action, browser run or mutation. The separate synthetic caller SDK remains
intentional. This auxiliary review is not human acceptance or an independent safety oracle.

[verified] Final 37-file package audit: 13 tracked changes and 24 new files, including the
17 JPEGs. All 184 baseline files outside the explicit tracked allowlist are unchanged; every
fault restoration hash matches. Exact contract/eight-section transfer, configured-value and
credential-pattern bounds, no listeners and empty index pass. Receipts:
work/scamkaki-s11/final-artifact-audit.json and final-hashes.json. This bounded scan is not a
guarantee about every possible secret format. Source remains unchanged from the final suite.

[unknown] Real SDK audio/connection, provider credential validity, account credit, deployed
Render revision, Telegram receipt, human comprehension, physical devices, named assistive
technology and CI. S11 is local and uncommitted. No Git publication or S12 work is authorized.
Fixture/browser/offline proof does not close S6/S7 or establish real-world effectiveness.
