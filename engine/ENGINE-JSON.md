# Setting up `engine/engine.json`

`engine/engine.json` is the one configuration file of the Build Engine's planning tool (`engine/tools/plan_tool.py`).
It is a **seed file**: the release installer creates it once and never overwrites it, so your edits survive updates.
Version information lives separately in `engine/release.json` (managed; do not edit it).

This guide is written for the operator of this repository (`inscope-labs/castiel`, public, with the plans stored in the
same repository). It is local to this repository and is not part of the Build Engine release.

## 1. What to change first

A fresh install carries `OWNER/PROJECT` placeholders. Replace them, commit the file through a pull request, and leave
everything else at its default unless you have a reason.

| Key | Set it to | Why |
|---|---|---|
| `private_slug` | `inscope-labs/castiel` | Fallback owner/repo for context URLs when `context.target_base` / `context.plan_base` are empty. |
| `target.upstream_slug` | `inscope-labs/castiel` | The repository the deliverables are merged into. Informational (see section 3). |
| `target.base_branch`, `target.pr_base` | `main` | Branch deliverables are based on and pull requests target. Informational. |
| `branches.engine` | `main` | The branch that holds `engine/` and `plans/`. Informational. Was `build-engine` in the old private-repository layout. |
| `context.target_base` | `https://raw.githubusercontent.com/inscope-labs/castiel` | Where agents read the files a task needs. |
| `context.plan_base` | `https://raw.githubusercontent.com/inscope-labs/castiel` | Where agents read plan files. Same repository, so same value. |

Everything else (`report_headings`, `deny_in_task_branches`, `limits`, `halt_file`, `context.gateway*`) can stay as shipped.

### Resulting file for this repository

```json
{
  "private_slug": "inscope-labs/castiel",
  "target": {
    "upstream_slug": "inscope-labs/castiel",
    "base_branch": "main",
    "pr_base": "main"
  },
  "branches": {
    "engine": "main",
    "task_prefix": "task-"
  },
  "halt_file": "HALT",
  "report_headings": [
    "Summary", "Deliverables", "Acceptance", "Spec references",
    "Verification", "Files", "Deviations", "Findings", "Open questions"
  ],
  "deny_in_task_branches": ["engine/", "plans/", ".github/"],
  "limits": {
    "max_tasks_per_order": 5,
    "max_file_bytes": 1000000,
    "verify_timeout_seconds": 900,
    "max_open_orders": 0
  },
  "context": {
    "target_base": "https://raw.githubusercontent.com/inscope-labs/castiel",
    "plan_base": "https://raw.githubusercontent.com/inscope-labs/castiel",
    "gateway_template": "",
    "gateway": { "base": "", "kid": "k1", "ttl_seconds": 86400, "secret_env": "CTXGATE_SECRET" }
  }
}
```

This exact combination was checked: the plan validates, coverage passes, and a work order prints context links of the
form `https://raw.githubusercontent.com/inscope-labs/castiel/<commit>/<path>`.

## 2. Field reference

| Key | Default | Read by the tool? | Meaning and guidance |
|---|---|---|---|
| `private_slug` | placeholder | Yes (fallback) | `owner/repo` used to build context URLs when `target_base` or `plan_base` is empty. |
| `target.upstream_slug` | placeholder | No | Public upstream the deliverables go to. Kept for documentation and tooling around the engine. |
| `target.base_branch` | `main` | No | Branch deliverables are based on. |
| `target.pr_base` | `main` | No | Branch pull requests target. |
| `branches.engine` | `build-engine` | No | Branch holding the engine and plans. |
| `branches.task_prefix` | `task-` | Yes | Prefix of task branches. A task `10008-1-102-00` is worked on branch `task-10008-1-102-00`. Changing it changes every future order, so do not change it once work has started. |
| `halt_file` | `HALT` | Yes | Name of the stop marker. If a file with this name exists at the repository root (or `plans/<plan>/HALT`), the tool refuses to write plan state. |
| `report_headings` | nine headings | Yes | Headings every worker report must contain, in this order. They are printed in each order and checked on submissions. |
| `deny_in_task_branches` | `engine/`, `plans/`, `.github/` | Yes | A task may not name a deliverable under these prefixes (`check` fails if it does). Keep `engine/`, `plans/` and `.github/` listed so agents cannot alter the engine, the plan or workflows. Prefixes are plain strings, not patterns. |
| `limits.max_tasks_per_order` | `5` | Yes | Most tasks one work order may carry. |
| `limits.max_file_bytes` | `1000000` | Yes | Largest single file accepted in a submission. |
| `limits.verify_timeout_seconds` | `900` | Yes | Time allowed for each verification command. |
| `limits.max_open_orders` | `0` (no cap) | Yes | Cap on open work orders at once. A plan's own `max_open_orders` takes precedence. `0` means unlimited. |
| `context.target_base` | placeholder | Yes | Base URL for repository files. Links are `target_base/<pinned commit>/<path>`. |
| `context.plan_base` | placeholder | Yes | Base URL for plan files, formed the same way. |
| `context.gateway_template` | `""` | Yes | Advanced; leave empty. |
| `context.gateway.*` | empty `base` | Yes | Signed-link gateway settings. **Not available in 0.5.0**: no gateway is deployed. Leave `base` empty. |

"Read by the tool? No" means `plan_tool.py` and `cbridge` in release 0.5.0 never read the key; the values are still
required to describe the setup truthfully and are what `docs/TEMPLATE.md` tells you to set.

## 3. How context URLs work here

- `plan_tool.py order ... --target <checkout>` pins every URL to the **full commit id of that checkout's HEAD**. Branch
  names are rejected, so an order always reads exactly the files you saw.
- The commit must exist on GitHub, or the links will return 404. Push or merge first, then order against a checkout of
  the merged commit. The plan files must be on that commit too.
- `castiel` is public, so agents need no credentials to read these links. The printed order text still says "a private
  repository"; that wording is fixed in release 0.5.0 and is harmless here.
- Anything in a public repository is public, including the plan, its decisions and every work order file stored under
  `plans/<plan>/orders/`. Do not put secrets or private notes in the plan.

## 4. After editing: validate

Run these from the repository root. All must succeed before you commit.

```
python3 -m json.tool engine/engine.json > /dev/null
python3 engine/tools/plan_tool.py plans
python3 engine/tools/plan_tool.py check castiel-framework
python3 engine/tools/plan_tool.py render castiel-framework --check
python3 engine/tools/plan_tool.py coverage castiel-framework --fail --target .
python3 engine/tools/plan_tool.py order castiel-framework <task id> --target .
```

The last command prints a work order without writing anything (writing needs `--write`). Open one context link in a
browser or with `curl` after the commit is on GitHub to confirm it resolves.

## 5. Common mistakes

- Leaving `OWNER/PROJECT` anywhere. Search: `grep -rn "OWNER/PROJECT" engine operator`.
- Invalid JSON (trailing commas, comments). JSON allows neither.
- Putting a branch name instead of a commit id in a context URL. The tool refuses it.
- Removing `plans/` from `deny_in_task_branches`, which would let task branches edit the plan.
- Editing `engine/release.json` or other managed files: the next update reports a conflict.
- Expecting `target.*` or `branches.engine` to change behaviour in 0.5.0. They do not; the values only document the setup.

## 6. What this file does not configure

`operator/cbridge` has its own configuration at `~/.config/cbridge/config` (see `operator/cbridge.config.example`).
In release 0.5.0 `cbridge` assumes a split between a private repository and a public upstream and refuses to run
unless the private repository is confirmed private. Working directly in the public `castiel` repository does not fit
that flow, so do not rely on `cbridge upload`, `publish` or `reconcile` here until a release that supports a
single-repository layout. The planning commands above (`check`, `render`, `next`, `order`, `set`, `decide`,
`coverage`) work with this file alone.

## 7. Updating

Updates never overwrite `engine/engine.json`. If a new release adds keys, the release notes say so; add them by hand.
This guide is not managed by the release either, so keep it in step with the file when you change the setup.
