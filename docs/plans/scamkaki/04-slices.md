# Slice plan: Scamkaki

Current amendment: website redesign, Gate 4 APPROVED 2026-10-30.
The original sections below describe the prior contract; the dated redesign section at the end
is the approved amendment. Status and approval authority remain in [00-status.md](00-status.md).

Compact gate draft, 2026-10-22.
Revised 2026-10-22: S2 is the Hindi voice slice; Hokkien is dropped; Mandarin is a stretch after S7 (was S6 before the 2026-10-28 split).
Revised 2026-10-24: S3 alerts the family by Telegram and a family alert page instead of transferring the call.
Revised 2026-10-27 (reopened): S5 grows to cover sophisticated scams: warning signs, already-acted handling and the rewritten Guardian fixtures, on top of the 7-day loop already built on its branch.
Revised 2026-10-28 (reopened): that S5 is split. S5 builds the sophisticated verdict behind the tool with no calls; S6 updates the Guardian agents and runs the live fixture calls; the dashboard and demo slice becomes S7.
Riskiest first.
Each slice ends with a visible, working result and evidence in `evidence/`.
Branch per slice: `scamkaki/slice-<N>-<slug>`.

## Build order

| ID | Slice | Visible result | Tests and evidence | Authorizations to request |
|---|---|---|---|---|
| S1 | Tracer: Guardian stub end to end | A phone call to Guardian hears the stub "Not sure, please call your family"; the call appears on the dashboard | Unit: env example test. Integration: webhook token, webhook stores call, match-script token. Evidence: call id, dashboard screenshot, execution JSON shape, whether call variables round-trip | `uv` install of pinned deps; Neon project + test branch; Render deploy; Bolna agent create; up to 3 test calls |
| S2 | Hindi voice | A Hindi web call to Guardian HI hears a Hindi auntie voice, Guardian HI extracts agency and demand and calls `match_script`; the call shows on the dashboard as `hi`. Builds `agents/guardian_hi.json`, `calls.language`, `agent_line`, a Talk to Guardian button per language, and removes the Hokkien TTS leftovers (`tts_modal/`, `TTS_*` settings) | Unit: `test_agent_line_maps_all_four_agents`, `test_hi_agents_match_english_twins`, env example test. Integration: webhook stores `language`. Live: 3 Hindi web calls under 1 minute each, STT provider and voice recorded; go/no-go: agency and demand extracted correctly in at least 2 of 3, reply latency recorded, and a Hindi speaker the user names says the voice is understandable, else English only | Bolna Guardian HI agent create; up to 3 web calls; Hindi listener |
| S3 | Guardian verdict and family alert | A scam description gets "likely scam" and, within a minute, a Telegram message on the family member's phone and a flashing alert on the family page; a legit description sends no alert; Guardian HI says the same verdicts in Hindi. Builds `decide`, `sentence_for`, `alert_text`, migration 0003, the Telegram sender and the family page; removes the transfer tool from both Guardian agents | Unit: all `decide`, `sentence_for`, `alert_text` tests with branch mutations. Integration: alert on likely scam only, Telegram failure still answers, family link check. Live: 2 English role-play calls (1 scam, 1 legit) and 1 Hindi scam call, with alert timing recorded | Up to 5 test calls (2 transfer probes used); the user creates the Telegram bot; `FAMILY_LINK_TOKEN`, `TELEGRAM_*` set on Render; listener check of the changed likely-scam sentences |
| S4 | Ah Ma Bait with extraction and leak guard | A teammate scammer call, in English or Hindi, produces a script row and a draft report on the dashboard | Unit: extraction and all leak tests, including Hindi digit words, with self-test and mutations. Integration: stores script and draft, idempotent, flags leak. Live: `scripts/check.py bait` over 5 English scam fixtures, at least 4 payees and zero leaks; `scripts/check.py bait --language hi` over 2 Hindi fixtures, at least 1 payee and zero leaks | Bait EN and Bait HI agent create; 7 synthetic-caller web calls (5 English, 2 Hindi) within a $0.75 budget |
| S5 | Sophisticated verdict behind the tool, no calls | `curl` to the deployed `/tools/match-script` with each Guardian fixture's expected report returns its expected verdict; the paid courier report returns `urgent` with the bank and 1799 sentence, the family page shows the urgent alert and a Telegram message arrives; a friend-money report returns the call-back sentence. Builds `GuardianReport`, `parse_guardian_report`, the new `decide` branches, sentences in English and Hindi, `alert_text`, migration 0005, the new `match-script` fields with defaults, the family page's urgent state and warning signs, and the 15 Guardian fixtures in `seed/scripts.json`; keeps the 7-day count already built. Continues on `scamkaki/slice-5-guardian-loop`, brought up to date by merging `main` | Unit: every new `decide` branch with a mutation per branch, `test_decide_matches_every_guardian_fixture`, `test_guardian_fixtures_avoid_giveaway_words`, `test_parse_guardian_report_drops_unknown_tactics_and_defaults_acted`, act-now and call-back sentences in both languages, urgent alert text. Integration: new fields stored, missing fields default, urgent alerts first, 7-day count across languages, error returns unclear. Evidence: `curl` outputs for all 15 reports against Render, family page screenshot at phone width, Telegram screenshot | Re-authorization of S5 under this contract; migration 0005 on the Neon test branch, then production; push and fast-forward `main` so Render deploys. No Bolna calls and no agent updates |
| S6 | Guardian asks the new questions, live | A synthetic senior who trusts a telco caller that handed her to a MinLaw officer hears "likely scam" on a Guardian web call; the senior who already paid the courier fee hears the bank and 1799 instruction first and the family gets an urgent alert; the grandson case hears "call him back on the number you already have"; a fixture whose agency and demand Bait collected hears "same script heard N times this week". Builds both Guardian agent prompts (channel, three warning-sign questions, already-acted question, repeat-back) and tool params (`channel`, `tactics`, `acted`), synthetic-caller `senior_lines` clips for the 15 fixtures, and `check.py guardian` reading the new fields | Unit: `test_hi_agents_match_english_twins` with the new params. Probe first: 1 English call to show all five values reach the app; falsifier: values missing or garbled in the stored check, then stop and re-plan before the full run. Live: `scripts/check.py guardian` over 12 English fixtures, at least 7 of 8 scams and at most 1 of 4 legit flagged, the paid courier case urgent; `--language hi` over 3 Hindi fixtures, 2 of 2 scams, 0 of 1 legit, the paid case urgent; call length per case recorded against the 3-minute target; reruns reported as reruns | Guardian EN and HI agent updates on Bolna; 1 probe plus up to 15 calls and a budget, asked when S5 is done; Hindi listener check of the new sentences |
| S7 | Dashboard, report review and demo | Dashboard matches the Gate 1 mockups at phone and desktop widths, including the warning-signs column and the urgent result; "Mark reviewed" works on a report page; demo rehearsed 3 times; backup video recorded | Integration: review marks reviewed and sends nothing; dashboard lists warning signs. Evidence: screenshots, demo run log | Render warm-up or paid instance if cold starts break calls |

S2 needs S1; S3 needs S1; S4 needs S1, and its Hindi half needs S2's provider choice; S5 needs S3 and S4; S6 needs S5; S7 needs S6.
If S2 is no-go, the Hindi parts of S3, S4, S5 and S6 drop and those slices run English only.

## Execution and design amendment, user-directed 2026-10-28

S6's offline implementation is ready, but its live exit checks are unmet and further calls are
deferred for credit reasons. The user directed the order: prepare S7, finish S7, then plan an
appropriate S6 live-validation run with current costs. S7 can therefore be planned and, once
separately authorized, built on S6's offline work without claiming that S6 passed live.
The original S6 targets and failed attempt stay in the record. This is not an S6 closure.

S7 uses Claude's relevant design skills and the midnight blue, ice blue, electric blue and
chartreuse direction in Gate 1. Existing screen content, fixture labels and human report review
remain required. The S7 row above is otherwise unchanged.

After S7, the follow-up is a written S6 validation plan, not an automatic paid run. It covers
current account access and wallet, current billing units/rounding and model/provider prices,
probe-first stop conditions, essential cases, optional wider English/Hindi samples, a conservative
per-call ceiling and total cap, rerun treatment, human/listener availability and evidence limits.
The earlier US$0.8625 unspent S6 cap is historical context, not new authority to spend it.
No session mint, agent update, call, paid hosting, top-up or other charge follows from this plan.

S7 demo rehearsals and backup capture must not silently place new Bolna calls. Label fixture
walkthroughs and replays accurately; record an unavailable demo check instead of claiming it ran.
Preparing this handoff does not authorize S7 implementation, branch creation, commits or pushes.

## Never cut

S1, S3, S4's leak guard, S5's already-acted path and offline fixture check, and the fixture labels on every screen.

## Cut order (first cut first)

1. S7 polish beyond the mockups (keep "Mark reviewed" and fixture labels).
2. S6 Hindi live run: run English only and report Hindi as offline-checked only.
3. S6 English live run: reduce to 4 cases (2 scam including the paid courier case, 2 legit), reported as such.

## Stretch, not planned

Bait extracts warning signs so the 7-day count can match on tactics; Mandarin Guardian and Bait agents, only after S7 is done and once Bolna accepts `zh` speech-to-text; BothBosu offline check of `decide`; SIP trunk `Diversion` detection.

## Plan-wide rules

- No slice starts without your authorization by ID.
- Every pass rate is reported with its sample size, as fixture results.
- A failed live run keeps its evidence; reruns are reported as reruns.

## Website redesign slices, 2026-10-30

**Gate 4 amendment, APPROVED 2026-10-30.** Gate 1's eight-screen direction and Gates 2-4 are approved; the user requested
the latter three together. S8 was subsequently authorized for local implementation and named
test-branch checks on 2026-10-30, as recorded in 00-status.md. S9 was subsequently authorized
for the same isolated local/test scope on 2026-10-30. S10 local implementation/branch and named
test-branch scope were then authorized on 2026-10-30, conditional on S9 reaching main first.
S11 local implementation/branch and named isolated test scope were authorized 2026-10-30
in 00-status.md. S11 local exit is complete; its publication was separately authorized on
2026-10-30, with resulting refs verified after execution. S12 still needs per-slice authorization
and verified S11 content in main. Publication remains separately scoped in 00-status.md.
S1-S7 retain their historical contracts and evidence. S6 remains open for live proof; S7's
backup video and full live demo remain open. The redesign does not waive or rerun either.

### Build order and shared authority

[verified] Approved design: Build S8, S9, S10, S11, then S12 on the existing local S7 implementation.
These are offline UI slices, independent of S6's deferred live calls. Approval of this amendment
accepts that dependency order; it does not authorize any slice, call or spend.

Create `scamkaki/slice-<N>-<slug>` from the verified then-current tip of `main` before each
slice's first application edit. Per-slice implementation authority covers the required branch
and local code only. It must name permission for the existing destructive test-branch checks
if those are to run: migrations/truncation on the verified `TEST_DATABASE_URL` branch, fake
Bolna and Telegram, never production. No real sessions, calls, account changes or notifications.

The planning boundary was `scamkaki/gates-ui-redesign` at `154d1d7`, with approved documents
and previews uncommitted. The user later authorized their commit, main fast-forward and push
on 2026-10-30. These files are included in that publication package. Re-verify current refs
and tracked documents before S8; do not assume the pre-publication dirty state still applies.
Preserve any newly discovered dirty work and resolve its scope before editing.
Before each later slice, verify main includes its prerequisites. If it does not, stop for the
separately authorized commit/fast-forward step; do not silently stack branches or discard work.
Commit, main integration, push, deployment, installation and provider use need named authority.

Every slice delivers a reachable working page with synthetic fixture data and fake providers.
Keep navigation limited to implemented destinations. Original report/family URLs remain usable
throughout. On the Overview, show only implemented diagrams/links; never ship dead controls.
Every new list/detail handles its populated, empty/missing and unavailable states. S11/S12
include the actual asynchronous loading/error states for calls and family polling.

### S8: Reviewer workspace and records

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

### S9: Visual script patterns

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

### S10: Focused report review

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

### S11: Voice room

- **Branch:** `scamkaki/slice-11-voice-room`; depends on S8-S10 in main.
- **Visible result:** Voice room lets a reviewer select Guardian/Bait and English/Hindi, read the
  microphone/credit disclosure and explicitly start. Connection, hang-up and failure are clear.
- **Builds:** `/voice`, owning template/controller, existing pinned SDK and session endpoint.
  Move call UI/controller out of Overview. No agent, model, price, prompt, tool or transcript change.
  State machine and configured-agent availability follow Gate 3; no duplicated SDK/controller.
- **Assigned tests:** route auth and configuration handling; fake-provider session contract;
  offline controller explicit-start/one-at-a-time/end/error/late-event checks. Selection and page
  load counters must remain zero; Start increments exactly once under the fake SDK.
- **Evidence:** `evidence/s11-voice-room.md`; fake-provider browser connection lifecycle and
  offline checks, screenshots at both widths, SDK/controller guard mutation receipts. Run no
  real microphone/provider session to make this evidence.
- **Falsifiers:** session minted on load/selection/navigation; double click creates two sessions;
  selectors change during connection; stale events reset a newer call; hidden account credit use.
- **Exit decision:** local fake lifecycle passes. Actual provider audio/connection remains
  unverified by this slice; stop for S12 authorization.
- **Authorizations to request:** S11 local implementation/branch and named test-branch checks.
  Any real web call or microphone/provider validation needs a separate named scope and budget.

### S12: Family view and completed website flow

- **Branch:** `scamkaki/slice-12-family-ui`; depends on S8-S11 in main.
- **Visible result:** Family gets concise urgent guidance, expandable reasons and earlier
  alerts through the existing private link. All eight screen types work together with real
  stored fixture data, safe fake providers and the approved responsive design.
- **Builds:** standalone family restyle, safe renderer/state feedback and stale/empty handling.
  Retain five-second poll, 24-hour urgent-first order, opt-in sound, reduced-motion flashing,
  secret-link checks and response headers. No reviewer access or navigation is granted to family.
- **Assigned tests:** family link/list/order/header tests; offline renderer safe text, empty,
  stale/error and new-alert transitions. Browser walkthrough all eight screens, each verdict,
  urgent/non-urgent, Hindi, empty/error, keyboard focus, responsive overflow and query navigation.
  Verify the three Gate 1 tasks take at most two navigation actions from Overview.
- **Evidence:** `evidence/s12-family-ui.md`; genuine browser screenshots and request log against
  local synthetic fixtures, complete task walkthrough, full relevant suite and guard receipts.
  Record missing tooling or named assistive-technology/human checks as unavailable, never passed.
- **Falsifiers:** wrong/private link exposed; family sees non-likely-scam records; changed 24-hour
  ordering; a successful empty response leaves an old alert; failure masks stale data as fresh;
  user text becomes HTML; lost opt-in sound or reduced-motion behavior; broken path to any screen.
- **Exit decision:** redesign go only when its assigned tests and full fake-provider walkthrough
  pass. Human comprehension and S6 live efficacy remain distinct. This does not close S7's
  unrecorded backup video or unrun live demo.
- **Authorizations to request:** S12 local implementation/branch and named test-branch checks.
  Any user walkthrough, real-device/screen-reader check or recording is evidence only if performed.
  No recording install, outreach, commit, deployment or live call is implied.

### Never cut, cut order and completion

Keep fixture/no-fixture labeling, failed attempts, honest missing fields, independent call/check
records, warning/urgent meanings, auth, human report review and family isolation. Keep the eight
approved screen functions unless the user re-steers. The original never-cut S1-S7 rules persist.
Cut optional motion, extra decoration and duplicate explanatory copy before any functional
screen or safety/provenance requirement. Original live-validation sample cuts remain unchanged.

After each slice: fresh focused/full checks as appropriate, actual local page walkthrough,
evidence/status update and `architect-reviewer` post-slice cleanup. Preserve historical
mockups/evidence and in-scope dirty work; do not install or publish implicitly. Ask
`Continue to slice N+1, or re-steer?` using S9 after S8, S10 after S9, S11 after S10 and S12
after S11. There is no S13 plan. After S12, report the redesign result and remaining evidence
limits, then stop for the user's next instruction. A fresh-session continuation requires the
self-contained slice handoff specified in AGENTS.md.
