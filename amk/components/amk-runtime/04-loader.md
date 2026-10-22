# Loader — Verification, Load Order, Isolation & Limits

**File number:** 5  
**Overview.**  
This module defines the obligations of the loader: what it verifies before any code runs, in what order packages load, how each runtime is isolated, and what limits apply. The loader is platform-agnostic here; implementation profiles describe concrete mechanisms.

---

## Placement

- **RTM-5:1** The loader is delivered as part of the controller release and is bound to the controller's trust root. Its identity and hash MUST be pinned in the Release Manifest (see RTM-O-01).
- **RTM-5:2** The loader MUST run behind an isolation boundary from the controller's enforcement logic. A fault or compromise inside a loaded runtime MUST NOT reach controller keys or enforcement state.
- **RTM-5:3** The loader MUST NOT hold console keys or operator credentials.

## Verification Before Load

- **RTM-5:4** Before executing any package code, the loader MUST verify, in this order:
  - the package hash matches the console-signed reference (RTM-4:10),
  - the manifest is self-consistent and every content digest matches,
  - the signature verifies against the correct key for the package class (Release Key for system, publisher key for third-party),
  - the contract version is supported,
  - the package is not `WITHDRAWN` or revoked (file 6),
  - the manifest's declared level, channels, egress and resources are acceptable under the session's kernel operating level and the loader's limits.
- **RTM-5:5** If any check fails, the loader MUST NOT execute the package, MUST report a standard error code to the controller, and MUST audit the failure.
- **RTM-5:6** The loader MUST NOT cache or reuse a package under any key other than its package hash. A cached copy MUST be re-verified on every load.

## Load Order

- **RTM-5:7** System packages load first, in the deterministic order fixed by the Release Manifest (file 7).
- **RTM-5:8** Third-party packages load after system packages, in the order selected by the console for the session.
- **RTM-5:9** Load order MUST NOT confer authority. A runtime loaded earlier has no privilege over one loaded later.

## Isolation

- **RTM-5:10** Each runtime executes in its own execution context, separate for each session. Contexts share no memory, state or authority (RTM-3:22, CTR-7:10).
- **RTM-5:11** Network egress from a runtime is denied by default. Only egress declared in the manifest and approved at inclusion is allowed (profile-dependent, file 8).
- **RTM-5:12** A runtime MUST NOT access controller storage, console storage, keys, or another runtime's context.
- **RTM-5:13** The loader mediates every call into and out of a runtime. A runtime has no direct handle to any other component.

## Resource Limits

- **RTM-5:14** The loader MUST enforce limits on CPU time, memory, package size, call duration and outbound calls for every runtime.
- **RTM-5:15** Limit values come from the defaults manifest (`DV-RTM-nn`, see file 9) and MAY be tightened per session by the controller. They MUST NOT be raised by a runtime.
- **RTM-5:16** A runtime that exceeds a limit MUST be stopped, and the event reported to the controller and audited.

## Failure Handling

- **RTM-5:17** The loader fails closed. A faulted runtime is moved to `SUSPENDED` for that session and its in-flight work ends with an error code.
- **RTM-5:18** A fault in one runtime MUST NOT halt another runtime or another session (CTR-2:7).

## Audit

- **RTM-5:19** The loader MUST emit audit events to the controller for: package verification results, load, include, remove, retire, limit breaches, faults, and rejected packages.
- **RTM-5:20** The loader MUST NOT write to the controller's audit chain directly. The controller records and signs audit entries (CTR-7:4).
