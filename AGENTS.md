# Repository and execution instructions

These reusable instructions govern communication, evidence, gates and execution.
The latest explicit user instruction overrides older notes.
Applicable runtime policies still apply.
Keep project scope and current state in the gate documents, not in this file.
The general agentic workflow (tiers, loop, escalation levers) lives in [docs/agentic-workflow.md](docs/agentic-workflow.md); this file wins where they differ.

## Project map

Scamkaki is a Bolna voice-agent project with two phone agents that feed each other.
Both run in English and in Hindi, one Bolna agent per language.
Ah Ma Bait answers scam calls as a Singapore auntie, stalls, and extracts the claimed agency, demand and payee details.
Ah Ma Guardian takes calls from seniors, compares what they heard with the scam scripts Bait collected, and hands risky cases to a family member.

| Path | Role |
|---|---|
| `AGENTS.md` | These rules |
| `PROGRESS.md` | Operational memory for long runs; never records a gate approval |
| `docs/plans/scamkaki/` | Gate folder: `00-status.md` (authority), `01-product.md`, `02-architecture.md`, `03-program-design.md`, `04-slices.md`, plus `checks/`, `evidence/`, `mockups/` |
| `docs/agentic-workflow.md` | Jaydon's Agentic Workflow (tiers, loop, ship ladder) |
| `outputs/`, `work/` | Pre-project research; historical context, not current scope |
| `src/scamkaki/app/` | HTTP surface: Bolna webhook, Bolna custom-function tool, dashboard |
| `src/scamkaki/domain/` | Pure logic: script matching, verdicts, extraction validation, leak guard, report drafts |
| `src/scamkaki/integrations/` | Bolna API client |
| `src/scamkaki/lib/` | Env loading, DB access, logging, ids, time |
| `agents/` | Bolna graph agent JSON exports (Bait and Guardian in English and Hindi), versioned |
| `migrations/` | Ordered SQL migrations for Neon Postgres |
| `seed/` | Labeled demo fixtures, including `seed/scripts.json` test cases |
| `scripts/` | Operator and check scripts, for example `scripts/check.py` for synthetic-caller fixture call results |
| `tests/unit/`, `tests/integration/`, `tests/e2e/`, `tests/support/` | Test tiers and shared fakes |
| `config/` | Tool configuration |

## Operating principles

- Honesty, accuracy and epistemic humility matter more than agreeableness.
  Never invent numbers, quotes, sources, test results, competitor behaviour or tool state.
- Label factual claims in planning, research and reviews: **[verified]** means supported by cited evidence; **[vendor claim]** means advertised but not independently validated; **[hypothesis]** means our judgment; **[unknown]** means not established.
  Preserve the distinction between evidence and interpretation.
- Lead with the answer.
  Be brief.
  Never open with praise, agreement or "great question", and never soften a critique with "but you're on the right track".
- Push back on weak logic.
  Lead with blockers, falsifiers, failure modes and uncertainty.
  Challenge non-trivial work for simplicity, coherence and evidence.
- Explain complex choices in short, concrete steps with low cognitive load.
  For layman or ADHD-friendly explanations, use the `layman-explain` skill at `~/.agents/skills/layman-explain/SKILL.md`: an everyday explanation, literal examples, scannable bullets or tables, and any concrete ask stated last.
  Label illustrative values; never invent a measurement to make an example work.
- Prefer the simplest complete solution.
  Find the root cause, change the narrowest responsible layer and avoid temporary fixes, unnecessary abstractions, dependencies and side effects.
- Do not use em dashes in new writing.
  Write `S1` or `Slice 1`, never a bare `S` when referring to a slice.
- Create visualization files as `.html`.

## Product hard rules

- Ah Ma Bait never speaks an NRIC, OTP, card number, password or real-looking bank or PayNow identifier.
  Asked for one, she stalls.
  A leak in any test call is a hard failure.
- No agent claims to be a government officer, police officer or bank employee.
- Scam reports are drafts.
  A human reviews every report before anything is sent to ScamShield, SPF or a bank; the code never files automatically.
- Seeded scripts, test callers and demo data are labeled fixtures in responses, the dashboard, evidence and videos.
  Never present synthetic-caller results as performance against real scammers.
- Seed scripts paraphrase public SPF advisories and stories; never copy victim names or identifying details.
- Guardian never tells a senior a call is safe as a certainty; its outputs are "likely scam", "unclear, talk to family" or "no scam signs found".

## Read order and authority

Before working, inspect the repository and read the existing task-relevant files:

1. Applicable `AGENTS.md` instructions and official buildathon requirements, if present.
2. The current supporting brief, including scope, evidence and unresolved risks.
3. `docs/plans/scamkaki/00-status.md` and every existing document in that gate folder.
4. Relevant research and decision records, including `outputs/` reports for background.
5. `tasks/lessons.md`, if present, for corrections relevant to this task.
6. Applicable skills.
   For gates, features, architecture, program design, slices or implementation, read `~/.agents/skills/software-factory/SKILL.md`.

- Approved gate documents supersede provisional supporting notes.
  When a durable decision changes, update every existing mirror that carries it in the same change.
- `00-status.md` is the authority for gate and slice state.
  `PROGRESS.md` is operational memory and may never record or imply a gate approval.
- Official rules and primary sources supersede stored summaries for time-sensitive external claims.
  Verify current access, capabilities and external state (Bolna features, model availability, numbers) before presenting them as current facts.
- A draft document, research result or review does not authorize a gate or an action.
  Never infer implementation, a later gate, installation, credentials or external service authorization from planning approval alone.
- Read the file map before assuming a document's role from its numbered filename.
  Treat historical inputs and superseded directions as context, not current scope.

## Software-factory workflow

Run the four gates separately: Product, Architecture, Program Design, then Vertical Slice Plan.
Workflow files live in `docs/plans/scamkaki/`; a supporting brief does not replace the gate documents.

- Obtain explicit approval at every gate.
  Resume from the first unapproved gate in `00-status.md`; do not redo an approved gate unless requested or invalidated by later evidence.
- Gate 1 covers the problem, measurable success metric, announcement and plain HTML screen mockups.
  Keep implementation choices out of it.
  Create one `.html` file per screen, with no framework or build step.
- At a required approval pause ask exactly: `Approve Gate N, or what should change?`, substituting the gate number.
  A review, critique or instruction to fix a draft does not itself approve the gate.
  Do not request approval again when it is already explicit in the current session.
- A change to an approved decision reopens the affected gate: update the document, set it to in progress in `00-status.md`, and obtain re-approval before dependent work continues.
  Recording approval or correcting wording without changing a decision does not itself reopen the gate.
- No application implementation begins before Gate 4 approval.
  Research, direction selection, context updates and evidence plans are not implementation approval.
  Time-boxed technical spikes (for example a voice provider spike) run only when the user authorizes them by name, live outside `src/`, and are recorded as evidence, not product code.
- Record approvals with dates and their limits in `00-status.md`.
  Update the gate line, applicable checklist, approval history and existing mirrors consistently.
  A stale or missing required mirror is a blocking finding.
- After Gate 4, implement one authorized vertical slice at a time.
  Each slice must produce a visible, working, testable result with recorded evidence.
  Do not build horizontal layers that cannot run end to end.
- After each slice, show the actual result, update `00-status.md`, and use the `architect-reviewer` skill in post-slice cleanup mode to check for stale or redundant files.
  Then ask `Continue to slice N+1, or re-steer?`, naming the next slice by its ID in the slice plan's build order.
- Whenever a slice will start or continue in a fresh session, write its handoff prompt as "Slice handoff prompts" below requires.
- Documentation-only maintenance and instruction consolidation do not create a new product gate when they do not change product behaviour or approved decisions.

## Execution discipline

- Inspect `git status` before editing.
  Treat existing changes as the user's work unless proven otherwise.
  Never stash, discard, rewrite or stage unrelated work.
- For non-trivial work outside the gate workflow, write a short actionable plan.
  Re-plan when evidence invalidates it.
  Skip ceremony for small, obvious changes.
- Establish a baseline proportional to risk.
  Documentation-only changes require documentary checks, not an application test suite.
- Keep changes inside the requested scope and preserve behaviour outside it.
  Once authority exists, fix in-scope bugs from logs, failing tests and reproducible evidence without requesting step-by-step guidance.
- After a correction, update the active plan and any in-scope durable record that would repeat the mistake.
  Do not widen the diff merely to document a correction.
- Do not install missing tools or dependencies without authorization.
  Report the unavailable check and provide complete manifests and exact commands when the user will perform the installation.
- Use subagents only when explicitly requested or permitted by applicable runtime instructions, for bounded independent tasks.
  A second LLM is not an independent oracle or the reviewer of record.
- Prefer non-interactive commands.
  Do not launch an editor, interactive rebase, login flow or confirmation prompt during an unattended run.
- On macOS, prefer `rg`, `uv run` for Python commands, and BSD-compatible `sed` flags; do not assume GNU tool behaviour.
- Do not change CI, lint configuration or lockfiles unless the task requires it.
- Never put secrets, tokens or credentials in repository notes, logs, fixtures, documentation, screenshots or commits.
  Architecture documents list environment variable names only.
  `.env.example` lists names only, never values.
  Deleting a published secret does not remove it from Git history; report the exposure and arrange authorized rotation.
- Placing real phone calls, buying numbers, spending Bolna or other cloud credit, and changing Bolna agents on a shared account are external actions.
  Request each by name unless the current slice authorization already covers it.

## Git discipline

- Create branches, commits, tags and pushes only within the user's authorization.
  Gate approval alone is not commit, push, publication or deployment approval.
  Never stage everything implicitly and never add a co-author trailer.
- Each implementation slice gets its own branch before its first edit, from the current tip of `main`.
  Confirm it with `git branch --show-current`.
  Do not begin slice work on `main` or continue on the previous slice's branch unless explicitly instructed otherwise.
- Use `scamkaki/slice-<N>-<slug>` by default, with a short descriptive slug (for example `scamkaki/slice-1-guardian-tracer`).
  When a branch covers only part of a slice, name the slug after the fixture or feature that part is about.
  Keep the name stable and record it in the slice's section of `00-status.md`.
- Authorization to implement a slice includes creating its required branch.
  It does not include pushing it.
  Do not create a branch for an unauthorized slice.
- Gate revisions and substantial reviews use descriptive `scamkaki/` branches under the same authorization rules.
  Small documentation maintenance does not require a new branch.
  Follow an explicit user request to work directly on `main`.
- Commit coherent concerns with messages stating what changed and why.
  Avoid generic messages such as "implement slice 1" for unrelated changes.
- On the user's instruction, integrate completed work using a fast-forward merge (`git merge --ff-only`).
  Keep the branch unless deletion is requested.
  Do not force-push or rewrite history without explicit authorization.
- Verify a requested push against the remote branch (`git ls-remote`), rather than assuming local tracking refs prove remote state.

## Verification and correction records

- Claim completion only after fresh evidence shows the result matches the request.
  Run relevant tests, lint, type checks or rendered-output checks in proportion to risk, and inspect the results before making a passing claim.
- Tests must detect broken behaviour.
  Never delete, skip, weaken or silence checks to obtain green output.
  Do not add tests that merely mirror the implementation.
- Prove guard coverage rather than counting test cases.
  Where guard coverage is claimed, mutate branches independently and demonstrate a failing check for each.
  A fault caught by two checks does not prove either check covers its own branch.
- For absence or leak assertions (for example Ah Ma never saying an NRIC or OTP), prove the scanner detects its needle on the actual serialized surface: the Bolna transcript and the extracted values as returned by the API.
  Use a representative injected self-test.
- Inventories describe structure, not coverage.
  A surface count does not prove any individual detection rule works.
- Explain invalid tests and preserve failure evidence.
  A fail followed by a pass on rerun is a flaky result, not clean proof from the rerun alone.
  Voice calls are nondeterministic: report pass rates over the named sample, never a single lucky run.
- During implementation, run focused checks while iterating and the relevant full suite before completion.
  Compare with the baseline and investigate new failures.
- Inspect the final diff for accidental scope, secrets, generated noise and line ending damage.
  Run `git diff --check`; inspect new untracked files separately.
- Report the actual URL and port for local previews.
  Inspect representative mobile and desktop views, rather than inferring rendered behaviour from CSS alone.
  Preview logs are scratch files, not product artifacts.
- Documentary consistency is part of completion.
  Mirror changed decisions in all existing status, brief, task and instruction files that carry them.
- If `tasks/lessons.md` exists, record material errors with what happened, root cause and a prevention rule.
  Do not create a generic lessons file just to expand the task.
  After four or more repetitions, propose a durable prevention rule; retain incident history unless its removal is requested.

## Long runs and recovery

Use these rules for explicitly unattended work or work likely to span compaction.

- If `PROGRESS.md` contains unfinished work, read it fully, re-verify the last completed step and resume from the first unchecked step.
  Do not restart finished work or prefer a compaction summary over the durable record.
- Otherwise create or extend a progress record with the goal, dependency-ordered checklist, dirty-worktree state and dated run log.
  Put risky independent checks early.
  Use `[ ]` for pending, `[x]` for verified and `[!]` for blocked with a reason.
- Keep the record around 150 lines by condensing old entries.
  Include assumptions, failures, exact verification commands, skipped scope and the result.
  Record facts needed to resume after verified steps and before compaction.
- Progress records cannot grant gate approval or Git authorization.
  Never commit them without authorization.
- Execute reversible steps covered by the request.
  Resolve harmless ambiguity with a stated reasonable assumption.
  Complete independent in-scope work when another part is impossible or blocked.
- Stop dependent work when required authority, credentials or a consequential decision is missing.
  Unattended mode does not widen authority for calls, spending, outreach, deployment, publication or gate approval.
  Honor existing authorization instead of requesting it again.
- After three materially different failed approaches to the same step, record the evidence and blocker, then continue independent work.
  If none remains, report the blocker instead of guessing or repeating unchanged attempts.
- Prefer targeted reads, `rg`, quiet checks and tailed logs after the required context pass.
  Avoid binary dumps, audio dumps, lockfile dumps and redundant full-file reads.
- Give concise milestone updates; do not paste the complete plan or progress log into chat.
- Run servers and watchers in controllable background sessions with captured logs.
  Record how to stop them; clean up when they are no longer needed.

## Context transfer

Use these rules to decide when to hand a session to a fresh chat.
The `transfer-context` skill produces the handoff and the independent review prompt.

- Transfer at roughly 50-70% of the context window.
  At 50%, start planning how to finish the task at hand and prepare for a handoff.
  Transfer before auto-compaction runs, because compaction is a lossy summary the user does not control.
- Prefer a clean boundary, whichever comes first: a finished slice, an approved gate or a merged branch.
- Transfer when the task changes to a new feature or a different area of the code.
- Transfer when degradation shows: re-reading files already read, contradicting earlier decisions, or retrying something that already failed.
- Transfer before a review.
  An independent reviewer works better in a fresh session.
- Do not transfer a small, tightly coupled change that is nearly done, or a debug loop in progress where the failed attempts are the useful context.

## Slice handoff prompts

A fresh session knows nothing about the project.
A copy-paste prompt that starts or continues a slice must therefore carry what the project is for and what the slice must deliver, not just a pointer to the documents.
Build the prompt from the gate documents at the current `main` tip and the actual repository state, never from memory or a chat summary.
It contains, in order:

1. **Project in brief.** From `01-product.md`: what the product is in two or three plain sentences; who the senior, the family member and the scammer are; the success target and whether it is tested; and the product hard rules above. State each gate's approval and date from `00-status.md`.
2. **Where this slice sits.** The whole build order by slice ID, which slices are done according to `00-status.md`, which are never cut, the cut order, and why this slice matters to the product goal.
3. **This slice's contract.** The slice's section from the slice plan, copied rather than paraphrased: visible result, builds, assigned tests, evidence, falsifiers, exit decision and the authorizations to request.
4. **Out of scope.** What the slice must not build because a later slice owns it, and cut or superseded scope that must not come back.
5. **Current state.** The branch to create or continue, the `main` SHA, which tools, accounts and credentials exist or are missing (Bolna, Neon, hosting), pending access checks and open user decisions, each labeled [verified] or [unknown] with its date.
6. **Authority.** The user's own words authorizing this slice, with the date, and every external action that must still be requested by name.
7. **Read first.** This file, the software-factory skill, `00-status.md`, the slice plan and the cited gate sections.
8. **Done means.** The slice's exit checks, the evidence to record in `00-status.md`, and the closing question `Continue to slice N+1, or re-steer?` naming the next slice by ID.

- Quote approved copy, names, numbers, error codes and test names exactly.
  Where the prompt and a gate document disagree, the gate document wins.
- Label claims as elsewhere in this file.
  Never present a plan, fixture, target or untested claim as built, measured or proven.
- Tell the receiving agent to re-verify Git and the files before acting, and to stop and ask instead of guessing when it finds a conflict with the prompt.
- Keep the prompt in one copy-pasteable block, with no secrets and no em dashes.

## Technology and proof boundaries

- Advertised capability is not working account access.
  Quotas, billing, regions, phone-number availability, permissions and integration availability remain unknown until verified.
- A Bolna changelog entry or doc page is a [vendor claim] until a call on our account shows the behaviour.
- Deterministic rules are not proof of correctness: they can act on a wrong input, such as a misheard transcript.
- Native platform use is not innovation by itself, and simulated integration does not prove real-world readiness.
- Keep fixtures and simulations visibly labeled through responses, evidence, screenshots, videos, metrics and UI.
  Never present them as live integrations, real scam interceptions, reviewed guidance or demonstrated outcomes.
- A passing static check, a regression suite or an LLM review supports only the claims it actually tests.
  It does not establish runtime, user, operational or domain safety without the corresponding evidence.
- Treat differentiation as a bounded hypothesis.
  Apate.ai already runs scam-baiting voice agents; no exact match in a bounded search does not prove uniqueness, and absent public documentation does not prove a competitor lacks a capability.
- Keep internal selection criteria separate from official requirements.
  Never present an internal taxonomy, planning score or conditional target as an earned result or an organizer's score.
- Sample size and uncertainty limit outcome claims.
  Report the evidence boundary rather than inferring broad safety or effectiveness from a small passing sample.
- Preserve closed directions as historical context.
  Do not resurrect superseded scope without an explicit user instruction.
