# Castiel — Pending Register

Work that is decided or requested but not yet done in this repository. It is the operator's to-do list: read it
before planning, and update it in the same pull request that changes an item's status. Defects found in the framework
specifications themselves belong in the specifications' own open-item lists, not here.

- Repository: `https://github.com/inscope-labs/castiel`
- Register created: 2026-10-29
- Local to this repository. It is not part of the Build Engine release and is never touched by the updater.
- Companion register for the engine: `docs/PENDING-REGISTER.md` in `inscope-labs/build-engine` (open as PR #30 at the
  time of writing).

## Rules

1. **One entry per piece of work.** IDs are `P-NNN`, assigned in order, never reused or renumbered.
2. **Statement first.** `Request` records what the operator asked for, as nearly as possible in their words, or says
   plainly that the entry was derived from a review. Everything else is analysis and may be corrected.
3. **Status words:** `OPEN` (accepted, not started), `IN PROGRESS` (a branch or PR exists; link it), `BLOCKED` (waiting on
   something named in the entry), `DONE` (merged; give the PR), `DROPPED` (operator decision; give date and reason).
4. **Priority is set by the operator.** `unassigned` means nobody has decided. Do not infer one.
5. **Done needs evidence:** the PR number and the check that proves the acceptance criteria. Move the entry to the
   Closed section.
6. **Specification content is not tracked here.** Writing the framework specifications is plan `castiel-framework`
   (`plans/castiel-framework/`); this register only tracks work around it.

## Summary

| ID | Title | Status | Priority | Blocked by |
|---|---|---|---|---|
| P-001 | Merge the castiel-framework plan and the `engine.json` guide | IN PROGRESS | unassigned | operator review of PR #3 |
| P-002 | Configure `engine/engine.json` and the operator config for this repository | OPEN | unassigned | none |
| P-003 | Repair the merge-spec workflows (paths point at a directory that does not exist) | OPEN | unassigned | none |
| P-004 | Execute plan 10008 (castiel-framework) | BLOCKED | unassigned | P-001, P-002, decisions D-01 to D-11 as each task needs them |
| P-005 | Confirm the repository setting the integration workflow needs | OPEN | unassigned | none |
| P-006 | Operator bridge (`cbridge`) cannot be used with a single public repository | BLOCKED | unassigned | build-engine register entry P-001 |
| P-007 | Retire the private `castiel-dev` repository | BLOCKED | unassigned | P-001 |

All entries below were derived from a review of this repository on 2026-10-29, not from individual operator requests,
except where the `Request` line says otherwise. Confirm or drop each one.

## Open entries

### P-001 — Merge the castiel-framework plan and the `engine.json` guide

- **Request:** Derived. The operator decided on 2026-10-29 to scaffold directly in this repository instead of through
  `castiel-dev`, and asked for the plan to be moved here and for an operator guide for `engine.json`.
- **Status:** IN PROGRESS: PR #3 (`plan/castiel-framework`), open, not merged.
- **What it contains:** `plans/castiel-framework/` (plan 10008: 125 tasks, 20 stages, 9 phases, 11 open decisions, none
  started), `plans/counter.json` (`next_plan_number: 10009`), `engine/ENGINE-JSON.md`.
- **Acceptance:** PR merged into `main`; `python3 engine/tools/plan_tool.py check castiel-framework` reports 0 errors,
  `render castiel-framework --check` reports the generated views current, and `coverage castiel-framework --fail
  --target .` passes.
- **Note:** this repository is public, so the plan, its decisions and any work orders are public once merged.

### P-002 — Configure `engine/engine.json` and the operator config for this repository

- **Request:** Derived. Release 0.5.0 installs `engine/engine.json` and `operator/cbridge.config.example` with
  `OWNER/PROJECT` placeholders (4 and 6 occurrences). They are seed files: updates never overwrite them, so only the
  operator can fill them in.
- **Status:** OPEN
- **Acceptance:** `grep -rn "OWNER/PROJECT" engine operator` finds nothing that the setup depends on; the values and
  validation commands in `engine/ENGINE-JSON.md` (from P-001) pass; a printed work order (no `--write`) shows context
  links of the form `https://raw.githubusercontent.com/inscope-labs/castiel/<commit>/<path>`.
- **Depends on:** the guide from P-001 for the recommended values. The operator config for `cbridge` is covered by P-006.

### P-003 — Repair the merge-spec workflows

- **Request:** Derived. The plan records the same fault as its decision D-03 and proposes "fix the paths by hand outside
  the plan, then regenerate", because workflows and tooling are code and the plan is Markdown-only.
- **Status:** OPEN
- **Evidence:** the five caller workflows (`merge-spec-amk-authority`, `-console`, `-controller`, `-prompt`,
  `-runtime`) pass `spec_dir: specs/core/amk-<name>`, and `merge-spec.yml` rejects anything not under
  `specs/core/amk-*`. There is no `specs/` directory; the component specs live under `amk/components/amk-<name>/`, where
  the five `*-spec-full.md` files also sit.
- **Consequence:** the workflows cannot succeed against the current layout, so the generated `*-spec-full.md` files cannot
  be regenerated by them.
- **Acceptance:** each caller points at an existing directory and the reusable workflow's path rule matches the layout;
  one run of each completes without error; the `*-spec-full.md` files are regenerated, not hand edited. The operator
  decides whether to fix or retire this tooling (decision D-03) before work starts.
- **Note:** `.github/` is a denied area for task branches, so this is operator work, not a plan task.

### P-005 — Confirm the repository setting the integration workflow needs

- **Request:** Derived. `.github/workflows/integrate-build-engine.yml` opens a draft pull request with the workflow
  token. That works only if the repository setting "Allow GitHub Actions to create and approve pull requests" is on.
  It could not be checked from the review tooling (settings need admin access).
- **Status:** OPEN
- **Acceptance:** setting confirmed on; one manual run of the workflow reports "nothing to do" while 0.5.0 is the latest
  release, or opens a draft PR when a higher release exists.
- **Reminder:** pull requests opened with the workflow token do not start the merge-spec workflows; run them yourself.

## Blocked entries

### P-004 — Execute plan 10008 (castiel-framework)

- **Request:** Derived from the operator's stated aim of building the framework directly in this repository.
- **Status:** BLOCKED
- **Blocked by:** P-001 (plan on `main`), P-002 (engine configured), and the owner decisions D-01 to D-11 in
  `plans/castiel-framework/decisions.json`. Only the tasks that cite a decision wait on it; for example task
  `10008-1-102-00` can be ordered first, whereas `10008-1-101-00` waits on D-01.
- **Open point:** `cbridge` cannot publish to this repository (P-006), so the route for turning a finished task into a
  pull request has to be decided first: manual, or another tool.
- **Acceptance:** per the plan: every task `done` with its pull request merged, `coverage --fail` passing, the plan's
  guarantees intact. Track progress in `plans/castiel-framework/PLAN.md`, not here.

### P-006 — Operator bridge (`cbridge`) cannot be used with a single public repository

- **Request:** Derived. In release 0.5.0 `cbridge` assumes a private working repository plus a public upstream and
  refuses to run unless the working repository is confirmed private. Plans now live in this public repository.
- **Status:** BLOCKED on `inscope-labs/build-engine` register entry P-001 (remove all references and constraints about
  the host repository's visibility), which is a change in a later release.
- **Until then:** use the planning commands that need no bridge (`check`, `render`, `next`, `order`, `set`, `decide`,
  `coverage`) and publish task work by hand. `engine/ENGINE-JSON.md` section 6 says the same.
- **Acceptance:** an installed engine release that runs `cbridge` against this repository without a privacy check; the
  integration workflow installs it; this entry closes.

### P-007 — Retire the private `castiel-dev` repository

- **Request (operator, 2026-10-29):** the private `castiel-dev` repository "will eventually be deleted".
- **Status:** BLOCKED on P-001. A review on 2026-10-29 found that the plan is the only content that must move; the rest is
  superseded by `build-engine` or already installed here.
- **Acceptance before deletion:** P-001 merged and the plan on `main`; `castiel-dev` still has only the `build-engine`
  branch at `88d77d5`, with no open pull requests or issues; the operator has checked its repository secrets, variables and
  webhooks, which the review could not read; deletion is done by the operator.

## Closed entries

None yet.

## Change log

| Date | Change |
|---|---|
| 2026-10-29 | Register created with P-001 to P-007, derived from the repository review. |
