# S12: Family view and completed website flow

2026-10-30, Asia/Singapore. Local synthetic fixtures and fake providers only.
Branch: `scamkaki/slice-12-family-ui`, based on published main
`b6620b1990e58baebdc9d34991d0adf73a7624bd`. Authority is in `../00-status.md`.

## Decision

Local redesign go. Implementation, full fake-provider walkthrough, post-review regression
fixes, final full suite and scoped cleanup are complete. This is local fixture evidence, not
human acceptance or real-world effectiveness.
No publication, deployment, real microphone/provider session, message, spend or installation.
S6 live efficacy and S7 backup video/full live demo remain open.

## Implementation and boundaries

Family remains standalone, on its existing private paths and FamilyDep. The midnight header,
light reading area and restrained fixture label follow the approved Family mockup. The latest
alert puts the existing urgent/non-urgent guidance before expandable recorded reasons, with
earlier alerts beneath it. Existing guidance sentences, DOM IDs, fixture labels and meanings
are retained. No reviewer navigation, source-call inference or private-link shortcut is added.

The owning inline script still polls every five seconds. Failure keeps the last received
alerts and explicitly calls them potentially out of date. Success removes that marker;
successful empty clears latest/earlier content and the attention title. First successful load
is quiet. Unseen later IDs trigger bounded flashing, and sound only follows explicit opt-in.
An independent timeout clears flashing even while all later polls fail. Polls run one at a
time and unlock after failure. Keyed native disclosures retain their open state and focused
summary across status changes and reordering. Singapore day changes refresh relative dates.
Unchanged responses retain the same DOM nodes. Recorded values use text nodes,
including unknown labels, missing fields and prototype-like property names. Sent does not
confirm receipt or reading. No-JS text explains that alerts cannot refresh.

Two narrow Overview defects found in this walkthrough were repaired: unknown recorded agency/
request text had disappeared from activity headings, and the weekly count `19` wrapped into
two lines at desktop width. Escaped fallbacks and a scoped no-wrap rule preserve those values.
No business rule, schema, provider, dependency, agent, seed expectation or Voice controller changed.

## Setup, ownership and teardown

- Preview URL: `http://127.0.0.1:8783/`. Family used the separate fake private URL
  `http://127.0.0.1:8783/family/preview-family`.
- Runner: `PYTHONPATH=.:src UV_PYTHON_DOWNLOADS=never uv run --offline --no-sync python work/scamkaki-s12/run_preview.py STATE`.
  STATE was sequentially populated, empty, error and unconfigured. Populated previews were
  restarted when their startup template snapshots needed refreshing. Stop was Ctrl-C through
  each owned exec session. The server printed a normal shutdown; no preview listener remains.
- Fresh private admission compared normalized test/production endpoints without printing
  either, connected only to TEST_DATABASE_URL and required zero other test clients.
  No client was terminated. Tests, mutations and previews owned the test branch sequentially.
- `preview_ui.py` explicitly overrides database settings and Bolna/Telegram dependencies.
  Both template replacement anchors are validated before a reset. Voice retains its existing
  fail-closed fake SDK owner. Family controls are loaded from `tests/support/family-preview.html`.
- Family controls first request the existing local JSON endpoint, then transform its result
  into labeled simulated UI transitions. A simulated failed refresh is not an HTTP 503 result.
  The separate error preview produced actual Family JSON 500 responses. No new polling endpoint.
- Sound used PreviewAudio counters, never real audio. Voice Start used its existing fake SDK,
  which makes a real local HTTP request to the fake session endpoint. Connected/end/error were
  simulated callbacks. No microphone request or real SDK was used.
- Browser tab closed and explicit 1280/375 viewport override reset after verification.
  No user walkthrough, physical device, named assistive technology or recording occurred.

## Stored fixture data

`fixture_rows` retains the previous 64 labeled call records, 19 draft reports and seven-day
Bait groups of 19 courier/card, 4 bank/code, 2 bank/transfer and 1 hostile-text record. It adds
one S12 likely-scam check with `acted=none`, Hindi and Telegram off. Family's actual stored
JSON order was exactly IDs 1 urgent, 5 non-urgent, 2 old urgent. ID 2 is 25 hours old, keeps
its urgent meaning and loses priority. IDs 3 unclear and 4 no-scam-signs never appear there.
The reviewer walkthrough reads these separate check records directly. Recorded fixture fields
are synthetic inputs, not evidence that a real conversation was understood.

## Browser walkthrough

All eight screen types were checked at 1280x900 and 375x812. Captures are genuine normal
viewport images in [s12-screenshots](s12-screenshots/), never illustrative mockups or fabricated
screens. Audit and per-capture main text/overflow are in `work/scamkaki-s12/browser-audit.json`.
There are 125 captures, including initial failures, measurement faults and repeat checks.

| Screen | Checks actually performed |
|---|---|
| Overview | Priority, separate verdict records, draft queue, preserved unknown text, weekly count, empty/503, navigation and keyboard skip |
| Calls | Real query+line form, Next/Previous, retained URL state, failed/missing/zero durations, no-match, empty/503 and mobile records |
| Call detail | Bait source report link, expanded stored Hindi/hostile transcript, unavailable transcript, no-report state, Guardian without inferred check, missing/503 |
| Guardian check | Every stored verdict, recent/old urgent, non-urgent Hindi, sent/failed/off, recorded reasons, separate call meaning, missing/503 |
| Patterns | Actual counts, numeric bars, expanded native disclosure using Enter, hostile text, empty/503 and matching explanation |
| Reports | Draft/leak/missing fields, source call link, required native confirmation, actual POST/303, reviewed reload, repeated HTTP review, empty/missing/503 |
| Voice | Load/selection counters zero, fake Start/connecting/connected/end/error, selector locks, restored controls, unconfigured Start disabled, zero microphones |
| Family | Quiet initial data/empty, populated failure retains stale data, recovery, successful empty, unseen non-urgent Hindi, hostile/missing text, history, opt-in fake sound, bounded flashing and keyboard-stable disclosures |

The three Gate 1 paths were performed separately at both widths:

1. Overview, Read urgent check, `/checks/1`: **one navigation action**.
2. Overview, Review draft #19, `/reports/19`: **one navigation action**.
3. Overview, Browse calls, Bait call #64, `/calls/64`: **two navigation actions**.

The direct draft is in the bounded queue. Scrolling on the narrow layout is not counted as
navigation. Family was visited separately by its fake private URL. These are automated task
paths, not measured human comprehension.

Each screen's Skip link was activated by keyboard at both widths, focusing `main` with a
visible solid outline, zero overflow. Native details, report checkbox validation and Voice
selection were exercised separately. Family's focused open summary survived six actual
poll requests after the startup snapshot was refreshed. Keyboard receipts are in `keyboard.json`.
This is not a screen-reader or comprehensive accessibility audit.

The final/repeat views have zero horizontal overflow. Five initial expanded-control mobile
captures had 184-205 px overflow from unbroken preview diagnostic JSON outside main. The
preview output now wraps; repeat stale/recovery/empty/new/hostile/missing captures have zero
scroll overflow. The production Family reading area was not the overflowing element.

Flashing was present after a new alert and absent after 53.864 seconds of repeatedly failed
polls, while the stale warning and old alert remained. The exact 29,999/30,000 ms boundary is
also checked with the fake clock. Browser CSSOM parsed the reduced-motion `animation:none!important`
rule correctly; the native browser preference was false and its tools expose no preference
emulation. A reduced-motion preference session and physical-device motion check were not run.
The conditional CSS guard was independently mutated and caught by the actual page check.

## Requests and effects

The runner retained method/path/query/status and privacy/redirect headers, without credentials,
in `requests-populated.jsonl`, `requests-empty.jsonl`, `requests-error.jsonl` and
`requests-unconfigured.jsonl`, all under `work/scamkaki-s12/`.

- Exactly two actual fake-session POSTs were recorded: Bait/Hindi and Guardian/English, each
  HTTP 200. Their UI counters showed one Start/session request per attempt and zero microphones.
- Actual review requests returned 303. The first-review datetime and original draft survived
  both reload and a second HTTP review. Native unchecked confirmation prevented submission.
- Wrong Family page/JSON links returned 404. Reviewer unauthenticated reads returned 401;
  invalid page/line queries returned 422. Missing call/check/report returned 404.
- Family HTML retained no-store/no-referrer/noindex. Family JSON retained no-store and only
  likely-scam rows in the exact urgent/new/old ordering above.
- Error previews returned actual 503 for reviewer database reads, distinct from empty 200.
  Family HTML was 200 with explicit unavailable status after its actual JSON 500.
- Retained fake effect files show no execution fetches or Telegram sends. The second populated
  run records one fake Guardian mint; the final populated/empty/error/unconfigured runs record
  no mints. The first populated counter file was overwritten by the scratch runner's same-state
  output name before a backup was made. Its Bait mint remains evidenced by the unbroken HTTP
  request log and UI counters. Do not treat the final-run zero as an aggregate mint count.

HTTP assertions and repeated review timestamps are in `http-results.json`. Fake callback events
are distinguished from those HTTP requests. Neither Telegram sent nor a fake callback proves
receipt, actual provider connection or audio.

## Tests, guard receipts and retained failures

Baseline: 331 passed, one existing Starlette/httpx deprecation warning in 72.59 seconds.
Initial Family route red: 1 failed/10 passed. Initial UI red exposed stale/empty/missing/receipt
and flash failures. Preview controls and anchor refusal each failed before their implementation.
The initial fake oscillator did not return its target from connect, causing an invalid harness
TypeError; it was fixed before interpreting the corrected red results. Both logs remain.

Polling/disclosure red reproduced replacement of unchanged nodes; it passed after retaining
rendered data. A separate red case proved prototype-key recorded values were lost, then passed
after own-property label lookup. Overview unknown-label red failed before escaped fallbacks.
Stored non-urgent preview red failed before that fixture was added. No checks were weakened.

Pre-review verification: 345 passed, one existing Starlette/httpx warning in 77.44 seconds.
Ruff lint/format, offline caller, all 34 owning-script UI checks and git diff --check pass.
All 49 independent automated faults were caught with intended assertion failures and exact
restoration. One additional real-browser CSS fault was caught and exactly restored. No setup,
connection, syntax or import failure was counted as a guard result. Protected baseline tracked
files outside the explicit S12 allowlist are byte-identical, including routes/store, agents,
seed expectations, migrations, CI, manifests and lockfile. The index remains empty.

The first final lint pass found one long test string. Splitting the same literal and running
the formatter resolved lint/format without changing its assertion. An initial full run was
interrupted for that correction; it is retained separately and not counted as the final suite.

Receipts: `work/scamkaki-s12/faults/results.json` and short redacted per-guard failure logs.
Each fault is applied alone, runs its assigned check and restores exact bytes in finally.
The separate live CSS fault removes count no-wrap, observes two lines for `19`, then restores
exact theme bytes and observes one line. Its JSON/restoration receipt and screenshot are retained.

Initial Family screenshot `family-urgent-1280` actually shows loading and is not urgent-state
proof. `family-focus-after-polls-1280` is the failed pre-restart snapshot, not a passing focus
check. `family-hostile-1280` captured the prior non-urgent response before fetch/render finished.
Final captures wait for their specific DOM result and native browser state before screenshots.
Three locator attempts used the wrong/ambiguous label and were corrected from the live DOM:
Source call, Calls, and REVIEWED not sent. These are instrumentation mistakes, not application
failures. Original captures and tool failures are not relabeled as passing output.

## Remaining limits and review

Fixture rendering does not establish real-scam efficacy, Hindi comprehension, Telegram receipt,
real provider credentials/credit, real audio/SDK connection, CI, deployment or human usability.
No named screen reader, real device, human walkthrough or recording was available/performed.
S6 remains incomplete and S7's two open demo items remain open. There is no S13 plan.

The fresh read-only code/design/architecture review found two Important issues after the
initial green suite: overlapping polls could overwrite newer data, and status/addition changes
could replace focused reasons. It also found Today retained after midnight. That date issue
was treated as correctness because recency is meaningful on an alert page. Five new actual-script
checks failed before the fix and passed after it. The fake DOM now models movement blur,
connection and focus rather than assuming them.

The fix serializes active polls and releases the lock in finally. Native reason/detail views
are keyed by alert ID, retain open state and summary nodes, and restore the same connected
focused node after reordering without scrolling. Singapore day changes refresh relative date
labels. Browser status-change and reorder/focus rechecks were performed with the actual updated
script; no second LLM review is substituted for these regression checks. Scoped architecture
cleanup found no justified deletion candidate. Original evidence and historical/user files remain.
Final post-review verification: 345 passed, 1 warning in 431.45s (0:07:11).
This elapsed duration is not an application performance benchmark; its cause was not measured.
Ruff lint/format, offline caller, all 39 actual-script UI checks and diff whitespace pass.
All 54 independent automated faults caught their intended assertions and restored exact final
bytes; the separate real-browser CSS fault was also caught/restored. Native browser follow-ups
confirmed latest/earlier open focus through status changes and movement of the same focused
alert into history at 1280/375, with zero overflow. The race and midnight boundaries use the
actual controller with controlled deferred responses/fake clock. No setup error counts as proof.
The scope/secret/restoration audit passed. No deletion, publication or live provider action.

The first closure over a closed browser tab failed during follow-up capture. It was rebound
to the new tab before collecting the passing follow-ups. This did not change application code.
