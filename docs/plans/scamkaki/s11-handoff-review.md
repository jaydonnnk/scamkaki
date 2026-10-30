# S11 handoff review prompt

Prepared 2026-10-30, Asia/Singapore. Review of handoff accuracy, not authorization to build S11.

```text
Review docs/plans/scamkaki/s11-handoff.md in /Users/jayd0/Desktop/bolna independently and
adversarially. Be unbiased, thorough and honest. Assume it may be wrong. Do not pass checks
for the sake of passing. Assess completeness and quality, weak assumptions and authority drift.

AGENTS.md's eight-section Slice handoff prompts and the current main-tip Gates 1-4 are the
standard. s8-handoff.md is the skeleton only. Confirm all S1-S12 slices, current status,
never-cut/cut order, S11-specific build sequence, exact copied S11 contract and S12 ownership.
The prompt's execution sequence is conditional, not a grant or a claim that S11 is built.

Re-verify branch/index/local main/remote main without exposing secrets. At preparation:
scamkaki/slice-10-report-review, HEAD/local main/remote main 6565bc40ae10c6d8d41a64739251c10e8b63ff8b,
empty index, dirty S10 source/tests/evidence/docs, no S11 branch. S9 is published. S10 remains
uncommitted and absent from main, so S11's S8-S10-in-main prerequisite is unmet. Its commit/
fast-forward, any push, S11 implementation and named destructive test checks need separate
authority. The latest user requested a handoff including slices/build plan, not implementation.

Verify source facts: /voice and its planned template/test/offline script are absent; existing
call UI/controller and pinned v3.0.1 SDK remain on Overview; POST /web-call/session keeps admin,
configuration and user_data behavior. preview_ui.py currently replaces the dashboard SDK and
its fake emits only error/end, so it cannot yet prove the proposed S11 lifecycle. No real
SDK/microphone/provider behavior is established by source inspection.

The retained S10 316-test/35-fault/17-screenshot results are prior S10 evidence, not fresh S11
checks. Their failures and auxiliary-review limits stay disclosed. The live synthetic preview
on 127.0.0.1:8783 is an inspection preview, with a verified listener at preparation; no concurrent
DB tests/reset are valid while it owns the test database. Its PID/session must be reverified.
No environment file was printed or hashed; no database/provider action prepared the handoff.

This is a read-only documentary review. Inspect actual Git/source/docs and retained records.
Fresh application tests or guard mutations, DB writes/resets, real sessions, credential use,
publication, installation, broad cleanup and later slices are not authorized by this prompt.
Flag unavailable verification rather than claiming it ran. Report PASS / ISSUES FOUND / FAIL
with exact file/line or concrete receipt per finding. Deliver your verdict and wait for instructions.
```
