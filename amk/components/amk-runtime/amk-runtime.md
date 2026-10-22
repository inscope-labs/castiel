# amk-runtime — Runtime Package Authority & Loader Specification

| Field | Value |
|---|---|
| Spec ID | `amk-runtime` |
| Version | 0.1.0-draft |
| Status | Draft — defines the runtime contract, the package format, and the runtime loader and package authority. Items that depend on unresolved review decisions are tracked in `99-open-items.md` as `RTM-O-nn` and referenced inline as "(see RTM-O-nn)". |
| Boundary | Runtime Package Authority & Loader. Defines what a runtime is, how a runtime package is identified, verified, loaded, included, retired and updated, and the contract a runtime must satisfy. |
| Trust | Trusted for package provenance, conformance verification and load integrity. Untrusted for operator authorization and for enforcement. |
| Normative language | MUST / MUST NOT / SHOULD / MAY as in RFC 2119. |

---

## Holistic System Overview

A runtime extends the kernel with capability. The kernel itself (the core OS/10 capabilities scaffolded by the kernel subtree) has no runtime. Everything beyond it, including the bundled system package `amk-core`, arrives as a runtime package.

The amk-runtime component is the single defined authority over **runtime packages**: what a package is, who signed it, whether it conforms to the protocol standards, and when and how its code is brought into execution. It is also the **loader**: the only means by which package code is placed into an execution context for a session.

It is deliberately **not** an authority over authorization or enforcement. The human operator, acting through the console, alone decides which packages are registered and which are included in a session. The controller alone enforces, issues capability tokens and holds state. The Attestation Authority alone issues role attestations. amk-runtime verifies and loads what those parties have already decided; it never decides for them.

Every runtime package, system packages included, must be downloaded and registered by the operator through the console, and its inclusion in a session must be authorized through the console. A console-signed pre-authorization may cover that inclusion where the console spec allows it (see RTM-O-04).

The specification is language-agnostic. Platform-specific loader implementations (for example sandboxed isolates on an edge platform) are described in companion implementation profiles, not here.

Three operational profiles (Basic, Standard, High) govern isolation, verification strength, and audit. Higher profiles subsume all requirements of lower profiles.

This document is an index. Normative requirements live in the module files listed below.

---

## Core Intent

*Informative overview. The normative module files remain authoritative wherever a requirement is already defined.*

- **Controlled integration, not sovereignty.** The runtime manages approved packages and their integration with AMK (discovery, verification, registration, loading, lifecycle, reporting). It implements only what the kernel and controller delegate, never overrides kernel invariants or grants permissions beyond its contract, and never lets convenience weaken a kernel-level check. A package cannot redefine the rules under which it is loaded or trusted, and logical boundaries stay explicit even when runtime and controller share a process or codebase.
- **Separate checks, never one vague "trust".** Provenance supports identity, integrity supports artifact validation, operator authorization permits an action, and enforcement constrains behavior. A package's self-description is not evidence of its identity or privileges, a valid hash or signature proves only what it is designed to prove, and neither proves approval, permission to load, or access to host resources. Unknown, untrusted, revoked, or unverifiable provenance takes the defined rejection or restricted path, and verification requirements are never silently downgraded.
- **Explicit, bound operator authorization.** Availability, verification, approval, registration, loading, and activation are distinct steps. Approval is explicit where required and bound to the package, version, scope, and action, so it never silently covers a different version, broader scope, or later action. Approval is never inferred from presence, a download, or a Host AI recommendation, and ambiguity takes the specified safe behavior.
- **Controlled, honest loading.** Loading happens only after identity, integrity, compatibility, registration, and authorization checks succeed, and only the artifacts the approved manifest selects are loaded, with substitution and time-of-check/time-of-use changes addressed by the integrity model. A partial load is never shown as activation, interrupted or failed loads have defined cleanup and rollback, and loading a package never authorizes every function it exposes.
- **Declared is not granted.** Packages, manifests, maps, prompts, and adapters may declare functionality but cannot self-authorize it. Capability requests are checked by the authoritative governance mechanism, map entries never override kernel invariants or controller policy, the controller alone decides whether a surface or capability is permitted, and privilege changes follow explicit policy and authorization. Signing keys and privileged credentials never reach the Host AI or package content.
- **Deterministic lifecycle, failure, and audit.** Lifecycle transitions (install, register, activate, deactivate, update, invalidate, remove) are explicit, preserve version history, and are recoverable or fail safely when interrupted. Updates re-verify and re-authorize, and rollback never silently restores a revoked or disallowed package. Mandatory check failures stop activation, outcomes are deterministic and distinguish integrity, authorization, compatibility, and operational errors, and audit records identify package, version, decision, and outcome without secrets. Status shown to the operator reflects authoritative results, with downloaded, verified, registered, loaded, active, failed, and rejected states kept distinct. Profiles state their formats, trust roots, verification, capability, and lifecycle rules, optional features never weaken mandatory checks, and conformance tests cover tampering, malformed manifests, stale approvals, revoked packages, dependency substitution, partial loads, and unauthorized capability requests.

**Essence:** the runtime brings verified packages into the system under controlled, bound authority; a package may declare what it offers but never decides what it is allowed to do.

---

## Reference ID Scheme

Every normative statement carries a stable identifier of the form:

**`RTM-<file>:<rule>`**

- `RTM` identifies this specification.
- `<file>` is the module file number (see table below).
- `<rule>` is the rule number inside that file. Each file begins numbering at 1.

Once published, an ID is never reassigned. A withdrawn requirement keeps its ID and is marked `RETIRED`.

---

## Module Index & File Numbers

| File # | File | Scope |
|--------|------|-------|
| 1 | [00-foundations.md](00-foundations.md) | Terms, role, authority limits, trust boundary, invariants |
| 2 | [01-package-format.md](01-package-format.md) | Package structure, manifest, identity, versioning, signatures |
| 3 | [02-contract.md](02-contract.md) | Runtime contract: in-band API, runtime map, channels, UI, errors |
| 4 | [03-lifecycle.md](03-lifecycle.md) | Registration, loading, inclusion, removal, update |
| 5 | [04-loader.md](04-loader.md) | Loader obligations: verification, load order, isolation, limits |
| 6 | [05-package-authority.md](05-package-authority.md) | Provenance, publishers, repositories, update flags, package revocation |
| 7 | [06-system-packages.md](06-system-packages.md) | System packages and `amk-core` |
| 8 | [07-profiles.md](07-profiles.md) | Basic / Standard / High profile requirements |
| 9 | [99-open-items.md](99-open-items.md) | Open questions and defaults needed (non-normative) |

---

## Relationship to Other Specifications

| Specification | Relationship |
|---|---|
| `amk-console` (`CNS`) | The console registers packages, converts a runtime map into a scoped subtree, decides inclusion, and signs every operator decision. amk-runtime never acts without a console-signed decision. |
| `amk-controller` (`CTR`) | The controller owns session state, builds the surface, issues capability tokens and invokes runtimes through the in-band API. The loader runs inside the controller release's trust domain (see RTM-O-01). |
| `amk-registry` / Attestation Authority (`ATA`) | Separate concern. The Authority issues role attestations to session participants; amk-runtime governs packages. Whether runtimes also receive role attestations is open (see RTM-O-16). |
| HTSM companion units | Define the Host AI traversal surface through which runtimes reach the Host AI. |

---

## Operational Profiles (Summary)

| Profile | Target | Verification keys | Isolation | Audit |
|---|---|---|---|---|
| **Basic** | Hobby / educational / prototypes | Software-protected | Soft isolation acceptable | Minimal |
| **Standard** | Production services | Non-exportable, OS keystore or equivalent | Per-runtime process, container or isolate; egress denied by default | Full signed load and lifecycle audit |
| **High** | Enterprise / regulated / high-assurance | HSM, secure element or TEE | Hardware-backed isolation; measured load | Hardware-protected audit; remote attestation of the loader SHOULD be supported |

Detailed obligations are defined in file 8.

---

## Errors, inconsistencies and critical deficiencies (cursory)

*Cursory pass only; a complete scan follows. It covered every module file of this specification at a skim level and checked the other four core specifications and `amk-ssot.md` only for references to the loader, in-band API, and package rules. IDs (`E-RTM-nn`) are provisional. **BLOCKING** means the item must be resolved before this specification can be released at the stated profile. Items already tracked as `RTM-O-nn` in `99-open-items.md` are not repeated unless their blocking status is itself inconsistent; that file records a draft position for each item but no blocking classification.*

### BASIC

- **E-RTM-01 (BLOCKING):** Each runtime runs in its own context sharing no memory, state, or authority (`RTM-5:10`, `RTM-5:12`, `RTM-1:15`, `RTM-3:22`), and the loader must sit behind an isolation boundary from controller enforcement logic (`RTM-5:2`). None of these carries a profile qualifier, yet Basic accepts "soft isolation" (`RTM-8:7`), which is never defined. As written, either those rules do not hold at Basic or Basic is non-conformant. Decide the minimum isolation Basic must keep.
- **E-RTM-02 (non-blocking):** Basic egress control "MAY be advisory, but undeclared egress MUST still be refused" (`RTM-8:8`), which is self-contradictory because advisory control cannot refuse. "Simplified mechanisms" for resource limits (`RTM-8:9`) are also undefined.

### STANDARD

- **E-RTM-03 (BLOCKING):** Key-protection requirements are aimed at the wrong keys. `RTM-8:6`, `RTM-8:11` and `RTM-8:16` require "verification keys" to be software, non-exportable (OS keystore), or HSM/TEE-protected, but verification keys are public, and the loader holds no signing key (`RTM-5:3`, `RTM-5:20`). What actually needs protection is the integrity of trust anchors (Release Key, registered publisher keys, package-hash records). Restate the requirement. Also affects HIGH.
- **E-RTM-04 (BLOCKING):** The loader must refuse withdrawn or revoked packages (`RTM-5:4`, `RTM-4:22`), but the source and freshness of withdrawal status are undefined (`RTM-O-09`), and no rule says what happens when status cannot be determined. This conflicts with Core Intent (unverifiable provenance takes the defined rejection or restricted path) and mirrors `E-ATA-01`. Also affects BASIC and HIGH.
- **E-RTM-05 (BLOCKING):** Several Standard MUSTs cannot be tested as written. The conformance rule set that both console and loader must apply (`RTM-6:13`, `RTM-6:14`, `RTM-O-08`) does not exist, and `RTM-5:4`'s pre-load verification list omits it although `RTM-6:14` requires it at load. Resource limits are mandatory (`RTM-5:14`), but their values are "defined only in the defaults manifest", which has been discontinued, so `DV-RTM-01` to `08` have no home. The package hash, manifest serialization, and error catalogue are also open (`RTM-O-12`, `RTM-O-13`). `RTM-O-08`, `O-09`, `O-12` and `O-13` need a blocking classification. Also affects HIGH.
- **E-RTM-06 (non-blocking):** Nothing requires that the bytes executed are the bytes verified. `RTM-5:4` verifies and `RTM-5:6` re-verifies cached copies, but there is no verify-then-load atomicity rule, which Core Intent expects for substitution and time-of-check/time-of-use changes. Also affects HIGH.

### HIGH

- **E-RTM-07 (BLOCKING):** High cannot be verified. Measured load and remote attestation of the loader are only SHOULD (`RTM-8:18`), profile discovery (`RTM-8:2`) relies on a status envelope with no behavioural rules, and, unlike the other core specifications (`CNS-7:23`, `CTR-8:22`, `ATA-06`), this specification has no peer profile rule at all.
- **E-RTM-08 (non-blocking):** A signed, complete, tamper-protected audit trail is required (`RTM-8:14`, `RTM-8:19`), but the loader must not write to the audit chain, which the controller records and signs (`RTM-5:20`, `CTR-7:4`). Assign the requirement to the controller, or define the integrity of loader-to-controller audit events.

### ALL PROFILES

- **E-RTM-09 (BLOCKING):** The loader is not reflected in the controller specification. The Release Manifest must pin the loader's identity and hash and list system packages with hashes and load order (`RTM-5:1`, `RTM-7:2`, `RTM-6:7`), but `CTR-2:2` lists neither. The controller spec defines no loader, no invocation of runtimes through the in-band API (`RTM-3:3`), and no audit events for package verification, load, include, or limit breaches (`CTR-7:6`). `RTM-O-01` also still assumes "exactly three components", whereas `amk-ssot.md` now defines five.
- **E-RTM-10 (non-blocking):** Registration obligations placed on the console (`RTM-4:4` to `RTM-4:8`, `RTM-6:5`, `RTM-6:6`) have no counterpart in the console specification, where runtime registration is simply console-local (`CNS-5:13`). The boundary of the "runtime" component is therefore spread across console and controller.
- **E-RTM-11 (non-blocking):** Core Intent expects lifecycle behavior that is not specified: no partial-load or interrupted-load state, no cleanup or rollback rule, no policy for failing to write a mandatory audit event, and no statement of who may clear `SUSPENDED` and how.
- **E-RTM-12 (non-blocking):** Stale or misleading references: `amk-defaults-manifest` (discontinued), `amk-registry` (now `amk-authority`), `ClarificationAnswer` and `CNS-3` (the envelope is discontinued), `RTM-2:4` pointing to `CTR-O-13` for risk classes (that item concerns envelope naming), and review IDs such as `CTR-14f` and `ATA-10` that match no current rule. The header table also lacks the suite-compatibility row used by the other specifications.
- **E-RTM-13 (non-blocking):** Several Core Intent points have no normative counterpart: conformance tests (tampering, malformed manifests, stale approvals, revoked packages, dependency substitution, partial loads, unauthorized capability requests), documentation of platform-specific constraints and unsupported behavior, and diagnostics that separate integrity, authorization, compatibility, and operational failures. `amk-test-matrix` is not yet updated.
