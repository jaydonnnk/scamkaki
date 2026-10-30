# S9 session transfer

Historical preparation snapshot. Later S9 publication and S10 local/test authority are recorded
in [00-status.md](00-status.md). Re-verify current Git prerequisites before execution.

Prepared 2026-10-30, Asia/Singapore. Background from actual S9 state, not execution instructions.
The retained skeleton is docs/plans/scamkaki/s8-handoff.md. Its historical authority does not apply.
The Envoi reference supplies structure only. Current authority is in 00-status.md.

```text
You are receiving background for Scamkaki S9 in /Users/jayd0/Desktop/bolna on macOS arm64.
Prepared 2026-10-30 from published main and actual working state. Gate documents win over this
prompt. Re-verification and the repository's slice-handoff rules govern any later work.

1. Project in brief

Scamkaki gives Singapore seniors English and Hindi Guardian phone lines to check suspicious
contact before moving money, or get guidance after acting. Likely-scam checks alert family
through Telegram and a private-link page. Bait stalls fictional scam callers and stores claimed
agency/request/payee details; a separate human reviewer reads draft reports.
The senior was contacted; the family member receives alerts and calls back; the fictional caller
may impersonate an agency, bank, courier, employer, investment group or relative. Reviewer and
family-link viewer remain separate roles.

Product targets, not real-world outcomes: family alert within 1 minute and callback before
money moves; EN Guardian at least 7/8 scams and at most 1/4 legit flagged; HI 2/2 scams and
0/1 legit; both already-acted courier cases urgent with bank guidance; every likely_scam alerts,
no other verdict does; EN Bait at least 4/5 planted payees, HI at least 1/2; zero leaks.
S6 live proof remains incomplete. Local fixture/UI checks do not establish efficacy or usability.
Bait never speaks an NRIC, OTP, card number, password or real-looking bank/PayNow identifier.
No agent claims to be a government, police or bank employee. Reports remain human-reviewed
drafts and are never automatically filed. Fixtures stay labeled; seed stories never copy victim
identities. Guardian never promises safety. Gates 1-4 remain APPROVED 2026-10-30 for redesign.

2. Where S9 sits

Build order: S1 tracer, S2 Hindi voice, S3 verdict/family alert, S4 Bait extraction/leak guard,
S5 sophisticated verdict, S6 live Guardian proof, S7 dashboard/review/demo, S8 reviewer records,
S9 script patterns, S10 focused report review, S11 voice room, S12 family/final checks.
S1-S5 are checked done; S6 live proof and S7 video/live demo remain open. S8 is published to
main. S9 is checked complete locally with a go decision after its acceptance checks and scoped
review. S9 remains uncommitted and unpublished. S10-S12 remain unstarted. Counts describe records, not unique
scammers, confirmed scams, accuracy or success. Differentiation remains a bounded hypothesis.
Never-cut behavior includes leak guards, already-acted guidance, auth, family isolation,
human review, independent calls/checks, fixture labels, failures and honest missing fields.
Optional motion, decoration and duplicate copy are cut before approved screen functions.
The original live cuts remain S7 polish, Hindi live, then four named English cases with disclosure.

3. S9 contract

Copied verbatim from published main's 04-slices.md, "### S9: Visual script patterns":

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

4. Out of scope

S10 owns /reports entry, focused review and acknowledgment. S11 owns /voice and the SDK move;
existing S7 voice controls remain on Overview. S12 owns family styling/polling repair.
Protected agents, seed meanings, domain verdict/extraction/leak/alert/report rules, migrations,
CI, manifests/lockfile, retained failed S6 records/audio and historical mockups remain intact.
No new languages, identities, embeddings, network tracking, automatic filing, installs,
production writes, provider/session/call, wallet check, Telegram message, spend or cleanup sweep.

5. Current state

[verified] Branch scamkaki/slice-9-script-patterns, HEAD/main 87739f0716da49641887401071cefae750696c98.
Remote main matched via ls-remote at the start. Index empty. All S9 work is uncommitted;
no integration/push/deployment. Inherited PROGRESS.md/status changes were extended; inherited
s9-handoff.md and s9-handoff-review.md remain byte-identical. Original snapshots are in ignored
work/scamkaki-s9/. No environment file was printed or hashed.

[verified] /patterns uses AdminDep, no-store, reviewer_page/reviewer_error and scripts_this_week.
The weekly SQL explicitly excludes Guardian parents, retains the seven-day script-age window
and combines EN/HI by agency/request. Overview uses the same source. Native details, numeric
bars and source-bound explanations work. Unknown labels are escaped consistently in both
weekly views. _matching.html is shared by Overview and Patterns; its nodes are vertical after
a cramped first desktop capture. Theme, shell/nav, dashboard, store and main.py changed.
New test_patterns.py plus auth/error matrix extensions preserve existing assertions.
preview_ui.py adds labeled synthetic groups; no production fallback or real SDK/provider.

[verified] Baseline 290 passed. Initial S9 red run 10 failed/10 passed, then 30 focused passed.
Preview fixture red 1 failed, then nine Patterns checks passed. Earlier full suite 302 passed.
An added Overview-hostile case reproduced blank labels, 1 failed/1 passed; fixed, then 20 focused
passed. Final full suite: 303 passed, one existing Starlette/httpx warning. Ruff check/format,
Node offline caller and diff checks passed. No dependency install.

[verified] First faults 24/24 caught; final 26/26 caught with exact source-byte restores.
Initial and final receipts remain. Failure-log URL representations were redacted; final fault
runner uses --tb=short and URL redaction. Claims cover named faults, not complete system coverage.

[verified] Actual fake-provider preview: http://127.0.0.1:8783/patterns, explicit test Settings.
Populated/empty/HTML 503 states at 1280x900 and 375x812, local Retry, Overview/nav links,
Tab/Enter focus and disclosures, Hindi and hostile stored text were checked. All measured
horizontal overflow was zero. Thirteen screenshots include two initial captures with stated
limits. Final six state screenshots are populated/empty/error at both widths. The scrolled
phone capture included an off-viewport skip-link artifact; final main captures start at top.
Control+Home was unavailable; navigation and scroll controls worked.
Previews were stopped with Ctrl-C: sessions 25489/PID 89570, 47107/PID 90535, 54558/PID 90629.
No listener remained before final tests; browser tab closed and viewport reset. Future PIDs
need fresh verification. Tests and preview resets ran sequentially.

[verified] Test endpoint was privately checked as distinct from production and connected.
Integration fixtures migrate/truncate that configured TEST_DATABASE_URL. A normal app launch
still uses DATABASE_URL and must not be treated as a test preview. Installed Python 3.12.15,
uv 0.13.0, Node v24.21.0 and existing libraries were used without installation.
[unknown] Live credentials, deployed revision, real voice, Telegram receipt, physical phones,
human comprehension, named assistive technology and CI. No such proof is claimed.

6. Authority

User on 2026-10-30: "please start", following the S9 background and the response awaiting S9
implementation and named test-branch authorization. The described S9 implementation/branch
and isolated TEST_DATABASE_URL migrations/truncation with fake Bolna/Telegram were authorized.
No production/provider action, calls, spend, installs, commit, main integration, push, deployment
or S10 work is authorized. The earlier S8 grant/publication applies only to that completed scope.

7. Read first

AGENTS.md, current 00-status.md and 01-product.md through 04-slices.md, PROGRESS.md,
evidence/s9-script-patterns.md, this transfer and s9-session-review.md. Paths above are under
docs/plans/scamkaki unless absolute. s8-handoff.md is the eight-section skeleton only.
Source under src/scamkaki/: app/main.py:381-395, app/templates/patterns.html:1-22,
app/templates/_matching.html:1-4, _reviewer.html:12, _theme.html:90-100 and dashboard.html:31-37;
domain/store.py:150-163 and unchanged labels in domain/verdict.py. Preview additions are
scripts/preview_ui.py:87-116. Tests: tests/integration/test_patterns.py:1-187, test_checks.py:79,
test_reviewer_errors.py:15-32 and existing dashboard checks. All paths are repository-relative.
Retained receipts are in work/scamkaki-s9/, screenshots in evidence/s9-screenshots/.

8. Done means

The assigned local acceptance checks, evidence and scoped architecture/UI review are complete.
Final documentary/protected-file audit passed. S9 is marked go for local completion. The fresh
read-only reviewer found no concrete S9 issue and performed no independent runtime checks. S10 is not
started and requires S9 in main plus separate authority. The exact closing question after S9
is "Continue to slice S10, or re-steer?". No real-world effectiveness claim follows from S9.

Wait for instructions before taking any action.
```
