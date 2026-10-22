# AGENTS.md

Jaydon's Agentic Workflow plus the ground rules for running it in this repo. Copy this file to a project root and fill in the PROJECT section before the first real task. Skills named here are installed globally under `~/.agents/skills`; invoke them by name.

Depth scales with the task (see Three speeds), so this file is safe to load for any task size; the tier system keeps small tasks light. The Unattended operation rules apply only when I explicitly ask for a run with nobody watching.

---

## Jaydon's Agentic Workflow

### The four invariants (always on, every tier)

1. **Smallest complete change.** Run in `ponytail` mode for build sessions: solve the whole problem with the least new code, deletion beats addition, no unrequested abstractions, no "for later" code.
2. **Research before code when the path is unknown.** Map the territory before writing: `Explore`/workspace search for the repo, `how` for how a module works, `recall` for what was already done, `why` for why it is built this way, Tavily for external facts. When `trail status` shows a built map, `trail ask`, `trail callers`, and `trail skeleton` answer structural questions before broad exploration.
3. **Evidence before claims.** Run the real artifact and quote the output (`principle-prove-it-works`, `verification-before-completion`). "It compiles" is not done.
4. **One plan artifact per effort.** Never keep a second parallel document. The loop's plan feeds the gate doc; the gate doc is the plan.

### Three speeds

| Tier | Trigger | What runs |
|------|---------|-----------|
| T1 Trivial | One-liner, typo, revert | Invariants only. No loop. |
| T2 Task/slice | Multi-file, single concern | The full loop. Review ladder stops at baseline unless a lever fires. |
| T3 Project/major feature | Big diff, spans sessions, a build from scratch | The loop plus `software-factory` gates at three points: Product (before any code exists), Architecture, pre-merge. |

Gate protocol for T3: approvals are explicit and gate-scoped; a gate reopens if its document changes; mirrors stay in sync; approved documents merge to main.

### The loop

```
0. Research      only when the path is unknown (invariant 2)
1. Frame         `brainstorming` for creative/new work; `reality-check` for a new idea
2. Plan          `writing-plans` (task) or `figure-it-out` (big or ambiguous). One artifact.
3. Isolate       worktree or a branch named for the task
4. Red test      `test-driven-development` (default). Escape hatch: `tdd` when the test path is
                 integration-heavy; log a `shortcut:` comment naming the limit
5. Build         ponytail constraints + `typescript-best-practices` + boundary discipline at input edges
6. Fix breaks    `systematic-debugging` (reproduce first, fix the root cause) + `blast-radius` when shared code
7. Verify        run the real artifact, record the evidence; progress/decision log when multi-session
8. Review ladder `trail check` when the repo has learnings -> `ponytail-review` (baseline) -> `interrogate` (pre-merge, high stakes) -> `review-security` (auth/money/PII only)
9. Ship          `no-mistakes` -> `autopilot` -> `split-to-prs`, first available
10. Learn        `correct` after any repeated correction; `reflect` + `ponytail-debt` periodically;
                 `trail note` for durable repo decisions
```

### Escalation levers

The only things that move a task up: a one-way door or hard-to-reverse change; auth, money, or PII; shared code with other callers; work spanning sessions; correcting the agent twice for the same mistake. No lever, no escalation.

### Fan-out

When 2 or more independent seams exist, fan out with `dispatching-parallel-agents` or `swarm`, each worker in its own worktree. Use `arena` for design exploration. Never fan out across shared state; separate first and serialize only when one shared writer is a real invariant.

### Special cases

- **Big architecture change.** Spawn a dedicated architect agent (`create-subagent`); `architect` designs; `arena` settles one-way doors; `architecture-communicator` only when a human stakeholder needs the story. Findings become the Gate 2 doc (T3) or a decision note (T2).
- **Projects with their own pipeline.** An established project pipeline (for example, a slice build/review/ship flow) remains the executor for that project. This workflow adds only the research step when entering unfamiliar areas, `interrogate` before high-stakes merges, and `correct`/`reflect` at close.
- **Domain work.** The Neon stack, UI stack (`functional-ui`, `marketing-ui`, `clone`, `shadcn`, `gsap`), Tavily, and `canvas` plug in at Build and Verify.

### Toolchain readiness (check once per environment)

- `no-mistakes` needs a per-repo `init` and a runnable pipeline agent. If it is not available, the ship ladder falls through to `autopilot`; say so rather than skipping the gate silently.
- `interrogate` uses the reviewer models configured in `~/.agents/pstack-models.md`. Without that file it falls back to the parent model: still useful, less adversarial diversity.
- Default `ponytail` level: full.
- Trail-code is optional. `trail status` shows whether a map exists; `trail init --agents claude` runs once per repo. Hooks and statusline wire into Claude Code only, so in other harnesses use the CLI manually. Telemetry is anonymous with an opt-out. Skip it for small or one-off repos.

---

## Ground rules

### Starting or resuming

Before doing anything else:

1. Check for `PROGRESS.md`. If it exists with unchecked steps, this is a resumed run. Read it fully, trust it over your own memory and over any compaction summary, re-verify the last done step, and continue from the first unchecked step. Never redo finished steps or start over.
2. If it does not exist, write it with the goal in one line and a checklist of steps. Order steps by dependency, and among independent steps put the riskiest first so blockers surface early. Keep each step small enough to verify and commit on its own; split any step that would need more than a handful of file changes.
3. Run `git status`. If there are uncommitted changes you did not make, leave them alone, never stash or discard them, and note them in `PROGRESS.md`.
4. If you are on the default branch, create a branch named for the task and work there.
5. Run the full test suite once and record the baseline in `PROGRESS.md`, including which tests already fail. Those are not yours to fix. If the suite cannot run because a tool is missing, do not install it: record the missing tool and the exact install command in `PROGRESS.md` and continue without that check. I run installs.

### The progress file

`PROGRESS.md` is the only memory that survives compaction and restarts, and it doubles as the decision trail. Keep it accurate at all times.

- Checklist marks: `[ ]` not started, `[x]` done and verified, `[!]` blocked with a one-line reason.
- After each step, mark it and write the one or two facts the next step needs.
- Keep a dated run log: when the run started or resumed, the baseline, and each blocker.
- For multi-session or high-stakes work, keep one row per decision: what, why, evidence, result.
- Keep memory scopes separate: `PROGRESS.md` is this run's state, Trail learnings in `.trail/` are durable repo and team knowledge, and Qoder memory is personal cross-project preference. Do not duplicate an entry across them.
- Record every assumption, every problem noticed but not fixed, and every failure with the command and the last few lines of output.
- Record the exact commands used to verify each step so a person can rerun them.
- Before the final report, write a Result section: what was done, what was verified and how, what was left out and why.
- Update with small edits, never a full rewrite. Keep it under about 150 lines by condensing old entries. Never put secrets, tokens, or credentials in it.
- Commit `PROGRESS.md` only when I ask; otherwise it stays local.

### Verification

A step is done only when the project's own tests, build, and lint pass for it and the result matches what was asked.

- Never make a check pass by deleting a test, skipping it, weakening an assertion, loosening a type, or silencing a lint rule. If a test is wrong, say so in `PROGRESS.md` and leave it.
- Never edit CI config, lint config, or lockfiles unless the task is about them.
- If a test fails once and passes on rerun, note it as flaky and move on. Do not count a flaky pass as verification of your change.
- Run the full suite, not just the new tests, before marking the last step done. Compare against the baseline: any new failure is yours.
- The oracle is executed evidence. A second agent's opinion, a subagent report, or a self-report never counts as verification.

### When a step keeps failing

- Do not blind-retry. Reproduce the failure, trace it to the root cause, and fix it there (`systematic-debugging`).
- If two or more fixes that share one premise have failed the same gate, attack the premise before writing another fix (`principle-attack-the-premise`).
- After three rigorous attempts at the same failure, stop. Record the failure with output, mark the step `[!]`, and move to the next step that does not depend on it.
- Mark dependents of a blocked step `[!]` too, with the reason.
- If nothing independent remains, write the Result section and finish. A clear record of what is blocked is a valid outcome. Guessing past it is not.

### Keeping the context small

Context growth is what forces compaction, and compaction is where long runs lose track. Read and print only what you need.

- Read the parts of files you need, not whole files. Never output a file over a few hundred lines; use line ranges or grep.
- Tail logs and test output. Run tests in quiet mode. Never print dependency trees, lockfiles, binary files, or data dumps.
- Do not re-read a file you just edited to confirm the edit.
- Do not repeat back the plan or the progress file in your messages; it is already on disk.

### Commands that can hang

A command waiting for input never returns and the run dies silently.

- Never run interactive commands: editors, `git rebase -i`, `git add -p`, login flows, anything that prompts for confirmation.
- Pass non-interactive flags where they exist, set `CI=true`, and redirect stdin from `/dev/null` when unsure.
- Run servers, watchers, and anything long-lived in the background.

---

## Unattended operation

These rules activate only when I explicitly ask for a run with nobody watching. Interactive approval gates (T3) stay closed and recorded instead.

- Nobody is watching and questions will not be answered.
- If a step is covered by the original request and can be undone, do it without asking.
- If the request is ambiguous, pick the reading a careful colleague would pick, record the assumption in `PROGRESS.md`, and continue.
- If part of the request is impossible, harmful, or contradicted by the code, do every other part, record why that part was skipped, and finish.
- Do not stop because the session is long, the context was compacted, or a lot of work remains. Stop only at a hard stop or when every step is done or marked blocked.

---

## PROJECT

*(Fill in before the first task in a new project.)*

- Test / build / lint commands, and how to run them quiet and non-interactive:
- Default branch and branch naming:
- Gate artifacts for T3 (where the Product, Architecture, and pre-merge documents live):
- Authorization notes (what still needs separate approval from me):
- Evidence boundaries (what must never be claimed without proof):
