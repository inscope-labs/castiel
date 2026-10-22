# amk-console — User Control Plane Specification

| Field | Value |
|---|---|
| Spec ID | `amk-console` |
| Version | 2.1.0-draft |
| Suite compatibility | `OS10-AMK 2.x` (suite version defined in `amk-ssot.md`) |
| Status | Draft — self-contained, language-agnostic, envelope-only contract with three operational profiles. |
| Boundary | User Control Plane. Defines only the console’s interaction surface. |
| Trust | Trusted for authenticated operator intent. Untrusted for enforcement. |
| Normative language | MUST / MUST NOT / SHOULD / MAY as in RFC 2119. |

---

## Holistic System Overview

The amk-console is the sole seat of human operator authority. It is a self-contained component that communicates with external entities through signed envelopes; the sole exception is delivery of the session handoff to a Host AI (CNS-3:21). It has no knowledge of the internal behaviour of the controller, Host AI, runtimes, gateways, or any other counterpart; it only knows the envelope schemas, the cryptographic verification rules it must apply, and the sequencing obligations defined in this specification.

The console is trusted to capture and transmit authenticated operator intent. It is untrusted for enforcement: every action is submitted as a signed envelope that the receiving party alone enforces. Mutual verification is mandatory.

All external interactions are envelope-based, except handoff delivery (CNS-3:21). Local presentation, user-interface design, notification rendering, first-run experience, and operator-load timing are outside the scope of this specification and belong in an implementation guide.

The specification is language-agnostic. Implementations may be written in any language that can satisfy the cryptographic and sequencing requirements of the claimed operational profile.

Three operational profiles—Basic, Standard, and High—govern privacy, security, and implementation complexity. Higher profiles subsume all requirements of lower profiles.

Normative requirements live in the module files listed below.

---

## Core Intent

*Informative overview. The normative module files remain authoritative wherever a requirement is already defined.*

- **Request and visibility boundary, never enforcement.** The console conveys operator intent and presents verified outcomes; the controller alone evaluates policy and enforces. The console never claims success early: delivery, acceptance, and completion are distinct, no lifecycle transition is shown as done until the authoritative component acknowledges it, unknown state is shown as unknown (never inferred from cache or from the absence of a denial), and a denial is never relabeled as success.
- **Explicit, attributable operator intent.** Consequential actions require a clear operator instruction, under the applicable risk policy, that identifies the action and its material consequences. A missing, ambiguous, stale, or conflicting instruction, silence, UI focus, clipboard contents, model suggestions, or inferred preference is never approval. The console never fabricates consent or silently broadens the scope of an approved request.
- **The operator is not the Host AI.** The Host AI, tasks, adapters, packages, and untrusted input cannot impersonate the operator, and their content stays distinguishable from operator-authored commands and authoritative responses. Model output is never converted into consequential approval unless a separately governed feature allows it, Host AI claims are verified against the authoritative source where possible, and prompt instructions are never a security boundary.
- **Bound, verified, unforged messages.** All communication uses the defined envelopes, bound to operator, client, session, and protocol context, and is validated before it is shown as a trusted result. Unknown fields, unsupported versions, invalid signatures, replays, and malformed payloads follow explicit rejection rules; signed content is never altered; presentation metadata is never confused with signed fields. Private keys and reusable credentials never reach the Host AI or task content, and authentication never equals authorization.
- **Scoped lifecycle and registration.** The console exposes the defined session controls (initiate, inspect, pause, invalidate, halt) with enough visible state to prevent actions against the wrong session. Unsupported transitions are rejected rather than substituted, and permissions, confirmations, and stale state never carry into another session. Package discovery, download, or signature validity never authorizes loading or running a runtime, and failed or partial registration is never shown as inclusion.
- **Platform-independent, stable contract.** The interface may be graphical, command-line, mobile, or otherwise, but authority, confirmation, identity, and validation semantics are identical. Convenience features cannot weaken mandatory confirmation, profiles define supported operations, accessibility, credential handling, and failure presentation, and conformance tests cover spoofed requests, stale state, duplicates, denied actions, and interrupted transitions.

**Essence:** the console carries the operator's explicit, verifiable intent to the controller and shows only what the controller has confirmed; it never decides, enforces, or manufactures success.

---

## Reference ID Scheme

Every normative statement carries a stable identifier of the form:

**`CNS-<file>:<rule>`**

- `CNS` identifies this specification.
- `<file>` is the module file number (see table below).
- `<rule>` is the rule number inside that file. Each file begins numbering at 1.

Once published, an ID is never reassigned. A withdrawn requirement keeps its ID and is marked `RETIRED`. File numbers are stable identifiers and need not follow file-name order.

---

## Module Index & File Numbers

| File # | File | Scope |
|--------|------|-------|
| 1 | [00-foundations.md](00-foundations.md) | Terms, role, trust boundary, invariants |
| 2 | [01-keys-authentication.md](01-keys-authentication.md) | Key hierarchy and authentication requirements |
| 3 | [02-envelope-interface.md](02-envelope-interface.md) | Envelope catalogue and common rules |
| 4 | [03-session-lifecycle.md](03-session-lifecycle.md) | Session start, handoff, mid-session changes |
| 5 | [04-runtimes-work-preauth.md](04-runtimes-work-preauth.md) | Runtime registration, work orders, pre-authorization, Auto Assist |
| 6 | [05-validation-revocation.md](05-validation-revocation.md) | Validation gates, state rules, revocation, recovery |
| 7 | [06-profiles.md](06-profiles.md) | Basic / Standard / High profile requirements |
| 8 | [99-open-items.md](99-open-items.md) | Open questions (non-normative) |

---

## Operational Profiles (Summary)

| Profile | Target | Key Protection | Isolation | Confirmation | Audit |
|---|---|---|---|---|---|
| **Basic** | Hobby / educational / rapid prototypes | Software keys permitted | Soft isolation acceptable | Risk-based; some high-impact actions may use weaker confirmation | Minimal |
| **Standard** | Production services | Non-exportable keys; OS keystore or equivalent | Process / container isolation | Fresh confirmation for all high-impact actions | Full envelope audit trail |
| **High** | Enterprise / regulated / high-assurance | Hardware-backed or HSM; keys never in ordinary process memory | Strong isolation (TEE or equivalent) | Strict fresh confirmation + measured environment | Hardware-protected audit + remote attestation support |

Detailed obligations are defined in file 7.

---

## Errors, inconsistencies and critical deficiencies (cursory)

*Cursory pass only; a complete scan follows. It covered every module file of this specification, but only at a skim level, and did not cross-check against `amk-controller` or `session-router`. IDs (`E-CNS-nn`) are provisional. **BLOCKING** means the item must be resolved before this specification can be released at the stated profile. Items already tracked as `CNS-O-nn` in `99-open-items.md` are not repeated unless their blocking status is itself inconsistent; that file currently contains no blocking classification at all.*

### BASIC

- **E-CNS-01 (BLOCKING):** Fresh confirmation "MAY be relaxed for some high-impact actions" (`CNS-7:9`, `CNS-2:8`), and "some" is undefined. This conflicts with Core Intent (convenience must not weaken mandatory confirmation) and with the settled rule that session start, runtime registration, pre-authorization creation or change, and key or credential changes always require a fresh confirmation, whatever the profile or risk tier. The Basic relaxation needs an explicit, closed list that excludes those four.
- **E-CNS-02 (non-blocking):** Basic relaxations are undefined or collide with invariants that apply at every profile (`CNS-7:5`): "simplified" sequencing and replay protection (`CNS-7:8`, `CNS-3:9`, tracked only by `CNS-O-04`) versus `CNS-1:14` and the nonce rule `CNS-3:8`; software keys versus "protected key store" in `CNS-1:13`; "soft isolation" (`CNS-7:7`) is never defined, yet isolation from the Host AI underpins the Core Intent point that it cannot impersonate the operator.
- **E-CNS-03 (non-blocking):** Only Standard and High forbid logging the handoff in clear text (`CNS-4:9`). Under Basic the handoff, a reusable credential until expiry, may be logged.

### STANDARD

- **E-CNS-04 (BLOCKING):** The fresh-confirmation list (`CNS-2:7`, `CNS-7:15`) omits runtime registration and credential changes ("key changes" only) from the always-confirm set, and includes active-session revocation. Revocation is a protective action, so requiring biometric confirmation may delay it; confirm that is intended. Also affects HIGH.
- **E-CNS-05 (BLOCKING):** A covering pre-authorization lets the console emit `SurfaceAcceptance` without additional confirmation (`CNS-4:6`, `CNS-5:9`), while session start requires a fresh confirmation at Standard and High (`CNS-2:7`, `CNS-7:15`). The spec doesn't say whether confirmation is satisfied once, at pre-authorization creation, or is still needed at each session start. Also affects HIGH.
- **E-CNS-06 (BLOCKING):** Several Standard MUSTs cannot be tested as written: the required recovery protocol (`CNS-6:11`) does not exist (`CNS-O-03`), and sequencing, freshness, and replay protection (`CNS-7:14`, `CNS-3:7`, `CNS-3:9`) lack skew windows, nonce lifetime, and sequence storage (`CNS-O-04`) and envelope schemas (`CNS-O-01`). `CNS-O-01`, `O-03`, `O-04`, `O-08`, `O-09` and `O-13` need a blocking classification. Also affects HIGH.
- **E-CNS-07 (non-blocking):** The "complete audit trail of emitted and accepted envelopes" (`CNS-7:16`) conflicts with the ban on logging the handoff in clear text (`CNS-4:9`); no redaction rule is defined for audited secrets.

### HIGH

- **E-CNS-08 (BLOCKING):** High cannot be verified. Remote attestation is only SHOULD (`CNS-7:19`) although the overview table says "measured environment". Profile discovery (`CNS-7:2`) relies on `StatusResponse`, which has no behavioural rules (`CNS-O-12`), and the peer rule (`CNS-7:23`) trusts that self-declared profile, so a High claim is unverifiable.
- **E-CNS-09 (BLOCKING):** "Strict fresh confirmation" and "additional environmental checks may be required" (`CNS-7:20`) are undefined. High-impact actions are defined only by the `CNS-2:7` list, which is identical to Standard, so there is no testable difference between the two profiles.
- **E-CNS-10 (BLOCKING):** A tamper-protected, hardware-backed audit trail is a MUST (`CNS-7:21`), but audit content, format, and retention are defined nowhere and no open item tracks them.
- **E-CNS-11 (non-blocking):** `CNS-7:22` says side-channel resistance and high-assurance practices are "expected", which is not RFC 2119 language and is untestable.

### ALL PROFILES

- **E-CNS-12 (non-blocking):** `CNS-O-05` is still open although a pre-authorization is settled as one multi-scope envelope (`CNS-5:6` still says "a named scope"). `CNS-2:10`, `CNS-2:11` and `CNS-3:13` are "Duplicate of ..." stubs rather than `RETIRED`, which the ID scheme requires.
- **E-CNS-13 (non-blocking):** Several Core Intent points have no normative counterpart in the files checked: an outcome-state model that separates delivery, acceptance, and completion; a rule that model or Host AI output is never auto-converted into approval except under a pre-authorization; no carry-over of permissions, confirmations, or state across sessions; and conformance test coverage. The mechanism for certifiable structured output on all internal operations, needed because UI is out of scope, is also not yet specified.
