# castiel-framework (plan 10008)

Completes the public `castiel` repository as an **abstract framework**: specifications only, no implementation
code. 125 tasks, 20 stages, 9 phases, 11 owner decisions. Generated views: `PLAN.md`, `CONCURRENCY.md`.

| Phase | Name | What it produces |
|---|---|---|
| 1 | Ground rules | clause-naming rules, terminology, classification, agent rules |
| 2 | Kernel foundations | canonical data model, trust/authority models, invariants, threats; bootstrap, crypto lifecycle, time, operating levels, extension model, security |
| 3 | System protocols | envelope model and catalog, identity, errors, policy, versioning; boot, session launch, authorization, work orders, agent interface, execution, verification, evidence |
| 4 | Cross-cutting and packaging | eight cross-cutting requirement areas; package framework incl. amk-core and session-memory |
| 5 | Component completion | resolves the open items of authority, console, controller + session-router, runtime, prompt |
| 6 | Implementation specification | contract, requirements, enforcement, platform abstraction, Basic/Standard/High profiles |
| 7 | Conformance | compliance model, taxonomy, declaration, harness interface, test vectors (prose), trust map, traceability, certification guidance |
| 8 | Reference material and governance | reference architecture, decisions, examples, five compliance mappings; governance, security, licensing |
| 9 | Integration and release | SSOT completion, defaults, clause index, neutrality audit, open-item reconciliation, cross-spec review, indexes, READMEs, versions, release |

Task ids follow `PLAN-PHASE-TASK-SUB` (`10008-5-102-00`: plan 10008, phase 5, stage 1, task 02, first version).
Every stage is a gate, so stages run in order; tasks inside a stage run concurrently where `CONCURRENCY.md` allows.

## Guarantees checked by `plan_tool.py`

- `coverage --fail`: every one of the 111 placeholder files in `amk/` and every open item (CORE, CNS, CTR, O-ATA,
  RTM, prompt) is cited by at least one task.
- `deliverable_patterns`: only `.md` files and the two plain-text version files can be deliverables; with
  `ALLOW_PATHS` set in the operator config, `cbridge publish` refuses anything else.
- Context is given as URLs into this repository (`castiel`), pinned to a full commit id; nothing is inlined. `engine/ENGINE-JSON.md` explains the settings that build them.

## Starting

1. Resolve the first decision: `python3 engine/tools/plan_tool.py decide castiel-framework D-01 --by <you> --notes "<prefixes>"`.
2. Configure `engine/engine.json` once (see `engine/ENGINE-JSON.md`) and keep a local checkout of `castiel` at the commit you order against: context URLs are pinned to that checkout's HEAD.
3. `python3 engine/tools/plan_tool.py next castiel-framework`, then
   `python3 engine/tools/plan_tool.py order castiel-framework <ids> --target ~/src/castiel --write --start`.

Decisions D-01 to D-11 are listed with their questions in `decisions.json`; only the tasks that cite a decision
wait on it. Operator tasks (licence text, merged-spec regeneration, release review) are never ordered.
