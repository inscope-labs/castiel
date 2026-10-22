# System Packages and amk-core

**File number:** 7  
**Overview.**  
This module defines the system package class and the rules for `amk-core`. System packages differ from third-party packages in provenance and load order, never in authority. The content of `amk-core` itself (its modules and tests) belongs to its own specification.

---

## System Package Class

- **RTM-7:1** A system package is shipped with an AMK release and signed by the Release Key.
- **RTM-7:2** Every system package MUST be listed in the Release Manifest by `package_id`, version and package hash, in the deterministic load order.
- **RTM-7:3** A system package follows the same contract (file 3), the same lifecycle (file 4) and the same loader obligations (file 5) as any other runtime.
- **RTM-7:4** A system package MUST NOT be granted any authority, privilege, risk class or level beyond those it declares and the controller and console grant. Class is not authority (RTM-1:7).
- **RTM-7:5** Every system package requires operator registration and console-authorized inclusion, exactly like a third-party package (RTM-4:24). Registration of the system packages is part of the console's first-run wizard.
- **RTM-7:6** Because system packages ship with a release, their versions change only with a new Release Manifest.

## Core Runtimes

- **RTM-7:7** A core runtime is a runtime available in every AMK release. A core runtime is a system package.
- **RTM-7:8** At least one core runtime MUST exist so that the system can be exercised end to end.
- **RTM-7:9** A runtime that is not part of every release, for example StepWise, is not a core runtime and is a third-party package.

## amk-core

- **RTM-7:10** `amk-core` is the bundled group of core runtime capabilities, loaded first (RTM-5:7).
- **RTM-7:11** `amk-core` is a system runtime. Its prompts scaffold through the kernel subtree, not through the controller. Authority rests with the console.
- **RTM-7:12** Where a system package scaffolds through the kernel subtree, its content is bound to the release: its package hash is covered by the Release Manifest, and changing it requires a new release.
- **RTM-7:13** Inclusion or removal of a system package that scaffolds through the kernel subtree is a change to the kernel subtree. It therefore takes effect only at a new session start and is never a mid-session inclusion (RTM-4:16, CTR-5:10). This is a draft position (see RTM-O-05).
- **RTM-7:14** The first tests of `amk-core` MUST exercise the kernel separation boundaries: a session with and without a runtime, and a runtime added and removed during an active session.

## Candidate First Module (non-normative)

- A host clarification module: a quiz-style UI shown to the operator for quick answers the Host AI needs, answered through the console (see `ClarificationAnswer`, CNS-3). Its definition belongs to the `amk-core` specification (see RTM-O-18).
